-- Exact three redirected Agoda null-slot reviews; read-only JSON diagnostics.
-- psql -X -q -v phase=before -v expected_approved=0 \
--   -v 'expected_entries_json=[...]' -f independent_verify.sql > independent-before.json
-- Repeat after/after-replay with the SAME manifest projection and actual approved count.
-- expected_entries_json is an array of {id,kind,version,before_hash,entry_hash,option_patch}.
-- option_patch = {url,evidence_url}; entry_hash is operator digest(full manifest entry).
-- The offline verifier MUST recompute entry hashes from the original manifest.
-- No raw actor UUID, reason, URLs, settings, ciphertext or other private metadata is emitted.
-- PostgreSQL metadata_json is JSON: explicitly cast to JSONB before operators.
-- The final JSON is emitted ONLY AFTER successful ROLLBACK; errors stop before output.
\set ON_ERROR_STOP on
\set QUIET on
\pset format unaligned
\pset tuples_only on
\pset footer off
\if :{?phase}
\else
SELECT 1 / 0 AS missing_phase;
\endif
\if :{?expected_approved}
\else
SELECT 1 / 0 AS missing_expected_approved;
\endif
\if :{?expected_entries_json}
\else
SELECT 1 / 0 AS missing_expected_entries_json;
\endif
\set tag 'hotel-review-redirects-20260909'
\set baseline_at '2026-09-08 23:08:17.381350+00:00'
\set baseline_hash '14978ec20e1b05f7f5991194c9568f56bb6da93486c91105ebc5391dc4fad56d'
\set root_id '5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a'
\set baseline_entries '[{"id":"00307d02-975e-4b2f-8843-df7000cd7c50","parent_id":"71374dce-0786-413b-aafd-b63c7d9a3786","before_hash":"5c58741036a5b4506718b8ebb10515135d14c51a42f3365f35a621cad2681b2d"},{"id":"2c41cd84-0813-42cf-8a54-003bc6f0cff4","parent_id":"6e824f93-a049-4a32-9df4-fe17dc4d3974","before_hash":"4f20257f0de198a3cdda37341391509b64cf8c4d0f1d95ce90d8c5d6221cdcff"},{"id":"d55df51d-b401-468a-8149-bec50508b4c2","parent_id":"4938181e-0007-4143-aa0c-4b5ed44f4f8b","before_hash":"f2b2bf01a6274d334cb9381c91f24d7670cf6970e2db41c29de74280e903ab6f"}]'

BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
SET LOCAL TIME ZONE 'UTC';
WITH expected AS (
    SELECT * FROM jsonb_to_recordset(:'expected_entries_json'::jsonb)
        AS e(id text, kind text, version integer, before_hash text, entry_hash text, option_patch jsonb)
), baseline AS (
    SELECT * FROM jsonb_to_recordset(:'baseline_entries'::jsonb)
        AS b(id text, parent_id text, before_hash text)
)
SELECT (
    :'phase' IN ('before', 'after', 'after-replay')
    AND :'expected_approved'::integer BETWEEN 0 AND 3
    AND (:'phase' <> 'before' OR :'expected_approved'::integer = 0)
    AND (SELECT count(*) FROM expected) = 3
    AND (SELECT count(DISTINCT id) FROM expected) = 3
    AND NOT EXISTS (
        SELECT 1 FROM expected e LEFT JOIN baseline b USING (id)
        WHERE b.id IS NULL OR e.kind IS DISTINCT FROM 'option' OR e.version IS DISTINCT FROM 1
          OR e.before_hash IS DISTINCT FROM b.before_hash
          OR e.entry_hash IS NULL OR e.entry_hash !~ '^[0-9a-f]{64}$'
          OR jsonb_typeof(e.option_patch) IS DISTINCT FROM 'object'
          OR e.option_patch - ARRAY['url', 'evidence_url'] <> '{}'::jsonb
          OR jsonb_typeof(e.option_patch->'url') IS DISTINCT FROM 'string'
          OR jsonb_typeof(e.option_patch->'evidence_url') IS DISTINCT FROM 'string'
          OR e.option_patch->>'url' NOT LIKE 'https://%'
          OR e.option_patch->>'evidence_url' NOT LIKE 'https://%'
    )
    AND NOT EXISTS (
        SELECT 1 FROM jsonb_array_elements(:'expected_entries_json'::jsonb) e
        WHERE e - ARRAY['id','kind','version','before_hash','entry_hash','option_patch'] <> '{}'::jsonb
    )
) AS inputs_valid
\gset
\if :inputs_valid
\else
SELECT 1 / 0 AS invalid_verification_inputs;
\endif

