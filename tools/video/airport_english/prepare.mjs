#!/usr/bin/env node
// Airport lessons -> the existing official video schema. This is free preparation, not QA.
import { createHash } from "node:crypto";
import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { main as videoMain } from "../cli.mjs";
import { cuePieces, LOCALE_RULES } from "../core/captions.mjs";
import { unknownTermsFor } from "../core/lexicon.mjs";
import { isInside, ROOT } from "../core/paths.mjs";
import { eachLine, textHash, validateVideo } from "../core/schema.mjs";
import { lintProject, loadProject } from "../core/state.mjs";
import { estimateTimeline, FPS, spokenUnits } from "../core/timeline.mjs";
import { sourceHashes } from "../core/translations.mjs";
import { billableForRequest, planRequests } from "../tts/requests.mjs";

export const PRODUCTION = path.join(ROOT, "docs/videos/airport-english-60-days/production");
export const LOCALES = ["en", "zh-TW", "zh-CN", "ja", "ko"];
const GUIDE_KEYS = ["hook", "goal", "recap", "comment", "subscribe"];
const json = (file) => JSON.parse(readFileSync(file, "utf8"));
const writeJson = (file, value) => { mkdirSync(path.dirname(file), { recursive: true }); writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`); };
const sha = (value) => createHash("sha256").update(JSON.stringify(value)).digest("hex");
export const stableId = (day, semanticKey) => sha(["airport-english", day, semanticKey]).slice(0, 8);
const allText = (value) => Array.isArray(value) && value.length === 5 && value.every((s) => typeof s === "string" && s.trim());
const numberWord = (number) => {
  const n = Number(number), small = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
  return n < 20 ? small[n] : ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"][Math.floor(n / 10)] + (n % 10 ? ` ${small[n % 10]}` : "");
};
// Day01 speaks its written counter range (30–34) as "thirty to thirty-four". This
// normalization is only a source consistency check, never a replacement for answer review.
const answerWords = (text) => String(text).toLowerCase().replace(/\b(\d{1,2})\s*[–—-]\s*(\d{1,2})\b/g, (_, a, b) => `${numberWord(a)} to ${numberWord(b)}`).replace(/\b\d{1,2}\b/g, numberWord).replace(/[^a-z0-9]+/g, " ").trim();

/** At most three balanced rows. Nonbreaking spaces keep the official fitText routine
 * shrinking an overwide row instead of silently wrapping it to a fourth visible row. */
export function englishCardText(text) {
  const words = text.trim().split(/\s+/);
  const count = Math.min(words.length, text.length > 75 ? 3 : text.length > 40 ? 2 : 1);
  let best = null;
  const visit = (start, rows) => {
    if (rows.length === count - 1) {
      const parts = [...rows, words.slice(start).join(" ")];
      const sizes = parts.map((part) => part.length);
      const cost = Math.max(...sizes) * 1000 + sizes.reduce((sum, size) => sum + size ** 2, 0);
      if (!best || cost < best.cost) best = { parts, cost };
      return;
    }
    for (let end = start + 1; end <= words.length - (count - rows.length - 1); end++) visit(end, [...rows, words.slice(start, end).join(" ")]);
  };
  visit(0, []);
  return best.parts.map((part) => part.replace(/ /g, "\u00a0").replace(/-/g, "\u2011")).join("\n");
}

// These directions explain why the same utterance is heard again; none exists just to fill time.
const COACH = {
  listen: ["Listen to the first conversation. Focus on what the speakers need to confirm.", "先聽第一段對話，留意雙方需要確認什麼。", "先听第一段对话，留意双方需要确认什么。", "最初の会話を聞き、二人が何を確認しているかに注目しましょう。", "첫 번째 대화를 듣고 두 사람이 무엇을 확인하는지 집중해 보세요."],
  repeat: ["Listen again. Connect each answer with the question before it.", "再聽一次，把每個回答和前面的問題連起來。", "再听一遍，把每个回答和前面的问题联系起来。", "もう一度聞き、答えがどの質問に対応するか確認しましょう。", "다시 듣고 각 대답이 앞의 어떤 질문에 답하는지 확인하세요."],
  practice: ["Practice one line at a time. Listen, then repeat. Pause the video if you need more time.", "現在逐段台詞練習。先聽，再開口跟讀。需要更多時間時，請暫停影片。", "现在逐条台词练习。先听，再开口跟读。需要更多时间时，请暂停视频。", "一つのセリフずつ練習します。聞いてから、声に出して繰り返しましょう。時間が足りなければ、動画を一時停止してください。", "한 줄씩 연습합니다. 먼저 듣고 소리 내어 따라 해 보세요. 시간이 더 필요하면 영상을 일시 정지하세요."],
  variation: ["Now try a different situation. Do not assume the answer is the same. Listen for what has changed.", "換一個情境，不要假設答案相同。請聽出改變了哪些資訊。", "换一个情境，不要假设答案相同。请听出哪些信息发生了变化。", "次は別の場面です。同じ答えだと思い込まず、何が変わったか聞き取りましょう。", "이번에는 다른 상황입니다. 답이 같다고 생각하지 말고 무엇이 바뀌었는지 들어 보세요."],
  contrast: ["Compare the changed details with the first exchange. Repeat aloud; pause the video if you need more time.", "和第一段對話比較改變的細節，再開口跟讀。需要更多時間時，請暫停影片。", "和第一段对话比较改变的细节，再开口跟读。需要更多时间时，请暂停视频。", "最初の会話と比べ、変わった情報を意識して声に出して繰り返しましょう。時間が足りなければ、動画を一時停止してください。", "첫 번째 대화와 달라진 정보를 비교하고 소리 내어 따라 해 보세요. 시간이 더 필요하면 영상을 일시 정지하세요."],
  quiz: ["Here are three listening questions. Hear the relevant exchange, then choose an answer before the explanation.", "接下來有三題聽力測驗。聽相關對話，在解答前選出答案。", "接下来有三道听力题。听相关对话，在解答前选出答案。", "リスニング問題は三つです。関連する会話を聞き、解説の前に答えを選びましょう。", "듣기 문제는 세 개입니다. 관련 대화를 듣고 해설 전에 답을 고르세요."],
  choose: ["Choose your answer now.", "現在選出你的答案。", "现在选出你的答案。", "ここで答えを選びましょう。", "이제 답을 고르세요."],
  review: ["Now listen to both conversations at a natural pace. For a challenge, switch off translated captions and focus on the voices.", "最後用自然語速重聽兩段對話。想挑戰自己，可以關掉翻譯字幕，專心聽聲音。", "最后用自然语速重听两段对话。想挑战自己，可以关闭翻译字幕，专心听声音。", "最後に自然な速さで二つの会話を聞きましょう。挑戦したい人は翻訳字幕をオフにして、音声に集中してください。", "마지막으로 두 대화를 자연스러운 속도로 다시 듣습니다. 도전하고 싶다면 번역 자막을 끄고 음성에 집중하세요."],
};
const CHAPTERS = {
  hook: ["Today's airport challenge", "今天的機場情境", "今天的机场情境", "今日の空港の場面", "오늘의 공항 상황"],
  first: ["Hear the first exchange", "聽懂第一段對話", "听懂第一段对话", "最初の会話を聞く", "첫 대화 듣기"],
  practice: ["Practice line by line", "逐段台詞練習", "逐条台词练习", "セリフを一つずつ練習", "한 줄씩 연습하기"],
  variation: ["Notice what changes", "聽出情境變化", "听出情境变化", "変わった情報を聞く", "바뀐 정보 듣기"],
  compare: ["Practice the changed details", "練習不同的細節", "练习不同的细节", "変わった情報を練習", "달라진 정보 연습"],
  quiz: ["Check three listening answers", "三題聽力驗收", "三道听力验收题", "三つの問題で確認", "세 문제로 확인"],
  review: ["Listen with less support", "減少提示再聽一次", "减少提示再听一遍", "ヒントを減らして聞く", "힌트를 줄여 다시 듣기"],
};

export function lessonProblems(lesson) {
  const errors = [];
  if (!Number.isInteger(lesson?.day) || lesson.day < 1 || lesson.day > 60) errors.push("day must be 1 through 60");
  if (!allText(lesson?.title_all)) errors.push("title_all must contain five complete translations");
  for (const name of GUIDE_KEYS) if (!allText(lesson?.guides?.[name])) errors.push(`guides.${name} must contain five complete translations`);
  const ids = new Set();
  for (const group of ["A", "B"]) {
    if (!Array.isArray(lesson?.[group]) || !lesson[group].length) { errors.push(`${group} needs dialogue turns`); continue; }
    for (const turn of lesson[group]) {
      if (!new RegExp(`^${group}[0-9]{2}$`).test(turn.id) || ids.has(turn.id)) errors.push(`invalid or duplicate dialogue id ${turn.id}`);
      ids.add(turn.id);
      if (!["T", "S"].includes(turn.speaker)) errors.push(`${turn.id} speaker must be the reviewed T or S role`);
      if (!allText(turn.all) || turn.all[0] !== turn.text) errors.push(`${turn.id} has incomplete translations or an English mismatch`);
      if (Object.hasOwn(turn, "practice_pause_ms") && (!Number.isInteger(turn.practice_pause_ms) || turn.practice_pause_ms < 4000 || turn.practice_pause_ms > 5000)) errors.push(`${turn.id} practice_pause_ms must be an integer from 4000 through 5000`);
    }
  }
  if (!Array.isArray(lesson?.quiz) || lesson.quiz.length !== 3) errors.push("exactly three quiz questions are required");
  for (const [index, quiz] of (lesson?.quiz ?? []).entries()) {
    if (!allText(quiz.all) || quiz.all[0] !== quiz.question || !allText(quiz.answer_all)) errors.push(`quiz ${index + 1}: question/answer translation mismatch`);
    if (!Array.isArray(quiz.choices) || quiz.choices.length !== 3 || !Array.isArray(quiz.choices_all) || quiz.choices_all.length !== 3 || quiz.choices_all.some((a, i) => !allText(a) || a[0] !== quiz.choices[i])) errors.push(`quiz ${index + 1}: three translated choices required`);
    if (!Number.isInteger(quiz.correct) || quiz.correct < 0 || quiz.correct > 2) errors.push(`quiz ${index + 1}: invalid answer index`);
    else if (quiz.answer !== quiz.choices?.[quiz.correct]) errors.push(`quiz ${index + 1}: answer differs from the selected choice`);
    if (allText(quiz.answer_all)) {
      const spoken = /^The (?:correct )?answer is ([ABC])[.:]\s*(.+)$/s.exec(quiz.answer_all[0]);
      const expected = answerWords(quiz.choices?.[quiz.correct] ?? "");
      if (!spoken || spoken[1] !== String.fromCharCode(65 + quiz.correct) || !expected || !` ${answerWords(spoken[2])} `.includes(` ${expected} `)) errors.push(`quiz ${index + 1}: spoken English answer must identify the correct letter and choice`);
    }
    if (!Array.isArray(quiz.evidence_ids) || !quiz.evidence_ids.length || new Set(quiz.evidence_ids).size !== quiz.evidence_ids.length || quiz.evidence_ids.some((id) => !ids.has(id))) errors.push(`quiz ${index + 1}: explicit, unique, existing evidence_ids required`);
  }
  return errors;
}

export function prepareLesson(lesson, profile) {
  const problems = lessonProblems(lesson);
  if (problems.length) throw new Error(`Day ${lesson?.day}: ${problems.join("; ")}`);
  const day = String(lesson.day).padStart(2, "0");
  const slug = `airport-english-day${day}`;
  const scenes = [], entries = [], originals = new Map(), chapterTranslations = {};
  const add = (key, all, { kind = "coach", turn = null, chapter = null, pause = 300, label = "Listen and practice" } = {}) => {
    const id = stableId(lesson.day, key), sceneId = `s-${id}`;
    const line = { id, text: all[0], pause_after_ms: pause };
    if (turn) {
      if (originals.has(turn.id)) line.audio_ref = originals.get(turn.id);
      else originals.set(turn.id, id);
    }
    const source = turn ? (turn.speaker === "T" ? "Traveler" : "Staff") : "Airport English";
    // The reviewed claim list applies to this lesson. Conservatively bind its non-fiction
    // claims to the dialogue scenes so a later NOT FOUND verdict cannot disappear from QA.
    const claims = turn ? (lesson.claims ?? []).filter((claim) => claim.status !== "fictional_scenario_not_external_fact").map((claim) => claim.id) : [];
    const scene = { id: sceneId, ...(chapter ? { chapter: CHAPTERS[chapter][0] } : {}), ...(claims.length ? { claims } : {}), template: "quote", data: { kicker: label, quote: englishCardText(all[0]), source }, lines: [line] };
    if (chapter) chapterTranslations[sceneId] = CHAPTERS[chapter];
    scenes.push(scene);
    entries.push({ id, semantic_key: key, kind, source_turn_id: turn?.id ?? null, source_take_id: line.audio_ref ?? id, all });
    return id;
  };
  const guide = (name, options) => add(`guide-${name}`, lesson.guides[name], options);
  const coach = (name, key, options) => add(`coach-${key ?? name}`, COACH[name], options);
  const turns = (group, pass, options) => {
    for (const turn of lesson[group]) add(`${pass}-${turn.id}`, turn.all, { ...options, ...(pass === "practice" ? { pause: turn.practice_pause_ms ?? 4000 } : {}), kind: "dialogue", turn });
  };
  guide("hook", { chapter: "hook", label: "Today's challenge" });
  guide("goal", { label: "What to listen for" });
  coach("listen", null, { chapter: "first", label: "Listen for meaning" });
  turns("A", "first", { label: "Conversation A" });
  coach("repeat", "repeat-a", { label: "Connect questions and answers" });
  turns("A", "connect", { label: "Conversation A · connect the answers" });
  coach("practice", null, { chapter: "practice", label: "Listen, then speak" });
  turns("A", "practice", { label: "Conversation A · your turn", pause: 4000 });
  coach("variation", null, { chapter: "variation", label: "Listen for changed details" });
  turns("B", "first", { label: "Conversation B" });
  coach("repeat", "repeat-b", { label: "Confirm the changed information" });
  turns("B", "connect", { label: "Conversation B · connect the answers" });
  coach("contrast", null, { chapter: "compare", label: "Compare and speak" });
  turns("B", "practice", { label: "Conversation B · your turn", pause: 4000 });
  coach("quiz", null, { chapter: "quiz", label: "Three listening questions" });
  const byId = new Map([...lesson.A, ...lesson.B].map((turn) => [turn.id, turn]));
  for (const [index, quiz] of lesson.quiz.entries()) {
    add(`quiz-${index + 1}-question`, quiz.all, { kind: "question", label: `Question ${index + 1}` });
    quiz.choices_all.forEach((all, choice) => add(`quiz-${index + 1}-choice-${choice}`, all.map((text) => `${String.fromCharCode(65 + choice)}. ${text}`), { kind: "choice", label: `Question ${index + 1} · ${String.fromCharCode(65 + choice)}` }));
    for (const evidenceId of quiz.evidence_ids) {
      const turn = byId.get(evidenceId);
      add(`quiz-${index + 1}-evidence-${turn.id}`, turn.all, { kind: "dialogue", turn, label: `Question ${index + 1} · listen for the answer` });
    }
    coach("choose", `choose-${index + 1}`, { label: `Question ${index + 1} · choose`, pause: 4000 });
    add(`quiz-${index + 1}-answer`, quiz.answer_all, { kind: "answer", label: `Answer ${index + 1}`, pause: 1000 });
  }
  coach("review", null, { chapter: "review", label: "Listen with less support" });
  turns("A", "review", { label: "Conversation A · final listening" });
  turns("B", "review", { label: "Conversation B · final listening" });
  for (const name of ["recap", "comment", "subscribe"]) guide(name, { label: name === "recap" ? "Today's answer" : name === "comment" ? "Your experience" : "Keep practicing" });
  const exampleQuiz = lesson.quiz[0];
  const chooseLine = scenes.find((scene) => scene.lines[0].id === stableId(lesson.day, "coach-choose-1")).lines[0];
  const workedExample = [
    "### 可跟著作答的實例：本集第 1 題",
    "",
    "以下直接取自本集既有、已覆核的虛構對話與測驗；兩個大綱選項都保留這個練習。",
    "實際播放順序：問題 → 三個選項 → 重播指定對話 → 提示作答並停頓 → 公布答案。觀眾先聽辨，再自行選答案，最後對照原稿解答。",
    "",
    `1. 先聽問題：${exampleQuiz.question}`,
    "2. 依序聽三個選項：",
    ...exampleQuiz.choices.map((choice, index) => `   - ${String.fromCharCode(65 + index)}. ${choice}`),
    `3. 重播支持答案的原對話（evidence_ids：${exampleQuiz.evidence_ids.join(", ")}）：`,
    ...exampleQuiz.evidence_ids.map((id) => {
      const turn = byId.get(id);
      return `   - ${id} / ${turn.speaker === "T" ? "Traveler" : "Staff"}: ${turn.text}`;
    }),
    `4. 提示作答：${chooseLine.text} 語句後停頓 ${chooseLine.pause_after_ms / 1000} 秒，讓觀眾選答案；需要更多時間可暫停影片。`,
    `5. 公布正解：${String.fromCharCode(65 + exampleQuiz.correct)}. ${exampleQuiz.answer}`,
    `   既有答案口播（逐字）：${exampleQuiz.answer_all[0]}`,
    "",
    "這個例子示範如何把聽到的資訊對回選項；完整影片再用其餘兩題檢查當集理解。",
  ].join("\n");
  const description = (localeIndex) => [lesson.guides.hook[localeIndex], lesson.guides.goal[localeIndex], ["Fictional airport conversations for listening practice. Numbers, airline names and locations are examples, not current travel instructions. Confirm actual arrangements with your airport and airline.", "本集使用虛構機場對話練習聽力；數字、航空公司與地點為教學示例，實際安排請向機場及航空公司確認。", "本集使用虚构机场对话练习听力；数字、航空公司与地点为教学示例，实际安排请向机场及航空公司确认。", "空港を舞台にした架空の会話で練習します。数字、航空会社名、場所は例です。実際の案内は空港と航空会社にご確認ください。", "가상의 공항 대화로 듣기를 연습합니다. 숫자, 항공사 이름과 장소는 예시입니다. 실제 안내는 공항과 항공사에 확인하세요."][localeIndex]].join("\n\n");
  const seriesTitles = ["Airport English", "機場英文", "机场英语", "空港英語", "공항 영어"];
  const titles = lesson.title_all.map((title, index) => `${title}${index === 0 ? " | " : "｜"}${seriesTitles[index]} Day ${day}`);
  const doc = { schema_version: 1, slug, format: "slides", category: "travel", narration_locale: "en", target_minutes: [10, 10], voice: { ...profile.voice }, youtube: { category_id: 27, made_for_kids: false, default_language: "en", title: titles[0], description: description(0), tags: ["airport English", "English listening", "travel English"], video_id: null }, thumbnail: { template: "thumb", data: { headline: lesson.thumbnail_headline ?? "Hear\n**Clearly**", tag: "Airport English", layout: "a" } }, sources: lesson.sources ?? [], scenes };
  const schemaProblems = validateVideo(doc);
  if (schemaProblems.length) throw new Error(JSON.stringify(schemaProblems));
  const translations = Object.fromEntries(LOCALES.slice(1).map((locale, offset) => {
    const i = offset + 1;
    return [locale, { schema_version: 1, locale, title: titles[i], description: description(i), tags: [["airport English", "English listening", "travel English"], ["機場英文", "英文聽力", "旅遊英文"], ["机场英语", "英语听力", "旅行英语"], ["空港英語", "英語リスニング", "旅行英語"], ["공항 영어", "영어 듣기", "여행 영어"]][i], chapters: Object.fromEntries(Object.entries(chapterTranslations).map(([id, all]) => [id, all[i]])), source_hashes: sourceHashes(doc), lines: Object.fromEntries(entries.map((entry) => [entry.id, { text: entry.all[i], source_hash: textHash(entry.all[0]) }])) }];
  }));
  const teachingAudio = { schema_version: 1, status: "requires_official_mixed_language_audio_adapter", source_locale: "en", source_script_sha256: sha(doc), generic_dub_allowed: false, locales: Object.fromEntries(LOCALES.slice(1).map((locale, offset) => [locale, { lines: entries.map((entry) => ({ id: entry.id, kind: entry.kind, text: entry.kind === "dialogue" ? entry.all[0] : entry.all[offset + 1], speech_locale: entry.kind === "dialogue" ? "en" : locale, ...(entry.kind === "dialogue" ? { reuse_source_take: entry.source_take_id } : {}), cc_text: entry.all[offset + 1] })) }])) };
  const brief = `# Day ${day}：${lesson.title_all[1]}\n\n狀態：修訂後的製作來源；正式關卡尚未核准。\n\n## 一句話問題\n\n${lesson.guides.hook[0]}\n\n## 目標觀眾\n\n準備自行搭機、需要辨識機場資訊的成人英語初學者。\n\n## 觀眾看完能做到的事\n\n${lesson.guides.goal[1]}\n\n## 站主觀點\n\n依使用者指定：每天十分鐘的實用情境聽力；英文常駐、英文預設語音，四語 CC 與教學語音可獨立選擇，角色對話維持英文。不代替即時旅運資訊。\n\n## 格式與長度\n\n官方投影片版型、1080p30、Sulafat。成片總長 600 秒，含實測品牌素材；目前只有文字估計，旁白合成後才確認時長。刻意重聽用於理解、問答連結、跟讀和減少提示，作答停頓用於練習。\n\n## 實際示範或實算\n\n兩段原創對話，三題明確指定 evidence_ids 的聽力題；每題重播必須包含支持答案的對話。\n\n${workedExample}\n\n## 章節大綱\n\n### 選項 A：逐段聽懂、跟讀，再比較（推薦）\n\n一行說明：先建立一段完整語境，再辨識變化；每段對話聽懂後立即跟讀。\n開場鉤子：${lesson.guides.hook[0]}\n章節順序：當集問題 → A 聽懂 → A 跟讀 → B 比較 → B 跟讀 → 三題驗收 → 減少提示重聽 → 回收與下一步。\n目前產生的劇本採此順序；推薦理由是先建立一段完整語境，再辨識變化。\n\n### 選項 B：先比較兩段對話，再集中練習\n\n一行說明：先完成兩段對話辨識，再集中跟讀與作答；仍保留相同問題與例句。\n開場鉤子：${lesson.guides.hook[0]}\n章節順序：當集問題 → A 聽懂 → B 比較 → A、B 集中跟讀 → 三題驗收 → 減少提示重聽 → 回收與下一步。\n此為替代順序；若選 B，須先調整劇本與對應字幕、音軌計畫，再依更新版本完成檢查。\n\n以上為製作提案，未代替正式大綱關卡。\n\n## 結尾\n\n${lesson.guides.recap[0]}\n${lesson.guides.comment[0]}\n${lesson.guides.subscribe[0]}\n`;
  const claims = `# Day ${day} claims\n\n狀態：來源清單，不是獨立查核通過證明。verify-1.md 必須由另一位審稿者依此版本完成。\n\n## 教學情境\n\n兩段對話是虛構例句；航班、櫃檯、航廈、時間、費用和人名不當作現行班表或通用政策。\n\n## 旅運事實\n\n${(lesson.claims ?? []).map((claim) => `- ${claim.id}: ${claim.text}\n  - 狀態：${claim.status}; 來源：${claim.source_urls.join("、")}`).join("\n") || (Array.isArray(lesson.claims) ? "此集未列通用旅運政策；對話屬虛構教學情境。獨立審稿仍須確認沒有未列入的事實主張。" : "尚待逐集分類：若僅有虛構教學情境，應由獨立審稿確認；若有通用旅運政策，須補官方來源。")}\n\n## 測驗證據\n\n${lesson.quiz.map((q, i) => `- Q${i + 1}: ${q.question}\n  - 正解：${q.choices[q.correct]}\n  - 重播：${q.evidence_ids.join(", ")}\n${q.evidence_ids.map((id) => `  - ${id}: ${byId.get(id).text}`).join("\n")}`).join("\n")}\n`;
  const reviewedClaims = claims + (lesson.editorial_review ? `\n## 已有內容覆核\n\n[獨立內容覆核](../${lesson.editorial_review})。此文件覆核教學來源，不是成片、聲音或發布核准。生成後的逐集 verify-1.md 仍須確認來源版本一致。\n` : "");
  const captionPlan = { schema_version: 1, status: "text_segmentation_only_not_timed_captions", rules: LOCALE_RULES, lines: entries.map((entry) => ({ id: entry.id, by_locale: Object.fromEntries(LOCALES.map((locale, i) => [locale, cuePieces(entry.all[i], locale)])) })) };
  const timeline = estimateTimeline(doc);
  const responseIds = new Set(entries.filter((entry) => entry.semantic_key.startsWith("practice-") || entry.semantic_key.startsWith("coach-choose-")).map((entry) => entry.id));
  const responsePauseSeconds = [...eachLine(doc)].filter(({ line }) => responseIds.has(line.id)).reduce((sum, { line }) => sum + line.pause_after_ms, 0) / 1000;
  const duration = { basis: "text_estimate_only", estimated_body_seconds: timeline.total_frames / FPS, target_total_seconds: 600, measured_body_seconds: null, branding_seconds: null, measured_total_seconds: null, fixed_practice_pause_seconds: responsePauseSeconds, release_ready: false };
  const metadata = { schema_version: 1, title_options: [titles[0], `${lesson.title_all[0]}: listen, respond and check`, `${lesson.title_all[0]} | Daily travel listening`], pinned_comment: lesson.guides.comment[0], localized_pinned_comments: Object.fromEntries(LOCALES.map((locale, i) => [locale, lesson.guides.comment[i]])), decisions: { made_for_kids_proposal: false, paid_promotion: null, synthetic_content_disclosure: null, schedule: null }, uploaded_to_youtube: false };
  return { doc, translations, teachingAudio, brief, claims: reviewedClaims, captionPlan, duration, metadata, entries };
}

