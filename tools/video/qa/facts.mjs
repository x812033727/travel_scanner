// The facts check: nothing the last fact-check round marked NOT FOUND is still cited by a scene.
//
// A fact-checker writes docs/videos/<slug>/verify-<round>.md with a claim table whose verdict
// column reads CONFIRMED, CHANGED, NOT FOUND or OUT OF SCOPE (the verifier prompts in
// tools/video/automation/prompts.mjs and .agents/skills/youtube-video). NOT FOUND means the number
// or the sentence was dropped, so its claim id (claims.md's c-numbers, which the scenes list in
// `claims`) must no longer be cited anywhere. The table may use ASCII or full-width bars, and the
// id column may read 12, c12 or #12: numeric ids require an explicit claim-id header,
// while a c-number identifies itself. Ordinary verifier row numbers are not claim ids.
export const VERIFY_FILE = /^verify-(\d+)\.md$/;
// The verdict as the prompts spell it, upper-case: a claim that begins "Not found on the page" is a claim.
const NOT_FOUND = /^NOT[ _]FOUND\b/;
const SEPARATOR = /^[\s:|｜-]+$/;
const CLAIM_ID_HEADER = /^(?:claim[ _-]*(?:id|number|no\.?|#)|(?:主張|聲明|事實)\s*(?:編號|id))$/i;
const VERDICT_HEADER = /^(?:verdict|result|判定|結論|結果)$/i;

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
  let claimColumn = null;
  for (const line of String(markdown).replace(/\r\n/g, "\n").split("\n")) {
    if (!/[|｜]/.test(line)) { claimColumn = null; continue; }
    if (SEPARATOR.test(line)) continue;
    const cells = line.split(/[|｜]/).map((cell) => cell.trim());
    if (cells[0] === "") cells.shift();
    if (cells.at(-1) === "") cells.pop();
    if (cells.length < 3) continue;
    const notFound = cells.some((cell) => NOT_FOUND.test(cell));
    const header = cells.findIndex((cell) => CLAIM_ID_HEADER.test(cell));
    if (!notFound) {
      if (header !== -1) claimColumn = header;
      else if (cells.some((cell) => VERDICT_HEADER.test(cell))) claimColumn = null;
      continue;
    }
    const raw = String(cells[claimColumn ?? 0] ?? "").trim().replace(/^[#`*\s]+|[`*\s]+$/g, "");
    if (claimColumn === null && !/^c\d[\w-]*$/i.test(raw)) continue;
    const id = normalizeClaimId(raw);
    if (/^\d[\w-]*$/.test(id)) rows.push({ id, cells });
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
