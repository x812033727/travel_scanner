# VPS web settings browser acceptance

Status on 2026-10-01: **not accepted — local preview startup was blocked**.

The production build for source commit
`76b39a25e3819d5ef97648e10a5b8c6bb1bfbd74` completed successfully with Node
24.21.0. The tool's automatic approval review then rejected the hidden local Next
server launch with `blocked by policy`. That command did not execute. No alternate
launcher was attempted. No browser submission, screenshot or visual inspection
was completed in this attempt.

The unchanged runtime fixture and a separate synthetic settings proxy had started
on loopback ports 18780 and 18781. Both owned processes were stopped; those ports
and the unused Next port 3016 had no listeners at cleanup. All forwarding in the
prepared proxy was restricted to explicit GET routes on the loopback runtime.
Settings saves and diagnostics were designed as synthetic in-memory responses.
No production, VPS, Google or paid-service operation was performed.

[The attempt receipt](attempt-20261001.json) records the build, prepared helper
hashes and cleanup. Private helpers and build logs remain outside the repository;
their existence is preparation evidence, not evidence that browser assertions
passed. There are no screenshots to review.

The open browser-acceptance task must still verify all of these through the real
local Next/BFF interface when an approved preview can run:

- Desktop and mobile layouts in light and dark themes, including clipping and
  horizontal overflow.
- Save and reload; empty password input and no saved secret in returned data or
  evidence; successful and failed synthetic diagnostics followed by retry.
- A stale-write 409 that retains edited channel and secret fields; refresh that
  incorporates an unchanged desktop field from the latest version; a retry that
  submits the new revision and only edited fields.
- Read-only disabled fields and save/test buttons, a usable refresh action, no UI
  writes and denied direct synthetic write attempts.
- The saved desktop link and the unconfigured uploader's settings link reaching
  the intended local destinations.

This task covers isolated UI acceptance only. Actual VPS connectivity, Google
login, channel identity, upload and owner review remain separate work.
