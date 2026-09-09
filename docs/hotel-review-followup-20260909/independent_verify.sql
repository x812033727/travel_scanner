-- Run unchanged before/after/replay with the finalized manifest size:
-- psql -X -v ON_ERROR_STOP=1 -v expected_count=<1..174> -f independent_verify.sql
-- expected_count is a required psql variable, safely SQL-quoted and integer-cast.
-- Counts before the batch may be zero; expected_count is the FINAL subset size.
-- This diagnostic does not replace operator verify/full-row SHA-256 comparison.
\set ON_ERROR_STOP on
\if :{?expected_count}
\else
\echo 'Missing required -v expected_count=<final manifest decision count>'
-- Deliberate read-only error: ON_ERROR_STOP gives a nonzero script exit.
SELECT 1 / 0 AS missing_expected_count;
\endif
-- Read-only, one consistent snapshot. No raw settings, credentials, emails or
-- click identifiers are returned. MD5 values are comparison fingerprints, not
-- the operator's SHA-256 manifest/row verification or authorization check.
-- Live traffic may legitimately increase click counts; inspect such differences.
BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
SET LOCAL TIME ZONE 'UTC';

-- Invalid or non-integer input stops before querying any application rows.
SELECT (:'expected_count'::integer BETWEEN 1 AND 174) AS expected_count_valid
\gset
\if :expected_count_valid
\else
\echo 'expected_count must be an integer between 1 and 174'
SELECT 1 / 0 AS invalid_expected_count;
\endif

SELECT 'snapshot' AS section, transaction_timestamp() AS captured_at,
       current_setting('transaction_isolation') AS isolation_level,
       current_setting('transaction_read_only') AS read_only;

SELECT 'hotel_products' AS section, destination_id AS city, status,
       count(*) AS rows,
       md5(coalesce(string_agg(md5(to_jsonb(p)::text), '' ORDER BY id), '')) AS rows_md5
FROM travel_service_products p
WHERE kind = 'hotel'
GROUP BY destination_id, status
ORDER BY destination_id, status;

SELECT 'hotel_options' AS section, p.destination_id AS city, o.provider,
       o.status, o.discovery_status, count(*) AS rows,
       md5(coalesce(string_agg(md5(to_jsonb(o)::text), '' ORDER BY o.id), '')) AS rows_md5
FROM hotel_booking_options o
JOIN travel_service_products p ON p.id = o.product_id
WHERE p.kind = 'hotel'
GROUP BY p.destination_id, o.provider, o.status, o.discovery_status
ORDER BY p.destination_id, o.provider, o.status, o.discovery_status;

-- The root identifies the authenticated actor, NOT hotel review membership.
SELECT 'root_actor_provenance' AS section, count(*) AS matching_roots,
       count(*) FILTER (WHERE r.mode = 'review_pending') AS review_pending_roots,
       count(*) FILTER (WHERE u.is_active) AS active_actors,
       count(*) FILTER (WHERE EXISTS (
           SELECT 1 FROM admin_audit_logs a
           WHERE a.action = 'catalog_review_requested'
             AND a.target = 'catalog-review:5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a'
             AND a.actor_user_id = r.actor_user_id
       )) AS authenticated_request_audits
FROM catalog_review_runs r
JOIN users u ON u.id = r.actor_user_id
WHERE r.id = '5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a'::uuid;

