// Timeline for build.py: start and length of every scene by the lint estimate (tools/video/core/timeline.mjs).
//   node tl.mjs <video.json>  ->  {"total": seconds, "scenes": {"s01": [start, seconds], ...}}
// The original lived in the writer's session scratch and was not moved with build.py; rebuilt 2026-10-31.
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../../../../..");
const { estimateTimeline } = await import(pathToFileURL(path.join(root, "tools/video/core/timeline.mjs")).href);
const t = estimateTimeline(JSON.parse(readFileSync(process.argv[2], "utf8")));
const sec = (f) => f / t.fps;
console.log(JSON.stringify({ total: sec(t.total_frames), scenes: Object.fromEntries(t.scenes.map((s) => [s.id, [sec(s.start_frame), sec(s.end_frame - s.start_frame)]])) }));
