# Service catalogue — 2026-09-16

The catalogue contains 122 services and 1755 domain entries. This expansion added
49 service entries and 1188 domains, preserving previous group identifiers and
ownership. Existing custom templates retain their selections. The default full
template includes ordinary new groups; existing opt-in exclusions remain intact.

## Coverage

AI additions include Runway, ElevenLabs, Suno, Udio, Stability, Replicate, fal,
Cohere, Grok, Qwen, Kling, Luma, HeyGen, Synthesia, You.com, FLUX, SambaNova,
Cerebras, Midjourney, Leonardo and Ideogram. Existing ChatGPT, Claude, Gemini,
DeepSeek, Mistral, Perplexity, Hugging Face and coding tools remain available.

Game additions include Warframe, Destiny/Bungie, Escape from Tarkov,
Battlestate, Gaijin, Wargaming, Square Enix, FFXIV, Guild Wars 2, Facepunch,
Dead by Daylight, Overwolf, Modrinth and FiveM. Steam, Rockstar, PlayStation,
Xbox, Epic, Warzone and the other existing publisher groups are retained.

Windows Update has a separate group for update.microsoft.com, windowsupdate.com
and adl.windows.com. Delivery Optimization endpoints under mp.microsoft.com
are already owned by Xbox: select that group as well for these downloads.

Linux repositories include Debian, Ubuntu, Fedora, Rocky, AlmaLinux, openSUSE,
Kali, Raspbian and NixOS. The shared Linux mirror group combines HTTP/HTTPS
hosts from the official Debian, Ubuntu, Arch and Alpine lists. Arch entries
must be active with at least 95% completion in the fetched status snapshot.
Shared hosts are stored once, not once per distribution. Existing parent
rules may already cover a mirror, so source counts differ from added counts.

## Domain rules

A domain covers itself and all subdomains at any depth. For example,
example.com covers api.example.com and a.b.example.com but not fakeexample.com.
The longest matching domain wins, so explicit subdomain bypass rules remain
effective. This is already implemented by dnsmasq and smartdns-rules; no broad
catch-all rule or invented wildcard domains are required.

## Verification and limits

[The source manifest](../domains/catalogue-sources.json) records a source and
check date for each added domain, overlaps, and failed website checks that
were excluded. Official lists establish mirror identity, not continuous health.
A responding vendor homepage identifies a website, not a complete backend list.
The catalogue is not a claim that every entry is sanctioned or blocked in Iran.
No end-to-end relay/exit connectivity or Iranian ISP tests were performed.

These rules route HTTP/SNI traffic. They do not provide general UDP, rsync, FTP,
voice, game-server connectivity or guaranteed access to region-restricted accounts.
Download and mirror traffic consumes relay/exit quota. This is a dated snapshot,
not an exhaustive list of every service or every Linux mirror worldwide.

## Primary sources

- [OpenAI network guidance](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)
- [Microsoft Windows endpoints](https://learn.microsoft.com/en-us/windows/privacy/windows-11-endpoints-non-enterprise-editions)
- [Debian mirror master list](https://mirror-master.debian.org/status/Mirrors.masterlist)
- [Ubuntu archive mirrors](https://launchpad.net/ubuntu/+archivemirrors)
- [Arch mirror status](https://archlinux.org/mirrors/status/json/)
- [Alpine mirror list](https://dl-cdn.alpinelinux.org/alpine/MIRRORS.txt)

Edit services.json and domains.txt together, preserve group keys and rebuild
with `python tools/build-installer.py`. The legacy classify-services.py tool
rebuilds classifications and should not be run over this curated catalogue.


## DynX import — 2026-09-21

Current total: 123 services and 6808 domains. Imported 5470 unique domains from
[DynX](https://github.com/MrDevAnony/DynX-AntiBan-Domains), adding 5053 and preserving 417 existing entries.
See [the import manifest](../domains/sources/dynx-import.json) for original hashes,
normalization and group assignments. Source entries are not independently verified.
Existing opt-in subdomains remain excluded by default.
