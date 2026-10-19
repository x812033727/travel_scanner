# A01 fresh read-only capture — always HOLD

The older A01-host-export-candidate rejects anything other than 80 audit links.
This command captures the current A01 files and at least 104 event directories
without changing the host. It is an evidence collection tool, not an importer,
script-review receipt, deployment, or permission to make a paid call.

From a local Windows PowerShell, with Node 24 and a saved PuTTY session named
hostinger2 that works with plink -batch, run one command. The output path must
be absolute, new, and outside every Git checkout:

    node "C:/Users/x8120/.codex/worktrees/a01-readonly-capture/travel_scanㄐ/tools/video/a01-capture/capture.mjs" --out "C:/Users/x8120/AppData/Local/Temp/a01-fresh-20261019-03"

The command invokes only fixed read-only remote commands through
C:/Program Files/PuTTY/plink.exe with -batch -T -load hostinger2 -l root.
It does not use the login state of an already-open PuTTY terminal; the saved
session itself must authenticate noninteractively. It does not accept a
password, key, alternate slug, host command or write option. If PuTTY prompts
for a password or host key, batch mode fails. Keep the output directory local
and private; share only its path with the reviewer, never paste its contents
or a password into chat.

The new directory contains a01-source.tar (binary-safe stream of exact
A01 source files, six chapters, the A01 story-lexicon snapshot and every audit event), before/after
host-state-*.txt, db-*.json, budget-*.json, and capture-report.json with
hashes and HOLD reasons. Host state also records the running video-worker image ID,
release Git SHA, `tools/video` Git tree SHA and an inventory digest of the full
in-container `tools/video` file tree. The database query uses BEGIN TRANSACTION READ ONLY;
the budget CLI omits action and apply flags. The script records global
queued, running and uncertain stage jobs, plus live media jobs, even from
other videos. An unresolved A01 stage job also holds the gate if the global
projection misses it. If a remote step or
comparison fails, it leaves the partial directory and a HOLD report; use a
new path for a subsequent capture.

`capture_complete: true` and `files_captured=7/7` mean all seven outputs were
collected and parsed. `issues=GLOBAL_JOB_ACTIVE` or `A01_STAGE_UNRESOLVED` can leave the operational
gate on HOLD. `capture_consistent: true` means the two sampled host, database and budget
views match and the narrow audit, STOP, job and budget checks pass. It cannot prove an atomic
snapshot, authentic host origin, complete media enumeration, no locks, formal
fact review or readiness to adopt. An independent reader must verify archive
members and hashes, current deployment, jobs, controls, budget and the exact
104→105 adoption plan before any host write. The A01 STOP stays in place.

After a complete capture, verify its archive locally without extracting it:

    node "C:/Users/x8120/.codex/worktrees/a01-readonly-capture/travel_scanㄐ/tools/video/a01-capture/verify-archive.mjs" --capture "C:/Users/x8120/AppData/Local/Temp/a01-fresh-20261019-03"

The verifier checks each tar header, checksum, member type and path, rejects
links, traversal, duplicate names, unexpected files and PAX extensions, and
streams each file through SHA-256. It also checks the seven captured output
files against `capture-report.json` and rejects linked destination ancestors.
Every source, A01 story-lexicon snapshot and audit file must match both
host-state inventories. Manual revision receipts must match the exact hash in
their audit index; the exact legacy install receipt is pinned separately. The
running worker image and runtime tree pins must be complete and internally
consistent. GNU tar's default long-name extension is supported. A valid
archive remains a HOLD until the independent story, job, budget and adoption
checks finish. The verifier reads local files only and writes nothing.

Local synthetic checks:

    node --test tools/video/a01-capture/capture.test.mjs
    node --test tools/video/a01-capture/verify-archive.test.mjs
    node tools/video/a01-capture/capture.mjs --help
