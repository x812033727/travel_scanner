// Authoring source for this episode. Rebuild only this folder's draft text files.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { createHash } from "node:crypto";
import { STORY_VOICE_STYLE, setPauseBeats } from "../../../tools/video/automation/register.mjs";
import { estimateTimeline, spokenUnits, formatClock } from "../../../tools/video/core/timeline.mjs";

const dir = path.dirname(fileURLToPath(import.meta.url));
const ids = readFileSync(path.join(dir, "line-ids.txt"), "utf8").replace(/^\uFEFF/, "").trim().split(/\r?\n/);
let at = 0;
const scenes = [];
const camera = ["push in", "pan right", "pull out", "tilt down", "pan left", "drift", "tilt up"];
let shotIndex = 0;
let place = "";
let lighting = [];
const line = (text, reveal) => ({ id: ids[at++], text, ...(reveal ? { reveal } : {}) });
const card = (id, template, data, text, claims = ["c1"], chapter) => {
  const texts = Array.isArray(text) ? text : [text];
  const reveals = ["chat", "steps", "compare", "bullets", "table", "stats", "terminal"].includes(template);
  scenes.push({ id, ...(chapter ? { chapter } : {}), template, data, claims, lines: texts.map((text) => line(text, reveals ? 1 : undefined)) });
};
const shot = (id, text, picture, claims = ["c1"]) => {
  scenes.push({ id, template: "shot", data: {
    prompt: `${picture.size} in ${place}, ${picture.action}, ${picture.object}, ${picture.light}; ${["the action sits at midframe", "compose the scene around the central gesture", "the subject occupies the middle third", "place the hands along the center strip"][shotIndex % 4]}`,
    camera: camera[shotIndex++ % camera.length], visual: "still",
  }, claims, lines: [line(text)] });
};
let lightAt = 0;
const p = (size, action, object, light) => ({ size, action, object, light: light ?? lighting[lightAt++ % lighting.length] });

place = "a neighborhood community center foyer on a rainy morning";
lighting = ["rain-filtered illumination diffuses through the glass entrance", "soft overcast light fills the foyer from open doors", "reflected grey sky lights the bench from behind"];
card("hook", "title", { title: "會接話，**查到了嗎？**", subtitle: "大型語言模型：一份回答，三種工作", tag: "AI 名詞十分鐘" }, "你以為話說得完整，就代表真的查到了嗎？", ["c2"], "會接話，查到了嗎");
shot("counter-arrival", "一把雨傘、一位失主，櫃台只需要交出可信的答案。", p("Wide shot", "a visitor shakes water off a coat while a volunteer gestures to an umbrella stand", "a folded fabric umbrella with a curved wooden handle", "soft daylight comes through the glass entrance"));
card("fictional-label", "big", { kicker: "故事與資料", text: "虛構示意，**不是模型實測**", sub: "用一份失物清單，分清接話、查找與計數" }, "其實接話不等於查到了，那要怎麼找到證據？", ["c1", "c2", "c3"]);
// The short cold open is a chapter of its own, directly followed by the example.
scenes.push(scenes.splice(1, 1)[0]);
scenes[2].chapter = "一份回答，三種工作";
shot("counter-hands", "這份清單寫了物件和位置，沒有寫失主叫什麼名字。", p("Close-up", "a volunteer lifts a folded umbrella by its handle", "the worn wooden handle and a fabric strap"), ["c4"]);
shot("counter-handoff", "你以為答案說得肯定，就代表每個細節都有根據。", p("Medium shot", "a volunteer offers an umbrella and a visitor pauses with an open palm", "the umbrella resting horizontally between their hands"), ["c2"]);
shot("counter-empty-hook", "其實清單裡沒有失主姓名，也沒有他的聯絡電話。", p("Low angle shot", "a volunteer points at an empty wall hook beside a hanging scarf", "a bare metal hook with a curved end"), ["c4"]);
card("first-three-jobs", "chat", { title: "同一份回答，差在哪裡？", messages: [{ side: "left", name: "查紀錄", text: "L001：雨傘、北側櫃台、未領" }, { side: "right", name: "錯誤示意", text: "已找到王先生的雨傘與電話" }] }, ["找到那一筆紀錄，可以說雨傘放在北側櫃台。", "加上王先生和電話，就是編輯刻意寫的錯誤示意。"], ["c4", "c5"]);
shot("counter-match", "查到位置跟確認所有權，是兩件需要不同證據的事。", p("Overhead shot", "two visitors compare the fabric straps of two folded umbrellas", "two different umbrella straps crossing on a wooden bench"), ["c6"]);
shot("counter-boxes", "把已知內容整理成一句話，叫做把資料寫得好懂。", p("Medium shot", "a volunteer arranges a bottle and a cap into separate shallow bins", "a ceramic bottle in a wooden bin"), ["c7"]);
shot("counter-pair", "若問未領雨傘有幾把，就要先看哪些真的還沒領。", p("Close-up", "a volunteer holds two umbrella handles together while another person checks the stand", "a pair of curved wooden handles"), ["c8"]);
card("three-jobs-card", "steps", { title: "一份回答，可以含三種工作", steps: [{ title: "生成文字", detail: "把內容組成回答" }, { title: "查找資料", detail: "回到可確認的紀錄" }, { title: "工具計數", detail: "看條件與實際結果" }] }, ["一份回答，可以同時含生成文字、查找資料和工具計數。", "拿到資料或工具結果後，最後的文字也可能由模型生成。", "三欄是核對依據和執行紀錄，不是把能力分成互斥的三種。"], ["c7", "c8", "c9"]);
shot("counter-unclaimed", "這三件事可以合作，但不能用一句肯定回答全數代替。", p("From behind", "a departing volunteer passes a basket to the next shift", "a woven basket holding one glove"), ["c7", "c9"]);
shot("counter-dog", "櫃台旁的小狗也想領帽子，清單卻不能證明是牠的。", p("Wide shot", "a visitor gently pulls a cap away from a small dog sitting beside a bench", "a plain fabric cap held above the dog's nose"), ["c1", "c6"]);
shot("counter-question", "那個很會接話的模型，到底怎麼生出眼前這段文字？", p("Medium shot", "a visitor watches a volunteer open a small empty storage drawer", "the empty wooden drawer"), ["c10"]);

