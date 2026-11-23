import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { ALL_SHEET, csvCell, everyFrom, INDEX_DIR, INDEX_STATE, indexSheets, linkCell, sheetCsv, sheetName, writeDriveIndex } from "./drive-index.mjs";

const NOW = new Date("2026-11-18T06:00:00Z");
const later = (hours) => new Date(NOW.getTime() + hours * 60 * 60 * 1000);

const row = (slug, extra = {}) => ({
  slug, code: slug.toUpperCase(), topic: "H-歷史懸案", title: `${slug} 標題`, state: "published",
  youtube_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", folder: `AI劇/奇聞檔案局/H-歷史懸案/${slug}`,
  backup_state: "done", bytes: 52_428_800, backed_up_at: "2026-11-17T16:30:00Z",
  drive_folder_url: "https://drive.google.com/drive/folders/1AbCdEfGhIjKlMn", drive_final_url: null, ...extra,
});
const INDEX = {
  path: "AI/備份", generated_at: NOW.toISOString(),
  groups: [
    { key: "curio", name: "奇聞檔案局", rows: [row("h01"), row("h02", { drive_folder_url: null, backup_state: "not_queued", youtube_url: null, state: "ready" })] },
    { key: "tai-nainai", name: "恁祖媽今年18", rows: [row("tai-nainai-e001", { topic: null, code: "第001集" })] },
    { key: "Shorts", name: "Shorts", rows: [row("curio-h01-short", { topic: null })] },
  ],
};

/** The parts of backup.mjs's job the index uses, with a fake rclone that records every call. */
function jobFor({ index = INDEX, now = NOW, fail = false, env = {} } = {}) {
  const base = mkdtempSync(path.join(os.tmpdir(), "drive-index-"));
  const calls = [];
  const uploads = {};
  const job = {
    base, env, now, lines: [], remote: "videobackup", prefix: "",
    client: { index: async () => { if (index instanceof Error) throw index; return index; } },
    rclone: async (args) => {
      calls.push(args);
      if (fail) return { code: 1, stdout: "", stderr: "ERROR : quota exceeded" };
      uploads[args[2]] = readFileSync(args[1], "utf8");
      return { code: 0, stdout: "", stderr: "" };
    },
  };
  return { job, calls, uploads, base };
}

test("cells: quotes, BOM-safe text, no formula from a title, links only for https", () => {
  assert.equal(csvCell("平常"), "平常");
  assert.equal(csvCell('他說 "好"'), '"他說 ""好"""');
  assert.equal(csvCell("a,b"), '"a,b"');
  assert.equal(csvCell(null), "");
  assert.equal(csvCell("=HYPERLINK(\"x\")"), "\"'=HYPERLINK(\"\"x\"\")\"", "a title is never a formula");
  assert.equal(csvCell("-1 度"), "'-1 度");
  assert.equal(linkCell("https://drive.google.com/drive/folders/abc", "開啟"), '"=HYPERLINK(""https://drive.google.com/drive/folders/abc"",""開啟"")"');
  assert.equal(linkCell("javascript:alert(1)", "開啟"), "");
  assert.equal(linkCell('https://x.test/"),evil', "開啟"), "", "a URL that would close the formula is dropped");
  assert.equal(linkCell(null, "開啟"), "");
  assert.equal(sheetName("奇聞/檔案:局"), "奇聞_檔案_局");
  assert.equal(sheetName("  "), "其他");
});

