"""Embed local UI assets; deployed templates remain standard-library-only."""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def build():
    assets = ROOT / 'assets' / 'ui'
    font = base64.b64encode((assets / 'Vazirmatn.woff2').read_bytes()).decode('ascii')
    css = ('/* Vazirmatn v33.003 — https://github.com/rastikerdar/vazirmatn\n'
           + (assets / 'OFL.txt').read_text(encoding='utf-8') + '\n*/\n'
           + '@font-face{font-family:Vazirmatn;font-style:normal;font-weight:100 900;'
           'font-display:swap;src:url(data:font/woff2;base64,' + font + ') format("woff2")}\n'
           + (assets / 'panel.css').read_text(encoding='utf-8'))
    script = '<script>' + (assets / 'panel.js').read_text(encoding='utf-8') + '</script>'
    for name, variable in [('smartdns-admin', 'CSS'), ('smartdns-sync', 'USER_CSS')]:
        path = ROOT / 'templates' / name
        text = path.read_text(encoding='utf-8')
        start = text.index('# BEGIN GENERATED UI')
        end = text.index('# END GENERATED UI', start) + len('# END GENERATED UI')
        block = '# BEGIN GENERATED UI — run tools/build-ui.py\n'
        block += variable + ' += ' + repr(css) + '\nUI_SCRIPT = ' + repr(script)
        block += '\n# END GENERATED UI'
        path.write_text(text[:start] + block + text[end:], encoding='utf-8', newline='\n')


if __name__ == '__main__':
    build()