place = "a bakery kitchen in late morning";
lighting = ["warm work lamps shine down on the floured counter", "hanging kitchen lights illuminate the baker's fingers", "low under-shelf lamps pool across the dough board"];
card("generation-chapter", "chapter", { title: "模型怎麼接出一句話", number: "2" }, "先把它想成學過很多語言模式的文字生成模型。", ["c10", "c11"], "模型怎麼接出一句話");
shot("bakery-skill", "大型語言模型，英文常縮寫成 LLM，這是模型的類別。", p("Wide shot", "a baker shows an apprentice how to fold a piece of dough", "a lump of dough in the apprentice's cupped hands"), ["c11"]);
shot("bakery-pieces", "文字進來，通常先轉成模型用來處理的小單位。", p("Overhead shot", "an apprentice separates a dough roll into uneven pieces", "small dough pieces arranged along a wooden board"), ["c12"]);
shot("bakery-uneven", "這些單位叫 token，並不是固定一個中文字一個單位。", p("Close-up", "an apprentice pinches a small piece from a larger piece of dough", "two dough pieces of visibly different sizes"), ["c12"]);
card("token-card", "compare", { title: "單位不是固定字數", left: { heading: "文字", points: ["字、詞與標點"] }, right: { heading: "token", points: ["依切分方式決定"] } }, ["同一段文字的切分，不能套一個通用的字數換算。", "這裡只用麵團做比喻，沒有真的在替文字計數。"], ["c12", "c1"]);
shot("bakery-next-piece", "常見的生成式模型，會依目前材料產生下一個單位。", p("Medium shot", "a baker places one dough piece at the end of a short row", "the new dough piece touching the end of the row"), ["c10"]);
shot("bakery-row", "新產生的內容又成了材料，讓後面的文字接著出現。", p("Low angle shot", "an apprentice extends a row of dough knots one knot at a time", "the nearest unfinished dough knot"), ["c10"]);
shot("bakery-selection", "接哪個單位會受前文影響，也受生成時的選擇方式影響。", p("Close-up", "a baker chooses one of two differently folded rolls from a tray", "a dough roll lifted between fingertips"), ["c13"]);
card("generation-not-all", "bullets", { title: "這段機制的範圍", items: ["常見因果式文字生成", "依已有上下文接續", "其他架構不能一概而論"] }, ["這裡講的是常見的因果式文字生成，不包辦所有架構。", "它產生這一個單位時，不能先偷看還沒生成的後文。", "不要把這種機制，說成所有語言模型完全一模一樣。"], ["c10", "c14"]);
shot("bakery-relations", "前文的誰指向誰，也會影響這一輪怎麼處理文字。", p("From behind", "two apprentices pass a bowl across a workbench while a baker points to the receiver", "a ceramic mixing bowl between two pairs of hands"), ["c15"]);
shot("bakery-carry", "比方她拿走他的杯子，光看她字，還不知道是哪個人。", p("Medium shot", "one apprentice takes a plain cup while the other reaches for a flour scoop", "a ceramic cup in the first apprentice's hand"), ["c1", "c15"]);
shot("bakery-weigh", "常見的注意力機制，用數學運算衡量材料之間的關係。", p("Overhead shot", "a baker balances different dough pieces on a simple beam scale", "a wooden balance beam and uneven dough pieces"), ["c15"]);
card("attention-boundary", "big", { kicker: "注意力機制", text: "運算關係，處理上下文" }, "它可以幫忙處理上下文和材料之間的關係。", ["c15"]);
card("attention-check", "big", { kicker: "仍要檢查", text: "不能保證每次找對指涉" }, "但是不能保證永遠找對每個指涉。", ["c16"]);
shot("bakery-mistake", "比喻像配料分量，卻不是模型裡真的住了一位麵包師。", p("Wide shot", "an apprentice notices a tiny roll sitting inside an oversized baking tin", "the tiny dough roll at the center of the tin"), ["c1"]);
shot("bakery-next-question", "那麼它學到的本事，跟你剛貼上去的資料差在哪裡？", p("Close-up", "a baker holds a dough cutter still while an apprentice presents fresh dough", "the metal cutter beside fresh dough"), ["c17"]);