WITH baseline AS (
    SELECT * FROM jsonb_to_recordset(:'baseline_entries'::jsonb)
        AS b(id text, parent_id text, before_hash text)
), expected AS (
    SELECT * FROM jsonb_to_recordset(:'expected_entries_json'::jsonb)
        AS e(id text, kind text, version integer, before_hash text, entry_hash text, option_patch jsonb)
), root_actor AS (
    SELECT r.actor_user_id, r.mode, u.is_active,
        (SELECT count(*) FROM admin_audit_logs a
         WHERE a.action = 'catalog_review_requested'
           AND a.target = 'catalog-review:' || :'root_id'
           AND a.actor_user_id = r.actor_user_id) AS requested_audits
    FROM catalog_review_runs r JOIN users u ON u.id = r.actor_user_id
    WHERE r.id = :'root_id'::uuid
), products AS (
    SELECT p.*, md5(to_jsonb(p)::text) AS row_md5
    FROM travel_service_products p WHERE p.kind = 'hotel'
), options AS (
    SELECT o.*, md5(to_jsonb(o)::text) AS row_md5
    FROM hotel_booking_options o JOIN products p ON p.id = o.product_id
), receipts AS (
    SELECT a.id, a.target, a.actor_user_id, a.created_at, a.metadata_json::jsonb AS m,
           md5(to_jsonb(a)::text) AS row_md5
    FROM admin_audit_logs a
    WHERE a.action = 'hotel_catalog_evidence_review' AND a.target LIKE :'tag' || ':%'
), normal_audits AS (
    SELECT a.id, a.action, a.target, a.actor_user_id, a.created_at,
           md5(to_jsonb(a)::text) AS row_md5,
           EXISTS (SELECT 1 FROM baseline b WHERE b.id = a.target) AS in_scope
    FROM admin_audit_logs a WHERE a.created_at >= :'baseline_at'::timestamptz
      AND (
        (a.action IN ('travel_services.hotel_option_edit','travel_services.hotel_option_review')
            AND EXISTS (SELECT 1 FROM options o WHERE o.id::text = a.target))
        OR (a.action IN ('travel_services.product_edit','travel_services.product_review')
            AND EXISTS (SELECT 1 FROM products p WHERE p.id::text = a.target))
      )
), protected_rows AS (
    SELECT 'all_hotel_products' AS name, p.id::text AS id, p.row_md5 FROM products p
    UNION ALL
    SELECT 'non_scope_hotel_options', o.id::text, o.row_md5 FROM options o
    WHERE NOT EXISTS (SELECT 1 FROM baseline b WHERE b.id = o.id::text)
    UNION ALL
    -- New approvals are excluded. Any illegal non-scope status change is ALSO
    -- caught by the full 357-row fingerprint, preventing mutable-status evasion.
    SELECT 'baseline_approved', 'product:' || p.id::text, p.row_md5
    FROM products p WHERE p.status = 'approved'
    UNION ALL
    SELECT 'baseline_approved', 'option:' || o.id::text, o.row_md5 FROM options o
    WHERE o.status = 'approved' AND NOT EXISTS (SELECT 1 FROM baseline b WHERE b.id = o.id::text)
    UNION ALL
    SELECT 'travel_service_config', c.id::text, md5(to_jsonb(c)::text) FROM travel_service_config c
    UNION ALL
    SELECT 'provider_configs_full', c.id::text, md5(to_jsonb(c)::text) FROM provider_configs c
    UNION ALL
    SELECT 'provider_configs_stable', c.id::text, md5((to_jsonb(c) - ARRAY[
        'created_at','updated_at','last_tested_at','last_test_status','last_test_message'
    ])::text) FROM provider_configs c
    UNION ALL
    SELECT 'brands_all', b.id::text, md5(to_jsonb(b)::text) FROM travel_service_brands b
    UNION ALL
    SELECT 'hotel_offers', o.id::text, md5(to_jsonb(o)::text)
    FROM travel_service_offers o JOIN products p ON p.id = o.product_id
    UNION ALL
    SELECT 'destination_hotel_offers', o.id::text, md5(to_jsonb(o)::text)
    FROM destination_affiliate_offers o WHERE o.module = 'hotel'
    UNION ALL
    SELECT 'hotel_booking_clicks_all', c.id::text, md5(to_jsonb(c)::text) FROM hotel_booking_clicks c
    UNION ALL
    SELECT 'affiliate_clicks_hotel', c.id::text, md5(to_jsonb(c)::text)
    FROM affiliate_clicks c WHERE c.service_type = 'hotel' OR c.module = 'hotel'
    UNION ALL
    SELECT 'all_historical_audits', a.id::text, md5(to_jsonb(a)::text)
    FROM admin_audit_logs a WHERE a.created_at < :'baseline_at'::timestamptz
    UNION ALL
    SELECT 'old_hotel_receipts_384', a.id::text, md5(to_jsonb(a)::text)
    FROM admin_audit_logs a WHERE a.action = 'hotel_catalog_evidence_review'
      AND a.target LIKE ANY(ARRAY[
        'hotel-review-all-20260908:%','hotel-review-followup-20260909:%',
        'hotel-review-remaining-20260909:%'
      ])
), group_specs(name, expected_count) AS (VALUES
    ('all_hotel_products',60),('non_scope_hotel_options',357),('baseline_approved',316),
    ('travel_service_config',NULL::integer),('provider_configs_full',NULL::integer),
    ('provider_configs_stable',NULL::integer),('brands_all',NULL::integer),
    ('hotel_offers',0),('destination_hotel_offers',0),('hotel_booking_clicks_all',0),
    ('affiliate_clicks_hotel',0),('all_historical_audits',NULL::integer),('old_hotel_receipts_384',384)
), protected_groups AS (
    SELECT g.name, count(p.id) AS count, g.expected_count,
           CASE WHEN g.expected_count IS NULL THEN NULL ELSE count(p.id) = g.expected_count END AS count_matches,
           md5(coalesce(string_agg(p.row_md5, '' ORDER BY p.id)
               FILTER (WHERE p.id IS NOT NULL), '')) AS rows_md5
    FROM group_specs g LEFT JOIN protected_rows p USING(name) GROUP BY g.name,g.expected_count
), scope_rows AS (
    SELECT b.id, b.parent_id, o.provider, o.status, o.version, o.row_md5,
           o.property_id IS NULL AS property_id_null, o.url IS NULL AS url_null,
           o.evidence_url IS NULL AS evidence_url_null,
           o.product_id::text = b.parent_id AS parent_match,
           p.status AS parent_status, p.destination_id AS parent_destination_id,
           o.url IS NOT DISTINCT FROM e.option_patch->>'url' AS url_matches_manifest,
           o.evidence_url IS NOT DISTINCT FROM e.option_patch->>'evidence_url' AS evidence_url_matches_manifest
    FROM baseline b LEFT JOIN options o ON o.id::text = b.id
    LEFT JOIN products p ON p.id::text = b.parent_id JOIN expected e ON e.id = b.id
), receipt_details AS (
    SELECT r.id AS receipt_id, r.target, r.created_at, r.row_md5,
           r.actor_user_id = (SELECT actor_user_id FROM root_actor) AS actor_root_match,
           r.actor_user_id IS NULL AS actor_null,
           r.m->>'kind' AS kind, r.m->>'target_id' AS target_id,
           r.m->>'requested_decision' AS requested_decision, r.m->>'outcome' AS outcome,
           r.m->>'guard_code' AS guard_code, r.m->>'entry_hash' AS entry_hash,
           r.m->>'before_hash' AS before_hash, r.m->>'after_hash' AS after_hash,
           (r.m->>'before_version')::integer AS before_version,
           (r.m->>'after_version')::integer AS after_version,
           r.m->>'browser_verified' AS browser_verified,
           r.m->>'tag' IS NOT DISTINCT FROM :'tag'
             AND r.m->>'root_run_id' IS NOT DISTINCT FROM :'root_id'
             AND r.m->>'baseline_hash' IS NOT DISTINCT FROM :'baseline_hash' AS provenance_match,
           e.id IS NOT NULL AND r.target = :'tag' || ':option:' || e.id
             AND r.m->>'kind' = 'option' AS scope_match,
           r.m->>'entry_hash' IS NOT DISTINCT FROM e.entry_hash AS entry_hash_match,
           r.m->>'before_hash' IS NOT DISTINCT FROM b.before_hash AS before_hash_match,
           r.m->'option_patch' IS NOT DISTINCT FROM e.option_patch AS option_patch_match,
           r.m->>'after_hash' ~ '^[0-9a-f]{64}$' AS after_hash_valid
    FROM receipts r LEFT JOIN expected e ON e.id = r.m->>'target_id'
    LEFT JOIN baseline b ON b.id = e.id
), entry_checks AS (
    SELECT s.id,
        (SELECT count(*) FROM receipts r WHERE r.target = :'tag' || ':option:' || s.id) AS receipt_count,
        (SELECT count(*) FROM normal_audits a WHERE a.target=s.id
            AND a.action='travel_services.hotel_option_edit') AS edit_audit_count,
        (SELECT count(*) FROM normal_audits a WHERE a.target=s.id
            AND a.action='travel_services.hotel_option_review') AS review_audit_count,
        r.m->>'outcome' AS outcome,
        CASE WHEN :'phase'='before' THEN s.status='pending' AND s.version=1
                 AND s.url_null AND s.property_id_null
             WHEN r.m->>'outcome'='approved' THEN s.status='approved' AND s.version=3
                 AND s.url_matches_manifest AND s.evidence_url_matches_manifest AND s.property_id_null
                 AND (r.m->>'before_version')::integer=1 AND (r.m->>'after_version')::integer=3
             WHEN r.m->>'outcome'='hold' THEN s.status='pending' AND s.version=1
                 AND s.url_null AND s.property_id_null
                 AND r.m->>'before_hash' IS NOT DISTINCT FROM r.m->>'after_hash'
                 AND (r.m->>'before_version')::integer=1 AND (r.m->>'after_version')::integer=1
             ELSE false END AS row_transition_valid
    FROM scope_rows s LEFT JOIN receipts r ON r.target=:'tag' || ':option:' || s.id
)
SELECT jsonb_build_object(
    'schema_version',1,'tag',:'tag','phase',:'phase','baseline_hash',:'baseline_hash',
    'baseline_at',:'baseline_at','completed_with','ROLLBACK',
    'expected',jsonb_build_object('scope_count',3,'receipts',
        CASE WHEN :'phase'='before' THEN 0 ELSE 3 END,
        'approved',:'expected_approved'::integer,'edits',:'expected_approved'::integer,
        'holds',CASE WHEN :'phase'='before' THEN 0 ELSE 3-:'expected_approved'::integer END),
    'snapshot',jsonb_build_object('captured_at',transaction_timestamp(),
        'isolation_level',current_setting('transaction_isolation'),
        'read_only',current_setting('transaction_read_only'),
        'matching_roots',(SELECT count(*) FROM root_actor),
        'review_pending_roots',(SELECT count(*) FROM root_actor WHERE mode='review_pending'),
        'active_actors',(SELECT count(*) FROM root_actor WHERE is_active),
        'authenticated_request_audits',(SELECT coalesce(sum(requested_audits),0) FROM root_actor)),
    'inventory',jsonb_build_object('hotel_products',(SELECT count(*) FROM products),
        'hotel_options',(SELECT count(*) FROM options),
        'approved_products',(SELECT count(*) FROM products WHERE status='approved'),
        'approved_options',(SELECT count(*) FROM options WHERE status='approved')),
    'protected_groups',(SELECT jsonb_agg(to_jsonb(g) ORDER BY name) FROM protected_groups g),
    'scope_rows',(SELECT jsonb_agg(to_jsonb(s) ORDER BY id) FROM scope_rows s),
    'receipts',coalesce((SELECT jsonb_agg(to_jsonb(r) ORDER BY target,receipt_id)
        FROM receipt_details r),'[]'::jsonb),
    'receipt_totals',jsonb_build_object('count',(SELECT count(*) FROM receipts),
        'distinct_targets',(SELECT count(DISTINCT target) FROM receipts),
        'approved',(SELECT count(*) FROM receipts WHERE m->>'outcome'='approved'),
        'holds',(SELECT count(*) FROM receipts WHERE m->>'outcome'='hold'),
        'rows_md5',(SELECT md5(coalesce(string_agg(row_md5,'' ORDER BY id),'')) FROM receipts)),
    'normal_audits',coalesce((SELECT jsonb_agg(jsonb_build_object(
        'audit_id',a.id,'action',a.action,'target',a.target,'created_at',a.created_at,
        'row_md5',a.row_md5,'in_scope',a.in_scope,
        'actor_root_match',a.actor_user_id=(SELECT actor_user_id FROM root_actor),
        'actor_null',a.actor_user_id IS NULL) ORDER BY a.target,a.action,a.id)
        FROM normal_audits a),'[]'::jsonb),
    'entry_checks',(SELECT jsonb_agg(to_jsonb(e) ORDER BY id) FROM entry_checks e),
    'interpretation','Comparison MD5s are not authorization hashes. Compare all protected groups across phases and hold scope row hashes to before; recompute expected entry SHA256 from the full local manifest. No private metadata or URLs are emitted.'
) AS report
\gset
ROLLBACK;
\echo :report
