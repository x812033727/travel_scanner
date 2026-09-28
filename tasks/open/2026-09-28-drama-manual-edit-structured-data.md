---
id: 2026-09-28-drama-manual-edit-structured-data
title: Keep drama manual edits consistent with structured production data
status: review
priority: P1
area: api
owner: codex-ten-drama
claimed_at: 2026-09-28T15:03:43Z
created_at: 2026-09-28T14:13:50Z
completed_at:
branch: codex/ten-drama-audit-fixes
depends_on: []
scope:
  - apps/api/app/video_automation/series.py
  - apps/api/tests/test_video_series.py
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
---

# Keep drama manual edits consistent with structured production data

## Why

The native document editor sends only body_md and approve. edit_doc retains the
previous body_json when it is absent, then permits approval. An owner correcting
one of the ten imported drama plans can therefore approve visible changes while
the machine-readable cast, episode rows and beats remain unchanged. The worker
receives contradictory approved inputs.

Offline reproduction with the real Wedding setting changed the lead from
沈知棠 to 沈知芸 in Markdown. The resulting document was approved, the new name
was visible, and body_json.characters still named 沈知棠. The actual edit_doc,
_apply_approval and approved_doc implementations are identical to deployed
revision 045afc1e. No production document was edited for this test.

## Definition of done

- [x] Semantic manual edits cannot be approved with stale structured data.
  Choose an explicit coherent editing/reconciliation contract; do not merely
  suppress the mismatch in the UI or silently drop structured content.
- [x] Markdown and structured changes are reviewed together before approval.
  Formatting-only edits may preserve data when the contract proves that safe.
- [x] Cover setting cast/rules, outline episode rows, and chapter beats; verify
  what subsequent production actually reads, including edits of approved docs.
- [x] Preserve version history and make any required reconciliation a visible
  review step rather than silently authorizing generation or paid model calls.
- [x] Add API and native editor regressions for the real body_md-only payload.

## Steps

- [x] Inspect admin-video-series.tsx:558-564: save() serializes only body_md and
  approve. series.py:1345 retains latest.body_json; :1369-1378 approves the
  combination. doc_problem validates its shape, not semantic agreement.
- [x] Trace downstream consumers: flow.mjs:799 and :850 take the old cast from
  body_json; series.mjs:235-242 preserves its names, appearance and voice. Outline
  and chapter approvals likewise use structured episode data.
- [x] Coordinate with active video/API owners and PR #929's importer workflow.
  Related preloaded approval order is tracked separately in
  2026-09-28-drama-preloaded-document-approval-order.

## How to verify

Observed output from actual extracted repository functions and an in-memory
session (not an HTTP/database/browser integration test):

```json
{"status":"approved","markdown_lead":"沈知芸","machine_cast_lead":"沈知棠","retained_old_body_json":true,"series_status":"outline"}
```

Reproduce without a database, network access, generation or repository writes.
From the repository root, pass this code to Python using a PowerShell literal
here-string and `python -X utf8 -`:

```python
import ast, asyncio, json
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace as N
from typing import Any, cast
from uuid import uuid4
src = Path('apps/api/app/video_automation/series.py').read_text(encoding='utf-8')
names = 'edit_doc latest_docs doc_problem is_story is_one_off _apply_approval'.split()
async def get_series(session, slug, lock=False): return session.series
async def get_docs(session, series): return session.docs
async def view(session, slug): return session.docs[-1]
ns = dict(_series=get_series, _docs=get_docs, series_view=view,
          _now=lambda: datetime.now(UTC), uuid4=uuid4, cast=cast, Any=Any,
          SeriesDocSubmitIn=N, VideoDramaDoc=N, AdminAuditLog=N, AUTO_TITLE='__auto__')
exec('from __future__ import annotations\n' + '\n\n'.join(
    ast.get_source_segment(src, n) for n in ast.parse(src).body
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in names), ns)
raw = json.loads(Path('docs/videos/series-plans/binge-five-20260928/wedding-reckoning/documents.json').read_text(encoding='utf-8'))['documents'][0]
class Session:
    def __init__(self):
        self.series = N(id='test', slug='wedding-reckoning', kind='series',
                        status='setting', title='喜宴未散，清算開始')
        self.docs = [N(**raw, status='review', version=1, note=None)]
    def add(self, row):
        if hasattr(row, 'kind'): self.docs.append(row)
    async def commit(self): pass
async def main():
    session = Session()
    old = session.docs[0].body_json['characters'][0]['name']
    new = '沈知芸'
    result = await ns['edit_doc'](session, N(id='owner'), 'wedding-reckoning',
        'setting', 0, N(body_md=raw['body_md'].replace(old, new), body_json=None, approve=True))
    assert result.status == 'approved' and new in result.body_md
    assert result.body_json['characters'][0]['name'] == old
    print(json.dumps(dict(status=result.status, markdown_lead=new,
        machine_cast_lead=result.body_json['characters'][0]['name'],
        retained_old_body_json=result.body_json == raw['body_json'],
        series_status=session.series.status), ensure_ascii=False))
asyncio.run(main())
```

For the fix, run focused database-backed series service/API tests and native
editor tests using dev-and-ci and web-i18n-e2e guidance. Assert downstream data
agrees with what the owner approved, not just that the PUT returns success.

## Notes

- Discovered during the second ten-drama audit on 2026-09-28. It is distinct from
  PUT rejecting a brand-new work with no document, and from approval order.
- Current imported source data was consistent at the previous read-only snapshot;
  this finding concerns the correction path, not evidence it has already damaged
  the ten works. No code fix, approval, production edit or deployment was performed.

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
