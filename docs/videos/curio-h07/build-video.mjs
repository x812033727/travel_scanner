// Draft assembler for Curio H07. Narration remains in the two reviewed Markdown
// files; this writes the pipeline's video.json without renumbering existing
// spoken lines when a new sentence is inserted elsewhere.
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const example = JSON.parse(readFileSync(path.join(here, "../curio-h01/video.json"), "utf8"));
const date = "2026-10-14";
const archivalPath = "docs/videos/curio-h07/assets/bastille-register-1698.jpg";
const archivalUrl = "https://commons.wikimedia.org/wiki/File:L%27homme_au_masque_de_fer,_acte_d%27%C3%A9crou,_1698.jpg";

// Each group stays in one broad place. The camera and foreground action vary
// within it; words and dates are composited later, never delegated to MiniMax.
const visuals = [
  [
    "A Bastille prison clerk enters a death in a heavy blank register at a desk, a barred window behind him, candlelight at night",
    "A clerk's quill pauses over a nearly blank ledger while an unidentified prisoner remains a dark silhouette beyond the office doorway, cool lamplight",
    "A sealed ministerial letter is carried into a seventeenth-century stone fortress office by one messenger, morning sun across the paper",
    "One gloved finger hovers over a covered line in a folded official letter on a wooden desk, the writing hidden from view, side light",
    "An unidentified prisoner in a plain cloak enters a fortress gate from behind, his face outside the frame, cloudy autumn afternoon",
    "A Bastille clerk opens a blank register at a desk while a prison gate stands distant through the window, pale daytime light",
    "An eighteenth-century writer reaches for an unopened letter at a plain Paris writing desk, morning light from one window",
    "One writer's hand lifts a quill above a blank letter beside a closed book, the paper facing away from camera, warm daylight",
    "A ribbon-tied case folder closes over an unseen object on a bare archive table, one hand withdrawing, dim evening light",
    "A plain sealed folder stands alone in an archive drawer, only its blank spine visible, late evening light"
  ],
  [
    "A Bastille clerk writes in a large ledger at a desk beside a barred window, black ink and a quill, winter evening light",
    "A black velvet mask lies beside a closed register in the prison office, its fabric folds clear, lamp light from above",
    "An empty stone cell with a simple cot and a closed wooden door, a soft strip of light crossing the floor",
    "A prison bell swings in a high tower over the seventeenth-century city at night, moonlight on its rim",
    "A clerk turns a single page of a heavy prison register, one gloved finger holding the corner, candlelight",
    "A plain parish burial book sits open beside a spent candle, an ink pen in the foreground, grey dawn through the window",
    "A small wooden coffin is seen from a respectful distance at a church gate, two attendants only as distant figures, misty morning",
    "A sealed ledger is carried across a quiet fortress courtyard by one clerk, autumn light and long shadows",
    "A parchment page with blank lines is placed beside a black cloth mask on a wooden desk, one hand arranging them",
    "An old fortress outer gate closes slowly behind one shadowed person, stone arch and overcast sky"
  ],
  [
    "A seventeenth-century minister signs one official letter at a broad writing desk, sealed papers nearby, midday light",
    "A messenger carries a sealed letter across a fortress courtyard on foot, mountains behind the walls, clear morning",
    "A key turns inside a heavy wooden prison door at Pignerol fortress, one guard's hand visible, hard side light",
    "A jailer carries a simple covered meal tray down a quiet corridor, one barred window at the end, afternoon light",
    "A folded official letter stands against an ink pot on a stone desk, one ribbon hanging loose, candlelight",
    "A lone prisoner in a plain dark cloak sits on a simple cot facing away from camera, a closed door behind, morning light",
    "A guard watches a closed inner door from the far side of an empty corridor, one small lantern in his hand",
    "A ministerial desk with one blank parchment sheet and a newly pressed wax seal, a hand withdrawing a stamp",
    "Four small fortress silhouettes appear on separate neutral paper cards spread across a table, one hand placing the last card",
    "A historian's hand places one question mark token beside a seventeenth-century letter on a modern archive table"
  ],
  [
    "A sea island fortress rises above a quiet Mediterranean shore, one small rowboat crossing the foreground at dawn",
    "An officer holds a sealed transfer order while standing in a stone passage, a single key hanging at his belt",
    "A route map made of plain parchment lies on a desk, one hand tracing a path between four unlabelled fortresses",
    "A shadowed prisoner walks beside a jailer through a fortress gate, viewed from behind with no face detail, cloudy morning",
    "A carriage wheel rolls through a seventeenth-century city street toward a high prison gate, late afternoon sun",
    "The Bastille outer gate looms over one arriving clerk carrying a closed ledger, cool autumn light",
    "A prison clerk bends over an open register in the Bastille office, one finger pointing to a fresh entry, candlelight",
    "A folded black cloth mask rests beside an unmarked paper name card on a desk, a quill lying across both",
    "A parish clerk closes a burial ledger after an entry, simple church office and daylight through a small window",
    "Several differently spelled name slips lie separate on a clean archive table, a hand hesitating above them"
  ],
  [
    "An eighteenth-century writer in a plain coat writes a letter at a Paris desk, a quill in one hand, morning window light",
    "A printer pulls a sheet from a hand press in a small Paris workshop, stacks of unmarked pages beside him",
    "A reader opens a freshly bound book at a café table, surprised eyes visible above the page, warm daylight",
    "A printshop worker sets metal type into a wooden composing stick, hands centred, diffuse light",
    "An old letter is laid beside a later printed book on a desk, one scholar's hand pointing to the earlier item",
    "A stage actor lifts a theatrical metal mask beside a velvet curtain, clearly backstage, warm stage light",
    "A novelist writes by a lamp at a cluttered nineteenth-century desk, a stack of blank manuscript pages on one side",
    "A theatre audience watches a distant costumed actor under warm lamps, viewed from the back of the hall",
    "A reader places a fictional iron-helmet illustration onto a pile beside a differently coloured unmarked folder",
    "A newspaper seller holds one freshly printed sheet in a busy old Paris street, soft late afternoon light"
  ],
  [
    "Two separate old case folders lie open on a modern archive table, one gloved hand compares their paper edges",
    "A researcher holds a magnifying glass over an uncertain name in a centuries-old ledger, warm desk lamp light",
    "A historian turns a page between two stacks of official documents, face not visible, quiet archive room",
    "Two portrait silhouettes on separate unlabelled cards sit beside an open register, one hand keeps them apart",
    "A narrow stone cell stands empty while a single folder remains on a desk outside, cool grey light",
    "A scholar places a question mark token between two competing folders on a neat wooden table",
    "A stack of old registers ends with one blank name card on top, sunlight through an archive window",
    "A black velvet mask is set beside an unpainted metal theatrical prop, separate on two different tables, soft studio light",
    "One hand closes a disputed case folder but leaves a small ribbon bookmark visible, quiet archive room",
    "An archive drawer stays slightly open after a clerk walks away, one folder visible inside, low evening light"
  ],
  [
    "A worn case folder slides back into a labelled drawer with the label left blank, one hand visible, sunset light",
    "A clerk presses a plain red stamp onto a closed folder in an archive office, only one clear action, warm light",
    "The archive cabinet closes with one folder still visible through a narrow gap, quiet blue evening light"
  ]
];

