"""Topic vocabulary for intel, guide and lifestyle articles.

The first nine slugs are the ones ``app.discovery.taxonomy`` already uses for hotspots and
dishes. Reusing those ids is what lets a guide and an attraction that share a subject find
each other later instead of living in two vocabularies that only look alike.

Each topic belongs to one section. A travel topic on a lifestyle article, or the reverse,
is refused at write time (``admin_service._resolve_topics``), so the two vocabularies never
bleed into each other's filters.

Topics are two levels deep. A lifestyle parent such as ``ai`` holds sub-topics such as
``ai-terms`` (``GuideTopic.parent_id``); an article may carry the parent, the child or both.
Filtering by the parent includes its children, and the listing counts each article once
under the parent however many of its children it carries.

The travel vocabulary is one level everywhere except under ``food``. Its second axis is
still the destination, grouped by country in ``service``; but a food special is written one
dish and one city at a time (豬肉湯飯 in Busan, 豬肉湯飯 in Seoul), and the destination axis
cannot gather the same dish across cities. ``TRAVEL_SEED_SUBTOPICS`` is that gathering: one
sub-topic per dish, plus ``cafe``. A special carries its sub-topic alone, not ``food`` as
well. ``?topic=food`` lists it either way, and the article's breadcrumb is built from its
first topic in display order, which would be ``food`` and would leave the dish out.
"""

from __future__ import annotations

from typing import cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleTopic, GuideTopic
from app.guides.publication import published_filters
from app.guides.schemas import Section, TopicList, TopicOption
from app.i18n import DEFAULT_LOCALE, LOCALES, Locale

Labels = tuple[str, str, str, str, str]

# slug -> (en, ja, ko, zh-TW, zh-CN), in the order of app.i18n.LOCALES.
SEED_TOPICS: tuple[tuple[str, Labels], ...] = (
    ("transport", ("Transport", "交通", "교통", "交通", "交通")),
    ("entry", ("Entry rules", "入国手続き", "입국 규정", "簽證入境", "签证入境")),
    ("packing", ("Before you go", "出発前の準備", "출발 전 준비", "行前準備", "行前准备")),
    ("itinerary", ("Itineraries", "モデルコース", "추천 일정", "行程範例", "行程范例")),
    ("budget", ("Budget", "予算", "예산", "預算", "预算")),
    ("deal", ("Deals", "お得情報", "할인 정보", "優惠情報", "优惠情报")),
    ("season", ("Seasonal", "季節の催し", "계절 행사", "季節活動", "季节活动")),
    ("connectivity", ("Staying online", "通信・ネット", "통신・인터넷", "網路通訊", "网络通讯")),
    ("etiquette", ("Etiquette", "マナー", "에티켓", "禮儀文化", "礼仪文化")),
    ("safety", ("Safety", "安全・緊急時", "안전・비상", "安全應變", "安全应变")),
    ("food", ("Food", "グルメ", "음식", "美食", "美食")),
    ("shopping", ("Shopping", "ショッピング", "쇼핑", "購物", "购物")),
    ("hotel", ("Hotels", "ホテル", "호텔", "飯店", "酒店")),
    ("culture", ("Culture", "文化", "문화", "文化", "文化")),
    ("nature", ("Nature", "自然", "자연", "自然", "自然")),
    ("family", ("Family", "家族向け", "가족 여행", "親子", "亲子")),
    ("nightlife", ("Nightlife", "ナイトライフ", "야간 활동", "夜生活", "夜生活")),
    ("viewpoint", ("Viewpoints", "展望スポット", "전망 명소", "觀景", "观景")),
    ("beach", ("Beaches", "ビーチ", "해변", "海灘", "海滩")),
)

