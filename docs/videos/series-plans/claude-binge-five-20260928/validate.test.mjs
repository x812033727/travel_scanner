// Regression tests for build.mjs and validate.mjs: a synthetic work that obeys every rule
// passes, and each rule this batch adds on top of the pipeline's own is actually enforced.
//   node --test docs/videos/series-plans/claude-binge-five-20260928/validate.test.mjs
import assert from "node:assert/strict";
import { test } from "node:test";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

import { SLUGS, compile, loadSource } from "./build.mjs";
import { validateSource, validateFiles } from "./validate.mjs";

const CLIFF_CYCLE = ["danger", "emotion", "choice"];
const HOOK_CYCLE = ["question", "danger", "image", "line", "reversal"];
const ARC_CYCLE = ["wins", "mixed", "suffers"];
const CAST = [
  ["hero", "林測試", "lead"],
  ["foe", "邵反派", "antagonist"],
  ["ally", "周盟友", "support"],
  ["kid", "陳小孩", "support"],
  ["elder", "鄧長者", "support"],
  ["host", "蘇主播", "support"],
];
const PLACES = ["home", "gate", "tower"];

/** A work that satisfies every rule: eight mysteries paid on a schedule that leaves no four
 * episodes without a payoff, cliffhanger types that never repeat, chapters closing on a reveal
 * or a reversal, and the world flip on episode 20. */
export function syntheticSource() {
  const mysteries = [];
  for (let i = 1; i <= 8; i++) {
    const advanced = [i + 8, i + 16, i + 24];
    if (i === 1) advanced.unshift(4);
    if (i === 2) advanced.unshift(8);
    mysteries.push({ id: `m0${i}`, question: `問題 ${i}？`, answer: `答案 ${i}`, planted: i, advanced, revealed: 32 + i, reserved: false });
  }
  const episodes = [];
  for (let n = 1; n <= 40; n++) {
    const chapterEnd = n % 10 === 0;
    const type = chapterEnd ? (n % 20 === 0 ? "reversal" : "reveal") : CLIFF_CYCLE[(n - 1) % 3];
    const setups = mysteries.filter((m) => m.planted === n).map((m) => m.id);
    const payoffs = mysteries.filter((m) => m.revealed === n || m.advanced.includes(n)).map((m) => m.id);
    episodes.push({
      number: n,
      title: `第${n}集的標題`,
      logline: `第 ${n} 集回答一個問題並丟出更大的問題。`,
      timeline: "present",
      hook: `第${n}集的鉤子是一句短話`,
      hook_type: HOOK_CYCLE[n % 5],
      conflict: "她必須在門開之前把老人帶出地下室，杜的人堵住了唯一的樓梯。",
      turn: "她發現存檔點不是自己設的，讀檔的代價落在她最在意的記憶上。",
      cliffhanger: { type, text: "門開了，怪物的影子落在阿嬤的床上。" },
      satisfaction: [
        { beat: "opening", type: "face_slap", text: "嘲笑她沒有職業的人被首殺公告打臉" },
        { beat: "second_half", type: "rescue", text: "她在氧氣機停下的最後一秒接回電源" },
      ],
      lead_arc: ARC_CYCLE[n % 3],
      setups,
      payoffs,
      tension: [3, 4, 3, 4, 5],
      characters: ["hero", CAST[1 + (n % 5)][0]],
      locations: [PLACES[n % 3]],
      theme: "不能忘的事，寫下來。",
      carry: "鑰匙在晚照口袋；周嶼負傷；杜知道名單被偷。",
      ...(n === 20 ? { world_flip: true } : {}),
    });
  }
  const chapters = [1, 2, 3, 4].map((c) => ({
    number: c,
    title: `第 ${c} 篇`,
    theme: "賭注升級。",
    stakes: "全城",
    question: "誰在利用誰？",
    start_state: "起點",
    end_state: "終點",
    turn: "篇末的翻轉",
    episodes: episodes.slice((c - 1) * 10, c * 10),
  }));
  return {
    series: { slug: "synthetic-work", title: "測試作品", logline: "一句話賣點", premise: "一段前提。", note: "備註。", genre: "system-game", lead: "female", tone: "no-romance", aspects: [] },
    setting: {
      world: {
        era: "2026 年的臨港市。",
        places: PLACES.map((id) => ({ id, name: `地點 ${id}`, description: "固定辨識物。" })),
        factions: [{ name: "星軌", wants: "第九層", hides: "存檔" }, { name: "鐵幕", wants: "發電機", hides: "名單" }],
      },
      rules: ["規則一", "規則二", "規則三", "規則四"],
      characters: CAST.map(([id, name, role]) => ({
        id, name, role, age: "30 歲", appearance: "a woman of thirty with short black hair, grey hoodie, a red notebook", voice: { provider: "gemini", name: "Kore", style: "台灣國語" },
        personality: "冷靜", want: "活著", fear: "忘記", secret: "秘密", speech: "先確認一件事", relationships: [{ with: "hero", kind: "盟友" }],
      })),
      mysteries,
      tone: "冷而克制。",
      imagery: "冷藍的面板光。",
      naming: ["人名兩到三字", "門以數字命名"],
      never: ["借用既有作品", "說教", "血腥"],
      lexicon: Object.fromEntries(CAST.map(([, name]) => [name, null])),
      ending: "天梯消失。",
      cold_open: [1, 2, 3, 4].map((i) => ({ seconds: `${(i - 1) * 8}–${i * 8}`, picture: "畫面", audio: "聲音" })),
    },
    chapters,
    packaging: {
      titles: ["標題一", "標題二", "標題三"],
      description: "說明欄本文。",
      tags: ["漫劇", "AI漫劇", "一口氣看完", "系統"],
      thumbnails: ["A", "B", "C"].map((id) => ({ id, headline: "她死了30次", tag: null, composition: "構圖", episode: 1, scene: "場景", promise: "兌現" })),
      audience: "觀眾", visual_identity: "視覺", music: "音樂", pinned_comment: "置頂",
      why_million: ["一", "二", "三"],
    },
    continuity_notes: ["一", "二", "三"],
  };
}

