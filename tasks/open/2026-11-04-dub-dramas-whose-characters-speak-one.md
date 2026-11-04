---
id: 2026-11-04-dub-dramas-whose-characters-speak-one
title: Dub dramas whose characters speak: one foreign voice per character
status: in-progress
priority: P2
area: tools
owner: claude-opus-stw-dialogue
claimed_at: 2026-11-04T11:27:10Z
created_at: 2026-11-04T11:25:31Z
completed_at:
branch: claude/focused-hopper-zq70n8-p02-langs
depends_on: []
scope:
  - tools/video/dubs/plan.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/cast.test.mjs
  - docs/videos/DUBS.md
---

# Dub dramas whose characters speak: one foreign voice per character

## Why

站主 2026-11-04 在後台替 `sothatswhy-p02-cloud-rain` 勾了八語配音。`dub` 原本只用旁白一個聲音唸每一句，遇到角色說話的漫劇就以結束碼 3 拒絕；原來如此的對話版有所長與小問兩個人說話。

## Definition of done

- [x] 原來如此的對話解說片（`isDialogueExplainer`）配音時，每個說話角色用自己的 Gemini 聲音、人設不變、換成該語系的語言（`plan.mjs` `dubCharacterVoice`）；一般漫劇仍拒絕。
- [ ] P02 八語配音錄完、`check-audio` 過、交站主。
- [ ] `docs/videos/DUBS.md` 記下這條例外。

## Notes

- 只開放對話解說片，不改既有測試（`dubs.test.mjs` 綁在長片收據上）；新測試在 `cast.test.mjs`。
- 2026-11-04 用 `--force` 認領：scope 跟 `2026-10-09-dub-skipped-because-jev-still-hears`、`2026-10-13-dub-narrator-only-explainer-dramas-tool`、`2026-10-14-make-whisper-second-opinion-work-with`、`2026-10-16-bind-story-audits-and-narration-to`、`2026-10-19-worker-video-languages-five`、`2026-10-25-record-the-english-card-eight-language` 重疊，它們的認領都超過 24 小時（過期，`tasks/README.md` 允許接手）。這張只動 `dubs/plan.mjs` 的兩個新函式與 `dubScript` 一處、`dubs/cli.mjs` 的 `spokenByCharacter`，加一個新測試檔，不碰它們的範圍內其他檔。