test("sheets: 全部 first, one per show in the site's order, each a UTF-8 CSV with a BOM", () => {
  const sheets = indexSheets(INDEX);
  assert.deepEqual(sheets.map((sheet) => sheet.name), [ALL_SHEET, "奇聞檔案局", "恁祖媽今年18", "Shorts"]);
  const all = sheets[0].csv;
  assert.ok(all.startsWith("﻿系列,代碼,分類,標題,狀態,YouTube,雲端資料夾,成片,備份,大小 (MB),備份時間,資料夾,slug\r\n"));
  assert.equal(all.trim().split("\r\n").length, 1 + 4, "a header and every video");
  const lines = sheets[1].csv.trim().split("\r\n");
  assert.equal(lines.length, 3);
  assert.match(lines[1], /^奇聞檔案局,H01,H-歷史懸案,h01 標題,已上架,"=HYPERLINK\(""https:\/\/www\.youtube\.com/);
  assert.match(lines[1], /=HYPERLINK\(""https:\/\/drive\.google\.com\/drive\/folders\/1AbCdEfGhIjKlMn"",""開啟""\)/);
  assert.match(lines[1], /,已備份,50\.0,2026-11-18 00:30,AI劇\/奇聞檔案局\/H-歷史懸案\/h01,h01$/, "size in MB and Taipei time");
  assert.match(lines[2], /,可上傳,,,,未排入,/, "no links, ready, not queued");
  assert.equal(sheetCsv([]).trim(), sheetCsv([]).trim().split("\r\n")[0]);
  // Two groups with one name do not overwrite each other.
  const twins = indexSheets({ groups: [{ key: "a", name: "同名", rows: [] }, { key: "b", name: "同名", rows: [] }] });
  assert.deepEqual(twins.map((sheet) => sheet.name), [ALL_SHEET, "同名", "同名-b"]);
});

test("a round uploads every sheet as a Google Sheet into _總表, updating the one already there", async () => {
  const { job, calls, uploads, base } = jobFor({ env: {} });
  const result = await writeDriveIndex(job);
  assert.deepEqual(result, { uploaded: 4 });
  assert.deepEqual(calls.map((args) => args[2]), ["videobackup:_總表/全部.csv", "videobackup:_總表/奇聞檔案局.csv", "videobackup:_總表/恁祖媽今年18.csv", "videobackup:_總表/Shorts.csv"]);
  for (const args of calls) {
    assert.equal(args[0], "copyto");
    assert.deepEqual(args.slice(3, 7), ["--drive-import-formats", "csv", "--drive-export-formats", "csv"], "stored as a sheet, matched as .csv next time");
  }
  assert.ok(uploads["videobackup:_總表/奇聞檔案局.csv"].includes("h02 標題"));
  assert.ok(!existsSync(path.join(base, INDEX_DIR)), "the local CSVs go");
  assert.deepEqual(job.lines, [], "a success is not a log line: the deploy check reads unknown backup lines as failures");
  const state = JSON.parse(readFileSync(path.join(base, INDEX_STATE), "utf8"));
  assert.deepEqual([state.at, state.sheets, state.videos, state.folder], [NOW.toISOString(), 4, 4, "_總表"]);

  // Within the day nothing is read or sent; after it, unchanged rows send nothing either.
  job.now = later(5);
  assert.deepEqual(await writeDriveIndex(job), { skipped: "recent" });
  job.now = later(25);
  assert.deepEqual(await writeDriveIndex(job), { skipped: "unchanged" });
  assert.equal(calls.length, 4);
  // Changed rows a day after that are uploaded again, under the configured path.
  job.now = later(50);
  job.prefix = "AI/備份";
  job.client.index = async () => ({ ...INDEX, groups: [INDEX.groups[0]] });
  assert.deepEqual(await writeDriveIndex(job), { uploaded: 2 });
  assert.equal(calls.at(-1)[2], "videobackup:AI/備份/_總表/奇聞檔案局.csv");
});

test("a site or upload failure is one line and the next round tries again; 0 hours turns it off", async () => {
  const site = jobFor({ index: new Error("HTTP 502") });
  assert.deepEqual(await writeDriveIndex(site.job), { skipped: "site" });
  assert.match(site.job.lines.at(-1), /could not be read from the site \(HTTP 502\)/);
  assert.ok(!existsSync(path.join(site.base, INDEX_STATE)), "nothing recorded, so the next round tries");

  const upload = jobFor({ fail: true });
  assert.deepEqual(await writeDriveIndex(upload.job), { skipped: "upload" });
  assert.match(upload.job.lines.at(-1), /sheet 全部 could not be uploaded \(ERROR : quota exceeded\)/);
  assert.ok(!existsSync(path.join(upload.base, INDEX_STATE)));
  assert.ok(!existsSync(path.join(upload.base, INDEX_DIR)));

  const off = jobFor({ env: { VIDEO_BACKUP_INDEX_HOURS: "0" } });
  assert.deepEqual(await writeDriveIndex(off.job), { skipped: "off" });
  assert.equal(off.calls.length, 0);
  assert.equal(everyFrom({}), 24 * 60 * 60 * 1000);
  assert.equal(everyFrom({ VIDEO_BACKUP_INDEX_HOURS: "6" }), 6 * 60 * 60 * 1000);
  assert.equal(everyFrom({ VIDEO_BACKUP_INDEX_HOURS: "soon" }), 24 * 60 * 60 * 1000);

  // A state file that cannot be read is treated as no index yet.
  const broken = jobFor();
  writeFileSync(path.join(broken.base, INDEX_STATE), "{not json");
  assert.deepEqual(await writeDriveIndex(broken.job), { uploaded: 4 });
});
