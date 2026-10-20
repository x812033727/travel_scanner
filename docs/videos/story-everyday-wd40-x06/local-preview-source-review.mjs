// Carry original source/blind review through a separately signed visual-only delta.
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";

const OLD_SCRIPT = "4c9215b06364b3fb96cd9249054c6e7c15de381b4e8717a39a11fb9ad62bf1ba";
const FIRST_VISUAL_SCRIPT = "907f8e3ff45f3edf0bbed64a54216c761696e8e954d51c315a8a228069e204d1";
const SECOND_VISUAL_RECEIPT = "b0f8d00eada61391a518dc8c952619b70e7100df91233035e21c73b182411c56";
const SECOND_VISUAL_PROPOSAL = "6ddb574d1bcb16c6c89703d375605882bf11f93390bf85e20d9f028064cbe6fc";
const SECOND_VISUAL_SCRIPT = "d1ac6f93e15396813dda6ac2d76028f6539be2d746d647d1fd44e4790dd5d0c5";
const THIRD_VISUAL_SCRIPT = "931efad38297c832fd11a2aedfc12cc2ef5c61373e36632a1fcd916dbdf0fc68";
const THIRD_VISUAL_RECEIPT = "5ab635105dc384bbec80b4f32346697247c0ebdcdcff539391674f7b436c84a7";
const THIRD_VISUAL_PROPOSAL = "a7a1033bffe6293a53cf8d4911f3a2d27724bfd94cbb337f8b70a689d0b94239";
const PRIOR = {
  "source-audit-final.md": ["prior_source_review_sha256", "2b386249fdb86d2747ef0d25f36f621da109a0890e98d2dd5ef5c909b724599c"],
  "blind-a-final.md": ["prior_blind_a_sha256", "553c6f7bc007f36923901b675ff59844a74e5d027e1ae58eebfb10abcf8727c1"],
  "blind-b-4c9215.md": ["prior_blind_b_sha256", "4482bb7c207e6d4dbf8f379adebde6d77a85e6ccb1edd2bfaa21b9f177f0c7c9"],
};
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");

export function inspectIndependentVisualReview({ dir, scriptSha }) {
  const issues = [];
  const reviewsDir = path.join(dir, "reviews");
  const receiptFile = path.join(reviewsDir, "visual-change-independent.json");
  if (!existsSync(receiptFile)) return { issues: ["independent visual-change review is missing"], sha256: null, receipt: null };
  const bytes = readFileSync(receiptFile);
  const receipt = JSON.parse(bytes.toString("utf8"));
  if (receipt.kind !== "independent-visual-delta-review" || receipt.status !== "PASS"
    || receipt.reviewer !== "/root" || receipt.authorizes_final_art_or_publication !== false) {
    issues.push("visual-change receipt is not an independent prompt-only PASS");
  }
  if (receipt.old_video_json_sha256 !== OLD_SCRIPT || receipt.video_json_sha256 !== FIRST_VISUAL_SCRIPT) {
    issues.push("visual-change receipt belongs to another video.json");
  }
  const note = path.join(reviewsDir, "visual-prompt-delta.md");
  if (!existsSync(note) || hash(readFileSync(note)) !== receipt.delta_note_sha256) {
    issues.push("visual-change receipt does not bind the current delta note");
  }
  for (const [name, [field, expected]] of Object.entries(PRIOR)) {
    const file = path.join(reviewsDir, name);
    const contents = existsSync(file) ? readFileSync(file) : null;
    if (!contents || hash(contents) !== expected || receipt[field] !== expected
      || !contents.toString("utf8").includes(OLD_SCRIPT)) {
      issues.push(`original source/blind receipt changed: ${name}`);
    }
  }
  if (scriptSha === FIRST_VISUAL_SCRIPT) return { issues, sha256: hash(bytes), receipt };

  const nextFile = path.join(reviewsDir, "visual-v2-independent.json");
  if (!existsSync(nextFile)) return { issues: [...issues, "independent visual-v2 review is missing"], sha256: null, receipt: null };
  const nextBytes = readFileSync(nextFile);
  const next = JSON.parse(nextBytes.toString("utf8"));
  if (hash(nextBytes) !== SECOND_VISUAL_RECEIPT || next.kind !== "independent-visual-delta-review"
    || next.status !== "PASS" || next.reviewer !== "/root"
    || next.authorizes_final_art_or_publication !== false) {
    issues.push("visual-v2 receipt is not the frozen independent prompt-only PASS");
  }
  if (next.old_video_json_sha256 !== FIRST_VISUAL_SCRIPT || next.video_json_sha256 !== SECOND_VISUAL_SCRIPT) {
    issues.push("visual-v2 receipt belongs to another video.json");
  }
  const proposal = path.join(reviewsDir, "visual-v2-offline-proposal.md");
  if (!existsSync(proposal) || hash(readFileSync(proposal)) !== SECOND_VISUAL_PROPOSAL
    || next.offline_proposal_sha256 !== SECOND_VISUAL_PROPOSAL
    || JSON.stringify(next.changed_shot_ids) !== JSON.stringify(["x06-b02-s01", "x06-b02-s02"])) {
    issues.push("visual-v2 receipt does not bind the two-shot offline proposal");
  }
  if (scriptSha === SECOND_VISUAL_SCRIPT) return { issues, sha256: hash(nextBytes), receipt: next };

  const thirdFile = path.join(reviewsDir, "visual-v3-independent.md");
  const thirdProposal = path.join(reviewsDir, "visual-v3-offline-proposal.md");
  if (!existsSync(thirdFile) || !existsSync(thirdProposal)) {
    return { issues: [...issues, "independent visual-v3 review or proposal is missing"], sha256: null, receipt: null };
  }
  const thirdBytes = readFileSync(thirdFile);
  const thirdText = thirdBytes.toString("utf8");
  if (hash(thirdBytes) !== THIRD_VISUAL_RECEIPT
    || hash(readFileSync(thirdProposal)) !== THIRD_VISUAL_PROPOSAL
    || !thirdText.includes("**PASS，僅限離線視覺文字差異。**")
    || ![SECOND_VISUAL_SCRIPT, THIRD_VISUAL_SCRIPT, THIRD_VISUAL_PROPOSAL, "x06-b03-s07", "x06-b03-s12"].every((value) => thirdText.includes(value))) {
    issues.push("visual-v3 review does not bind the frozen two-shot prompt-only proposal");
  }
  if (scriptSha !== THIRD_VISUAL_SCRIPT) issues.push("visual-v3 receipt belongs to another video.json");
  return { issues, sha256: hash(thirdBytes), receipt: { kind: "independent-visual-delta-review", status: "PASS", reviewer: "/root" } };
}
