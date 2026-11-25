import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  buildDrivePushCommand,
  convertVideoJsonToFlowSpec,
  sanitizeH3TagsForFlow,
} from "./bridges/video-json-adapter.mjs";
import { estimateClipCredits } from "./config.mjs";
import { FlowDriver } from "./drivers/driver-interface.mjs";
import { GflowCliDriver } from "./drivers/gflow-cli-driver.mjs";
import { planClipBudget, recordCreditEvent } from "./guards/budget-guard.mjs";
import { resolveEpisodePaths } from "./guards/path-boundary.mjs";
import { preflightShotList, scanPromptText } from "./guards/prompt-safety.mjs";
import { JobQueue } from "./jobs/job-queue.mjs";
import { FlowOrchestrator } from "./orchestrator.mjs";
import { writeStillsQaGallery } from "./postprocess/qa-contact-sheet.mjs";
import {
  buildExtractLastFrameArgs,
  buildExtractRawAudioArgs,
  inspectClipQc,
  parsePsnrFromStderr,
  parseSceneCutTimesFromStderr,
} from "./postprocess/upscale-1080p30.mjs";

function makePngBuffer(width, height) {
  const buf = Buffer.alloc(33);
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]).copy(buf, 0);
  buf.writeUInt32BE(13, 8);
  buf.write("IHDR", 12, "ascii");
  buf.writeUInt32BE(width, 16);
  buf.writeUInt32BE(height, 20);
  return buf;
}

class DramaMockDriver extends FlowDriver {
  constructor() {
    super({ name: "drama-mock" });
    this.calls = [];
    this.remoteVideos = [];
    this.credits = 900;
  }

  async getVersion() {
    return "gflow-cli 0.99.0";
  }

  async checkAuth({ profile } = {}) {
    return { authenticated: true, profile: profile || "default", account: "owner@example.com", plan: "Google AI Ultra" };
  }

  async getCredits() {
    return { credits: this.credits, plan: "Google AI Ultra" };
  }

  async listProfiles() {
    return [
      { profile: "default", isDefault: true, authenticated: true, account: "a@example.com", plan: "Pro", credits: 450 },
      { profile: "pro-2", isDefault: false, authenticated: true, account: "b@example.com", plan: "Ultra", credits: 1200 },
    ];
  }

  async createProject({ name }) {
    this.calls.push({ op: "createProject", name });
    return { projectId: `proj_${name}`, name };
  }

  async createCharacter(params) {
    this.calls.push({ op: "createCharacter", ...params });
    return { entityId: `ent_${params.name}`, name: params.name, projectId: params.projectId };
  }

  async generateImage(params) {
    this.calls.push({ op: "generateImage", ...params });
    fs.mkdirSync(path.dirname(params.outFile), { recursive: true });
    const [w, h] = params.aspect === "9:16" ? [768, 1376] : [1376, 768];
    fs.writeFileSync(params.outFile, makePngBuffer(w, h));
    return {
      outFile: params.outFile,
      mediaId: `img_${this.calls.length}`,
      projectId: params.projectId,
      model: params.model,
      charged: "no",
    };
  }

  async generateVideo(params) {
    this.calls.push({ op: "generateVideo", ...params });
    fs.mkdirSync(path.dirname(params.outFile), { recursive: true });
    fs.writeFileSync(params.outFile, Buffer.from(`fake-mp4-${this.calls.length}`));
    const cost = estimateClipCredits({ model: params.model, durationSec: params.durationSec });
    this.credits -= cost;
    const mediaId = `vid_${this.calls.length}`;
    this.remoteVideos.push({ media_id: mediaId, out_file: params.outFile });
    return {
      outFile: params.outFile,
      mediaId,
      projectId: params.projectId,
      model: params.model,
      creditsSpent: cost,
      charged: "yes",
    };
  }

