"""Verify the shipped admin renderer, including duplicate and escaped names."""
import runpy
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
load = runpy.run_path(str(ROOT / 'tools' / 'preview-ui.py'))['load']
admin, panel = load('smartdns-admin'), load('smartdns-panel')
admin.CFG = {'ADMIN_PATH': 'test-only'}
with tempfile.TemporaryDirectory() as temp:
    path = str(Path(temp) / 'panel.db')
    store = panel.Store(path)
    store.db.execute("INSERT INTO users(id,username,first_name,created_at) VALUES(1,'amin','amin','2026-09-14')")
    store.db.commit()
    admin.STORE = admin.Store(path)
    handler = object.__new__(admin.Admin)
    for name in ('amin', ' AMIN ', '', 'Different name', '<script>name</script>'):
        admin.STORE.run('UPDATE users SET first_name=? WHERE id=1', (name,))
        rendered = handler.users()
        assert "class='username-badge'" in rendered
        assert '>amin</bdi>' in rendered
        assert "class='user-display-name'" not in rendered
        assert rendered.count('>amin</bdi>') == 1
        assert name not in rendered if name in ('Different name', '<script>name</script>') else True
    admin.STORE.run('UPDATE users SET username=? WHERE id=1', ('<script>name</script>',))
    rendered = handler.users()
    assert '&lt;script&gt;name&lt;/script&gt;' in rendered
    assert '<script>name</script>' not in rendered
    admin.STORE.db.close()
    store.db.close()

installer = (ROOT / 'dns.sh').read_text(encoding='utf-8')
source = (ROOT / 'templates' / 'smartdns-admin').read_text(encoding='utf-8').rstrip('\n')
assert '\n'.join('#' + line for line in source.split('\n')) in installer
print('PASS: only one green username badge, no secondary name; HTML escaped; installer matches source')
