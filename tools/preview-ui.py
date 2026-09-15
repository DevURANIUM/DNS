"""Offline preview using real page renderers and disposable sample data.

Run python tools/preview-ui.py, then python -m http.server 8765 --bind
127.0.0.1 --directory docs/preview. Forms are preview-only.
"""
import importlib.machinery
import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    loader = importlib.machinery.SourceFileLoader(name, str(ROOT / 'templates' / name))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def main():
    admin, panel, sync = [load('smartdns-' + name) for name in ('admin', 'panel', 'sync')]
    target = ROOT / 'docs' / 'preview'
    target.mkdir(exist_ok=True)
    admin.CFG = {'ADMIN_PATH': 'preview'}
    sync.CFG = {'SELF_IP': '203.0.113.10', 'PANEL_DOMAIN': 'dns.example.com'}
    with tempfile.TemporaryDirectory() as temp:
        db = str(Path(temp) / 'preview.db')
        store = panel.Store(db)
        for index, (name, username, status) in enumerate([
            ('علی رضایی', 'ali_reza', 'active'), ('سارا احمدی', 'sara', 'pending'),
            ('کیان', 'kian', 'over_quota'), ('نیلوفر', 'niloufar', 'expired')], 1):
            store.db.execute('INSERT INTO users (id, first_name, username, status, created_at, quota_bytes, used_bytes) VALUES (?,?,?,?,?,?,?)',
                             (index, name, username, status, '2026-09-14T00:00:00+00:00', int(10.5 * admin.GB), index * admin.GB))
        store.db.commit()
        admin.STORE = admin.Store(db)
        handler = object.__new__(admin.Admin)
        customer = object.__new__(sync.UserPanel)
        customer.session = lambda: 'preview-only'
        customer.banner = lambda: ''
        customer.client_ip = lambda: '198.51.100.2'
        customer.send_html = lambda body, *args: sync.user_page(body)
        sync.post = lambda *args: {'ok': True, 'name': 'علی، خوش آمدید',
                                  'status': 'active', 'plan': 'ماهانه',
                                  'quota': 10 * admin.GB, 'used': 3 * admin.GB,
                                  'ip': '198.51.100.2', 'speed_kbps': 20000}
        pages = {'landing.html': sync.user_page(sync.landing()),
                 'user-login.html': sync.user_page(sync.login_form()),
                 'admin.html': admin.page('نمای کلی', handler.home(), admin.CFG),
                 'users.html': admin.page('مدیریت کاربران', handler.users(), admin.CFG, 'users'),
                 'login.html': admin.login_page(admin.CFG),
                 'signup.html': sync.user_page(sync.signup_form()),
                 'user.html': customer.dashboard()}
        for name, content in pages.items():
            # Preview must never submit administrative operations.
            content = content.replace('<form ', '<form onsubmit="event.preventDefault()" ')
            (target / name).write_text(content, encoding='utf-8')
        admin.STORE.db.close()
        store.db.close()
    print('Preview written to docs/preview')


if __name__ == '__main__':
    main()
