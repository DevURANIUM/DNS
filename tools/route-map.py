"""Compile the shipped domain catalogue into an nginx hostname allowlist.

This is destination discovery for HTTP, not inference from DNS query timing.
Unknown protocols and destinations must never be guessed from this list.
"""
import ipaddress
import re


def route_map(text):
    domains = set()
    for number, line in enumerate(text.splitlines(), 1):
        name = line.split('#', 1)[0].strip().lower().rstrip('.')
        if not name:
            continue
        if len(name) > 253 or '.' not in name or any(
            not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', part)
            for part in name.split('.')
        ):
            raise ValueError('Invalid routing domain on line %d: %r' % (number, name))
        try:
            ipaddress.ip_address(name)
        except ValueError:
            pass
        else:
            raise ValueError('IP literals are not routing domains: %s' % name)
        domains.add(name)
    if not domains:
        raise ValueError('Refusing an empty routing catalogue')
    # A parent already covers its descendants. Removing redundant entries
    # keeps the hostname hash small and avoids duplicate nginx map keys.
    roots = [name for name in sorted(domains) if not any(
        '.'.join(name.split('.')[i:]) in domains
        for i in range(1, len(name.split('.')))
    )]
    return '\n'.join('        .%s 1;' % name for name in roots)
