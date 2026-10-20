// A local concept may use only source-bound, individually inspected MiniMax takes.
// This is a production guard, not an official narration or channel approval.
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";

const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

export function inspectHumanArtReview({ doc, manifest, manifestSha, scriptSha, workdir }) {
  const file = path.join(workdir, "review/local-preview/art-review.json");
  if (!existsSync(file)) return { issues: ["individual human art review is missing"], sha256: null, review: null };
  const bytes = readFileSync(file);
  const review = JSON.parse(bytes.toString("utf8"));
  const issues = [];
  if (review.kind !== "human-art-gate" || review.status !== "PASSED") issues.push("human art review has not passed");
  if (review.video_json_sha256 !== scriptSha) issues.push("human art review belongs to another video.json");
  if (review.keyframes_manifest_sha256 !== manifestSha) issues.push("human art review belongs to another keyframes manifest");
  const scenes = doc.scenes.filter((scene) => scene.template === "shot" && !scene.data?.source);
  if (Object.keys(review.shots ?? {}).length !== scenes.length) issues.push("human art review does not cover every drawn shot");
  for (const scene of scenes) {
    const shot = manifest.shots?.[scene.id];
    const item = review.shots?.[scene.id];
    if (!shot || !item || item.status !== "usable" || item.selected_file !== shot.file
      || item.selected_sha256 !== shot.sha256 || shot.needs_review || shot.judge?.passed !== true) {
      issues.push(`unapproved or changed illustration: ${scene.id}`);
    }
  }
  return { issues, sha256: sha256(bytes), review };
}
