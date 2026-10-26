"""Round B of measure.py: same method, second keyword set (2026-10-26).

For each genre, run three zh searches, keep the top 40 results of each that are
long-form (>= 4 min), dedupe by video id, and report view medians.
"""

import json
import statistics
import subprocess
import sys

GENRES = {
    "預言與末日": ["2027 預言", "預言家 預言 世界", "瑪雅 預言 真相"],
    "歷史懸案與老刑案": ["未解之謎 懸案", "失蹤 懸案 真相", "歷史 懸案 至今"],
    "災難與生還": ["鐵達尼號 最後", "災難 倖存者 故事", "車諾比 那一夜"],
    "古文明": ["古文明 未解之謎", "金字塔 之謎", "史前文明 證據"],
    "外星與UFO": ["UFO 目擊 事件", "外星人 證據", "不明飛行物 解密"],
    "靈異與怪談": ["靈異 故事", "怪談 真實", "鬼故事 真實事件"],
    "古代人怎麼生活": ["古代人 冷知識", "古代 生活 是怎樣", "中世紀 生活 有多慘"],
    "歷史騙局": ["騙局 歷史 最大", "騙子 騙了全世界", "龐氏騙局 由來"],
    "宮廷秘史": ["宮廷 秘聞", "皇帝 秘史", "清宮 秘史"],
    "深海與太空": ["深海 恐懼", "宇宙 有多大", "黑洞 真相"],
    "神秘生物": ["UMA 神秘生物", "水怪 目擊", "神秘生物 真的存在"],
    "品牌故事": ["品牌 背後的故事", "企業 興衰 故事", "這家公司 為什麼 倒閉"],
    "童話神話原版": ["童話 原版 黑暗", "希臘神話 宙斯", "神話 故事 起源"],
    "中國志怪": ["中國 古代 怪談", "志怪 故事", "聊齋 鬼故事"],
    "三國": ["三國 歷史 真相", "三國 人物", "諸葛亮 真實"],
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
