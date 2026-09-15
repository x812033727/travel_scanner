"""Add this batch's seven articles to the January–September index, in place, in five languages.

Run once, after the seven packs carry all five locales:
``python docs/ai-news-2026-09-mid/update_index.py``. Every sentence edit is an exact
replacement that must match once, so a second run fails instead of editing twice.

It also repairs the Japanese month headings above the link lists: batch #497 published them
with the callout text and eight article titles in place of "2026年N月のニュース解説".
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTENT = ROOT / "apps/api/app/guides/content"
INDEX = CONTENT / "ai-news-2026-january-september-index.json"
CHECKED = "2026-09-15"
LOCALES = ["zh-TW", "en", "ja", "ko", "zh-CN"]

# (slug, place the link after this existing slug; a leading "<" means before it)
NEW = [
    ("ai-news-gpt-live-voice-20260708", "<ai-news-chatgpt-work-20260709"),
    ("ai-news-google-assistant-gemini-20260904", "ai-news-lyria-35-gemini-20260904"),
    ("ai-news-anthropic-threat-report-20260910", "ai-news-chatgpt-images-25-20260908"),
    ("ai-news-openai-agents-api-20260910", "ai-news-anthropic-threat-report-20260910"),
    ("ai-news-deepseek-v41-flash-20260910", "ai-news-openai-agents-api-20260910"),
    ("ai-news-pace-the-frontier-20260912", "ai-news-deepseek-v41-flash-20260910"),
    ("ai-news-siri-ai-ios-27-20260914", "ai-news-pace-the-frontier-20260912"),
]
# The index cites one source from each of these two articles.
CITED = ["ai-news-anthropic-threat-report-20260910", "ai-news-siri-ai-ios-27-20260914"]

EDITS: dict[str, list[tuple[str, str]]] = {
    "zh-TW": [
        ("description", "依月份整理 31 則", "依月份整理 38 則"),
        (0, "這份索引於 2026-09-14 查核，收錄三十一則重要事件", "這份索引於 2026-09-14 查核、2026-09-15 增補，收錄三十八則重要事件"),
        (1, "形成可連續閱讀的時間線。", "形成可連續閱讀的時間線。2026-09-15 再補上七則：七月的 GPT-Live 語音，以及九月的 Google 助理改由 Gemini 接手、Anthropic 濫用威脅報告、OpenAI Agents API、DeepSeek V4.1-Flash、Amodei 呼籲放慢前沿 AI 與 Siri AI。"),
        (16, "七月接著有 ChatGPT Work、Gemini 3.6 Flash", "七月接著有 ChatGPT Work、GPT-Live 語音、Gemini 3.6 Flash"),
        (20, "Lyria 3.5 和 ChatGPT Images 2.5。", "Lyria 3.5 和 ChatGPT Images 2.5，之後又有 Google 助理改由 Gemini 接手、Anthropic 威脅報告、OpenAI Agents API、DeepSeek V4.1-Flash、〈We Must Pace the Frontier〉一文與 Siri AI。"),
        (23, "三十一則新聞", "三十八則新聞"),
        (24, "本次整理是截至 2026-09-14 的一次性編輯專輯", "本次整理是截至 2026-09-14 的一次性編輯專輯（2026-09-15 增補七則）"),
    ],
    "en": [
        ("description", "Organizing 31 key AI news stories", "Organizing 38 key AI news stories"),
        (0, "Verified as of 2026-09-14, this index brings together full analyses of thirty-one key events", "Verified as of 2026-09-14 and expanded on 2026-09-15, this index brings together full analyses of thirty-eight key events"),
        (1, "spanning January to July.", "spanning January to July. On 2026-09-15 seven more were added: GPT-Live voice from July, and from September Gemini replacing Google Assistant, Anthropic's misuse threat report, the OpenAI Agents API, DeepSeek V4.1-Flash, Amodei's call to pace frontier AI, and Siri AI."),
        (16, "July brought ChatGPT Work, Gemini 3.6 Flash", "July brought ChatGPT Work, GPT-Live voice, Gemini 3.6 Flash"),
        (20, "Lyria 3.5, and ChatGPT Images 2.5.", "Lyria 3.5, and ChatGPT Images 2.5, followed by Gemini replacing Google Assistant, Anthropic's threat report, the OpenAI Agents API, DeepSeek V4.1-Flash, the essay \"We Must Pace the Frontier\", and Siri AI."),
        (23, "Below, thirty-one news reports", "Below, thirty-eight news reports"),
        (24, "a one-off editorial feature current through 2026-09-14", "a one-off editorial feature current through 2026-09-14 (seven articles added on 2026-09-15)"),
    ],
    "ja": [
        ("description", "重要AIニュース31件", "重要AIニュース38件"),
        (0, "このインデックスは2026-09-14に検証されたもので、31件の重要ニュース", "このインデックスは2026-09-14に検証され、2026-09-15に追補したもので、38件の重要ニュース"),
        (1, "タイムラインを構成しています。", "タイムラインを構成しています。2026-09-15には、7月のGPT-Live音声と、9月のGoogleアシスタントからGeminiへの移行、Anthropicの悪用に関する脅威レポート、OpenAI Agents API、DeepSeek V4.1-Flash、フロンティアAIの歩調を緩めるよう求めたAmodei氏の論考、Siri AIの7本を追加しました。"),
        (16, "7月にはChatGPT Work、Gemini 3.6 Flash", "7月にはChatGPT Work、GPT-Live音声、Gemini 3.6 Flash"),
        (20, "Lyria 3.5、ChatGPT Images 2.5が続いています。", "Lyria 3.5、ChatGPT Images 2.5が続き、その後にGoogleアシスタントからGeminiへの移行、Anthropicの脅威レポート、OpenAI Agents API、DeepSeek V4.1-Flash、論考「We Must Pace the Frontier」、Siri AIがあります。"),
        (23, "下記に31件のニュース", "下記に38件のニュース"),
        (24, "2026-09-14時点での一回限りの編集特集であり", "2026-09-14時点での一回限りの編集特集（2026-09-15に7本を追補）であり"),
    ],
    "ko": [
        ("description", "주요 AI 뉴스 31건", "주요 AI 뉴스 38건"),
        (0, "2026-09-14에 검증된 이 색인은 31건의 주요 사건", "2026-09-14에 검증되고 2026-09-15에 보완된 이 색인은 38건의 주요 사건"),
        (1, "타임라인을 형성합니다.", "타임라인을 형성합니다. 2026-09-15에는 7월의 GPT-Live 음성과 9월의 Google 어시스턴트의 Gemini 전환, Anthropic 오남용 위협 보고서, OpenAI Agents API, DeepSeek V4.1-Flash, 프런티어 AI의 속도 조절을 촉구한 Amodei의 글, Siri AI 등 7편을 추가했습니다."),
        (16, "7월에는 ChatGPT Work, Gemini 3.6 Flash", "7월에는 ChatGPT Work, GPT-Live 음성, Gemini 3.6 Flash"),
        (20, "Lyria 3.5, ChatGPT Images 2.5로 이어집니다.", "Lyria 3.5, ChatGPT Images 2.5로 이어지고, 이후 Google 어시스턴트의 Gemini 전환, Anthropic 위협 보고서, OpenAI Agents API, DeepSeek V4.1-Flash, 「We Must Pace the Frontier」 글, Siri AI가 뒤따릅니다."),
        (23, "아래에 31건의 뉴스", "아래에 38건의 뉴스"),
        (24, "2026-09-14 기준의 일회성 편집 특집으로", "2026-09-14 기준의 일회성 편집 특집(2026-09-15에 7편 보완)으로"),
    ],
    "zh-CN": [
        ("description", "按月份整理 31 条", "按月份整理 38 条"),
        (0, "这份索引于 2026-09-14 查核，收录三十一条重要事件", "这份索引于 2026-09-14 查核、2026-09-15 增补，收录三十八条重要事件"),
        (1, "形成可连续阅读的时间线。", "形成可连续阅读的时间线。2026-09-15 再补上七条：七月的 GPT-Live 语音，以及九月的 Google 助理改由 Gemini 接手、Anthropic 滥用威胁报告、OpenAI Agents API、DeepSeek V4.1-Flash、Amodei 呼吁放慢前沿 AI 与 Siri AI。"),
        (16, "七月接着有 ChatGPT Work、Gemini 3.6 Flash", "七月接着有 ChatGPT Work、GPT-Live 语音、Gemini 3.6 Flash"),
        (20, "Lyria 3.5 和 ChatGPT Images 2.5。", "Lyria 3.5 和 ChatGPT Images 2.5，之后又有 Google 助理改由 Gemini 接手、Anthropic 威胁报告、OpenAI Agents API、DeepSeek V4.1-Flash、《We Must Pace the Frontier》一文与 Siri AI。"),
        (23, "三十一条新闻", "三十八条新闻"),
        (24, "本次整理是截至 2026-09-14 的一次性编辑专辑", "本次整理是截至 2026-09-14 的一次性编辑专辑（2026-09-15 增补七篇）"),
    ],
}
TABLE = {
    # locale: (July focus, September label, September focus, caption old, caption new)
    "zh-TW": ("交付、效率、費用與語音", "9 月 1–14 日", "模型、代理、資安與個人助理", "共 31 篇", "共 38 篇"),
    "en": ("Delivery, efficiency, pricing, voice", "Sept 1–14", "Models, agents, security, assistants", "31 articles in total", "38 articles in total"),
    "ja": ("成果物納品、効率、コスト、音声", "9月1〜14日", "モデル、エージェント、セキュリティ、アシスタント", "全31本", "全38本"),
    "ko": ("결과물 인도, 효율, 비용, 음성", "9월 1~14일", "모델, 에이전트, 보안, 어시스턴트", "총 31편", "총 38편"),
    "zh-CN": ("交付、效率、费用与语音", "9 月 1–14 日", "模型、代理、网络安全与个人助理", "共 31 篇", "共 38 篇"),
}
JA_MONTH = "2026年{}月のニュース解説"


def replace_once(text: str, old: str, new: str, where: str) -> str:
    count = text.count(old)
    if count != 1:
        sys.exit(f"{where}: expected one '{old[:40]}', found {count}")
    return text.replace(old, new)


def main() -> None:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    packs = {slug: json.loads((CONTENT / f"{slug}.json").read_text(encoding="utf-8")) for slug, _ in NEW}
    for slug, pack in packs.items():
        if list(pack["locales"]) != LOCALES:
            sys.exit(f"{slug} does not carry all five locales yet")

    for locale in LOCALES:
        doc = index["locales"][locale]
        blocks = doc["blocks"]
        for target, old, new in EDITS[locale]:
            if target == "description":
                doc["description"] = replace_once(doc["description"], old, new, f"{locale} description")
            else:
                block = blocks[target]
                assert block["type"] == "paragraph", (locale, target, block["type"])
                block["text"] = replace_once(block["text"], old, new, f"{locale} block {target}")

        table = blocks[9]
        assert table["type"] == "table" and len(table["rows"]) == 9, (locale, "table")
        july, september = table["rows"][6], table["rows"][8]
        assert july[1] == "4" and september[1] == "5" and september[0] == TABLE[locale][1], (locale, july, september)
        july[1], july[2] = "5", TABLE[locale][0]
        september[1], september[2] = "11", TABLE[locale][2]
        table["caption"] = replace_once(table["caption"], TABLE[locale][3], TABLE[locale][4], f"{locale} caption")

        month_headings = [i for i, b in enumerate(blocks) if i > 25 and b["type"] == "heading"]
        assert len(month_headings) == 9, (locale, month_headings)
        if locale == "ja":
            for month, i in enumerate(month_headings, start=1):
                blocks[i]["text"] = JA_MONTH.format(month)

        for slug, after in NEW:
            url = f"https://mokaair.com/{locale}/life/{slug}"
            if any(b["type"] == "link" and b["url"] == url for b in blocks):
                sys.exit(f"{locale}: {slug} is already linked")
            anchor = f"https://mokaair.com/{locale}/life/{after.lstrip('<')}"
            position = next(i for i, b in enumerate(blocks) if b["type"] == "link" and b["url"] == anchor)
            title = packs[slug]["locales"][locale]["title"]
            offset = 0 if after.startswith("<") else 1
            blocks.insert(position + offset, {"type": "link", "text": title, "url": url})

        for slug in CITED:
            source = dict(packs[slug]["locales"][locale]["sources"][0])
            assert source["checked_on"] == CHECKED
            doc["sources"].append(source)

    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("index updated:", {locale: len(index["locales"][locale]["blocks"]) for locale in LOCALES})


if __name__ == "__main__":
    main()
