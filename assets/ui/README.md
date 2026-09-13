# Panel assets

Edit `panel.css` and `panel.js`, then run `python tools/build-installer.py`.
The build embeds these assets and the font in both Python templates and rebuilds
the standalone installer. No CDN, npm, pip, or runtime asset downloads are needed.
Do not edit the generated UI blocks in the templates manually.

Vazirmatn variable font, version 33.003, by Saber Rastikerdar:
https://github.com/rastikerdar/vazirmatn/tree/v33.003
Distributed under the SIL Open Font License; see `OFL.txt`.

Run `python tools/preview-ui.py` to generate disposable sample pages, then
`python -m http.server 8765 --bind 127.0.0.1 --directory docs/preview`.
The preview is static and uses sample data, not a deployed DNS service.
