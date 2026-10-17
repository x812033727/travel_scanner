#!/usr/bin/env node
// Read-only, exact 80-to-81 captured transition inspection. Never releases production.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { verifyPinnedTransition } from './transition.mjs';

export function inspectPinnedSnapshot(options) {
  try {
    const result = verifyPinnedTransition(options);
    return { ...result, inspection: 'EXACT_PINNED_CAPTURE_PASS', release_allowed: false };
  } catch (error) {
    // Do not leak raw chapter/state data or arbitrary parse errors into reports.
    const code = typeof error?.code === 'string' && /^[A-Z][A-Z0-9_]+$/.test(error.code)
      ? error.code : 'PINNED_CAPTURE_INVALID';
    return { inspection: 'HOLD', reason: code, production_status: 'HOLD',
      installation_allowed: false, paid_work_allowed: false, release_allowed: false };
  }
}

export function parseInspectionArgs(args) {
  if (args.length !== 6 || args[0] !== '--before' || args[2] !== '--after' || args[4] !== '--old-lexicon'
    || ![args[1], args[3], args[5]].every(value => typeof value === 'string' && value && !value.startsWith('--'))) {
    throw new Error('usage: --before <local-80-capture> --after <local-81-capture> --old-lexicon <historical-json>');
  }
  return { beforeRoot: path.resolve(args[1]), afterRoot: path.resolve(args[3]), oldLexiconFile: path.resolve(args[5]) };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  let report;
  try { report = inspectPinnedSnapshot(parseInspectionArgs(process.argv.slice(2))); }
  catch { report = { inspection: 'HOLD', reason: 'INSPECTION_ARGUMENTS_INVALID', production_status: 'HOLD',
    installation_allowed: false, paid_work_allowed: false, release_allowed: false }; }
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  process.exitCode = report.inspection === 'EXACT_PINNED_CAPTURE_PASS' ? 0 : 2;
}
