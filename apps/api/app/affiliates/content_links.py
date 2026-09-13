"""Non-travel affiliate programs an article may link to, and how an affiliate URL is recognised.

Travel partners never reach an article as a raw URL: destination offers are resolved on the
server and leave the site through a same-origin clickout that 303-redirects with
``Referrer-Policy: no-referrer``. That pattern is wrong for these programs. Hostinger's
Affiliate Program Agreement (updated 2026-08-19) forbids "link cloaking or masking
techniques ... hiding that traffic source", and a redirect that strips the referrer hides
exactly that. So a content partner link is the program's own URL, pasted by the editor into
a ``partner_link`` block, drawn as a direct ``rel="sponsored"`` link, with the click counted
by a separate request.

Two jobs live here:

- ``CONTENT_PARTNERS`` is the allowlist for those blocks. Adding a program is one entry, and
  the entry names every host its links may use: networks often track through a domain of
  their own, and that one has to be listed too.
- ``affiliate_marker`` recognises an affiliate or tracking URL wherever an *ordinary* link is
  written (article links, sources, image credits, legal pages), so the only way a tracked
  link reaches a reader is the block that discloses it.

Nothing here raises. The write paths turn an answer into their own error; the read path uses
the same answer to draw no button rather than fail.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from functools import cache
from typing import Literal
from urllib.parse import SplitResult, parse_qsl, urlsplit

ContentCategory = Literal["hosting", "books", "courses", "software"]


@dataclass(frozen=True)
class ContentPartner:
    code: str
    display_name: str
    category: ContentCategory
    #: Hosts a link may point at. A subdomain of one matches; a lookalike suffix does not.
    hosts: tuple[str, ...]
    #: Query keys (lower case) that mark this program's tracked links on its own hosts.
    tracking_params: frozenset[str] = frozenset()
    #: Path prefixes that mark a tracked link on this program's own hosts.
    tracking_path_prefixes: tuple[str, ...] = ()
    #: Query keys of links the program's own terms keep off websites, and the reason why.
    forbidden_params: tuple[tuple[str, str], ...] = ()


CONTENT_PARTNERS: tuple[ContentPartner, ...] = (
    ContentPartner(
        code="hostinger",
        display_name="Hostinger",
        category="hosting",
        hosts=("hostinger.com",),
        tracking_params=frozenset({"referralcode"}),
        # REFERRALCODE links belong to the customer referral program, whose page says they
        # "should not" be published "on commercial websites, blogs, or YouTube channels".
        # The separate affiliate program is the one an article may use.
        forbidden_params=(
            (
                "referralcode",
                "這是 Hostinger 顧客推薦計畫（REFERRALCODE）的連結，條款不允許放在網站上；"
                "請改用聯盟計畫後台產生的連結",
            ),
        ),
    ),
    ContentPartner(
        code="books_com_tw",
        display_name="博客來",
        category="books",
        hosts=("books.com.tw",),
        # 策略聯盟 (AP) links: /exep/assp.php/<AP id>/products/<product id>
        tracking_path_prefixes=("/exep/assp.php/",),
    ),
)
PARTNERS_BY_CODE: dict[str, ContentPartner] = {
    partner.code: partner for partner in CONTENT_PARTNERS
}

#: Query keys that only affiliate tracking uses, refused on an ordinary link to any host.
AFFILIATE_QUERY_KEYS = frozenset(
    {
        "marker",
        "trs",
        "aff",
        "aff_id",
        "affid",
        "affiliate_id",
        "aff_sub",
        "sub_id",
        "subid",
        "clickid",
        "irclickid",
        "cjevent",
        "awc",
        "ranmid",
        "raneaid",
        "ransiteid",
    }
)
#: Keys that mean affiliate tracking on a merchant's own host but are ordinary elsewhere: a
#: news site's ``?aid=`` is an article id, Booking.com's is a partner account.
HOST_SCOPED_KEYS = frozenset({"aid", "cid", "sid", "tag", "allianceid", "utm_source"})
AMAZON_HOSTS: tuple[str, ...] = (
    "amazon.com",
    "amazon.co.jp",
    "amazon.co.uk",
    "amazon.de",
    "amazon.fr",
    "amazon.ca",
    "amazon.com.au",
    "amazon.sg",
)
#: Any link to these is a tracked redirect or a short link that hides where it goes.
REDIRECT_HOSTS: tuple[str, ...] = (
    # The travel side's own tracked links.
    "tp.st",
    "tp.media",
    "affiliate.klook.com",
    "s.klook.com",
    # Affiliate network click domains: Rakuten Advertising, Awin, CJ, Partnerize,
    # PartnerStack and Impact.
    "click.linksynergy.com",
    "awin1.com",
    "anrdoezrs.net",
    "dpbolvw.net",
    "jdoqocy.com",
    "kqzyfj.com",
    "tkqlhce.com",
    "prf.hn",
    "partnerlinks.io",
    "sjv.io",
    "pxf.io",
    # Short links.
    "amzn.to",
    "shope.ee",
    "s.shopee.tw",
    "bit.ly",
    "tinyurl.com",
    "reurl.cc",
    "lihi.cc",
    "lihi1.cc",
    "pse.is",
)


@dataclass(frozen=True)
class LinkProblem:
    code: Literal["partner_link_unknown", "partner_link_host", "partner_link_forbidden"]
    detail: str


def host_matches(host: str, allowed: str) -> bool:
    """The same rule as ``app.affiliates.service.validate_target_url``: the host itself or a
    subdomain of it, so ``evilhostinger.com`` never passes for ``hostinger.com``."""
    return host == allowed or host.endswith(f".{allowed}")


def _split(url: str) -> tuple[SplitResult, str] | None:
    try:
        parts = urlsplit(url)
    except ValueError:
        return None
    return parts, (parts.hostname or "").lower().rstrip(".")


@cache
def _merchant_hosts() -> tuple[str, ...]:
    # Imported on first use rather than at module load: the travel registry pulls in the
    # destination catalog, and the legal-page writer that imports this module needs none of it.
    from app.travel_services.registry import BRANDS

    travel = [host for brand in BRANDS.values() for host in brand.hosts]
    partners = [host for partner in CONTENT_PARTNERS for host in partner.hosts]
    return tuple(dict.fromkeys([*travel, *partners, *AMAZON_HOSTS]))


def affiliate_marker(url: str) -> str | None:
    """What makes ``url`` an affiliate or tracked link, or ``None`` for an ordinary one.

    Returns the matched host, query key or path prefix so an error can name it. Only http(s)
    URLs are examined; ``mailto:`` and anything malformed are not this check's business.
    """
    split = _split(url)
    if split is None:
        return None
    parts, host = split
    if parts.scheme not in {"http", "https"} or not host:
        return None
    for redirect in REDIRECT_HOSTS:
        if host_matches(host, redirect):
            return redirect
    keys = {key.lower() for key, _ in parse_qsl(parts.query, keep_blank_values=True)}
    generic = sorted(keys & AFFILIATE_QUERY_KEYS)
    if generic:
        return generic[0]
    if any(host_matches(host, merchant) for merchant in _merchant_hosts()):
        scoped = sorted(keys & HOST_SCOPED_KEYS)
        if scoped:
            return scoped[0]
    for partner in CONTENT_PARTNERS:
        if not any(host_matches(host, allowed) for allowed in partner.hosts):
            continue
        tracked = sorted(keys & partner.tracking_params)
        if tracked:
            return tracked[0]
        for prefix in partner.tracking_path_prefixes:
            if parts.path.startswith(prefix):
                return prefix
    return None


def partner_link_problem(code: str, url: str) -> LinkProblem | None:
    """Why a ``partner_link`` block may not carry ``url`` for partner ``code``, if it may not.

    The block's own model has already required an https URL with a host; this is the part
    that depends on the registry, which is why it runs on writes and on reads but never
    inside the model that validates stored revisions.
    """
    partner = PARTNERS_BY_CODE.get(code)
    if partner is None:
        return LinkProblem("partner_link_unknown", f"「{code}」不在合作連結的合作夥伴清單上")
    split = _split(url)
    if split is None or not any(host_matches(split[1], allowed) for allowed in partner.hosts):
        return LinkProblem(
            "partner_link_host",
            f"{partner.display_name} 的合作連結只能連到：{'、'.join(partner.hosts)}",
        )
    keys = {key.lower() for key, _ in parse_qsl(split[0].query, keep_blank_values=True)}
    for key, reason in partner.forbidden_params:
        if key in keys:
            return LinkProblem("partner_link_forbidden", reason)
    return None


def link_key(url: str) -> str:
    """A stable name for one stored link: survives reordering and republication, and says
    nothing a reader cannot already see, since the URL itself is in the public article."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
