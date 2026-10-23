# Context
講座籌備 folder has three "final" outlines. Pick the truly latest one, rename it to `講座簡報大綱_2026-11-14.md`, and archive the other two into `封存/` with their modification date prefixed.

# Finding: newest by timestamp ≠ newest by content
| File | Modified | Content |
|---|---|---|
| 最終版 | 2026-10-05 | 16:00 end, 2nd speaker "待邀請", no Q&A |
| 真的最終版 | 2026-10-18 22:10 | 14:00–16:30, both speakers 皆已確認, includes Q&A 20 min |
| 這次絕對最終版 | 2026-10-20 08:45 | 16:00 end, 范可甯 "待確認", no Q&A (looks like an older draft edited later) |

`活動說明.md` (10/18) says 14:00–16:30 (extended for Q&A) and both speakers confirmed — matches **真的最終版** only. So the real latest is 真的最終版, even though 這次絕對最終版 has the later mtime.

# Steps (all in `<home>\mokaair-work\videos\claude-code-beginner-event-folder\run\lab\講座籌備`)
1. Create `封存/`.
2. `講座簡報大綱_真的最終版.md` → `講座簡報大綱_2026-11-14.md`
3. `講座簡報大綱_最終版.md` → `封存/2026-10-05_講座簡報大綱_最終版.md`
4. `講座簡報大綱_這次絕對最終版.md` → `封存/2026-10-20_講座簡報大綱_這次絕對最終版.md`

Use Move-Item (mtime preserved). Nothing else touched (舊版簡報大綱_2025.md stays; not one of the three).

# Verification
List the folder and `封存/`; confirm 3 files moved/renamed, mtimes unchanged, and the new file's content shows 16:30 / 皆已確認.
