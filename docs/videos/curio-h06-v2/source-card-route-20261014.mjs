// One-time, reviewable conversion from the rejected MiniMax storyboard to
// source-led native slides. Run from the repository root with Node.js.
// The map is intentionally explicit: no card is inferred from a narration line.
import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";

const file = "docs/videos/curio-h06-v2/video.json";
const video = JSON.parse(readFileSync(file, "utf8"));
const before = video.scenes.flatMap((scene) => scene.lines.map(({ id, text }) => [id, text]));
const bgh = "來源：BGH 1970 判決掃描｜編輯整理";
const plos = "來源：Coble 等，PLOS ONE 2009";
const dna = "來源：CSHL 研究者訪談；CSUEB 解說";
const dnalc = "來源：DNA Learning Center 教材";
const nij = "來源：美國 NIJ 母系 DNA 教材";
const pubmed = "來源：Nature Genetics／PubMed 書目";
const time = "來源：TIME 1928；BGH 判決掃描";
const big = (kicker, text, source) => ({ template: "big", data: { kicker, text, sub: source } });
const compare = (title, leftHeading, leftPoint, rightHeading, rightPoint, source) => ({
  template: "compare", data: { title, left: { heading: leftHeading, points: [leftPoint] }, right: { heading: rightHeading, points: [rightPoint] }, source },
});
const stats = (title, stat, source) => ({ template: "stats", data: { title, stats: stat.map(([value, label]) => ({ value, label })), source } });
const bullets = (title, items, source) => ({ template: "bullets", data: { title, items, source } });
const steps = (title, items, source) => ({ template: "steps", data: { title, steps: items.map(([title, detail]) => ({ title, detail })), source } });

const cards = {
  "hook-hospital-door-beat-2": compare("誰先說出公主名字？", "判決版本一", "她先自稱", "判決版本二", "旁人先提", bgh),
  "hook-three-answers-beat-2": big("法院卷宗的另一條線", "另一個女人的名字", bgh),
  "hook-sample-box": compare("兩類保存檢體", "醫院保存", "病理組織", "另一組取得", "頭髮", dna),
  "hook-sample-box-beat-2": big("片頭未解的問題", "兩份檢體能回答什麼？", dna),
  "hook-forest-path": stats("俄國林地的新線索", [["2007", "林地發現不明碎片"]], plos),
  "hook-forest-path-beat-2": compare("碎片帶來的問題", "已發現", "小型遺骸碎片", "待核對", "兩名缺席孩子的身分", plos),
  "hook-empty-file": big("柏林女子的身分", "她真是安娜塔西亞嗎？", "編輯提問｜證據待查"),
  "berlin-closed-album": big("1918 年後的傳聞", "皇室留下的空位", "來源：PLOS ONE 2009｜歷史脈絡"),
  "berlin-two-visitors": big("病院裡的起點", "誰先提起安娜塔西亞？", bgh),
  "hospital-visitors-enter": stats("名字被帶進病院", [["1922", "病院出現公主身分說法"]], bgh),
  "hospital-story-spreads": big("從病院到公眾", "猜測向外流傳", bgh),
  "hospital-two-folders": compare("判決留下兩種記述", "一種說法", "她先表明身分", "另一種說法", "旁人先提出名字", bgh),
  "hospital-doorway": big("起點無法判定", "還能靠什麼辨認？", "編輯提問｜依 BGH 判決範圍"),
  "relatives-tea-tray": compare("親友態度與證明", "可以確認", "一九二八年有人接待", "仍需證據", "接待不等於身分鑑定", time),
  "relatives-letter": compare("親友證詞並不一致", "願意接待", "皇室遠親的反應", "明確否認", "另一名親近皇室者的看法", time),
  "relatives-distant-woman": bullets("證詞進入法庭", ["親友的接待與辨認", "否認公主身分的證言"], bgh),
  "relatives-court-corridor": big("民事官司", "繼承權請求進入舉證", bgh),
  "relatives-legal-question": big("官司的前提", "她要如何證明公主身分？", bgh),
  "court-day-exterior": big("身分主張必須舉證", "資料能支持請求嗎？", bgh),
  "court-closed-case": compare("案件類型", "本案在審", "民事繼承請求", "本案未審", "刑事詐欺罪", bgh),
  "court-two-parties": compare("法庭上的兩條說法", "安德森", "主張公主與繼承權", "對方", "提出另一個身分說法", bgh),
  "court-schanzkowska-name": big("卷宗裡的另一個名字", "法蘭齊絲卡・尚茨科夫斯卡", bgh),
  "court-family-album": bullets("前審衡量的材料", ["親友辨認與否認", "其他身分資料與證言"], bgh),
  "court-hamburg-corridor": stats("前審與法律審", [["1967", "前審作不利證據評價"]], bgh),
  "court-hamburg-corridor-beat-2": bullets("前審比較什麼？", ["證人曾經見過誰", "多年後的記憶與資料"], bgh),
  "court-appeal-paper": big("判決即將落下", "公主主張能成立嗎？", bgh),
  "court-two-names-logic": compare("兩種身分主張", "法院結論", "公主身分未獲證明", "後續線索", "女工身分仍要另查", bgh),
  "court-exit-day": compare("判決回答的範圍", "沒有裁定", "安德森的主觀動機", "仍待調查", "皇室家人的墓葬線索", "來源：BGH 判決；PLOS ONE 2009"),
  "grave-forest-1991": stats("第一座墓被找到", [["1970 年代末", "阿夫多寧找到第一座墓"]], plos),
  "grave-map-table": big("第一座墓", "位置保密多年", plos),
  "grave-empty-places": big("第一座墓還有缺口", "少一男、一女", plos),
  "dna-hospital-archive": big("身分研究的另一種材料", "保存檢體進入研究", pubmed),
  "dna-sealed-sample-beat-2": big("檢體來源", "醫院保存的病理組織", dna),
  "dna-hair-and-box": compare("兩份安德森檢體", "保存組織", "醫院留存的組織", "頭髮", "另一組取得的樣本", dna),
  "dna-mother-child": compare("先比對哪兩份？", "第一份", "保存組織", "第二份", "頭髮", dna),
  "dna-family-tree-pieces": steps("母系序列怎麼傳？", [["母親", "傳給子女"], ["同一母系", "親屬可共享序列"]], nij),
  "dna-lab-two-researchers-beat-2": compare("兩組研究", "分析時", "起初各自調查", "完成後", "互通比對結果", dna),
  "dna-two-glass-vials": big("下一個比對", "能對上皇后母系嗎？", dna),
  "dna-method-limit": big("另一份參照", "還要比對另一條母系", dnalc),
  "dna-blank-id": big("毛赫爾的母系關係", "尚茨科夫斯卡的旁系親屬", dnalc),
  "dna-maucher-support": compare("毛赫爾比對的意義", "能支持", "可能與女工同一母系", "不能獨自證明", "安德森的唯一姓名", "來源：DNA Learning Center；美國 NIJ"),
  "dna-forest-transition": big("還有兩個空位", "第二座墓會回答什麼？", plos),
  "grave-2007-path": stats("第二座墓", [["2007", "業餘考古者發現碎片"]], plos),
  "grave-2007-path-beat-2": steps("第二墓調查順序", [["業餘發現", "先注意到地上碎片"], ["正式調查", "隊伍隨後進場整理"]], plos),
  "grave-fragments-limit": big("碎片不能自己署名", "還要比對家族關係", plos),
  "grave-lab-two-researchers": compare("兩座墓的樣本", "第一墓", "已核對的家族資料", "第二墓", "新發現的兩人樣本", plos),
  "grave-family-board": big("第二墓的男孩", "他能對上誰？", plos),
  "end-blank-motive": compare("證據有回答的範圍", "檢體能回答", "母系親緣線索", "檢體不能回答", "她當年的內心想法", "來源：BGH 判決；美國 NIJ"),
};

