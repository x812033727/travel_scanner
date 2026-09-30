import {
  copyFileSync, linkSync, lstatSync, mkdirSync, mkdtempSync, readdirSync,
  realpathSync, renameSync, rmSync,
} from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const SEED = "/opt/mokaair/docs-seed/videos";
const TARGET = "/opt/mokaair/docs/videos";

function statIfPresent(file) {
  try { return lstatSync(file); }
  catch (error) {
    if (error.code === "ENOENT") return null;
    throw error;
  }
}

// Resolve existing ancestors too, so aliases cannot put the output inside its seed.
function realLocation(file) {
  if (statIfPresent(file)) return realpathSync(file);
  const parent = path.dirname(file);
  if (parent === file) throw new Error(`No existing ancestor for docs path: ${file}`);
  return path.join(realLocation(parent), path.basename(file));
}

function contains(parent, child) {
  const relative = path.relative(parent, child);
  return relative === "" || (!path.isAbsolute(relative)
    && relative !== ".." && !relative.startsWith(`..${path.sep}`));
}

function requireDirectory(file) {
  const stat = statIfPresent(file);
  if (!stat?.isDirectory() || stat.isSymbolicLink()) {
    throw new Error(`Expected a real directory: ${file}`);
  }
}

function requireMatchingType(stat, directory, file) {
  if (stat.isSymbolicLink() || !(directory ? stat.isDirectory() : stat.isFile())) {
    throw new Error(`Docs entry has an incompatible type: ${file}`);
  }
}

function copySeed(source, destination) {
  const stat = lstatSync(source);
  if (stat.isFile()) {
    copyFileSync(source, destination);
  } else if (stat.isDirectory()) {
    mkdirSync(destination);
    for (const name of readdirSync(source).sort()) {
      copySeed(path.join(source, name), path.join(destination, name));
    }
  } else {
    throw new Error(`Seed must contain only regular files and directories: ${source}`);
  }
}

/** Refresh image-owned files before the worker starts; preserve all existing video folders. */
export function syncDocs(seedDir = SEED, targetDir = TARGET) {
  const seed = path.resolve(seedDir);
  const target = path.resolve(targetDir);
  requireDirectory(seed);
  if (statIfPresent(target)) requireDirectory(target);
  const sourceRoot = realLocation(seed);
  const targetRoot = realLocation(target);
  if (contains(sourceRoot, targetRoot) || contains(targetRoot, sourceRoot)) {
    throw new Error("Docs seed and target must be separate, non-overlapping directories");
  }
  mkdirSync(targetRoot, { recursive: true });
  // Stage on the same volume: failed copies cannot leave a partial video directory
  // that the next startup would mistake for a worker-owned draft.
  const staging = mkdtempSync(path.join(targetRoot, ".docs-seed-"));
  try {
    for (const name of readdirSync(sourceRoot).sort()) {
      const source = path.join(sourceRoot, name);
      const destination = path.join(targetRoot, name);
      const sourceStat = lstatSync(source);
      const existing = statIfPresent(destination);
      if (!sourceStat.isDirectory() && !sourceStat.isFile()) {
        throw new Error(`Seed must contain only regular files and directories: ${source}`);
      }
      if (existing) requireMatchingType(existing, sourceStat.isDirectory(), destination);
      if (existing && (sourceStat.isDirectory() || name === "lexicon.json")) continue;
      const staged = path.join(staging, name);
      copySeed(source, staged);
      if (name === "lexicon.json" && sourceStat.isFile()) {
        // Publish a missing dictionary without replacing one created concurrently.
        // Staging is on the same volume; cleanup removes only the temporary link.
        try { linkSync(staged, destination); }
        catch (error) {
          if (error.code !== "EEXIST") throw error;
          requireMatchingType(lstatSync(destination), false, destination);
        }
        continue;
      }
      // Only this startup writes before the worker loop. Recheck a folder in
      // case an operator added one while the copy was being prepared.
      if (sourceStat.isDirectory()) {
        const appeared = statIfPresent(destination);
        if (appeared) {
          requireMatchingType(appeared, true, destination);
          continue;
        }
      }
      renameSync(staged, destination);
    }
  } finally {
    rmSync(staging, { recursive: true, force: true });
  }
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  try {
    const args = process.argv.slice(2);
    if (args.length !== 0 && args.length !== 2) {
      throw new Error("Usage: node sync-docs.mjs [seed-directory target-directory]");
    }
    syncDocs(...args);
  } catch (error) {
    console.error(`video-worker: docs sync failed: ${error.message}`);
    process.exitCode = 1;
  }
}