function readSections(filename) {
  const body = readFileSync(path.join(here, filename), "utf8").replace(/\r/g, "");
  const sections = [];
  for (const raw of body.split("\n")) {
    const line = raw.trim();
    if (!line) continue;
    const heading = line.match(/^#{2,3}\s+(.+)$/);
    if (heading) { sections.push({ title: heading[1].trim(), lines: [] }); continue; }
    if (line.startsWith("# ") || line.startsWith("<!--") || line.startsWith("來源：")) continue;
    if (!sections.length) throw new Error(`${filename}: narration before first ## heading`);
    sections.at(-1).lines.push(line.replace(/^[-*]\s+/, "").replace(/\s*\[C\d+(?:,\s*C\d+)*\]$/, ""));
  }
  return sections.filter((section) => section.lines.length);
}

const sections = [
  ...readSections("narration-first.md"),
  ...readSections("narration-second.md")
];
if (sections.length < 5 || sections.length > 7) throw new Error(`expected 5–7 narrated sections, got ${sections.length}`);

const clean = (text) => text.replace(/\*\*/g, "").replace(/\s*\([^)]*C\d+[^)]*\)\s*$/, "").trim();
const seenText = new Map();
const cameras = ["slow push in", "slow pan left", "slow drift", "slow pull out", "slow pan right", "slow tilt up", "slow tilt down"];
const sizes = ["Wide shot", "Medium shot", "Close-up", "Overhead shot", "Medium close-up", "Low-angle shot", "Macro close-up", "From behind", "High-angle shot", "Extreme close-up"];
const delivery = ["低聲，放慢", "短停後繼續", "平穩，留白", "強調關鍵字", "輕微提高疑問語氣", "壓低，留下懸念"];
const documentaryCards = {
  "h07-22b75408": {
    template: "compare",
    data: {
      title: "傳說不能替囚犯填姓名",
      left: { heading: "後世故事", points: ["金屬頭罩", "王室雙胞胎"] },
      right: { heading: "獄方紀錄", points: ["真名：未確證"] },
      verdict: "故事可以傳播，身分仍要靠文件查證",
      source: "伏爾泰；大仲馬小說；Funck-Brentano 1899"
    },
    claims: ["C16", "C17"]
  },
  "h07-143be677": {
    template: "compare",
    data: {
      title: "兩份可核查的姓名線索",
      left: { heading: "1669 年公文", points: ["記下：多熱"] },
      right: { heading: "1703 年下葬名摹本", points: ["Marchialy／Marchioly"] },
      verdict: "兩份紀錄是否指向同一人，還沒有定論",
      source: "Madry 2016；Topin 1870；Funck-Brentano 1899"
    },
    claims: ["C05", "C07", "C17"]
  },
  "h07-e690a274": {
    template: "big",
    data: {
      kicker: "1698 年 7 月移監公文",
      text: "**別讓人看見或認出囚犯**",
      sub: "僅指這趟押送的要求｜Topin 1870 英譯"
    },
    claims: ["C09"]
  },
  "h07-22c31821": {
    template: "compare",
    data: {
      title: "黑絲絨與「鐵面人」",
      left: { heading: "1703 死亡補記", points: ["面具：黑絲絨"] },
      right: { heading: "1738 伏爾泰書信", points: ["稱呼：鐵面人"] },
      verdict: "後來的名稱，不等於實物材質查驗",
      source: "Funck-Brentano 1899；Garnier 版 1738 書信"
    },
    claims: ["C03", "C12"]
  },
  "h07-a0b99b19": {
    template: "big",
    data: {
      kicker: "伏爾泰《路易十四時代》",
      text: "**下巴有鋼製彈簧**",
      sub: "書中的描述，不是留存面具的實物檢驗｜Garnier 版第 25 章"
    },
    claims: ["C13"]
  },
  "h07-a1d34f98": {
    template: "compare",
    data: {
      title: "彈簧與面具，分開看",
      left: { heading: "書中鋼製部分", points: ["下巴的彈簧"] },
      right: { heading: "整副面具材質", points: ["不能據此確定是鐵"] },
      verdict: "不能把局部機件推成整副面具",
      source: "伏爾泰《路易十四時代》Garnier 版第 25 章"
    },
    claims: ["C13"]
  },
  "h07-7e41df5a": {
    template: "big",
    data: {
      kicker: "1771 年版《哲學辭典》",
      text: "**編者增補**",
      sub: "作者是否伏爾泰仍有爭議｜Garnier 版編者註"
    },
    claims: ["C15"]
  },
  "h07-5df72cd6": {
    template: "big",
    data: {
      kicker: "1738 年伏爾泰書信",
      text: "**目擊細節：未記錄**",
      sub: "信說他問過服侍者，沒有留下逐字問答｜Garnier 版轉錄"
    },
    claims: ["C12"]
  },
  "h07-f8262028": {
    template: "big",
    data: {
      kicker: "1738 年伏爾泰書信",
      text: "**「鐵」等於材質？**",
      sub: "有這個稱呼，沒有面具實物查驗｜Garnier 版轉錄"
    },
    claims: ["C12"]
  },
  "h07-c7a67f2d": {
    template: "big",
    data: {
      kicker: "坎城｜鐵面人博物館",
      text: "**真實身分不明**",
      sub: "館方展覽說明｜cannes.com"
    },
    claims: ["C17"]
  },
  "h07-1648d74e": {
    template: "big",
    data: {
      kicker: "1771 年版《哲學辭典》",
      text: "**國王的兄長？**",
      sub: "編者增補文字；作者仍有爭議｜Garnier 1878"
    },
    claims: ["C15"]
  },
  "h07-7c22ba05": {
    template: "compare",
    data: {
      title: "兩份史料，留下不同線索",
      left: { heading: "1698 入獄登記", points: ["稱呼：蒙面囚犯", "姓名：未寫"] },
      right: { heading: "1669 關押公文", points: ["提到：多熱", "與死者：未證實同一人"] },
      verdict: "有線索可追，還不能補上真名",
      source: "BnF／Funck-Brentano 1899；Madry 2016"
    },
    claims: ["C01", "C07"]
  },
  "h07-4ee87957": {
    template: "big",
    data: {
      kicker: "1698 年巴士底入獄登記",
      text: "**聖馬爾曾在皮涅羅爾看管他**",
      sub: "副官記下的舊監獄線索｜BnF／Funck-Brentano 1899"
    },
    claims: ["C01"]
  },
  "h07-bdea9e04": {
    template: "big",
    data: {
      kicker: "1738 年致杜博斯書信",
      text: "**鐵面人**",
      sub: "伏爾泰在信中使用的稱呼｜Garnier 版轉錄"
    },
    claims: ["C12"]
  },
  "h07-172c4b5f": {
    template: "big",
    data: {
      kicker: "1669 年 7 月 19 日公文",
      text: "**那個名字是誰？**",
      sub: "先看公文寫了什麼，再看能否連到 1703 年死者"
    },
    claims: ["C07"]
  },
  "h07-067878ed": {
    template: "big",
    data: {
      kicker: "1669 年 7 月 19 日",
      text: "**盧福瓦 → 聖馬爾**",
      sub: "關押公文的發信官員與收信典獄長｜Madry 2016"
    },
    claims: ["C07"]
  },
  "h07-22215fc5": {
    template: "big",
    data: {
      kicker: "1669 年盧福瓦給聖馬爾的信",
      text: "**聖馬爾親自送飯**",
      sub: "哨兵不能聽見囚犯說話｜Madry 2016"
    },
    claims: ["C07"]
  },
  "h07-1f2116f6": {
    template: "big",
    data: {
      kicker: "1669 年盧福瓦給聖馬爾的信",
      text: "**「男僕」**",
      sub: "公文用語；不能據此確定他的職業｜Madry 2016"
    },
    claims: ["C08"]
  },
  "h07-e6345955": {
    template: "big",
    data: {
      kicker: "1669 年關押公文",
      text: "**沒有提到面具**",
      sub: "這封信沒提，不代表其他時期都沒戴｜Madry 2016"
    },
    claims: ["C07", "C11"]
  },
  "h07-458d1f68": {
    template: "big",
    data: {
      kicker: "《路易十四時代》第 25 章的移監年",
      text: "**1690 年**",
      sub: "Garnier 1878 年版轉錄"
    },
    claims: ["C13"]
  },
  "h07-42fdf9fe": {
    template: "compare",
    data: {
      title: "伏爾泰敘述與入獄登記",
      left: { heading: "書中年份", points: ["1690 年"] },
      right: { heading: "獄方登記", points: ["1698 年 9 月 18 日"] },
      verdict: "獄方入獄日期比書中年份晚八年",
      source: "伏爾泰 Garnier 1878；Funck-Brentano 1899"
    },
    claims: ["C01", "C13"]
  },
  "h07-5d60fd05": {
    template: "steps",
    data: {
      title: "若蒙面囚犯就是多熱：四站路線",
      steps: [
        { title: "皮涅羅爾" },
        { title: "埃克西耶" },
        { title: "聖瑪格麗特島" },
        { title: "巴士底獄" }
      ],
      source: "坎城鐵面人博物館；Funck-Brentano 1899"
    },
    claims: ["C10"]
  },
  "h07-ca6f2073": {
    template: "compare",
    data: {
      title: "約 34 年：囚禁還是戴面具？",
      left: { heading: "囚禁", points: ["約 1669–1703 年", "只在多熱身分推定成立時"] },
      right: { heading: "戴面具", points: ["起始時間未知", "配戴多久未知"] },
      verdict: "不能把囚禁年數當成戴面具年數",
      source: "坎城博物館；Funck-Brentano 1899"
    },
    claims: ["C10", "C11"]
  },
  "h07-5c6e9a3e": {
    template: "compare",
    data: {
      title: "下葬名的不同讀法",
      left: { heading: "Topin 1870 刊出摹本", points: ["Marchialy"] },
      right: { heading: "Funck-Brentano 1899 轉錄", points: ["Marchioly"] },
      verdict: "拼讀可比對；本名仍未確證",
      source: "Topin 1870；Funck-Brentano 1899"
    },
    claims: ["C05"]
  },
  "h07-67729286": {
    template: "big",
    data: {
      kicker: "伏爾泰敘述／1698 入獄登記",
      text: "**作家敘事 ≠ 獄方紀錄**",
      sub: "年份相差八年；核對日期仍須回到登記｜Garnier 版；Funck-Brentano 1899"
    },
    claims: ["C01", "C13"]
  },
  "h07-029cafbf": {
    template: "compare",
    data: {
      title: "兩位候選人，分開查",
      left: { heading: "多熱", points: ["1669 年公文有名"] },
      right: { heading: "馬提歐里", points: ["下葬名的後世聯想"] },
      verdict: "死者本名仍未確定",
      source: "Madry 2016；Topin 1870；Funck-Brentano 1899"
    },
    claims: ["C05", "C07", "C17"]
  },
  "h07-ec47a1b6": {
    template: "big",
    data: {
      kicker: "有條件的身分推定",
      text: "**若死者就是多熱**",
      sub: "同一典獄長的監禁路線才可接上｜坎城博物館；Funck-Brentano 1899"
    },
    claims: ["C10", "C17"]
  },
  "h07-f5c35d28": {
    template: "big",
    data: {
      kicker: "多熱身分推定成立時",
      text: "**四處／約 34 年**",
      sub: "指監禁地點與年數；不是面具配戴年數｜坎城博物館"
    },
    claims: ["C10", "C11"]
  },
  "h07-40285df9": {
    template: "big",
    data: {
      kicker: "桑尼諾的推論",
      text: "**財務總管的男僕？**",
      sub: "推測多熱曾任其僕役；並非公文記載的罪名｜UCSB 2016"
    },
    claims: ["C18"]
  },
  "h07-6c44c3b1": {
    template: "big",
    data: {
      kicker: "桑尼諾的動機推論",
      text: "**外交風險？**",
      sub: "推測秘密可能妨礙法王爭取英王參戰；不是已證實的關押理由｜UCSB 2016"
    },
    claims: ["C18"]
  },
  "h07-13f0cb04": {
    template: "big",
    data: {
      kicker: "另一條身分線索",
      text: "**下葬名**",
      sub: "有不同拼讀，不能單獨當成確定本名｜Topin 1870；Funck-Brentano 1899"
    },
    claims: ["C05"]
  },
  "h07-87ab87c4": {
    template: "compare",
    data: {
      title: "原簿已毀，刊本留存",
      left: { heading: "堂區原簿", points: ["1871 年毀失"] },
      right: { heading: "十九世紀刊本", points: ["留有不同拼讀"] },
      verdict: "可比對拼讀；刊本不是原件",
      source: "Topin 1870；Funck-Brentano 1899"
    },
    claims: ["C05"]
  },
  "h07-1fb84766": {
    template: "big",
    data: {
      kicker: "實物查驗的界線",
      text: "**沒有留存面具實物**",
      sub: "1703 年登記記黑絲絨；其他年份無從實物驗證｜坎城博物館；Funck-Brentano 1899"
    },
    claims: ["C03", "C11"]
  },
  "h07-ef2940a1": {
    template: "big",
    data: {
      kicker: "若下葬名另有所指",
      text: "**多熱路線還成立嗎？**",
      sub: "若死者不是多熱，四站／約 34 年就不能套在他身上｜坎城博物館"
    },
    claims: ["C10", "C17"]
  },
  "h07-14d8d94f": {
    template: "big",
    data: {
      kicker: "芬克布倫塔諾 1899 年的推定",
      text: "**指向馬提歐里？**",
      sub: "依下葬名轉錄提出的候選；不是原簿直接證實真名"
    },
    claims: ["C05", "C17"]
  }
};
const scenes = [];
let screenshotUsed = false;
for (let sectionIndex = 0; sectionIndex < sections.length - 1; sectionIndex++) {
  const section = sections[sectionIndex];
  const visualGroup = visuals[Math.min(sectionIndex, visuals.length - 1)];
  section.lines.forEach((rawText, lineIndex) => {
    const text = clean(rawText);
    const occurrence = seenText.get(text) ?? 0;
    seenText.set(text, occurrence + 1);
    const id = createHash("sha256").update(`h07\0${text}\0${occurrence}`).digest("hex").slice(0, 8);
    const scene = {
      id: `h07-${id}`,
      ...(lineIndex === 0 ? { chapter: section.title } : {}),
      template: "shot",
      data: {
        prompt: `${sizes[(sectionIndex * 2 + lineIndex) % sizes.length]}: ${visualGroup[lineIndex % visualGroup.length]}.`,
        camera: cameras[(sectionIndex * 3 + lineIndex) % cameras.length],
        visual: "still"
      },
      lines: [{ id, text, ...((lineIndex % 2 === 0 || /[？?]$/.test(text)) ? { emotion: delivery[(sectionIndex + lineIndex) % delivery.length] } : {}) }]
    };
    if (!screenshotUsed && sectionIndex >= 3 && /入獄登記/.test(text)) {
      scene.template = "screenshot";
      scene.data = {
        title: "1698 年巴士底獄入獄登記",
        image: archivalPath,
        highlight: { x: 10, y: 5, w: 80, h: 80 },
        caption: "寫蒙面及不公開姓名；沒有寫面具材質",
        credit: "Agence Meurisse / BnF Gallica / Wikimedia Commons，公有領域"
      };
      scene.claims = ["C01"];
      screenshotUsed = true;
    }
    if (sectionIndex === 1 && /死亡補記還寫著：面具是黑絲絨/.test(text)) {
      scene.template = "big";
      scene.data = {
        kicker: "1703 年 11 月 19 日死亡補記",
        text: "**黑絲絨**",
        sub: "Du Junca 登記｜Funck-Brentano 1899 年轉錄"
      };
      scene.claims = ["C03"];
    }
    if (sectionIndex === 3 && /黑絲絨出自死亡補記/.test(text)) {
      scene.template = "compare";
      scene.data = {
        title: "1698 入獄／1703 死亡：分開看",
        left: { heading: "1698 入獄登記", points: ["稱呼：蒙面囚犯", "本名：未寫", "材質：未寫"] },
        right: { heading: "1703 死亡補記", points: ["稱呼：蒙面囚犯", "本名：未確證", "材質：黑絲絨"] },
        verdict: "1698 照片：BnF／Commons；1703 轉錄：Funck-Brentano 1899"
      };
      scene.claims = ["C01", "C03"];
    }
    if (documentaryCards[scene.id]) Object.assign(scene, documentaryCards[scene.id]);
    scenes.push(scene);
  });
}
if (!screenshotUsed) throw new Error("narration needs a 1698 register line after section two");
const missingDocumentaryCards = Object.keys(documentaryCards).filter((id) => !scenes.some((scene) => scene.id === id));
if (missingDocumentaryCards.length) throw new Error(`narration no longer matches documentary cards: ${missingDocumentaryCards.join(", ")}`);

