# Food merchant navigation and reservation links

Navigation and reservation are separate contracts. Navigation keeps the existing
reviewed Google Place ID or Korean Naver place identity. A reservation link is an
optional, manually reviewed branch page and never acts as location or source evidence.

The country mapping is fixed: Japan uses TableCheck, South Korea Catchtable Global,
Taiwan EZTABLE, Singapore Chope, Hong Kong OpenRice, Thailand Hungry Hub and Vietnam
PasGo. Public responses include only `verified` rows whose HTTPS host and path match
the country's provider. Home, search, discovery, ranking and restaurant-list pages are
rejected. Missing, ambiguous and disabled outcomes remain stored but are not public.

The initial catalog records an outcome for every curated merchant. It intentionally
uses `ambiguous` unless an exact branch page was confirmed, because missing seed evidence
does not prove that a page is absent. Administrators can open the page, record
locale-specific variants and set `verified` one merchant at a time. The
unique provider URL constraint prevents one branch page from being attached to two
different merchants.
