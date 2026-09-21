# DNS

A self-hosted Smart DNS service with user accounts, traffic quotas, service templates and Persian web panels.

[Repository](https://github.com/DevURANIUM/DNS) · [Report an issue](https://github.com/DevURANIUM/DNS/issues) · [راهنمای فارسی](README.fa.md)

## How it works

Deploy a relay in Iran and an exit server abroad. The relay answers selected domain names with its own address and forwards their connections through the exit. Other domains resolve normally. HTTPS routing reads SNI without decrypting TLS traffic.

```text
Client → Relay → Exit → Destination
           │      │
     User panel   Admin panel + SQLite
           └──────┘
       Sync every 30 seconds
```

Accounts and usage live in a central database on the exit. Relays send usage and fetch access rules. This is domain-based routing, not a general-purpose VPN.

## Features

- **Administration:** users, fractional quotas, download limits, expiry dates, service templates and domain rules.
- **User accounts:** signup, login, IP registration, usage, password changes.
- **Redesigned panels:** Persian RTL layout, responsive pages, local Vazirmatn font and persistent light/dark themes for users.
- **Panel tools:** Persian table search, status filters, result counts and an overview of accounts needing attention.
- **Connection setup:** DNS copy button, setup guide and password visibility controls.
- **Access control:** per-IP allowlists and traffic accounting through nftables, quota enforcement and monthly or one-time allowances.
- **Operations:** host monitoring, logs, backup/restore and TLS certificate provisioning and renewal.

UI assets and fonts are embedded in the installer; the panels do not depend on a CDN. Signup creates a pending account. An operator must save a plan before access is activated.

## Services and templates

The current catalogue contains **123 service entries and 6808 domain entries**.
The September 16 expansion adds 49 service entries and 1188 domains while keeping existing
service and group identifiers intact.

| Category | Examples |
| --- | --- |
| Games and platforms | Call of Duty / Warzone, CS2, Dota 2, Valorant, Steam, Epic, PlayStation, Xbox |
| More games | Marvel Rivals, Delta Force, ARC Raiders, THE FINALS, Fortnite, Rocket League, Fall Guys, Path of Exile, PUBG Mobile |
| Video and music | YouTube / YouTube Music, Netflix, Twitch, Spotify, Vimeo, SoundCloud |
| Communication and storage | Discord, Telegram Web, Signal website/downloads, Proton, Dropbox |
| Learning and browsing | Wikipedia, Internet Archive, Duolingo, DeepL, Reddit, Pinterest, Firefox |
| Development and creative tools | GitHub, GitLab, Docker, GitBook, Read the Docs, Blender, OBS, VLC, Kdenlive |
| AI | OpenAI, Anthropic and other catalogue entries |

In the admin panel's template editor, select service groups and adjust their
domains, save the template, then assign it to a user. New ordinary groups are
included in the default full template; existing custom templates keep their
selections, so enable new services explicitly. Opt-in groups remain off by default.

Entries cover configured website and content domains, not every operation of an
app or game. CS2 and Dota 2 may also need Steam; YouTube sign-in needs the Google
group. Game sessions, voice calls and arbitrary UDP traffic are not carried by
the HTTP/SNI proxy. See the [catalogue guide](docs/service-catalogue.md).

### Player hub redesign

The panels use a gaming-inspired layout with violet accents, clear account cards
and a compact icon button for copying DNS. Day/night themes and password
visibility controls are available only in the user panel. Receipt upload and
review have been removed; administrators activate and renew accounts directly.

### Recent panel fixes

Usernames appear once in a green badge matching the IP address. The template
selector has more room for its label and an RTL arrow layout. The local Vazirmatn
font, theme controls and table filters remain available.

## Requirements

- Two Debian or Ubuntu servers with public IP addresses: a relay and an exit.
- Root or sudo access and a working network path between the servers.
- Access to distribution package repositories.
- A domain pointing to each server that serves an HTTPS panel, with a valid certificate. Automatic HTTP certificate validation requires reachable port 80.

The installer uses distribution packages including Python, nginx, dnsmasq and nftables. No npm, pip or Docker is required to run the service.

## Install

Install the **exit first**, then the **relay**. Run on each server:

```sh
curl -fsSLO https://raw.githubusercontent.com/DevURANIUM/DNS/main/dns.sh && sudo bash dns.sh
```

Choose the server role and follow the prompts. Supply the exit's sync token when configuring the relay. The installer prints connection details and enabled panel addresses when finished.

Download the file before executing it: the installer reads embedded payloads from itself and expects interactive input. The installer filename is `dns.sh`.

### Ports

| Port | Relay | Exit |
| --- | --- | --- |
| 53 TCP/UDP | Client DNS | — |
| 80 TCP | HTTP forwarding and certificate validation | HTTP and certificate validation |
| 443 TCP | SNI proxy | SNI proxy |
| 3478 UDP | STUN | — |
| 8443 TCP | TLS user panel | Sync API |
| 9443 TCP, default | — | Configurable admin panel |
| 22 TCP | SSH | SSH |

Port 8446 on the exit is loopback-only for its Google IPv6 route; it does not need public exposure. Configure both host and provider firewalls for the services used on each machine.

### First connection

1. Create an account in the user panel.
2. Save its quota and validity period in the admin panel to activate it.
3. Open the user panel from the intended internet connection and register its IP.
4. Set the displayed DNS address on the device. Repeat the same address if a secondary DNS is required.
5. Register the IP again after changing networks or receiving a new public IP.

A new relay starts open. It automatically enables access enforcement after the first sync containing a registered address. Check with `sudo smartdns-acl enforce status`. SSH is not gated.

## Update or uninstall

Download the installer again and rerun it. It compares versions and asks before continuing. Existing users and settings are preserved; database backups are stored under `/var/backups/smart-dns/`.

```sh
# Print the version without installing
bash dns.sh --version

# Remove the service from this machine
sudo bash dns.sh --uninstall
```

## Useful commands

```sh
# Exit: find the admin panel
sudo smartdns-access

# Relay: inspect service and domain routing
sudo smartdns status
sudo smartdns list
sudo smartdns find spotify
sudo smartdns-rules check example.com
sudo smartdns-acl enforce status

# Either server: diagnostics and restart
sudo smartdns-logs -e
sudo smartdns-logs -f
sudo smartdns-logs --report
sudo smartdns-restart
```

Reports mask configuration secrets but can still contain customer IPs and usernames. Review before sharing. Restarting can briefly interrupt active connections.

## Development

| Path | Purpose |
| --- | --- |
| `templates/` | Python services, management commands and service configuration |
| `tools/installer-logic.sh` | Install and upgrade logic |
| `assets/ui/` | CSS, JavaScript, font and font license |
| `domains/` | Domain lists and service catalogue |
| `common/` | Shared network configuration |
| `tools/` | Builds and previews |

```sh
# Rebuild panel assets and the standalone installer
python tools/build-installer.py
bash -n dns.sh

# Generate sample pages and serve them locally
python tools/preview-ui.py
python -m http.server 8765 --bind 127.0.0.1 --directory docs/preview
```

Open the local [admin overview](http://127.0.0.1:8765/admin.html), [user management](http://127.0.0.1:8765/users.html) or [customer panel](http://127.0.0.1:8765/user.html). Previews use sample data and do not execute server operations. Generated previews, local screenshots and Python caches are excluded from version control; generate the preview pages before opening these links.

Edit source assets and rebuild instead of editing the installer or generated UI blocks directly. See the [UI asset guide](assets/ui/README.md) and [Persian UI change notes](docs/UI-update.fa.md).

## Limitations and bug reports

This project is alpha software. Connectivity depends on the relay-to-exit path, ISP and destination service. Speed limits apply to downloads only. A relay without a TLS certificate does not serve a user panel. Xbox download stalls were previously reported; this update does not establish that they are fixed.

Report bugs in [DNS Issues](https://github.com/DevURANIUM/DNS/issues), including server role, OS, version, reproduction steps and relevant output. Do not publish passwords, tokens or private admin panel URLs.

## License and contributions

The code is distributed under the [MIT License](LICENSE). Vazirmatn is distributed separately under the [SIL Open Font License](assets/ui/OFL.txt). Issues and pull requests belong in [DevURANIUM/DNS](https://github.com/DevURANIUM/DNS).

Thanks to previous contributors, including [Armin Toranj](https://github.com/arminandtoo).


## DynX — 2026-09-21

Imported all 5470 unique domain names from the three user-selected DynX lists;
5053 were new and 417 already existed. Original downloads are retained in
`domains/sources/dynx/`; [import report](domains/sources/dynx-import.json).
Nginx map files were parsed as data, not installed as executable configuration.
Existing opt-in exceptions retain their behavior. Custom templates must enable
the new DynX groups explicitly; the full default template includes ordinary new domains.
These third-party lists have not been independently verified for ownership or connectivity.


## IP registration API

Update the exit and relay to 0.3.30 or later. In the user panel, expand the API key
section and click Generate/Replace. No password prompt is required for a signed-in user.
The new random 48-character hexadecimal key appears inline with a copy button.
Generating a key invalidates the previous key. Save it immediately; it is shown only once.
Only a SHA-256 digest is stored. Deleting the user also deletes their key.

```sh
curl --fail-with-body -X POST 'https://dns.azrael.cfd:8443/ip' \
  -H 'Authorization: Bearer YOUR_KEY' \
  --data-urlencode 'ip=YOUR_PUBLIC_IPV4'
```

Use your relay hostname. POST form encoding is required. Do not put keys in URLs.
The curl `--key` option is for TLS client certificates, not this API.
A successful response is JSON with `ok: true` and `ip`; propagation takes up to
30 seconds. The request replaces the account's previous IP and does not activate
or extend its plan. Private, loopback, multicast and IPv6 addresses are rejected.
HTTP errors: 400 invalid IP, 401 invalid/revoked key, 403 suspended account,
409 IP owned by another user, 429 rate limit (10 valid-key requests/minute),
503 exit unavailable. The key grants IP registration only, not account management.
