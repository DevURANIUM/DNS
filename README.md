# 🛡️ DNS — High-Performance Smart DNS & Geo-Bypass Routing Infrastructure

[![GitHub stars](https://img.shields.io/github/stars/DevURANIUM/DNS?style=flat-square&color=7dd3a0)](https://github.com/DevURANIUM/DNS/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/DevURANIUM/DNS?style=flat-square&color=5eead4)](https://github.com/DevURANIUM/DNS/network)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Automated Tests](https://img.shields.io/badge/Tests-110%2F110%20Passed-7dd3a0?style=flat-square)](tools/)
[![Platform](https://img.shields.io/badge/Platform-Debian%20%7C%20Ubuntu-orange?style=flat-square)](https://debian.org)

**DNS** is a modern, self-contained Smart DNS platform engineered to seamlessly bypass international sanctions and geo-restrictions. Built with split routing and transparent SNI proxying, it delivers optimized low-latency access for gaming consoles, workstations, smart TVs, and mobile devices—without requiring client VPN software or custom root certificates.

*[نسخه فارسی (Persian)](README.fa.md)*

---

## 📑 Table of Contents
- [Architecture & Mechanics](#-architecture--mechanics)
- [Key Features](#-key-features)
- [Network Ports Overview](#-network-ports-overview)
- [System Requirements](#-system-requirements)
- [Quick Start Installation](#-quick-start-installation)
- [Deployment Topologies](#-deployment-topologies)
- [Web Management Consoles](#-web-management-consoles)
- [CLI Reference & Commands](#-cli-reference--commands)
- [Telegram Bot Service](#-telegram-bot-service)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Credits](#-credits)
- [License](#-license)

---

## 🏛️ Architecture & Mechanics

The system decouples DNS resolution and traffic forwarding across two synchronized server tiers: **Relay Nodes** (situated in the restricted locale) and **Exit Nodes** (situated abroad).

```text
  Client Device (PS5 / Xbox / PC / Phone)
                    │
                    │ 1. DNS Query
                    ▼
         ┌────────────────────┐
         │  Relay Node (Local)│
         │   (dnsmasq daemon) │
         └─────────┬──────────┘
                   │
         ┌─────────┴────────────────────────┐
         ▼                                  ▼
[Sanctioned & Filtered Domains]      [Standard Unrestricted Domains]
         │                                  │
         │ Responds with Relay IP           │ Resolves directly via upstreams
         ▼                                  ▼
┌───────────────────┐              ┌───────────────────┐
│       Nginx       │              │  Direct Outbound  │
│    (SNI Proxy)    │              │  Connection (ISP) │
└─────────┬─────────┘              └───────────────────┘
          │
          │ 2. Raw TCP Stream Passthrough
          ▼
┌───────────────────┐
│  Exit Node (Host) │
│ (Transparent Pipe)│
└─────────┬─────────┘
          │
          │ 3. Forward to Target Endpoint
          ▼
[PlayStation / Steam / Docker / etc.]
```

### Zero-Decryption Principles:
1. **No TLS Termination:** The relay does not decrypt packets or hold private client certificates. It inspects the Server Name Indication (SNI) from the initial TLS handshake and tunnels the raw TCP stream overseas.
2. **Zero Root CA Requirements:** Eliminates client-side security risks; devices do not need custom configuration profiles or root authority installation.
3. **Domestic Speed Preservation:** Traffic destined for local networks bypasses the international link entirely, maintaining minimal latency and unconstrained bandwidth.

---

## ✨ Key Features

- **🎮 Tailored for Gaming & Entertainment:**
  - Dedicated routing catalogs for PlayStation Network (PSN), Xbox Live, Steam, Epic Games Store, EA Desktop, Battle.net, Riot Games, and PUBG Mobile.
  - Native STUN/TURN integration on the relay to preserve NAT Type (Open/Moderate) for console party chat, voice rooms, and P2P lobbies.
  - Direct routing for game package downloads from untargeted CDN edges, preserving line-speed downloading.

- **⚡ Kernel-Level Access Control (`nftables`):**
  - Ultra-fast packet filtering with kernel-resident IP allowlists.
  - Granular byte counting per customer without context switches into user space.
  - Automatic quota exhaustion cutoffs and scheduled cycle resets.
  - Bandwidth throttling powered by modern `htb` and `fq_codel` queuing disciplines.

- **🎨 Redesigned Glassmorphic Web Panels:**
  - **Operator Panel (Admin):** Comprehensive cluster status, real-time bandwidth graphs, user provisioning, custom pricing plans, and flexible exit node mapping.
  - **User Portal (Customer):** One-click self-service IP registration with bilingual digit support (Persian & Latin), remaining allowance widgets, and instant DNS presets.
  - Custom UI aesthetic featuring variable typography (`Vazirmatn` & `JetBrains Mono`) with automatic Light and Dark theme adaptation.

- **🛡️ Censorship-Resistant Tunneling:**
  - Resilient fallback transports (wrapped TLS sessions, alternative link ports, and KCP optimizations) when direct connections face carrier disruption.
  - High availability Standby Node replication with zero-touch automated failover.

- **📦 Fully Self-Contained:**
  - Packed into a standalone installer (`dns.sh`) without reliance on third-party repositories, Docker daemons, or runtime pip installations.

---

## 🔌 Network Ports Overview

The following ports are utilized across the infrastructure. When choosing a port for the administrative panel, ensure it avoids colliding with these reserved services:

| Port | Protocol | Usage / Service |
|---|---|---|
| **22** | TCP | System administration (SSH) |
| **53** | UDP/TCP | Domain Name Service (DNS) resolution |
| **80** | TCP | HTTP transport and console package caching |
| **443** | TCP | Transparent SNI proxying for secure traffic |
| **8443** | TCP | Authenticated synchronization between Relay and Exit nodes |
| **8446** | TCP | Encrypted node-to-relay tunneling channel |
| **3478** | UDP/TCP | STUN/TURN daemon for console NAT traversal |

> [!NOTE]
> Select an unassigned port (e.g. **9443**) for the operator administration dashboard to prevent network conflicts.

---

## 📋 System Requirements

- **Operating System:** Debian 11 / 12, Ubuntu 20.04 / 22.04 / 24.04 LTS (x86_64 or ARM64)
- **Privileges:** Root privileges (`sudo` or `root`)
- **Topology:** A minimum of two virtual machines: one Relay (domestic) and one Exit (abroad)

---

## 🚀 Quick Start Installation

Download and execute the self-contained installer on your server:

```bash
curl -sSL https://raw.githubusercontent.com/DevURANIUM/DNS/main/dns.sh -o dns.sh && sudo bash dns.sh
```

---

## 🛠️ Deployment Topologies

1. **Exit Node (Overseas):** Install this first. The script configures the outbound forwarder and outputs a **Pairing Token**.
2. **Relay Node (Domestic):** Install this on the server that interfaces with users. Enter the Exit Node's IP address and pairing token when prompted.
3. **Standby / Node Nodes:** Register supplementary exits to load-balance plans or configure automated failover.

---

## 💻 Web Management Consoles

- **Operator Dashboard (Admin):**
  `http://[Server-IP-or-Domain]:[PORT]/[SECRET_PATH]`
- **Customer Self-Service Portal:**
  `http://[Server-IP-or-Domain]:[PORT]/`

---

## ⌨️ CLI Reference & Commands

A rich suite of terminal commands is bundled for operational administration:

```sh
smartdns status
smartdns list
smartdns find spotify
smartdns add example.com
smartdns del example.com
smartdns bypass api.example.com
smartdns test example.com
smartdns-rules
smartdns-rules show test
smartdns-rules check gemini.google.com
smartdns-access
smartdns-access username ali
smartdns-access port 9443
smartdns-access path [new]
smartdns-access password [new]
smartdns-access rotate
smartdns-acl list
smartdns-acl usage 5.188.44.19
smartdns-acl add 5.188.44.19 ali
smartdns-acl del 5.188.44.19
smartdns-acl reset <ip>|--all
smartdns-acl enforce status
smartdns-acl enforce on
smartdns-acl enforce off
smartdns-acl save
smartdns-shape list
smartdns-shape off
smartdns-cert panel.example.com
```

---

## 🤖 Telegram Bot Service

Automate client registrations and account administration with the bundled bot implementation in `examples/telegram-bot/`:

1. Configure environment variables:
   ```bash
   cp examples/telegram-bot/bot.env.example examples/telegram-bot/bot.env
   nano examples/telegram-bot/bot.env
   ```
2. Launch the daemon:
   ```bash
   sudo systemctl enable --now dns-bot.service
   ```

---

## 🧪 Testing & Quality Assurance

The codebase includes an extensive suite of **110 integration tests** verifying firewall integrity, routing stability, and UI engines:

```bash
python tools/test-theme.py
python tools/test-ports.py
python tools/test-menu.py
python tools/test-tunnel.py
```

All 110 automated tests pass consistently across supported Linux distributions.

---

## 🤝 Credits

Special acknowledgment to Amin Mohammadi for the BackPack transport architecture licensed under AGPL-3.0 at github.com/AminMGMT/BackPack.

---

## 📄 License

This project is licensed under the terms of the [MIT License](LICENSE).
