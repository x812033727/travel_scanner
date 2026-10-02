// Package the authored planning catalog for a GET-only admin view. No site calls or DB writes.
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, realpathSync, writeFileSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { CATALOG_COUNTS, DURATION_NOTE, proposedChapters, recordHash, reviseDurationText, ROOT, validatePolicy } from "./plans.mjs";

export const PLANS_PATH = "docs/videos/long-form/plans.json";
export const OUTPUT_PATH = "apps/api/app/video_plans/data/catalog.json";
const POLICY_PATH = "docs/videos/long-form/policy.json";
const SHA = /^[a-f0-9]{64}$/;
const SOURCES = {
  season1: ["docs/videos/so-thats-why/episodes.json", "episodes"],
  season2: ["docs/videos/so-thats-why/season2/dispositions.json", "episodes"],
  season3: ["docs/videos/so-thats-why/season3-topics.json", "episodes"],
  "brand-stories": ["docs/videos/story-plans/brand-stories-100/stories.json", "stories"],
  "ai-terms": ["docs/videos/ai-terms/terms.json", "terms"],
};
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const same = (left, right) => JSON.stringify(left) === JSON.stringify(right);
const requiredText = (value, name) => {
  if (typeof value !== "string" || !value.trim()) throw new Error(`${name}: nonempty text required`);
  return value;
};

export function requireSourcePath(relative) {
  if (typeof relative !== "string" || !relative.startsWith("docs/videos/")
    || relative.includes("\\") || relative.includes("\0") || relative.includes(":")) {
    throw new Error("source path must stay inside docs/videos");
  }
  if (relative.split("/").some((part) => !part || part === "." || part === "..")) {
    throw new Error("source path must stay inside docs/videos");
  }
  return relative;
}

/** A reader of repository source files, refusing traversal and symlinks outside the source tree. */
export function sourceReader(root = ROOT) {
  const directory = realpathSync(path.join(root, "docs", "videos"));
  return (relative) => {
    requireSourcePath(relative);
    const file = realpathSync(path.join(root, relative));
    const inside = path.relative(directory, file);
    if (!inside || inside === ".." || inside.startsWith(`..${path.sep}`) || path.isAbsolute(inside)) {
      throw new Error("source path must stay inside docs/videos");
    }
    return readFileSync(file);
  };
}

const list = (values) => (values ?? []).map((value) => `- ${value}`).join("\n");
const field = (heading, value) => typeof value === "string" && value.trim() ? `${heading}\n${value}` : "";
const paragraphs = (...values) => values.filter(Boolean).join("\n\n");

