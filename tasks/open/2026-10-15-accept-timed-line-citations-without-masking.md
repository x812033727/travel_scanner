---
id: 2026-10-15-accept-timed-line-citations-without-masking
title: Accept timed line citations without masking narrative no answers
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-15T17:22:04Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
---

# Accept timed line citations without masking narrative no answers

## Why

The narrative panel receives narration lines formatted `[id mm:ss]`, but `panelVerdict` accepts only `[id]` in returned evidence. A real A01 round-5 response quoted the input format and returned nine true answers and four false answers. The parser changed all thirteen to false, obscuring the four genuine content failures. Correct citation parsing must preserve the independent reader's actual yes/no decisions and must not turn the old failed film into a pass.

## Definition of done

- [ ] Exact supported timed citations and plain IDs are recognized; missing/malformed evidence still fails closed.
- [ ] Actual `yes: false` answers remain false with either citation format.
- [ ] Regression coverage includes the round-5 shape, absent evidence, malformed times and nonboolean answers.
- [ ] No historical review or production approval is rewritten as part of the code change.

## Steps

- [ ] Check current ownership/main, claim, and inspect the narration format and evidence parser together.
- [ ] Implement the narrow parser correction with tests and normal PR review.

## How to verify

Run `node --test tools/video/core/narrative.test.mjs`, the affected video-tool checks, and `npm run check:tasks`. Explicitly demonstrate that a mixed nine-true/four-false timed response remains failed with exactly the four real required failures.

## Notes

- 2026-10-16: Found during authorized A01 continuation. Producer `story.mjs` SHA `f9825a7ce9649111d3e49ab33a2846a8be61111dd2cb2df40db3b68b974676f3`, deployed commit `aac8d73fb0e5f2321cf9d929c6ea52e001198b23`. Parser at `tools/video/core/narrative.mjs` currently uses `/\[[A-Za-z0-9_-]{2,}\]/` without accepting its input's timestamp.
- The succeeded raw job is `308a8ced-f368-40c5-ad55-43fbdc59beb8`; request hash `cf4f3752838b16e6008bd907865a7b6b534e0729afc6c3b1ce448bfb26183730`. Raw false checks are `payoffs`, `no_recap`, `one_thread`, `no_detour`. The rejected canonical narrative receipt SHA is `b8261e364f349ad21acb4108bed4a833444e774c3ee70f67aca6ecc32239b976` and stays rejected.
- Exact evidence is retained under the A01 host `story/recheck-audit/2026-10-15T17-19-30.456Z-abbf5612-c0fd-488d-a530-903910ad0e19`; downloaded archive SHA `46415e4fa1747b208f3706a5ed89aea923ac3feec19ae0098d1587f52e849a73`. Do not dispatch the same prompt unchanged to make the mixed verdict disappear.