test("a synthetic work that obeys every rule validates with no errors", () => {
  const { errors } = validateSource(syntheticSource());
  assert.deepEqual(errors, []);
});

test("the same cliffhanger type across a chapter boundary is refused", () => {
  const source = syntheticSource();
  source.chapters[1].episodes[0].cliffhanger.type = "reveal"; // episode 11 after episode 10's reveal
  const { errors } = validateSource(source);
  assert.ok(errors.some((e) => e.includes("episode 11") && e.includes("chapter boundaries")), errors.join("\n"));
});

test("a hook that would take longer than about six seconds to say is refused", () => {
  const source = syntheticSource();
  source.chapters[0].episodes[2].hook = "這一句鉤子實在太長了太長了太長了太長了太長了太長了太長了太長了完全說不完";
  const { errors } = validateSource(source);
  assert.ok(errors.some((e) => e.includes("episode 3") && e.includes("spoken characters")), errors.join("\n"));
});

test("four episodes in a row without a payoff fail the pipeline's own retention rule", () => {
  const source = syntheticSource();
  for (const e of source.chapters[0].episodes) e.payoffs = [];
  const { errors } = validateSource(source);
  assert.ok(errors.some((e) => e.includes("pay nothing off")), errors.join("\n"));
});

test("exactly one world flip, between episodes 18 and 22", () => {
  const source = syntheticSource();
  delete source.chapters[1].episodes[9].world_flip;
  assert.ok(validateSource(source).errors.some((e) => e.includes("exactly one episode carries world_flip")));
  source.chapters[0].episodes[4].world_flip = true; // episode 5, far too early
  assert.ok(validateSource(source).errors.some((e) => e.includes("episode 5") && e.includes("world flip")));
});

test("an unregistered character, place or mystery is refused", () => {
  const source = syntheticSource();
  source.chapters[2].episodes[3].characters = ["hero", "nobody"];
  source.chapters[2].episodes[4].locations = ["nowhere"];
  source.chapters[2].episodes[5].setups = ["m99"];
  const { errors } = validateSource(source);
  assert.ok(errors.some((e) => e.includes('unknown character "nobody"')));
  assert.ok(errors.some((e) => e.includes('unknown place "nowhere"')));
  assert.ok(errors.some((e) => e.includes("unknown setup m99")));
});