/** Retain authored sentences, chapter points and their limitations as readable source text. */
function sourceText(catalog, record) {
  if (catalog === "season1" || catalog === "season3") {
    return paragraphs(field("題目", record.title), field("開場問題", record.hook), field("核心解釋", record.answer),
      field("Shorts 題目提案", list(record.shorts)), field("畫面提案", list(record.key_visuals)),
      field("原企劃列出的查核項目", list(record.facts_to_verify)), field("原查核判定", record.verdict),
      field("原查核入口", record.fact_check ?? record.check));
  }
  if (catalog === "season2") {
    return paragraphs(field("製作題目", record.production_title),
      record.original_title !== record.production_title ? field("查核前的原題", record.original_title) : "",
      field("題目處置與限制", record.reason), field("原查核判定", record.original_verdict),
      field("原查核入口", record.original_check), field("原文字審稿收據", record.review_receipt),
      field("相關題目", list(record.duplicate_of)));
  }
  if (catalog === "brand-stories") {
    const chapters = record.chapters.map((chapter, index) => `第 ${index + 1} 章\n${chapter.point}`).join("\n\n");
    const claims = record.must_verify.map((claim, index) => paragraphs(`${index + 1}. ${claim.claim}`,
      `來源編號：${claim.sources.map((number) => number + 1).join("、")}`,
      claim.core ? "原企劃標示為核心主張。" : "",
      claim.attributed ? "保留來源歸屬，不改寫成無條件結論。" : "",
      claim.reviewer_only ? "原查核標示：僅審稿者可讀的來源。" : "")).join("\n\n");
    const sources = record.sources.map((source, index) => paragraphs(`${index + 1}. ${source.publisher}\n${source.url}`,
      field("原來源類型", source.kind), field("原來源支持的內容", source.supports), field("原確認日期", source.checked))).join("\n\n");
    const cast = record.cast.map((person) => paragraphs(field("原人物識別", person.id), person.role, person.appearance)).join("\n\n");
    return paragraphs(field("題目", record.title), field("故事主題", record.subject), field("原企劃分類", record.category),
      field("原企劃地區", record.region), field("原企劃敏感議題標記", record.sensitivity), field("相關站內文章", record.related_guide),
      field("原企劃製作序號", String(record.number)), field("故事摘要", record.logline), field("核心問題", record.question),
      field("章節要點", chapters), field("帶走的觀點", record.takeaway), field("必須核對的主張", claims),
      field("原企劃來源", sources), field("查核限制與未採用說法", record.caveats), field("畫面注意事項", record.image_notes),
      field("人物畫面提案", cast), field("人名與名稱", list(record.names)),
      field("縮圖文字提案", record.thumbnail?.headline), field("縮圖畫面提案", record.thumbnail?.idea),
      record.publish ? `原企劃的發布順序提案（不是正式排程）\n第 ${record.publish.day} 天，${record.publish.slot}` : "");
  }
  return paragraphs(field("來源文章標題", record.article_title), field("名詞", record.zh), field("英文名詞", record.en),
    field("其他稱呼", list(record.aliases)), field("開場問題", record.hook), field("企劃備註與分工", record.notes),
    field("來源文章", record.article_url), field("相鄰名詞", list(record.related)),
    field("原企劃列出的既有影片參考", list(record.existing_videos)));
}

function stageFor(catalog, record) {
  if (catalog === "season1" || catalog === "season2") return "REVIEWED_OUTLINE_NOT_MEDIA";
  if (catalog === "season3") return "CHECKED_CANDIDATE_REQUIRES_OUTLINE";
  if (catalog === "brand-stories") return "REVIEWED_STORY_PLAN_NOT_MEDIA";
  return record.status === "covered" ? "COVERED_DO_NOT_REMAKE" : "TERM_PLAN_NOT_MEDIA";
}

