"""Add this batch's articles to their vertical's index, in place, in five languages.

``update_index.py [crypto|tech|ai]...`` -- with no vertical named, every vertical that has
something to add. Run once, after that vertical's packs carry all five locales. Every sentence
edit is an exact replacement that must match once, so a second run fails instead of editing
twice.

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
"""
from __future__ import annotations

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
EXPANDED_ON = "2026-09-18"
EXPANDED = {
    "zh-TW": "2026 年 9 月 18 日",
    "en": "September 18, 2026",
    "ja": "2026年9月18日",
    "ko": "2026년 9월 18일",
    "zh-CN": "2026 年 9 月 18 日",
}

# vertical -> (slug, where to put the link). ``after`` is the existing slug to place the link
# after (a leading "<" means before it), or an anchor of the ``INSERT`` kind -- per locale,
# as a dict, when it names a heading whose text differs by locale. Applied in order: an entry
# may name a slug inserted just before it.
#
# Batch 4.5 (2026-09-18): the news since 2026-09-16. The AI index lists by month, so the six
# go after September's last link; the tech and crypto indexes group by topic and region, so
# each new link goes into its group, and the crypto index gains a United Kingdom group.
NEW: dict[str, list[tuple[str, object]]] = {
    "crypto": [
        ("crypto-news-cftc-passive-software-20260917", "crypto-news-sec-regulation-crypto-assets-20260821"),
        ("crypto-news-fca-perimeter-guidance-20260916", {"zh-TW": "heading:英國", "en": "heading:The United Kingdom", "ja": "heading:英国", "ko": "heading:영국", "zh-CN": "heading:英国"}),
        ("crypto-news-fca-p2p-crypto-crackdown-20260917", "crypto-news-fca-perimeter-guidance-20260916"),
    ],
    "tech": [
        ("tech-news-app-store-bundles-multiseat-20260916", "tech-news-pixel-drop-20260915"),
        ("tech-news-taiwan-matsu-cable-tm4-20260918", "tech-news-taiwan-matsu-cable-20260623"),
        ("tech-news-eu-kids-act-20260917", "tech-news-eu-cra-reporting-20260911"),
        ("tech-news-apple-att-eu-20260916", "tech-news-apple-eu-business-terms-20260818"),
    ],
    "ai": [
        ("ai-news-chatgpt-sponsored-agents-20260916", "ai-news-gemini-38-live-20260915"),
        ("ai-news-firefox-smart-window-mistral-20260916", "ai-news-chatgpt-sponsored-agents-20260916"),
        ("ai-news-openai-misalignment-reports-20260917", "ai-news-firefox-smart-window-mistral-20260916"),
        ("ai-news-anthropic-pace-metrics-20260917", "ai-news-openai-misalignment-reports-20260917"),
        ("ai-news-astra-for-law-20260917", "ai-news-anthropic-pace-metrics-20260917"),
        ("ai-news-google-cc-family-agent-20260918", "ai-news-astra-for-law-20260917"),
    ],
}
# vertical -> the articles whose first source the index cites. A source the index already
# carries is skipped, not appended twice. Every article of this batch fits under the cap
# (crypto 11 + 3, tech 13 + 4, AI 13 + 6, against a cap of 20).
CITED: dict[str, list[str]] = {
    "crypto": [slug for slug, _ in NEW["crypto"]],
    "tech": [slug for slug, _ in NEW["tech"]],
    "ai": [slug for slug, _ in NEW["ai"]],
}

# vertical -> locale -> new title. Empty leaves the title alone: none of the three titles
# names a date or a count, so none of them is wrong after this batch.
RETITLE: dict[str, dict[str, str]] = {
    "crypto": {},
    "tech": {},
    "ai": {},
}