# slug, parent slug, (en, ja, ko, zh-TW, zh-CN). Seeded by 0082 in this order and, like the
# lifestyle tuples, appended to and never reordered.
#
# A dish sub-topic is spelled the way ``app.foods.catalog`` spells a dish: ``kr-`` and the
# Revised Romanization with a hyphen between words. A dish the catalog seeds and its hub then
# share one slug (``kr-naengmyeon``), and the zh-TW and ko labels here are that dish's names.
# Two kinds of hub have no twin. A dish an administrator created before the convention keeps
# its own production slug (``dakhanmari``, ``kalguksu``, ``jokbal``, ``ganjang-gejang``,
# ``seolleongtang``), so its hub is spelled by the convention instead. And a hub two dishes
# share has a slug no dish will ever take: ``kr-beef-bone-soup`` gathers seolleongtang and
# gomtang, which one special covers together. Busan's milmyeon files under ``kr-naengmyeon``
# for the opposite reason: it is the same family in another city, and one hub with Seoul and
# Busan in it is the dish-across-cities shape the sub-topics exist for. ``cafe`` is the one
# that is not a dish.
#
# The labels were checked language by language against the Korea Tourism Organization's own
# sites (テジクッパ rather than デジクッパ, 刀切面 and 猪蹄 for zh-CN). ``cafe`` reads 咖啡店 in
# zh-TW because that is the site owner's word for it; KTO's Traditional Chinese pages prefer
# 咖啡廳, and either is natural in Taiwan.
TRAVEL_SEED_SUBTOPICS: tuple[tuple[str, str, Labels], ...] = (
    ("cafe", "food", ("Cafes", "カフェ", "카페", "咖啡店", "咖啡厅")),
    (
        "kr-dwaeji-gukbap",
        "food",
        ("Dwaeji-gukbap", "テジクッパ", "돼지국밥", "豬肉湯飯", "猪肉汤饭"),
    ),
    ("kr-naengmyeon", "food", ("Naengmyeon", "韓国冷麺", "냉면", "韓式冷麵", "韩国冷面")),
    ("kr-samgyetang", "food", ("Samgyetang", "サムゲタン", "삼계탕", "蔘雞湯", "参鸡汤")),
    (
        "kr-beef-bone-soup",
        "food",
        (
            "Seolleongtang & Gomtang",
            "ソルロンタン・コムタン",
            "설렁탕·곰탕",
            "雪濃湯・牛骨湯",
            "雪浓汤・牛骨汤",
        ),
    ),
    ("kr-dak-hanmari", "food", ("Dak-hanmari", "タッカンマリ", "닭한마리", "一隻雞", "一只鸡")),
    ("kr-kalguksu", "food", ("Kalguksu", "カルグクス", "칼국수", "刀切麵", "刀切面")),
    ("kr-jokbal", "food", ("Jokbal", "チョッパル", "족발", "韓式豬腳", "韩式猪蹄")),
    ("kr-tteokbokki", "food", ("Tteokbokki", "トッポッキ", "떡볶이", "辣炒年糕", "辣炒年糕")),
    ("kr-heukdwaeji", "food", ("Jeju black pork", "済州黒豚", "흑돼지", "黑豬肉", "黑猪肉")),
    ("kr-gogi-guksu", "food", ("Gogi-guksu", "コギグクス", "고기국수", "豬肉湯麵", "猪肉汤面")),
    ("kr-jjim-galbi", "food", ("Jjim-galbi", "チムカルビ", "찜갈비", "辣燉排骨", "辣炖排骨")),
    ("kr-makchang", "food", ("Makchang", "マクチャン", "막창", "烤腸", "烤肠")),
    (
        "kr-ganjang-gejang",
        "food",
        ("Ganjang-gejang", "カンジャンケジャン", "간장게장", "醬蟹", "酱蟹"),
    ),
    ("kr-bibimbap", "food", ("Bibimbap", "ビビンバ", "비빔밥", "韓式拌飯", "韩式拌饭")),
)

