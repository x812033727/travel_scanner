---
id: 2026-10-01-owner-settles-the-looks-the-ten
title: Owner settles the looks the ten drama plans leave open
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-01T14:28:10Z
completed_at:
branch:
depends_on:
  - 2026-10-01-setting-planner-writes-character-looks-and
scope:
  - docs/videos/series-plans/binge-five-20260928
  - docs/videos/series-plans/claude-binge-five-20260928
---

# Owner settles the looks the ten drama plans leave open

## Why

Task `2026-10-01-setting-planner-writes-character-looks-and` moved into `looks` every change in
the ten forty-episode plans whose episodes and drawing the plans already state (docs/videos/SERIES.md,
換裝與變化). What it left in `continuity_notes` needs a decision the plans do not make: a change in
the middle of one episode (the pipeline would need a second character id, which changes the
episode's cast), a range the notes do not pin down, or an outfit nobody wrote. Each is drawn from
the base appearance or a shot prompt until someone decides. None of the ten works has started an
episode, so nothing produced is wrong yet.

## Definition of done

- [ ] Each item below is either written into a character's `looks` (or a second character id),
  or recorded in the plan's `continuity_notes` as "stays a shot prompt", with the owner's choice.
- [ ] `node build.mjs`, `node validate.mjs` and `node --test validate.test.mjs` clean in both
  plan directories.
- [ ] The independent review receipts for wedding-reckoning and seventh-passenger re-read
  (their `source_sha256` is stale since the looks were added; `node validate.mjs
  --require-reviews` in binge-five-20260928 reports it), and the shared
  `validation-report.json` / `local-revision-manifest.json` refreshed by whoever owns them.

## Steps

Changes inside one episode (second character id, or composition only):

- [ ] wedding-reckoning: episode 1 cold open (0–5 s, Zhitang at the warehouse door in her
  past life) sits inside the wedding-gown look (1–3).
- [ ] seventh-passenger: He Zhao takes the conductor coat off and gets his identity back in the
  middle of episode 27; the episode uses the base look and the steady base voice from its start.
- [ ] ghost-at-his-side: Lu Zheng becomes 93 at the burn beat of episode 30 (look aged-61 covers
  24–30); Zong Dan ages ninety years and his voice fades to breath in episode 37; Lu Zheng's
  wrists wrinkle from a beat in episode 16 (hidden by sleeves until 23).
- [ ] reload-first-day: the panels go out in the middle of episodes 1, 21, 38–39 and 40 (note 面板
  already asks for a variant); Su Xing's flat voice starts at the line 「好。」 inside episode 35
  and Du Chengye's after he bows in episode 31 (looks start at 36 and 32).
- [ ] three-needles: Wei Cheng's voice after he turns (episode 32, his last).

Ranges or outfits the plans do not state:

- [ ] city-owes-a-light: Lin Jiming's clothes on the observation bed in episode 38 (base has
  rain boots; note ④ covers his legs) and in episodes 39–40 (six months and a year on); Zhou He's
  blue hard hat in 39–40; voice styles 周禾「後段減少搶話」 (which episodes?).
- [ ] seventh-passenger: 徐浩「後段放低聲量」 (which episodes?).
- [ ] wedding-reckoning: 沈知夏「敢說真話後語速放穩」 and 沈崇岳「敗局才出現呼吸失序」 (from which
  episode?).
- [ ] ghost-at-his-side: 老尤「後半段話變少、動作變多」 (second half of the series, or of a scene?).
- [ ] remembered-by-rival: Qi Yan's right wrist after the cord is cut (36–38 a shallow wound, 40
  a faint mark; note 呈現界線 allows either bandage or healed mark, 39 is unstated).
- [ ] before-the-hammer: Zhiyuan in custody in episodes 33 and 38 (base is the three-piece suit,
  gold watch and pen; round-5 review left it to this).
- [ ] taste-of-the-throne: the empress dowager and the regent in the inner prison still in court
  robes and crowns, Liu Gugu in the prison (18–22) with apron and keys (round-5 review).
- [ ] three-needles: voice styles that carry episode numbers (沈鶴亭「只在第 16 集開口」, 郭思思
  「第 34 集第一個字」, 谿翁「第 37 集才開口」) are production notes sent with every line.

## How to verify

In each plan directory: `node build.mjs`, `node validate.mjs`, `node --test validate.test.mjs`.

## Notes

- Additions a shot prompt can make (a crown, badges, a lantern, bandages, a backpack, the ghost's
  glow) were left as shot prompts on purpose: the ticket that added looks moved only what a
  shot prompt cannot add or a voice that changes for a run of episodes. If the owner wants the
  approved character sheet to show a long-worn addition (for example Ye Sui's crown in 2–28),
  that is a look too.
