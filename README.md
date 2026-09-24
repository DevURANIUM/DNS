# DNS

Self-hosted Smart DNS with Persian admin and user panels, service profiles, traffic quotas, and an API for registering a user's public IP address.

**Release: 0.3.36**

[راهنمای فارسی](README.fa.md) · [Repository](https://github.com/DevURANIUM/DNS) · [Report an issue](https://github.com/DevURANIUM/DNS/issues) · [Domain catalogue](docs/service-catalogue.md)

## Quick start

Install the **exit server first**, then the **relay server**. Run this command on each:

```bash
curl -fsSLO https://raw.githubusercontent.com/DevURANIUM/DNS/main/dns.sh && sudo bash dns.sh
```

Select the appropriate server role and follow the prompts. You will need the exit server's sync token when configuring the relay. The installer prints the available panel addresses when setup finishes.

The installer is self-contained; cloning this repository is not required. Download the file before running it rather than piping it into Bash, because it reads its embedded configuration payloads from disk.

> This command downloads the version published on the main branch. Local changes become available through this URL only after they are published.

## How it works

Deploy a relay inside Iran and an exit server outside Iran. The relay returns its own IP address for selected domains and forwards supported web connections through the exit. Domains with direct-routing rules resolve to their original addresses.

```text
Client → Relay DNS
           ├─ Direct domain → Original destination
           └─ Routed domain → Relay → Exit → HTTP/HTTPS destination

User panel on Relay ← Sync → Admin panel and database on Exit
```

The exit uses the HTTP hostname or TLS SNI to identify the web destination. HTTPS traffic passes through without TLS decryption. Accounts and quotas are stored on the exit; the relay normally synchronizes every 30 seconds.

Upstream web addresses are resolved on demand with a 60-second DNS cache. Existing connections are not moved when an address changes.

**DNS is not a general-purpose VPN or game tunnel.** It does not automatically identify arbitrary UDP destinations, decide which services require a direct route, or guarantee access to every game.

## Features

| Area | Capabilities |
| --- | --- |
| Administration | Activate, block and delete users; reset user passwords |
| Plans | Traffic quotas, expiry dates, download speed limits and service profiles |
| User panel | Registration, login, usage display and public IP registration |
| API keys | Generate or replace a key for IPv4 registration |
| Service profiles | Select service categories and configure domain rules |
| Access control | IP allowlists and traffic accounting through nftables |
| Interface | Persian RTL panels, bundled fonts, user light/dark themes and copy buttons |
| Operations | Service logs, domain-route inspection, TLS certificate management and installer backups |

Vazirmatn and JetBrains Mono are bundled with the panels, so fonts do not require an external CDN. Payment receipt submission is not included; administrators activate accounts directly.

## Requirements

- Two Debian or Ubuntu servers with public IPv4 addresses.
- Root or sudo access on both servers.
- A working network path between the relay and exit, and access to distribution package repositories.
- A domain and TLS certificate for each HTTPS panel, with DNS pointing to the appropriate server.
- Reachable port 80 for HTTP certificate validation, unless another certificate method is used.

The installer uses distribution packages such as nginx, dnsmasq, Python, nftables and coturn. Docker, npm and pip are not required to run the service. Validate your chosen operating system and network setup before production use.

## Set up the first user

1. Register an account in the user panel.
2. In the admin panel, save a plan for that user to activate the account.
3. From the internet connection that will use the service, sign in to the user panel and register its IP.
4. Set the device's DNS server to the address shown in the panel.
5. Register the IP again whenever the connection's public address changes.

If the device requires a secondary DNS address, repeat the same service address. An unrelated public resolver can bypass the configured routing rules.

A new relay starts with access enforcement disabled. It automatically enables enforcement after the first sync containing a registered address. Check the current state with:

```bash
sudo smartdns-acl enforce status
```

## Services and domain rules

The catalogue groups domains into categories such as games, AI, development, media, Windows and Linux. Examples include Steam, CS2, Dota 2, Warzone, PlayStation, Xbox, YouTube and Linux distribution repositories.

A parent domain covers itself and its subdomains. A more specific rule can override that route. Preserve the direct-routing exceptions for Warzone and other services unless you have verified a reason to change them.

The full default profile includes ordinary groups and excludes opt-in groups. Custom profiles retain their saved selections. Adding a domain to a selected group is different from adding a new group, which may need to be selected explicitly.

The default HTTP proxy accepts domains in the installer's generated allowlist and their subdomains; explicit HTTP exceptions also remain available. Custom domains added through the panel do not automatically update that build-time HTTP allowlist. Update the source catalogue and rebuild the installer to change it.

See the [catalogue guide](docs/service-catalogue.md) for editing instructions, sources and coverage limits.

## IP registration API

In the user panel, open the API key section and select Generate/Replace. The new key appears inline with a copy button. Save it immediately; replacing a key invalidates the previous one. Only its hash is stored.

```bash
curl --fail-with-body 'https://YOUR_DNS_DOMAIN:8443/ip' -H 'Authorization: Bearer YOUR_KEY' -d 'ip=YOUR_PUBLIC_IPV4'
```

Replace the hostname, key and public IPv4 address. The `-d` option makes this a POST request. Do not put keys in URLs. The curl `--key` option is for TLS client certificates and is unrelated to this API.

A successful request replaces the account's previous IP. It does not activate an account or extend its plan. Changes can take approximately 30 seconds to reach the relay.

| HTTP status | Meaning |
| --- | --- |
| 200 | IP registered successfully |
| 400 | Invalid IP address |
| 401 | Invalid or replaced API key |
| 403 | Account not permitted |
| 409 | IP belongs to another account |
| 429 | Rate limit exceeded |
| 503 | Exit unavailable |

## Network ports

| Port | Relay | Exit |
| --- | --- | --- |
| TCP/UDP 53 | Client DNS | — |
| TCP 80 | HTTP forwarding and certificate validation | HTTP proxy and certificate validation |
| TCP 443 | HTTPS forwarding | SNI proxy |
| UDP 3478 | STUN | — |
| TCP 8443 | HTTPS user panel | Sync API |
| TCP 9443 | — | Default admin panel port; configurable |
| TCP 22 | SSH, if using the default port | SSH, if using the default port |

Port 8446 on the exit is reserved for an internal Google route and is not publicly exposed. Configure host and provider firewalls for the services you use; opening all ports is unnecessary.

## Update or uninstall

Download and run the installer again, updating the exit before the relay. The installer displays version changes and preserves existing users and settings.

```bash
# Version of the downloaded installer
bash dns.sh --version

# Version installed on this server
cat /var/lib/smart-dns/version

# Uninstall from this server
sudo bash dns.sh --uninstall
```

Installer backups are stored under `/var/backups/smart-dns/`. Keep an independent backup of your deployment's data and configuration before uninstalling or making major changes.

## Troubleshooting

```bash
# Exit: show admin access information
sudo smartdns-access

# Relay: inspect service state and a domain's route
sudo smartdns status
sudo smartdns-rules check example.com
sudo smartdns-acl enforce status

# Logs and diagnostic report
sudo smartdns-logs -e
sudo smartdns-logs -f
sudo smartdns-logs --report

# Restart services; active connections may be interrupted
sudo smartdns-restart
```

A correct DNS answer does not prove that a game connection succeeds. Direct client connections do not pass through the relay and will not appear in its packet captures. Speed limits apply to downloads.

When [reporting an issue](https://github.com/DevURANIUM/DNS/issues), include the version, operating system, server role and reproduction steps. Remove passwords, API keys, sync tokens and private admin paths. Diagnostic reports can still contain customer IPs or usernames.

## Project layout

```text
dns.sh                    Generated standalone installer
templates/
  services/               Admin panel, central API, relay sync and user panel
  commands/               Management commands installed on the servers
  config/                 nginx, nftables and STUN configuration templates
  systemd/                Service units and timers
common/                   Shared DNS and network configuration
domains/                  Domain lists, service catalogue and source records
assets/ui/                CSS, JavaScript, fonts and font licenses
tools/                    Installer build, UI build and preview tools
docs/                     Maintenance and development guides
```

Build from source:

```bash
python -B tools/build-installer.py
bash -n dns.sh
```

Edit source files rather than the generated installer. Repository paths differ from installed server paths. See the [development guide](docs/development.md) for build and release checks.

## License

The code is distributed under the [MIT License](LICENSE). [Vazirmatn](assets/ui/OFL.txt) and [JetBrains Mono](assets/ui/JetBrainsMono-OFL.txt) retain their separate font licenses. Third-party domain source records are preserved for provenance.