# The lead paragraph of each travel sub-topic's hub, which is also its meta description.
# Seeded by 0082 only where a topic has none; an editor's own text is never overwritten.
TRAVEL_TOPIC_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "cafe": {
        "zh-TW": (
            "一個街區寫一篇的咖啡店特輯：這一區怎麼逛、每家店是哪一種店，"
            "逐店附入選依據的官方來源與查核日期。"
        )
    },
    "kr-dwaeji-gukbap": {
        "zh-TW": (
            "釜山的日常湯飯，首爾也吃得到：依城市分篇，寫菜單怎麼看、桌上的佐料怎麼加，"
            "以及有官方來源點名的店家。"
        )
    },
    "kr-naengmyeon": {
        "zh-TW": (
            "首爾的平壤冷麵與咸興冷麵、釜山的小麥冷麵（밀면）：依城市分篇，"
            "寫各自的吃法與有官方來源點名的店家。"
        )
    },
    "kr-samgyetang": {
        "zh-TW": ("一人一鍋的蔘雞湯（삼계탕）：怎麼點、怎麼吃，以及各城市有官方來源點名的店家。")
    },
    "kr-beef-bone-soup": {
        "zh-TW": (
            "雪濃湯（설렁탕）與牛骨湯（곰탕）：兩種牛湯的差別、在桌上自己調味的吃法，"
            "以及各城市有官方來源點名的店家。"
        )
    },
    "kr-dak-hanmari": {
        "zh-TW": (
            "整隻雞下鍋的一隻雞（닭한마리）：怎麼點、怎麼吃，以及各城市有官方來源點名的店家。"
        )
    },
    "kr-kalguksu": {
        "zh-TW": (
            "現切麵條的韓式湯麵刀切麵（칼국수）：怎麼點、配什麼，以及各城市有官方來源點名的店家。"
        )
    },
    "kr-jokbal": {
        "zh-TW": ("韓式豬腳（족발）：份量怎麼選、怎麼包著吃，依城市分篇，附有官方來源點名的店家。")
    },
    "kr-tteokbokki": {
        "zh-TW": (
            "辣炒年糕（떡볶이）：從市場小攤到桌邊現煮的年糕鍋，依城市分篇，附有官方來源點名的店家。"
        )
    },
    "kr-heukdwaeji": {
        "zh-TW": ("濟州的黑豬肉（흑돼지）燒烤：部位怎麼選、怎麼吃，以及有官方來源點名的店家。")
    },
    "kr-gogi-guksu": {
        "zh-TW": ("濟州的豬肉湯麵（고기국수）：怎麼點、怎麼吃，以及有官方來源點名的店家。")
    },
    "kr-jjim-galbi": {
        "zh-TW": ("大邱東仁洞的辣燉排骨（찜갈비）：怎麼點、怎麼吃，以及有官方來源點名的店家。")
    },
    "kr-makchang": {"zh-TW": "大邱的烤腸（막창）：怎麼點、怎麼吃，以及有官方來源點名的店家。"},
    "kr-ganjang-gejang": {
        "zh-TW": ("醬油醃生蟹的醬蟹（간장게장）：怎麼點、怎麼吃，以及各城市有官方來源點名的店家。")
    },
    "kr-bibimbap": {
        "zh-TW": (
            "韓式拌飯（비빔밥）：全州拌飯與各城市的版本，怎麼點、怎麼拌，附有官方來源點名的店家。"
        )
    },
}

# The lifestyle section's top-level vocabulary, same shape. None of these slugs may collide
# with SEED_TOPICS or app.discovery.taxonomy.LABELS: a slug is global (uq_guide_topic_slug)
# and the section it belongs to is what keeps a "food" guide out of the lifestyle filter.
LIFE_SEED_TOPICS: tuple[tuple[str, Labels], ...] = (
    ("ai", ("AI tools", "AIツール", "AI 도구", "AI 工具", "AI 工具")),
    ("tutorial", ("Tutorials", "チュートリアル", "튜토리얼", "教學", "教程")),
    (
        "software",
        ("Apps & software", "アプリ・ソフト", "앱·소프트웨어", "軟體與 App", "软件与应用"),
    ),
    ("gadgets", ("Gadgets", "ガジェット", "가젯", "3C 裝置", "3C 设备")),
    ("productivity", ("Productivity", "仕事効率化", "생산성", "效率工作", "效率工作")),
    ("daily", ("Everyday life", "暮らし", "일상", "生活雜記", "生活杂记")),
    ("misc", ("Other", "その他", "기타", "其他", "其他")),
    # Appended, never inserted: 0075 seeds this one and
    # tests/test_guides_migration.py compares the two migrations' lists to this tuple in
    # order, so a slug that moves silently disagrees with what a live database holds.
    ("finance", ("Money & finance", "お金・家計", "돈・재테크", "理財與金錢", "理财与金钱")),
    # 0076 seeds these two, as parents for the site-building and marketing articles that
    # used to sit under ``software`` and ``misc``.
    (
        "website",
        (
            "Websites & e-commerce",
            "サイト構築・EC",
            "웹사이트·이커머스",
            "架站與電商",
            "建站与电商",
        ),
    ),
    (
        "marketing",
        ("Marketing & SEO", "マーケティング・SEO", "마케팅·SEO", "行銷與 SEO", "营销与 SEO"),
    ),
    # 0079 seeds this one, as the parent for news that is neither AI nor a 3C device:
    # chips, telecoms, platforms and the regulation of them. ``gadgets`` and ``software``
    # stay single-level, so there was nowhere else for it to hang.
    (
        "tech",
        ("Tech & industry", "テクノロジー・業界", "테크·산업", "科技與產業", "科技与产业"),
    ),
)

