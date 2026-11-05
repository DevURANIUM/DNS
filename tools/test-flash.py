#!/usr/bin/env python3
"""What an action did, shown on the next page - and never in the address.

What has to hold: after a save, the address the browser is sent to carries no
message (it used to end in ?m=%D8%A8..., which the address bar showed, history
kept and a reload repeated); the message rides in a cookie instead, the next
page shows it once and clears it, a refusal still reads as one, and a link
with ?m= in it prints nothing on either panel.
"""
import importlib.machinery
import importlib.util
import io
import os
import sys
import time
import urllib.parse

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
admin.log = sync.log = lambda *a, **k: None
admin.CFG = {"ADMIN_PATH": "p"}
admin.users_view = lambda handler: []


class Rec:
    """Enough of a request handler to answer once and keep what it sent."""

    def __init__(self, path="/", cookie=""):
        self.path = path
        self.headers = {"Cookie": cookie}
        self._headers_buffer = []
        self.sent = []
        self.wfile = io.BytesIO()

    def send_response(self, code):
        self.sent.append(("status", code))

    def send_header(self, k, v):
        self.sent.append((k, v))

    def end_headers(self):
        pass

    def header(self, name):
        return [v for k, v in self.sent if k == name]


print("the admin panel")
Rec.send = admin.Admin.send
Rec.redirect = admin.Admin.redirect
r = Rec()
r.redirect("users?m=!عدد سهمیه درست نیست")
loc = r.header("Location")[0]
check("the address carries no message", loc == "/p/users", loc)
cookie = r.header("Set-Cookie")[0]
check("it rides in a cookie, kept from scripts and other sites",
      cookie.startswith(admin.ADMIN_FLASH + "=") and "HttpOnly" in cookie
      and "SameSite=Strict" in cookie and "Max-Age=120" in cookie)
value = cookie.split(";", 1)[0].split("=", 1)[1]
check("readable once more on the next page, refusal and all",
      admin.flash_read({"Cookie": "sdns=x; " + admin.ADMIN_FLASH + "=" + value},
                       admin.ADMIN_FLASH) == "!عدد سهمیه درست نیست")
check("an address with other fields keeps them, without the message",
      (lambda r: (r.redirect("nodes?x=1&m=done"), r.header("Location")[0])[1])(Rec())
      == "/p/nodes?x=1")
check("the clearing cookie empties it",
      "Max-Age=0" in admin.flash_cookie(admin.ADMIN_FLASH, "", "Strict"))

print("the customer's panel")
Rec.send = sync.UserPanel.send
Rec.redirect = sync.UserPanel.redirect
Rec.banner = sync.UserPanel.banner
r = Rec()
r.redirect("/register-ip", "آی‌پی ثبت شد")
check("the address carries no message", r.header("Location") == ["/register-ip"],
      str(r.header("Location")))
cookie = r.header("Set-Cookie")[0]
check("it rides in a cookie", cookie.startswith(sync.USER_FLASH + "=") and "HttpOnly" in cookie)
value = cookie.split(";", 1)[0].split("=", 1)[1]
page = Rec("/register-ip", "sdu=s1; %s=%s" % (sync.USER_FLASH, value))
shown = page.banner()
check("the next page shows it", "آی‌پی ثبت شد" in shown and "msg good" in shown, shown)
page.send("x", 200, {})
check("  once: that page clears it", any(v.startswith(sync.USER_FLASH + "=;") and "Max-Age=0" in v
                                        for v in page.header("Set-Cookie")))
r = Rec()
r.redirect("/", "رمز اشتباه است", bad=True)
value = r.header("Set-Cookie")[0].split(";", 1)[0].split("=", 1)[1]
check("a refusal still reads as one",
      "msg err" in Rec("/", "%s=%s" % (sync.USER_FLASH, value)).banner())
check("a link with ?m= in it prints nothing",
      Rec("/?m=" + urllib.parse.quote("پیام جعلی")).banner() == "")
Rec.send_html = sync.UserPanel.send_html
page = Rec("/", "%s=%s" % (sync.USER_FLASH, value))
page.send_html(page.banner())
check("a whole page clears it too, not only a bare reply",
      any(v.startswith(sync.USER_FLASH + "=;") for v in page.header("Set-Cookie")))

print()
if fails:
    print("%d FAILED: %s" % (len(fails), ", ".join(fails)))
    sys.exit(1)
print("all checks passed")
