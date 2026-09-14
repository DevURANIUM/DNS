# Game and media catalogue

The catalogue now includes 31 additional service entries and 62 additional
domains. Existing service/group identifiers are retained so saved plans keep
their selections. Warzone is explicitly named under the existing Blizzard /
Activision group; its `callofduty.com` and `activision.com` domains were already
present. CS2 has its own official-site entry and also names its Steam dependency.

New entries: CS2, Dota 2, Fortnite/Rocket League/Fall Guys, Marvel Rivals,
Delta Force, ARC Raiders/THE FINALS, Path of Exile 1/2, Wuthering Waves,
PUBG Mobile, HoYoLAB, YouTube/Music, Reddit, Pinterest, Vimeo, SoundCloud,
Mozilla/Firefox, Proton, Dropbox, Wikipedia, Internet Archive, Duolingo, DeepL,
Telegram Web, Signal, Speedtest, GitBook, Read the Docs, Blender, OBS, VLC
and Kdenlive. Warzone and Valorant are named in their existing publisher entries.

## Scope

These are website/content routing entries, **not a verified complete game
backend allowlist**. A game's own domain often serves only its website; sign-in
and downloads can depend on Steam, Epic, console or publisher groups. The panel
shows these dependencies beside each entry. Live matches, UDP, voice and
non-HTTP ports are not tunneled by this HTTP/SNI proxy. No lower-ping or NAT
improvement is promised. Real relay-to-exit testing is still required.

YouTube includes youtube.com, youtu.be, youtube-nocookie.com, ytimg.com and
googlevideo.com. Google sign-in requires the existing Google group. Video
traffic consumes relay and exit bandwidth. QUIC is not carried by this proxy.

The default template includes new ordinary groups automatically. Custom
templates retain their existing selections; select new entries explicitly.
Existing Epic/EA/PlayStation opt-in exceptions stay intact. Do not add shared
UDP game backends (for example Steam Datagram Relay) as HTTP routing domains.

## Sources checked on 2026-09-14

- [Activision TCP/UDP ports](https://support.activision.com/articles/ports-used-for-call-of-duty-games)
- [Steam networking requirements](https://help.steampowered.com/en/faqs/view/2EA8-4D75-DA21-31EB)
- [CS2](https://www.counter-strike.net/cs2), [Dota 2](https://www.dota2.com/)
- [Warzone](https://www.callofduty.com/warzone), [Marvel Rivals](https://www.marvelrivals.com/)
- [ARC Raiders](https://arcraiders.com/), [Delta Force](https://www.playdeltaforce.com/)
- [Fortnite](https://www.fortnite.com/), [Rocket League](https://www.rocketleague.com/)
- [Path of Exile](https://www.pathofexile.com/), [Path of Exile 2](https://pathofexile2.com/)
- [Wuthering Waves](https://wutheringwaves.kurogames.com/), [PUBG Mobile](https://www.pubgmobile.com/)
- [HoYoLAB](https://www.hoyolab.com/), [Supercell](https://supercell.com/en/games/)
- [Cisco YouTube domain guidance](https://www.cisco.com/c/en/us/support/docs/application-networking-services/wide-area-application-services-waas-software/201014-Configure-Youtube-Traffic-Optimization-w.pdf)

Official website identification does not establish that every service operation
works through this deployment. Domain notes describe the supported scope.

## Maintenance

Edit `domains/services.json` and add ordinary routed domains to
`domains/domains.txt`. Keep a domain owned by exactly one group. Do not run `tools/classify-services.py` over the curated catalogue: that
legacy classifier rebuilds it and can discard manually added services and notes.
Run `python tools/test-service-catalogue.py`, the template and opt-in tests,
then `python tools/build-installer.py` to update `dns.sh`.
