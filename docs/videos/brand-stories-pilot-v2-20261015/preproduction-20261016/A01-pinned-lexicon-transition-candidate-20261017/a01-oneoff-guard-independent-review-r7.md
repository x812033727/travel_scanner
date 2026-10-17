# Independent A01 one-off guard review, r7 — 2026-10-17

## Verdict

**Conditional PASS for the reviewed guard package. No remaining P1 found in
the exact r7 code or disposable fault evidence.** `stop-recovery-guard/SHA256SUMS.txt`
has SHA-256 `6d4993ee445d9441b04be4be2a99dcdd04e35ab09dd9e8abaa6f88867c58b989`.
All listed hashes passed my independent `sha256sum -c`; r7 changed only README
and fault-plan text from r6. The exact code passed 30/30 WSL Linux unit tests,
`bash -n`, and Python compilation. The supplied manifest remains deliberately
unfilled and `fault_test_allowed=false`, so it cannot run on production as-is.

The r5 P1 from Docker's lowercase `error: no such object: <ID>` was fixed in
r6's recovery and normal runner. The parser now accepts only that exact
case-insensitive absence response bound to the inspected full ID. It rejects
another ID and a generic daemon error. R7 retained those code bytes.

## Evidence accepted

- Docker 29.1.3/Compose 2.40.3 one-off semantics: full ID, `oneoff=True`,
  `AutoRemove=true`, `restart=no`; `compose ps --all` includes original and
  one-off. Original lookup uses `oneoff=False`, and created one-off lookup
  independently requires exact name, project/service/phase labels and full ID.
  Receipt: `fault-lab/compose-semantics-20261017.md`.
- Real disposable systemd `Type=exec` MainPID SIGKILL: baseline, missing marker,
  and after-`arm` lifted STOP all killed the labelled one-off before STOP
  readback, with `ExecStopPost=0`; STOP hash/inode remained original. Corrupt
  marker killed the one-off and preserved STOP but correctly left
  `ExecStopPost=1`. Receipts: `fault-lab/sigkill-baseline-pass-20261017.md`,
  `sigkill-missing-marker-pass-20261017.md`,
  `sigkill-lifted-stop-pass-20261017.md`, and
  `sigkill-corrupt-marker-20261017.md`.
- Lifted-STOP Docker daemon restart: both originals persisted `restart=no` and
  remained down, the `AutoRemove` one-off vanished, and the held original STOP
  inode survived. Exact guard restore relinked STOP before any worker restart.
  Receipt: `fault-lab/daemon-restart-pass-20261017.md`.
- Exact r7 **full runner** `fault-test` in a provider-free WSL fixture: supervised
  systemd invocation, synthetic Git/DB/API/budget preflight, pinned original
  IDs and image, all 979 reviewed payload files and six phase-critical hashes,
  one-off copy/identity/marker, then MainPID SIGKILL. Journal showed
  `A01_ONEOFF_PINNED` and `A01_FAULT_TEST_READY`, followed by
  `A01_ONEOFF_STOPPED` before STOP readback. `ExecStopPost=0`, label scan empty,
  STOP hash/inode and original states/policies unchanged. A first synthetic
  checkout attempt failed closed on an untracked `__pycache__`; the fixture
  was corrected without changing candidate code. Raw receipt SHA-256
  `36efa28d6b035aa35a3323c0e80bb354c93b862d10271f5ec9a528f124dcd4a5`:
  `fault-lab/full-runner-fault-test-raw-20261017.txt`.
- Fresh production **read-only** boot inventory at 15:32–15:33 UTC found no
  enabled video Compose/autodeploy starter in systemd, timer, cron, init or
  cloud script paths. The only custom Mokaair enabled unit runs
  `ai_accounts_agent`; `/etc/rc.local` and root user units are absent. Scripts:
  `round12-boot-inventory-readonly.sh` and
  `round12-boot-inventory-extra-readonly.sh` in the capture directory.

## Limits and action gates

These lab tests used Ubuntu ARM64 WSL, sanitized psql/API/budget stubs and an
inert image. They did **not** exercise production x86_64, real credentials,
real API/DB, a paid editorial phase or the direct driver through its final
audit link. A full shared WSL reboot was not run. Given the lifted-STOP Docker
daemon-restart result, persisted `restart=no`, a unit that is not enabled at
boot, and the fresh production boot inventory, I accept reboot as a documented
residual rather than a hard pre-approval test. A new boot starter or manual
privileged `docker compose up/start/restart` would bypass the host-only fence;
recheck boot inventory at action time and prohibit such starts during the
maintenance window. After any real reboot, restore/read back STOP and
reconcile jobs, budget and hold before starting a video container.

Before any production write: independently verify the exact r7 package and
archive SHA, action-time HEAD/image/volume/STOP/container/site/job/budget
state, release hold and four locks; fill and hash the manifest. Obtain one
**named site-owner approval** for the concrete installation, no-model
`validate`, worker/policy/hold changes, temporary STOP lift, and at most the
four ordered A01 editorial phases under the existing **US$25 total cap**.
The approval should state that ordinary video auto and Shorts pause during
each phase and that the AI worker temporarily loses automatic crash restart.
Repository `prod-host-ops`, `deploy` and `ops/release` rules require consent
for those host writes; they do not require a new consent for each phase when
one explicit conditional approval names all four. The r7 README now matches
that scope.

Run no-model `validate` first and require its terminal systemd result,
`ExecStopPost=0`, exact source/link receipt, no one-off, STOP hash and job/budget
readback. Before each paid phase, pin a fresh manifest/source, verify no drift
or unsettled job and stop immediately on any failure or uncertainty. A
`systemctl start --no-block` acceptance is not a phase result; pin and poll
the invocation to terminal readback, and never repeat a phase after SSH loss
without reconciliation. A timeout or signal after model dispatch is an
uncertain outcome even if one-off cleanup succeeds. This review does not
claim A01 manuscript approval, completed video, or YouTube publication.
