---
id: 2026-09-28-drama-preloaded-document-approval-order
title: Guard approval order for preloaded drama review documents
status: review
priority: P1
area: api
owner: codex-ten-drama
claimed_at: 2026-09-28T14:38:38Z
created_at: 2026-09-28T14:01:50Z
completed_at:
branch: codex/ten-drama-audit-fixes
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/tests/test_video_series.py
  - apps/api/tests/test_video_drama_messages.py
  - apps/api/tests/test_video_series_binge.py
  - apps/api/tests/test_video_story.py
  - apps/api/tests/test_video_series_document_lifecycle.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/messages.py
  - tools/video/automation/discuss.mjs
  - tools/video/automation/discuss.test.mjs
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-thread.tsx
  - apps/web/components/admin-video-thread.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Guard approval order for preloaded drama review documents

## Why

The ten imported drama plans each preload setting, outline and four chapter
documents as review. The UI renders every document and enables Approve on all
review documents. Approving outline before setting can strand the series in
outline status even after both documents and a chapter are approved. The worker
then returns no next job, despite ready episodes.

Confirmed during the ten-drama audit on 2026-09-28. The production snapshot at
13:57:22Z has all ten series still in setting with sixty review docs and no
episodes/requests/projects/media jobs; the bad approval sequence has not yet
been applied to these targets. No production state was mutated to reproduce it.

## Definition of done

- [x] Server either rejects out-of-order decisions before changing any state,
  with an actionable explanation, or deterministically reconciles series status
  from approved prerequisites so all valid orders can progress.
- [x] UI makes document dependencies understandable; API calls cannot bypass
  the invariant. Cover edit_doc with approve=true as well as decide_doc.
- [x] All six preloaded review docs remain readable; setting-only approval must
  not accidentally approve downstream documents or start an unapproved episode.
- [x] Regression tests cover imported six-document state, normal order, outline
  before setting, chapter before prerequisites, and safe repeated decisions.
- [x] Any already affected work has a reviewable recovery path preserving
  approvals and episode data; production recovery requires separate authorization.

## Steps

- [x] Inspect _apply_approval, decide_doc, edit_doc and next_job_for in
  apps/api/app/video_automation/series.py. In current checkout, setting approval
  only changes setting to outline (:1255), outline approval only changes outline
  to active (:1273), and decide_doc only checks the document's review status
  (:1306), not its prerequisites.
- [x] Inspect apps/web/components/admin-video-series.tsx:586-590 and :709.
  Approve is disabled only while busy; all documents are mapped to DocPanel
  regardless of series status or dependency approval.
- [x] Coordinate with PR #929 codex/import-reviewed-drama-plans, which introduces
  the preloaded-document workflow, and current API/UI task owners before edits.
  The importer itself avoids unwanted planning by importing all documents as review.

## How to verify

Offline reproduction used actual functions extracted from the current module's
AST, an in-memory session, and the real wedding-reckoning/documents.json. It did
not mock the state-transition or next-job logic. This is a focused state-machine
reproduction, not an HTTP/database integration test.

```text
initial 6 review documents: next_job = None
setting -> outline -> chapter 1: status active, 40 episodes, 10 ready, next episode 1
outline -> setting -> chapter 1: status outline, 40 episodes, 10 ready, next_job None
chapter 1 -> outline -> setting: status outline, 40 episodes, 10 ready, next_job None
chapter 1 -> setting -> outline: status active, 40 episodes, 10 ready, next episode 1
```

For the fix, add a real database-backed service/API regression in
apps/api/tests/test_video_series.py, run the related tests and API lint/types, and
run admin-video-series component tests if changing the UI. Read backend-conventions,
dev-and-ci and web-i18n-e2e skills as appropriate before implementation.

Exact stdlib-only reproduction from the repository root (PowerShell; replace
python with the installed interpreter path if necessary):