  async extendVideo(params) {
    this.calls.push({ op: "extendVideo", ...params });
    fs.mkdirSync(path.dirname(params.outFile), { recursive: true });
    fs.writeFileSync(params.outFile, Buffer.from(`fake-extended-mp4-${this.calls.length}`));
    return {
      outFile: params.outFile,
      mediaId: `ext_${this.calls.length}`,
      projectId: params.projectId,
      creditsSpent: 15,
      charged: "yes",
    };
  }

  async listRemoteVideos() {
    return this.remoteVideos;
  }

  async downloadMedia({ mediaId, outDir }) {
    fs.mkdirSync(outDir, { recursive: true });
    const dest = path.join(outDir, `${mediaId}-recovered.mp4`);
    fs.writeFileSync(dest, Buffer.from(`recovered-${mediaId}`));
    return { mediaId, outFile: dest };
  }
}

test("estimateClipCredits scales Omni 1.2 Flash by duration and maps Veo tiers accurately", () => {
  assert.equal(estimateClipCredits({ model: "omni-1.2-flash", durationSec: 4 }), 12);
  assert.equal(estimateClipCredits({ model: "omni-1.2-flash", durationSec: 6 }), 18);
  assert.equal(estimateClipCredits({ model: "omni-1.2-flash", durationSec: 10 }), 30);
  assert.equal(estimateClipCredits({ model: "veo-lite" }), 10);
  assert.equal(estimateClipCredits({ model: "veo-fast" }), 20);
  assert.equal(estimateClipCredits({ model: "veo-quality" }), 100);
});

test("drama safety profile treats martial action words as warnings while still hard-blocking minors/gore", () => {
  const dramaAction = scanPromptText("A dramatic bloody duel in the rain", { series: "drama-16x9" });
  assert.equal(dramaAction.ok, true);
  assert.equal(dramaAction.warningCount, 1);

  const explainerAction = scanPromptText("A dramatic bloody duel in the rain", { series: "curio" });
  assert.equal(explainerAction.ok, false);

  const dramaMinor = scanPromptText("A little girl runs across the yard", { series: "drama-16x9" });
  assert.equal(dramaMinor.ok, false);
});

test("video.json adapter strips H3 <Picture N> tags, preserves 0-credit data.source cuts, and adds silent guard on shorts", () => {
  assert.equal(sanitizeH3TagsForFlow("Cat shown in <Picture 1> knocks over mug"), "Cat from the starting frame knocks over mug");

  const videoJson = {
    slug: "shorts-cat-office-e01",
    kind: "shorts",
    characters: [{ id: "cat", name: "OrangeCat", sheet: "/tmp/cat.png", no_accessories: ["glasses"] }],
    scenes: [
      {
        id: "s01",
        chapter: "setup",
        data: {
          characters: ["cat"],
          camera: "Medium shot at office desk",
          prompt: "OrangeCat shown in <Picture 1> staring at coffee cup",
          motion: "Slowly raises paw toward mug",
        },
      },
      {
        id: "s02",
        chapter: "payoff",
        data: { source: "s01", characters: ["cat"] },
      },
    ],
  };

  const converted = convertVideoJsonToFlowSpec(videoJson);
  assert.equal(converted.series, "shorts");
  assert.equal(converted.stats.clips, 1);
  assert.equal(converted.stats.cuts, 1);
  assert.doesNotMatch(converted.shotList.shots[0].still_prompt, /<Picture 1>/);
  assert.match(converted.shotList.shots[0].video_prompt, /zero spoken dialogue/i);
  assert.equal(converted.shotList.shots[1].mode, "cut");
  assert.equal(converted.shotList.shots[1].source, "s01");

  const pre = preflightShotList(converted.shotList, { series: "shorts" });
  assert.equal(pre.ok, true);
  assert.equal(pre.summary.cutCount, 1);
  assert.equal(pre.summary.estimatedCredits, 12);
});