place = "a pottery studio at midday";
lighting = ["cool illumination drops through overhead skylights", "a high roof opening spreads light across the wheel", "soft upper windows illuminate the wet clay"];
card("training-chapter", "chapter", { title: "訓練與貼資料差在哪", number: "3" }, "訓練塑造模型的能力，這一輪的材料提供當次資訊。", ["c17"], "訓練與貼資料差在哪");
shot("pottery-apprentice", "陶藝師練出拉胚的手感，不等於記住每個客人的杯子。", p("Wide shot", "a potter guides an apprentice's hands around a clay vessel", "a wet clay vessel between their hands"), ["c1"]);
shot("pottery-adjust", "模型訓練會調整很多數值，這些數值通常叫做參數。", p("Close-up", "a potter slightly narrows the rim of a clay bowl with two fingertips", "the clay rim between the fingertips"), ["c18"]);
shot("pottery-many-pots", "參數一起參與運算，不是一本能逐條翻查的失物簿。", p("Low angle shot", "an apprentice looks over many empty ceramic vessels on a shelf", "a smooth empty ceramic vessel in the foreground"), ["c18", "c19"]);
card("parameters-context", "compare", { title: "兩種來源，不要混在一起", left: { heading: "訓練與參數", points: ["訓練過程調整數值", "形成可運用的模式"] }, right: { heading: "當次上下文", points: ["這輪提供的材料", "用來處理眼前任務"] } }, ["參數來自訓練調整；當次上下文是這一輪能看到的材料。", "把資料貼上去，和重新進行模型訓練，是兩件不同的事。"], ["c17", "c18"]);
shot("pottery-new-clay", "你拿來一塊新黏土，改變的是這次要處理的東西。", p("Medium shot", "a visitor sets a fresh block of clay beside the potter's wheel", "a fresh clay block on a wooden board"), ["c1", "c17"]);
shot("pottery-brief", "你貼失物清單，讓這次回答有資料可用，沒有重練整個模型。", p("From behind", "a visitor places a broken ceramic handle in front of a potter", "the broken handle on a cloth mat"), ["c17"]);
shot("pottery-bare-table", "下一次對話看不看得到它，要看系統有沒有再次提供材料。", p("Overhead shot", "a potter clears a worktable while an apprentice carries the clay block away", "the newly empty patch of wooden table"), ["c20"]);
card("article-diagram", "diagram", { svg: "apps/web/public/guides/what-is-a-large-language-model/diagram-1.svg", caption: "模型、當次材料與外部工具，各有角色" }, "模型、當次材料和外部工具，請分成三個角色來看。", ["c17", "c9", "c20"]);
shot("pottery-instruction", "你還能要求用表格回答，這是調整這輪的任務指令。", p("Medium shot", "an apprentice sorts finished clay bowls into neat rows as a potter gestures", "rows of small clay bowls"), ["c21"]);
shot("pottery-limit", "要求每欄都寫滿，卻可能逼出資料根本沒有的內容。", p("Close-up", "an apprentice presses an empty mold while a potter holds back their hand", "an empty clay mold with a visible cavity"), ["c22"]);
card("unknown-rule", "chat", { title: "把不知道也留在格式裡", messages: [{ side: "left", name: "指令示意", text: "依清單回答；無法確認請寫未知" }, { side: "right", name: "編輯示意", text: "位置：北側櫃台；失主：未知" }] }, ["可以先說，只依這份清單，無法確認的欄位請寫未知。", "這是你對回答的要求；仍然要核對它有沒有真的遵守。"], ["c23"]);
shot("pottery-capability", "逐步生成是機制，不是判定它有沒有推理能力的完整考試。", p("Wide shot", "a potter tests whether a new vessel stands steadily while an apprentice observes", "a ceramic vessel resting on a narrow support"), ["c24"]);
shot("pottery-uncertainty", "會不會完成任務，得拿那個任務的結果和標準來比較。", p("Medium shot", "two apprentices inspect a repaired handle from opposite sides", "the joined ceramic handle between them"), ["c24"]);
shot("pottery-demo-question", "先不考模型，我們能不能把清單裡能確定的部分跑出來？", p("Close-up", "a potter places a finished cup on a flat testing board", "the cup's bottom touching the board"), ["c3"]);

