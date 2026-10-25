// packageRefusal (flow.mjs): whether a dub asked for again could be packaged, read from the cut on
// disk the way package/cli.mjs reads it. A drama's cut (a brand story is one) is bound to its clips.
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { dramaFixture } from "../core/fixtures/load.mjs";
import { lookHash, mixHash, sfxHash, subtitlesHash } from "../core/drama.mjs";
import { ARTIFACTS } from "../core/state.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { packageRefusal } from "./flow.mjs";

const STALE = "成片不在了，或它的檢查記錄比現在的腳本和畫面舊";

function put(dir, relative, value) {
  const file = path.join(dir, relative);
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, typeof value === "string" ? value : JSON.stringify(value));
}

test("a drama's cut with its clips is not called stale, and one without its clips manifest is", () => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "package-refusal-"));
  try {
    const doc = dramaFixture();
    const lexicon = { terms: {} };
    const checks = {
      ok: true, speech_hash: speechHash(doc, lexicon), visual_hash: visualHash(doc),
      look_hash: lookHash(doc), subtitles_hash: subtitlesHash(doc), mix_hash: mixHash(doc), clips_hash: "c1",
      ...(doc.sfx ? { sfx_hash: sfxHash(doc) } : {}),
    };
    put(dir, ARTIFACTS.checks, checks);
    put(dir, ARTIFACTS.timeline, { total_frames: 900 });
    put(dir, ARTIFACTS.video, "cut");
    put(dir, ARTIFACTS.clips, { clips_hash: "c1" });
    // The cut is current; what is left is the narration evidence, which this fixture does not have.
    assert.notEqual(packageRefusal({ doc, lexicon }, dir), STALE);
    put(dir, ARTIFACTS.clips, { clips_hash: "c2" });
    assert.equal(packageRefusal({ doc, lexicon }, dir), STALE, "clips changed since the cut");
    rmSync(path.join(dir, ARTIFACTS.clips));
    assert.equal(packageRefusal({ doc, lexicon }, dir), STALE, "no clips manifest to compare");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
