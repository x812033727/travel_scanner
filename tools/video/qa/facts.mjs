// The facts check: nothing the last fact-check round marked NOT FOUND is still cited by a scene.
//
// A fact-checker writes docs/videos/<slug>/verify-<round>.md with a claim table whose verdict
// column reads CONFIRMED, CHANGED, NOT FOUND or OUT OF SCOPE (the verifier prompts in
// tools/video/automation/prompts.mjs and .agents/skills/youtube-video). NOT FOUND means the number
// or the sentence was dropped, so its claim id (claims.md's c-numbers, which the scenes list in
// `claims`) must no longer be cited anywhere. The table may use ASCII or full-width bars, and the
// id column may read 12, c12 or #12: all are compared without the prefix.
export const VERIFY_FILE = /^verify-(\d+)\.md$/;
// The verdict as the prompts spell it, upper-case: a claim that begins "Not found on the page" is a claim.
const NOT_FOUND = /^NOT[ _]FOUND\b/;
const SEPARATOR = /^[\s:|｜-]+$/;

/** The report of the last round among some file names, or null when there was no round. */
export function lastVerifyReport(names) {
  let best = null;
  for (const name of names) {
    const match = VERIFY_FILE.exec(name);
    if (match && (!best || Number(match[1]) > best.round)) best = { name, round: Number(match[1]) };
  }
  return best;
}

/** A claim id as both sides are compared: lower-case, without a leading # or c. */
export const normalizeClaimId = (id) => String(id ?? "").trim().replace(/^[#`*\s]+|[`*\s]+$/g, "").toLowerCase().replace(/^c(?=\d)/, "");

/** The rows of a report's claim table whose verdict is NOT FOUND: [{ id, cells }]. */
export function notFoundClaims(markdown) {
  const rows = [];
  for (const line of String(markdown).replace(/\r\n/g, "\n").split("\n")) {
    if (!/[|｜]/.test(line) || SEPARATOR.test(line)) continue;
    const cells = line.split(/[|｜]/).map((cell) => cell.trim());
    if (cells[0] === "") cells.shift();
    if (cells.at(-1) === "") cells.pop();
    if (cells.length < 3 || !cells.some((cell) => NOT_FOUND.test(cell))) continue;
    const id = normalizeClaimId(cells[0]);
    if (id) rows.push({ id, cells });
  }
  return rows;
}

/** The claim ids every scene cites, by scene id. */
export function citedClaims(doc) {
  const cited = new Map();
  for (const scene of doc.scenes ?? []) {
    for (const claim of scene.claims ?? []) {
      const id = normalizeClaimId(claim);
      if (!cited.has(id)) cited.set(id, []);
      cited.get(id).push(scene.id);
    }
  }
  return cited;
}

/** The facts item's verdict: { ok, detail }. `report` is { name, markdown } or null. */
export function factsChecks({ report, doc }) {
  if (!report) return { ok: false, detail: "no verify-*.md beside video.json: the script has not been fact-checked" };
  const dropped = notFoundClaims(report.markdown);
  if (!dropped.length) return { ok: true, detail: `${report.name} marks no claim NOT FOUND` };
  const cited = citedClaims(doc);
  const still = dropped.filter((row) => cited.has(row.id));
  if (!still.length) return { ok: true, detail: `${report.name} marks ${dropped.length} claims NOT FOUND (${dropped.map((row) => row.id).join(", ")}); no scene cites them` };
  return { ok: false, detail: still.map((row) => `claim ${row.id} was NOT FOUND in ${report.name} but ${cited.get(row.id).join(", ")} still cites it`).join("; ") };
}
