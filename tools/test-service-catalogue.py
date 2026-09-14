"""Catalogue invariants and actual route selection against a disposable DB."""
import json
import re
import runpy
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
load = runpy.run_path(str(ROOT / 'tools' / 'preview-ui.py'))['load']
panel = load('smartdns-panel')
catalogue = json.loads((ROOT / 'domains' / 'services.json').read_text(encoding='utf-8'))['services']
owners = {}
keys = set()
for service in catalogue:
    assert service['key'] not in keys
    keys.add(service['key'])
    for group in service['groups']:
        for domain in group['domains']:
            assert re.fullmatch(r'(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}', domain), domain
            assert domain not in owners, (domain, owners.get(domain))
            owners[domain] = (service['key'], group['key'])
assert {'cs2', 'youtube', 'marvelrivals', 'deltaforce', 'embark'} <= keys
assert owners['callofduty.com'] == ('blizzard', 'main')
assert owners['steampowered.com'] == ('steam', 'main')
with tempfile.TemporaryDirectory() as temp:
    store = panel.Store(str(Path(temp) / 'test.db'))
    default = store.ensure_default_template(catalogue)
    # Use the real schema and persisted choices, not a mirrored routing algorithm.
    store.db.execute("INSERT INTO templates(id,name,is_default,created_at) VALUES(999,'YouTube only',0,'2026-09-14')")
    store.db.execute("INSERT INTO template_services(template_id,service_key,group_key) VALUES(999,'youtube','main')")
    store.db.commit()
    routed = store.routed_for(999, catalogue)
    bypass = store.bypass_for(999, catalogue)
    assert 'youtube.com' in routed and 'googlevideo.com' in routed
    assert 'counter-strike.net' in bypass and 'callofduty.com' in bypass
    assert not set(routed).intersection(bypass)
    default_row = store.one('SELECT id FROM templates WHERE is_default=1')
    for service in catalogue:
        for group in service['groups']:
            if group.get('opt_in'):
                assert not set(group['domains']).intersection(store.routed_for(default_row['id'], catalogue))
    store.db.close()
print('PASS: unique domains, stable existing keys, isolated YouTube routes and opt-in protections')