# slug, parent slug, (en, ja, ko, zh-TW, zh-CN). Seeded by 0076 in this order; the same
# append-only rule as LIFE_SEED_TOPICS applies. ``tutorial`` is deliberately not a parent:
# it marks the format of 659 of 818 lifestyle articles, not their subject, so the subjects
# hang under ``ai``, ``website``, ``marketing`` and ``finance`` instead.
LIFE_SEED_SUBTOPICS: tuple[tuple[str, str, Labels], ...] = (
    ("ai-terms", "ai", ("AI glossary", "AI用語解説", "AI 용어 해설", "AI 名詞解釋", "AI 名词解释")),
    ("ai-news", "ai", ("AI news", "AIニュース", "AI 뉴스", "AI 新聞與趨勢", "AI 新闻与趋势")),
    (
        "ai-search",
        "ai",
        ("AI search & GEO", "AI検索とGEO", "AI 검색과 GEO", "AI 搜尋與 GEO", "AI 搜索与 GEO"),
    ),
    ("ai-chat", "ai", ("AI assistants", "AIアシスタント", "AI 어시스턴트", "對話助理", "对话助理")),
    (
        "claude-code",
        "ai",
        ("Claude Code", "Claude Code", "Claude Code", "Claude Code", "Claude Code"),
    ),
    ("codex", "ai", ("Codex", "Codex", "Codex", "Codex", "Codex")),
    (
        "gemini-dev",
        "ai",
        (
            "Gemini CLI & API",
            "Gemini CLI・API",
            "Gemini CLI·API",
            "Gemini CLI 與 API",
            "Gemini CLI 与 API",
        ),
    ),
    (
        "ai-coding",
        "ai",
        (
            "AI coding & local models",
            "AIコーディング・ローカルLLM",
            "AI 코딩·로컬 모델",
            "AI 寫程式與本機模型",
            "AI 编程与本地模型",
        ),
    ),
    (
        "ai-create",
        "ai",
        (
            "AI images, video & audio",
            "AI画像・動画・音声",
            "AI 이미지·영상·음성",
            "AI 圖片、影片與聲音",
            "AI 图片、视频与声音",
        ),
    ),
    ("ai-work", "ai", ("AI at work", "仕事でのAI活用", "업무용 AI", "AI 工作應用", "AI 工作应用")),
    (
        "ai-safety",
        "ai",
        (
            "AI safety & privacy",
            "AIの安全と法規",
            "AI 안전·개인정보",
            "AI 安全、隱私與法規",
            "AI 安全、隐私与法规",
        ),
    ),
    (
        "ai-plans",
        "ai",
        ("AI plans & pricing", "AIの料金プラン", "AI 요금제", "AI 方案與費用", "AI 方案与费用"),
    ),
    ("wordpress", "website", ("WordPress", "WordPress", "WordPress", "WordPress", "WordPress")),
    (
        "woocommerce",
        "website",
        ("WooCommerce", "WooCommerce", "WooCommerce", "WooCommerce", "WooCommerce"),
    ),
    (
        "web-basics",
        "website",
        (
            "Domains, hosting & front-end",
            "ドメイン・ホスティング・フロントエンド",
            "도메인·호스팅·프런트엔드",
            "網域、主機與前端",
            "域名、主机与前端",
        ),
    ),
    ("seo", "marketing", ("SEO", "SEO", "SEO", "SEO", "SEO")),
    (
        "ads",
        "marketing",
        (
            "Ads & affiliates",
            "広告・アフィリエイト",
            "광고·제휴 마케팅",
            "廣告與聯盟行銷",
            "广告与联盟营销",
        ),
    ),
    (
        "content-marketing",
        "marketing",
        ("Content & brand", "コンテンツ・ブランド", "콘텐츠·브랜드", "內容與品牌", "内容与品牌"),
    ),
    (
        "finance-basics",
        "finance",
        ("Money basics", "お金の基本", "재테크 기초", "理財入門", "理财入门"),
    ),
    (
        "banking",
        "finance",
        ("Banking & payments", "銀行・決済", "은행·결제", "銀行與支付", "银行与支付"),
    ),
    (
        "credit",
        "finance",
        (
            "Credit cards & credit",
            "クレジットカード・信用",
            "신용카드·신용",
            "信用卡與信用",
            "信用卡与信用",
        ),
    ),
    (
        "tax-insurance",
        "finance",
        (
            "Tax, insurance & pensions",
            "税金・保険・年金",
            "세금·보험·연금",
            "稅務、保險與勞退",
            "税务、保险与劳退",
        ),
    ),
    (
        "investing",
        "finance",
        ("Investing basics", "投資の基本", "투자 입문", "投資入門", "投资入门"),
    ),
    # 0079 seeds these two. ``crypto`` hangs under ``finance`` rather than standing alone:
    # it is the same YMYL subject under the same review standard, and ``pack_ingest``'s
    # ``finance_no_disclaimer`` keys on it for exactly that reason.
    (
        "tech-news",
        "tech",
        ("Tech news", "テックニュース", "테크 뉴스", "科技新聞", "科技新闻"),
    ),
    (
        "crypto",
        "finance",
        (
            "Crypto & blockchain",
            "暗号資産・ブロックチェーン",
            "가상자산·블록체인",
            "加密貨幣與區塊鏈",
            "加密货币与区块链",
        ),
    ),
)

