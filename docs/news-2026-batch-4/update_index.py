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

# vertical -> (slug, the existing slug to place the link after; a leading "<" means before it)
NEW: dict[str, list[tuple[str, str]]] = {
    "crypto": [],
    "tech": [],
    # Batch 4.3's twelve, each placed by event date among the month's existing links. An entry
    # may name a slug inserted just before it: the list is applied in order.
    "ai": [
        ("ai-news-openai-astral-20260319", "ai-news-claude-interactive-visuals-20260312"),
        ("ai-news-openai-funding-20260331", "ai-news-lyria-3-pro-20260325"),
        ("ai-news-gpt-55-instant-20260505", "<ai-news-gemini-omni-20260519"),
        ("ai-news-chatgpt-ads-20260505", "ai-news-gpt-55-instant-20260505"),
        ("ai-news-frontier-governance-20260528", "ai-news-gemini-spark-20260519"),
        ("ai-news-openai-s1-20260608", "<ai-news-claude-fable-5-access-20260609"),
        ("ai-news-openai-broadcom-chip-20260624", "ai-news-claude-fable-5-access-20260609"),
        ("ai-news-nvidia-hugging-face-20260903", "ai-news-gpt-6-astra-20260903"),
        ("ai-news-chatgpt-financial-services-20260910", "ai-news-deepseek-v41-flash-20260910"),
        ("ai-news-gpt-live-1-api-20260910", "ai-news-chatgpt-financial-services-20260910"),
        ("ai-news-chatgpt-storage-scale-20260911", "ai-news-gpt-live-1-api-20260910"),
        ("ai-news-gemini-38-live-20260915", "ai-news-siri-ai-ios-27-20260914"),
    ],
}
# vertical -> the articles whose first source the index cites. A source the index already
# carries is skipped, not appended twice: the index's nine include this batch's own subjects.
CITED: dict[str, list[str]] = {
    "crypto": [],
    "tech": [],
    "ai": [
        "ai-news-openai-funding-20260331",
        "ai-news-gpt-55-instant-20260505",
        "ai-news-nvidia-hugging-face-20260903",
        "ai-news-gemini-38-live-20260915",
    ],
}

# vertical -> locale -> new title. Empty leaves the title alone. The AI index loses the days
# from its range (ai.md: "1 月 1 日至 9 月 14 日" is wrong the moment 9/15 is added, and a range
# without days is still right next time); it loses its article count to the rule below.
RETITLE: dict[str, dict[str, str]] = {
    "crypto": {},
    "tech": {},
    "ai": {
        "zh-TW": "2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用",
        "en": "2026 AI News Roundup: Highlights and Daily Life Applications from January to September",
        "ja": "2026年AIニュース総まとめ：1月から9月までの重要動向と実生活への応用",
        "ko": "2026년 AI 뉴스 총정리: 1월부터 9월까지의 핵심과 일상 적용",
        "zh-CN": "2026 年 AI 新闻总整理：1 月至 9 月的重点与生活应用",
    },
}

