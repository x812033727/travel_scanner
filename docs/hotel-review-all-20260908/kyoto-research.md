# Kyoto hotel research — 2026-09-08

Read-only supporting evidence for task `2026-09-08-hotel-review-all-20260908`. No production mutation, paid API, reservation search, or booking action was performed. The structured companion is [kyoto-research.json](kyoto-research.json).

## Review result

- Reviewed official identities for all 10 Kyoto hotel products and opened the exact stored URLs for all 33 pending platform options with URLs.
- None is represented here as browser-verified. This agent's CUA inventory had Chrome/Edge but no IAB; parent instructed no Chrome fallback. Root still needs to review actual IAB hotel/address pages and exact Google Place IDs.
- All 10 products and 33 options remain `hold` in this research artifact. This is evidence preparation, not a blanket rejection or a live status change.
- Four coordinate candidates are non-OTA Wikidata statements; six are specifically identified OSM elements. Coordinates alone do not authorize publication.

## Coordinate candidates

| Hotel | Latitude, longitude | Durable source | Point interpretation |
|---|---|---|---|
| Celestine Gion | 34.9985143, 135.7736963 | [OSM way 457365863](https://www.openstreetmap.org/way/457365863) | Bounding-box center, ODbL |
| Cross Kyoto | 35.0082055, 135.7696681 | [OSM way 205862942](https://www.openstreetmap.org/way/205862942) | Bounding-box center, ODbL |
| Daiwa Terrace Hachijo | 34.9842238, 135.7614466 | [OSM node 8840587666](https://www.openstreetmap.org/node/8840587666) | Published node, ODbL |
| Granvia Kyoto | 34.985861, 135.760222 | [Wikidata Q11337862](https://www.wikidata.org/wiki/Q11337862) | Selected non-OTA P625, CC0 |
| Hyatt Regency Kyoto | 34.988556, 135.773361 | [Wikidata Q11325962](https://www.wikidata.org/wiki/Q11325962) | Selected non-OTA P625, CC0; closure hold |
| Mitsui Garden Shijo | 35.0030109, 135.7549679 | [OSM node 4813050121](https://www.openstreetmap.org/node/4813050121) | Published node, ODbL |
| Miyako Kyoto Hachijo | 34.983778, 135.755917 | [Wikidata Q11501050](https://www.wikidata.org/wiki/Q11501050) | Selected non-OTA P625, CC0 |
| Royal Park Sanjo | 35.0090754, 135.7694863 | [OSM way 581621455](https://www.openstreetmap.org/way/581621455) | Bounding-box center, ODbL |
| Vischio Kyoto | 34.9834469, 135.7594632 | [OSM node 7428574567](https://www.openstreetmap.org/node/7428574567) | Published node, ODbL |
| Westin Miyako Kyoto | 35.00886111, 135.78794444 | [Wikidata Q11288502](https://www.wikidata.org/wiki/Q11288502) | Selected non-OTA P625, CC0 |

The JSON preserves official addresses, source URLs, Wikidata claim IDs/revisions, OSM versions/timestamps and individual reasoning. These are hotel representative points, not certified entrances. The three way centers are Overpass bounding-box centers, **not polygon centroids**, and must not be advertised as entrance locations. The selected Granvia Wikidata point differs from an alternate Skyscanner point; the latter was deliberately excluded.

## Operational and identity findings

### Hyatt: scheduled closure, not already closed

The operator's [2026-04-09 announcement](https://www.orix-realestate.co.jp/news/pdf/press_20260409.pdf) gives **2027-05-09** as the operation-ending date. [Current Hyatt identity](https://www.hyatt.com/hyatt-regency/en-US/kyoto-hyatt-regency-kyoto/hotel-info) and the [Kyoto tourism listing](https://ja.kyoto.travel/tourism/single01.php?category_id=13&tourism_id=3117) refer to the same property. Keep the product and all five pending options held while `future_closure_date_guard_missing` remains. A matching OTA page does not remove that blocker.

### Westin: partial facilities notice

The [operator contact](https://www.miyakohotels.ne.jp/westinkyoto/contact/) establishes the full premises address; the [Marriott overview](https://www.marriott.com/en-us/hotels/ukywi-the-westin-miyako-kyoto/overview/) uses broader Sanjo/Keage wording. The [January 2027 notice](https://www.miyakohotels.ne.jp/westinkyoto/topic/information/3336/) is for SPA, fitness and indoor pool maintenance, not hotel-wide closure. The JSON preserves each facility's exact local-time interval. Map/browser review remains open.

### Names needing careful matching

- The operator's [2023 rebrand table, page 2](https://www.daiwaroynet.jp/datas/files/2023/03/10/550e57d5cd03265131360bfbc6e1cc3836c9e181.pdf) supports the old Terrace Hachijo Higashiguchi name in OSM becoming Terrace Hachijo PREMIER. Separate Kyoto Ekimae and Hachijoguchi hotels must not be substituted.
- Granvia is inside Kyoto Station; Vischio is the distinct hotel south of the station. Their points must not be exchanged.
- Mitsui Shijo is not Shinmachi Bettei; Royal Park Sanjo is not Nijo or Umekoji.
- Miyako's Agoda URL contains `hatasho-cho-jp`. That suspicious slug alone is insufficient to approve or reject the hotel; actual landing name and street address are required.

## Platform URL outcome

| Platform | Pending URLs opened | Web reader result | Browser approval |
|---|---:|---|---:|
| Agoda | 10 | Empty input placeholders; no hotel identity/address readable | 0 |
| Booking.com | 10 | JavaScript/robot-verification interstitial | 0 |
| Rakuten | 10 | Correct property names; full street address not established by reviewed text | 0 |
| Official | 2 | Hyatt exact street address; Marriott Westin district-level address | 0 |
| Trip.com | 1 | Hyatt name and full street address match | 0 |

Rakuten Shijo and Royal Park Sanjo succeeded after one timeout retry. The reader reported older cached content for Daiwa (8 months), Granvia (10 months), Miyako (2 months), and Vischio (last week); these cannot establish live availability. No rates, review bodies, room photos, or provider coordinates were copied into these artifacts. Every option ID, version and original URL is preserved in the JSON for exact IAB follow-up.

## Reuse and licensing

The pre-existing [Kyoto municipal permit evidence](../hotel-platforms/kyoto.evidence.json), from [dataset 00039](https://data.city.kyoto.lg.jp/dataset/00039/) / [resource 21412](https://data.city.kyoto.lg.jp/resource/?id=21412), corroborates names and premises addresses under CC BY 4.0. It has **no coordinate columns**; no coordinates were inferred from that file.

[Wikidata's licensing policy](https://www.wikidata.org/wiki/Wikidata:Licensing) places structured statements under CC0. Selected P625 claims explicitly reference Japanese Wikipedia; alternate Skyscanner claims were excluded. Do not relabel an OTA-backed coordinate as an independent source by passing it through Wikidata or Commons.

**© OpenStreetMap contributors.** Selected OSM data is available under [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/); see [OSM copyright and attribution requirements](https://www.openstreetmap.org/copyright). Publication must display appropriate attribution, identify ODbL availability and meet applicable share-alike requirements for derived data. Merely naming OSM privately does not satisfy the public interface's obligations. No OSM contributor personal identifiers were retained.

## Handoff checklist

- Root: open each exact URL in IAB and match the full name/street, or retain explicit hold for blockers.
- Root: obtain genuine Google Place IDs through observed provider results; never derive them from CID values.
- Root: validate candidate points against exact hotel identity without persisting Google coordinates.
- Preserve Hyatt's closure hold until a supported date guard exists.
- Resolve OSM public attribution/license handling before any of the six OSM-backed points is published.
- Keep previous approved options and unknown-URL options outside this 33-option re-review unchanged.