export function localLexicon(docs, inherited = { schema_version: 1, terms: {} }) {
  const lexicon = structuredClone(inherited);
  // English letter abbreviations get an explicit spelling. Never mark unlistened takes approved.
  for (const doc of docs) for (const { line } of eachLine(doc)) for (const term of unknownTermsFor(line.text, lexicon, "en")) lexicon.terms[term] = [...term].join(" ");
  return lexicon;
}

export function prepareSeries({ lessonsDir = path.join(PRODUCTION, "lessons"), out = PRODUCTION, profile = json(path.join(PRODUCTION, "profile.json")), days = null } = {}) {
  const files = readdirSync(lessonsDir).filter((name) => /^day\d{2}\.json$/.test(name)).sort().filter((name) => !days || days.includes(Number(name.slice(3, 5))));
  const prepared = files.map((name) => { const lesson = json(path.join(lessonsDir, name)); return { lesson, result: prepareLesson(lesson, profile) }; });
  const inherited = json(path.join(ROOT, "docs/videos/lexicon.json"));
  const selected = new Set(prepared.map(({ lesson }) => `day${String(lesson.day).padStart(2, "0")}`));
  const otherDocs = existsSync(out) ? readdirSync(out).filter((name) => /^day\d{2}$/.test(name) && !selected.has(name) && existsSync(path.join(out, name, "video.json"))).map((name) => json(path.join(out, name, "video.json"))) : [];
  const lexicon = localLexicon([...otherDocs, ...prepared.map(({ result }) => result.doc)], inherited);
  writeJson(path.join(out, "lexicon.json"), lexicon);
  for (const { lesson, result } of prepared) {
    const dir = path.join(out, `day${String(lesson.day).padStart(2, "0")}`);
    for (const [name, value] of Object.entries({ "video.json": result.doc, "teaching-audio.json": result.teachingAudio, "caption-plan.json": result.captionPlan, "duration-plan.json": result.duration, "metadata-plan.json": result.metadata, "line-map.json": { schema_version: 1, lesson_sha256: sha(lesson), lines: result.entries.map(({ all, ...entry }) => entry) } })) writeJson(path.join(dir, name), value);
    writeFileSync(path.join(dir, "brief.md"), result.brief);
    writeFileSync(path.join(dir, "claims.md"), result.claims);
    for (const [locale, translation] of Object.entries(result.translations)) writeJson(path.join(dir, "i18n", `${locale}.json`), translation);
  }
  const episodes = prepared.map(({ lesson, result }) => {
    const project = loadProject({ file: path.join(out, `day${String(lesson.day).padStart(2, "0")}`, "video.json"), root: ROOT });
    const lint = lintProject(project);
    const requests = planRequests(result.doc, project.lexicon);
    return { day: lesson.day, slug: result.doc.slug, lines: result.entries.length, dialogue_replays: requests.filter((r) => r.audio_ref).length, unique_source_characters: requests.filter((r) => !r.audio_ref).reduce((sum, r) => sum + billableForRequest(r.body), 0), teaching_characters_by_locale: Object.fromEntries(Object.entries(result.teachingAudio.locales).map(([locale, track]) => [locale, track.lines.filter((line) => line.kind !== "dialogue").reduce((sum, line) => sum + [...line.text].length, 0)])), spoken_words_approximate: Math.round([...eachLine(result.doc)].reduce((sum, { line }) => sum + spokenUnits(line.text), 0) / 2), ...result.duration, lint: { errors: lint.errors, warnings: lint.warnings }, sources_present: result.doc.sources.length > 0, claim_statuses: [...new Set((lesson.claims ?? []).map((claim) => claim.status))], independent_verification_present: existsSync(path.join(project.dir, "verify-1.md")) };
  });
  const report = { schema_version: 1, phase: "source_preparation", official_lint_used: true, minimum_duration_override: false, media_created: false, approvals_created: false, release_ready: false, episode_count: episodes.length, episodes };
  writeJson(path.join(out, "prepare-report.json"), report);
  return report;
}