# vertical -> locale -> (where, old, new). ``where`` is "description" or a block index.
#
# The AI index: its opening, closing and callout sentences name the days it was expanded, and
# batch 4.3 wrote them as a list of two dates. Rewritten once more to "expanded several times
# since, most recently on <EXPANDED_ON>", so the next batch edits the date and nothing else;
# the events it covers now run to 2026-09-18. Its second paragraph gains one undated sentence
# naming this batch's six subjects. The tech and crypto indexes: the check-date sentence gains
# the expansion date, the crypto opening widens its date range and its list of regions, the
# crypto description names the new region, and one crypto heading is renamed for the CFTC
# letter that joins the SEC documents. The block indexes are those of the indexes as they
# read on 2026-09-18, before this run's inserts.
EDITS: dict[str, dict[str, list[tuple[object, str, str]]]] = {
    "crypto": {
        "zh-TW": [
            ("description", "依台灣、美國、歐盟、日本四個地區，", "依台灣、美國、英國、歐盟、日本五個地區，"),
            ("description", "歐盟 MiCA 過渡期與支付規則的銜接、", "英國 FCA 的監理範圍指引與執法行動、歐盟 MiCA 過渡期與支付規則的銜接、"),
            (0, "這一批的事件日落在 2026 年 2 月到 8 月之間。內容依台灣、美國、歐盟、日本四個地區編排", "這一批的事件日落在 2026 年 2 月到 9 月之間。內容依台灣、美國、英國、歐盟、日本五個地區編排"),
            (1, "本索引於 2026 年 9 月 17 日查核。", f"本索引於 2026 年 9 月 17 日查核，{EXPANDED['zh-TW']}增補。"),
            (33, "美國：證券法的解釋與提案", "美國：證券法的解釋、提案與 CFTC 職員函"),
        ],
        "en": [
            ("description", "arranged by jurisdiction — Taiwan, the United States, the European Union, Japan:", "arranged by jurisdiction — Taiwan, the US, the UK, the EU, Japan:"),
            ("description", "and the reports published by Japan's FSA.", "the UK FCA's perimeter guidance, and Japan's FSA reports."),
            (0, "fall between February and August 2026. It is arranged by four jurisdictions — Taiwan, the United States, the European Union and Japan —", "fall between February and September 2026. It is arranged by five jurisdictions — Taiwan, the United States, the United Kingdom, the European Union and Japan —"),
            (1, "This index was checked on September 17, 2026.", f"This index was checked on September 17, 2026 and expanded on {EXPANDED['en']}."),
            (33, "The United States: the securities law interpretation and proposal", "The United States: the securities law interpretation, the proposal and a CFTC staff letter"),
        ],
        "ja": [
            ("description", "台湾、米国、EU、日本の四つの地域ごとに", "台湾、米国、英国、EU、日本の五つの地域ごとに"),
            ("description", "日本の金融庁が公表した報告書を取り上げます。", "英国FCAの規制範囲ガイダンスと執行措置、日本の金融庁が公表した報告書を取り上げます。"),
            (0, "2026年2月から8月の間にあります。内容は台湾、米国、EU、日本の四つの地域ごとに並べ", "2026年2月から9月の間にあります。内容は台湾、米国、英国、EU、日本の五つの地域ごとに並べ"),
            (1, "この索引は2026年9月17日に確認しました。", f"この索引は2026年9月17日に確認し、{EXPANDED['ja']}に追補しました。"),
            (33, "米国：証券法の解釈と提案", "米国：証券法の解釈と提案、CFTCの職員レター"),
        ],
        "ko": [
            ("description", "대만, 미국, EU, 일본 네 지역별로", "대만, 미국, 영국, EU, 일본 다섯 지역별로"),
            ("description", "일본 금융청이 공개한 보고서를 다룹니다.", "영국 FCA의 규제 범위 지침과 집행 조치, 일본 금융청이 공개한 보고서를 다룹니다."),
            (0, "2026년 2월에서 8월 사이에 있습니다. 내용은 대만, 미국, EU, 일본 네 지역별로 배열했고", "2026년 2월에서 9월 사이에 있습니다. 내용은 대만, 미국, 영국, EU, 일본 다섯 지역별로 배열했고"),
            (1, "이 색인은 2026년 9월 17일에 확인했습니다.", f"이 색인은 2026년 9월 17일에 확인했고, {EXPANDED['ko']}에 보완했습니다."),
            (33, "미국: 증권법의 해석과 제안", "미국: 증권법의 해석과 제안, CFTC 직원 서한"),
        ],
        "zh-CN": [
            ("description", "依台湾、美国、欧盟、日本四个地区，", "依台湾、美国、英国、欧盟、日本五个地区，"),
            ("description", "欧盟 MiCA 过渡期与支付规则的衔接、", "英国 FCA 的监管范围指引与执法行动、欧盟 MiCA 过渡期与支付规则的衔接、"),
            (0, "这一批的事件日落在 2026 年 2 月到 8 月之间。内容依台湾、美国、欧盟、日本四个地区编排", "这一批的事件日落在 2026 年 2 月到 9 月之间。内容依台湾、美国、英国、欧盟、日本五个地区编排"),
            (1, "本索引于 2026 年 9 月 17 日核查。", f"本索引于 2026 年 9 月 17 日核查，{EXPANDED['zh-CN']}增补。"),
            (33, "美国：证券法的解释与提案", "美国：证券法的解释、提案与 CFTC 职员函"),
        ],
    },
    "tech": {
        "zh-TW": [(1, "本索引於 2026 年 9 月 17 日查核。", f"本索引於 2026 年 9 月 17 日查核，{EXPANDED['zh-TW']}增補。")],
        "en": [(1, "This index was checked on September 17, 2026.", f"This index was checked on September 17, 2026 and expanded on {EXPANDED['en']}.")],
        "ja": [(1, "本索引は2026年9月17日に確認しました。", f"本索引は2026年9月17日に確認し、{EXPANDED['ja']}に追補しました。")],
        "ko": [(1, "본 색인은 2026년 9월 17일에 검증했습니다.", f"본 색인은 2026년 9월 17일에 검증했고, {EXPANDED['ko']}에 보완했습니다.")],
        "zh-CN": [(1, "本索引于 2026 年 9 月 17 日查核。", f"本索引于 2026 年 9 月 17 日查核，{EXPANDED['zh-CN']}增补。")],
    },
    "ai": {
        "zh-TW": [
            (0, "這份索引於 2026-09-14 查核，2026-09-15 與 2026-09-18 兩度增補，", f"這份索引於 2026-09-14 查核，之後多次增補（最近一次 {EXPANDED_ON}），"),
            (1, "Habitat 儲存架構與 Gemini 3.8 Live。", "Habitat 儲存架構與 Gemini 3.8 Live。之後又補上 9 月 16 日至 18 日的新消息：ChatGPT 廣告的 Sponsored Agents 測試、Firefox Smart Window 加入 Mistral 的模型、OpenAI 的失準通報框架、Anthropic 的三項前沿 AI 指標、Astra for Law，以及 Google CC 的家庭版。"),
            (24, "本專輯最初整理到 2026-09-14，之後在 2026-09-15 與 2026-09-18 增補，", f"本專輯最初整理到 2026-09-14，之後多次增補（最近一次 {EXPANDED_ON}），"),
            (25, "本輯收錄的事件到 2026-09-15 為止，最後增補於 2026-09-18。", f"本輯收錄的事件到 2026-09-18 為止，最後增補於 {EXPANDED_ON}。"),
        ],
        "en": [
            (0, "Verified as of 2026-09-14 and expanded on 2026-09-15 and 2026-09-18, this index", f"Verified as of 2026-09-14 and expanded several times since (most recently on {EXPANDED_ON}), this index"),
            (1, "the Habitat storage platform and Gemini 3.8 Live.", "the Habitat storage platform and Gemini 3.8 Live. Later additions cover the news of September 16 to 18: the Sponsored Agents test in ChatGPT ads, Mistral's model joining Firefox Smart Window, OpenAI's misalignment reporting framework, Anthropic's three frontier-AI metrics, Astra for Law, and the family version of Google's CC."),
            (24, "This editorial feature was first compiled through 2026-09-14 and expanded on 2026-09-15 and 2026-09-18,", f"This editorial feature was first compiled through 2026-09-14 and expanded several times since (most recently on {EXPANDED_ON}),"),
            (25, "This series covers events through 2026-09-15 and was last expanded on 2026-09-18.", f"This series covers events through 2026-09-18 and was last expanded on {EXPANDED_ON}."),
        ],
        "ja": [
            (0, "このインデックスは2026-09-14に検証され、2026-09-15と2026-09-18に追補したもので、", f"このインデックスは2026-09-14に検証され、その後複数回追補（最終追補は{EXPANDED_ON}）したもので、"),
            (1, "ストレージ基盤Habitat、Gemini 3.8 Liveです。", "ストレージ基盤Habitat、Gemini 3.8 Liveです。その後、9月16日から18日のニュースも追加しました。ChatGPT広告のSponsored Agentsテスト、Firefox Smart WindowへのMistralモデルの追加、OpenAIのミスアライメント報告の枠組み、Anthropicの3つのフロンティアAI指標、Astra for Law、Google CCの家族版です。"),
            (24, "本特集は2026-09-14時点でまとめ、2026-09-15と2026-09-18に追補した編集特集であり、", f"本特集は2026-09-14時点でまとめ、その後複数回追補（最終追補は{EXPANDED_ON}）した編集特集であり、"),
            (25, "本特集の対象は2026-09-15までの出来事で、最終追補は2026-09-18です。", f"本特集の対象は2026-09-18までの出来事で、最終追補は{EXPANDED_ON}です。"),
        ],
        "ko": [
            (0, "2026-09-14에 검증되고 2026-09-15와 2026-09-18에 보완된 이 색인은", f"2026-09-14에 검증되고 이후 여러 차례 보완된(마지막 보완 {EXPANDED_ON}) 이 색인은"),
            (1, "스토리지 기반 Habitat, Gemini 3.8 Live입니다.", "스토리지 기반 Habitat, Gemini 3.8 Live입니다. 이후 9월 16일부터 18일까지의 소식도 추가했습니다. ChatGPT 광고의 Sponsored Agents 테스트, Firefox Smart Window에 Mistral 모델 추가, OpenAI의 미스얼라인먼트 보고 프레임워크, Anthropic의 프런티어 AI 지표 세 가지, Astra for Law, 그리고 Google CC의 가족용 버전입니다."),
            (24, "이번 특집은 2026-09-14 기준으로 정리한 뒤 2026-09-15와 2026-09-18에 보완한 편집 특집으로,", f"이번 특집은 2026-09-14 기준으로 정리한 뒤 이후 여러 차례 보완한(마지막 보완 {EXPANDED_ON}) 편집 특집으로,"),
            (25, "본 특집은 2026-09-15까지의 사건을 다루며, 마지막 보완은 2026-09-18입니다.", f"본 특집은 2026-09-18까지의 사건을 다루며, 마지막 보완은 {EXPANDED_ON}입니다."),
        ],
        "zh-CN": [
            (0, "这份索引于 2026-09-14 查核，2026-09-15 与 2026-09-18 两度增补，", f"这份索引于 2026-09-14 查核，之后多次增补（最近一次 {EXPANDED_ON}），"),
            (1, "Habitat 存储架构与 Gemini 3.8 Live。", "Habitat 存储架构与 Gemini 3.8 Live。之后又补上 9 月 16 日至 18 日的新消息：ChatGPT 广告的 Sponsored Agents 测试、Firefox Smart Window 加入 Mistral 的模型、OpenAI 的失准通报框架、Anthropic 的三项前沿 AI 指标、Astra for Law，以及 Google CC 的家庭版。"),
            (24, "本专辑最初整理到 2026-09-14，之后在 2026-09-15 与 2026-09-18 增补，", f"本专辑最初整理到 2026-09-14，之后多次增补（最近一次 {EXPANDED_ON}），"),
            (25, "本辑收录的事件到 2026-09-15 为止，最后增补于 2026-09-18。", f"本辑收录的事件到 2026-09-18 为止，最后增补于 {EXPANDED_ON}。"),
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


# vertical -> locale -> (anchor, block). A whole block the index does not have yet: the tech
# index's prose describes every article in its group, so each group that gains articles gets
# one paragraph after its last one; the crypto index gains a United Kingdom section -- a prose
# heading and paragraph before Japan's, and a link-list heading before Japan's -- and a
# paragraph on the CFTC letter after the securities-law paragraph. The anchor names a block by
# what it is: ``link:<slug>``, ``heading:<exact text>`` or ``paragraph:<opening text>``, with a
# leading ``<`` to insert before it instead of after. Applied in order, before ``NEW``.
INSERT: dict[str, dict[str, list[tuple[str, dict]]]] = {
    "crypto": {
        "zh-TW": [
            ("paragraph:證券法這一邊，解釋令與提案規則性質不同。", _p("商品交易法這一邊，2026 年 9 月 17 日 CFTC 市場參與者部門發布職員無異議函 Letter 26-25，把同年 3 月只有單一申請人能援用的 Letter 26-09，擴大到所有符合十項條件的被動軟體提供者；那是部門層級的職員函，信中寫明對委員會沒有拘束力，也沒有失效日期。")),
            ("<heading:日本：建議報告、後續立法與資安", _h("英國：監理範圍指引定案，點對點交易執法")),
            ("<heading:日本：建議報告、後續立法與資安", _p("英國金融行為監理總署（FCA）在 2026 年 9 月 16 日發布政策聲明 PS26/18《加密資產監理範圍指引》，說明加密資產活動在什麼情況下需要 FCA 授權：授權申請窗口 9 月 30 日開放，新制本身要到 2027 年 10 月 25 日才生效，既有登記不會自動轉換。9 月 17 日，FCA 又公布與稅務海關總署、倫敦警察廳於 9 月 10 日對倫敦 3 處涉嫌非法點對點加密資產交易場所採取的行動，3 處都收到停止並終止通知書；登記義務只及於以營業方式經營者，個人之間的點對點交易不需要登記。")),
            ("<heading:日本", _h("英國")),
        ],
        "en": [
            ("paragraph:On the securities law side, an interpretation and a proposed rule are ", _p("On the commodities side, on September 17, 2026 the CFTC's Market Participants Division issued staff no-action letter 26-25, extending to every passive software provider that meets ten conditions the position that Letter 26-09 had given a single applicant in March; it is a staff letter at division level, which says itself that it does not bind the Commission, and it carries no expiry date.")),
            ("<heading:Japan: a report of recommendations, the legislation that followed, and cybersecurity", _h("The United Kingdom: perimeter guidance finalised, and enforcement against peer-to-peer trading")),
            ("<heading:Japan: a report of recommendations, the legislation that followed, and cybersecurity", _p("On September 16, 2026 the Financial Conduct Authority published policy statement PS26/18, its cryptoasset perimeter guidance on when a cryptoasset activity needs FCA authorisation: the application window opens on September 30, the regime itself commences on October 25, 2027, and existing registrations do not convert automatically. On September 17 the FCA announced the action it had taken on September 10 with HM Revenue & Customs and the Metropolitan Police at three London premises suspected of illegal peer-to-peer cryptoasset trading, all three served with cease and desist notices; the registration duty reaches only those trading by way of business, and peer-to-peer trading on a personal basis needs no registration.")),
            ("<heading:Japan", _h("The United Kingdom")),
        ],
        "ja": [
            ("paragraph:証券法の側では、解釈と提案規則は性質が異なります。", _p("商品取引法の側では、2026年9月17日にCFTCの市場参加者部門が職員によるノーアクションレター26-25を発出し、3月に単一の申請者だけが援用できたレター26-09の立場を、10項目の条件を満たすすべてのパッシブ・ソフトウェア提供者に広げました。部門レベルの職員レターであり、委員会を拘束しないと自ら記しており、失効日もありません。")),
            ("<heading:日本：提言の報告書、その後の立法、そしてサイバーセキュリティ", _h("英国：規制範囲ガイダンスの確定と、P2P取引への執行")),
            ("<heading:日本：提言の報告書、その後の立法、そしてサイバーセキュリティ", _p("英国金融行為監督機構（FCA）は2026年9月16日、政策声明PS26/18「暗号資産の規制範囲ガイダンス」を公表し、暗号資産に関する活動がどのような場合にFCAの認可を必要とするかを示しました。認可申請の受付は9月30日に始まり、新制度そのものは2027年10月25日に施行され、既存の登録は自動的には移行しません。9月17日にはFCAが、歳入関税庁およびロンドン警視庁と9月10日にロンドン3か所の違法なP2P暗号資産取引が疑われる拠点に対して行った措置を公表し、3か所すべてに停止命令通知が交付されました。登録義務は事業として取引を行う者に限られ、個人間のP2P取引に登録は不要です。")),
            ("<heading:日本", _h("英国")),
        ],
        "ko": [
            ("paragraph:증권법 쪽에서는 해석과 제안 규칙의 성격이 다릅니다.", _p("상품거래법 쪽에서는 2026년 9월 17일 CFTC 시장참가자부가 직원 무이의 서한 26-25를 발행해, 3월에 단일 신청자만 원용할 수 있었던 서한 26-09의 입장을 열 가지 조건을 충족하는 모든 패시브 소프트웨어 제공자로 넓혔습니다. 부서 차원의 직원 서한으로, 위원회를 구속하지 않는다고 스스로 적고 있으며 실효일도 없습니다.")),
            ("<heading:일본: 제언 보고서, 그 뒤의 입법, 그리고 사이버보안", _h("영국: 규제 범위 지침 확정, 그리고 P2P 거래 집행")),
            ("<heading:일본: 제언 보고서, 그 뒤의 입법, 그리고 사이버보안", _p("영국 금융행위감독청(FCA)은 2026년 9월 16일 정책성명 PS26/18 '가상자산 규제 범위 지침'을 발표해 가상자산 활동이 어떤 경우에 FCA 인가를 필요로 하는지 설명했습니다. 인가 신청 창구는 9월 30일에 열리고, 새 제도 자체는 2027년 10월 25일에야 시행되며, 기존 등록은 자동으로 전환되지 않습니다. 9월 17일에는 FCA가 국세관세청, 런던광역경찰청과 함께 9월 10일 런던의 불법 P2P 가상자산 거래가 의심되는 3곳에 취한 조치를 공개했고, 3곳 모두 중지 통지서를 받았습니다. 등록 의무는 영업으로 거래하는 자에게만 미치며, 개인 간 P2P 거래에는 등록이 필요 없습니다.")),
            ("<heading:일본", _h("영국")),
        ],
        "zh-CN": [
            ("paragraph:证券法这一边，解释令与提案规则性质不同。", _p("商品交易法这一边，2026 年 9 月 17 日 CFTC 市场参与者部门发布职员无异议函 Letter 26-25，把同年 3 月只有单一申请人能援用的 Letter 26-09，扩大到所有符合十项条件的被动软件提供者；那是部门层级的职员函，信中写明对委员会没有约束力，也没有失效日期。")),
            ("<heading:日本：建议报告、后续立法与网络安全", _h("英国：监管范围指引定案，点对点交易执法")),
            ("<heading:日本：建议报告、后续立法与网络安全", _p("英国金融行为监管局（FCA）在 2026 年 9 月 16 日发布政策声明 PS26/18《加密资产监管范围指引》，说明加密资产活动在什么情况下需要 FCA 授权：授权申请窗口 9 月 30 日开放，新制本身要到 2027 年 10 月 25 日才生效，既有登记不会自动转换。9 月 17 日，FCA 又公布与税务海关总署、伦敦警察厅于 9 月 10 日对伦敦 3 处涉嫌非法点对点加密资产交易场所采取的行动，3 处都收到停止并终止通知书；登记义务只及于以营业方式经营者，个人之间的点对点交易不需要登记。")),
            ("<heading:日本", _h("英国")),
        ],
    },
    "tech": {
        "zh-TW": [
            ("paragraph:Google 在 9 月 15 日發布 9 月 Pixel Drop", _p("9 月 16 日，Apple 另外公告 App Store 訂閱隨 iOS 27 而來的變動：多個訂閱可合併成組合方案或套組，最多五個開發者參與；多名額購買在 App Store Connect 預設開啟，大量採購預定 10 月 22 日推出，群組購買只預告今年冬天。官方頁面沒有寫出任何國家或地區。")),
            ("paragraph:9 月 15 日，數位發展部啟動「臺灣主權AI訓練語料庫」", _p("9 月 18 日，中華電信宣布全長近 300 公里的臺馬第四海纜已完成建置、登陸與測通，臺馬聯外海纜由兩條增為三條，整體傳輸容量提升至約 1.9 Tbps；公告寫投入近新臺幣 14 億元，但沒有寫商轉日或啟用日，數位發展部的「新聞發布」頁在本站查核當天也沒有對應公告。")),
            ("paragraph:Apple 在 8 月 18 日宣布調整歐盟地區的 App 商業條款", _p("9 月 16 日，Apple 在開發者新聞公告歐盟的 App 追蹤透明度詢問框另有版本：自 iOS 27.2 與 iPadOS 27.2 起，德國、法國、義大利、波蘭與羅馬尼亞五國只能使用新版，歐盟的裝置設定改名，開發者可在使用者上次回答滿一年後再問一次；Apple 沒有點名主管機關，也沒有說依據哪一部法律。9 月 17 日，歐盟執委會通過 KIDS Act 提案，規定社群媒體平台不得讓未滿 13 歲的兒童持有帳號、15 歲才能自己開帳號；那是送交歐洲議會與理事會審議的提案，官方頁面沒有寫生效日。")),
        ],
        "en": [
            ("paragraph:Google published its September Pixel Drop on September 15", _p("Also on September 16, Apple announced the subscription changes that come with iOS 27: several subscriptions may be sold as one purchase, as a bundle or a suite, with up to five developers taking part; multiseat purchases are on by default in App Store Connect, volume purchasing is scheduled for October 22 and group purchases are only promised for this winter. The official pages name no country or region.")),
            ("paragraph:On September 15, moda launched a public call for content", _p("On September 18, Chunghwa Telecom announced that the nearly 300-kilometre fourth Taiwan–Matsu cable had been built, landed and tested, taking the Taiwan–Matsu links from two cables to three and the overall capacity to about 1.9 Tbps; it put the investment at nearly NT$1.4 billion but gave no date for commercial service, and moda's press-release page carried no matching release on the day this site checked.")),
            ("paragraph:Apple announced on August 18 that it was adjusting its EU App business", _p("On September 16, Apple told developers in its news feed that the App Tracking Transparency prompt has another version in the EU: from iOS 27.2 and iPadOS 27.2, only the new version may be used in Germany, France, Italy, Poland and Romania, the device setting is renamed in the EU, and a developer may ask again a year after the user last answered; Apple named no regulator and no law. On September 17, the European Commission adopted its KIDS Act proposal, under which social media platforms may not let children under 13 hold an account and a minor may open one alone only at 15; it is a proposal sent to the European Parliament and the Council, and the official pages give no date of application.")),
        ],
        "ja": [
            ("paragraph:Googleは9月15日に9月のPixel Dropを公開しました。", _p("同じ9月16日、AppleはiOS 27に伴うサブスクリプションの変更も発表しました。複数のサブスクリプションをバンドルまたはスイートとして1回の購入にまとめられ、最大5つのデベロッパーが参加できます。マルチシート購入はApp Store Connectで既定で有効になり、ボリューム購入は10月22日の提供予定、グループ購入は今年の冬とだけ予告されています。公式ページには国や地域の記載がありません。")),
            ("paragraph:9月15日、デジタル発展部は「Taiwan Sovereign AI Training Corpus", _p("9月18日、中華電信は全長約300kmの台馬第四海底ケーブルの敷設、陸揚げ、疎通試験が完了したと発表しました。台湾と馬祖を結ぶ海底ケーブルは2本から3本になり、総伝送容量は約1.9Tbpsに高まります。投資額は約14億台湾ドルとしていますが、商用開始日は書かれておらず、当サイトが確認した日にはデジタル発展部のプレスリリース一覧に対応する発表はありませんでした。")),
            ("paragraph:Appleは8月18日、EU向けのApp事業条件を調整すると発表しました。", _p("9月16日、AppleはデベロッパーニュースでEU向けのApp Tracking Transparencyの確認ダイアログに別バージョンが加わると発表しました。iOS 27.2とiPadOS 27.2以降、ドイツ、フランス、イタリア、ポーランド、ルーマニアの5か国では新バージョンしか使えず、EUではデバイス設定の名称が変わり、デベロッパーは利用者が前回回答してから1年後に再度確認できます。Appleは規制当局も根拠法も名指ししていません。9月17日、欧州委員会はKIDS Act提案を採択し、SNSプラットフォームは13歳未満の子どもにアカウントを持たせてはならず、未成年者が自分でアカウントを開設できるのは15歳からとしました。欧州議会と理事会に送られた提案であり、公式ページに適用日は書かれていません。")),
        ],
        "ko": [
            ("paragraph:Google은 9월 15일 9월 Pixel Drop을 공개했습니다.", _p("같은 9월 16일, Apple은 iOS 27과 함께 오는 구독 변경도 발표했습니다. 여러 구독을 번들이나 스위트로 묶어 한 번의 구매로 팔 수 있고, 최대 5개 개발자가 참여할 수 있습니다. 멀티시트 구매는 App Store Connect에서 기본으로 켜지고, 볼륨 구매는 10월 22일 출시 예정이며, 그룹 구매는 올겨울이라고만 예고됐습니다. 공식 페이지에는 국가나 지역이 적혀 있지 않습니다.")),
            ("paragraph:9월 15일, 디지털발전부는 'Taiwan Sovereign AI Training Corpus", _p("9월 18일, 중화전신은 길이 약 300km의 타이완–마쭈 제4 해저케이블의 건설, 육양, 소통 시험이 끝났다고 발표했습니다. 타이완과 마쭈를 잇는 해저케이블은 2개에서 3개로 늘고, 전체 전송 용량은 약 1.9Tbps로 높아집니다. 투자액은 약 14억 대만달러라고 밝혔지만 상용 개시일은 적지 않았고, 본 사이트가 확인한 날 디지털발전부의 보도자료 목록에는 대응하는 발표가 없었습니다.")),
            ("paragraph:Apple은 8월 18일 EU 대상 App 사업 조건을 조정한다고 발표했습니다.", _p("9월 16일, Apple은 개발자 뉴스에서 EU 대상 App Tracking Transparency 요청 대화상자에 다른 버전이 추가된다고 발표했습니다. iOS 27.2와 iPadOS 27.2부터 독일, 프랑스, 이탈리아, 폴란드, 루마니아 5개국에서는 새 버전만 쓸 수 있고, EU에서는 기기 설정의 이름이 바뀌며, 개발자는 사용자가 마지막으로 답한 뒤 1년이 지나면 다시 물을 수 있습니다. Apple은 규제 기관도 근거 법률도 밝히지 않았습니다. 9월 17일, EU 집행위원회는 KIDS Act 제안을 채택해 SNS 플랫폼이 13세 미만 아동에게 계정을 갖게 해서는 안 되고, 미성년자가 스스로 계정을 열 수 있는 나이를 15세로 정했습니다. 유럽의회와 이사회에 보낸 제안이며, 공식 페이지에 적용일은 적혀 있지 않습니다.")),
        ],
        "zh-CN": [
            ("paragraph:Google 在 9 月 15 日发布 9 月 Pixel Drop", _p("9 月 16 日，Apple 另外公告 App Store 订阅随 iOS 27 而来的变动：多个订阅可合并成组合方案或套组，最多五个开发者参与；多名额购买在 App Store Connect 默认开启，批量采购预定 10 月 22 日推出，群组购买只预告今年冬天。官方页面没有写出任何国家或地区。")),
            ("paragraph:9 月 15 日，数位发展部启动“台湾主权 AI 训练语料库”", _p("9 月 18 日，中华电信宣布全长近 300 公里的台马第四海缆已完成建置、登陆与测通，台马联外海缆由两条增为三条，整体传输容量提升至约 1.9 Tbps；公告写投入近新台币 14 亿元，但没有写商转日或启用日，数位发展部的“新闻发布”页在本站查核当天也没有对应公告。")),
            ("paragraph:Apple 在 8 月 18 日宣布调整欧盟地区的 App 商业条款", _p("9 月 16 日，Apple 在开发者新闻公告欧盟的 App 跟踪透明度询问框另有版本：自 iOS 27.2 与 iPadOS 27.2 起，德国、法国、意大利、波兰与罗马尼亚五国只能使用新版，欧盟的设备设置改名，开发者可在用户上次回答满一年后再问一次；Apple 没有点名主管机关，也没有说依据哪一部法律。9 月 17 日，欧盟委员会通过 KIDS Act 提案，规定社交媒体平台不得让未满 13 岁的儿童持有账号、15 岁才能自己开账号；那是送交欧洲议会与理事会审议的提案，官方页面没有写生效日。")),
        ],
    },
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


def update(vertical) -> None:
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
        if list(pack["locales"]) != LOCALES:
            sys.exit(f"{slug} does not carry all five locales yet")
    already: list[str] = []

    for locale in LOCALES:
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

    path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{name}: index updated,", {locale: len(index["locales"][locale]["blocks"]) for locale in LOCALES})
    if already:
        print(f"{name}: already cited, not added again:", sorted(set(already)))
    if RETITLE[name]:
        print(f"{name}: link text refreshed in {retitle(vertical.index, RETITLE[name])} packs")


def main() -> None:
    named = [a for a in sys.argv[1:] if not a.startswith("--")]
    unknown = [n for n in named if n not in BY_NAME]
    if unknown:
        sys.exit(f"unknown vertical {unknown}; one of " + ", ".join(BY_NAME))
    chosen = [BY_NAME[n] for n in named] if named else list(VERTICALS)
    # Only the verticals this run touches: an AI sentence nobody has written yet is no reason
    # to refuse a crypto run that has nothing to do with it.
    pending = [line for vertical in chosen for line in unwritten(vertical.name)]
    if pending:
        sys.exit("edits still to write:\n - " + "\n - ".join(pending))
    for vertical in chosen:
        if not has_work(vertical.name):
            print("nothing to add:", vertical.name)
            continue
        update(vertical)


if __name__ == "__main__":
    main()
