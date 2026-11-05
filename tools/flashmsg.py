"""Where a panel sent the browser, with the message it carried.

The panels hand what an action did to the next page in a one-time cookie,
never in the address. The checks were written against "page?m=message", so
this puts the cookie's message back in that place - still percent-encoded,
as the address had it - and each check reads as it did.
"""

NAMES = ("sdns_msg", "sdu_msg")


def where(headers):
    """The Location of a redirect, with its flash message as ?m=...

    `headers` is the dict a test's stand-in handler kept, or an
    http.client response.
    """
    get = headers.getheader if hasattr(headers, "getheader") else headers.get
    loc = get("Location") or ""
    name, _, rest = (get("Set-Cookie") or "").partition("=")
    value = rest.split(";", 1)[0]
    if name.strip() not in NAMES or not value:
        return loc
    base, _, query = loc.partition("?")
    return base + "?m=" + value + ("&" + query if query else "")
