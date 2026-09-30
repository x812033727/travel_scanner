"""Add this batch's articles to their vertical's index, in place, in the locales it publishes.

``update_index.py [crypto|tech|ai]... [--locale=<locale>] [--dry-run]`` -- with no vertical
named, every vertical that has something to add; with no locale named, all five. Run once,
after that vertical's packs carry the locales the run edits. Every sentence edit is an exact
replacement that must match once, so a second run fails instead of editing twice.

Three things changed from batch 3:

* Three indexes instead of one, so every table here is keyed by vertical first. The AI index
  keeps its slug forever (``docs/article-architecture.md``: every existing URL stays), so it is
  retitled in place, never renamed.
* The index's own link lists are ``article`` inlines now, not ``link`` blocks -- ``pack_cli
  relink`` ran over them -- and so are its opening paragraphs. Batch 3 looked up anchors by URL
  and asserted ``block["type"] == "paragraph"``; both now miss. Everything here addresses a
  block by its role and edits a rich paragraph's text nodes in place.
* Retitling an index breaks the link text of every article that points at it, because an
  ``article`` inline's ``text`` is frozen into the pack and rendered as it stands
  (``tasks/open/2026-09-16-retitled-guides-stale-link-text.md``). ``retitle`` walks the JSON
  structure of every pack and rewrites only the inlines whose ``slug`` is the index -- never a
  regular expression over the file, because the batches do not agree on field order.

Batch 3's one-off repair of the Japanese month headings is gone: batch #497's damage was fixed
by that run and the headings now read 2026年N月のニュース解説.

Batch 3 wrote whatever it produced. This one reads the site's own rules -- the schema, the
source cap, the reader-text walk -- and validates the finished index before it is written, so
an index that the importer would refuse is a refusal here instead of a red CI run.

Batch 4.5 (the news since 2026-09-16) added ``INSERT``: the crypto and tech indexes are
grouped by region and topic, and a batch that opens a group the index does not have -- the
United Kingdom, in crypto -- needs a heading and a paragraph the tables above cannot place.
Their generators (``build_*_index.py``) are not rerun, because they rewrite zh-TW from scratch
and would discard the relinked inlines and the four translations.

Batch 4.6 (the eleven articles of 2026-09-18) is zh-TW only, so this run learned ``--locale``:

    update_index.py ai tech crypto --locale=zh-TW [--dry-run]

Repeatable, or a comma list; without it the run is all five locales, which is what every batch
before this one was. The tables were keyed by locale already, so what the flag changes is the
pack check -- a zh-TW-only article carries no five locales -- and the guards in ``main``, which
refuse the three things one locale cannot decide on its own: an edit written for a locale the
run does not touch, citing a source (the five locale documents of one index would end up
citing different ones) and retitling. ``--dry-run`` prints the diff the run would write, and
writes nothing.

Batch 4.7 (the fifteen articles of 2026-09-20 onwards, with three earlier events written up
late) is zh-TW only as well, and changes nothing in this script: the same three tables, the
same flag, the same refusal on a second run. What it does change is the AI index's callout,
which names the last event the series covers as well as the day it was last expanded -- the
batch's newest AI article happened on 2026-09-21, so this time both dates in that sentence
move, not only the second.

Batch 4.8 (ten articles the hourly automation missed, events of 2026-09-17 to 09-25) is five
locales again, the first batch since 4.5 to be, so it runs without ``--locale``:

    update_index.py ai tech crypto [--dry-run]

Two things are new. The four locales other than zh-TW had not been expanded since 2026-09-18
while zh-TW had moved on to 2026-09-23, so every date sentence below is written per locale:
different old dates, the same new one. And the crypto index opens a South Korea group the way
4.5 opened the United Kingdom's, which changes the number of regions the index names in three
places -- the description, the opening paragraph and the first summary item. ``edit_block``
could not reach a summary item until now, which is why that item still said four regions
after 4.5 had made them five; it edits a summary's or a list's items the way it edits a rich
paragraph's text nodes, one item, once.

Batch 4.9 (one article, GPT-6.1 Sol, 2026-09-29, five locales) touches the AI index alone:

    update_index.py ai [--dry-run]

One link at the end of September and the three date sentences. The crypto and tech rows of
4.8 and its inserted blocks are kept as ``_EDITS_4_8`` and ``_INSERT_4_8``, which nothing runs.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verticals import (  # noqa: E402
    BY_NAME,
    CONTENT,
    LOCALES,
    VERTICALS,
    block_kind,
    block_text,
    link_of,
)

from app.guides.content_pack import ArticlePack  # noqa: E402
from app.guides.pack_ingest import _document_text  # noqa: E402
from app.guides.schemas import GuideDocument  # noqa: E402

# An edit whose replacement is still an editorial decision. The run stops and lists them all
# before it touches anything, so a half-filled table cannot write the word TODO into an index.
TODO = "«TODO»"

#: How many sources a document may carry, read off the schema instead of retyped. The index
#: already cites nine, and a batch that cites one source per article reaches the cap long
#: before anyone notices -- ``GuideDocument`` is the only place that number should live.
MAX_SOURCES = next(
    rule.max_length
    for rule in GuideDocument.model_fields["sources"].metadata
    if hasattr(rule, "max_length")
)

# The day this run expands the indexes: the one date the sentences below print, so the next
# batch changes this constant and the same sentences instead of finding new ones to edit.
EXPANDED_ON = "2026-09-30"
EXPANDED = {
    "zh-TW": "2026 年 9 月 30 日",
    "en": "September 30, 2026",
    "ja": "2026年9月30日",
    "ko": "2026년 9월 30일",
    "zh-CN": "2026 年 9 月 30 日",
}
#: The newest event the AI series covers after this run, which the AI index's callout prints
#: beside the expansion date: batch 4.9's GPT-6.1 Sol article, 2026-09-29 in Taipei.
NEWEST_AI_EVENT = "2026-09-29"

# vertical -> (slug, where to put the link). ``after`` is the existing slug to place the link
# after (a leading "<" means before it), or an anchor of the ``INSERT`` kind -- per locale,
# as a dict, when it names a heading whose text differs by locale. Applied in order: an entry
# may name a slug inserted just before it.
#
# Batch 4.9 (2026-09-30): one article, GPT-6.1 Sol, five locales. It goes at the end of
# September's group, which ends on the Google Vids article (09-24) in all five locales.
NEW: dict[str, list[tuple[str, object]]] = {
    "crypto": [],
    "tech": [],
    "ai": [("ai-news-gpt-61-sol-20260929", "ai-news-google-vids-omni-free-20260924")],
}
# What batch 4.8 (2026-09-27) added, kept for the record, as it ran:
#
# # Batch 4.8 (2026-09-27): ten articles the hourly automation missed, five locales each. The
# # zh-TW documents carry the zh-TW-only links of 4.4, 4.6 and 4.7 and the other four do not, so
# # a group can end on a different link per locale; those rows name their anchor per locale.
# #
# # * AI: September's group, by event date, after whatever the group ends on in that locale
# #   (09-22 Opus 5.5, then the two 09-23 articles in Taipei order -- GPT-6 at 02:00, the Taiwan
# #   ads rollout at 10:00 -- then 09-24 Vids).
# # * Tech: WordPress and then Synology at the end of Platforms and Software (the coordinator's
# #   order, not event order), Snapdragon at the end of Consumer Hardware and Chips.
# # * Crypto: the central bank at the end of Taiwan, the forum at the end of Japan, and Korea
# #   under the South Korea heading ``INSERT`` adds behind the Japan group. That heading is placed
# #   after the Japan group's last link before this table runs, so the forum's link, placed after
# #   that same link, lands above it.
# _TW_LAST_AI = "ai-news-nvidia-physical-ai-safety-20260921"
# _FIVE_LAST_AI = "ai-news-google-cc-family-agent-20260918"
# NEW: dict[str, list[tuple[str, object]]] = {
#     "crypto": [
#         (
#             "crypto-news-taiwan-cbc-stablecoin-deposit-token-cbdc-20260917",
#             {
#                 "zh-TW": "crypto-news-taiwan-vasp-tax-ruling-20260903",
#                 "en": "crypto-news-taiwan-vasp-act-20260630",
#                 "ja": "crypto-news-taiwan-vasp-act-20260630",
#                 "ko": "crypto-news-taiwan-vasp-act-20260630",
#                 "zh-CN": "crypto-news-taiwan-vasp-act-20260630",
#             },
#         ),
#         ("crypto-news-japan-onchain-finance-forum-20260925", "crypto-news-jfsa-cybersecurity-20260723"),
#         (
#             "crypto-news-korea-market-manipulation-referrals-20260923",
#             {
#                 "zh-TW": "heading:韓國",
#                 "en": "heading:South Korea",
#                 "ja": "heading:韓国",
#                 "ko": "heading:한국",
#                 "zh-CN": "heading:韩国",
#             },
#         ),
#     ],
#     "tech": [
#         (
#             "tech-news-wordpress-712-20260922",
#             {
#                 "zh-TW": "tech-news-enisa-threat-landscape-20260922",
#                 "en": "tech-news-app-store-bundles-multiseat-20260916",
#                 "ja": "tech-news-app-store-bundles-multiseat-20260916",
#                 "ko": "tech-news-app-store-bundles-multiseat-20260916",
#                 "zh-CN": "tech-news-app-store-bundles-multiseat-20260916",
#             },
#         ),
#         ("tech-news-synology-dsm-sa2613-20260918", "tech-news-wordpress-712-20260922"),
#         ("tech-news-snapdragon-8-elite-gen6-20260922", "tech-news-apple-m6-m5-ultra-20260825"),
#     ],
#     "ai": [
#         (
#             "ai-news-claude-opus-55-20260922",
#             {
#                 "zh-TW": _TW_LAST_AI,
#                 "en": _FIVE_LAST_AI,
#                 "ja": _FIVE_LAST_AI,
#                 "ko": _FIVE_LAST_AI,
#                 "zh-CN": _FIVE_LAST_AI,
#             },
#         ),
#         ("ai-news-gpt-6-sol-luna-20260923", "ai-news-claude-opus-55-20260922"),
#         ("ai-news-chatgpt-ads-taiwan-20260923", "ai-news-gpt-6-sol-luna-20260923"),
#         ("ai-news-google-vids-omni-free-20260924", "ai-news-chatgpt-ads-taiwan-20260923"),
#     ],
# }
# What batch 4.4 wave 1 (2026-09-23) added, kept for the record: six AI articles about August and
# early-September events, zh-TW only, each placed in its month group by event date -- after the
# existing link whose event date precedes it (the batch-4.3 practice), not at the end of September.
#
#     "ai": [
#         ("ai-news-claude-text-watermark-20260815", "ai-news-chatgpt-free-thinking-20260806"),
#         ("ai-news-gemini-student-offer-20260820", "ai-news-claude-text-watermark-20260815"),
#         ("ai-news-openai-zero-data-retention-20260820", "ai-news-gemini-student-offer-20260820"),
#         ("ai-news-openai-hugging-face-incident-20260826", "ai-news-gemini-live-20260826"),
#         ("ai-news-openai-cursor-wind-down-20260828", "ai-news-openai-hugging-face-incident-20260826"),
#         ("ai-news-meta-muse-agent-20260909", "ai-news-chatgpt-images-25-20260908"),
#     ],
# What batch 4.7 (2026-09-23) added, kept for the record: the twelve articles of the window that
# opened on 2026-09-20 and three write-ups of earlier events, zh-TW only; the AI links went after
# September's last link in display_order, the tech and crypto links joined existing groups
# (Petal at the end of compute infrastructure by the owner's ruling).
#
#     "crypto": [
#         ("crypto-news-taiwan-deposit-token-pilot-20260922", "crypto-news-taiwan-vasp-act-20260630"),
#         ("crypto-news-sec-innovation-exemption-20260917", "crypto-news-sec-regulation-crypto-assets-20260821"),
#         ("crypto-news-taiwan-vasp-tax-ruling-20260903", "crypto-news-taiwan-deposit-token-pilot-20260922"),
#     ],
#     "tech": [
#         ("tech-news-googlebook-launch-20260921", "tech-news-iphone-duo-dev-resources-20260918"),
#         ("tech-news-eu-data-centre-rating-20260921", "tech-news-eu-cra-reporting-20260911"),
#         ("tech-news-cisa-kev-zyxel-gs1900-20260921", "tech-news-cisa-kev-linux-kernel-20260918"),
#         ("tech-news-meta-petal-subsea-cable-20260921", "tech-news-nvidia-mediatek-20260831"),
#         ("tech-news-enisa-threat-landscape-20260922", "tech-news-cisa-kev-zyxel-gs1900-20260921"),
#         ("tech-news-moda-mydata-student-loan-20260917", "tech-news-taiwan-sovereign-ai-corpus-20260915"),
#     ],
#     "ai": [
#         ("ai-news-openai-math-advisory-20260921", "ai-news-kimi-k3-bedrock-20260918"),
#         ("ai-news-openai-frontier-standards-20260921", "ai-news-openai-math-advisory-20260921"),
#         ("ai-news-anthropic-life-sciences-verification-20260917", "ai-news-openai-frontier-standards-20260921"),
#         ("ai-news-meta-one-subscription-20260915", "ai-news-anthropic-life-sciences-verification-20260917"),
#         ("ai-news-openai-academy-paths-20260921", "ai-news-meta-one-subscription-20260915"),
#         ("ai-news-nvidia-physical-ai-safety-20260921", "ai-news-openai-academy-paths-20260921"),
#     ],
# What batch 4.6 (2026-09-22) added, kept for the record. Its comment said the same thing this
# one does about CISA: the index has no security group outside the European Union's.
#
#     "crypto": [
#         ("crypto-news-occ-three-trust-charters-20260918", "crypto-news-ncua-genius-act-20260518"),
#         ("crypto-news-sec-crypto-fraud-patterns-20260918", "crypto-news-cftc-passive-software-20260917"),
#         ("crypto-news-eba-third-party-risk-20260918", "crypto-news-eba-psd2-mica-20260212"),
#     ],
#     "tech": [
#         ("tech-news-iphone-duo-dev-resources-20260918", "tech-news-iphone-duo-20260909"),
#         ("tech-news-windows-cloud-rebuild-20260918", "tech-news-windows-project-zenith-20260904"),
#         ("tech-news-npm-stage-only-tokens-20260918", "tech-news-app-store-bundles-multiseat-20260916"),
#         ("tech-news-cisa-kev-linux-kernel-20260918", "tech-news-npm-stage-only-tokens-20260918"),
#     ],
#     "ai": [
#         ("ai-news-anthropic-accenture-evaluation-20260918", "ai-news-google-cc-family-agent-20260918"),
#         ("ai-news-openai-australia-youth-safety-20260918", "ai-news-anthropic-accenture-evaluation-20260918"),
#         ("ai-news-gemini-notebook-study-tools-20260918", "ai-news-openai-australia-youth-safety-20260918"),
#         ("ai-news-kimi-k3-bedrock-20260918", "ai-news-gemini-notebook-study-tools-20260918"),
#     ],
# vertical -> the articles whose first source the index cites. A source the index already
# carries is skipped, not appended twice.
#
# Nothing this batch either, and not because the sources are unsuitable. The AI index already
# cites 19 of the 20 sources a document may carry and the tech index 17, so six more do not
# fit either index. And citing is a five-locale act: the source list belongs to a locale
# document, so a zh-TW-only run would leave the five documents of one index citing different
# sources, which no later batch could put back without editing four locales it never read.
# The fifteen packs of this batch carry no other locale to cite from either. ``main`` refuses
# a non-empty table unless all five locales are in the run.
#
# Batch 4.8 is a five-locale run, so the second reason is gone and the first is not: the AI
# index still cites 19 sources, tech 17 and crypto 14, and one per article is four, three and
# three more. The coordinator kept the table empty (DELTA-4-8 item 6).
CITED: dict[str, list[str]] = {"crypto": [], "tech": [], "ai": []}

# vertical -> locale -> new title. Empty leaves the title alone: none of the three titles
# names a date or a count, so none of them is wrong after this batch.
RETITLE: dict[str, dict[str, str]] = {
    "crypto": {},
    "tech": {},
    "ai": {},
}

# vertical -> locale -> (where, old, new). ``where`` is "description" or a block index.
#
# Batch 4.7 and 4.4 wave 1 filled only the "zh-TW" rows and left the four other locales alone
# on purpose: every one of them states the day its own document was last expanded, and that
# sentence stays true for as long as a run adds nothing to it. Batch 4.8 adds to all five, so
# all five move -- zh-TW from 2026-09-23, the other four from 2026-09-18 -- each in its own
# sentence's wording. The block indexes are those of the indexes as they read on 2026-09-27,
# before this run's links and inserted blocks; every batch has appended its links behind the
# prose, so the prose blocks sit at the same index in all five locales even though zh-TW has
# more link blocks than the others.
#
# The crypto rows also carry the region count: the South Korea group makes six regions, and the
# description, the opening paragraph (block 0) and the first summary item (block 2) all name
# them. Batch 4.5 moved the first two to five when it added the United Kingdom and could not
# reach the third, which said four until this run. The en description was already 499 of the
# schema's 500 characters, so its row rewrites the whole description in shorter words instead
# of adding two names to it.
#
# What batch 4.4 wave 1 (2026-09-23) edited, kept for the record -- the AI index, zh-TW only:
#
#     (0, "之後多次增補（最近一次 2026-09-23），", ...), (24, the same sentence),
#     (25, "最後增補於 2026-09-23。", ...) -- the callout's first date stayed 2026-09-21.
_CRYPTO_EN_DESCRIPTION = (
    "This site's 2026 crypto news explainers, in six jurisdictions — Taiwan, the US, the UK, the"
    " EU, Japan, South Korea: the Virtual Asset Service Act, the proposed GENIUS Act rules, the"
    " joint SEC–CFTC interpretation and the SEC's own proposal, the end of MiCA's transitional"
    " period and its link to the payment rules, the FCA's perimeter guidance, Japan's FSA reports"
    " and South Korea's manipulation referrals. Regulation, technology and industry only, no"
    " prices, with official sources and a check date."
)
# Batch 4.8's table, as it ran (its dates read EXPANDED, which has moved on since).
_EDITS_4_8: dict[str, dict[str, list[tuple[object, str, str]]]] = {
    "crypto": {
        "zh-TW": [
            ("description", "依台灣、美國、英國、歐盟、日本五個地區", "依台灣、美國、英國、歐盟、日本、韓國六個地區"),
            (
                "description",
                "、日本金融廳公布的報告。",
                "、日本金融廳公布的報告、韓國金融委員會交偵查機關的市場操縱嫌疑案。",
            ),
            (0, "內容依台灣、美國、英國、歐盟、日本五個地區編排", "內容依台灣、美國、英國、歐盟、日本、韓國六個地區編排"),
            (1, "之後多次增補（最近一次 2026 年 9 月 23 日）", f"之後多次增補（最近一次 {EXPANDED['zh-TW']}）"),
            (2, "這份索引依台灣、美國、歐盟、日本四個地區", "這份索引依台灣、美國、英國、歐盟、日本、韓國六個地區"),
        ],
        "en": [
            (
                "description",
                "An index to this site's 2026 crypto news explainers, arranged by jurisdiction — Taiwan,"
                " the US, the UK, the EU, Japan: the Virtual Asset Service Act, the proposed rules put"
                " forward under the GENIUS Act, the joint SEC and CFTC interpretation and the SEC's own"
                " proposal, the end of the MiCA transitional period and where MiCA meets the payment"
                " rules, the UK FCA's perimeter guidance, and Japan's FSA reports. Regulation,"
                " technology and industry only, no prices, with official sources and a check date.",
                _CRYPTO_EN_DESCRIPTION,
            ),
            (
                0,
                "five jurisdictions — Taiwan, the United States, the United Kingdom, the European Union"
                " and Japan —",
                "six jurisdictions — Taiwan, the United States, the United Kingdom, the European Union,"
                " Japan and South Korea —",
            ),
            (1, "and expanded on September 18, 2026.", f"and expanded on {EXPANDED['en']}."),
            (
                2,
                "four jurisdictions — Taiwan, the United States, the European Union and Japan —",
                "six jurisdictions — Taiwan, the United States, the United Kingdom, the European Union,"
                " Japan and South Korea —",
            ),
        ],
        "ja": [
            ("description", "台湾、米国、英国、EU、日本の五つの地域ごとに", "台湾、米国、英国、EU、日本、韓国の六つの地域ごとに"),
            (
                "description",
                "日本の金融庁が公表した報告書を取り上げます。",
                "日本の金融庁が公表した報告書、韓国金融委員会が捜査機関へ告発・通報した仮想資産の相場操縦疑い事案を取り上げます。",
            ),
            (0, "台湾、米国、英国、EU、日本の五つの地域ごとに並べ", "台湾、米国、英国、EU、日本、韓国の六つの地域ごとに並べ"),
            (1, "2026年9月18日に追補しました。", f"{EXPANDED['ja']}に追補しました。"),
            (2, "台湾、米国、EU、日本の四つの地域ごとに", "台湾、米国、英国、EU、日本、韓国の六つの地域ごとに"),
        ],
        "ko": [
            ("description", "대만, 미국, 영국, EU, 일본 다섯 지역별로", "대만, 미국, 영국, EU, 일본, 한국 여섯 지역별로"),
            (
                "description",
                "일본 금융청이 공개한 보고서를 다룹니다.",
                "일본 금융청이 공개한 보고서, 한국 금융위원회가 수사기관에 고발·통보한 가상자산 불공정거래 혐의 사건을 다룹니다.",
            ),
            (0, "대만, 미국, 영국, EU, 일본 다섯 지역별로 배열했고", "대만, 미국, 영국, EU, 일본, 한국 여섯 지역별로 배열했고"),
            (1, "2026년 9월 18일에 보완했습니다.", f"{EXPANDED['ko']}에 보완했습니다."),
            (2, "대만, 미국, EU, 일본 네 지역별로", "대만, 미국, 영국, EU, 일본, 한국 여섯 지역별로"),
        ],
        "zh-CN": [
            ("description", "依台湾、美国、英国、欧盟、日本五个地区", "依台湾、美国、英国、欧盟、日本、韩国六个地区"),
            (
                "description",
                "、日本金融厅公布的报告。",
                "、日本金融厅公布的报告、韩国金融委员会移送侦查机关的市场操纵嫌疑案。",
            ),
            (0, "内容依台湾、美国、英国、欧盟、日本五个地区编排", "内容依台湾、美国、英国、欧盟、日本、韩国六个地区编排"),
            (1, "2026 年 9 月 18 日增补。", f"{EXPANDED['zh-CN']}增补。"),
            (2, "这份索引依台湾、美国、欧盟、日本四个地区", "这份索引依台湾、美国、英国、欧盟、日本、韩国六个地区"),
        ],
    },
    # The tech index states its dates in block 1 alone; the table caption's check date is the
    # table's own and stays.
    "tech": {
        "zh-TW": [
            (1, "之後多次增補（最近一次 2026 年 9 月 23 日）", f"之後多次增補（最近一次 {EXPANDED['zh-TW']}）"),
        ],
        "en": [(1, "and expanded on September 18, 2026.", f"and expanded on {EXPANDED['en']}.")],
        "ja": [(1, "2026年9月18日に追補しました。", f"{EXPANDED['ja']}に追補しました。")],
        "ko": [(1, "2026년 9월 18일에 보완했습니다.", f"{EXPANDED['ko']}에 보완했습니다.")],
        "zh-CN": [(1, "2026 年 9 月 18 日增补。", f"{EXPANDED['zh-CN']}增补。")],
    },
    # The AI index says it twice (blocks 0 and 24) and its callout (25) names both the newest
    # event and the expansion day; both callout dates move this time.
    "ai": {
        "zh-TW": [
            (0, "（最近一次 2026-09-23）", f"（最近一次 {EXPANDED_ON}）"),
            (24, "（最近一次 2026-09-23）", f"（最近一次 {EXPANDED_ON}）"),
            (
                25,
                "本輯收錄的事件到 2026-09-21 為止，最後增補於 2026-09-23。",
                f"本輯收錄的事件到 {NEWEST_AI_EVENT} 為止，最後增補於 {EXPANDED_ON}。",
            ),
        ],
        "en": [
            (0, "(most recently on 2026-09-18)", f"(most recently on {EXPANDED_ON})"),
            (24, "(most recently on 2026-09-18)", f"(most recently on {EXPANDED_ON})"),
            (
                25,
                "covers events through 2026-09-18 and was last expanded on 2026-09-18.",
                f"covers events through {NEWEST_AI_EVENT} and was last expanded on {EXPANDED_ON}.",
            ),
        ],
        "ja": [
            (0, "（最終追補は2026-09-18）", f"（最終追補は{EXPANDED_ON}）"),
            (24, "（最終追補は2026-09-18）", f"（最終追補は{EXPANDED_ON}）"),
            (
                25,
                "本特集の対象は2026-09-18までの出来事で、最終追補は2026-09-18です。",
                f"本特集の対象は{NEWEST_AI_EVENT}までの出来事で、最終追補は{EXPANDED_ON}です。",
            ),
        ],
        "ko": [
            (0, "(마지막 보완 2026-09-18)", f"(마지막 보완 {EXPANDED_ON})"),
            (24, "(마지막 보완 2026-09-18)", f"(마지막 보완 {EXPANDED_ON})"),
            (
                25,
                "본 특집은 2026-09-18까지의 사건을 다루며, 마지막 보완은 2026-09-18입니다.",
                f"본 특집은 {NEWEST_AI_EVENT}까지의 사건을 다루며, 마지막 보완은 {EXPANDED_ON}입니다.",
            ),
        ],
        "zh-CN": [
            (0, "（最近一次 2026-09-18）", f"（最近一次 {EXPANDED_ON}）"),
            (24, "（最近一次 2026-09-18）", f"（最近一次 {EXPANDED_ON}）"),
            (
                25,
                "本辑收录的事件到 2026-09-18 为止，最后增补于 2026-09-18。",
                f"本辑收录的事件到 {NEWEST_AI_EVENT} 为止，最后增补于 {EXPANDED_ON}。",
            ),
        ],
    },
}
# Batch 4.9 (2026-09-30) moves the AI index's three date sentences in all five locales, from
# batch 4.8's 2026-09-27 (expanded) and 2026-09-24 (newest event); tech and crypto are untouched.
EDITS: dict[str, dict[str, list[tuple[object, str, str]]]] = {
    "crypto": {locale: [] for locale in LOCALES},
    "tech": {locale: [] for locale in LOCALES},
    "ai": {
        "zh-TW": [
            (0, "（最近一次 2026-09-27）", f"（最近一次 {EXPANDED_ON}）"),
            (24, "（最近一次 2026-09-27）", f"（最近一次 {EXPANDED_ON}）"),
            (
                25,
                "本輯收錄的事件到 2026-09-24 為止，最後增補於 2026-09-27。",
                f"本輯收錄的事件到 {NEWEST_AI_EVENT} 為止，最後增補於 {EXPANDED_ON}。",
            ),
        ],
        "en": [
            (0, "(most recently on 2026-09-27)", f"(most recently on {EXPANDED_ON})"),
            (24, "(most recently on 2026-09-27)", f"(most recently on {EXPANDED_ON})"),
            (
                25,
                "covers events through 2026-09-24 and was last expanded on 2026-09-27.",
                f"covers events through {NEWEST_AI_EVENT} and was last expanded on {EXPANDED_ON}.",
            ),
        ],
        "ja": [
            (0, "（最終追補は2026-09-27）", f"（最終追補は{EXPANDED_ON}）"),
            (24, "（最終追補は2026-09-27）", f"（最終追補は{EXPANDED_ON}）"),
            (
                25,
                "本特集の対象は2026-09-24までの出来事で、最終追補は2026-09-27です。",
                f"本特集の対象は{NEWEST_AI_EVENT}までの出来事で、最終追補は{EXPANDED_ON}です。",
            ),
        ],
        "ko": [
            (0, "(마지막 보완 2026-09-27)", f"(마지막 보완 {EXPANDED_ON})"),
            (24, "(마지막 보완 2026-09-27)", f"(마지막 보완 {EXPANDED_ON})"),
            (
                25,
                "본 특집은 2026-09-24까지의 사건을 다루며, 마지막 보완은 2026-09-27입니다.",
                f"본 특집은 {NEWEST_AI_EVENT}까지의 사건을 다루며, 마지막 보완은 {EXPANDED_ON}입니다.",
            ),
        ],
        "zh-CN": [
            (0, "（最近一次 2026-09-27）", f"（最近一次 {EXPANDED_ON}）"),
            (24, "（最近一次 2026-09-27）", f"（最近一次 {EXPANDED_ON}）"),
            (
                25,
                "本辑收录的事件到 2026-09-24 为止，最后增补于 2026-09-27。",
                f"本辑收录的事件到 {NEWEST_AI_EVENT} 为止，最后增补于 {EXPANDED_ON}。",
            ),
        ],
    },
}

# vertical -> locale -> (row label in column 0, column index, current cell, new cell). Nothing
# this batch: the AI month table's reading-focus cells were widened in batch 4.3 and September
# already reads "models, agents, security, assistants, voice, infrastructure".
TABLE: dict[str, dict[str, list[tuple[str, int, str, str]]]] = {
    "crypto": {locale: [] for locale in LOCALES},
    "tech": {locale: [] for locale in LOCALES},
    "ai": {locale: [] for locale in LOCALES},
}
# vertical -> locale -> the header cell of a table column to remove. The AI index's count
# column went in batch 4.3; nothing is left to drop.
DROP_COLUMN: dict[str, dict[str, str]] = {
    "crypto": {},
    "tech": {},
    "ai": {},
}
# vertical -> locale -> (old caption fragment, new caption fragment). None this batch.
CAPTION: dict[str, dict[str, tuple[str, str]]] = {
    "crypto": {},
    "tech": {},
    "ai": {},
}


def _p(text: str) -> dict:
    return {"type": "paragraph", "text": text}


def _h(text: str) -> dict:
    return {"type": "heading", "level": 2, "text": text}


# vertical -> locale -> (anchor, block). A whole block the index does not have yet: batch 4.5
# gave the tech index one paragraph per group that gained articles, and the crypto index a
# whole United Kingdom section. The anchor names a block by what it is: ``link:<slug>``,
# ``heading:<exact text>`` or ``paragraph:<opening text>``, with a leading ``<`` to insert
# before it instead of after. Applied in order, before ``NEW``.
#
# Batches 4.6, 4.7 and 4.4 wave 1 inserted nothing: they were zh-TW only, and prose written
# for zh-TW alone would leave the five locale documents of one index saying different things.
#
# Batch 4.8 is five locales, so it may, and does in two indexes:
#
# * crypto: a South Korea section, the way 4.5 added the United Kingdom's -- a heading and one
#   paragraph in the narrative part after the Japan section, and a link-group heading after the
#   Japan link group, under which ``NEW`` puts the Korea link. The paragraph says only what
#   the Korea article says: suspects, not convictions; no coin, exchange or person named; no
#   price. Besides that, one paragraph of one sentence each in the Taiwan section (the central
#   bank's 9/17 material) and the Japan section (the FSA's 9/25 forum), since both sections
#   already describe their groups' articles. The Korea heading anchors on the Japan forum
#   paragraph inserted just before it, which is why the rows run in this order.
# * tech: one sentence each where Consumer Hardware and Chips and Platforms and Software
#   already describe their articles: Snapdragon after the M6 paragraph, the two security
#   advisories after the App Store paragraph.
#
# The AI index gets no inserted prose. Its narrative names months, not articles past
# 2026-09-14, and its second paragraph -- which named 4.5's six by name -- has not named the
# zh-TW-only batches since; a sentence for 4.8 alone would be the odd one out.
_KR_HEADING = {
    "zh-TW": "韓國：虛擬資產操縱嫌疑案交偵查機關",
    "en": "South Korea: suspected market manipulation cases referred to investigators",
    "ja": "韓国：仮想資産の相場操縦疑い事案、捜査機関へ告発・通報",
    "ko": "한국: 가상자산 불공정거래 혐의 사건, 수사기관에 고발·통보",
    "zh-CN": "韩国：虚拟资产操纵嫌疑案移送侦查机关",
}
_KR_GROUP = {"zh-TW": "韓國", "en": "South Korea", "ja": "韓国", "ko": "한국", "zh-CN": "韩国"}
_KR = {
    "zh-TW": (
        "2026 年 9 月 23 日，韓國金融委員會（與台灣的金管會是不同機關）在第 16 次定例會議中，"
        "對它與金融監督院共同調查的 4 件虛擬資產市場操縱嫌疑案議決處置：1 件告發，3 件通報偵查機關。"
        "其中 3 件是用自動交易程式（API）反覆小額下單、讓掛單簿看起來熱絡的超短線操縱，"
        "另 1 件是虛擬資產營運公司主管與員工僱用造市業者、以借名帳戶互相成交灌出交易量，"
        "以不實方式滿足交易所的上架維持條件。公告沒有點名任何虛擬資產、交易所或當事人，"
        "也沒有寫不當得利金額；4 件的當事人一律是嫌疑人，不是被起訴或定罪的人。"
    ),
    "en": (
        "On September 23, 2026, at its 16th regular meeting, South Korea's Financial Services"
        " Commission (a different agency from Taiwan's Financial Supervisory Commission) resolved on"
        " four suspected virtual-asset market manipulation cases it had investigated together with"
        " the Financial Supervisory Service: one criminal complaint and three notifications to the"
        " investigative authorities. Three of the cases were ultra-short-term price manipulation in"
        " which automated trading programs (APIs) repeated small orders to make the order book look"
        " active; in the fourth, executives and employees of a virtual-asset operating company hired"
        " a market maker and traded between borrowed-name accounts to inflate volume, falsely"
        " meeting an exchange's listing-maintenance requirements. The announcement named no virtual"
        " asset, exchange or individual and gave no figure for illicit gains; the parties in all"
        " four cases are suspects only, not people who have been indicted or convicted."
    ),
    "ja": (
        "2026年9月23日、韓国金融委員会（台湾の金融監督管理委員会とは別の機関）は第16回定例会議で、"
        "金融監督院と共同で調査した仮想資産市場の相場操縦疑いの4件について措置を議決しました。"
        "告発が1件、捜査機関への通報が3件です。うち3件は自動売買プログラム（API）で少額の注文を繰り返し、"
        "板を活発に見せる超短期の相場操縦で、残る1件は仮想資産運営会社の役職員がマーケットメイカーを雇い、"
        "借名口座同士で売買を成立させて出来高を水増しし、取引所の上場維持要件を不正に満たしていたものです。"
        "公表資料はいかなる仮想資産や取引所、当事者の名前も挙げておらず、不当利得の金額も記していません。"
        "4件の当事者はいずれも容疑者であり、起訴または有罪が確定した人物ではありません。"
    ),
    "ko": (
        "2026년 9월 23일, 한국 금융위원회(대만의 금융감독관리위원회와는 다른 기관)는 제16차 정례회의에서"
        " 금융감독원과 공동으로 조사한 가상자산시장 불공정거래 혐의 사건 4건에 대한 조치를 의결했습니다."
        " 고발이 1건, 수사기관 통보가 3건입니다. 이 가운데 3건은 자동매매 프로그램(API)으로 소액 주문을"
        " 반복해 호가창을 활발하게 보이게 한 초단기 시세조종이고, 나머지 1건은 가상자산 운영사 임직원 등이"
        " 마켓메이킹 업자를 고용해 차명 계정끼리 매매를 체결시켜 거래량을 부풀리고 거래소의 상장유지 요건을"
        " 허위로 충족시킨 사건입니다. 발표문은 어떤 가상자산이나 거래소, 당사자의 이름도 밝히지 않았고"
        " 부당이득 금액도 적지 않았습니다. 4건의 당사자는 모두 혐의자일 뿐, 기소되거나 유죄가 확정된 사람이"
        " 아닙니다."
    ),
    "zh-CN": (
        "2026 年 9 月 23 日，韩国金融委员会（与台湾的金融监督管理委员会是不同机关）在第 16 次定例会议中，"
        "对它与金融监督院共同调查的 4 起虚拟资产市场操纵嫌疑案议决处置：1 起告发，3 起通报侦查机关。"
        "其中 3 起是用自动交易程序（API）反复小额下单、让挂单簿看起来活跃的超短线操纵，"
        "另 1 起是虚拟资产运营公司主管与员工雇用做市业者、以借名账户互相成交灌出交易量，"
        "以不实方式满足交易所的上架维持条件。公告没有点名任何虚拟资产、交易所或当事人，"
        "也没有写不当得利金额；4 起案件的当事人一律是嫌疑人，不是被起诉或定罪的人。"
    ),
}
_TW_CBC = {
    "zh-TW": (
        "2026 年 9 月 17 日，中央銀行在理監事會後記者會的書面資料中比較穩定幣、存款代幣與央行數位貨幣（CBDC），"
        "認為三者可在不同層級共存、互補，並表示台灣目前尚無發行零售型 CBDC 的急迫性；"
        "那是央行自己準備的書面問答，不是理事會的決議，也沒有給出任何發行時程。"
    ),
    "en": (
        "On September 17, 2026, Taiwan's Central Bank compared stablecoins, deposit tokens and"
        " central bank digital currency (CBDC) in the written materials of its post-meeting press"
        " conference, saying the three can coexist and complement each other across different"
        " layers and that there is no urgency for Taiwan to issue a retail CBDC; those materials are"
        " a written question-and-answer the Central Bank prepared itself, not a resolution of its"
        " board, and they give no timetable for issuing one."
    ),
    "ja": (
        "2026年9月17日、中央銀行は理監事会後の記者会見資料でステーブルコイン、預金トークン、中央銀行デジタル通貨（CBDC）を比較し、"
        "三者は異なる階層で共存し補い合えるとしたうえで、台湾では一般利用型CBDCを発行する急務はまだないと述べましたが、"
        "これは中央銀行自身が用意した書面の質疑応答であって理事会の決議ではなく、発行時期も示されていません。"
    ),
    "ko": (
        "2026년 9월 17일 중앙은행은 이사·감사 연석회의 후 기자회견 자료에서 스테이블코인, 예금토큰,"
        " 중앙은행디지털화폐(CBDC)를 비교하며 세 가지가 서로 다른 계층에서 공존하고 보완할 수 있고 대만은"
        " 소매형 CBDC를 발행할 시급성이 아직 없다고 밝혔는데, 이는 중앙은행이 스스로 준비한 서면 질의응답으로"
        " 이사회의 의결이 아니며 발행 시기도 제시하지 않았습니다."
    ),
    "zh-CN": (
        "2026 年 9 月 17 日，中央银行在理监事会后记者会的书面资料中比较稳定币、存款代币与央行数字货币（CBDC），"
        "认为三者可在不同层级共存、互补，并表示台湾目前尚无发行零售型 CBDC 的急迫性；"
        "那是央行自己准备的书面问答，不是理事会的决议，也没有给出任何发行时程。"
    ),
}
_JP_FORUM = {
    "zh-TW": (
        "2026 年 9 月 25 日，金融廳又宣布與相關省廳等一起設立「AI時代を見据えたオンチェーン金融フォーラム」"
        "（著眼 AI 時代的鏈上金融論壇），把穩定幣、代幣化存款與國債等的代幣化列入跨部會檢討；"
        "那是設立一個檢討場域，不是修法，也不是核准任何產品。"
    ),
    "en": (
        "On September 25, 2026 the FSA announced that, together with relevant ministries and"
        " agencies, it is setting up the 「AI時代を見据えたオンチェーン金融フォーラム」 (an Onchain"
        " Finance Forum With an Eye on the AI Era), putting stablecoins, tokenized deposits and the"
        " tokenization of government bonds into a cross-ministry review; it sets up a place for"
        " review, not a change of law or the approval of any product."
    ),
    "ja": (
        "2026年9月25日には、金融庁が関係省庁等とともに「AI時代を見据えたオンチェーン金融フォーラム」を立ち上げると公表し、"
        "ステーブルコイン、トークン化預金、国債等のトークン化を省庁横断の検討に載せましたが、"
        "これは検討の場の設置であって、法改正でもいかなる製品の承認でもありません。"
    ),
    "ko": (
        "2026년 9월 25일에는 금융청이 관계 부처 등과 함께 'AI時代を見据えたオンチェーン金融フォーラム'(AI 시대를"
        " 내다본 온체인 금융 포럼)을 신설한다고 발표하며 스테이블코인, 토큰화 예금, 국채 등의 토큰화를 부처 횡단"
        " 검토 대상에 올렸는데, 이는 검토의 장을 만든 것이지 법 개정이나 어떤 상품의 승인이 아닙니다."
    ),
    "zh-CN": (
        "2026 年 9 月 25 日，金融厅又宣布与相关省厅等一起设立“AI時代を見据えたオンチェーン金融フォーラム”"
        "（着眼 AI 时代的链上金融论坛），把稳定币、代币化存款与国债等的代币化列入跨部门检讨；"
        "那是设立一个检讨场域，不是修法，也不是核准任何产品。"
    ),
}
# Where each of those goes: the last paragraph of the Taiwan and the Japan narrative sections,
# by their opening words in each locale.
_TW_LAST = {
    "zh-TW": "paragraph:最容易被忽略的是時間。",
    "en": "paragraph:The easiest thing to overlook is the timing.",
    "ja": "paragraph:最も見落とされやすいのは時期です。",
    "ko": "paragraph:가장 놓치기 쉬운 것은 시간입니다.",
    "zh-CN": "paragraph:最容易被忽略的是时间。",
}
_JP_LAST = {
    "zh-TW": "paragraph:2026 年 7 月 23 日，金融廳在官網公布",
    "en": "paragraph:On July 23, 2026 the FSA published",
    "ja": "paragraph:2026年7月23日、金融庁はウェブサイトで",
    "ko": "paragraph:2026년 7월 23일 금융청은",
    "zh-CN": "paragraph:2026 年 7 月 23 日，金融厅在官网公布",
}
_HW = {
    "zh-TW": (
        "9 月 22 日，高通以茂宜島為電頭，同時發表 Snapdragon 8 Elite Extreme Gen 6 與 Snapdragon 8 Elite"
        " Gen 6 兩款旗艦手機平台；新聞稿除了 2 奈米製程節點之外沒有其他規格數字，也沒有寫代工廠、上市日、"
        "售價或台灣資訊。"
    ),
    "en": (
        "On September 22, Qualcomm unveiled two flagship mobile platforms at once, the Snapdragon 8"
        " Elite Extreme Gen 6 and the Snapdragon 8 Elite Gen 6, in a press release datelined Maui;"
        " beyond the 2nm process node it gives no specification figures, and it names no foundry,"
        " launch date, price or Taiwan information."
    ),
    "ja": (
        "9月22日、Qualcommはマウイを発信地とするプレスリリースで、Snapdragon 8 Elite Extreme Gen 6と"
        "Snapdragon 8 Elite Gen 6という2つのフラッグシップ向けモバイルプラットフォームを同時に発表しましたが、"
        "2nmプロセスノード以外の仕様数値はなく、受託製造先、発売日、価格、台湾情報も記載されていません。"
    ),
    "ko": (
        "9월 22일 퀄컴은 마우이 발신 보도자료로 Snapdragon 8 Elite Extreme Gen 6와 Snapdragon 8 Elite"
        " Gen 6라는 두 종의 플래그십 모바일 플랫폼을 동시에 발표했지만, 보도자료에는 2nm 공정 노드 외의 사양"
        " 수치가 없고 파운드리, 출시일, 가격, 대만 정보도 없습니다."
    ),
    "zh-CN": (
        "9 月 22 日，高通以茂宜岛为电头，同时发表 Snapdragon 8 Elite Extreme Gen 6 与 Snapdragon 8 Elite"
        " Gen 6 两款旗舰手机平台；新闻稿除了 2 纳米制程节点之外没有其他规格数字，也没有写代工厂、上市日、"
        "售价或台湾信息。"
    ),
}
_PF = {
    "zh-TW": (
        "9 月 18 日，Synology 發布資安公告 Synology-SA-26:13，處理 DSM 的八個 CVE 編號，其中兩個由 Synology"
        " 評為 Critical、CVSS 3.1 基本分數 9.8，不需要登入就可能被利用；9 月 22 日，WordPress 發布 7.1.2"
        " 安全版，修補一個自評為嚴重等級的核心漏洞，修補範圍從 7.1 分支回溯到 4.7 分支；兩篇都整理了各自的"
        "修補版本對照，以及怎麼核對自己的版本號。"
    ),
    "en": (
        "On September 18, Synology published security advisory Synology-SA-26:13, covering eight"
        " CVE entries in DSM, two of them rated Critical by Synology, with a CVSS 3.1 base score of"
        " 9.8, and exploitable without authentication; on September 22, WordPress released 7.1.2, a"
        " security release patching a core vulnerability it rates as critical severity, with"
        " patches reaching back from the 7.1 branch to the 4.7 branch; both articles set out the"
        " patched versions and how to check your own version number."
    ),
    "ja": (
        "9月18日、SynologyはDSMのセキュリティ勧告Synology-SA-26:13を公表し、挙げた8件のCVEのうち2件をCritical、"
        "CVSS 3.1基本値9.8、認証不要で悪用されうるものとし、9月22日にはWordPressが、自ら重大と評価したコアの脆弱性を"
        "7.1系から4.7系まで遡って修正するセキュリティリリース7.1.2を公開しており、どちらの記事もそれぞれの修正バージョンと"
        "自分のバージョン番号の確認方法を整理しています。"
    ),
    "ko": (
        "9월 18일 Synology는 DSM 보안 권고문 Synology-SA-26:13을 발표해 CVE 8건 가운데 2건을 Critical,"
        " CVSS 3.1 기본 점수 9.8, 인증 없이 악용될 수 있는 취약점으로 밝혔고, 9월 22일 WordPress는 스스로 심각"
        " 등급으로 평가한 코어 취약점을 7.1 브랜치부터 4.7 브랜치까지 거슬러 패치하는 보안 릴리스 7.1.2를"
        " 배포했으며, 두 기사 모두 각각의 패치 버전과 자신의 버전 번호를 확인하는 방법을 정리했습니다."
    ),
    "zh-CN": (
        "9 月 18 日，Synology 发布网络安全公告 Synology-SA-26:13，处理 DSM 的八个 CVE 编号，其中两个由 Synology"
        " 评为 Critical、CVSS 3.1 基本分数 9.8，无需登录就可能被利用；9 月 22 日，WordPress 发布 7.1.2"
        " 安全版，修复一个自评为严重级别的核心漏洞，修复范围从 7.1 分支回溯到 4.7 分支；两篇都整理了各自的"
        "修复版本对照，以及如何核对自己的版本号。"
    ),
}
_HW_LAST = {
    "zh-TW": "paragraph:8 月 25 日，Apple 發表 M6",
    "en": "paragraph:On August 25, Apple introduced two chips",
    "ja": "paragraph:8月25日、Appleは新しいMac mini",
    "ko": "paragraph:8월 25일, Apple은 새 Mac mini",
    "zh-CN": "paragraph:8 月 25 日，Apple 发表 M6",
}
_PF_LAST = {
    "zh-TW": "paragraph:9 月 16 日，Apple 另外公告 App Store",
    "en": "paragraph:Also on September 16, Apple announced",
    "ja": "paragraph:同じ9月16日、AppleはiOS 27",
    "ko": "paragraph:같은 9월 16일, Apple은 iOS 27",
    "zh-CN": "paragraph:9 月 16 日，Apple 另外公告 App Store",
}
# Batch 4.8's table, as it ran.
_INSERT_4_8: dict[str, dict[str, list[tuple[str, dict]]]] = {
    "crypto": {
        locale: [
            (_TW_LAST[locale], _p(_TW_CBC[locale])),
            (_JP_LAST[locale], _p(_JP_FORUM[locale])),
            # The Korea section follows the Japan section's new last paragraph ...
            ("paragraph:" + _JP_FORUM[locale][:24], _h(_KR_HEADING[locale])),
            ("heading:" + _KR_HEADING[locale], _p(_KR[locale])),
            # ... and its link group follows the Japan link group.
            ("link:crypto-news-jfsa-cybersecurity-20260723", _h(_KR_GROUP[locale])),
        ]
        for locale in LOCALES
    },
    "tech": {
        locale: [
            (_HW_LAST[locale], _p(_HW[locale])),
            (_PF_LAST[locale], _p(_PF[locale])),
        ]
        for locale in LOCALES
    },
    "ai": {locale: [] for locale in LOCALES},
}
# Batch 4.9 inserts nothing: the AI index names months, not articles (see the 4.8 note above).
INSERT: dict[str, dict[str, list[tuple[str, dict]]]] = {
    "crypto": {locale: [] for locale in LOCALES},
    "tech": {locale: [] for locale in LOCALES},
    "ai": {locale: [] for locale in LOCALES},
}

#: A number of articles shown to the reader is wrong from the next batch onwards, so an index
#: states none (``docs/article-architecture.md`` Phase 5, the owner's decision of 2026-09-16).
#: The run refuses while one survives anywhere a reader sees it.
#:
#: What makes a number a count of articles is the unit or the noun beside it, never the digits,
#: and the five locales write it five ways: 38 則 / thirty-eight news reports / 38件 / 38편 /
#: 三十八条. So the quantity is Arabic, a Chinese numeral or an English number word, and then:
#:
#: * ``則 则 篇 편 本`` count written pieces and nothing else, so they stand on their own --
#:   simplified 则 as well as traditional 則, because zh-CN is one of the five locales this
#:   batch publishes and 「一月的三则消息」 is how it writes the sentence 「一月的三則消息」;
#: * ``條 条 件 건`` also count legal clauses and enforcement actions -- ``crypto.md``'s own
#:   vocabulary (「第 5 條」, 「本法第 12 条」, 「3件の行政処分」, 「2건의 제재」) -- so they
#:   count articles only beside a word that says so, which is why this is one rule for all
#:   three verticals rather than three that drift;
#: * in spaced text a quantity a few words from 新聞/ニュース/뉴스/articles/stories is a count
#:   whatever unit it uses ("38 key AI news stories", 「38건의 뉴스」).
#:
#: Years and version numbers are not quantities (2026-09-14, GPT-5.4, Lyria 3.5), and 同/每/第
#: turn a numeral into a determiner (「同一篇完整解析」). A false positive that survives all
#: that is still visible -- the refusal prints what it matched -- which is the right way round.
_QUANTITY = (
    r"(?<![\d.-])\d{1,3}(?![\d.-])"
    r"|(?<![同每這这其另某第])[一二兩两三四五六七八九十百]+"
    r"|(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)-\w+"
    r"|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen"
    r"|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy"
    r"|eighty|ninety)"
)
_PIECES = r"則|则|篇|편|本"
_CLAUSES = r"條|条|件|건"
_ARTICLES = (
    r"新聞|新闻|ニュース|뉴스|記事|기사|文章|報導|报道|事件|사건"
    r"|articles?|stories|reports?|pieces|events?|analyses|news|more"
)
_ADDED = r"收錄|收录|納入|纳入|補上|补上|增補|增补|追補|追加|보완|추가"
_NEAR = r"[^。．.!?！？]{0,12}?"
#: Which indexes the count rule guards. The AI index once printed its article count and must
#: never do so again. The crypto and tech indexes were generated by ``build_*_index.py`` without
#: any count, and their prose refers to documents and announcements by number (「那一篇」,
#: 「兩篇微軟公告」, "three of these articles"), which the rule cannot tell from a count: on
#: 2026-09-18 it matched 17/8/6/2/17 places in the tech index and 1/2/0/0/1 in crypto, none a
#: count of articles. Guarding those two would refuse every update for the wrong reason.
COUNT_RULE = {"crypto": False, "tech": False, "ai": True}

COUNT = re.compile(
    rf"(?:{_QUANTITY})\s*(?:{_PIECES})"
    rf"|(?:{_ARTICLES}|{_ADDED}){_NEAR}(?:{_QUANTITY})\s*(?:{_CLAUSES})"
    rf"|(?:{_QUANTITY})\s*(?:{_CLAUSES}){_NEAR}(?:{_ARTICLES}|{_ADDED})"
    rf"|(?:{_QUANTITY})(?:\W+\w+){{0,2}}\W+(?:{_ARTICLES})"
)


def replace_once(text: str, old: str, new: str, where: str) -> str:
    count = text.count(old)
    if count != 1:
        sys.exit(f"{where}: expected one '{old[:40]}', found {count}")
    return text.replace(old, new)


def edit_block(block: dict, old: str, new: str, where: str) -> None:
    """Replace inside a paragraph, rich or plain. Only ``text`` inlines are touched: an
    ``article`` inline's text is a link label owned by the target article's title."""
    # A callout's body is prose like any paragraph: the AI index's callout states the date the
    # series runs to, which is wrong the day a later event is added. A heading is a sentence
    # too: a group that gains a second kind of document is renamed, not given a second heading.
    if block["type"] in ("paragraph", "callout", "heading"):
        block["text"] = replace_once(block["text"], old, new, where)
        return
    # A summary's items are sentences a reader sees first: the crypto index's first item names
    # the regions the index is arranged by. The edit lands in exactly one item, once, like the
    # text nodes below, so an item that says it twice or two items that both say it refuse.
    if block["type"] in ("summary", "list"):
        items = [i for i, item in enumerate(block["items"]) if old in item]
        if len(items) != 1 or block["items"][items[0]].count(old) != 1:
            sys.exit(f"{where}: expected one '{old[:40]}' in the {block['type']}'s items, found {len(items)}")
        block["items"][items[0]] = block["items"][items[0]].replace(old, new)
        return
    if block["type"] != "rich_paragraph":
        sys.exit(f"{where}: block is a {block['type']}, not a paragraph")
    hits = [node for node in block["inlines"] if node["type"] == "text" and old in node["text"]]
    if len(hits) != 1 or hits[0]["text"].count(old) != 1:
        sys.exit(f"{where}: expected one '{old[:40]}' in the paragraph's text nodes, found {len(hits)}")
    hits[0]["text"] = hits[0]["text"].replace(old, new)


def as_document(doc: dict, where: str) -> GuideDocument:
    """The edited locale, read by the site's own schema. Every edit above works on raw JSON, so
    this is where a source list grown past the cap or a paragraph edited into nonsense is
    caught -- with the field named, rather than as a traceback or a pack CI refuses tomorrow."""
    try:
        return GuideDocument.model_validate(doc)
    except ValueError as error:
        sys.exit(f"{where}: the edited document is invalid\n - " + str(error).replace("\n", "\n   "))


def reader_text(doc: dict, document: GuideDocument) -> list[tuple[str, str]]:
    """(where, text) for everything in the index a reader sees, for the count rule.

    Every block, not only the prose ones: a count in a month heading, a diagram caption or a
    table header is a count. ``doc`` is the raw JSON, which is what can name where a match is;
    ``document`` is the site's own reading of it, and the assert holds this walk to everything
    ``pack_ingest`` reads, so a block type added to the schema -- ``summary`` and ``faq`` were
    added to that walk while this batch was being written -- cannot fall out of the guard."""
    parts = [("title", doc["title"]), ("description", doc["description"])]
    for i, block in enumerate(doc["blocks"]):
        where, kind = f"block {i}", block_kind(block)
        if kind in ("paragraph", "link", "heading"):
            parts.append((where, block_text(block)))
        elif kind == "list":
            parts.extend((f"{where} item", item) for item in block["items"])
        elif kind == "image":
            parts.append((f"{where} caption", block.get("caption", "")))
            parts.append((f"{where} alt", block["alt"]))
        elif kind == "table":
            parts.append((f"{where} caption", block.get("caption", "")))
            parts.extend((f"{where} header", cell) for cell in block["header"])
            parts.extend((f"{where} cell", cell) for row in block["rows"] for cell in row)
        elif kind == "callout":
            parts.append((f"{where} title", block.get("title", "")))
            parts.append((where, block["text"]))
        elif kind == "summary":
            parts.extend((f"{where} item", item) for item in block["items"])
        elif kind == "faq":
            parts.extend((f"{where} question", item["question"]) for item in block["items"])
            parts.extend((f"{where} answer", item["answer"]) for item in block["items"])
        elif kind == "code":
            parts.append((f"{where} label", block["label"]))
            parts.append((where, block["code"]))
    read = "".join(text for _, text in parts)
    missed = [line for line in _document_text(document).split("\n") if line not in read]
    assert not missed, f"reader_text does not read what pack_ingest reads: {missed[:3]}"
    return parts


def find_link(blocks: list[dict], target: str, locale: str) -> int:
    for i, block in enumerate(blocks):
        if block_kind(block) == "link" and link_of(block, locale)[0] == target:
            return i
    sys.exit(f"{locale}: no link to {target} in the index")


def find_anchor(blocks: list[dict], anchor: str, locale: str) -> int:
    """The index of the block an anchor names, whichever kind it names: ``link:<slug>``,
    ``heading:<exact text>`` or ``paragraph:<opening text>`` (a prose block that starts with
    it), each of which must match exactly one block."""
    kind, _, key = anchor.lstrip("<").partition(":")
    if kind == "link":
        return find_link(blocks, key, locale)
    if kind == "heading":
        hits = [i for i, b in enumerate(blocks) if block_kind(b) == "heading" and block_text(b) == key]
    elif kind == "paragraph":
        hits = [i for i, b in enumerate(blocks) if block_kind(b) == "paragraph" and block_text(b).startswith(key)]
    else:
        sys.exit(f"{locale}: an anchor is link:<slug>, heading:<text> or paragraph:<text>, not {anchor!r}")
    if len(hits) != 1:
        sys.exit(f"{locale}: expected one {kind} {key[:40]!r}, found {len(hits)}")
    return hits[0]


def insert_blocks(blocks: list[dict], inserts: list[tuple[str, dict]], locale: str) -> None:
    for anchor, block in inserts:
        if block_kind(block) == "heading" and any(
            block_kind(b) == "heading" and block_text(b) == block_text(block) for b in blocks
        ):
            sys.exit(f"{locale}: the index already has the heading {block_text(block)!r}")
        position = find_anchor(blocks, anchor, locale)
        offset = 0 if anchor.startswith("<") else 1
        blocks.insert(position + offset, block)


def link_block(slug: str, title: str) -> dict:
    """The relinked form the index already uses, so ``pack_cli relink`` has nothing to do."""
    return {"type": "rich_paragraph", "inlines": [{"type": "article", "text": title, "kind": "life", "slug": slug}]}


def has_work(name: str) -> bool:
    """Whether this vertical has anything wired up at all. Every table the run acts on, not the
    three batch 3 had: a vertical whose only pending change is a table cell, a caption or a
    cited source must not be reported as "nothing to add" and skipped in silence."""
    return bool(
        NEW[name]
        or CITED[name]
        or RETITLE[name]
        or any(EDITS[name].values())
        or any(TABLE[name].values())
        or DROP_COLUMN[name]
        or CAPTION[name]
        or any(INSERT[name].values())
    )


def unwritten(name: str) -> list[str]:
    """Every edit of this vertical whose replacement is still an editorial decision -- from all
    four tables, so the pre-flight names the work instead of the run dying half way through."""
    pending = [
        f"{name} {locale}: {old[:40]}"
        for locale in LOCALES
        for _, old, new in EDITS[name][locale]
        if new == TODO
    ]
    pending += [f"{name} {locale} title" for locale, title in RETITLE[name].items() if title == TODO]
    pending += [
        f"{name} {locale} table row {row_label}, column {column}"
        for locale in LOCALES
        for row_label, column, _, new in TABLE[name][locale]
        if new == TODO
    ]
    pending += [f"{name} {locale} caption" for locale, (_, new) in CAPTION[name].items() if new == TODO]
    pending += [
        f"{name} {locale} inserted {block_kind(block)} at {anchor}"
        for locale in LOCALES
        for anchor, block in INSERT[name][locale]
        if TODO in block_text(block)
    ]
    return pending


def misdirected(name: str, locales: list[str]) -> list[str]:
    """Every entry of this vertical written for a locale ``--locale`` leaves out.

    A table keyed by locale is only safe under a narrowed run while nothing is left in the
    rows the run skips: content there would be passed over in silence, which is how one locale
    ends up saying the index was expanded on a day the other four never heard of. Named here,
    before anything is read, rather than found in a diff later."""
    def many(entries: list, thing: str) -> str:
        return f"{len(entries)} {thing}" + ("" if len(entries) == 1 else "s")

    outside = [locale for locale in LOCALES if locale not in locales]
    lines = [
        f"{name} {locale}: {many(EDITS[name][locale], 'sentence edit')}"
        for locale in outside
        if EDITS[name][locale]
    ]
    lines += [
        f"{name} {locale}: {many(INSERT[name][locale], 'inserted block')}"
        for locale in outside
        if INSERT[name][locale]
    ]
    lines += [
        f"{name} {locale}: {many(TABLE[name][locale], 'table cell')}"
        for locale in outside
        if TABLE[name][locale]
    ]
    lines += [f"{name} {locale}: a dropped table column" for locale in outside if locale in DROP_COLUMN[name]]
    lines += [f"{name} {locale}: a caption" for locale in outside if locale in CAPTION[name]]
    lines += [f"{name} {locale}: a new title" for locale in outside if locale in RETITLE[name]]
    return lines


def retitle(index_slug: str, titles: dict[str, str]) -> int:
    """Carry a new index title into the link text of every article that points at it."""
    touched = 0
    for path in sorted(CONTENT.glob("*.json")):
        pack = json.loads(path.read_text(encoding="utf-8"))
        if pack.get("slug") == index_slug:
            continue
        changed = False
        for locale, doc in pack.get("locales", {}).items():
            if locale not in titles:
                continue
            for block in doc["blocks"]:
                if block["type"] != "rich_paragraph":
                    continue
                for node in block["inlines"]:
                    if node["type"] == "article" and node["slug"] == index_slug and node["text"] != titles[locale]:
                        node["text"] = titles[locale]
                        changed = True
        if changed:
            path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            touched += 1
    return touched


def update(vertical, locales: list[str], dry_run: bool) -> None:
    name = vertical.name
    path = CONTENT / f"{vertical.index}.json"
    if not path.is_file():
        sys.exit(f"{name}: {path.name} does not exist yet; the index article is written first")
    index = json.loads(path.read_text(encoding="utf-8"))
    # Linked and cited are different lists: an article may be cited without being new to the
    # index, and reading its pack for a source it does not have is a traceback, not an answer.
    wanted = list(dict.fromkeys([slug for slug, _ in NEW[name]] + CITED[name]))
    for slug in wanted:
        if not (CONTENT / f"{slug}.json").is_file():
            sys.exit(f"{name}: {slug}.json does not exist")
    packs = {slug: json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8")) for slug in wanted}
    for slug, pack in packs.items():
        # A five-locale run wants the five, in the order every pack writes them: a batch that
        # publishes all five and has translated only four is not ready for its index. A run
        # narrowed by ``--locale`` asks only for the locales it is going to read, which is
        # what lets a zh-TW-only batch be linked at all.
        if locales == LOCALES:
            if list(pack["locales"]) != LOCALES:
                sys.exit(f"{slug} does not carry all five locales yet")
        else:
            missing = [locale for locale in locales if locale not in pack["locales"]]
            if missing:
                sys.exit(f"{slug} carries no {', '.join(missing)}; run with --locale=" + ",".join(pack["locales"]))
    already: list[str] = []

    for locale in locales:
        doc = index["locales"][locale]
        blocks = doc["blocks"]
        if locale in RETITLE[name]:
            doc["title"] = RETITLE[name][locale]
        for target, old, new in EDITS[name][locale]:
            if target == "description":
                doc["description"] = replace_once(doc["description"], old, new, f"{locale} description")
            else:
                # The block index is written by hand and shifts every time the index grows a
                # link, so a stale one is the ordinary mistake in this table. Named, like every
                # other misdirection here, rather than left to an IndexError.
                if not isinstance(target, int) or not 0 <= target < len(blocks):
                    sys.exit(f"{locale}: there is no block {target}; the index has {len(blocks)}")
                edit_block(blocks[target], old, new, f"{locale} block {target}")

        table = next((b for b in blocks if b["type"] == "table"), None)
        if TABLE[name][locale] or locale in DROP_COLUMN[name] or locale in CAPTION[name]:
            if table is None:
                sys.exit(f"{locale}: the index has no table to edit")
            for row_label, column, old, new in TABLE[name][locale]:
                row = next((r for r in table["rows"] if r[0] == row_label), None)
                if row is None:
                    sys.exit(f"{locale}: no table row labelled {row_label}")
                if not 0 <= column < len(row):
                    sys.exit(f"{locale}: row {row_label} has {len(row)} columns, no column {column}")
                if row[column] != old:
                    sys.exit(f"{locale}: row {row_label} column {column} is {row[column]!r}, expected {old!r}")
                row[column] = new
            if locale in DROP_COLUMN[name]:
                label = DROP_COLUMN[name][locale]
                if table["header"].count(label) != 1:
                    sys.exit(f"{locale}: expected one table column headed {label!r}, found {table['header']}")
                column = table["header"].index(label)
                if len(table["header"]) < 3:
                    sys.exit(f"{locale}: dropping {label!r} would leave a table of one column")
                del table["header"][column]
                for row in table["rows"]:
                    del row[column]
            if locale in CAPTION[name]:
                old, new = CAPTION[name][locale]
                table["caption"] = replace_once(table["caption"], old, new, f"{locale} caption")

        insert_blocks(blocks, INSERT[name][locale], locale)

        for slug, after in NEW[name]:
            if any(block_kind(b) == "link" and link_of(b, locale)[0] == slug for b in blocks):
                sys.exit(f"{locale}: {slug} is already linked")
            # A bare slug anchors on that article's link; a ``heading:`` anchor -- per locale
            # when the heading's text differs by locale -- places the first link of a group the
            # index gains in this batch, straight after its inserted heading.
            anchor = after[locale] if isinstance(after, dict) else after
            position = find_anchor(blocks, anchor, locale) if ":" in anchor else find_link(blocks, anchor.lstrip("<"), locale)
            offset = 0 if anchor.startswith("<") else 1
            blocks.insert(position + offset, link_block(slug, packs[slug]["locales"][locale]["title"]))

        # The index cites one source per article, and it already cites nine -- several of them
        # this batch's own subjects. A repeat is the same URL listed twice under the article,
        # and the cap is the schema's, so both are decided here rather than discovered by the
        # importer after the file is written.
        cited = doc["sources"]
        seen = {source["url"] for source in cited}
        for slug in CITED[name]:
            sources = packs[slug]["locales"][locale]["sources"]
            if not sources:
                sys.exit(f"{locale}: {slug} carries no source for the index to cite")
            source = dict(sources[0])
            if not source.get("checked_on"):
                sys.exit(f"{locale}: the source cited from {slug} has no checked_on")
            if source["url"] in seen:
                already.append(slug)
                continue
            if len(cited) >= MAX_SOURCES:
                sys.exit(
                    f"{locale}: the index already cites {len(cited)} sources and a document carries"
                    f" at most {MAX_SOURCES}; {slug}'s source does not fit. Cite fewer articles."
                )
            cited.append(source)
            seen.add(source["url"])

        document = as_document(doc, f"{name} {locale}")
        left = [(where, m.group(0))
                for where, value in reader_text(doc, document) for m in COUNT.finditer(value)]
        if left and COUNT_RULE[name]:
            sys.exit(f"{locale}: the index still shows an article count: {left}")

    try:
        ArticlePack.model_validate(index)
    except ValueError as error:
        sys.exit(f"{name}: the updated index is not a valid pack\n - " + str(error).replace("\n", "\n   "))

    # One serialisation, whether it is printed or written, so a dry run shows the bytes the
    # real run would put on disk -- indentation and all -- and never a reflowed near-miss.
    before = path.read_text(encoding="utf-8")
    after = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    counted = {locale: len(index["locales"][locale]["blocks"]) for locale in LOCALES}
    if dry_run:
        sys.stdout.writelines(
            difflib.unified_diff(
                before.splitlines(keepends=True),
                after.splitlines(keepends=True),
                fromfile=f"a/{path.name}",
                tofile=f"b/{path.name}",
            )
        )
        print(f"{name}: dry run over {', '.join(locales)}, nothing written;", counted)
        if RETITLE[name]:
            print(f"{name}: dry run, the link text in the other packs is not refreshed either")
        return

    path.write_text(after, encoding="utf-8")
    print(f"{name}: index updated,", counted)
    if already:
        print(f"{name}: already cited, not added again:", sorted(set(already)))
    if RETITLE[name]:
        print(f"{name}: link text refreshed in {retitle(vertical.index, RETITLE[name])} packs")


def parse_args(argv: list[str]) -> tuple[list[str], list[str], bool]:
    """``(verticals, locales, dry run)`` off the command line.

    ``--locale`` may be repeated and may carry a comma list; without it the run is all five
    locales, in the order every pack writes them, which is what every batch up to 4.5 was. The
    locales are returned in that same order however they were typed, so two runs of the same
    command cannot differ in which locale was edited first."""
    names: list[str] = []
    chosen_locales: list[str] = []
    dry_run = False
    rest = list(argv)
    while rest:
        argument = rest.pop(0)
        if argument == "--dry-run":
            dry_run = True
        elif argument == "--locale" or argument.startswith("--locale="):
            value = argument.partition("=")[2] if "=" in argument else (rest.pop(0) if rest else "")
            wanted = [part.strip() for part in value.split(",") if part.strip()]
            if not wanted:
                sys.exit("--locale takes a locale: --locale=zh-TW, or --locale=zh-TW,en")
            chosen_locales += wanted
        elif argument.startswith("-"):
            sys.exit(f"unknown option {argument}; this script takes --locale=<locale> and --dry-run")
        else:
            names.append(argument)
    unknown = [n for n in names if n not in BY_NAME]
    if unknown:
        sys.exit(f"unknown vertical {unknown}; one of " + ", ".join(BY_NAME))
    stray = [locale for locale in chosen_locales if locale not in LOCALES]
    if stray:
        sys.exit(f"unknown locale {stray}; one of " + ", ".join(LOCALES))
    locales = [locale for locale in LOCALES if locale in chosen_locales] or list(LOCALES)
    return names, locales, dry_run


def main() -> None:
    # The dry run prints a diff of Chinese, Japanese and Korean text; a console that is not
    # already UTF-8 would raise UnicodeEncodeError part way through it.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    named, locales, dry_run = parse_args(sys.argv[1:])
    chosen = [BY_NAME[n] for n in named] if named else list(VERTICALS)
    # Only the verticals this run touches: an AI sentence nobody has written yet is no reason
    # to refuse a crypto run that has nothing to do with it.
    pending = [line for vertical in chosen for line in unwritten(vertical.name)]
    if pending:
        sys.exit("edits still to write:\n - " + "\n - ".join(pending))
    if locales != LOCALES:
        # What a narrowed run may not do. Each of these three would leave the five documents of
        # one index disagreeing with each other, and four of them unread by whoever ran this.
        skipped = [line for vertical in chosen for line in misdirected(vertical.name, locales)]
        if skipped:
            sys.exit(
                f"this run is {', '.join(locales)}, and these edits are written for a locale it"
                " does not touch:\n - " + "\n - ".join(skipped)
            )
        citing = [vertical.name for vertical in chosen if CITED[vertical.name]]
        if citing:
            sys.exit(
                f"{', '.join(citing)}: CITED needs all five locales -- a source added to one"
                " locale document is a source the other four do not carry. Run without"
                " --locale, or empty the table."
            )
        renaming = [vertical.name for vertical in chosen if RETITLE[vertical.name]]
        if renaming:
            sys.exit(
                f"{', '.join(renaming)}: RETITLE needs all five locales -- it rewrites the link"
                " text of every pack that points at the index, and the locales this run skips"
                " would keep pointing at a title that no longer exists. Run without --locale."
            )
    for vertical in chosen:
        if not has_work(vertical.name):
            print("nothing to add:", vertical.name)
            continue
        update(vertical, locales, dry_run)


if __name__ == "__main__":
    main()
