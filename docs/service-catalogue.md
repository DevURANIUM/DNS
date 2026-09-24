# Domain catalogue

The live catalogue is `domains/services.json`. It groups services by category,
rather than keeping a separate visible entry for every imported source.
`domains/domains.txt` supplies the base relay DNS list and the exit HTTP allowlist.

## Editing

1. Update the relevant group in `services.json`.
2. Update `domains.txt` for names that should be routed by the base resolver.
3. For a direct exception, update `common/bypass.conf` and add an opt-in
   exception group so default and custom profiles can preserve the direct path.
4. Run `python -B tools/build-installer.py`.
5. Deploy the exit first, then the relay.

Keep category/group keys and `legacy_sources` metadata stable. The panel uses
those identifiers when migrating saved template selections. Existing templates
inherit changes inside selected groups; newly added groups are not necessarily
selected in custom templates. Opt-in groups are excluded from the full default.

## Matching and automatic web routing

A rule for `example.com` covers the root and all its subdomains, but does not
match `fakeexample.com` or `example.com.attacker.invalid`. More specific DNS
rules take precedence. Avoid routing and bypassing the exact same hostname in
different ordinary groups: equal-specificity rules can undermine an exception.

The installer builds an HTTP hostname map from `domains.txt`. Invalid names
abort the build. Redundant descendants are collapsed in that map, not removed
from the catalogue. The default HTTP server rejects hosts absent from the map;
explicit HTTP server exceptions are retained.

HTTPS uses SNI. Upstream web addresses are resolved on demand with a 60-second
cache. This is not automatic detection of non-web game destinations or automatic
selection between direct and relay. Panel custom domains do not update the
build-time HTTP map automatically.

## Games

Steam web dependencies for CS2 and Dota 2 are in Games together with
`counter-strike.net` and `dota2.com`. The Akamai domain is a shared CDN and its
inclusion also affects non-Steam subdomains.

Warzone STUN hosts `genesis.stun.eu.demonware.net`,
`genesis.stun.us.demonware.net` and the observed lobby hostname
`lsg.7400.prod.demonware.net` have direct exceptions. Preserve those separately
from the routed parent `demonware.net`.

Listing a game's domains does not provide arbitrary UDP/TCP forwarding or
guarantee matchmaking. Valve documents this distinction in its
[required ports and proxy domains](https://help.steampowered.com/en/faqs/view/2EA8-4D75-DA21-31EB).

## Sources

- [Source manifest](../domains/catalogue-sources.json): historical research and provenance.
- [DynX import report](../domains/sources/dynx-import.json): imported files and hashes.
- [Original DynX snapshots](../domains/sources/dynx/): retained for reproducibility.

Snapshots are reference data, not executable nginx configuration. Source reports
describe imports at their recorded dates; their counts are not current totals.
No list is an exhaustive inventory of every game backend or Linux mirror, and
third-party entries are not a guarantee of ownership, regional restrictions or
current reachability. Review proposed entries before deploying them.