# The lead paragraph of a topic's hub page, per locale. Seeded by 0076 only where a topic
# has none yet; an editor's own text is never overwritten. Sub-topics without a lead fall
# back to their parent's on the web side.
LIFE_TOPIC_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "ai": {
        "zh-TW": (
            "從名詞解釋、工具評比到寫程式與本機模型："
            "把 AI 用在工作與生活裡的每一步，都有一篇可以照著做的文章。"
        ),
        "en": (
            "From glossary entries and tool comparisons to coding agents and local models: "
            "every step of putting AI to work, written to be followed."
        ),
    },
    "website": {
        "zh-TW": "自己架站與開店：WordPress、WooCommerce、網域主機與前端基礎，從零開始到上線維運。",
        "en": (
            "Build and run your own site: WordPress, WooCommerce, domains, hosting and "
            "front-end basics, from zero to live."
        ),
    },
    "marketing": {
        "zh-TW": "讓內容被看見：SEO、廣告與聯盟行銷、內容與品牌經營的做法與取捨。",
        "en": (
            "Getting content seen: SEO, ads and affiliate programmes, and how to run content "
            "and a brand."
        ),
    },
    "finance": {
        "zh-TW": (
            "看懂錢的流向：記帳、銀行與信用卡、稅務保險、投資入門，只講制度與方法，不推薦商品。"
        ),
        "en": (
            "Understand where the money goes: budgeting, banking and cards, tax and insurance, "
            "investing basics. Methods and rules, never product picks."
        ),
    },
    "software": {
        "zh-TW": "軟體與 App 的設定、比較與替代方案。",
        "en": "Set-up, comparisons and alternatives for apps and software.",
    },
    "ai-terms": {"zh-TW": "一詞一篇：先講定義、再講為什麼重要、最後給一個看得懂的例子。"},
    "ai-news": {"zh-TW": "模型發布、價格變動與政策：只記錄查證過的事實與日期。"},
    "ai-search": {"zh-TW": "AI 搜尋怎麼挑內容、GEO 與 AEO 要做什麼、llms.txt 與結構化資料的實作。"},
    "ai-chat": {"zh-TW": "ChatGPT、Gemini、Claude 與其他對話助理的用法、方案與限制。"},
    "claude-code": {"zh-TW": "Claude Code 從入門到進階的系列教學，附可複製的指令與範例。"},
    "codex": {"zh-TW": "Codex 學習中心：五種語言的系列教學與練習。"},
    "gemini-dev": {"zh-TW": "Gemini CLI 與 API：安裝、認證、腳本化與整合。"},
    "ai-coding": {"zh-TW": "用 AI 寫程式的工具與工作流，以及在自己電腦上跑模型的做法。"},
    "ai-create": {"zh-TW": "圖片、影片與聲音的生成與編修工具，附授權與標示的注意事項。"},
    "ai-work": {"zh-TW": "會議、郵件、簡報、試算表與自動化流程裡的 AI 應用。"},
    "ai-safety": {"zh-TW": "帳號安全、隱私、提示注入、詐騙與各國法規。"},
    "ai-plans": {"zh-TW": "免費與付費方案、API 計價與用量控制。"},
    "wordpress": {"zh-TW": "WordPress 主題、外掛、主機與維運。"},
    "woocommerce": {"zh-TW": "WooCommerce 開店：金流、物流、稅務設定與商品 SEO。"},
    "web-basics": {"zh-TW": "網域、DNS、主機方案與前端基礎。"},
    "seo": {"zh-TW": "站內外 SEO、工具與資料來源。"},
    "ads": {"zh-TW": "Google Ads、AdSense 與聯盟行銷的設定與規範。"},
    "content-marketing": {"zh-TW": "內容行銷、品牌、電子報與社群經營。"},
    "finance-basics": {"zh-TW": "記帳、預算、緊急預備金與家庭財務的第一步。"},
    "banking": {"zh-TW": "銀行帳戶、數位銀行、行動支付與海外用卡。"},
    "credit": {"zh-TW": "信用卡怎麼選、聯徵信用分數與分期的取捨。"},
    "tax-insurance": {"zh-TW": "所得稅、勞健保、勞退與保險的制度說明。"},
    "investing": {"zh-TW": "投資的觀念、台股與海外投資的開戶與流程，不含任何買賣建議。"},
    "tech": {
        "zh-TW": "晶片、裝置、平台與電信的產業消息：只記錄查證過的事實與日期，不做推薦。",
        "en": (
            "Chips, devices, platforms and telecoms: verified facts and dates, "
            "never a recommendation."
        ),
    },
    "tech-news": {
        "zh-TW": "非 AI 的科技與產業消息：發布、法規、資安事件與服務變動，附官方來源與查核日。"
    },
    "crypto": {
        "zh-TW": (
            "加密貨幣與區塊鏈的法規、技術與產業動態。只講制度與運作方式，不寫價格、漲跌或買賣時機。"
        )
    },
}