place = "a municipal assembly hall in early afternoon";
lighting = ["broad ceiling panels illuminate the sorting trays", "an open side door spreads reflected daylight over the table", "high wall windows provide even illumination across the belongings"];
card("demo-chapter", "chapter", { title: "六筆失物，離線跑三題", number: "4" }, "只跑離線資料，三題分別是查位置、問缺欄位、數物件。", ["c3"], "六筆失物，離線跑三題");
shot("demo-six-objects", "桌上有六件虛構失物，雨傘、水瓶、圍巾、帽子和手套。", p("Wide shot", "two volunteers lay out two umbrellas, a bottle, a scarf, a cap and a glove", "the six belongings arranged on a long wooden table"), ["c25"]);
card("six-records-table", "table", { title: "虛構資料的六筆紀錄", columns: ["代號", "物件", "狀態"], rows: [["L001", "雨傘", "未領"], ["L002", "水瓶", "已領"], ["L003", "雨傘", "未領"], ["L004", "圍巾", "未領"], ["L005", "帽子", "已領"], ["L006", "手套", "未領"]] }, ["第一筆雨傘未領，第二筆水瓶已領，這兩個狀態不同。", "第三筆也是雨傘，第四筆圍巾，都還在未領清單裡。", "第五筆帽子已領，第六筆手套未領，現在有六筆紀錄。", "不要先把六筆全部加起來，問的條件會決定該算誰。", "清單保留已領紀錄，是為了示範篩選條件有多重要。", "物件代號和位置都可回查；這裡完全沒有真實失主資料。"], ["c25", "c26"]);
shot("demo-one-umbrella", "第一題，查第一筆雨傘的位置，程式先找到那個代號。", p("Close-up", "a volunteer lifts one folded umbrella away from the other objects", "the wooden umbrella handle in their fingers"), ["c4"]);
card("evidence-terminal", "terminal", { title: "有據：查那筆紀錄", prompt: ">", command: "python demo.py evidence", output: ["fictional_data=true; model_called=false", "L001 | umbrella | north_counter | unclaimed"], ran_on: "2026-10-04", tool_version: "Python 3.14.6" }, ["第一行說明虛構資料，並且沒有呼叫語言模型。", "第二行找到第一筆雨傘，位置是北側櫃台，狀態未領。"], ["c3", "c4"]);
shot("demo-counter-place", "這個回答的根據，是資料裡真的存在的那筆位置紀錄。", p("Medium shot", "a volunteer places the folded umbrella in a shallow counter tray", "the fabric umbrella lying in the wooden tray"), ["c4"]);
shot("demo-phone-gap", "第二題，問失主電話，程式先检查那個欄位是否存在。", p("Overhead shot", "a volunteer opens a small storage case and finds an empty compartment", "the empty compartment in a wooden case"), ["c4", "c27"]);
card("missing-terminal", "terminal", { title: "缺資料：不補造電話", prompt: ">", command: "python demo.py missing", output: ["record=L001; field=owner_phone", "result=UNKNOWN; reason=field_not_in_dataset"], ran_on: "2026-10-04", tool_version: "Python 3.14.6" }, ["它檢查的是失主電話欄位，而不是到別處搜尋一組電話。", "結果是未知，原因是這份資料根本沒有這個欄位。"], ["c27"]);
shot("demo-empty-palm", "查不到，不表示世界上沒電話，只表示這份資料不能回答。", p("Close-up", "a volunteer turns an empty palm upward beside a folded scarf", "the open palm and soft fabric edge"), ["c27", "c28"]);
shot("demo-two-baskets", "第三題問未領幾件，程式先按狀態把紀錄分成兩堆。", p("Wide shot", "two volunteers sort belongings into a large basket and a small basket", "two wicker baskets of visibly different contents"), ["c8", "c26"]);
shot("demo-cap-out", "水瓶和帽子已領，不能再算成等著找失主的物件。", p("Medium shot", "a volunteer moves a bottle and a cap aside while another points to the remaining belongings", "the bottle and cap set on a separate stool"), ["c26"]);
card("count-terminal", "terminal", { title: "工具計數：條件與代號", prompt: ">", command: "python demo.py count", output: ["records=6; returned=2; unclaimed=4", "unclaimed_ids=L001,L003,L004,L006", "unclaimed_umbrellas=2; ids=L001,L003"], ran_on: "2026-10-04", tool_version: "Python 3.14.6" }, ["六筆紀錄裡，兩筆已領，所以符合未領條件的是四筆。", "這四筆的代號列在第二行，你可以回清單逐筆核對。", "再從未領裡只挑雨傘，留下兩把，也留下對應代號。"], ["c8", "c26"]);
shot("demo-two-umbrellas", "同一份清單，全部是六件，未領是四件，未領雨傘是兩把。", p("Close-up", "a volunteer holds the two umbrella handles above the remaining glove and scarf", "two curved wooden handles side by side"), ["c8", "c26"]);
shot("demo-trace", "數字後面留著條件和代號，就有機會發現算錯哪一步。", p("From behind", "a volunteer retraces the objects from one basket to their separate original trays", "one glove being returned to a wooden tray"), ["c29"]);
card("article-cta", "cta", { kicker: "完整示例", title: "圖解與六筆示範資料", sub: "說明欄附文章連結、資料與結果" }, "圖解在說明欄文章；這次用的六筆資料另附示範紀錄。", ["c30"]);
shot("demo-not-benchmark", "這個結果證明程式按條件計數，不證明任何模型從不犯錯。", p("Wide shot", "a volunteer closes a storage crate while the other continues inspecting a single item", "the wooden crate lid held halfway open"), ["c3", "c31"]);
shot("demo-tools-question", "要讓聊天工具也完成這些步驟，中間還缺哪幾個角色？", p("Medium shot", "two volunteers pass a basket across a doorway to a third volunteer", "the woven basket suspended between their hands"), ["c9"]);