const closing = scenes.at(-1);
const outroSection = sections.at(-1);
if (outroSection.lines.length !== 3) throw new Error("the close needs exactly three spoken sentences");
const outroLines = outroSection.lines.map((rawText, index) => {
  const text = clean(rawText);
  return {
    id: createHash("sha256").update(`h07-outro\0${text}`).digest("hex").slice(0, 8),
    text,
    emotion: ["放慢，說出結論", "輕聲提問", "溫和邀請"][index]
  };
});
scenes.push({
  id: "h07-answer-card", chapter: outroSection.title, template: "big",
  data: { kicker: "1703 年死亡登記", text: "**黑絲絨**／身分未定", sub: "其他年份的面具材質無從確定" },
  claims: ["C03", "C17"],
  lines: [outroLines[0]]
});
scenes.push({
  id: "h07-comment-shot", template: "big",
  data: { kicker: "獄方檔案／後世傳說", text: "**你聽過哪一版？**", sub: "1698／1703 年登記，還是王室雙胞胎故事？" },
  claims: ["C01", "C03", "C16"],
  lines: [outroLines[1]]
});
scenes.push({
  id: "h07-outro", template: "outro",
  data: { title: "這份檔案：未結", cta: "你最早聽到哪一個版本？", lines: ["1703 年：黑絲絨", "身分：仍待考證"] },
  lines: [outroLines[2]]
});