def seed_names(labels: Labels) -> dict[str, str]:
    return dict(zip(LOCALES, labels, strict=True))


def topic_label(topic: GuideTopic, locale: Locale) -> str:
    """The reader's language if the topic has it, else the default locale, else the slug.

    A topic an administrator added may not carry all five labels yet. Showing the slug is
    honest about that; inventing a translation is not.
    """
    names = topic.names_json or {}
    return names.get(locale) or names.get(DEFAULT_LOCALE) or topic.slug


def topic_description(topic: GuideTopic, locale: Locale) -> str | None:
    """The hub lead in the reader's language, or nothing. Unlike the label, a lead in the
    wrong language is worse than none: the label is one word, the lead is a paragraph."""
    descriptions = topic.descriptions_json or {}
    text = descriptions.get(locale)
    return text.strip() if isinstance(text, str) and text.strip() else None


def topic_option(
    topic: GuideTopic,
    locale: Locale,
    *,
    parent: str | None = None,
    counts: dict[str, int] | None = None,
) -> TopicOption:
    counts = counts or {}
    return TopicOption(
        slug=topic.slug,
        label=topic_label(topic, locale),
        section=cast(Section, topic.section),
        parent=parent,
        description=topic_description(topic, locale),
        count=counts.get(locale, 0),
        counts=counts,
    )