place = "an outdoor street market in midafternoon";
lighting = ["leaf-filtered sun falls through a canopy above the stall", "dappled tree shade surrounds the crates", "late-afternoon brightness reflects off the paved aisle"];
card("tools-chapter", "chapter", { title: "聊天產品與工具差在哪", number: "5" }, "模型可以提出工具要求；程式要把要求交給工具執行。", ["c9"], "聊天產品與工具差在哪");
shot("market-courier", "像你請攤主數貨，說出要求並不會讓每個箱子自己盤點。", p("Wide shot", "a shopper gestures to stacked crates while a stallholder reaches for one crate", "a stack of wooden fruit crates"), ["c1", "c9"]);
shot("market-request", "工具要接到要求，處理資料，再把結果送回後續流程。", p("Close-up", "a stallholder hands a small wooden scoop to an assistant", "the scoop passing between their hands"), ["c9"]);
card("tool-three-steps", "steps", { title: "完成前，要找三個證據", steps: [{ title: "要求", detail: "查什麼、算什麼" }, { title: "執行", detail: "工具真的處理了嗎" }, { title: "回傳", detail: "結果、條件與錯誤" }] }, ["先看要求，把全部紀錄和未領紀錄分清楚。", "再看是否執行，缺權限、找不到檔案，都可能停在途中。", "最後看工具回傳，不能只拿模型那句我算好了當證據。"], ["c9", "c29", "c32"]);
shot("market-empty-crate", "若要求查空箱，工具回傳空的，模型就不該自行填滿。", p("Overhead shot", "an assistant tips an empty wooden crate toward a waiting shopper", "the bare bottom of the wooden crate"), ["c23", "c9"]);
shot("market-scoop", "它可以把回傳內容整理成話，但整理時仍可能漏掉條件。", p("Medium shot", "a stallholder separates a small scoop of beans from a larger sack", "beans resting in a wooden scoop"), ["c32", "c2"]);
shot("market-boundary", "因此你看到的聊天產品，通常不只包含那一個文字模型。", p("Wide shot", "a shopper watches a stallholder, an assistant and a courier coordinate at one stall", "a crate passed through the center of the group"), ["c33"]);
card("product-model", "compare", { title: "一個模型與完整產品", left: { heading: "模型", points: ["處理輸入", "產生文字或工具要求"] }, right: { heading: "產品與程式", points: ["準備資料、權限與工具", "執行、保存與呈現"] } }, ["模型處理這輪輸入，產品還負責資料、工具和呈現方式。", "所以同一個模型在不同產品裡，能做的事也可能不同。"], ["c33"]);
shot("market-key", "是否能讀你的檔案，先看產品是否把檔案內容交給它。", p("Close-up", "a stallholder places a plain metal key in an assistant's palm", "a small metal key in an open hand"), ["c20", "c33"]);
shot("market-access", "是否能查庫存，還要看工具有沒有接上，以及能查哪部分。", p("From behind", "a courier stops at a closed storage gate while a stallholder opens a smaller hatch", "a small wooden hatch in a storage gate"), ["c9", "c33"]);
shot("market-saved", "畫面說記住了，不等於模型的參數真的重做了一次訓練。", p("Medium shot", "an assistant stores a sealed pouch on a shelf while another continues serving a shopper", "the sealed fabric pouch on a wooden shelf"), ["c17", "c20"]);
card("memory-rule", "big", { kicker: "產品記憶", text: "保存／再次提供，**與訓練分開**" }, "產品可以保存材料，再提供給後續對話。", ["c20"]);
card("memory-product-rule", "big", { kicker: "實際做法", text: "回到你使用的產品說明" }, "存什麼、何時再提供，要看產品的說明。", ["c20"]);
shot("market-two-roles", "會說話的攤主加上會數貨的助手，各自仍需要被檢查。", p("Wide shot", "a stallholder speaks to a shopper while an assistant sorts two small crates behind them", "two small crates beside the assistant's knees"), ["c1", "c32"]);
shot("market-receipt", "請求、回傳和最後那句話，三者對得上才算完成這次任務。", p("Close-up", "a shopper compares beans in two cupped hands while a stallholder observes", "two small portions of beans held side by side"), ["c29", "c32"]);
shot("market-errors-question", "有資料也有工具，為什麼最後的回答還是可能出錯？", p("Medium shot", "an assistant notices a single glove accidentally tucked into a produce crate", "a fabric glove among wooden crate slats"), ["c2", "c32"]);