```powershell
@'
import ast, asyncio, json
from pathlib import Path
from types import SimpleNamespace as N
from datetime import datetime, UTC
from uuid import uuid4
src=Path('apps/api/app/video_automation/series.py').read_text(encoding='utf-8')
names='_apply_approval _new_episode next_job_for _rewrite_job latest_docs episode_rows_from_outline beats_from_chapter chapter_count chapter_range chapter_of is_story is_one_off setting_kind'.split()
async def get_rows(session,series): return session.rows
ns=dict(VideoDramaEpisode=N,NextJob=N,_now=lambda:datetime.now(UTC),uuid4=uuid4,_episodes=get_rows,AUTO_TITLE='__auto__',DISCUSSION_NOTE='__discussion__')
exec('from __future__ import annotations\n'+'\n\n'.join(ast.get_source_segment(src,n) for n in ast.parse(src).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names),ns)
raw=json.loads(Path('docs/videos/series-plans/binge-five-20260928/wedding-reckoning/documents.json').read_text(encoding='utf-8'))['documents']
class Session:
 def __init__(self): self.rows=[]
 def add(self,row): self.rows.append(row)
settings=N(series_doc_rewrites=2,series_max_in_flight=1,series_episodes_per_month=40,series_auto_continue=True,series_chapter_ahead=2)
async def run(order):
 s=N(id='test',kind='series',status='setting',title='test',planned_episodes=40,episodes_per_chapter=10,compilation=True,requested_chapter=None,force_next=False)
 docs=[N(**d,status='review',version=1,note=None) for d in raw]; session=Session()
 assert ns['next_job_for'](s,docs,[],settings,started_this_month=0) is None
 for kind in order:
  d=next(d for d in docs if d.kind==kind and d.chapter_number==(1 if kind=='chapter' else 0)); d.status='approved'
  await ns['_apply_approval'](session,s,d)
 job=ns['next_job_for'](s,docs,session.rows,settings,started_this_month=0)
 print('>'.join(order),s.status,len(session.rows),sum(e.status=='ready' for e in session.rows),vars(job) if job else None)
async def main():
 for order in [('setting','outline','chapter'),('outline','setting','chapter'),('chapter','outline','setting'),('chapter','setting','outline')]: await run(order)
asyncio.run(main())
'@ | python -
```

## Notes

- Production revision was 045afc1e. Live API container series.py SHA-256 was
  b514b5c26ef4926f526e9314d40533808007b3efbd3cd8bc37dd750062a571a0,
  equal to that revision's Git blob. _apply_approval, decide_doc and _rewrite_job
  are byte-identical to the audited checkout after LF normalization. The later
  next_job_for changes add brand-story handling, not this drama-state transition.
- Production repository admin-video-series.tsx SHA-256 was
  3fb1543d8d10243a4e304ef4b1156af96ebe4f9f5a70f380d7e68cda1076b883,
  matching 045afc1e. Its only difference from current checkout is the Shorts query
  filter; approval controls are unchanged. Browser control timed out, so this
  does not claim an actual click-through reproduction in production.
- Current safe ordering is setting, then outline, then chapter documents. Do not
  approve flawed content merely to exercise this workaround.
- Separate editorial findings are in 2026-09-28-ten-drama-plan-audit-findings.
  This task files the defect only; no application or production changes were made.

## Implementation coordination

- On 2026-09-28 the owner explicitly authorized isolated-branch fixes despite
  overlapping task claims, preserving other branches and claims. This ticket
  owns coordinated API/web fixes for approval order, structured editing, review
  discussion context and revision readiness; related tickets retain evidence.
- Branch codex/ten-drama-audit-fixes, worktree 31ce. No production operation.

## Repair implementation, 2026-09-28

- Implemented in isolated branch `codex/ten-drama-audit-fixes` under the claimed
  ten-drama content / preloaded-approval / listener tasks. The owner explicitly
  approved parallel backend repairs despite other task claims; no other branch
  or owner claim was changed.
- Report: `docs/videos/series-plans/binge-five-20260928/AUDIT-REPAIR-20260928.md`.
- Local source/documents and code are revised; historical production/import
  receipts are unchanged. No deployment, production update, approval, generation
  or publication has been performed by this repair.

### Verification and handoff

- Content: both ten-work validators pass; 34 generator/continuity tests pass;
  independent revised-source receipts and all 60 current document hashes checked.
- API: 80 focused tests pass, including SQLite transaction coverage; 5 PostgreSQL
  integration tests remain skipped locally. Ruff and touched-file mypy pass.
- Worker/tool suite: 578 pass, 1 existing Windows/Bash environment skip.
- The branch is ready for code review; it has not been merged or deployed. The
  independent production/browser follow-up remains with its existing owner.
- Revision race protections also bind AI replies to target/parent snapshots
  and owner decisions to the displayed expected_version. Stale operations cannot
  overwrite a newer draft or approve an unseen version.
