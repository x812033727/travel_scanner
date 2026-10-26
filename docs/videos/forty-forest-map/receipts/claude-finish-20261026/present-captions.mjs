// Body-timed SRT -> presented SRT: every cue that starts at or after the intro (body frame 682)
// moves 5 s later. Cues never straddle the intro (Codex checked linesAcrossIntro).
import { readFileSync, writeFileSync } from "node:fs";
const [input, output] = process.argv.slice(2);
const AT = 682 * 1000 / 30, SHIFT = 5000;
const ms = (t) => { const [h, m, s] = t.replace(",", ".").split(":"); return Math.round((+h * 3600 + +m * 60 + +s) * 1000); };
const fmt = (v) => { const h = Math.floor(v / 3600000), m = Math.floor(v / 60000) % 60, s = Math.floor(v / 1000) % 60, x = v % 1000; return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")},${String(x).padStart(3, "0")}`; };
const blocks = readFileSync(input, "utf8").trim().split(/\n\s*\n/).map((b) => {
  const rows = b.split("\n"); const [a, z] = rows[1].split(" --> ").map(ms);
  if (a < AT - 1 && z > AT + 1) throw new Error(`cue ${rows[0]} straddles the intro`);
  const d = a >= AT - 1 ? SHIFT : 0;
  return [rows[0], `${fmt(a + d)} --> ${fmt(z + d)}`, ...rows.slice(2)].join("\n");
});
writeFileSync(output, `${blocks.join("\n\n")}\n`);