place = "an apartment kitchen in late afternoon";
lighting = ["a warm kitchen work lamp lights the ceramic bowls", "an under-cabinet fixture directs light onto the work surface", "a ceiling lamp illuminates the jars without glare"];
card("errors-chapter", "chapter", { title: "流暢回答的三個陷阱", number: "6" }, "第一個陷阱是補不存在的欄位，第二個是換掉題目的條件。", ["c22", "c32"], "流暢回答的三個陷阱");
shot("kitchen-empty-jar", "你以為表格每格都有字，這份報告就比留空的更可靠。", p("Wide shot", "a cook examines a row of jars while another reaches for a visibly empty jar", "an empty glass jar on a kitchen table"), ["c22"]);
shot("kitchen-gap", "其實清單沒寫物品主人，填王先生只會讓錯誤更完整。", p("Close-up", "a cook lowers a spoon into an empty jar and lifts it empty", "the bare metal spoon above the glass jar"), ["c5", "c22"]);
card("invented-name", "chat", { title: "錯誤示意，非模型輸出", messages: [{ side: "left", name: "清單可說", text: "雨傘未領，位置在北側櫃台" }, { side: "right", name: "編輯錯誤稿", text: "王先生已領走北側櫃台的雨傘" }] }, ["這句錯誤稿自己加上失主，還把未領改成已領。", "哪怕語句非常順，兩個新增內容都沒有清單能支持。"], ["c5", "c22"]);
shot("kitchen-counterexample", "第二個陷阱是問未領，回答卻把所有紀錄的數量端給你。", p("Overhead shot", "a cook separates two empty plates from four plates holding fruit", "four occupied plates beside two empty ones"), ["c26", "c32"]);
shot("kitchen-count", "六、四、二都出現在同一份資料裡，但各自回答不同問題。", p("Medium shot", "two cooks sort a bowl of beans into a large and a small portion", "the two portions of beans in separate ceramic bowls"), ["c8", "c26"]);
card("condition-stats", "stats", { title: "三個數字，三個條件", stats: [{ value: "6", label: "全部紀錄" }, { value: "4", label: "未領物件" }, { value: "2", label: "未領雨傘" }], source: "虛構資料／demo.py count，2026-10-04" }, ["問全部紀錄，答案是六；它包含兩筆已領紀錄。", "問未領物件，答案是四；那兩筆已領要排除。", "問未領雨傘，答案是兩；圍巾和手套也要排除。"], ["c8", "c26"]);
shot("kitchen-repeat", "第三個陷阱是重問同一句，把重複出現當成獨立證據。", p("From behind", "a cook pours the same beans from one bowl into another and back again", "one stream of beans moving between two bowls"), ["c34"]);
shot("kitchen-agree", "兩份相同文字，可能只是一起重複了同一個沒有根據的說法。", p("Wide shot", "two cooks each hold an identical empty jar and glance at the same empty shelf", "two empty glass jars in their hands"), ["c34"]);
shot("kitchen-evidence", "真正要補的是來源、資料與執行證據，不只是多一份答案。", p("Close-up", "a cook checks a cracked ceramic bowl by feeling the visible crack", "the crack across the ceramic bowl"), ["c23", "c29", "c34"]);
card("check-lines", "bullets", { title: "查的是哪一種缺口？", items: ["欄位：來源有寫嗎", "條件：是不是同一題", "執行：結果真的回來嗎"] }, ["先找來源有沒有寫，缺欄位就保留無法確認。", "再找條件是不是同一題，把代號和狀態逐筆對上。", "最後找執行結果真的回来沒有，失敗訊息也要保留。"], ["c23", "c29", "c32"]);
shot("kitchen-bias", "找得到一句來源，也還要看它是不是支持你實際說的內容。", p("Medium shot", "a cook compares a matching jar lid with a visibly different jar opening", "a metal lid held above an incompatible glass jar"), ["c35"]);
shot("kitchen-task", "評估模型能力也是同樣道理，要看任務和核對標準。", p("Overhead shot", "two cooks compare a carefully divided serving with the ingredients still in a bowl", "the divided serving on a plain ceramic plate"), ["c24"]);
shot("kitchen-action-question", "知道三種陷阱以後，你能立刻拿哪個方法檢查自己的回答？", p("Close-up", "a cook hands three plain small bowls to another person", "three ceramic bowls stacked loosely in two hands"), ["c23", "c29"]);

