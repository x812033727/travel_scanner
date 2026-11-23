// The daily Drive index (docs/videos/BACKUP.md §每日總表; owner, 2026-11-18): one Google Sheet per
// show, plus 全部, in <path>/_總表/, so whoever opens Drive can see every episode, where it stands
// and a link to its folder and final cut without walking the folders.
//
// The site has every row (GET /video/automation/backup/index, apps/api/app/video_backup/
// admin_status.py drive_index); this file turns them into CSV and uploads each with
// `--drive-import-formats csv`, so Drive stores a Google Sheet, and `--drive-export-formats csv`,
// so the sheet already there reads back as <name>.csv and is updated in place instead of a second
// sheet appearing beside it. It runs at the end of a backup round, at most once every
// INDEX_EVERY_MS, and uploads nothing when the rows did not change. A failure is one line in the
// round's log and is tried again next round; it never holds a video's backup or the tidy.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";

// Beside the work directories; the tidy skips names that start with "_".
export const INDEX_STATE = "_backup-index.json";
export const INDEX_DIR = "_backup-index";
export const INDEX_FOLDER = "_總表";
export const INDEX_EVERY_MS = 24 * 60 * 60 * 1000;
// Hours between two indexes on the host; "0" turns the index off.
export const INDEX_HOURS_ENV = "VIDEO_BACKUP_INDEX_HOURS";
export const ALL_SHEET = "全部";
const COLUMNS = ["系列", "代碼", "分類", "標題", "狀態", "YouTube", "雲端資料夾", "成片", "備份", "大小 (MB)", "備份時間", "資料夾", "slug"];
const STATES = { working: "製作中", ready: "可上傳", published: "已上架", dropped: "已放棄" };
const BACKUPS = {
  done: "已備份", stale: "要補檔", pending: "排隊中", failed: "失敗", blocked_quota: "空間不足",
  partial: "缺檔", not_queued: "未排入", off: "不備份",
};
// What Google Drive for desktop cannot write on the owner's PC (apps/api/app/video_backup/target.py).
const FORBIDDEN = /[<>:"/\\|?*\x00-\x1f\x7f]/g;
const HTTP_URL = /^https:\/\/[^\s"]+$/;

/** One CSV cell: quoted when it must be, and never read as a formula unless it is one of ours. */
export function csvCell(value) {
  let text = value === null || value === undefined ? "" : String(value);
  // A title starting with = + - @ would run as a formula in Sheets.
  if (/^[=+\-@]/.test(text)) text = `'${text}`;
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

/** A clickable cell: a HYPERLINK formula for an https URL, empty for anything else. */
export function linkCell(url, label) {
  if (typeof url !== "string" || !HTTP_URL.test(url)) return "";
  const formula = `=HYPERLINK("${url}","${label}")`;
  return `"${formula.replace(/"/g, '""')}"`;
}

/** A sheet's name as a Drive file name. */
export function sheetName(name) {
  const clean = String(name ?? "").replace(FORBIDDEN, "_").trim();
  return clean || "其他";
}

const megabytes = (bytes) => (typeof bytes === "number" && bytes >= 0 ? (bytes / 1024 ** 2).toFixed(1) : "");
const taipei = (iso) => {
  const when = new Date(String(iso ?? ""));
  if (!Number.isFinite(when.getTime())) return "";
  return new Date(when.getTime() + 8 * 60 * 60 * 1000).toISOString().slice(0, 16).replace("T", " ");
};

/** The CSV of some rows, each with its group's name; UTF-8 with a BOM so Sheets reads the Chinese. */
export function sheetCsv(rows) {
  const lines = [COLUMNS.map(csvCell).join(",")];
  for (const { group, row } of rows) {
    lines.push([
      csvCell(group), csvCell(row.code), csvCell(row.topic), csvCell(row.title), csvCell(STATES[row.state] ?? row.state),
      linkCell(row.youtube_url, "YouTube"), linkCell(row.drive_folder_url, "開啟"), linkCell(row.drive_final_url, "成片"),
      csvCell(BACKUPS[row.backup_state] ?? row.backup_state), csvCell(megabytes(row.bytes)), csvCell(taipei(row.backed_up_at)),
      csvCell(row.folder), csvCell(row.slug),
    ].join(","));
  }
  return `﻿${lines.join("\r\n")}\r\n`;
}

/** The sheets for an index: 全部 first, then one per group in the site's order. */
export function indexSheets(index) {
  const groups = Array.isArray(index?.groups) ? index.groups : [];
  const tagged = (group) => (Array.isArray(group.rows) ? group.rows : []).map((row) => ({ group: group.name, row }));
  const sheets = [{ name: ALL_SHEET, csv: sheetCsv(groups.flatMap(tagged)) }];
  const taken = new Set([ALL_SHEET]);
  for (const group of groups) {
    let name = sheetName(group.name);
    if (taken.has(name)) name = sheetName(`${group.name}-${group.key}`);
    taken.add(name);
    sheets.push({ name, csv: sheetCsv(tagged(group)) });
  }
  return sheets;
}

/** INDEX_EVERY_MS, or the hours VIDEO_BACKUP_INDEX_HOURS names (0 turns the index off). */
export function everyFrom(env = {}) {
  const raw = env?.[INDEX_HOURS_ENV];
  if (raw === undefined || raw === "") return INDEX_EVERY_MS;
  const hours = Number(raw);
  return Number.isFinite(hours) && hours >= 0 ? hours * 60 * 60 * 1000 : INDEX_EVERY_MS;
}

function readState(file) {
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch {
    return {};
  }
}

/**
 * Write the index into <prefix>/_總表/ when a day has passed since the last one; a quiet round
 * returns at once. `job` is backup.mjs's: base, client, rclone, remote, prefix, now, lines.
 */
export async function writeDriveIndex(job, { everyMs = everyFrom(job.env) } = {}) {
  if (everyMs === 0) return { skipped: "off" };
  const stateFile = path.join(job.base, INDEX_STATE);
  const state = readState(stateFile);
  const last = Date.parse(String(state.at ?? ""));
  if (Number.isFinite(last) && job.now.getTime() - last < everyMs) return { skipped: "recent" };
  let index;
  try {
    index = await job.client.index();
  } catch (error) {
    job.lines.push(`backup: the Drive index could not be read from the site (${error.message}); the next round tries again`);
    return { skipped: "site" };
  }
  const sheets = indexSheets(index);
  const hash = createHash("sha256").update(JSON.stringify(sheets)).digest("hex");
  const save = (fields) => writeFileSync(stateFile, `${JSON.stringify({ ...state, ...fields }, null, 2)}\n`);
  if (hash === state.hash) {
    save({ at: job.now.toISOString() });
    return { skipped: "unchanged" };
  }
  const local = path.join(job.base, INDEX_DIR);
  rmSync(local, { recursive: true, force: true });
  mkdirSync(local, { recursive: true });
  const folder = [job.prefix, INDEX_FOLDER].filter(Boolean).join("/");
  try {
    for (const sheet of sheets) {
      const file = path.join(local, `${sheet.name}.csv`);
      writeFileSync(file, sheet.csv);
      const sent = await job.rclone(["copyto", file, `${job.remote}:${folder}/${sheet.name}.csv`, "--drive-import-formats", "csv", "--drive-export-formats", "csv", "--retries", "3"]);
      if (sent.code !== 0) {
        const why = String(sent.stderr || sent.stdout || "").trim().split("\n").at(-1) || `exit ${sent.code}`;
        job.lines.push(`backup: the Drive index sheet ${sheet.name} could not be uploaded (${why}); the next round tries again`);
        return { skipped: "upload" };
      }
    }
  } finally {
    if (existsSync(local)) rmSync(local, { recursive: true, force: true });
  }
  // Recorded in the state file, not the round's log: the deploy check
  // (.agents/skills/deploy/scripts/host-verify.sh) reads an unknown backup line next to a capped
  // exit as a failure, and a daily success is not news. A failure above is a line, as it should be.
  const rows = (index.groups ?? []).reduce((sum, group) => sum + (group.rows?.length ?? 0), 0);
  save({ at: job.now.toISOString(), hash, sheets: sheets.length, videos: rows, folder });
  return { uploaded: sheets.length };
}