const sources = [
  ["1698 年巴士底入獄登記，BnF Gallica／Wikimedia Commons", archivalUrl],
  ["Funck-Brentano, Legends of the Bastille, 1899", "https://www.gutenberg.org/ebooks/43231"],
  ["Topin, The Man with the Iron Mask, 1870", "https://www.gutenberg.org/ebooks/70207"],
  ["Voltaire, 1738 年致 Dubos 書信", "https://fr.wikisource.org/wiki/Correspondance_de_Voltaire/1738/Lettre_952"],
  ["Voltaire, Le Siècle de Louis XIV, chapitre 25", "https://fr.wikisource.org/wiki/Le_Si%C3%A8cle_de_Louis_XIV/%C3%89dition_Garnier/Chapitre_25"],
  ["Voltaire, Dictionnaire philosophique, Ana, Anecdotes", "https://fr.wikisource.org/wiki/Dictionnaire_philosophique/Garnier_%281878%29/Ana,_Anecdotes"],
  ["Alexandre Dumas, The Vicomte de Bragelonne, fiction", "https://www.gutenberg.org/ebooks/2759"],
  ["坎城市立鐵面人博物館", "https://www.cannes.com/fr/culture/musees-et-expositions/musee-du-masque-de-fer-et-du-fort-royal/a-voir-au-musee.html"],
  ["UC Santa Barbara, Paul Sonnino 研究訪談", "https://news.ucsb.edu/2016/016743/mystery-unmasked"],
  ["Madry, The Valet, Early Modern France, 2016", "https://earlymodernfrance.org/journal/2016-volume-xvii/valet-marquis-louvois%E2%80%99s-invited-guest-mystery-man-iron-mask"]
].map(([title, url]) => ({ title, url, checked_on: date }));