place = "a residential garden in early evening before sunset";
lighting = ["slanting sun illuminates the woven baskets", "soft outdoor light reflects from the garden wall", "late rays pass between leaves at the garden gate"];
card("action-chapter", "chapter", { title: "用三欄卡檢查下一份回答", number: "7" }, "把一份回答分三欄，先找生成文字，再找資料和工具結果。", ["c23", "c29"], "用三欄卡檢查下一份回答");
shot("garden-three-baskets", "不用先懂完整的模型架構，也能把這份回答拆成三種工作。", p("Wide shot", "two neighbors place three shallow baskets on a garden bench", "three woven baskets across the center of the bench", "low sunlight enters from the left"), ["c23", "c29"]);
shot("garden-language", "第一欄放生成文字，它把語句組好，不自動成為事實證明。", p("Close-up", "a neighbor folds a plain fabric scarf into the first basket", "the soft fabric scarf pressed between fingers", "low sunlight lights the hands"), ["c2", "c7"]);
card("three-column-card", "table", { title: "你的下一份回答，分三欄", columns: ["工作", "要找的證據"], rows: [["生成文字", "話說得通，不代表查到"], ["資料查找", "哪筆紀錄、哪段來源"], ["工具計數", "條件、執行、回傳"]] }, ["第一欄先認出哪些是在組織文字，不拿流暢度當證據。", "第二欄找資料查找，要能說出哪筆紀錄或哪段來源。", "第三欄找工具計數，條件、執行和回傳要能互相對上。"], ["c2", "c7", "c29"]);
shot("garden-record", "第二欄放可以回查的紀錄，位置和狀態要跟來源一致。", p("Medium shot", "one neighbor matches a glove to an empty space in a small tray", "a fabric glove fitting in the tray", "sunlight falls across the bench"), ["c4", "c29"]);
shot("garden-tool", "第三欄放真的跑過的結果，不只寫一句我已經幫你算好。", p("Overhead shot", "a neighbor separates a small group of pebbles from a larger group", "the two groups of stone pebbles", "even outdoor daylight"), ["c9", "c29"]);
shot("garden-boundary", "哪一欄沒有證據，就先留未知，別用另一欄的內容補洞。", p("Close-up", "a neighbor leaves one basket empty while holding back a spare glove", "the empty woven basket", "warm daylight from the side"), ["c23"]);
card("rewrite-request", "steps", { title: "可照做的三句要求", steps: [{ title: "只依這份資料", detail: "標出紀錄或來源" }, { title: "缺資料請說明", detail: "不補失主與電話" }, { title: "數字列出條件", detail: "附實際結果與代號" }] }, ["你可以要求，只依這份資料回答，請標出支持的紀錄。", "無法確認的欄位寫未知，並說明還缺什麼資料。", "若有計數，請列條件、實際結果和能回查的代號。"], ["c23", "c29"]);
shot("garden-check-it", "這三句不是保證正確的咒語，你還是要真的點開核對。", p("Wide shot", "two neighbors compare the contents of their baskets and move a misplaced scarf", "the scarf being moved across the gap between baskets", "sunlight filters through leaves"), ["c23", "c35"]);
shot("garden-next-context", "需要更多資料時，就補那份資料，不先要求回答更有自信。", p("Medium shot", "a neighbor brings an extra small tray to the bench while another makes room", "the new wooden tray held at waist height", "soft late daylight"), ["c23", "c20"]);
shot("garden-related-token", "token 是處理單位，上下文是材料，參數是訓練調整的數值。", p("Close-up", "a neighbor holds a pebble, a fabric swatch and a pottery piece in separate hands", "three distinct small objects above a woven mat", "outdoor daylight illuminates the objects"), ["c12", "c17", "c18"]);
card("nearby-terms", "compare", { title: "鄰近名詞：各管哪件事", left: { heading: "模型與上下文", points: ["模型：依學到的模式運算", "上下文：這輪可見材料"] }, right: { heading: "檢索與工具", points: ["檢索：找到相關材料", "工具：執行指定處理"] } }, ["模型和上下文分清楚，就比较知道該補資料還是改任務。", "檢索找材料，工具執行處理；它們的結果仍然需要核對。"], ["c17", "c9", "c36"]);
shot("garden-own-acceptance", "你要的不是聽起來像高手，而是這次任務有可確認的成果。", p("From behind", "a neighbor returns the matching glove to a waiting visitor", "the glove crossing between their hands", "low sunlight comes from the garden gate"), ["c24", "c29"]);
shot("garden-follow-up", "下次看到完整答案，先找哪些內容有資料，哪些數字有工具結果。", p("Overhead shot", "two neighbors separate belongings into three baskets without filling the empty basket", "the three baskets with distinct contents", "even light under an open pergola"), ["c23", "c29"]);
shot("garden-closing", "若用了工具，再核對它實際傳回的結果，才把工作交出去。", p("Medium shot", "a volunteer closes an umbrella while a visitor walks away carrying the matching item", "the umbrella's closed wooden handle", "last daylight enters through the courtyard gate"), ["c9", "c29"]);
card("wrap", "outro", { title: "會接話，還要**有據可查**", cta: "用三欄卡檢查下一份回答的依據", lines: ["有來源也會生成文字；用工具再查結果"] }, "話完整不等於查到了；可信回答要有據可查。", ["c2", "c9", "c29"]);

// Actual-image review: preserve the recorded narration and look; correct only
// these two compositions before buying their replacement pictures.
const promptOverrides = {
  "counter-arrival": "Wide shot, community-center foyer, rainy morning. A wet-coated visitor and volunteer stand together by a rack holding one folded umbrella. The volunteer points to it. Both figures, hands and the entire rack fit in the central vertical third. Rain on glass, grey overcast light, soft shadows. All walls, glass and props are blank; no signs, posters, letters, digits, symbols, pseudo-writing, signatures, logos or watermarks.",
  "counter-handoff": "Medium shot, community-center foyer, rainy morning. A volunteer offers one tightly folded, strapped umbrella horizontally at waist height to a visitor's open palm. Both faces, hands and the whole closed umbrella fit in the central vertical third; both people stand close. No open canopy or upright shaft. Rain on glass, grey overcast light, soft shadows. All surfaces blank; no signs, letters, symbols, pseudo-writing, signatures or logos.",
};
for (const scene of scenes) {
  if (promptOverrides[scene.id]) scene.data.prompt = promptOverrides[scene.id];
}

