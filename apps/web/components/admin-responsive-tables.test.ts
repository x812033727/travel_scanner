import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

/**
 * Under 768px .admin-responsive-table turns every cell into a two-column grid whose
 * left column is `td::before { content: attr(data-label) }`, and hides the thead. A
 * table that takes the class without labelling its cells therefore renders as a
 * stack of right-aligned values with ~93px of blank space beside each one and no
 * column name anywhere — which is how nine admin tables shipped.
 *
 * This reads the source rather than rendering: the panels need sessions, API stubs
 * and filter state to reach their tables, and the rule being protected is a static
 * property of the markup.
 */
const COMPONENTS = import.meta.dirname;
const TABLE = /<table\b[^>]*>/g;
const ROW = /<tr\b[\s\S]*?<\/tr>/g;
const UNLABELLED_CELL = /<td\b(?![^>]*data-label)(?![^>]*colSpan)[^>]*>/g;

function responsiveTables(source: string) {
  const found: string[] = [];
  for (const match of source.matchAll(TABLE)) {
    if (!match[0].includes("admin-responsive-table")) continue;
    const end = source.indexOf("</table>", match.index + match[0].length);
    found.push(source.slice(match.index, end === -1 ? undefined : end));
  }
  return found;
}

const files = readdirSync(COMPONENTS)
  .filter((name) => name.startsWith("admin") && name.endsWith(".tsx") && !name.includes(".test."))
  .map((name) => ({ name, source: readFileSync(join(COMPONENTS, name), "utf8") }))
  .filter((file) => responsiveTables(file.source).length > 0);

describe("admin tables on a phone", () => {
  it("finds the tables it is meant to be checking", () => {
    // Without this the sweep below could pass by checking nothing at all.
    expect(files.length).toBeGreaterThanOrEqual(8);
  });

  it.each(files.map((file) => file.name))("%s labels every cell it cards up", (name) => {
    const file = files.find((entry) => entry.name === name)!;
    const missing: string[] = [];
    for (const table of responsiveTables(file.source)) {
      for (const row of table.matchAll(ROW)) {
        for (const cell of row[0].matchAll(UNLABELLED_CELL)) {
          missing.push(cell[0].slice(0, 60));
        }
      }
    }
    expect(missing, `${name} has cells with no column name on a phone`).toEqual([]);
  });
});
