// The language batch review-push sends is the one YouTube sync reads (docs/videos/APPROVED-LANGUAGE-PACKAGE.md):
// apps/api/tests/test_video_youtube_language_contract.py feeds the copy kept in
// apps/api/tests/fixtures/video_language_contract/ to the real consumer, so that copy must be
// what the producer sends now. LANGUAGE_CONTRACT_WRITE=1 writes it again.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import { CONTRACT_CASES, emitContract, readContract, writeContract } from "./language-contract.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const AGAIN = "LANGUAGE_CONTRACT_WRITE=1 node --test tools/video/review/language-contract.test.mjs, review the diff, then cd apps/api && uv run pytest tests/test_video_youtube_language_contract.py";

test("the language contract the API tests read is what package and review-push send now", async () => {
  const emitted = await emitContract();
  if (process.env.LANGUAGE_CONTRACT_WRITE === "1") writeContract(emitted);
  const committed = readContract();
  assert.deepEqual(Object.keys(committed), Object.keys(CONTRACT_CASES).sort(), `the committed cases are not the emitted ones; run ${AGAIN}`);
  for (const [name, { record, files }] of Object.entries(emitted)) {
    // What the producer sends now is "actual", the committed copy "expected", as in a diff of a write.
    assert.equal(record, committed[name].record, `${name}/case.json is not what review-push sends now; run ${AGAIN}`);
    assert.deepEqual([...files.keys()], [...committed[name].files.keys()], `${name}'s stored files are not the ones sent now; run ${AGAIN}`);
    for (const [hash, bytes] of files) {
      assert.equal(sha(bytes), hash);
      assert.ok(committed[name].files.get(hash)?.equals(bytes), `${name}/files/${hash} differs; run ${AGAIN}`);
    }
    // What the consumer is fed: the newest review is the batch, approved (on arrival, or by the
    // owner once a dub track is up), and its proof is the manifest the review's content hash names.
    const { reviews } = JSON.parse(record);
    const [batch] = reviews;
    assert.equal(batch.gate, "languages");
    assert.equal(batch.status, "approved");
    const roles = batch.files.map((file) => file.role);
    assert.ok(roles.includes("metadata") && roles.at(-1) === "languages_manifest", roles.join(", "));
    const manifest = JSON.parse(files.get(batch.content_sha256));
    assert.equal(batch.files.at(-1).sha256, batch.content_sha256);
    assert.deepEqual(manifest.files, batch.files.slice(0, -1));
    assert.deepEqual(manifest.locales, batch.payload.locales);
    const publish = reviews.find((row) => row.gate === "publish");
    assert.deepEqual(manifest.source.publish, { review_id: publish.id, content_sha256: publish.content_sha256 });
    assert.ok(publish.created_at < batch.created_at, "the batch follows the confirmation it names");
  }
});
