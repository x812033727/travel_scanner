// Offline cuts only: every narrated sentence and illustration shot comes from video.json.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const videoBytes = readFileSync(path.join(dir, "video.json"));
const video = JSON.parse(videoBytes);
const videoSha = createHash("sha256").update(videoBytes).digest("hex");
const scenesByLine = new Map(video.scenes.flatMap(scene => scene.lines.map(line => [line.id, { scene, line }])));
const take = (id, beat, headline) => {
  const found = scenesByLine.get(id);
  if (!found) throw new Error(`Missing from-episode line ${id}`);
  return { beat, shot: found.scene.id, headline, narration: [found.line.text] };
};
const common = { schema_version: 2, format: "shorts", locale: "zh-TW", line: "cut", series: "illustrated", source: { slug: video.slug }, synthetic_media: true, hashtags: ["BlackBerry", "黑莓", "品牌故事"], tags: ["BlackBerry", "黑莓", "品牌故事", "手機", "企業轉型"] };
const shorts = [
  {
    ...common, slug: `${video.slug}-short-1`,
    titles: ["BlackBerry KEYone 是誰做的？代工與授權差在哪", "黑莓手機名字還在，誰買進、誰做硬體？"],
    description: "2017 年 TCL 宣布有實體鍵盤的 BlackBerry KEYone。幾年前 Foxconn 也替 BlackBerry 做過手機，但 FY2015 申報說那些手機仍由 BlackBerry 買進轉賣；FY2017 授權夥伴接下新品牌手機的設計、製造、銷售與客服，BlackBerry 保留安全軟體與品牌授權。完整財報脈絡請看本集長片。畫面為匿名概念插畫。",
    links: [
      { label: "BlackBerry FY2015 40-F AIF", url: "https://www.sec.gov/Archives/edgar/data/1070235/000107023515000029/bbry-02282015x40fexhibit11.htm" },
      { label: "BlackBerry FY2017 40-F AIF", url: "https://www.sec.gov/Archives/edgar/data/1070235/000107023517000008/bbry-02282017x40fexhibit11.htm" },
    ],
    scenes: [
      take("x090101", "hook", "2017｜黑莓鍵盤手機"),
      take("x090103", "setup", "宣布者是 TCL"),
      take("x090104", "turn", "幾年前，Foxconn 也製造手機"),
      take("x090207", "proof", "當年由黑莓買進轉賣"),
      take("x090405", "turn", "新機交給授權夥伴"),
      take("x090408", "payoff", "黑莓授權軟體和品牌"),
    ],
  },
  {
    ...common, slug: `${video.slug}-short-2`,
    titles: ["BlackBerry 自有設備收入為何只剩 6400 萬？", "KEYone 為何不在黑莓自有設備收入裡？"],
    description: "BlackBerry 申報把 FY2016→FY2017 硬體及其他收入下降主要歸於需求轉弱與機型老化；FY2018 自有手持設備收入降至 US$64m，當年降幅主要與轉向軟體授權及夥伴製造新機有關。這個 FY2018 收入類別還包含舊機配件與修理；手機本體收入來自不再補貨的公司既有庫存。US$64m 不是 KEYone 等授權夥伴新機的銷量；金額是收入，非手機支數或利潤。完整事件請看本集長片。畫面為匿名概念插畫。",
    links: [
      { label: "BlackBerry FY2017 40-F MD&A", url: "https://www.sec.gov/Archives/edgar/data/1070235/000107023517000008/bbry-02282017x40fexhibit13.htm" },
      { label: "BlackBerry FY2018 40-F MD&A", url: "https://www.sec.gov/Archives/edgar/data/1070235/000107023518000007/bb-02282018x40fexhibit13.htm" },
    ],
    scenes: [
      take("x090501", "hook", "FY2018｜自有設備 US$64m"),
      take("x090502", "turn", "轉向授權與夥伴新機"),
      take("x090503", "contrast", "前一年另有跌幅原因"),
      take("x090509", "scope", "不是 KEYone 銷量"),
      take("x090510", "scope", "類別還含配件和修理"),
      take("x090512", "payoff", "手機本體來自舊庫存"),
      take("x090513", "close", "庫存不再補貨"),
    ],
  },
];
const length = short => short.scenes.flatMap(scene => scene.narration).join("").length;
for (const short of shorts) {
  const chars = length(short);
  if (chars < 105 || chars > 225) throw new Error(`${short.slug}: ${chars} chars outside 25–55 s planning range`);
}
const bytes = JSON.stringify(shorts, null, 2) + "\n";
writeFileSync(path.join(dir, "shorts.json"), bytes);
const shortsSha = createHash("sha256").update(bytes).digest("hex");
writeFileSync(path.join(dir, "shorts-script.md"), [
  "# X09 BlackBerry｜兩支從長片衍生的 Shorts", "",
  `主片 SHA-256：\`${videoSha}\`；Shorts SHA-256：\`${shortsSha}\`。以下文字逐句取自鎖定長片，估時以每分鐘 250–300 個字計，成片仍以 TTS／剪輯實測；片頭動畫和片尾動畫不加進 Shorts。`, "",
  ...shorts.flatMap((short, i) => [`## Short ${i + 1}｜${short.titles[0]}`, "", `- 來源：\`${short.source.slug}\`；剪輯方式：\`from-episode\`，重用主片語音與圖。`, `- 字數：${length(short)}；估時約 ${(length(short) / 300 * 60).toFixed(1)}–${(length(short) / 250 * 60).toFixed(1)} 秒。`, `- 說明中的直接資料連結：${short.links.map(link => link.url).join("、")}`, "", ...short.scenes.map(scene => `- **${scene.beat}｜${scene.headline}**（\`${scene.shot}\`）：${scene.narration.join("")}`), ""]),
].join("\n"));
console.log(JSON.stringify({ video_sha256: videoSha, shorts_sha256: shortsSha, cuts: shorts.map(short => ({ slug: short.slug, characters: length(short), estimated_seconds_at_250_cpm: +(length(short) / 250 * 60).toFixed(1), estimated_seconds_at_300_cpm: +(length(short) / 300 * 60).toFixed(1) })) }, null, 2));
