"""Assemble dns.sh from the templates in this repo.

The installer has to be one self-contained file: someone who clones nothing and
downloads only dns.sh should get a working relay or exit. So every config
lives inside it, below `exit 0`, between markers that awk copies out.

Each payload line is prefixed with '#'. That is what keeps the whole file valid
bash, so `bash -n dns.sh` genuinely checks it - without the prefix, nginx
braces and dnsmasq syntax make the parser choke even though the data sits after
exit 0 and would never run. The alternative, base64, would pass the check too but
leave a reviewer unable to read the configs they are about to run as root.

This script is the single source of truth in the other direction: edit the files
under templates/ and common/, then re-run this to regenerate dns.sh.
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


PAYLOADS = [
    ("SYSCTL", "common/sysctl-tuning.conf"),
    ("SYSCTL_BBR", "common/sysctl-bbr.conf"),
    ("BYPASS", "common/bypass.conf"),
    ("NO_AAAA", "common/no-aaaa.conf"),
    ("EXIT_NGINX", "templates/config/exit-nginx.conf"),
    ("RELAY_NGINX", "templates/config/relay-nginx.conf"),
    ("TURNSERVER", "templates/config/turnserver.conf"),
    ("SMARTDNS", "templates/commands/smartdns"),
    ("NFTABLES", "templates/config/nftables-smartdns.conf"),
    ("SMARTDNS_ACL", "templates/commands/smartdns-acl"),
    ("SMARTDNS_SHAPE", "templates/commands/smartdns-shape"),
    ("ACL_SAVE_SERVICE", "templates/systemd/smartdns-acl-save.service"),
    ("ACL_SAVE_TIMER", "templates/systemd/smartdns-acl-save.timer"),
    ("PANEL", "templates/services/smartdns-panel"),
    ("PANEL_SERVICE", "templates/systemd/smartdns-panel.service"),
    ("SYNC", "templates/services/smartdns-sync"),
    ("SYNC_SERVICE", "templates/systemd/smartdns-sync.service"),
    ("DNS_PROFILE_UNIT", "templates/systemd/smartdns-dns@.service"),
    ("CERT", "templates/commands/smartdns-cert"),
    ("CERT_SERVICE", "templates/systemd/smartdns-cert.service"),
    ("CERT_TIMER", "templates/systemd/smartdns-cert.timer"),
    ("ADMIN", "templates/services/smartdns-admin"),
    ("ADMIN_SERVICE", "templates/systemd/smartdns-admin.service"),
    ("SMARTDNS_ACCESS", "templates/commands/smartdns-access"),
    ("SMARTDNS_LOGS", "templates/commands/smartdns-logs"),
    ("SMARTDNS_RULES", "templates/commands/smartdns-rules"),
    ("SMARTDNS_RESTART", "templates/commands/smartdns-restart"),
    ("EPIC_PIN", "templates/commands/epic-pin"),
    ("EPIC_PIN_SERVICE", "templates/systemd/epic-pin.service"),
    ("EPIC_PIN_TIMER", "templates/systemd/epic-pin.timer"),
    ("DOMAINS", "domains/domains.txt"),
    ("SERVICES", "domains/services.json"),
]


def main():
    # Keep both standalone templates and the downloadable installer in sync.
    import runpy
    runpy.run_path(os.path.join(ROOT, "tools", "build-ui.py"))["build"]()
    compile_routes = runpy.run_path(os.path.join(ROOT, "tools", "route-map.py"))["route_map"]
    http_routes = compile_routes(read("domains/domains.txt"))
    logic = read("tools/installer-logic.sh")
    parts = [logic, "", "# " + "=" * 68,
             "# Config payloads. Everything below is data, never executed.",
             "# " + "=" * 68, ""]
    for name, path in PAYLOADS:
        body = read(path)
        if name == "EXIT_NGINX":
            body = body.replace("__HTTP_ROUTE_MAP__", http_routes)
        # relay-nginx.conf carries MODULE_PATH; the installer fills it in after
        # writing, so normalise it to the same placeholder style as the rest.
        if name == "RELAY_NGINX":
            body = body.replace("load_module MODULE_PATH;",
                                "load_module __MODULE_PATH__;")
        if ("#__BEGIN_" in body or "#__END_" in body
                or "#__DOCTOR_DNS_COMPLETE__" in body):
            raise SystemExit("%s contains a payload marker" % path)
        parts.append("#__BEGIN_%s__" % name)
        commented = [("#" + line) for line in body.split("\n")]
        parts.append("\n".join(commented))
        parts.append("#__END_%s__" % name)
        parts.append("")

    # The very last line, and what the installer checks for before it does
    # anything: a download that stopped early ends somewhere else. One exact
    # line rather than "a terminator" - a cut can land on a middle payload's.
    parts.append("#__DOCTOR_DNS_COMPLETE__")
    parts.append("")

    text = "\n".join(parts)
    dest = os.path.join(ROOT, "dns.sh")
    with io.open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    os.chmod(dest, 0o755)
    print("wrote dns.sh: %d lines, %d KB, %d payloads"
          % (text.count("\n") + 1, len(text) // 1024, len(PAYLOADS)))


if __name__ == "__main__":
    main()