export function stageProject({ production = PRODUCTION, projectRoot, mediaRoot, days = null }) {
  if (!projectRoot || !mediaRoot || isInside(projectRoot, ROOT) || isInside(mediaRoot, ROOT) || isInside(mediaRoot, projectRoot) || isInside(projectRoot, mediaRoot)) throw new Error("Staged project and media must be separate directories outside the repository");
  const profile = json(path.join(production, "profile.json"));
  const shelf = path.join(projectRoot, "docs/videos");
  mkdirSync(shelf, { recursive: true });
  cpSync(path.join(production, "lexicon.json"), path.join(shelf, "lexicon.json"));
  cpSync(path.join(production, "profile.json"), path.join(shelf, "profile.json"));
  // Keep the linked independent evidence and source lessons beside the staged episodes.
  // Their relative links in claims/verify documents then resolve to the same snapshot.
  for (const name of ["reviews", "lessons"]) {
    const target = path.join(shelf, name);
    rmSync(target, { recursive: true, force: true });
    if (existsSync(path.join(production, name))) cpSync(path.join(production, name), target, { recursive: true });
  }
  const episodes = [];
  for (const name of readdirSync(production).filter((name) => /^day\d{2}$/.test(name) && (!days || days.includes(Number(name.slice(3))))).sort()) {
    const source = path.join(production, name), doc = json(path.join(source, "video.json"));
    if (doc.slug !== `airport-english-${name}`) throw new Error(`${name} contains an unexpected slug; refusing to replace its staged directory`);
    const target = path.join(shelf, doc.slug);
    // Copies bind all downstream review hashes to the exact source snapshot used for synthesis.
    // Remove obsolete reviews/translations: an overlay could keep a deleted verify-9.md and
    // let the official last-round check select a report that is not in the current source.
    rmSync(target, { recursive: true, force: true });
    cpSync(source, target, { recursive: true });
    writeJson(path.join(mediaRoot, doc.slug, "languages.json"), { locales: profile.languages, decided_at: new Date().toISOString(), decision_source: "explicit user request in this task; timestamp records this selection snapshot, not a production approval" });
    episodes.push(doc.slug);
  }
  return episodes;
}