function lineIdContaining(fragment) {
  const found = scenes.flatMap((scene) => scene.lines ?? []).filter((line) => line.text.includes(fragment));
  if (found.length !== 1) throw new Error(`expected one line containing ${fragment}, got ${found.length}`);
  return found[0].id;
}
const loops = [
  { setup: lineIdContaining("那個名字，會不會就是副官缺少的答案"), payoff: lineIdContaining("但死亡登記沒有寫多熱"), what: "1669 年密令的名字能否證明死者身分" },
  { setup: lineIdContaining("那一筆入獄登記，會怎麼稱呼"), payoff: lineIdContaining("黑絲絨出自死亡補記"), what: "1698 年登記怎樣稱呼無名囚犯" },
  { setup: lineIdContaining("他的寫法，會讓這副面具變成什麼模樣"), payoff: lineIdContaining("伏爾泰寫的是面具下巴有鋼製彈簧"), what: "伏爾泰後來怎樣描寫面具" }
];

// Bind every illustration to its exact spoken line. The plan is intentionally
// separate from narration so an edit cannot silently pair a paid image with
// the wrong historical claim.
const promptPlan = JSON.parse(readFileSync(path.join(here, "visual-prompts.json"), "utf8"));
if (promptPlan.schema_version !== 1 || promptPlan.index_base !== 0 || !promptPlan.prompts) {
  throw new Error("visual-prompts.json has an unsupported schema");
}
for (const [index, scene] of scenes.entries()) {
  const entry = promptPlan.prompts[String(index)];
  if (scene.template !== "shot") {
    if (entry) throw new Error(`visual prompt ${index} belongs to a ${scene.template} scene`);
    continue;
  }
  if (!entry || entry.line !== scene.lines[0].text || typeof entry.prompt !== "string" || !entry.prompt.trim()) {
    throw new Error(`visual prompt ${index} does not match its spoken line`);
  }
  scene.data.prompt = entry.prompt.replace(/\.+$/, "");
}
if (Object.keys(promptPlan.prompts).length !== scenes.filter((scene) => scene.template === "shot").length) {
  throw new Error("visual prompt count does not match illustration scene count");
}

