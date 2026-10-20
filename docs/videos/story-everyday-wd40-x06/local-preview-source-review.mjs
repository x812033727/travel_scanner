// Carry original source/blind review through a separately signed visual-only delta.
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";

const OLD_SCRIPT = "4c9215b06364b3fb96cd9249054c6e7c15de381b4e8717a39a11fb9ad62bf1ba";
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
  if (receipt.old_video_json_sha256 !== OLD_SCRIPT || receipt.video_json_sha256 !== scriptSha) {
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
  return { issues, sha256: hash(bytes), receipt };
}
