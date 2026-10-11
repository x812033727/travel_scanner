---
id: 2026-10-09-give-the-automated-route-a-way
title: Give the automated route a way to answer 要先實作: a recorded hands-on run before the writer starts
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T02:41:26Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - docs/videos/AUTOMATION.md
---

# Give the automated route a way to answer 要先實作: a recorded hands-on run before the writer starts

## Why

The content-value rules (PR 1392) and the teaching route (PR 1390) both say a tutorial's
outcomes need a real run: input, action, observed result, date, tool version. When there is
none, the planner now writes 「要先實作：…」 in the brief's 示範或實算. On the host nobody can
answer that: the worker plans, writes and checks from pages it reads, and has no step that
installs or runs the tool the video is about. So a tutorial planned there either stops at the
brief or goes out labelled untested, which is the video the owner rejected on 2026-10-09
(its description said nothing had been installed or run).

The one hand-made sample that did have a run (two mods written, validated and tested on
2026-10-09, `claude plugin validate` and `claude plugin test` output kept) was made by an
agent session on the owner's machine.

## Definition of done

- [ ] A brief that says 「要先實作」 has a defined next step and an owner of that step, shown on
  the video's card.
- [ ] A run record supplied for it (commands, real output, date, tool version) reaches the
  writer as a source and can back a `terminal` scene.
- [ ] Nothing is run on the production host that installs third-party code.

## Steps

- [ ] Ask the owner which it is: an agent session on their machine does the run and uploads the
  record, a sandbox on the host does it, or such topics leave the automated route.
- [ ] Define the record's shape and where it lives in the work folder.
- [ ] Wire the waiting state into the flow and the admin card.

## How to verify

A tutorial brief with 「要先實作」 waits with a reason; after a record is supplied the writer's
payload carries it and the script's terminal scene shows its date and tool version.

## Notes

- A mod runs with the user's permissions and is not sandboxed; the same holds for most tools a
  tutorial would install. Where the run happens is a security decision, not only a convenience.
- Open tasks that touch the same idea from the recording side:
  `2026-09-24-video-obs-import`.