const shots = video.scenes.filter((scene) => scene.template === "shot");
assert.equal(shots.length, 48, "expected exactly the current 48 unaccepted MiniMax scenes");
assert.deepEqual(new Set(shots.map((scene) => scene.id)), new Set(Object.keys(cards)), "every rejected shot must be mapped once");
for (const scene of shots) {
  const { template, data } = cards[scene.id];
  scene.template = template;
  scene.data = data;
}
// The art prompt belongs to the abandoned paid-image route. The accepted route
// has authored diagrams, sourced photos and native slides; no shot is generated.
delete video.look;
const oldDisclosure = "歷史場景的可愛卡通插圖是 AI 生成的情境示意，並非當時照片、原始判決或實際檢體；片中的三張真實歷史照片會在畫面上標示可確認的年代及館藏。安娜・安德森只用背影或剪影，不重建其臉部。";
const newDisclosure = "本集以附來源的原創圖解、對照與資料卡敘事；三張歷史照片標示可確認的年代及館藏。圖解是現代編輯整理，並非事發現場、原始判決、實際檢體或遺骸影像；不重建安娜・安德森的臉部。";
assert.ok(video.youtube.description.includes(oldDisclosure), "description disclosure changed unexpectedly");
video.youtube.description = video.youtube.description.replace(oldDisclosure, newDisclosure);
const oldSample = "頭髮信封與紙片家族分支畫面是現代教學示意，並非當年檢體、遺骸或檢驗紀錄。";
video.youtube.description = video.youtube.description.replace(oldSample, "母系與墓葬圖卡是現代教學示意，並非檢驗紀錄或遺骸照片。");
const staff = video.scenes.find((scene) => scene.id === "berlin-staff-corridor");
assert.equal(staff?.template, "big");
staff.data.sub = "來源：BGH 判決掃描｜編輯整理";
const after = video.scenes.flatMap((scene) => scene.lines.map(({ id, text }) => [id, text]));
assert.deepEqual(after, before, "narration IDs, text and order must not change");
assert.equal(video.scenes.filter((scene) => scene.template === "shot").length, 0);
writeFileSync(file, `${JSON.stringify(video, null, 2)}\n`, "utf8");
console.log(`Converted ${shots.length} shots; preserved ${before.length} lines and ${video.scenes.length} scenes.`);