test("GflowCliDriver builds verified args for character create and video extend", () => {
  const driver = new GflowCliDriver({ binary: "gflow", profile: "pro-2", runtimeHome: "/tmp/flow" });
  const charArgs = driver.buildCreateCharacterArgs({
    projectId: "p1",
    name: "Nora",
    imagePath: "/tmp/nora.png",
    bodyImagePath: "/tmp/nora-body.png",
    voice: "Aoede",
  });
  assert.deepEqual(charArgs, [
    "character",
    "create",
    "--project",
    "p1",
    "--name",
    "Nora",
    "--image",
    "/tmp/nora.png",
    "--body-image",
    "/tmp/nora-body.png",
    "--voice",
    "Aoede",
    "--json",
    "--profile",
    "pro-2",
  ]);

  const extArgs = driver.buildExtendVideoArgs({
    source: "media-99",
    prompt: "Camera glides forward through mist",
    projectId: "p1",
    durationSec: 5,
    maxCredits: 20,
    outFile: "/tmp/ext.mp4",
  });
  assert.deepEqual(extArgs, [
    "video",
    "extend",
    "media-99",
    "Camera glides forward through mist",
    "--project",
    "p1",
    "--duration",
    "5",
    "--max-credits",
    "20",
    "--out-file",
    "/tmp/ext.mp4",
    "--json",
    "--profile",
    "pro-2",
  ]);
});