test("a mystery must be paid where its schedule says", () => {
  const source = syntheticSource();
  const ep33 = source.chapters[3].episodes[2];
  ep33.payoffs = ep33.payoffs.filter((id) => id !== "m01");
  const { errors } = validateSource(source);
  assert.ok(errors.some((e) => e.includes("mystery m01") && e.includes("episode 33")), errors.join("\n"));
});

test("a chapter's last episode must end on a reveal or a reversal", () => {
  const source = syntheticSource();
  source.chapters[2].episodes[9].cliffhanger.type = "danger";
  const { errors } = validateSource(source);
  assert.ok(errors.some((e) => e.includes("episode 30") && e.includes("reveal or a reversal")), errors.join("\n"));
});

test("compile writes the six pipeline documents and the one-button request", () => {
  const files = compile(syntheticSource());
  const documents = JSON.parse(files["documents.json"]).documents;
  assert.deepEqual(documents.map((d) => [d.kind, d.chapter_number]), [["setting", 0], ["outline", 0], ["chapter", 1], ["chapter", 2], ["chapter", 3], ["chapter", 4]]);
  for (const d of documents) {
    assert.ok(d.body_md.length > 0);
    assert.ok(d.body_json);
  }
  const request = JSON.parse(files["series-request.json"]);
  assert.equal(request.total_minutes, 120);
  assert.equal(request.compilation, true);
  assert.equal(request.hands_off, false);
  assert.equal(request.visual_tier, "hybrid");
  assert.equal(JSON.parse(files["outline.json"]).body_json.chapters.length, 4);
  assert.equal(JSON.parse(files["chapter-02.json"]).body_json.episodes[0].number, 11);
});

test("every work of the batch validates", async () => {
  for (const slug of SLUGS) {
    const source = await loadSource(slug);
    const { errors } = validateSource(source, slug);
    assert.deepEqual(errors, [], `${slug}:\n${errors.join("\n")}`);
  }
});

test("every continuity rule reaches the setting and its importable document", async () => {
  for (const slug of SLUGS) {
    const source = await loadSource(slug);
    const files = compile(source);
    const setting = JSON.parse(files["setting.json"]);
    const imported = JSON.parse(files["documents.json"]).documents.find(d => d.kind === "setting");
    assert.deepEqual(setting.body_json.continuity_notes, source.continuity_notes, slug);
    assert.deepEqual(imported.body_json.continuity_notes, source.continuity_notes, slug);
    assert.equal(imported.body_md, setting.body_md, slug);
    assert.equal(files["setting.md"], setting.body_md, slug);
    for (const rule of source.continuity_notes) assert.ok(imported.body_md.includes(rule), `${slug}: ${rule}`);
  }
});

test("a continuity-only edit invalidates the setting and import bundle until rebuilt", async (t) => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "claude-plan-drift-"));
  assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  const source = syntheticSource();
  const slug = source.series.slug;
  await fs.mkdir(path.join(root, slug));
  const write = async () => {
    for (const [name, body] of Object.entries(compile(source))) await fs.writeFile(path.join(root, slug, name), body);
  };
  await write();
  assert.deepEqual(await validateFiles(slug, source, root), []);
  source.continuity_notes.push("回歸測試專用：第三十五集仍須保留前集傷口與縫線。");
  const errors = await validateFiles(slug, source, root);
  for (const name of ["setting.md", "setting.json", "documents.json", "manifest.json"]) {
    assert.ok(errors.some(e => e.startsWith(`${name}:`)), `${name} failed to detect changed continuity`);
  }
  await write();
  assert.deepEqual(await validateFiles(slug, source, root), []);
});

test("blank continuity constraints cannot be delivered as production guidance", () => {
  const source = syntheticSource();
  source.continuity_notes = ["one", "two", "   "];
  assert.ok(validateSource(source).errors.some(e => e.includes("continuity_notes")));
});
