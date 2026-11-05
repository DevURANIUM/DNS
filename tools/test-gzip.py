#!/usr/bin/env python3
"""Both panels send their pages compressed.

What has to hold: a browser that says it takes gzip gets a page a fraction of
its size, marked as such and with the length of what is actually sent; one
that does not gets the page as it is; and a file that is already packed - an
image, a font, a backup - or a page too small to matter is never wrapped.
"""
import gzip
import importlib.machinery
import importlib.util
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
fails = []


def check(label, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + label +
          ((" - " + detail) if detail and not cond else ""))
    if not cond:
        fails.append(label)


def load(path, mod):
    spec = importlib.util.spec_from_loader(
        mod, importlib.machinery.SourceFileLoader(mod, os.path.join(HERE, "..", path)))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


admin = load("templates/smartdns-admin", "admin")
sync = load("templates/smartdns-sync", "sync")


class Rec:
    def __init__(self, accept="gzip, deflate, br"):
        self.headers = {"Accept-Encoding": accept} if accept else {}
        self._headers_buffer = []
        self.sent = {}
        self.wfile = io.BytesIO()

    def send_response(self, code):
        self.sent["status"] = code

    def send_header(self, k, v):
        self.sent[k] = v

    def end_headers(self):
        pass


big = "<p>%s</p>" % ("سرویس فعال است " * 2000)
for name, send in (("admin panel", admin.Admin.send), ("customer panel", sync.UserPanel.send)):
    print("the " + name)
    Rec.send = send
    r = Rec()
    r.send(big, 200, {"Content-Type": "text/html; charset=utf-8"})
    body = r.wfile.getvalue()
    check("a page goes gzipped", r.sent.get("Content-Encoding") == "gzip"
          and r.sent.get("Vary") == "Accept-Encoding")
    check("  much smaller, and its length is what is sent",
          len(body) * 5 < len(big.encode()) and r.sent["Content-Length"] == str(len(body)))
    check("  and opens to the same page", gzip.decompress(body).decode() == big)
    r = Rec(accept="")
    r.send(big, 200, {"Content-Type": "text/html; charset=utf-8"})
    check("a browser that takes no gzip gets it plain",
          "Content-Encoding" not in r.sent and r.wfile.getvalue() == big.encode())
    r = Rec()
    r.send(b"\x89PNG" + b"\0" * 5000, 200, {"Content-Type": "image/png"})
    check("an image is left as it is", "Content-Encoding" not in r.sent)
    r = Rec()
    r.send("<p>ok</p>", 200, {"Content-Type": "text/html; charset=utf-8"})
    check("a tiny page is not worth wrapping", "Content-Encoding" not in r.sent)

print("the customer panel's own pages")
Rec.send_html = sync.UserPanel.send_html
r = Rec()
r.send_html(big)
check("go gzipped as well", r.sent.get("Content-Encoding") == "gzip"
      and r.sent["Content-Length"] == str(len(r.wfile.getvalue())))

print()
if fails:
    print("%d FAILED: %s" % (len(fails), ", ".join(fails)))
    sys.exit(1)
print("all checks passed")