export async function runStage({ command, args = [], projectRoot, mediaRoot, day, production = PRODUCTION }) {
  if (["dub", "approve", "youtube-sync", "auto", "import"].includes(command)) throw new Error(`${command} is not allowed by the airport adapter: preserve English takes, actual approvals and the user's publishing boundary`);
  const allowed = ["lint", "status", "tts", "check-audio", "review-push", "review-pull", "render", "assemble", "captions", "qa", "package", "branding"];
  if (!allowed.includes(command)) throw new Error(`Unsupported production stage ${command}`);
  if (!projectRoot || !mediaRoot || isInside(projectRoot, ROOT) || isInside(mediaRoot, ROOT) || isInside(mediaRoot, projectRoot) || isInside(projectRoot, mediaRoot)) throw new Error("Staged project and media must be separate directories outside the repository");
  const slug = `airport-english-day${String(day).padStart(2, "0")}`;
  // Staging is explicit. Replacing a source after an approval requires another staged snapshot
  // and the official hash checks, rather than silently changing it before every stage.
  if (!existsSync(path.join(projectRoot, "docs/videos", slug, "video.json"))) throw new Error("Run stage-project first; no staged source exists");
  if (command === "tts") {
    const bindingFile = path.join(production, `day${String(day).padStart(2, "0")}`, "review-binding.json");
    if (!args.includes("--dry-run") || existsSync(bindingFile)) {
      // The binding module imports this preparation module. Load it only when a stage is
      // requested, so there is no top-level circular dependency or invented review result.
      const { assertReviewBindingCurrent } = await import("./review-bindings.mjs");
      const binding = assertReviewBindingCurrent({ production, day });
      assertStagedReviewBinding({ production, day, projectRoot, binding });
    }
  }
  const selected = command === "branding" ? [] : ["--slug", slug];
  const work = command === "lint" ? [] : ["--workdir", mediaRoot];
  return videoMain([command, ...selected, ...work, ...args], { root: projectRoot });
}