async def parent_slugs(session: AsyncSession, topics: list[GuideTopic]) -> dict[UUID, str]:
    """``parent_id -> parent slug`` for every parent among ``topics``, in one query."""
    parent_ids = {topic.parent_id for topic in topics if topic.parent_id is not None}
    if not parent_ids:
        return {}
    rows = await session.execute(
        select(GuideTopic.id, GuideTopic.slug).where(GuideTopic.id.in_(parent_ids))
    )
    return {row.id: row.slug for row in rows}


async def topic_ids_including_children(session: AsyncSession, slug: str) -> list[UUID]:
    """The topic named by ``slug`` and, when it is a parent, its children.

    Empty when the slug is unknown, so a filter on it answers with nothing rather than
    with everything -- the same contract as ``service.kind_filter``.
    """
    normalized = slug.strip().casefold()
    parent_id = await session.scalar(select(GuideTopic.id).where(GuideTopic.slug == normalized))
    if parent_id is None:
        return []
    children = await session.scalars(select(GuideTopic.id).where(GuideTopic.parent_id == parent_id))
    return [parent_id, *children]


async def published_counts(
    session: AsyncSession, topics: list[GuideTopic]
) -> dict[UUID, dict[str, int]]:
    """Published articles per topic per locale, with a parent counting its children's.

    One query over the article-topic links joined to the published translations, then
    aggregated here: a parent's number is the distinct union of its own articles and its
    children's, so an article carrying ``ai`` and ``ai-terms`` counts once under ``ai``.
    """
    if not topics:
        return {}
    rows = await session.execute(
        select(GuideArticleTopic.topic_id, GuideArticleTopic.article_id, GuideArticleLocale.locale)
        .join(GuideArticle, GuideArticle.id == GuideArticleTopic.article_id)
        .join(GuideArticleLocale, GuideArticleLocale.article_id == GuideArticle.id)
        .where(*published_filters())
    )
    articles: dict[UUID, dict[str, set[UUID]]] = {}
    for topic_id, article_id, locale in rows:
        articles.setdefault(topic_id, {}).setdefault(locale, set()).add(article_id)
    counts: dict[UUID, dict[str, int]] = {}
    for topic in topics:
        merged: dict[str, set[UUID]] = {}
        members = [topic.id, *(child.id for child in topics if child.parent_id == topic.id)]
        for member in members:
            for locale, ids in articles.get(member, {}).items():
                merged.setdefault(locale, set()).update(ids)
        counts[topic.id] = {locale: len(ids) for locale, ids in merged.items() if ids}
    return counts


async def list_topics(
    session: AsyncSession, locale: Locale, section: Section | None = None
) -> TopicList:
    """The active vocabulary of a section with, per topic, how many articles each locale
    publishes under it. Parents come first in display order, then their children in
    theirs, so a chip row can be built from the list without sorting it again."""
    query = select(GuideTopic).where(GuideTopic.is_active.is_(True))
    if section is not None:
        query = query.where(GuideTopic.section == section)
    rows = list(await session.scalars(query.order_by(GuideTopic.display_order, GuideTopic.slug)))
    parents = await parent_slugs(session, rows)
    counts = await published_counts(session, rows)
    ordered = [row for row in rows if row.parent_id is None]
    for parent in list(ordered):
        ordered.extend(row for row in rows if row.parent_id == parent.id)
    # A child whose parent is inactive or in the other section still lists, after the rest.
    ordered.extend(row for row in rows if row not in ordered)
    return TopicList(
        topics=[
            topic_option(
                row,
                locale,
                parent=parents.get(row.parent_id) if row.parent_id else None,
                counts=counts.get(row.id),
            )
            for row in ordered
        ]
    )
