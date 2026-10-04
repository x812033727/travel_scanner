---
id: 2026-10-04-audit-look-reviews-another-character-overwrote
title: Audit look reviews another character overwrote
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-10-04T16:30:15Z
completed_at:
branch:
depends_on:
  - 2026-10-02-keep-character-look-review-identities-distinct
scope:
  - docs/videos/series-plans/look-review-audit-20261004
---

# Audit look reviews another character overwrote

## Why

From the look stage's start (#800) until the fix in
`2026-10-02-keep-character-look-review-identities-distinct`, review-push sent every
character's look review with the one hash of `characters/manifest.json`, and
`submit_review` reused a review by gate and hash alone. On production that left two
kinds of damage on any drama with two or more characters:

- the first character's review was still pending: the second character's summary,
  payload (its own `subject`, options and suggestion) and files overwrote it, and the
  row kept the first character's `subject`;
- the first one was decided: the second character got no review at all, and
  review-pull waits for that character forever.

The fix stops both from happening again; it does not repair rows already written. A
pending overwritten row heals when review-push sends the look gate again, but a row the
owner decided while it showed another character's sheets keeps a choice made on the
wrong pictures, and review-pull records that choice for the row's subject.

## Definition of done

- [ ] Production's look reviews whose `payload->>'subject'` differs from `subject`
      are listed with their slug, status and choice (or the list is shown empty).
- [ ] Every drama whose look gate waits on a character without a review is listed.
- [ ] The owner has decided what to do with each decided, overwritten review
      (re-review the character or keep it); nothing is changed without that decision.

## Steps

- [ ] Wait until the fix is deployed (migration `0124_video_review_subject` is the head).
- [ ] With the owner's go-ahead, run the read-only query below on the host (skill
      `prod-host-ops`), and save the result without personal data under the scope path.
- [ ] For a waiting drama, run `review-push --gate look` again from the work machine.
- [ ] Bring the decided, overwritten rows to the owner.

## How to verify

Read only, on production's database (`json` column, so `->>`, no jsonb operators):

```sql
SELECT p.slug, r.id, r.subject, r.payload ->> 'subject' AS payload_subject,
       r.status, r.choice, r.created_at, r.decided_at
FROM video_reviews r JOIN video_projects p ON p.id = r.project_id
WHERE r.gate = 'look'
  AND r.payload ->> 'subject' IS NOT NULL
  AND r.subject IS DISTINCT FROM r.payload ->> 'subject'
ORDER BY p.slug, r.created_at;
```

An empty result, or each row listed with the owner's decision next to it.

## Notes

Filed by claude-opus-5-5-look-review-subject while fixing the identity; no production
data was read (the session had no host access). A review whose payload has no
`subject` (an older CLI) cannot be judged by this query; look at its
`payload->'character'->>'name'` against the subject instead.
