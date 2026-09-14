"""Protect plan editing against partial writes and invalid numeric input."""
import runpy
import tempfile
from pathlib import Path

load = runpy.run_path(str(Path(__file__).with_name('preview-ui.py')))['load']
admin, panel = load('smartdns-admin'), load('smartdns-panel')
with tempfile.TemporaryDirectory() as temp:
    db = str(Path(temp) / 'test.db')
    store = panel.Store(db)
    store.db.execute("INSERT INTO users(id,username,created_at,status,quota_bytes,used_bytes,warned,speed_kbps) VALUES(1,'test','2026-01-01','over_quota',?,?,3,1000)",
                     (int(10.5 * admin.GB), 11 * admin.GB))
    store.db.commit()
    admin.STORE = admin.Store(db)
    admin.CFG = {'ADMIN_PATH': 'test-path'}
    handler = object.__new__(admin.Admin)
    messages = []
    handler.redirect = messages.append
    before = dict(admin.STORE.one('SELECT * FROM users WHERE id=1'))
    invalid = [('quota_gb', '-1'), ('quota_gb', '-1e-100'), ('quota_gb', 'inf'),
               ('quota_gb', 'nan'), ('quota_gb', '1e40'), ('speed_mb', 'bad'),
               ('speed_mb', 'nan'), ('speed_mb', 'inf'), ('speed_mb', '-1'),
               ('speed_mb', '1e40'), ('days', 'bad'), ('days', 'nan'),
               ('days', 'inf'), ('days', '-1'), ('days', '1e20')]
    for field, value in invalid:
        params = {k: [v] for k, v in {'id': '1', 'quota_gb': '20', 'speed_mb': '5', 'days': '30'}.items()}
        params[field] = [value]
        handler.action('user-save', params)
        assert '!عدد' in messages[-1] or '!تعداد' in messages[-1], (field, value)
        assert dict(admin.STORE.one('SELECT * FROM users WHERE id=1')) == before, (field, value)
    assert "value='10.5'" in handler.users(), 'Fractional quota must survive rendering'
    handler.action('user-save', {k: [v] for k, v in {'id': '1', 'quota_gb': '10.5', 'speed_mb': '2.5', 'days': ''}.items()})
    saved = admin.STORE.one('SELECT * FROM users WHERE id=1')
    assert saved['quota_bytes'] == int(10.5 * admin.GB)
    assert saved['speed_kbps'] == 2500
    admin.STORE.db.close()
    store.db.close()
print('PASS: 15 invalid edits leave the complete account unchanged; fractional plans save correctly')
