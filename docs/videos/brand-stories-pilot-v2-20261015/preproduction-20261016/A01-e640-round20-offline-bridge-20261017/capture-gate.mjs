#!/usr/bin/env node
// Summarize an already exported, sanitized A01 read-only receipt. Never writes.
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const NEW_LEXICON_SHA256 = 'e6403c824aac13b4c0a1ae737e8a597a8bf60c353e9faf0cc4915c3214114a30';
const SHA = /^[a-f0-9]{64}$/u;
const fixed = Object.freeze({ production_status: 'HOLD', installation_allowed: false,
  paid_work_allowed: false, owner_approval_verified: false,
  exclusive_writer_window_verified: false, complete_81_snapshot_verified: false });

export function inspectCaptureSummary(receipt, receiptSha256 = null) {
  const report = { schema_version: 1, kind: 'a01_e640_round20_capture_gate',
    result: 'REJECTED', receipt_sha256: receiptSha256, reasons: [], ...fixed };
  if (receipt?.schema_version !== 1 || receipt?.kind !== 'a01_read_only_capture_summary'
    || receipt?.production_status !== 'HOLD'
    || !SHA.test(receipt?.archive?.tar_sha256 ?? '')
    || !Number.isSafeInteger(receipt?.chain?.links)
    || !SHA.test(receipt?.chain?.captured_lexicon_sha256 ?? '')
    || !Number.isSafeInteger(receipt?.host?.controls_absent_count)
    || !Number.isSafeInteger(receipt?.readback?.stage_job_status_counts?.uncertain)) {
    report.reasons.push('INVALID_SANITIZED_CAPTURE_RECEIPT');
    return report;
  }
  if (receipt.chain.captured_lexicon_sha256 !== NEW_LEXICON_SHA256)
    report.reasons.push('LEXICON_NOT_E640_CANDIDATE');
  if (receipt.chain.links !== 81) report.reasons.push('NO_VERIFIED_81_EVENT');
  if (receipt.host.controls_absent_count > 0)
    report.reasons.push('CAPTURED_CONTROLS_ABSENT');
  if (receipt.readback.stage_job_status_counts.uncertain > 0)
    report.reasons.push('UNCERTAIN_STAGE_JOB');
  if (receipt.chain.result !== 'LOCAL_81_EVENT_TRANSITION_PASS')
    report.reasons.push('AUDIT_SOURCE_NOT_REBASELINED');
  // A complete, separately captured 81-link source and live writer exclusion
  // are not represented by this summary, even if these visible counts clear.
  if (report.reasons.length === 0) report.reasons.push('SUMMARY_IS_NOT_FULL_81_EXPORT');
  return report;
}

function localReceipt(file) {
  if (typeof file !== 'string' || !path.isAbsolute(file)
    || file.startsWith('\\\\') || file.startsWith('//')) throw Error('ABSOLUTE_LOCAL_FILE_REQUIRED');
  const stat = fs.lstatSync(file);
  if (!stat.isFile() || stat.isSymbolicLink() || stat.size > 1_048_576)
    throw Error('UNSAFE_LOCAL_FILE');
  const bytes = fs.readFileSync(file);
  return { receipt: JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/u, '')),
    sha256: createHash('sha256').update(bytes).digest('hex') };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const args = process.argv.slice(2);
  let report;
  try {
    if (args.length !== 2 || args[0] !== '--receipt') throw Error('READ_ONLY_RECEIPT_ARGUMENT_REQUIRED');
    const { receipt, sha256 } = localReceipt(args[1]);
    report = inspectCaptureSummary(receipt, sha256);
  } catch (error) {
    report = { schema_version: 1, kind: 'a01_e640_round20_capture_gate',
      result: 'REJECTED', receipt_sha256: null,
      reasons: [error.message ?? 'LOCAL_RECEIPT_READ_ERROR'], ...fixed };
  }
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  process.exitCode = 1;
}