export function assertStagedReviewBinding({ production, day, projectRoot, binding }) {
  const name = `day${String(day).padStart(2, "0")}`, source = path.join(production, name), staged = path.join(projectRoot, "docs/videos", `airport-english-${name}`);
  const digest = (file) => existsSync(file) ? createHash("sha256").update(readFileSync(file)).digest("hex") : null;
  const compare = (file, expected) => {
    if (!expected || digest(path.join(staged, file)) !== expected) throw new Error(`${name}: staged ${file} is missing or differs from the current reviewed source; stage-project again`);
  };
  for (const file of ["review-binding.json", "verify-1.md"]) compare(file, digest(path.join(source, file)));
  for (const [file, expected] of Object.entries(binding.generated_artifacts)) compare(file, expected);
  compare(`../lessons/${name}.json`, binding.lesson_sha256);
  compare("../profile.json", binding.profile_sha256);
  compare("../lexicon.json", binding.lexicon_sha256);
  for (const review of binding.reviews) compare(review.path, review.sha256);
}

export async function main(argv) {
  const [command = "prepare", ...args] = argv;
  const values = parseArgs({ args, options: { lessons: { type: "string" }, out: { type: "string" }, days: { type: "string" }, "project-root": { type: "string" }, "media-root": { type: "string" }, stage: { type: "string" }, "dry-run": { type: "boolean" }, gate: { type: "string" }, json: { type: "boolean" } }, strict: true }).values;
  const days = values.days?.split(",").map(Number) ?? null;
  if (days?.some((day) => !Number.isInteger(day) || day < 1 || day > 60)) throw new Error("--days expects comma-separated days 1 through 60");
  const out = path.resolve(values.out ?? PRODUCTION);
  if (command === "prepare") {
    const report = prepareSeries({ lessonsDir: values.lessons ? path.resolve(values.lessons) : undefined, out, days });
    console.log(JSON.stringify({ episodes: report.episode_count, lint_errors: report.episodes.reduce((sum, e) => sum + e.lint.errors.length, 0), media_created: false, release_ready: false }));
    return report.episodes.some((e) => e.lint.errors.length) ? 1 : 0;
  }
  if (command === "stage-project") { console.log(JSON.stringify(stageProject({ production: out, projectRoot: values["project-root"], mediaRoot: values["media-root"], days }))); return 0; }
  if (command === "run") {
    if (days?.length !== 1 || !values.stage) throw new Error("run requires one --days value and --stage");
    return runStage({ command: values.stage, day: days[0], projectRoot: values["project-root"], mediaRoot: values["media-root"], production: out, args: [...(values["dry-run"] ? ["--dry-run"] : []), ...(values.gate ? ["--gate", values.gate] : []), ...(values.json ? ["--json"] : [])] });
  }
  throw new Error(`Unknown command ${command}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) main(process.argv.slice(2)).then((code) => { process.exitCode = code; }).catch((error) => { console.error(error.message); process.exitCode = 1; });
