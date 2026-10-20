// Deterministic, offline X13 preproduction compiler. Never calls media or upload providers.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const slug = "story-everyday-spotify-x13";
const sources = [
  ["S1", "Spotify 2019 Q1 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000156459019013731/ck0001639920-6k_20190429.htm"],
  ["S2", "Spotify 2020 Q1 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000156459020019718/ck0001639920-6k_20200429.htm"],
  ["S3", "Spotify 2023 Q2 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000163992023000010/spot-20230630x6xk.htm"],
  ["S5", "Spotify 2024 Q2 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000163992024000009/spot-20240630x6xk.htm"],
  ["S6", "Spotify 2024 Q4 earnings exhibit", "https://www.sec.gov/Archives/edgar/data/1639920/000114036125002936/ef20042791_ex99-1.htm"],
  ["S7", "Spotify 2025 Q2 6-K", "https://www.sec.gov/Archives/edgar/data/1639920/000163992025000012/spot-20250630x6xk.htm"],
  ["S9", "Spotify 2023-07-25 Q2 earnings exhibit", "https://www.sec.gov/Archives/edgar/data/1639920/000114036123035965/brhc20056303_ex99-1.htm"],
].map(([code, title, url]) => ({ code, title, url, checked_on: "2026-10-20" }));

const sourceRefs = note => {
  const refs = new Set([...note.matchAll(/S([1-9])\s*[–-]\s*S([1-9])/g)].flatMap(([, first, last]) => Array.from({ length: Number(last) - Number(first) + 1 }, (_, i) => `S${Number(first) + i}`)));
  for (const [, number] of note.matchAll(/\bS([1-9])\b/g)) refs.add(`S${number}`);
  return [...refs].sort();
};
const markdown = readFileSync(path.join(dir, "drafts/narration.md"), "utf8");
const chapters = Array.from({ length: 6 }, () => []);
const titles = [];
let chapterIndex = -1;
for (const raw of markdown.split(/\r?\n/)) {
  const heading = raw.match(/^## 第[一二三四五六]章｜(.+)$/);
  if (heading) { chapterIndex += 1; titles.push(heading[1].replace("（開場濃縮）", "")); continue; }
  const match = raw.match(/^- `(x13\d{4})` (.*?)〔([^〕]+)〕$/);
  if (!match) continue;
  if (chapterIndex < 0 || chapterIndex > 5) throw new Error(`Narration line outside chapter: ${raw}`);
  const [, id, text, note] = match;
  if (!id.startsWith(`x13${String(chapterIndex + 1).padStart(2, "0")}`)) throw new Error(`Wrong chapter ID: ${id}`);
  if (text.length > 42) throw new Error(`Narration line over 42 chars: ${id} (${text.length})`);
  chapters[chapterIndex].push({ id, text, note, refs: sourceRefs(note) });
}
if (titles.length !== 6 || chapters.some((rows, i) => rows.length < (i === 0 ? 9 : 16))) throw new Error("Need six complete chapters");
const outro = chapters[5].splice(-3);
if (outro.map(row => row.id).join(",") !== "x130624,x130625,x130626") throw new Error("Expected exactly three ending lines");
const allRows = [...chapters.flat(), ...outro];
if (new Set(allRows.map(row => row.id)).size !== allRows.length) throw new Error("Duplicate line IDs");

const statCards = new Map([
  [
    "x130104",
    {
      "title": "兩案收購對價",
      "stats": [
        {
          "value": "€308m",
          "label": "2019 Anchor＋Gimlet；合計，含現金及股份獎酬"
        }
      ],
      "source": "S1｜2019 Q1 6-K"
    }
  ],
  [
    "x130311",
    {
      "title": "整個廣告業務｜2020 Q1 同比",
      "stats": [
        {
          "value": "+€22m",
          "label": "Ad-Supported 收入增額；非播客獨立收入"
        }
      ],
      "source": "S2｜2020 Q1 6-K"
    }
  ],
  [
    "x130312",
    {
      "title": "整個廣告業務｜2020 Q1 同比",
      "stats": [
        {
          "value": "+€42m",
          "label": "Ad-Supported 總成本增額；非播客成本"
        }
      ],
      "source": "S2｜2020 Q1 6-K"
    }
  ],
  [
    "x130315",
    {
      "title": "播客內容成本｜2020 Q1 同比",
      "stats": [
        {
          "value": "+€12m",
          "label": "Ad-Supported 總成本變動中的一項"
        }
      ],
      "source": "S2｜2020 Q1 6-K"
    }
  ],
  [
    "x130403",
    {
      "title": "部分播客內容資產沖銷",
      "stats": [
        {
          "value": "€30m",
          "label": "2023 Q2；非全部播客投資損失"
        }
      ],
      "source": "S3｜2023 Q2 6-K"
    }
  ],
  [
    "x130407",
    {
      "title": "平台可用影片播客",
      "stats": [
        {
          "value": ">100,000",
          "label": "2023-07-25 公告當時；非 6 月 30 日數"
        }
      ],
      "source": "S9｜2023 Q2 earnings exhibit"
    }
  ],
  [
    "x130410",
    {
      "title": "整個廣告業務毛利率",
      "stats": [
        {
          "value": "+1% → −6%",
          "label": "2022 Q2 → 2023 Q2；Ad-Supported"
        }
      ],
      "source": "S3｜2023 Q2 6-K"
    }
  ],
  [
    "x130501",
    {
      "title": "整個廣告業務毛利率",
      "stats": [
        {
          "value": "+13%",
          "label": "2024 Q2；Ad-Supported，前一年同季為負"
        }
      ],
      "source": "S5｜2024 Q2 6-K"
    }
  ],
  [
    "x130515",
    {
      "title": "Spotify 全公司｜2024 全年",
      "stats": [
        {
          "value": "首次營業獲利",
          "label": "整家公司全年結果；非播客獨立獲利"
        }
      ],
      "source": "S6｜2024 Q4 earnings exhibit"
    }
  ],
  [
    "x130610",
    {
      "title": "廣告欄的播客成本",
      "stats": [
        {
          "value": "−€21m",
          "label": "2025 Q2 同比；Ad-Supported 播客成本"
        }
      ],
      "source": "S7｜2025 Q2 6-K"
    }
  ]
]);

const cues = [
  [
    "a plain recording tool lies beside one blank acquisition envelope",
    "a second blank envelope arrives beside an unrelated anonymous production studio",
    "two separated unmarked worktables with a microphone on one and an audio reel on the other",
    "two closed purchase envelopes with an empty space between them",
    "an unnamed creator presses record while a distant listener's player lights up",
    "a hand touches play on a plain free audio player beside an empty ad slot",
    "an outside researcher opens an unlabeled content-change notice but keeps the result covered",
    "a different creator raises a plain camera as a member touches a blank video tile",
    "two separate playback icons face one still-covered future decision"
  ],
  [
    "two distinct unbranded worktables open toward a shared blank player",
    "an unnamed creator trims an audio waveform on a plain editing desk",
    "unbranded creator tools are packed into a simple distribution tray",
    "an unrelated studio crew passes an anonymous audio reel toward the listener side",
    "creator workbench and studio workbench send different audio tiles toward a plain player",
    "a public statement sheet sits beside growing creator and production workspaces",
    "a closed cash drawer waits beside a blank play button",
    "a free listener taps play while a blank ad placement waits for a buyer",
    "an anonymous advertiser places a coin at the unmarked ad slot",
    "music and spoken-audio symbols occupy separate spaces in one broad green service lane",
    "a member puts a monthly coin beside an orange listening screen",
    "two listeners press play on different service screens, green and orange",
    "a producer replaces a plain microphone windscreen while cost tokens accumulate off to one side",
    "cash coins and unmarked share-award tokens sit beside a purchase folder",
    "a new anonymous creator starts another recording in a different room",
    "a line of playback lights grows beside broad service income and cost trays",
    "the incoming and outgoing streams meet at a covered quarterly result"
  ],
  [
    "the broad green service line dips below its neutral mark",
    "an audio-cost tile moves into the green advertising service lane",
    "music and audio tiles share one broad advertising lane without show names",
    "a listener presses play as a broad cost pile rises outside the device",
    "many blank play lights appear faster than advertising coins",
    "a broad green report page opens with income on one side and total service cost on the other",
    "a prior-quarter green account has a small positive gap between income and cost",
    "the current-quarter income and cost trays cross, leaving a negative gap",
    "the researcher moves two dated broad service cards into a direct comparison",
    "the green whole-service income tray grows beside a still-covered total-cost tray",
    "the green whole-service total-cost tray grows further than the income tray",
    "two broad change bars show a larger cost rise than income rise",
    "a covered portion of the total cost pile is separated for inspection",
    "a small audio-content cost pile is placed inside the large service-cost field",
    "a separate royalty-cost pile stands beside, not on top of, the audio-cost pile",
    "the researcher carefully leaves the larger whole-service cost pile intact",
    "a free listener still uses a plain player while the broad green service line hangs low",
    "several anonymous audio tiles remain distinct beneath one category line",
    "the still-active play button and a below-zero category line appear in different areas",
    "a creator turns off a generic recording light after finishing an unnamed episode",
    "a later unmarked content-portfolio notice enters a different records shelf",
    "the new content folder and old green quarterly card sit on separate desks",
    "an anonymous content shelf opens with some positions hidden"
  ],
  [
    "the broad content-portfolio shelf opens, holding many unrelated unnamed assets",
    "the researcher unfolds a public portfolio notice without a show-by-show list",
    "part of a generic content-asset stack is removed from a larger shelf",
    "the remaining asset shelf stays partly occupied after a partial removal",
    "several blank audio slots close without names or show-cover art",
    "the notice shows no individual show identity, only empty label areas",
    "a separate video catalog shelf holds many blank tiles at an announcement date",
    "closed audio slots and open video tiles stay visibly separate, never the same tile",
    "an outside viewer compares the two distinct catalog shelves without linking any title",
    "a broad green service margin lane falls below neutral",
    "content-asset, contract and staffing folders enter one broad reorganization tray",
    "a broad advertising category card is set apart from all individual show tiles",
    "different anonymous listeners still hold headphones near generic devices",
    "an unrelated video creator faces a fresh unmarked camera frame",
    "a broad negative-margin sheet lies beside a future empty slot",
    "a new quarter card approaches the old broad green service line"
  ],
  [
    "the whole green service margin line crosses into positive space",
    "last-year negative card and current positive card sit in one category frame",
    "an old reorganization packet is put away beside a current-quarter clean desk",
    "a generic production workbench uses a smaller staffing and materials pile",
    "an outgoing-cost pile shrinks beside an unopened stream of incoming advertising tokens",
    "advertising coins arrive from several unbranded buyers",
    "music-shaped ad tiles bring the largest incoming pile to the green service lane",
    "podcast and self-service ad tiles enter one jointly marked conceptual tray without labels",
    "three distinct factors surround the rising green category line",
    "a free listener keeps playing beside a sealed whole-company annual-results envelope",
    "a warm orange member-service lane rises beside, but not inside, the green lane",
    "a different member taps an anonymous audio tile on a plain phone",
    "two broad service ledgers hold many content types, without show-level profit cells",
    "a sealed whole-company annual-results folder enters a room separate from quarterly ledgers",
    "a whole-company annual result card opens under a different wider frame",
    "a calendar year ring surrounds a whole-company card, apart from quarter cards",
    "the service results remain on a desk while a creator's studio door opens",
    "an anonymous listener looks at an audio player then toward a new camera setup",
    "a new unnamed creator fixes a simple camera above a plain microphone",
    "a new blank video tile is placed on an unrelated creator desk",
    "an unopened creator-program envelope arrives beside the new video tile"
  ],
  [
    "a fresh creator-program doorway opens near a plain camera",
    "four unlabeled market tiles surround a newly opened partnership door",
    "an eligible unnamed video creator receives a generic view-based compensation token",
    "the different new creator uploads an unmarked video frame",
    "an anonymous member watches a blank video tile without a midstream break symbol",
    "the creator and member appear on separate sides of a service hallway",
    "a new video-experience cost token waits between green and orange service lanes",
    "the old green lane contains all generic podcast content-cost tiles",
    "the member presses play as two colored cost lanes remain unopened",
    "the green advertising lane reveals a smaller podcast-cost area",
    "an outside reader holds the lighter green service card without claiming total savings",
    "an orange member lane receives only the relevant new video-experience cost token",
    "the green lane keeps the unrelated remaining podcast-cost tokens",
    "a transfer amount cell remains blank between green and orange lanes",
    "the analyst leaves the overall podcast-savings label blank",
    "two differently colored service lanes still both contain anonymous audio tiles",
    "a creator camera and audio microphone remain distinct instead of merging all shows",
    "the program door admits eligible new video creators but leaves other anonymous formats outside",
    "a new unnamed creator records video while a separate member watches",
    "one old purchase envelope is put aside from a still-active playback screen",
    "earlier closed audio slots and a newer creator-program door occupy distinct shelves",
    "a listener touches a new blank video play icon on an ordinary device",
    "partly closed old content shelf faces a clearly open new creator-program door"
  ]
];
const cueOverrides = new Map(Object.entries({
  "x130401": "a broad anonymous content-portfolio shelf opens in the central frame, with separate blank audio tiles and no identifiable program",
  "x130405": "several generic unmarked audio slots close in the central frame, with no show name or cover art",
  "x130406": "a public notice with no readable lettering faces anonymous closed audio slots, all in the central crop",
  "x130404": "a partly removed generic content stack and a larger remaining stack sit side by side in the central crop",
  "x130408": "closed audio slots and open video catalog tiles stack vertically, never implying they are the same program",
  "x130409": "two separate catalog shelves, one with some closed audio slots and one with available video tiles, stay centered",
  "x130601": "a fresh video creator program doorway opens beside a plain camera and microphone in the center",
  "x130603": "an eligible anonymous video creator receives an unmarked view-based payment token in the center",
  "x130605": "a Premium member watches an unbranded blank video tile without an ad interruption symbol, centered",
  "x130616": "green advertising and orange member ledgers stack vertically, each holding anonymous podcast cost tiles",
  "x130619": "a new anonymous creator records video while a different member presses play, both inside a central vertical composition",
  "x130611": "a lighter green advertising podcast-cost card sits over an unopened orange member card in the central frame",
  "x130607": "an unassigned new video cost token waits between vertically stacked green and orange service lanes",
  "x130612": "only a limited new video experience cost token moves into the orange member lane, both lanes vertically stacked",
  "x130613": "green advertising lane retains other unrelated podcast-cost tiles beneath an orange member lane",
  "x130614": "a blank unknown-transfer cell rests between vertically stacked green and orange cost lanes",
  "x130615": "an analyst removes an unsupported all-service savings sticker from a smaller green account"
}));
const camera = ["Medium shot, push in", "Close-up, pull out", "Wide shot, gentle pan left", "Overhead shot, tilt down", "Medium close-up, pan right", "Low-angle shot, lift gently"];
const rooms = ["at a plain recording table", "between a recording booth and a listening nook", "beside a free-playback window and a cost register", "along a content-catalog aisle", "between a small listener cafe and a service counter", "inside a quiet video studio facing a living area"];
const promptTails = [
  "Unidentified people only; no readable writing, corporate insignia, copyrighted illustrations or celebrity likeness. Reserve open background for editor-applied titles.",
  "All objects are plain and without print; avoid numbers, lettering and trademark shapes. Show the important gesture in full view.",
  "Do not imitate a named host, published series imagery, historical contract or company emblem. Arrange scene elements distinctly on camera.",
  "Conceptual rather than archival: empty paper surfaces and invented characters only. Compose a clear action.",
  "No generated glyphs or brand marks; exact dates and figures are added in postproduction as typeset copy.",
  "Unmarked props, fictional adults and no protected visual works. Leave an open background for typeset copy.",
];
const portraitTail = " Place hands and focal props in the central 608-pixel corridor of the 1920x1080 image for 9:16 reframing.";
const shortSourceLines = new Set(["x130401", "x130404", "x130405", "x130406", "x130408", "x130409", "x130601", "x130603", "x130605", "x130616", "x130619", "x130607", "x130611", "x130612", "x130613", "x130614", "x130615"]);
const lineFor = row => ({ id: row.id, text: row.text, pause_after_ms: 0, emotion: row.text.endsWith("？") ? "台灣國語自然說書，問題落地稍停" : "台灣國語自然說書，年份與分母清楚" });
const scenes = [];
for (const [ci, rows] of chapters.entries()) {
  let shot = 0;
  for (let i = 0; i < rows.length;) {
    const first = rows[i], second = rows[i + 1];
    const pair = second && !statCards.has(first.id) && !statCards.has(second.id) && !shortSourceLines.has(first.id) && !shortSourceLines.has(second.id) && first.text.length + second.text.length <= 34;
    const selected = pair ? [first, second] : [first];
    const sceneId = `x13-b${String(ci + 1).padStart(2, "0")}-s${String(++shot).padStart(2, "0")}`;
    const card = statCards.get(first.id);
    const scene = card
      ? { id: sceneId, template: "stats", data: card, lines: selected.map(lineFor) }
      : { id: sceneId, template: "shot", data: { prompt: `${camera[(scenes.length + ci) % camera.length]} ${rooms[ci]}, ${cueOverrides.get(first.id) ?? cues[ci][rows.indexOf(first)]}. ${promptTails[scenes.length % promptTails.length]}${selected.some(row => shortSourceLines.has(row.id)) ? portraitTail : ""}`, camera: camera[(scenes.length + ci) % camera.length], visual: "still" }, lines: selected.map(lineFor) };
    if (shot === 1) scene.chapter = titles[ci];
    scenes.push(scene);
    i += selected.length;
  }
}
scenes.push({ id: "x13-outro", template: "outro", data: { title: "播客沒有全面退場", cta: "訂閱品牌故事" }, lines: outro.map(lineFor) });
const loops = [
  ["x130106", "x130209", "免費端播放仍須廣告商買下曝光才有收入"],
  ["x130107", "x130403", "內容調整紀錄揭出部分播客內容資產沖銷"],
  ["x130108", "x130601", "更晚出現影片播客創作者的新方案"],
  ["x130109", "x130624", "關閉部分節目後並未全面放棄播客"],
  ["x130217", "x130301", "2020 廣告業務毛利轉負"],
  ["x130310", "x130312", "同一業務總成本增額超過收入增額"],
  ["x130314", "x130315", "播客內容成本是總成本增額的一項"],
  ["x130324", "x130401", "2023 重整的是內容組合的一部分"],
  ["x130406", "x130407", "若干節目關閉後，公告仍列出大量可用影片播客"],
  ["x130416", "x130501", "2024 整個廣告業務毛利轉正"],
  ["x130514", "x130515", "2024 全公司首個全年營業獲利"],
  ["x130521", "x130601", "2025 為合格影片創作者開新方案"],
  ["x130607", "x130612", "新影片會員觀看體驗相關成本列入 Premium"],
  ["x130611", "x130614", "廣告欄下降無法拆出搬移與真正節省"],
  ["x130623", "x130624", "內容收縮但新影片合作啟動，不是全面退出"],
].map(([setup, payoff, what]) => ({ setup, payoff, what }));
const position = new Map(allRows.map((row, index) => [row.id, index]));
for (const loop of loops) if (!(position.has(loop.setup) && position.has(loop.payoff) && position.get(loop.setup) < position.get(loop.payoff))) throw new Error(`Broken loop: ${JSON.stringify(loop)}`);

const description = [
  "2019 年，Spotify 連續兩天收購 Anchor 與 Gimlet，分別取得播客創作／發布工具及節目製作能力；兩案收購對價合計 €308m，含股份獎酬。2023 年部分播客內容資產被沖銷、若干節目關閉。這代表 Spotify 全面放棄播客嗎？本集沿 SEC 原件看 2020 的廣告成本壓力、2023 的內容重整、2024 的分類回升與 2025 的影片播客合作方案。",
  "",
  "2023 Q2 的 €30m 僅是部分播客內容資產沖銷；2023-07-25 公告當時平台可用影片播客超過十萬，不是同季末數，也無法對上被關節目的身分。2024 首個全年營業獲利屬全公司。2025 對合格影片播客創作者推出依觀看表現給付的 Partner Program；提供給 Premium 會員的新觀看體驗相關成本部分改列 Premium，其餘播客成本仍在 Ad-Supported。廣告欄 2025 Q2 播客成本同比少 €21m，不能全算真正節省。兩案是否回本無逐案公開收支可判。畫面是匿名概念插畫，數字由後製排字。查核日期：2026-10-20。",
  "",
  "SEC 原始資料：",
  ...sources.map(source => `${source.title}\n${source.url}`),
  "",
  "主片、兩支 Shorts 與播放清單的真實 YouTube 連結待實際上傳後回填。",
].join("\n");
const video = {
  schema_version: 1, slug, format: "drama", category: "explainer", narration_locale: "zh-TW", target_minutes: [8, 12],
  voice: { provider: "gemini", name: "Sulafat", style: "標準國語，台灣自然口音，像向朋友追一條播客服務的公開變化；日期、季度、業務範圍清楚。", performance: "從創作者錄音、聽眾按播放走向內容調整與影片合作；每個數字清楚講其分母，不把抽象帳冊念成故事主角。" },
  subtitles: { burn_in: false }, look: { preset: "cute-mystery" }, characters: [],
  series: { slug: "brand-stories-everyday-reversals-extra", episode: 13, chapter: 1 },
  music: { prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 }, loops,
  youtube: { category_id: 27, made_for_kids: false, default_language: "zh-TW", title: "Spotify 關掉節目，真的放棄播客了嗎？｜品牌故事", description, tags: ["Spotify", "播客", "品牌故事", "Anchor", "Gimlet", "商業故事"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "播客\n被放棄？", tag: "品牌故事", brand: "Spotify", shot: "x13-b01-s01" } },
  sources: sources.map(({ code, ...source }) => source), assets: [], scenes,
};
const bytes = JSON.stringify(video, null, 2) + "\n";
writeFileSync(path.join(dir, "video.json"), bytes);
const hash = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "series.json"), JSON.stringify({ kind: "story", slug: "brand-stories-everyday-reversals-extra", episode: 13, chapter: 1, planned_episodes: 20, title: "Spotify：播客重整後真的退場了嗎", logline: "2019 買進創作與製作能力，2020 廣告成本承壓，2023 部分內容資產沖銷與若干節目關閉；2024 業務毛利回升、全公司首次全年營業獲利，2025 又推出影片播客合作方案並讓部分相關成本進入 Premium。從服務措施判斷是否全面退出，不把分類變動誤當純節省。", names: ["Spotify", "Anchor", "Gimlet"], characters: [], target_minutes: 10, image_model: "image-01", style_preset: "custom", look: { preset: "cute-mystery" }, visual_tier: "stills", compilation: false }, null, 2) + "\n");
writeFileSync(path.join(dir, "script.md"), ["# X13 Spotify｜六章繁中逐句稿 v10", "", `離線前製；\`video.json\` SHA-256：\`${hash}\`。未獨立逐句審核、盲評、配音或測量實際時長。濃縮開場後接正式 5 秒片頭；最後三句後接正式 21 秒 v4 片尾。`, "", ...chapters.flatMap((rows, i) => [`## 第 ${i + 1} 章｜${titles[i]}${i === 0 ? "（開場濃縮）" : ""}`, "", ...rows.map(row => `- \`${row.id}\` ${row.text}`), ""]), "## 最後三句", "", ...outro.map(row => `- \`${row.id}\` ${row.text}`), ""].join("\n"));
writeFileSync(path.join(dir, "line-source-matrix.md"), ["# X13 Spotify｜作者逐句來源索引", "", `\`video.json\` SHA-256：\`${hash}\`。作者標記不等於獨立來源審核；來源 URL 與邊界見 [source-matrix.md](source-matrix.md)。`, "", "| 句 ID | 旁白 | 作者來源 |", "| --- | --- | --- |", ...allRows.map(row => `| \`${row.id}\` | ${row.text.replaceAll("|", "\\|")} | ${row.refs.join("、") || "敘事分析／提問"} |`), ""].join("\n"));
console.log(JSON.stringify({ video_sha256: hash, lines: allRows.length, scenes: scenes.length, shots: scenes.filter(scene => scene.template === "shot").length, cards: scenes.filter(scene => scene.template === "stats").length, opening_chars: chapters[0].map(row => row.text).join("").length, body_chars: chapters.slice(1).flat().map(row => row.text).join("").length }, null, 2));