test("FFmpeg QC parses PSNR and mid-clip hard cuts, plus 9:16 HTML gallery includes safe-zone and JSON copy button", async () => {
  assert.equal(parsePsnrFromStderr("PSNR y:28.4 u:34.1 v:35.0 average:29.85 min:29.85"), 29.85);
  assert.deepEqual(
    parseSceneCutTimesFromStderr("n:0 pts_time:0.04\nn:1 pts_time:2.350\nn:2 pts_time:3.70"),
    [2.35, 3.7],
  );
  assert.ok(buildExtractLastFrameArgs({ inputPath: "a.mp4", outputPngPath: "b.png" }).includes("-sseof"));
  assert.ok(buildExtractRawAudioArgs({ inputPath: "a.mp4", outputWavPath: "b.wav" }).includes("pcm_s16le"));

  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "flow-qc-"));
  try {
    const kf = path.join(dir, "s01.png");
    const clip = path.join(dir, "s01.mp4");
    fs.writeFileSync(kf, makePngBuffer(768, 1376));
    fs.writeFileSync(clip, Buffer.from("mp4"));

    const qc = await inspectClipQc({
      clipPath: clip,
      keyframePath: kf,
      durationSec: 4,
      runFfmpeg: async (_bin, args) => {
        if (args.some((a) => a.includes("psnr"))) {
          return { exitCode: 0, stderr: "PSNR y:25.1 average:26.40" };
        }
        return { exitCode: 0, stderr: "pts_time:2.500" };
      },
    });
    assert.equal(qc.psnrOk, true);
    assert.equal(qc.frame0Psnr, 26.4);
    assert.deepEqual(qc.hardCutTimes, [2.5]);
    assert.equal(qc.recommendedTrim.durSec, 2.4);

    const gallery = writeStillsQaGallery({
      galleryFile: path.join(dir, "qa-gallery.html"),
      slug: "drama-vertical-e01",
      series: "drama-9x16",
      safeZoneOverlay: true,
      items: [{ shotId: "s01", track: "character", width: 768, height: 1376, qaStatus: "pending", filePath: kf, prompt: "Test" }],
    });
    const html = fs.readFileSync(gallery, "utf8");
    assert.match(html, /safe-zone/);
    assert.match(html, /copyApprovePayload/);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test("full AI drama lifecycle: cast + @Name, edit_from chain, continue_from last frame, multi-take + MAX_CLIP_TAKES=2, extend, reconcile, and profiles", async () => {
  const fakeRepo = fs.mkdtempSync(path.join(os.tmpdir(), "flow-drama-repo-"));
  const runtimeHome = fs.mkdtempSync(path.join(os.tmpdir(), "flow-drama-home-"));
  const driver = new DramaMockDriver();
  const queue = new JobQueue({ runtimeHome, minPauseMs: 0, maxPauseMs: 0 });

  const extractedFrames = [];
  const orchestrator = new FlowOrchestrator({
    driver,
    queue,
    repoRoot: fakeRepo,
    runtimeHome,
    extractLastFrameFn: async ({ inputPath, outputPngPath }) => {
      extractedFrames.push({ inputPath, outputPngPath });
      fs.mkdirSync(path.dirname(outputPngPath), { recursive: true });
      fs.writeFileSync(outputPngPath, makePngBuffer(1376, 768));
      return { outputPngPath, sha256: "lastframesha" };
    },
    upscaleFn: async ({ inputPath, outputPath, qa4OutputPath, rawAudioOutputPath }) => {
      fs.mkdirSync(path.dirname(outputPath), { recursive: true });
      fs.writeFileSync(outputPath, Buffer.from(`up:${path.basename(outputPath)}`));
      if (qa4OutputPath) {
        fs.mkdirSync(path.dirname(qa4OutputPath), { recursive: true });
        fs.writeFileSync(qa4OutputPath, Buffer.from("qa4"));
      }
      if (rawAudioOutputPath) {
        fs.mkdirSync(path.dirname(rawAudioOutputPath), { recursive: true });
        fs.writeFileSync(rawAudioOutputPath, Buffer.from("wav"));
      }
      return {
        inputPath,
        outputPath,
        qa4Path: qa4OutputPath,
        rawAudioPath: rawAudioOutputPath,
        qc: { frame0Psnr: 29.5, psnrOk: true, hardCutTimes: [], recommendedTrim: { inSec: 0, durSec: 4, keepCuts: false }, ok: true },
        rawSha256: "rawsha",
        upscaledSha256: `sha_${path.basename(outputPath)}`,
        spec: { width: 1920, height: 1080, fps: 30, colorspace: "bt709", colorRange: "tv", audioStripped: true },
      };
    },
  });

  try {
    // 1. Multi-profile overview
    const profiles = await orchestrator.flowProfiles();
    assert.equal(profiles.ok, true);
    assert.equal(profiles.count, 2);
    assert.equal(profiles.totalCredits, 1650);

    // 2. Init drama-16x9 episode with dramaName & episodeLabel
    const slug = "zhong-tian-qu-qi-e033";
    const init = await orchestrator.flowInitEpisode({
      slug,
      series: "drama-16x9",
      dramaName: "zhong-tian-qu-qi",
      episodeLabel: "第033集",
      createProjects: true,
    });
    assert.equal(init.ok, true);

    // 3. Register two cast characters with wardrobe look + noAccessories anti-bleed + Flow @Name
    const heroSheet = path.join(fakeRepo, "work", "video-episodes", slug, "hero.png");
    const rivalSheet = path.join(fakeRepo, "work", "video-episodes", slug, "rival.png");
    fs.writeFileSync(heroSheet, makePngBuffer(1376, 768));
    fs.writeFileSync(rivalSheet, makePngBuffer(1376, 768));

    const reg1 = await orchestrator.flowRegisterCharacter({
      slug,
      id: "hero",
      name: "LinChen",
      refs: [heroSheet],
      looks: { winter: heroSheet },
      noAccessories: ["glasses"],
      createFlowEntity: true,
    });
    assert.equal(reg1.mentionSyntax, "@LinChen");
    await orchestrator.flowRegisterCharacter({
      slug,
      id: "rival",
      name: "Zhou",
      refs: [rivalSheet],
    });

    // 4. Write drama shot list using edit_from (s02 -> s01), continue_from (s03 -> s02), and 0-credit cut (s04 -> s01)
    const epDir = path.join(fakeRepo, "work", "video-episodes", slug);
    fs.writeFileSync(
      path.join(epDir, "flow-shot-list.json"),
      JSON.stringify({
        series: "drama-16x9",
        shots: [
          {
            id: "s01",
            chapter: "act1",
            track: "character",
            mode: "clip",
            characters: ["hero", "rival"],
            character_looks: { hero: "winter" },
            clip_duration_sec: 6,
            still_prompt: "Courtyard confrontation in falling snow",
            video_prompt: "Hero raises hand calmly in falling snow",
          },
          {
            id: "s02",
            chapter: "act1",
            track: "character",
            mode: "clip",
            edit_from: "s01",
            characters: ["hero", "rival"],
            clip_duration_sec: 4,
            still_prompt: "Same courtyard angle, rival steps back surprised",
            video_prompt: "Rival flinches backward dropping fan",
          },
          {
            id: "s03",
            chapter: "act1",
            track: "character",
            mode: "clip",
            continue_from: "s02",
            clip_duration_sec: 4,
            still_prompt: "Fallback description",
            video_prompt: "Folded fan hits stone tiles and slides",
          },
          {
            id: "s04",
            chapter: "act1",
            track: "character",
            mode: "cut",
            source: "s01",
          },
        ],
      }),
    );

    // 5. Generate stills (s02 chains off s01 via edit_from; multi-character prompt gets anti-bleed suffix!)
    const stillRun = await orchestrator.flowGenerateStills({ slug, shotIds: ["s01", "s02"], waitMs: 5000 });
    assert.equal(stillRun.job.status, "completed");
    const imgCalls = driver.calls.filter((c) => c.op === "generateImage");
    assert.match(imgCalls[0].prompt, /LinChen has NO glasses/);
    assert.ok(imgCalls[1].refs.includes(path.join(epDir, "stills", "s01.png")));

    await orchestrator.flowApproveStills({ slug, approved: ["s01", "s02"] });

    // 6. Plan & run s01 (6s=18cr) + s02 (4s=12cr) + s03 (continue_from s02, 4s=12cr) = 42 credits!
    const plan1 = await orchestrator.flowPlanClips({ slug });
    assert.equal(plan1.ok, true);
    assert.equal(plan1.plannedCredits, 42);
    const clipRun1 = await orchestrator.flowGenerateClips({
      slug,
      confirm_token: plan1.confirm_token,
      waitMs: 5000,
    });
    assert.equal(clipRun1.job.status, "completed");
    assert.equal(extractedFrames.length, 1); // s03 extracted real last frame of s02!

    // 7. Take 2 retake on s01 succeeds and preserves Take 1; Take 3 is blocked by MAX_CLIP_TAKES=2!
    const planTake2 = await orchestrator.flowPlanClips({ slug, shotIds: ["s01"] });
    assert.equal(planTake2.ok, true);
    assert.equal(planTake2.shotPlans[0].nextTake, 2);
    const runTake2 = await orchestrator.flowGenerateClips({
      slug,
      shotIds: ["s01"],
      confirm_token: planTake2.confirm_token,
      waitMs: 5000,
    });
    assert.equal(runTake2.job.status, "completed");

    const blockedTake3 = await orchestrator.flowPlanClips({ slug, shotIds: ["s01"] });
    assert.equal(blockedTake3.ok, false);
    assert.equal(blockedTake3.reason, "retake_limit_reached");

    // 8. Select Take 1 back while keeping Take 2 preserved in flow-clips/takes/
    const selected = await orchestrator.flowSelectTake({ slug, shotId: "s01", take: 1 });
    assert.equal(selected.ok, true);
    assert.equal(selected.selectedTake, 1);
    assert.equal(selected.totalPreservedTakes, 2);
    assert.ok(fs.existsSync(selected.clipsImportBridgeFile));

    // 9. Extend s01 with explicit confirm_token (model="extend")
    const paths = resolveEpisodePaths(slug, { repoRoot: fakeRepo });
    const extPlan = planClipBudget({
      episodePaths: paths,
      series: "drama-16x9",
      shotIds: ["s01"],
      model: "extend",
      shotPlans: [{ shotId: "s01", model: "extend", durationSec: 5, credits: 15 }],
    });
    const extRun = await orchestrator.flowExtendClip({
      slug,
      shotId: "s01",
      prompt: "Snow intensifies as courtyard lantern flickers",
      confirm_token: extPlan.confirm_token,
      durationSec: 5,
      waitMs: 5000,
    });
    assert.equal(extRun.job.status, "completed");

    // 10. Simulate a `charged: maybe` entry & reconcile from remote Flow catalog
    const knownMediaId = driver.remoteVideos[0].media_id;
    recordCreditEvent(paths.ledgerFile, {
      slug,
      series: "drama-16x9",
      shotId: "s02",
      credits: 12,
      charged: "maybe",
      mediaId: knownMediaId,
      note: "Timeout after submit",
    });
    const rec = await orchestrator.flowReconcile({ slug });
    assert.equal(rec.ok, true);
    assert.equal(rec.recovered.length, 1);
    assert.ok(fs.existsSync(rec.recovered[0].downloadedPath));

    // 11. Ledger reports drama Drive path, 0-credit cut count, multi-takes, and readyForDrivePush
    const ledger = await orchestrator.flowEpisodeLedger({ slug });
    assert.equal(ledger.clips.zeroCreditCuts, 1);
    assert.equal(ledger.readyForDrivePush, true);
    assert.match(ledger.drivePushCommand, /--series zhong-tian-qu-qi --path "第033集\/製作檔\/zhong-tian-qu-qi-e033"/);
    assert.match(buildDrivePushCommand({ slug: "shorts-cat-e01", series: "shorts", workdir: epDir, dramaName: "社畜地獄" }), /--series shorts --path "社畜地獄\/shorts-cat-e01"/);
  } finally {
    fs.rmSync(fakeRepo, { recursive: true, force: true });
    fs.rmSync(runtimeHome, { recursive: true, force: true });
  }
});

test("Phase 3 polish: shared series Cast inheritance, flow_plan_extend + spillover profiles, 2K still upscale, import-all, and validated Drive push", async () => {
  const { runImportBridgeBatch, runValidatedDrivePush } = await import("./cli.mjs");
  const fakeRepo = fs.mkdtempSync(path.join(os.tmpdir(), "flow-p3-repo-"));
  const runtimeHome = fs.mkdtempSync(path.join(os.tmpdir(), "flow-p3-home-"));

  const driver = new DramaMockDriver();
  driver.credits = 5; // Force insufficient balance on default profile to test spillover recommendation!
  driver.upscaleImage = async ({ mediaId, scale, outFile }) => {
    fs.mkdirSync(path.dirname(outFile), { recursive: true });
    fs.writeFileSync(outFile, makePngBuffer(2752, 1536));
    return { mediaId, scale, outFile };
  };

  const cliDriver = new GflowCliDriver({ binary: "gflow", profile: "pro-2", runtimeHome });
  assert.deepEqual(
    cliDriver.buildUpscaleImageArgs({ mediaId: "m-1", scale: "4k", projectId: "p1", outFile: "/tmp/u.png" }),
    ["image", "upscale", "m-1", "--scale", "4k", "--project", "p1", "--out-file", "/tmp/u.png", "--json", "--profile", "pro-2"],
  );

  const queue = new JobQueue({ runtimeHome, minPauseMs: 0, maxPauseMs: 0 });
  const orchestrator = new FlowOrchestrator({
    driver,
    queue,
    repoRoot: fakeRepo,
    runtimeHome,
    upscaleFn: async ({ inputPath, outputPath }) => {
      fs.mkdirSync(path.dirname(outputPath), { recursive: true });
      fs.writeFileSync(outputPath, Buffer.from("fake-1080p"));
      return { inputPath, outputPath, qa4Path: null, rawSha256: "r", upscaledSha256: "u", spec: { width: 1920, height: 1080, fps: 30, colorspace: "bt709", colorRange: "tv", audioStripped: true } };
    },
  });

  try {
    // 1. Register character on Ep 33 with saveToSeries: true -> Ep 34 auto-inherits it!
    await orchestrator.flowInitEpisode({ slug: "zt-e033", series: "drama-16x9", dramaName: "zhong-tian-qu-qi", createProjects: true });
    const reg = await orchestrator.flowRegisterCharacter({
      slug: "zt-e033",
      id: "hero",
      name: "LinChen",
      noAccessories: ["glasses"],
      saveToSeries: true,
    });
    assert.ok(reg.seriesCastFile && fs.existsSync(reg.seriesCastFile));

    const ep34Init = await orchestrator.flowInitEpisode({ slug: "zt-e034", series: "drama-16x9", dramaName: "zhong-tian-qu-qi", createProjects: true });
    assert.equal(ep34Init.inheritedSeriesCharacters, 1);
    const ep34Cast = JSON.parse(fs.readFileSync(path.join(fakeRepo, "work", "video-episodes", "zt-e034", "cast.json"), "utf8"));
    assert.equal(ep34Cast.characters.hero.name, "LinChen");

    // 2. Generate still on Ep 34 -> upscale to 2K (0 Veo credits)
    const ep34Dir = path.join(fakeRepo, "work", "video-episodes", "zt-e034");
    fs.writeFileSync(
      path.join(ep34Dir, "flow-shot-list.json"),
      JSON.stringify({
        series: "drama-16x9",
        shots: [{ id: "s01", track: "character", mode: "clip", characters: ["hero"], still_prompt: "Hero on mountain ridge", video_prompt: "Wind blows cloak" }],
      }),
    );
    await orchestrator.flowGenerateStills({ slug: "zt-e034", waitMs: 5000 });
    await orchestrator.flowApproveStills({ slug: "zt-e034", approved: ["s01"] });

    const upStill = await orchestrator.flowUpscaleStill({ slug: "zt-e034", shotId: "s01", scale: "2k" });
    assert.equal(upStill.ok, true);
    assert.equal(upStill.dimensions.width, 2752);
    assert.equal(upStill.dimensions.ok, true);

    // 3. Spillover profile suggestion when default account has only 5 credits (< 12 needed)
    const lowPlan = await orchestrator.flowPlanClips({ slug: "zt-e034", checkLiveBalance: true });
    assert.equal(lowPlan.ok, false);
    assert.equal(lowPlan.reason, "insufficient_account_credits");
    assert.equal(lowPlan.suggestedProfiles[0].profile, "pro-2");
    assert.match(lowPlan.spilloverHint, /pro-2/);

    // 4. Restore credits, generate clip, then use flow_plan_extend -> flow_extend_clip seamlessly
    driver.credits = 500;
    const okPlan = await orchestrator.flowPlanClips({ slug: "zt-e034", checkLiveBalance: true });
    await orchestrator.flowGenerateClips({ slug: "zt-e034", confirm_token: okPlan.confirm_token, waitMs: 5000 });

    const extPlan = await orchestrator.flowPlanExtend({ slug: "zt-e034", shotId: "s01", durationSec: 5, checkLiveBalance: true });
    assert.equal(extPlan.ok, true);
    assert.equal(extPlan.plannedCredits, 15);
    const extRun = await orchestrator.flowExtendClip({
      slug: "zt-e034",
      shotId: "s01",
      prompt: "Clouds drift over valley",
      confirm_token: extPlan.confirm_token,
      durationSec: 5,
      waitMs: 5000,
    });
    assert.equal(extRun.job.status, "completed");

    // 5. Batch import-all & validated Drive push CLI helpers
    const importDry = runImportBridgeBatch({ slug: "zt-e034", repoRoot: fakeRepo, dryRun: true });
    assert.equal(importDry.ok, true);
    assert.equal(importDry.importedCount, 1);

    const spawned = [];
    const pushRes = await runValidatedDrivePush({
      slug: "zt-e034",
      driveSeries: "zhong-tian-qu-qi",
      drivePath: "第034集/製作檔/zt-e034",
      repoRoot: fakeRepo,
      orchestrator,
      spawnFn: (_bin, args) => {
        spawned.push(args);
        return { status: 0, stdout: "vdrive: pushed OK", stderr: "" };
      },
    });
    assert.equal(pushRes.ok, true);
    assert.ok(spawned[0].includes("push-episode"));
    assert.ok(spawned[0].includes("第034集/製作檔/zt-e034"));
  } finally {
    fs.rmSync(fakeRepo, { recursive: true, force: true });
    fs.rmSync(runtimeHome, { recursive: true, force: true });
  }
});