const doc = {
  schema_version: 1, slug: "curio-h07", format: "slides", category: "explainer",
  narration_locale: "zh-TW", target_minutes: [9, 11],
  voice: {
    ...example.voice,
    performance: "像翻開一份有缺頁的監獄檔案：死亡登記壓低、放慢；密令讀得緊張但不演成陰謀；伏爾泰和小說段落稍微明亮，提到原始紀錄時收住；每個條件句和年份前留半拍；最後坦白說未結，不假裝破案。"
  },
  subtitles: { burn_in: false },
  look: {
    ...example.look,
    style: "2D editorial cartoon of a French historical mystery for adults: mature people with natural adult proportions, expressive coherent faces and hands; history scenes use 17th-19th century French clothing, pale limestone forts and steep slate roofs; modern research scenes use contemporary European archives and museums; bold dark outlines, flat colours and restrained cel shading, subtle paper grain, deep navy, parchment yellow, muted teal, small warning-red accent; simple backgrounds, one clear subject near centre, 16:9",
    negative: "readable text, letters, numerals, watermarks, logos, Chinese/Japanese/Korean script, East Asian architecture and clothing, upturned tiled rooftops, manga or anime schoolchildren, babies, child-sized adults, oversized chibi heads, miniature people, extra bystanders, modern writing tools in historical scenes"
  },
  youtube: {
    category_id: 27, made_for_kids: false, default_language: "zh-TW",
    title: "鐵面人是誰？黑絲絨面具的巴士底獄檔案｜奇聞檔案局",
    description: "1703 年的巴士底獄記錄寫的是黑絲絨面具，後世為什麼稱他鐵面人？這集從 1669 年的公文、1698 年的入獄登記和 1703 年的死亡登記，一路追到伏爾泰的書信與小說傳說，分清楚當年的記載、後人的推測和至今沒有答案的身分。\n\n若把蒙面囚犯視為 1669 年公文裡的 Dauger，四座監獄與約 34 年的關押才成立；這不是戴面具的年數。王室雙胞胎是後出的故事。資料截至 2026-10-14。畫面插圖由 AI 生成；1698 年登記影像的來源與公有領域授權見圖片來源。",
    tags: ["鐵面人", "黑絲絨面具", "巴士底獄", "歷史懸案", "路易十四", "伏爾泰", "奇聞檔案局", "Man in the Iron Mask"],
    video_id: null
  },
  thumbnail: { template: "thumb", data: { headline: "**不是鐵？**", tag: "歷史懸案", sub: "1703 年的記錄", shot: scenes.find((scene) => scene.template === "shot" && scene.lines[0].text.includes("一七零三年，巴士底獄副官"))?.id } },
  loops,
  sources,
  assets: [{ path: archivalPath, source: "BnF Gallica btv1b90561976/f1; Agence Meurisse 1927 photo via Wikimedia Commons", license: "Public domain (PD-author; PD-Art/PD-old-100)", author: "Agence Meurisse", url: archivalUrl }],
  scenes
};
writeFileSync(path.join(here, "video.json"), `${JSON.stringify(doc, null, 2)}\n`, "utf8");
console.log(`H07 draft: ${sections.length} chapters; ${scenes.length} scenes; ${scenes.filter((s) => s.template === "shot").length} illustration shots; last spoken scene ${closing.id}`);
