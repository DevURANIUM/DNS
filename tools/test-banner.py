#!/usr/bin/env python3
"""The installer opens with its name, large.

What has to hold: before anything else - root or not - an install, an
upgrade or an uninstall shows DNS in block letters and the version, narrow
enough for any terminal, shaded on a terminal and plain in a log; --version
and --help print only what a script asking wants.
"""
import os
import re
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
fails = []


def check(label, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + label +
          ((" - " + str(detail)[:400]) if detail and not cond else ""))
    if not cond:
        fails.append(label)


with open(os.path.join(ROOT, "tools", "installer-logic.sh"), encoding="utf-8") as fh:
    logic = fh.read()
body = logic[logic.index("banner() {"):logic.index("\n}\n", logic.index("banner() {"))]
rows = re.findall(r"^\s+'(  [^']*)'", body, re.M)
check("six rows of block letters, inside 80 columns",
      len(rows) == 6 and max(len(r) for r in rows) <= 80, rows)
check("in block letters", all("█" in r or "╚" in r for r in rows) and sum("█" in r for r in rows) == 5)
check("the name is DNS alone", "DOCTOR" not in body.upper().replace("DNS", ""))
check("shaded on a terminal, row by row, and plain in a log",
      "[ -t 1 ]" in body and "38;5;%sm" in body and len(re.findall(r"\d+", body[body.index("tint=("):body.index(")", body.index("tint=("))])) == 6)
check("the version beneath", '"$VERSION"' in body and "smart DNS for Iran" in body)
check("before the preflight, so even a run without root shows it",
      logic.index('case "${1:-}" in -V|--version|-h|--help) ;; *) banner ;; esac')
      < logic.index("# ---------------------------------------------------------------- preflight")
      < logic.index('[ "$(id -u)" = 0 ] || die "run as root'))
check("  and after --version and --help are answered, which print only themselves",
      logic.index("--version|-V) printf '%s\\n' \"$VERSION\"; exit 0 ;;")
      < logic.index("banner() {"))

bash = shutil.which("bash")
if bash:
    script = "VERSION=9.9.9\nB=\n" + body + "\n}\nbanner\n"
    for cols, lines in (("120", 6), ("80", 6)):
        r = subprocess.run([bash, "-c", script], capture_output=True, text=True, encoding="utf-8",
                           env=dict(os.environ, COLUMNS=cols))
        drawn = [l for l in r.stdout.splitlines() if "█" in l or "╚" in l]
        check("at %s columns it draws %d rows" % (cols, lines), len(drawn) == lines
              and "version 9.9.9" in r.stdout, r.stdout[-300:] + r.stderr)

print()
print("%d FAILED: %s" % (len(fails), "; ".join(fails)) if fails else "all checks passed")
sys.exit(1 if fails else 0)
