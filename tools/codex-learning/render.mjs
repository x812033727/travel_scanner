import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const catalog = JSON.parse(await fs.readFile(path.join(root, "apps/web/lib/codex-learning/catalog.json"), "utf8"));
for (const slug of [...catalog.filter((row) => row.ready).map((row) => row.slug), "codex-learning-hub"]) {
  const dir = path.join(root, "apps/web/public/guides", slug);
  const entry = catalog.find(row => row.slug === slug);
  if (entry) {
    const svgPath = path.join(dir, "diagram-1.svg");
    const source = await fs.readFile(svgPath, "utf8");
    // Course order lives in the catalog/navigation. The cover must not confuse
    // a permanent article ID with the current reading order or a diagram step.
    const branded = source.replace(/CODEX \/ \d{2}/, "CODEX LEARNING");
    if (branded !== source) await fs.writeFile(svgPath, branded);
  }
  await sharp(path.join(dir, "diagram-1.svg")).jpeg({ quality: 86 }).toFile(path.join(dir, "hero.jpg"));
}
console.log("Rendered original artwork for all ready lessons and hub.");
