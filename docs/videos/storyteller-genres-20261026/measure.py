"""Measure YouTube search demand per story genre (2026-10-26, round A).

Round B is the same script with the second keyword set in results.json
(queries_b). Usage: PYTHONUTF8=1 python3 measure.py out.json

For each genre, run three zh searches, keep the top 40 results of each that are
long-form (>= 4 min), dedupe by video id, and report view medians.
"""

import json
import statistics
import subprocess
import sys

GENRES = {
    "預言與末日": ["預言 末日 應驗", "諾查丹瑪斯 預言", "末日預言"],
    "歷史懸案與老刑案": ["開膛手傑克 真相", "十二宮殺手", "世紀懸案 未解之謎"],
    "災難與生還": ["鐵達尼號 沉沒 真相", "空難 生還 真實故事", "龐貝 最後一天"],
    "古文明": ["金字塔 怎麼建造", "亞特蘭提斯 真相", "失落文明"],
    "外星與UFO": ["外星人 UFO 事件", "羅斯威爾 外星人", "51區 真相"],
    "靈異與怪談": ["靈異事件 真實", "鬼屋 真實事件", "日本怪談"],
    "古代人怎麼生活": ["古代人 怎麼上廁所", "古代人 生活 真相", "皇帝的一天"],
    "歷史騙局": ["史上最大騙局", "天才騙子 真實故事", "賣掉艾菲爾鐵塔 騙子"],
    "宮廷秘史": ["慈禧 真實", "武則天 真實歷史", "後宮 秘史"],
    "深海與太空": ["馬里亞納海溝", "宇宙盡頭", "旅行者號"],
    "神秘生物": ["尼斯湖水怪", "大腳怪 真相", "未確認生物"],
    "品牌故事": ["品牌故事 崛起", "公司 倒閉 故事", "這家公司 如何 稱霸"],
    "童話神話原版": ["格林童話 原版", "希臘神話 故事", "北歐神話"],
    "中國志怪": ["聊齋 故事", "山海經 怪物", "聊齋誌異"],
    "三國": ["三國 正史", "三國演義 故事", "赤壁之戰"],
}
PER_QUERY = 40
MIN_SECONDS = 240


def search(query):
    out = subprocess.run(
        [
            sys.executable, "-m", "yt_dlp", "--flat-playlist", "--print",
            "%(id)s\t%(view_count)s\t%(duration)s\t%(channel)s\t%(title)s",
            f"ytsearch{PER_QUERY}:{query}",
        ],
        capture_output=True, text=True, encoding="utf-8", timeout=300,
    ).stdout
    rows = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 5 or parts[1] in ("NA", "None") or parts[2] in ("NA", "None"):
            continue
        vid, views, dur, channel, title = parts
        if float(dur) < MIN_SECONDS:
            continue
        rows.append({"id": vid, "views": int(views), "seconds": int(float(dur)),
                     "channel": channel, "title": title, "query": query})
    return rows


def main():
    raw = {}
    summary = []
    for genre, queries in GENRES.items():
        seen = {}
        for q in queries:
            for row in search(q):
                seen.setdefault(row["id"], row)
        rows = sorted(seen.values(), key=lambda r: -r["views"])
        raw[genre] = rows
        views = [r["views"] for r in rows]
        summary.append({
            "genre": genre,
            "videos": len(views),
            "median": int(statistics.median(views)) if views else 0,
            "p75": int(statistics.quantiles(views, n=4)[2]) if len(views) > 3 else 0,
            "over_1m": sum(v >= 1_000_000 for v in views),
            "channels": len({r["channel"] for r in rows}),
            "top": [(r["views"], r["channel"], r["title"]) for r in rows[:3]],
        })
        print(genre, summary[-1]["videos"], summary[-1]["median"], file=sys.stderr, flush=True)
    summary.sort(key=lambda s: -s["median"])
    json.dump({"summary": summary, "raw": raw}, open(sys.argv[1], "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