WITH receipts AS (
    SELECT a.* FROM admin_audit_logs a
    WHERE action = 'hotel_catalog_evidence_review'
      AND target LIKE 'hotel-review-followup-20260909:%'
), root_actor AS (
    SELECT actor_user_id FROM catalog_review_runs
    WHERE id = '5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a'::uuid
)
SELECT 'receipt_totals' AS section, :'expected_count'::integer AS expected_final_rows,
       count(*) AS rows, count(DISTINCT target) AS distinct_targets,
       count(*) - count(DISTINCT target) AS duplicate_targets,
       count(DISTINCT actor_user_id) AS distinct_actors,
       count(*) FILTER (WHERE actor_user_id = (SELECT actor_user_id FROM root_actor))
           AS root_actor_rows,
       count(*) FILTER (WHERE actor_user_id IS NULL) AS null_actor_rows,
       count(*) FILTER (WHERE metadata_json->>'tag' IS DISTINCT FROM 'hotel-review-followup-20260909'
           OR metadata_json->>'root_run_id' IS DISTINCT FROM '5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a'
           OR metadata_json->>'baseline_hash' IS DISTINCT FROM
              'd9823e0996ad09ba14fe05b2e9a674544544d4dacb7b87d6fac288be5e51453c')
           AS invalid_provenance_rows,
       md5(coalesce(string_agg(md5(to_jsonb(receipts)::text), '' ORDER BY id), '')) AS rows_md5
FROM receipts;

SELECT 'receipt_outcomes' AS section,
       metadata_json->>'kind' AS kind,
       metadata_json->>'requested_decision' AS requested_decision,
       metadata_json->>'outcome' AS outcome,
       coalesce(metadata_json->>'guard_code', '(none)') AS guard_code,
       count(*) AS rows,
       count(*) FILTER (WHERE metadata_json->>'outcome' = 'hold'
           AND (metadata_json->>'before_hash' IS DISTINCT FROM metadata_json->>'after_hash'
             OR metadata_json->>'before_version' IS DISTINCT FROM metadata_json->>'after_version'))
           AS changed_hold_rows
FROM admin_audit_logs
WHERE action = 'hotel_catalog_evidence_review'
  AND target LIKE 'hotel-review-followup-20260909:%'
GROUP BY 2, 3, 4, 5
ORDER BY 2, 3, 4, 5;

-- Exact normal-service action names, exact hotel product/option UUID targets.
-- Both lifetime and post-baseline counts allow the same query to be run before
-- receipts exist. Post-baseline counts can include concurrent administrator work;
-- receipt_target_rows additionally identify this batch's receipted targets.
WITH actions(action, kind) AS (VALUES
    ('travel_services.product_edit', 'product'),
    ('travel_services.product_review', 'product'),
    ('travel_services.hotel_option_review', 'option')
), targets AS (
    SELECT id::text AS target, 'product' AS kind
    FROM travel_service_products WHERE kind = 'hotel'
    UNION ALL
    SELECT o.id::text, 'option' FROM hotel_booking_options o
    JOIN travel_service_products p ON p.id = o.product_id WHERE p.kind = 'hotel'
), scoped AS (
    SELECT a.* FROM admin_audit_logs a
    JOIN actions x ON x.action = a.action
    JOIN targets t ON t.target = a.target AND t.kind = x.kind
), root_actor AS (
    SELECT actor_user_id FROM catalog_review_runs
    WHERE id = '5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a'::uuid
), windows(name, since) AS (VALUES
    ('lifetime', '-infinity'::timestamptz),
    ('since_baseline', '2026-09-08 16:20:20.550803+00'::timestamptz)
)
SELECT 'normal_service_audits' AS section, w.name AS audit_window, x.action,
       count(a.id) AS rows, count(DISTINCT a.actor_user_id) AS distinct_actors,
       count(a.id) FILTER (WHERE a.actor_user_id = (SELECT actor_user_id FROM root_actor))
           AS root_actor_rows,
       count(a.id) FILTER (WHERE a.actor_user_id IS NOT NULL
           AND a.actor_user_id IS DISTINCT FROM (SELECT actor_user_id FROM root_actor))
           AS other_actor_rows,
       count(a.id) FILTER (WHERE a.actor_user_id IS NULL) AS null_actor_rows,
       count(a.id) FILTER (WHERE EXISTS (
           SELECT 1 FROM admin_audit_logs r
           WHERE r.action = 'hotel_catalog_evidence_review'
             AND r.target = 'hotel-review-followup-20260909:' || x.kind || ':' || a.target
             AND r.metadata_json->>'outcome' = 'approved'
             AND r.actor_user_id = a.actor_user_id
       )) AS approved_receipt_target_rows,
       md5(coalesce(string_agg(md5(to_jsonb(a)::text), '' ORDER BY a.id)
           FILTER (WHERE a.id IS NOT NULL), '')) AS rows_md5