# vertical -> locale -> (where, old, new). ``where`` is "description" or a block index.
#
# The AI index's descriptions lose the days and the count for the same two reasons as the
# titles, and those two are decided. Every other entry below is a sentence that carries a
# reader-visible article count and needs the new checked date written into it as well -- one
# ``TODO`` each, quoted exactly as the index reads today, so the pre-flight can name the work
# instead of the run dying inside ``update()`` on the count rule. Blocks 3 of zh-TW and zh-CN
# count January's own items (「一月的三則消息」); the same sentence in en, ja and ko counts
# "updates", not articles, so COUNT leaves it alone -- keep the five in step by hand.
EDITS: dict[str, dict[str, list[tuple[object, str, str]]]] = {
    "crypto": {locale: [] for locale in LOCALES},
    "tech": {locale: [] for locale in LOCALES},
    "ai": {
        "zh-TW": [
            ("description", "從 2026 年 1 月 1 日至 9 月 14 日，依月份整理 38 則 AI 重要新聞", "從 2026 年 1 月至 9 月，依月份整理 AI 重要新聞"),
            (0, "2026-01-01 至 2026-09-14，", "2026 年一月至九月，"),
            (0, "這份索引於 2026-09-14 查核、2026-09-15 增補，收錄三十八則重要事件的完整解析", "這份索引於 2026-09-14 查核，2026-09-15 與 2026-09-18 兩度增補，收錄重要事件的完整解析"),
            (1, "原先七月底至九月的十篇新聞也納入索引，與這次補齊的一月至七月二十一篇形成", "原先七月底至九月的新聞也納入索引，與之後補齊的一月至七月各篇形成"),
            (1, "2026-09-15 再補上七則：", "2026-09-15 再補上："),
            (1, "Amodei 呼籲放慢前沿 AI 與 Siri AI。", "Amodei 呼籲放慢前沿 AI 與 Siri AI。2026-09-18 又補上先前沒寫到的事件：三月的 OpenAI 收購 Astral 與 1,220 億美元募資，五月的 GPT-5.5 Instant 成為預設模型、ChatGPT 廣告開放自助購買與 OpenAI 的前沿治理框架，六月的保密遞交 S-1 草稿與 Jalapeño 晶片，以及九月的 NVIDIA 收購 Hugging Face、ChatGPT for Financial Services、GPT-Live 1 開放 API、Habitat 儲存架構與 Gemini 3.8 Live。"),
            (3, "一月的三則消息", "一月的消息"),
            (20, "原先已刊登的十篇均保留", "原先已刊登的各篇均保留"),
            (23, "下方按月份排列三十八則新聞", "下方按月份排列各則新聞"),
            (24, "本次整理是截至 2026-09-14 的一次性編輯專輯（2026-09-15 增補七則），", "本專輯最初整理到 2026-09-14，之後在 2026-09-15 與 2026-09-18 增補，"),
            (25, "本輯截止 2026-09-14。", "本輯收錄的事件到 2026-09-15 為止，最後增補於 2026-09-18。"),
        ],
        "en": [
            ("description", "Organizing 38 key AI news stories month by month from January 1 to September 14, 2026", "Organizing key AI news stories month by month from January to September 2026"),
            (0, "From 2026-01-01 to 2026-09-14, AI news", "From January to September 2026, AI news"),
            (0, "Verified as of 2026-09-14 and expanded on 2026-09-15, this index brings together full analyses of thirty-eight key events", "Verified as of 2026-09-14 and expanded on 2026-09-15 and 2026-09-18, this index brings together full analyses of key events"),
            (1, "The ten news reports originally published from late July through September are also integrated into this index, forming a continuous reading timeline alongside the twenty-one newly added pieces spanning January to July.", "The news reports originally published from late July through September are also integrated into this index, forming a continuous reading timeline alongside the pieces later added for January to July."),
            (1, "On 2026-09-15 seven more were added:", "On 2026-09-15 more were added:"),
            (1, "Amodei's call to pace frontier AI, and Siri AI.", "Amodei's call to pace frontier AI, and Siri AI. On 2026-09-18 events not yet covered were added: from March, OpenAI's agreement to acquire Astral and its $122 billion funding round; from May, GPT-5.5 Instant becoming the default model, self-serve buying for ChatGPT ads and OpenAI's frontier governance framework; from June, the confidential S-1 draft and the Jalapeño chip; and from September, NVIDIA's agreement to acquire Hugging Face, ChatGPT for Financial Services, GPT-Live 1 in the API, the Habitat storage platform and Gemini 3.8 Live."),
            (3, "The three updates from January can be divided", "January's updates can be divided"),
            (20, "The ten articles previously published are fully retained", "The articles previously published are fully retained"),
            (23, "Below, thirty-eight news reports are arranged", "Below, the news reports are arranged"),
            (24, "This compilation is a one-off editorial feature current through 2026-09-14 (seven articles added on 2026-09-15),", "This editorial feature was first compiled through 2026-09-14 and expanded on 2026-09-15 and 2026-09-18,"),
            (25, "This series is current as of 2026-09-14.", "This series covers events through 2026-09-15 and was last expanded on 2026-09-18."),
        ],
        "ja": [
            ("description", "2026年1月1日から9月14日までの重要AIニュース38件を月別に整理し", "2026年1月から9月までの重要AIニュースを月別に整理し"),
            (0, "2026-01-01から2026-09-14にかけて、", "2026年1月から9月にかけて、"),
            (0, "このインデックスは2026-09-14に検証され、2026-09-15に追補したもので、38件の重要ニュースの完全な解説を", "このインデックスは2026-09-14に検証され、2026-09-15と2026-09-18に追補したもので、重要ニュースの完全な解説を"),
            (1, "先行して掲載されていた7月下旬から9月の10本の記事も収録され、今回追加された1月から7月の21本と合わせ", "先行して掲載されていた7月下旬から9月の記事も収録され、その後追加された1月から7月の記事と合わせ"),
            (1, "Siri AIの7本を追加しました。", "Siri AIを追加しました。2026-09-18には、未収録だった出来事を追加しました。3月のOpenAIによるAstral買収合意と1,220億ドルの資金調達、5月のGPT-5.5 Instantの既定モデル化、ChatGPT広告のセルフサービス購入開始、OpenAIのフロンティア・ガバナンス枠組み、6月のS-1ドラフトの非公開提出とJalapeñoチップ、9月のNVIDIAによるHugging Face買収合意、ChatGPT for Financial Services、GPT-Live 1のAPI提供、ストレージ基盤Habitat、Gemini 3.8 Liveです。"),
            (3, "1月の3つのニュースは", "1月のニュースは"),
            (20, "以前掲載された10本もすべて維持され", "以前掲載された記事もすべて維持され"),
            (23, "下記に38件のニュース", "下記に各ニュース"),
            (24, "今回のまとめは2026-09-14時点での一回限りの編集特集（2026-09-15に7本を追補）であり、", "本特集は2026-09-14時点でまとめ、2026-09-15と2026-09-18に追補した編集特集であり、"),
            (25, "本特集の対象は2026-09-14までです。", "本特集の対象は2026-09-15までの出来事で、最終追補は2026-09-18です。"),
        ],
        "ko": [
            ("description", "2026년 1월 1일부터 9월 14일까지의 주요 AI 뉴스 38건을 월별로 정리하여", "2026년 1월부터 9월까지의 주요 AI 뉴스를 월별로 정리하여"),
            (0, "2026-01-01부터 2026-09-14까지, ", "2026년 1월부터 9월까지, "),
            (0, "2026-09-14에 검증되고 2026-09-15에 보완된 이 색인은 38건의 주요 사건에 대한 전체 분석을", "2026-09-14에 검증되고 2026-09-15와 2026-09-18에 보완된 이 색인은 주요 사건에 대한 전체 분석을"),
            (1, "기존 7월 말부터 9월까지의 뉴스 10편도 색인에 포함되어, 이번에 보완된 1월부터 7월까지의 21편과 함께", "기존 7월 말부터 9월까지의 뉴스도 색인에 포함되어, 이후 보완된 1월부터 7월까지의 기사와 함께"),
            (1, "Siri AI 등 7편을 추가했습니다.", "Siri AI를 추가했습니다. 2026-09-18에는 아직 다루지 않았던 사건을 추가했습니다. 3월의 OpenAI의 Astral 인수 합의와 1,220억 달러 자금 조달, 5월의 GPT-5.5 Instant 기본 모델 전환, ChatGPT 광고 셀프서비스 구매 개시, OpenAI의 프런티어 거버넌스 프레임워크, 6월의 S-1 초안 비공개 제출과 Jalapeño 칩, 9월의 NVIDIA의 Hugging Face 인수 합의, ChatGPT for Financial Services, GPT-Live 1의 API 제공, 스토리지 기반 Habitat, Gemini 3.8 Live입니다."),
            (3, "1월의 3가지 소식은", "1월의 소식은"),
            (20, "기존에 게재된 10편은 그대로 유지되며", "기존에 게재된 기사는 그대로 유지되며"),
            (23, "아래에 38건의 뉴스", "아래에 각 뉴스"),
            (24, "이번 정리는 2026-09-14 기준의 일회성 편집 특집(2026-09-15에 7편 보완)으로,", "이번 특집은 2026-09-14 기준으로 정리한 뒤 2026-09-15와 2026-09-18에 보완한 편집 특집으로,"),
            (25, "본 특집은 2026-09-14 기준입니다.", "본 특집은 2026-09-15까지의 사건을 다루며, 마지막 보완은 2026-09-18입니다."),
        ],
        "zh-CN": [
            ("description", "从 2026 年 1 月 1 日至 9 月 14 日，按月份整理 38 条 AI 重要新闻", "从 2026 年 1 月至 9 月，按月份整理 AI 重要新闻"),
            (0, "2026-01-01 至 2026-09-14，", "2026 年一月至九月，"),
            (0, "这份索引于 2026-09-14 查核、2026-09-15 增补，收录三十八条重要事件的完整解析", "这份索引于 2026-09-14 查核，2026-09-15 与 2026-09-18 两度增补，收录重要事件的完整解析"),
            (1, "原先七月底至九月的十篇新闻也纳入索引，与这次补齐的一月至七月二十一篇形成", "原先七月底至九月的新闻也纳入索引，与之后补齐的一月至七月各篇形成"),
            (1, "2026-09-15 再补上七条：", "2026-09-15 再补上："),
            (1, "Amodei 呼吁放慢前沿 AI 与 Siri AI。", "Amodei 呼吁放慢前沿 AI 与 Siri AI。2026-09-18 又补上先前没写到的事件：三月的 OpenAI 收购 Astral 与 1,220 亿美元融资，五月的 GPT-5.5 Instant 成为默认模型、ChatGPT 广告开放自助购买与 OpenAI 的前沿治理框架，六月的保密递交 S-1 草案与 Jalapeño 芯片，以及九月的 NVIDIA 收购 Hugging Face、ChatGPT for Financial Services、GPT-Live 1 开放 API、Habitat 存储架构与 Gemini 3.8 Live。"),
            (3, "一月的三则消息", "一月的消息"),
            (20, "原先已刊登的十篇均保留", "原先已刊登的各篇均保留"),
            (23, "下方按月份排列三十八条新闻", "下方按月份排列各条新闻"),
            (24, "本次整理是截至 2026-09-14 的一次性编辑专辑（2026-09-15 增补七篇），", "本专辑最初整理到 2026-09-14，之后在 2026-09-15 与 2026-09-18 增补，"),
            (25, "本辑截止 2026-09-14。", "本辑收录的事件到 2026-09-15 为止，最后增补于 2026-09-18。"),
        ],
    },
}

