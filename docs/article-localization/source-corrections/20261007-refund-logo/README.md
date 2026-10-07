# Japan tax-free refund guide: source correction and missing languages

This work corrects the public `japan-tax-free-refund-2026` source before adding
English, Japanese, Korean and Simplified Chinese. It is separate from the
13-article / 52-document candidate in PR #1365.

## Exact source correction

The reviewed correction changes seven source-document pointers:

| Pointer | Result |
| --- | --- |
| `/blocks/12/items/3` | A store needs the tax-free-store licence; the recognition logo is voluntary. |
| `/sources` | Add the direct official symbol-system FAQ, retaining the previous nine citations. |
| `/blocks/0/text` | Explain consumption of consumables in Japan, rather than claiming every opened or used purchase loses eligibility. |
| `/blocks/6/text` | Keep purchase-record-wide rejection for consumed consumables or any missing item without broadening it to any use. |
| `/blocks/3/description` | Place the refund after customs export confirmation, without claiming physical departure is always required first. |
| `/blocks/11/text` | Rename the heading so the new conditions are not labelled unchanged. |
| `/blocks/12/items/2` | Distinguish continuing gold/platinum bullion exclusions from the new explicit coin exclusions. |

The source SVG changes only its description and the refund-stage heading to match
the customs-confirmation condition. Its geometry, styles, fonts and positions are
preserved. Both original photographs and their credits remain unchanged.

Primary sources checked by the independent source reviewer:

- [Japan Tourism Agency: new refund procedure](https://www.mlit.go.jp/kankocho/tax-free/page01_000001_00021.html)
- [Japan Tourism Agency: refund FAQ](https://www.mlit.go.jp/kankocho/tax-free/page01_000001_00023.html)
- [Japan Tourism Agency: symbol-system FAQ, II Q2](https://www.mlit.go.jp/kankocho/tax-free/content/001845126.pdf)
- [National Tax Agency: refund-procedure Q&A](https://www.nta.go.jp/publication/pamph/shohi/menzei/201805/pdf/0025003-110_02.pdf)

## Provenance

The source writer and independent reviewer are different agents. The actual
schema-v1 source-correction receipt passes `source_correction.verify_review`
against the original database publication and draft versions. Raw snapshots,
database identifiers, receipts and provider attempts remain in owner storage.

| Input | SHA-256 |
| --- | --- |
| Original source document | `6358cae7243f026ec6a2a27e9f26394e5805759ce42932ef92032a1367ff7c27` |
| Reviewed corrected source document | `8f19020e8412793852dd6502faa35f88b5953c950b06d456f6b20564f0308bb7` |
| Independent source review | `552fd065bbe7ffd3d4460f2d890ce820423e003f40623359bb5b90877051bb7e` |
| Independent source evidence | `d99b6c5f22f5ab3da2b8eb37f13bb2f5e2282faeb8fc88dac0f34305415c0603` |
| Original source SVG | `905b853bd85559828d1716f96ad3bad59b3b61c69fe88c479f66c3c292f29e1b` |
| Reviewed corrected source SVG | `9abff5f9592df1cb0313f614aad9056e88d5934a5134c8d3ecc8215e3383ed81` |

The root executor applied the exact reviewed source SVG after backing up the
original bytes. Four new derived jobs preserve the original jobs and attempts,
reuse their translations and apply the reviewed corrections. Nine compact
English/Japanese diagram labels have a separate proposal/application receipt.
The official drift guard and materializer passed without overriding their root,
editing attempts or invoking a provider.

## Current state

Source correction, four-locale rendering and genuine independent whole-document,
image and glyph review are complete. All five source/target diagrams have actual
minimum 15px fonts without overflow. The English month heading was corrected by
the root executor and independently rechecked; original jobs and before-edit
artifacts remain preserved.

The unchanged official local installer and replay both completed with exit 0.
Replay preserved pack, asset, receipt and durable-journal bytes exactly; the four
external jobs pass the official admitted-installation drift and artifact guards.
The final pack contains the reviewed source plus all four missing languages.

| Local evidence | SHA-256 |
| --- | --- |
| Complete independent four-target review | `1123f321497a81d02e20e40658a1960752939e4488fdedf72b1d7d0217c35b1b` |
| Official verified local bundle manifest | `05e3b08b830ab2e5aa89c117f8d87f41891a3174991e17631eaeefdc118f1585` |
| Installed five-language pack | `4f960fbb5b3c87883dbbb5e4704e8d27069f3175eb3e4ad4d2a295c4ca319f59` |
| Byte-identical durable local journal | `788ed729ef5062136fda1eeaac03327e5383156eff9ab32e60b06112de1a6519` |

Content PR, merge, deployment and publication remain pending. Production content
and settings were not changed. The separate release ticket is
`2026-10-07-release-reviewed-japan-refund-source-and`.

Publication requires a fresh post-deployment baseline, exact source/draft/target
guards, independent review of the final bytes, owner approval, a verified backup
and public-page validation. Fresh jobs must use the fresh baseline's actual
existing-target provenance; do not omit repository documents to reuse an old
job binding. Local authoring or CI does not count as publication.