FROM actions x CROSS JOIN windows w
LEFT JOIN scoped a ON a.action = x.action AND a.created_at >= w.since
GROUP BY w.name, x.action
ORDER BY w.name, x.action;

SELECT 'travel_service_config' AS section, id, version,
       md5(data::jsonb::text) AS data_md5, md5(to_jsonb(c)::text) AS row_md5
FROM travel_service_config c ORDER BY id;

-- The full-row digest also detects encrypted-secret changes without returning
-- ciphertext. The stable digest excludes health-test observations/timestamps;
-- it still covers config, encrypted secrets, enabled/priority and updater ID.
SELECT 'provider_configs' AS section, count(*) AS rows,
       md5(coalesce(string_agg(md5(to_jsonb(c)::text), '' ORDER BY id), '')) AS full_rows_md5,
       md5(coalesce(string_agg(md5((to_jsonb(c) - ARRAY[
           'created_at', 'updated_at', 'last_tested_at', 'last_test_status', 'last_test_message'
       ])::text), '' ORDER BY id), '')) AS stable_settings_md5
FROM provider_configs c;

-- Brands are shared across service kinds: protect their full table rather than
-- assuming a hotel-specific project_id. Offers and affiliate clicks use hotel scope.
SELECT 'travel_service_brands_all' AS section, count(*) AS rows,
       md5(coalesce(string_agg(md5(to_jsonb(b)::text), '' ORDER BY id), '')) AS rows_md5
FROM travel_service_brands b
UNION ALL
SELECT 'travel_service_offers_hotel', count(*),
       md5(coalesce(string_agg(md5(to_jsonb(o)::text), '' ORDER BY o.id), ''))
FROM travel_service_offers o
JOIN travel_service_products p ON p.id = o.product_id WHERE p.kind = 'hotel'
UNION ALL
SELECT 'destination_affiliate_offers_hotel', count(*),
       md5(coalesce(string_agg(md5(to_jsonb(o)::text), '' ORDER BY id), ''))
FROM destination_affiliate_offers o WHERE module = 'hotel'
UNION ALL
SELECT 'hotel_booking_clicks_all', count(*),
       md5(coalesce(string_agg(md5(to_jsonb(c)::text), '' ORDER BY id), ''))
FROM hotel_booking_clicks c
UNION ALL
SELECT 'affiliate_clicks_hotel', count(*),
       md5(coalesce(string_agg(md5(to_jsonb(c)::text), '' ORDER BY id), ''))
FROM affiliate_clicks c WHERE service_type = 'hotel' OR module = 'hotel'
ORDER BY section;

-- The completed previous batch is immutable. Retain the FULL receipt rows,
-- not only counts/outcome fields, and compare to its independent-after-replay.txt.
-- Source: docs/hotel-review-all-20260908/independent-after-replay.txt, receipt_totals.
-- This section must stay identical before/after/replay; unchanged must remain true.
WITH receipts AS (
    SELECT a.* FROM admin_audit_logs a
    WHERE action = 'hotel_catalog_evidence_review'
      AND target LIKE 'hotel-review-all-20260908:%'
), fingerprints AS (
    SELECT count(*) AS rows, count(DISTINCT target) AS distinct_targets,
           md5(coalesce(string_agg(md5(to_jsonb(receipts)::text), '' ORDER BY id), ''))
               AS rows_md5
    FROM receipts
)
SELECT 'previous_batch_receipts' AS section, 290 AS expected_rows,
       'd31bf5777d5dff64c86693fa74a24324' AS expected_rows_md5,
       rows, distinct_targets, rows_md5,
       rows = 290 AND distinct_targets = 290
           AND rows_md5 = 'd31bf5777d5dff64c86693fa74a24324' AS unchanged
FROM fingerprints;

COMMIT;
