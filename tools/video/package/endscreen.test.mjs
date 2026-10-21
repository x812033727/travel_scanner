import assert from "node:assert/strict";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { EXIT, main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { brandingHash } from "../core/branding.mjs";
import { fixtureLexicon, sandbox } from "../core/fixtures/load.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";

test("package uses the approved pinned outro and measured final frames for its Studio handoff", async (t) => {
  const box = sandbox();
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  mkdirSync(box.workdir, { recursive: true });
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  const lexicon = fixtureLexicon();
  const timeline = writeSyntheticNarration(doc, lexicon, box.workdir);
  const pin = {
    schema_version: 1,
    id: "curio-archive-original-candidate-20261020-v1",
    intro: { file: "intro.mp4", sha256: "a".repeat(64), frames: 150 },
    outro: { file: "outro.mp4", sha256: "275475470f1b7b5d93a2948f561d6e300d0406f9a5b2ab17cfb0dfe4bb3f34ee", frames: 630 },
  };
  const hash = brandingHash(pin);
  const totalFrames = 150 + timeline.total_frames + 630;
  writeFileSync(path.join(box.workdir, "branding.json"), JSON.stringify(pin));
  writeFileSync(path.join(box.workdir, "final.mp4"), "approved final cut");
  writeFileSync(path.join(box.workdir, "checks.json"), JSON.stringify({
    ok: true, speech_hash: speechHash(doc, lexicon), narration_sha256: timeline.audio_evidence.narration_sha256,
    visual_hash: visualHash(doc), problems: [], metrics: { frames: totalFrames },
    branding: { hash, id: pin.id, intro_frames: 150, body_frames: timeline.total_frames, outro_frames: 630 },
  }));
  mkdirSync(path.join(box.workdir, "captions"));
  writeFileSync(path.join(box.workdir, "captions", "zh-TW.srt"), "1\n00:00:00,000 --> 00:00:01,000\nzh\n");
  writeFileSync(path.join(box.workdir, "captions", "manifest.json"), JSON.stringify({ speech_hash: speechHash(doc, lexicon), branding_hash: hash, locales: { "zh-TW": { file: "captions/zh-TW.srt" } }, skipped: {} }));
  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir });
  const out = { stdout: "", stderr: "" };
  const ctx = { root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base, stdout: { write: (s) => (out.stdout += s) }, stderr: { write: (s) => (out.stderr += s) }, now: () => new Date("2026-10-20T00:00:00Z") };
  assert.equal(await main(["package", "--slug", box.slug], ctx), EXIT.ok, out.stderr + out.stdout);
  const upload = readFileSync(path.join(box.workdir, "upload", "UPLOAD.md"), "utf8");
  assert.match(upload, /可點片尾（私人上傳後在 Studio 設定）/);
  assert.match(upload, /成片長度減 16 秒/);
  assert.match(upload, /oxEtlA8GWas/);
  assert.equal(JSON.parse(readFileSync(path.join(box.workdir, "upload", "metadata.json"), "utf8")).branding_hash, hash);
});