const sources = [
  { title: "Google Machine Learning Crash Course: Introduction to Large Language Models", url: "https://developers.google.com/machine-learning/crash-course/llm", checked_on: "2026-10-04" },
  { title: "Google: What's a large language model? / Transformers and self-attention", url: "https://developers.google.com/machine-learning/crash-course/llm/transformers", checked_on: "2026-10-04" },
  { title: "Hugging Face Transformers: Causal language modeling", url: "https://huggingface.co/docs/transformers/tasks/language_modeling", checked_on: "2026-10-04" },
  { title: "Hugging Face Transformers: Text generation", url: "https://huggingface.co/docs/transformers/llm_tutorial", checked_on: "2026-10-04" },
  { title: "Google: Fine-tuning, distillation, and prompt engineering", url: "https://developers.google.com/machine-learning/crash-course/llm/tuning", checked_on: "2026-10-04" },
  { title: "Google AI for Developers: Function calling", url: "https://ai.google.dev/gemini-api/docs/function-calling", checked_on: "2026-10-04" },
];
const doc = {
  schema_version: 1, slug: "ai-term-large-language-model", format: "slides", category: "ai-terms", source_guide: "what-is-a-large-language-model", target_minutes: [9, 11],
  voice: { provider: "gemini", name: "Sulafat", style: STORY_VOICE_STYLE }, look: { preset: "tech-story" }, subtitles: { burn_in: false },
  youtube: { category_id: 28, made_for_kids: false, default_language: "zh-TW", title: "大型語言模型是什麼？會接話，為什麼不等於查到資料？｜AI 名詞十分鐘",
    description: "大型語言模型（LLM）如何生成文字？為什麼把話說得很完整，還不能當作已查到資料的證明？\n給會用聊天工具、卻常把模型、資料查找與工具執行混在一起的人；不需要懂程式。\n\n用六筆虛構失物紀錄，離線重跑有據、缺資料與工具計數三題。全部六件、未領四件、未領雨傘兩把；數字附條件與代號。故事、聊天泡泡和錯誤回答都是編輯自製示意，不是任何語言模型的實測輸出。Python 標準函式庫程式沒有網路或模型呼叫，只證明資料與計數，不評測模型能力。\n\n六筆示範資料：L001 雨傘／北側櫃台／未領；L002 水瓶／東側層架／已領；L003 雨傘／西側籃子／未領；L004 圍巾／南側掛鉤／未領；L005 帽子／東側層架／已領；L006 手套／西側籃子／未領。沒有失主姓名或電話欄位。\n真實離線輸出：查 L001 得到北側櫃台及未領；問 owner_phone 得到 UNKNOWN；未領代號 L001、L003、L004、L006，未領雨傘代號 L001、L003。\n\n三欄用來核對一份回答的依據與執行紀錄，並非互斥能力；即使拿到資料或工具結果，最後文字仍可能由模型生成。缺證據的部分先留未知。若用了工具，再核對條件與實際結果。\n\n完整文章與圖解：https://mokaair.com/zh-TW/life/what-is-a-large-language-model\nAI 名詞總索引：https://mokaair.com/zh-TW/life/ai-terms-index?utm_source=youtube&utm_medium=video&utm_campaign=ai-term-large-language-model",
    tags: ["大型語言模型", "LLM", "AI 名詞", "Large Language Model", "模型與工具", "上下文", "生成文字", "AI 名詞十分鐘", "Mokaair"], video_id: null },
  thumbnail: { template: "thumb", data: { headline: "LLM", tag: "AI 名詞十分鐘", sub: "會接話，查到了嗎？", shot: "counter-handoff" } },
  sources,
  assets: [{ path: "apps/web/public/guides/what-is-a-large-language-model/diagram-1.svg", source: "Mokaair 自有文章圖解（what-is-a-large-language-model）", license: "© Mokaair" }],
  scenes,
};
const traditional = { "話": "話", "會": "會", "個": "個", "检查": "檢查", "兩": "兩", "沒有": "沒有", "證明": "證明", "這些": "這些", "時": "時", "已經": "已經", "回来": "回來", "比较": "比較", "聽": "聽", "條件": "條件", "補": "補", "還": "還" };
const clean = (value) => {
  if (typeof value === "string") return Object.entries(traditional).reduce((text, [a, b]) => text.replaceAll(a, b), value);
  if (Array.isArray(value)) return value.map(clean);
  if (value && typeof value === "object") return Object.fromEntries(Object.entries(value).map(([key, value]) => [key, clean(value)]));
  return value;
};
Object.assign(doc, clean(doc));
let chapterNumber = 0;
for (const scene of doc.scenes) {
  if (scene.chapter) chapterNumber += 1;
  if (scene.template === "chapter") scene.data.number = String(chapterNumber);
}
setPauseBeats(doc);
// Measured 2026-10-04: keep the existing 700 ms scene gap and every recorded word,
// while these two exact takes fit within eight seconds per picture. Apply after
// register defaults so regenerating this source preserves the measured correction.
for (const scene of doc.scenes) {
  for (const line of scene.lines) {
    if (line.id === "ks7c") line.pause_after_ms = 80;
    if (line.id === "qizd") line.pause_after_ms = 30;
  }
}
writeFileSync(path.join(dir, "video.json"), `${JSON.stringify(doc, null, 2)}\n`, "utf8");
const timeline = estimateTimeline(doc);
const units = scenes.flatMap((s) => s.lines).reduce((n, l) => n + spokenUnits(l.text), 0);
const summary = { status: "draft; independent review and media generation pending", estimated_units: units, estimated_seconds: timeline.total_frames / timeline.fps, scenes: scenes.length, shots: shotIndex, lines: at, chapters: timeline.chapters, video_sha256: createHash("sha256").update(readFileSync(path.join(dir, "video.json"))).digest("hex") };
writeFileSync(path.join(dir, "draft-metrics.json"), `${JSON.stringify(summary, null, 2)}\n`);
console.log(JSON.stringify({ units, minutes: summary.estimated_seconds / 60, scenes: scenes.length, shots: shotIndex, lines: at, chapters: timeline.chapters.map((c) => ({ title: c.title, start: formatClock(c.start_frame / timeline.fps) })) }));