# vertical -> locale -> (row label in column 0, column index, current cell, new cell). The row
# is found by its first cell, not by its position, so an index that grows a month still works.
TABLE: dict[str, dict[str, list[tuple[str, int, str, str]]]] = {
    "crypto": {locale: [] for locale in LOCALES},
    "tech": {locale: [] for locale in LOCALES},
    # The reading-focus cells of the months that gained articles, and September's row label,
    # which named a day range that is wrong the moment 9/15 is in. Column indexes are those of
    # the table as it reads today; the count column (1) goes afterwards. The September label
    # is edited last, because the row is found by that label.
    "ai": {
        "zh-TW": [
            ("3 月", 2, "工作、圖解、音樂", "工作、圖解、音樂、開發工具與募資"),
            ("5 月", 2, "影片與背景工作", "影片、背景工作、預設模型、廣告與治理"),
            ("6 月", 2, "預覽與存取狀態", "預覽與存取狀態、保密遞件、自研晶片"),
            ("9 月 1–14 日", 2, "模型、代理、資安與個人助理", "模型、代理、資安、助理、語音與基礎設施"),
            ("9 月 1–14 日", 0, "9 月 1–14 日", "9 月"),
        ],
        "en": [
            ("March", 2, "Work, diagrams, music", "Work, diagrams, music, developer tools, funding"),
            ("May", 2, "Video and background tasks", "Video, background tasks, default model, ads, governance"),
            ("June", 2, "Previews and access status", "Previews, access status, confidential filing, custom chip"),
            ("Sept 1–14", 2, "Models, agents, security, assistants", "Models, agents, security, assistants, voice, infrastructure"),
            ("Sept 1–14", 0, "Sept 1–14", "September"),
        ],
        "ja": [
            ("3月", 2, "業務、図解、音楽", "業務、図解、音楽、開発ツール、資金調達"),
            ("5月", 2, "動画とバックグラウンドタスク", "動画、バックグラウンドタスク、既定モデル、広告、ガバナンス"),
            ("6月", 2, "プレビューと利用可能状況", "プレビュー、利用可能状況、非公開提出、自社チップ"),
            ("9月1〜14日", 2, "モデル、エージェント、セキュリティ、アシスタント", "モデル、エージェント、セキュリティ、アシスタント、音声、基盤"),
            ("9月1〜14日", 0, "9月1〜14日", "9月"),
        ],
        "ko": [
            ("3월", 2, "업무, 도해, 음악", "업무, 도해, 음악, 개발 도구, 자금 조달"),
            ("5월", 2, "동영상 및 백그라운드 작업", "동영상, 백그라운드 작업, 기본 모델, 광고, 거버넌스"),
            ("6월", 2, "프리뷰 및 접근 상태", "프리뷰, 접근 상태, 비공개 제출, 자체 칩"),
            ("9월 1~14일", 2, "모델, 에이전트, 보안, 어시스턴트", "모델, 에이전트, 보안, 어시스턴트, 음성, 인프라"),
            ("9월 1~14일", 0, "9월 1~14일", "9월"),
        ],
        "zh-CN": [
            ("3 月", 2, "工作、图解、音乐", "工作、图解、音乐、开发工具与融资"),
            ("5 月", 2, "视频与后台工作", "视频、后台工作、默认模型、广告与治理"),
            ("6 月", 2, "预览与访问状态", "预览与访问状态、保密递件、自研芯片"),
            ("9 月 1–14 日", 2, "模型、代理、网络安全与个人助理", "模型、代理、网络安全、助理、语音与基础设施"),
            ("9 月 1–14 日", 0, "9 月 1–14 日", "9 月"),
        ],
    },
}
# vertical -> locale -> the header cell of a table column to remove, after ``TABLE`` has run (so
# ``TABLE`` addresses columns as the index reads today). The AI index's month table carried a
# per-month number of articles: a number that grows with every batch, which is exactly what an
# index may not show (``ai.md``, "篇數"). Correcting 3 to 5 would be wrong again next batch, so
# the column goes and the table keeps the month and its reading focus.
DROP_COLUMN: dict[str, dict[str, str]] = {
    "crypto": {},
    "tech": {},
    "ai": {
        "zh-TW": "本輯新聞篇數",
        "en": "Articles in Series",
        "ja": "本特集の記事数",
        "ko": "본 특집 뉴스 편수",
        "zh-CN": "本辑新闻篇数",
    },
}
# vertical -> locale -> (old caption fragment, new caption fragment). The AI index's caption
# states the total; what it says instead is the same editorial decision as the paragraphs.
CAPTION: dict[str, dict[str, tuple[str, str]]] = {
    "crypto": {},
    "tech": {},
    "ai": {
        "zh-TW": ("篇數僅計新聞解析，不含這篇索引；共 38 篇，全部提供五種語言。", "各月的新聞解析都提供五種語言；完整清單見文末各月份的連結。"),
        "en": ("Count includes only news analyses, excluding this index; 38 articles in total, all offered in five languages.", "Every monthly analysis is offered in five languages; the full list follows below by month."),
        "ja": ("記事数はニュース解説のみで本インデックスを含みません。全38本、すべて5言語で提供。", "各月のニュース解説はすべて5言語で提供しています。全リストは記事末尾の月別リンクをご覧ください。"),
        "ko": ("편수는 뉴스 심층 분석 기사만 집계한 것이며 본 색인은 포함하지 않습니다. 총 38편으로 모두 5개 언어로 제공됩니다.", "각 월의 뉴스 분석은 모두 5개 언어로 제공됩니다. 전체 목록은 글 말미의 월별 링크에서 확인하세요."),
        "zh-CN": ("篇数仅计新闻解析，不含这篇索引；共 38 篇，全部提供五种语言。", "各月的新闻解析都提供五种语言；完整清单见文末各月份的链接。"),
    },
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
    # series runs to, which is wrong the day a later event is added.
    if block["type"] in ("paragraph", "callout"):
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

        for slug, after in NEW[name]:
            if any(block_kind(b) == "link" and link_of(b, locale)[0] == slug for b in blocks):
                sys.exit(f"{locale}: {slug} is already linked")
            position = find_link(blocks, after.lstrip("<"), locale)
            offset = 0 if after.startswith("<") else 1
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
        if left:
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
