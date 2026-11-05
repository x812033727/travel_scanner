---
id: 2026-10-30-h3-prompt-checks-from-henge
title: H3 prompt checks from Henge: no timecodes, Ref2VA sections in order, a concrete kept setting
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-30T06:28:30Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/minimax-h3-colab/scripts/check_manifest.py
  - tools/minimax-h3-colab.test.mjs
---

# H3 prompt checks from Henge: no timecodes, Ref2VA sections in order, a concrete kept setting

## Why

Henge (alisson-anjos/Henge, MIT) checks H3 prompts for things our `check_manifest.py` does not
(read 2026-10-30): it forbids timecodes inside the description (models follow "first, then,
finally" better than "00:05" or "2-4 s"), requires the six Ref2VA sections present and in order,
and refuses vague kept settings such as "the original setting" (the model then invents a room).
Each of these wastes a paid clip when it slips through.

## Definition of done

- [ ] `check_manifest.py` errors on a timecode in a prompt body (00:05, 2-4s, "at 3 seconds").
- [ ] For `reference` jobs, it errors when the six sections (`subject_definitions`, `summary`,
      `retention_analysis`, `detailed_description`, `overall_soundscape`, `non_diegetic_music`) are
      missing or out of order.
- [ ] It warns on "the original setting/background/scene" style phrases.
- [ ] Tests in `tools/minimax-h3-colab.test.mjs`.

## Steps

- [ ] Read Henge `docs/prompt-format.md` and `lib/h3-prompt-policy.json` for the exact rules.
- [ ] Add the checks and their tests.

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs   # Linux/macOS
```

## Notes

- The first-frame (FL2VA) body's official first line contains "0.00 seconds"; the timecode rule
  must skip that fixed line.
