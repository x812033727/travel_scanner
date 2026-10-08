"""Write a self-contained, offline player for the preschool pilot package.

The browser plays the silent picture and one selected standalone audio track.
Captions are embedded when building the page so local file playback never needs
fetch(), a web server, or cross-origin text-track permissions.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


LOCALES = ("zh-TW", "zh-CN", "ja", "ko")
PARENT_TIPS = {
    "greetings": "拿一個玩偶當新朋友，見面時揮手說 Hello，離開時說 Goodbye。孩子用動作回應也可以。",
    "feelings": "一起做開心和難過的表情，再讓孩子指一指。告訴孩子，每一種心情都可以和你分享。",
    "colors": "找紅色、藍色和黃色的安全物品，輪流說英文請對方找一找；先從兩種顏色開始。",
    "numbers": "準備三個大積木，每碰一個就數一次。換個排列再數數看，讓孩子慢慢觀察數量。",
    "actions": "清出一小塊安全空間，一起聽指令做動作。孩子也可以坐著拍手，依自己的身體狀況參與。",
}


def _seconds(value: str) -> float:
    parts = value.replace(",", ".").split(":")
    return sum(float(part) * 60**index for index, part in enumerate(reversed(parts)))


def _read_vtt(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    cues: list[dict[str, Any]] = []
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.splitlines()
        timing_index = next((i for i, line in enumerate(lines) if " --> " in line), None)
        if timing_index is None:
            continue
        timing = lines[timing_index].split(" --> ", 1)
        try:
            start = _seconds(timing[0].strip())
            end = _seconds(timing[1].strip().split()[0])
        except (ValueError, IndexError):
            continue
        content = "\n".join(lines[timing_index + 1 :]).strip()
        if content and end > start:
            cues.append({"start": start, "end": end, "text": content})
    return cues


def _text(value: Any, fallback: str = "") -> str:
    if isinstance(value, dict):
        value = value.get("zh-TW") or value.get("zh_TW") or value.get("en") or fallback
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value or fallback)


def _duration(episode: dict[str, Any]) -> float:
    if episode.get("episode_duration_ms") is not None:
        return float(episode["episode_duration_ms"]) / 1000
    if episode.get("duration_ms") is not None:
        return float(episode["duration_ms"]) / 1000
    for key in ("duration", "duration_seconds", "duration_sec"):
        if isinstance(episode.get(key), (int, float)):
            return float(episode[key])
    scenes = episode.get("scenes", [])
    return sum(float(scene.get("duration_ms", 0)) / 1000 for scene in scenes)


def write_player(resolved: dict[str, Any], output: Path) -> Path:
    """Create output/index.html beside epXX/final.mp4 and audio/caption folders."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    episodes = resolved.get("episodes", [])
    if isinstance(episodes, dict):
        episodes = [dict(value, id=key) for key, value in episodes.items()]
    prepared = []
    for index, episode in enumerate(episodes):
        episode_id = str(episode.get("id", f"ep{index + 1:02d}"))
        if not re.fullmatch(r"ep\d{2,}", episode_id):
            raise ValueError(f"Unexpected episode ID: {episode_id!r}")
        prepared.append(
            {
                "id": episode_id,
                "number": episode.get("number", index + 1),
                "season": episode.get("season", (int(episode.get("number", index + 1)) - 1) // 12 + 1),
                "title": _text(episode.get("title_zh_TW") or episode.get("title_zh-TW") or episode.get("title"), f"第 {index + 1} 集"),
                "titleEn": _text(episode.get("title_en"), "Let's learn together!"),
                "topic": _text(episode.get("topic")),
                "duration": _duration(episode),
                "goal": _text(episode.get("objectives_zh_TW") or episode.get("goal_zh_TW") or episode.get("learning_objective") or episode.get("objectives") or episode.get("goal"), "聽聽英文、跟著模仿，用動作和聲音一起練習。"),
                "parentTip": _text(episode.get("parent_tip_zh_TW") or episode.get("parent_tip") or episode.get("parent_activity"), PARENT_TIPS.get(_text(episode.get("topic")), "陪孩子一起指一指、動一動。遇到練習時可以暫停，留一點時間讓孩子回答；願意模仿，就是很好的開始。")),
                "captions": {locale: _read_vtt(output / episode_id / "captions" / f"{locale}.vtt") for locale in LOCALES},
            }
        )
    if not prepared:
        raise ValueError("At least one episode is required")
    data = json.dumps(prepared, ensure_ascii=False, separators=(",", ":"))
    # Keep all user-authored strings inside JSON, including literal </script>.
    data = data.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    page = _PAGE.replace("__EPISODE_DATA__", data).replace("__EPISODE_COUNT__", str(len(prepared)))
    path = output / "index.html"
    path.write_text(page, encoding="utf-8")
    return path


_PAGE = r'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light">
<title>Sunny 與 Pip · 幼兒英文 __EPISODE_COUNT__ 集</title>
<style>
:root{--ink:#243d35;--muted:#69776c;--cream:#faf7ed;--mint:#dcebdc;--green:#2b6150;--line:#dfdfd0;--white:#fffef8;--yellow:#f5d984;--orange:#d27950}
*{box-sizing:border-box}body{margin:0;background:var(--cream);color:var(--ink);font-family:ui-rounded,"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;line-height:1.6}button,select,input{font:inherit}button,a,input,select{-webkit-tap-highlight-color:transparent}button,select,input[type=range]{cursor:pointer}button:focus-visible,a:focus-visible,select:focus-visible,input:focus-visible{outline:3px solid #ad6c35;outline-offset:4px}button{color:inherit}a{color:var(--green)}svg{display:block}button:disabled{cursor:wait;opacity:.65}.wrap{max-width:1200px;margin:auto;padding:0 40px}.masthead{height:88px;display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line)}.brand{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:.06em}.brand-mark{display:grid;place-items:center;width:35px;height:35px;background:var(--green);border-radius:12px;color:var(--cream);font-size:19px}.edition{font-size:12px;color:var(--muted);letter-spacing:.13em}.hero{padding:40px 0 29px;display:flex;justify-content:space-between;align-items:center;gap:24px}.eyebrow{margin:0 0 9px;color:var(--green);font-size:11px;letter-spacing:.2em;font-weight:800}.hero h1{font-size:clamp(30px,4vw,43px);line-height:1.3;letter-spacing:.015em;margin:0 0 13px;font-weight:850}.hero h1 span{color:var(--green)}.intro{margin:0;font-size:14px;color:var(--muted)}.hero-art{width:158px;flex-shrink:0}.course-tags{display:flex;gap:8px;margin-top:17px;flex-wrap:wrap}.tag{font-size:11px;padding:4px 10px;border-radius:20px;border:1px solid #d2ddce;color:#4e6c57;background:#edf1e4}.layout{display:grid;grid-template-columns:minmax(0,1fr) 270px;gap:24px;align-items:start}.main-card{border:1px solid var(--line);border-radius:20px;overflow:hidden;background:var(--white);box-shadow:0 10px 35px #2e48390a}.screen{position:relative;aspect-ratio:16/9;background:#e7efdd;isolation:isolate;overflow:hidden}.screen video{display:block;width:100%;height:100%;object-fit:contain;background:#e7efdd}.captions{position:absolute;inset:auto 3% 2.8%;z-index:3;text-align:center;pointer-events:none;display:flex;justify-content:center;min-height:0}.caption-text{display:none;white-space:pre-line;background:rgba(31,46,39,.91);color:#fffdf5;padding:.13em .55em;border-radius:5px;line-height:1.3;font-size:clamp(11px,1.65vw,20px);font-weight:600;max-width:100%;text-wrap:balance;overflow-wrap:anywhere;max-height:2.86em;overflow:hidden}.caption-text.visible{display:block}.start-play{position:absolute;z-index:2;top:50%;left:50%;transform:translate(-50%,-50%);border:2px solid #fffc;border-radius:50%;width:70px;height:70px;display:grid;place-items:center;color:#fff;background:#2b6150e8;box-shadow:0 4px 20px #163c3930}.start-play[hidden]{display:none}.start-play svg{width:25px;height:25px;margin-left:4px}.controls{padding:12px 18px 14px;border-bottom:1px solid #e8e8dc}.transport{display:flex;gap:11px;align-items:center}.icon-button{border:0;padding:8px;background:transparent;display:grid;place-items:center;border-radius:8px;flex-shrink:0}.icon-button:hover{background:#edf1e4}.icon-button svg{width:20px;height:20px}.time{font-size:11px;font-variant-numeric:tabular-nums;white-space:nowrap;color:#667267}.seek{flex:1;min-width:20px;margin:0;accent-color:var(--green);height:24px}.volume{width:59px;margin:0;accent-color:var(--green)}.player-body{padding:22px 25px 25px}.now{font-size:10px;font-weight:800;color:var(--orange);letter-spacing:.15em;margin:0 0 5px}.episode-title{font-size:24px;line-height:1.4;letter-spacing:.015em;margin:0 0 3px}.episode-en{font-size:13px;color:var(--muted);margin:0 0 22px}.language-row{display:grid;grid-template-columns:1fr 1fr;gap:14px}.field label{display:block;font-size:11px;color:#637366;font-weight:700;margin-bottom:6px}.field select{width:100%;min-height:43px;color:var(--ink);border:1px solid #d7dece;border-radius:9px;padding:8px 11px;background:#fbfcf5;font-size:13px}.subtitle-note{font-size:11px;color:var(--muted);margin:12px 0 0}.message{min-height:0;font-size:12px;color:#904522;margin:8px 0 0}.message:empty{display:none}.section-heading{display:flex;justify-content:space-between;align-items:center;margin-bottom:11px}.section-heading h2{font-size:14px;margin:0}.section-heading span{font-size:11px;color:var(--muted)}.episode-list{display:grid;gap:10px}.episode-card{width:100%;display:flex;align-items:center;text-align:left;gap:12px;border:1px solid var(--line);border-radius:13px;padding:12px;background:#fffdf4;position:relative;transition:background .15s,border-color .15s,transform .15s}.episode-card:hover{background:#f0f4e8;transform:translateY(-1px)}.episode-card[aria-current=true]{border-color:#5d8c73;background:#eaf2e4;box-shadow:0 0 0 1px #5d8c7317}.tile{width:53px;height:53px;flex-shrink:0;background:#e4eadb;border-radius:10px;display:grid;place-items:center;color:#39604d;font-size:25px;font-weight:900}.episode-card:nth-child(2) .tile{background:#f7e7b2;color:#946c38}.episode-card:nth-child(3) .tile{background:#f3d7c5;color:#a66a46}.episode-card:nth-child(4) .tile{background:#dce8ee;color:#4b7780}.episode-card:nth-child(5) .tile{background:#e8dded;color:#7c5e83}.card-copy{min-width:0}.card-eyebrow{font-size:9px;color:#73806f;letter-spacing:.06em;margin-bottom:1px}.card-title{display:block;font-size:13px;font-weight:800;line-height:1.45}.card-time{display:block;font-size:10px;color:var(--muted);margin-top:3px}.aside-note{margin:17px 2px 0;color:var(--muted);font-size:11px;line-height:1.9}.learning{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin:24px 0 28px}.learning article{border:1px solid var(--line);border-radius:15px;padding:19px 23px;background:#f5f4e9}.learning h2{font-size:13px;margin:0 0 7px;display:flex;align-items:center;gap:7px}.learning p{font-size:12px;color:#637263;margin:0;line-height:1.9}.small-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#75a787}.small-dot.gold{background:#d4b264}.foot{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:0 0 34px;font-size:11px;color:var(--muted)}.download{display:inline-flex;gap:7px;align-items:center;font-size:12px;text-decoration:none;border-bottom:1px solid #8ca38d;padding-bottom:2px;white-space:nowrap}.download svg{width:15px;height:15px}.foot p{margin:0}.keyboard-note{font-size:10px;display:block;color:#8a9184;margin-top:3px}
.season-field{margin:0 0 14px}.episode-list{max-height:620px;overflow:auto;padding:2px 5px 5px 2px}.episode-card[hidden]{display:none}.episode-list .episode-card:last-child{grid-column:auto}
@media(min-width:1100px){.hero-art{margin-right:43px}}
@media(max-width:850px){.wrap{padding:0 24px}.layout{grid-template-columns:minmax(0,1fr) 230px;gap:17px}.episode-card{padding:10px;gap:9px}.tile{width:42px;height:47px;font-size:22px}.player-body{padding:18px}.hero{padding-top:30px}.hero-art{width:132px}.volume{display:none}.caption-text{font-size:clamp(11px,1.7vw,17px)}.episode-title{font-size:21px}}
@media(max-width:650px){.wrap{padding:0 18px}.masthead{height:70px}.brand{font-size:14px}.edition{font-size:9px;letter-spacing:.08em}.hero{padding:27px 0 24px;gap:10px}.hero h1{font-size:29px}.hero-art{width:92px}.intro{font-size:12px;max-width:250px}.eyebrow{font-size:9px}.tag{font-size:9px;padding:3px 8px}.course-tags{gap:5px;margin-top:13px}.layout{display:flex;flex-direction:column;gap:25px}.main-card{width:100%;border-radius:15px}.playlist{width:100%}.episode-list{grid-template-columns:1fr 1fr;gap:9px}.episode-card{min-height:91px}.episode-card:last-child{grid-column:1/-1}.episode-card:last-child .tile{width:42px}.card-title{font-size:12px}.aside-note{margin:10px 0 0}.controls{padding:9px 10px}.transport{gap:5px}.icon-button{padding:7px}.time{font-size:10px}.start-play{width:55px;height:55px}.start-play svg{width:21px;height:21px}.player-body{padding:17px}.episode-title{font-size:21px}.episode-en{margin-bottom:17px;font-size:12px}.caption-text{font-size:clamp(10px,2.65vw,16px)}.language-row{gap:10px}.field select{font-size:12px}.learning{grid-template-columns:1fr;gap:12px;margin-top:20px}.learning article{padding:17px 19px}.foot{flex-direction:column;align-items:flex-start;gap:13px;padding-bottom:25px}.keyboard-note{display:none}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
</style>
</head>
<body>
<div class="wrap">
  <header class="masthead"><div class="brand"><span class="brand-mark" aria-hidden="true">a</span>Sunny 與 Pip 的英文小花園</div><span class="edition">PRESCHOOL · __EPISODE_COUNT__ LESSONS</span></header>
  <section class="hero" aria-labelledby="page-title">
    <div><p class="eyebrow">LITTLE STEPS, HAPPY LEARNING</p><h1 id="page-title">小小英語，<span>一起開口。</span></h1><p class="intro">聽一聽、說一說，和孩子一起開始英文小冒險。</p><div class="course-tags"><span class="tag">幼兒啟蒙</span><span class="tag">__EPISODE_COUNT__ 集互動練習</span><span class="tag">四語教學・英文示範</span></div></div>
    <svg class="hero-art" viewBox="0 0 160 148" role="img" aria-label="小熊 Sunny 和小鳥 Pip"><path d="M25 88C6 65 29 28 73 31s73 18 76 52-24 61-64 59S30 122 25 88Z" fill="#deead7"/><circle cx="48" cy="48" r="17" fill="#f5ddb4" stroke="#ba9970" stroke-width="2"/><circle cx="104" cy="48" r="17" fill="#f5ddb4" stroke="#ba9970" stroke-width="2"/><circle cx="48" cy="48" r="10" fill="#edd0a0"/><circle cx="104" cy="48" r="10" fill="#edd0a0"/><path d="M49 95h53l9 34c-15 12-47 12-62 0Z" fill="#599b89"/><circle cx="77" cy="72" r="39" fill="#f5ddb4" stroke="#ba9970" stroke-width="2"/><ellipse cx="77" cy="83" rx="25" ry="18" fill="#fff4db"/><circle cx="62" cy="71" r="3" fill="#3f5147"/><circle cx="92" cy="71" r="3" fill="#3f5147"/><ellipse cx="77" cy="80" rx="5" ry="3" fill="#3f5147"/><path d="M77 83v6m-10 0q10 12 20 0" fill="none" stroke="#3f5147" stroke-width="2" stroke-linecap="round"/><ellipse cx="52" cy="83" rx="6" ry="4" fill="#e8b9a2"/><ellipse cx="102" cy="83" rx="6" ry="4" fill="#e8b9a2"/><rect x="68" y="114" width="18" height="15" rx="3" fill="#a5c9ac"/><ellipse cx="133" cy="42" rx="18" ry="15" fill="#91bfa7"/><path d="m148 39 11 5-11 3" fill="#d9a15e"/><circle cx="139" cy="38" r="2" fill="#3f5147"/><ellipse cx="128" cy="47" rx="9" ry="6" fill="#c1dbc2"/><path d="m18 30 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1Z" fill="#edcc72"/></svg>
  </section>
  <main>
    <div class="layout">
      <section class="main-card" aria-label="英文教學影片播放器">
        <div class="screen" id="screen">
          <video id="video" muted playsinline preload="metadata" aria-label="教學影片，英文字幕已在畫面中"></video>
          <audio id="audio" preload="metadata"></audio>
          <button id="start-play" class="start-play" type="button" aria-label="播放影片"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 2v20l17-10Z"/></svg></button>
          <div class="captions"><span id="caption-text" class="caption-text"></span></div>
        </div>
        <div class="controls"><div class="transport">
          <button type="button" id="play" class="icon-button" aria-label="播放" title="播放 / 暫停"><svg id="play-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 3v18l16-9Z"/></svg></button>
          <span id="current-time" class="time">0:00</span><input id="seek" class="seek" type="range" min="0" max="1" step="0.05" value="0" aria-label="影片播放進度" aria-valuetext="0 分 0 秒"><span id="duration" class="time">0:00</span>
          <button type="button" id="mute" class="icon-button" aria-label="靜音" aria-pressed="false" title="靜音"><svg id="sound-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M11 4 6 8H2v8h4l5 4ZM15 8c3 2 3 6 0 8m3-11c5 4 5 10 0 14"/></svg></button><input type="range" id="volume" class="volume" min="0" max="1" step="0.05" value="1" aria-label="音量">
          <button type="button" id="fullscreen" class="icon-button" aria-label="全螢幕" title="全螢幕"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M8 3H3v5m13-5h5v5M3 16v5h5m8 0h5v-5"/></svg></button>
        </div></div>
        <div class="player-body">
          <p class="now" id="now">NOW PLAYING · EPISODE 01</p><h2 class="episode-title" id="episode-title"></h2><p class="episode-en" id="episode-en"></p>
          <div class="language-row"><div class="field"><label for="voice">教學配音</label><select id="voice"><option value="zh-TW">繁體中文</option><option value="zh-CN">簡體中文</option><option value="ja">日本語</option><option value="ko">한국어</option><option value="en">English</option></select></div><div class="field"><label for="cc">翻譯字幕 CC</label><select id="cc"><option value="zh-TW">繁體中文</option><option value="zh-CN">簡體中文</option><option value="ja">日本語</option><option value="ko">한국어</option><option value="off">關閉翻譯字幕</option></select></div></div>
          <p class="subtitle-note">畫面保留英文字幕。配音和翻譯字幕可以分開選擇。</p><p id="message" class="message" role="status" aria-live="polite"></p>
        </div>
      </section>
      <aside class="playlist" aria-label="選擇集數"><div class="section-heading"><h2>今天一起學什麼？</h2><span id="episode-count">共 __EPISODE_COUNT__ 集</span></div><div class="field season-field"><label for="season">選擇學習階段</label><select id="season"></select></div><div class="episode-list" id="episode-list"></div><p class="aside-note">跟著孩子的步調，一次看一集就好。<br>想再聽一次，隨時暫停或重播。</p></aside>
    </div>
    <section class="learning" aria-label="陪伴學習"><article><h2><span class="small-dot" aria-hidden="true"></span>這一集的小目標</h2><p id="goal"></p></article><article><h2><span class="small-dot gold" aria-hidden="true"></span>和孩子一起玩</h2><p id="parent-tip"></p></article></section>
  </main>
  <footer class="foot"><div><p>本系列使用合成配音，尚未套用後台正式聲音。</p><span class="keyboard-note">播放器快捷鍵：空白鍵播放 / 暫停，← → 前後 5 秒，M 靜音。</span></div><a id="download" class="download" href="ep01/final.mp4" download><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/></svg>下載這一集 MP4</a></footer>
</div>
<script id="episode-data" type="application/json">__EPISODE_DATA__</script>
<script>
'use strict';
const episodes = JSON.parse(document.getElementById('episode-data').textContent);
const $ = id => document.getElementById(id);
const video = $('video'), audio = $('audio'), seek = $('seek'), voice = $('voice'), cc = $('cc');
let current = episodes[0], wantedPlaying = false, audioGeneration = 0, animation = 0;
let audioReady = false, pendingAudioTime = 0, currentCaption = '', dragging = false;
const playPath = '<path d="M6 3v18l16-9Z"/>', pausePath = '<path d="M5 3h5v18H5zM14 3h5v18h-5z"/>';
const soundPath = '<path d="M11 4 6 8H2v8h4l5 4ZM15 8c3 2 3 6 0 8m3-11c5 4 5 10 0 14"/>';
const mutedPath = '<path d="M11 4 6 8H2v8h4l5 4ZM16 8l6 8m0-8-6 8"/>';
const formatTime = seconds => {const n = Math.max(0, Math.floor(Number.isFinite(seconds) ? seconds : 0)); return `${Math.floor(n / 60)}:${String(n % 60).padStart(2, '0')}`;};
const duration = () => Number.isFinite(video.duration) ? video.duration : current.duration || 1;
function message(text = '') { $('message').textContent = text; }
function controls() {
  $('play-icon').innerHTML = wantedPlaying ? pausePath : playPath;
  $('play').setAttribute('aria-label', wantedPlaying ? '暫停' : '播放');
  $('start-play').hidden = wantedPlaying;
}
function captions() {
  const cues = cc.value === 'off' ? [] : current.captions[cc.value] || [];
  const cue = cues.find(item => video.currentTime >= item.start && video.currentTime < item.end);
  const text = cue ? cue.text : '';
  if (text !== currentCaption) {
    currentCaption = text;
    $('caption-text').textContent = text;
    $('caption-text').classList.toggle('visible', Boolean(text));
  }
}
function position() {
  if (!dragging) seek.value = String(video.currentTime || 0);
  $('current-time').textContent = formatTime(video.currentTime);
  seek.setAttribute('aria-valuetext', `${Math.floor(video.currentTime / 60) || 0} 分 ${Math.floor(video.currentTime % 60) || 0} 秒`);
  captions();
}
function seekAudio(time) {
  pendingAudioTime = Math.max(0, time || 0);
  if (audioReady) {
    try { audio.currentTime = Math.min(pendingAudioTime, Number.isFinite(audio.duration) ? Math.max(0, audio.duration - 0.01) : pendingAudioTime); } catch (_) {}
  }
}
function pause() {
  wantedPlaying = false;
  video.pause(); audio.pause(); cancelAnimationFrame(animation); controls(); position();
}
function frame() {
  if (!wantedPlaying) return;
  if (audioReady && !video.seeking && !video.paused && Math.abs(audio.currentTime - video.currentTime) > 0.18) seekAudio(video.currentTime);
  position(); animation = requestAnimationFrame(frame);
}
async function play() {
  if (video.ended || video.currentTime >= duration() - 0.05) { video.currentTime = 0; seekAudio(0); }
  wantedPlaying = true; controls(); message();
  const generation = audioGeneration;
  seekAudio(video.currentTime);
  try {
    // Both play calls originate in the user gesture for Safari/iOS permissions.
    await Promise.all([video.play(), audio.play()]);
    if (generation !== audioGeneration || !wantedPlaying) return;
    cancelAnimationFrame(animation); frame();
  } catch (error) {
    if (generation !== audioGeneration || !wantedPlaying || error.name === 'AbortError') return;
    pause(); message('暫時無法播放。請確認影片資料夾完整，然後再按一次播放。');
  }
}
function toggle() { wantedPlaying ? pause() : play(); }
function loadAudio() {
  audioGeneration += 1; audioReady = false;
  audio.pause(); pendingAudioTime = video.currentTime || 0;
  audio.src = `${current.id}/audio/${voice.value}.m4a`;
  audio.load();
}
function selectEpisode(episode) {
  pause(); current = episode; message();
  $('episode-title').textContent = episode.title;
  $('episode-en').textContent = episode.titleEn;
  $('now').textContent = `NOW PLAYING · EPISODE ${String(episode.number).padStart(2, '0')}`;
  $('goal').textContent = episode.goal; $('parent-tip').textContent = episode.parentTip;
  $('download').href = `${episode.id}/final.mp4`;
  $('download').download = `${episode.id}-${episode.titleEn.replace(/[^a-zA-Z0-9 -]/g, '').trim().replace(/ +/g, '-')}.mp4`;
  document.querySelectorAll('.episode-card').forEach(card => card.setAttribute('aria-current', String(card.dataset.id === episode.id)));
  video.poster = `${episode.id}/poster.jpg`;
  video.src = `${episode.id}/final.mp4`; video.muted = true; video.load();
  loadAudio();
  seek.max = String(episode.duration || 1); seek.value = '0';
  $('duration').textContent = formatTime(episode.duration); position();
}
episodes.forEach((episode, index) => {
  const card = document.createElement('button'); card.type = 'button'; card.className = 'episode-card'; card.dataset.id = episode.id; card.dataset.season = episode.season;
  card.setAttribute('aria-label', `第 ${episode.number} 集：${episode.title}`);
  const tile = document.createElement('span'); tile.className = 'tile'; tile.setAttribute('aria-hidden', 'true'); tile.textContent = String(episode.number).padStart(2, '0');
  const copy = document.createElement('span'); copy.className = 'card-copy';
  const eyebrow = document.createElement('span'); eyebrow.className = 'card-eyebrow'; eyebrow.textContent = `LESSON ${String(episode.number).padStart(2, '0')}`;
  const title = document.createElement('span'); title.className = 'card-title'; title.textContent = episode.title;
  const time = document.createElement('span'); time.className = 'card-time'; time.textContent = `${formatTime(episode.duration)} · 聽說互動`;
  copy.append(eyebrow, title, time); card.append(tile, copy); card.addEventListener('click', () => selectEpisode(episode)); $('episode-list').append(card);
});
$('episode-count').textContent = `共 ${episodes.length} 集`;
const seasonNames = {1:'第 1 季・初次開口',2:'第 2 季・我的身體與一天',3:'第 3 季・身邊的世界',4:'第 4 季・一起玩、說短句'};
[...new Set(episodes.map(episode => episode.season))].forEach(season => {
  const option = document.createElement('option'); option.value = String(season); option.textContent = seasonNames[season] || `第 ${season} 季`; $('season').append(option);
});
function filterSeason() {
  document.querySelectorAll('.episode-card').forEach(card => {card.hidden = card.dataset.season !== $('season').value;});
  $('episode-list').scrollTop = 0;
}
$('season').addEventListener('change', () => {filterSeason(); const first = episodes.find(episode => String(episode.season) === $('season').value); if(first) selectEpisode(first);});
filterSeason();
$('play').addEventListener('click', toggle); $('start-play').addEventListener('click', play);
video.addEventListener('click', toggle);
video.addEventListener('loadedmetadata', () => { seek.max = String(duration()); $('duration').textContent = formatTime(duration()); position(); });
video.addEventListener('timeupdate', position);
video.addEventListener('seeking', () => { audio.pause(); seekAudio(video.currentTime); position(); });
video.addEventListener('seeked', () => { seekAudio(video.currentTime); position(); if (wantedPlaying) audio.play().catch(() => {pause(); message('請再按一次播放，繼續觀看。');}); });
video.addEventListener('ended', pause);
video.addEventListener('pause', () => {
  if (!video.paused) return;
  audio.pause();
  if (wantedPlaying) {wantedPlaying = false; cancelAnimationFrame(animation); controls();}
});
video.addEventListener('ratechange', () => {audio.playbackRate = video.playbackRate;});
video.addEventListener('waiting', () => {if (wantedPlaying) audio.pause();});
video.addEventListener('playing', () => {if (wantedPlaying) {seekAudio(video.currentTime); audio.play().catch(() => {});}});
video.addEventListener('error', () => {pause(); message('找不到影片。請保留整個資料夾，再開啟這個播放器。');});
audio.addEventListener('loadedmetadata', () => { audioReady = true; seekAudio(pendingAudioTime); audio.playbackRate = video.playbackRate; });
audio.addEventListener('error', () => {pause(); message('這個語言的配音暫時無法播放，請確認音檔完整。');});
voice.addEventListener('change', () => {
  const wasPlaying = wantedPlaying, time = video.currentTime;
  pause(); loadAudio(); pendingAudioTime = time;
  if (wasPlaying) play();
});
cc.addEventListener('change', captions);
seek.addEventListener('input', () => {
  const time = Number(seek.value);
  if (video.readyState > 0) video.currentTime = time;
  seekAudio(time); position();
});
function volumeUI() {
  const muted = audio.muted || audio.volume === 0;
  $('sound-icon').innerHTML = muted ? mutedPath : soundPath;
  $('mute').setAttribute('aria-pressed', String(muted));
  $('mute').setAttribute('aria-label', muted ? '開啟聲音' : '靜音');
  $('mute').title = muted ? '開啟聲音' : '靜音';
  $('volume').value = String(audio.volume);
}
$('mute').addEventListener('click', () => {if(audio.volume === 0) {audio.volume = 1; audio.muted = false;} else {audio.muted = !audio.muted;} volumeUI();});
$('volume').addEventListener('input', () => {audio.volume = Number($('volume').value); audio.muted = false; volumeUI();});
audio.addEventListener('volumechange', volumeUI);
$('fullscreen').addEventListener('click', async () => {
  try {if (document.fullscreenElement) await document.exitFullscreen(); else if ($('screen').requestFullscreen) await $('screen').requestFullscreen(); else message('此瀏覽器不支援全螢幕，可將裝置轉為橫向觀看。');} catch (_) {message('此瀏覽器不支援全螢幕，可將裝置轉為橫向觀看。');}
});
document.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.target.matches('input,select,textarea,button,a') || event.target.isContentEditable) return;
  if (event.code === 'Space') {event.preventDefault(); toggle();}
  else if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {event.preventDefault(); if(video.readyState > 0) {video.currentTime = Math.max(0, Math.min(duration(), video.currentTime + (event.key === 'ArrowRight' ? 5 : -5))); seekAudio(video.currentTime); position();}}
  else if (event.key.toLowerCase() === 'm') {$('mute').click();}
});
window.addEventListener('pagehide', pause);
selectEpisode(episodes[0]); volumeUI();
</script>
</body>
</html>
'''