/** All reads are injectable for source-drift tests; the CLI uses the confined filesystem reader. */
export function buildAdminCatalog({ root = ROOT, readSource = sourceReader(root) } = {}) {
  const cache = new Map();
  const bytes = (relative) => {
    requireSourcePath(relative);
    if (!cache.has(relative)) cache.set(relative, readSource(relative));
    return cache.get(relative);
  };
  const json = (relative) => JSON.parse(bytes(relative).toString("utf8"));
  const plansBytes = bytes(PLANS_PATH);
  const plans = JSON.parse(plansBytes.toString("utf8"));
  const policy = json(POLICY_PATH);
  const policyProblems = validatePolicy(policy);
  if (policyProblems.length) throw new Error(policyProblems.join("; "));
  if (plans.schema_version !== 1 || plans.status !== "DURATION_PLANS_ONLY" || !Array.isArray(plans.entries)
    || plans.entries.length !== 473 || plans.totals?.entries !== 473 || !same(plans.totals.catalogs, CATALOG_COUNTS)) {
    throw new Error("all 473 plans in the five expected catalogs are required");
  }
  if (!plans.source_hashes || typeof plans.source_hashes !== "object" || Array.isArray(plans.source_hashes)) {
    throw new Error("plans source hashes are required");
  }
  for (const [relative, expected] of Object.entries(plans.source_hashes)) {
    if (!SHA.test(expected) || sha(bytes(relative)) !== expected) throw new Error(`source hash drift: ${relative}`);
  }
  if (plans.policy_sha256 !== sha(bytes(POLICY_PATH)) || plans.source_hashes[POLICY_PATH] !== plans.policy_sha256) {
    throw new Error("duration policy binding drift");
  }
  const boundBytes = (relative) => {
    if (!Object.hasOwn(plans.source_hashes, relative)) throw new Error(`source binding missing: ${relative}`);
    return bytes(relative);
  };
  const records = new Map();
  for (const [catalog, [relative, key]] of Object.entries(SOURCES)) {
    const document = JSON.parse(boundBytes(relative).toString("utf8"));
    if (!Array.isArray(document[key])) throw new Error(`${catalog}: source records missing`);
    const byId = new Map();
    for (const record of document[key]) {
      if (byId.has(record.id)) throw new Error(`${catalog}: duplicate source id ${record.id}`);
      byId.set(requiredText(record.id, `${catalog} source id`), record);
    }
    records.set(catalog, byId);
  }
  const packaging = new Map();
  for (const relative of Object.keys(plans.source_hashes).sort()) {
    if (!/^docs\/videos\/so-thats-why\/season2\/[^/]+-packaging\.json$/.test(relative)) continue;
    for (const record of json(relative).episodes) {
      if (packaging.has(record.id)) throw new Error(`season2: duplicate packaged id ${record.id}`);
      packaging.set(record.id, record);
    }
  }
  const identities = new Set();
  const slugs = new Set();
  const counts = Object.fromEntries(Object.keys(CATALOG_COUNTS).map((catalog) => [catalog, 0]));
  const entries = plans.entries.map((plan) => {
    const config = SOURCES[plan.catalog];
    if (!config || plan.source !== config[0]) throw new Error(`unknown catalog/source: ${plan.catalog}`);
    const record = records.get(plan.catalog).get(plan.id);
    if (!record || recordHash(record) !== plan.source_record_sha256) throw new Error(`source record drift: ${plan.catalog}/${plan.id}`);
    const identity = `${plan.catalog}/${plan.id}`;
    if (identities.has(identity)) throw new Error(`duplicate plan identity: ${identity}`);
    identities.add(identity);
    requiredText(plan.video_slug, `${identity} video slug`);
    if (slugs.has(plan.video_slug)) throw new Error(`duplicate video slug: ${plan.video_slug}`);
    slugs.add(plan.video_slug);
    counts[plan.catalog] += 1;
    const expectedSlug = plan.catalog === "brand-stories" ? record.slug
      : plan.catalog === "ai-terms" ? record.video_slug : `sothatswhy-${record.id.toLowerCase()}`;
    if (plan.video_slug !== expectedSlug || plan.stage !== stageFor(plan.catalog, record)
      || plan.source_status !== (record.status ?? "reviewed-plan")) throw new Error(`source identity/stage drift: ${identity}`);
    if (plan.target_seconds !== policy.catalogs[plan.catalog].target_seconds
      || plan.minimum_content_seconds !== 480 || plan.minimum_final_seconds !== 480) throw new Error(`duration drift: ${identity}`);
    if (plan.catalog === "season2" && !["adopt", "angle"].includes(record.decision)) throw new Error(`rejected second-season plan: ${identity}`);
    if (!["season1", "season2"].includes(plan.catalog) && plan.backend_inputs) throw new Error(`source is not a one-off input: ${identity}`);
    let title = record.title;
    if (plan.catalog === "season2") title = record.production_title;
    if (plan.catalog === "ai-terms") title = record.zh;
    const details = [{ label: "source_record", text: requiredText(sourceText(plan.catalog, record), `${identity} detail`) }];
    let packagePath = null;
    let packageSha = null;
    if (["season1", "season2"].includes(plan.catalog)) {
      packagePath = plan.catalog === "season1" ? `docs/videos/so-thats-why/${record.fact_check}`
        : `docs/videos/so-thats-why/season2/${record.package}`;
      if (plan.source_package !== packagePath) throw new Error(`source package path drift: ${identity}`);
      const packageBytes = boundBytes(packagePath);
      packageSha = sha(packageBytes);
      if (plan.source_package_sha256 !== packageSha) throw new Error(`source package hash drift: ${identity}`);
      const packageText = packageBytes.toString("utf8");
      details.push({ label: "source_package", text: packageText });
      let expectedInputs;
      if (plan.catalog === "season1") {
        const blocks = [...packageText.matchAll(/```text\r?\n([\s\S]*?)\r?\n```/g)].map((match) => match[1]);
        if (blocks.length !== 2) throw new Error(`${identity}: premise/note source blocks missing`);
        expectedInputs = { style_preset: "flat-explainer", target_minutes: 10, premise: blocks[0], note: reviseDurationText(blocks[1]) };
      } else {
        const original = packaging.get(plan.id);
        if (!original || original.package_sha256 !== packageSha) throw new Error(`second-season package binding drift: ${identity}`);
        expectedInputs = { style_preset: "flat-explainer", target_minutes: 10, premise: original.backend_inputs.premise,
          note: `${reviseDurationText(original.backend_inputs.note)}\n${DURATION_NOTE}` };
        if (!same(plan.proposed_chapters, proposedChapters(packageText))) throw new Error(`chapter revision drift: ${identity}`);
        if (plan.source_review !== `docs/videos/so-thats-why/season2/${record.review_receipt}`) throw new Error(`review source drift: ${identity}`);
        boundBytes(plan.source_review);
        details.push({ label: "effective_chapters", text: plan.proposed_chapters.map((chapter) =>
          `${chapter.heading}\n開始 ${chapter.start_seconds} 秒，章節預算 ${chapter.proposed_seconds} 秒\n${chapter.content}`).join("\n\n") });
      }
      if (!same(plan.backend_inputs, expectedInputs)) throw new Error(`effective input drift: ${identity}`);
      details.push({ label: "effective_inputs", text: paragraphs(field("故事前提", plan.backend_inputs.premise), field("新版製作備註", plan.backend_inputs.note)) });
    }
    return { catalog: plan.catalog, id: plan.id, video_slug: plan.video_slug, title: requiredText(title, `${identity} title`),
      source_status: plan.source_status, stage: plan.stage, target_duration_seconds: plan.target_seconds,
      min_duration_seconds: plan.minimum_content_seconds, source_path: plan.source, source_sha256: plans.source_hashes[plan.source],
      source_record_sha256: plan.source_record_sha256, source_package_path: packagePath, source_package_sha256: packageSha, details };
  });
  if (!same(counts, CATALOG_COUNTS) || entries.filter((entry) => entry.stage === "COVERED_DO_NOT_REMAKE").length !== 1) {
    throw new Error("catalog counts or covered reference drift");
  }
  const order = Object.keys(CATALOG_COUNTS);
  entries.sort((a, b) => order.indexOf(a.catalog) - order.indexOf(b.catalog) || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  return { format_version: 1, plans_sha256: sha(plansBytes), catalog_counts: counts, entries };
}

export const serializeCatalog = (catalog) => `${JSON.stringify(catalog, null, 2)}\n`;

/** Check requires byte-for-byte reproduction; only build writes the one new API bundle. */
export function runAdminCatalog(command, root = ROOT) {
  if (!["build", "check"].includes(command)) throw new Error("use build | check");
  const text = serializeCatalog(buildAdminCatalog({ root }));
  const destination = path.join(root, OUTPUT_PATH);
  if (command === "build") {
    mkdirSync(path.dirname(destination), { recursive: true });
    writeFileSync(destination, text);
  } else if (readFileSync(destination, "utf8") !== text) {
    throw new Error("admin catalog differs from current hash-bound source plans; rebuild and review it");
  }
  return `${command === "build" ? "Built" : "PASS:"} all 473 source planning entries; no database import or production work.`;
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  try {
    if (process.argv.length !== 3) throw new Error("use build | check");
    console.log(runAdminCatalog(process.argv[2]));
  } catch (error) {
    console.error(`FAIL: ${error.message}`);
    process.exitCode = 1;
  }
}
