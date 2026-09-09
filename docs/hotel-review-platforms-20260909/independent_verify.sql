-- Platform-source continuation: bounded pinned pending subset, read-only JSON.
-- psql -X -q -v phase=before -v expected_approved=0 \
--   -v 'expected_entries_json=[...]' -f independent_verify.sql > independent-before.json
-- Repeat after / after-replay with identical manifest projection and actual approvals.
-- Projection: [{id,kind,version,before_hash,entry_hash,option_patch:{url,evidence_url}}].
-- Scope is any nonempty subset of the 21 pinned candidates, NOT all 21 by default.
-- Full manifest SHA256 entry hashes must be independently recomputed offline.
-- All approvals here require normal option edit + review (+2 versions). Guard holds
-- must retain the complete before row, including Daiwa's existing non-null URLs.
-- No URL, raw actor UUID, reason, settings, credentials or private metadata is output.
-- metadata_json has PostgreSQL JSON type; cast to JSONB before JSON operators.
-- Output is emitted only after successful ROLLBACK. ON_ERROR_STOP rejects partial runs.
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
\set tag 'hotel-review-platforms-20260909'
\set baseline_at '2026-09-08 23:37:42.330750+00:00'
\set baseline_hash '7b86b02a40dfe00946f1df45d8e201e3dc59bf49066469c30dbfcc60f5628e49'
\set root_id '5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a'
\set baseline_candidates '[{"id":"159bc0b2-5bc7-481e-ba8f-b79bd121e76a","parent_id":"ad6930f9-64e2-4298-b90f-ad24fae50060","provider":"expedia","version":1,"before_hash":"f5ac7f88e01cbce4ad67f34d8e91c2a4dea7d54a495eff9fc7ef25390500a1e3","before_url":null,"before_evidence_url":null},{"id":"2025853a-e016-4b35-b9c1-f44b03c4a0d7","parent_id":"89873ccf-5a45-467d-b2c9-dd32c2b6a0df","provider":"expedia","version":1,"before_hash":"6fbb63fd6cdc68d292e15083a960d46c1e67471820281ce9a86d27e574eea42f","before_url":null,"before_evidence_url":null},{"id":"2279dc5a-7f1f-41b2-ad31-6326ebb24bd9","parent_id":"c934905c-8857-4dfc-963e-9d19e13cd16e","provider":"expedia","version":1,"before_hash":"7da93c6f3749ef9e89e3566ea156534903273991bdcd33cf3a7ff92758aa4f36","before_url":null,"before_evidence_url":null},{"id":"298dd0c5-9786-45b4-b5a5-db049f0a297f","parent_id":"352d2cf2-2a1b-48a4-ad94-3bfaa1a88303","provider":"expedia","version":1,"before_hash":"4555228e890530d668cebacdca914aaebe48cb57fd8131f9fc289d01b6929776","before_url":null,"before_evidence_url":null},{"id":"3d10dc70-0cc8-4f5a-9206-f6c1f6a95317","parent_id":"a5336bb9-321b-40a0-9d87-cf9d1e6d9d9b","provider":"expedia","version":1,"before_hash":"b6f983e380bfdc7e2d40919401844a46c1ac61fa3cab9c4c6ef5e725e0cff45e","before_url":null,"before_evidence_url":null},{"id":"4d2c8a10-e5d1-4334-8bd4-6f4e05c3dbe8","parent_id":"535688c6-4370-4550-9a66-d35c4f907eef","provider":"expedia","version":1,"before_hash":"595043be9efeb6e0eccda247f388497de4e495509c1745907a2814032f5c90b9","before_url":null,"before_evidence_url":null},{"id":"4ed42b59-20e6-4426-8bd4-941ed18e932b","parent_id":"ad6930f9-64e2-4298-b90f-ad24fae50060","provider":"agoda","version":1,"before_hash":"d3446acc74a4c3ed8f06701ac541bf1ac1385775cc06775c009b237b68539867","before_url":null,"before_evidence_url":null},{"id":"504edda5-ffc2-4888-93be-37380242386c","parent_id":"29a7720d-11c2-46ae-abe2-001cd69ac301","provider":"expedia","version":1,"before_hash":"b0b88933bfaf00ae2d0a241350faf3db3f75b7280fbcdbcae122b6684f66ab02","before_url":null,"before_evidence_url":null},{"id":"52c1c7c2-9660-459b-94a9-fe3a0b58a3d9","parent_id":"6b6f2564-93f4-4aff-aa97-bfe34d456cad","provider":"expedia","version":1,"before_hash":"b5ef915beda317762529db228d49f164e586e4244876efdad3fe4239e158faa5","before_url":null,"before_evidence_url":null},{"id":"6f5246ab-96fd-4dfc-aa25-f4cf8ca308a8","parent_id":"352d2cf2-2a1b-48a4-ad94-3bfaa1a88303","provider":"agoda","version":1,"before_hash":"b8f514b16dfef70424757fc4f80864f3419b35037d31a52b61d0b489a3603c83","before_url":null,"before_evidence_url":null},{"id":"853b4a8c-35fd-4585-9ed7-29a8ed1a1e55","parent_id":"68646c86-2aed-4bd6-a453-29450ab50d6c","provider":"expedia","version":1,"before_hash":"c1598fbfbf77c797ad1ec2ae8e2e3dcf244639a8dee3f2c60c6214ce11a5a1d7","before_url":null,"before_evidence_url":null},{"id":"b4a2e4da-e250-4892-b159-a7066d2c6c6a","parent_id":"c934905c-8857-4dfc-963e-9d19e13cd16e","provider":"agoda","version":1,"before_hash":"4d8626876e27572bd748083336b1511f5686a880bb1fd1d4af8f44d1fadfbc9e","before_url":null,"before_evidence_url":null},{"id":"bcb4aa32-4f64-4a88-a8c0-d9f02763a38f","parent_id":"6b6f2564-93f4-4aff-aa97-bfe34d456cad","provider":"agoda","version":1,"before_hash":"3298f4639008b2283dbfe280b9ee61e2672d4a0a2d1fe3aceeaad6ea787f78fa","before_url":null,"before_evidence_url":null},{"id":"c05f72cb-8597-491e-9b53-da8f64f6a4bf","parent_id":"f4dc5d28-5de4-4e81-b79f-f8471f1e4863","provider":"expedia","version":1,"before_hash":"33b9eaab6740faee58a4bc8cc97d843d157ab0a5712c2b39b14468624001025a","before_url":null,"before_evidence_url":null},{"id":"cfa7e834-e904-45da-9d4a-a90bbfcb0945","parent_id":"535688c6-4370-4550-9a66-d35c4f907eef","provider":"agoda","version":1,"before_hash":"d30e7177270b11e169160af593ef6383a8f7d7ed8bdeba4630d9d2613e103b98","before_url":null,"before_evidence_url":null},{"id":"ec0b9313-17c7-454c-801d-4e77f9bb0556","parent_id":"89873ccf-5a45-467d-b2c9-dd32c2b6a0df","provider":"agoda","version":1,"before_hash":"74762f89acf8eef69d4bf76f64709d997aff60ef692033c9dc8282e3c0a1ac8e","before_url":null,"before_evidence_url":null},{"id":"ee94fca7-7a70-4894-b05a-09f4092c811d","parent_id":"c74448b6-1fa7-426e-b5af-17b7d0953382","provider":"expedia","version":1,"before_hash":"2b6ab12321278ca9bc9d425ec217f868e68dc89301d75c9d9ba0e7dc24ef12fe","before_url":null,"before_evidence_url":null},{"id":"efef0014-bb15-46cc-a8c3-5ab5c5de9dd9","parent_id":"68646c86-2aed-4bd6-a453-29450ab50d6c","provider":"agoda","version":1,"before_hash":"5df1a9bc4cdb4370c41f4dc000c9bb8283c327af0cd448f574ca438c85c39332","before_url":null,"before_evidence_url":null},{"id":"f4f26da8-cfa0-42c0-b2a3-01bf6d34bc4d","parent_id":"f73ce087-d361-4f74-8bac-45ed71d5c1ce","provider":"agoda","version":1,"before_hash":"38983ffe92a5f98bf4ee2e823f41beec5787e1c8b25b51d5947596f30152390c","before_url":null,"before_evidence_url":null},{"id":"f62855b8-50a7-4c2f-9ddf-aa1a78948141","parent_id":"a725fc3d-60bc-4f4b-9ca5-00a87ee6af6a","provider":"expedia","version":1,"before_hash":"6ebc84128c66b7587ca6b4da49045e1a5879997d18f1dc241dadfadb7aa6c942","before_url":null,"before_evidence_url":null},{"id":"ff023c57-7f7c-460f-9523-a55805fa42e0","parent_id":"0a47515c-1b5a-4750-9790-1b7969048e30","provider":"agoda","version":1,"before_hash":"467748358abe1502cb2e6486da534e47d52c505f7ec687d3e00cbe2dc04e693d","before_url":"https://www.agoda.com/en-us/daiwa-roynet-hotel-kyoto-terrace-hachijohigashiguchi/hotel/kyoto-jp.html","before_evidence_url":"https://www.daiwaroynet.jp/en/kyoto-terrace/"}]'

BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
SET LOCAL TIME ZONE 'UTC';
WITH expected AS (
    SELECT * FROM jsonb_to_recordset(:'expected_entries_json'::jsonb)
        AS e(id text, kind text, version integer, before_hash text, entry_hash text, option_patch jsonb)
), candidates AS (
    SELECT * FROM jsonb_to_recordset(:'baseline_candidates'::jsonb)
        AS b(id text, parent_id text, provider text, version integer, before_hash text,
             before_url text, before_evidence_url text)
)
SELECT (
    :'phase' IN ('before', 'after', 'after-replay')
    AND (SELECT count(*) FROM expected) BETWEEN 1 AND 21
    AND (SELECT count(DISTINCT id) FROM expected) = (SELECT count(*) FROM expected)
    AND :'expected_approved'::integer BETWEEN 0 AND (SELECT count(*) FROM expected)
    AND (:'phase' <> 'before' OR :'expected_approved'::integer = 0)
    AND NOT EXISTS (
        SELECT 1 FROM expected e LEFT JOIN candidates b USING (id)
        WHERE b.id IS NULL OR e.kind IS DISTINCT FROM 'option'
          OR e.version IS DISTINCT FROM b.version OR e.before_hash IS DISTINCT FROM b.before_hash
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

WITH candidates AS (
    SELECT * FROM jsonb_to_recordset(:'baseline_candidates'::jsonb)
        AS b(id text, parent_id text, provider text, version integer, before_hash text,
             before_url text, before_evidence_url text)
), expected AS (
    SELECT * FROM jsonb_to_recordset(:'expected_entries_json'::jsonb)
        AS e(id text, kind text, version integer, before_hash text, entry_hash text, option_patch jsonb)
), baseline AS (
    -- Only the manifest subset is exempt from full non-scope protection.
    SELECT b.* FROM candidates b JOIN expected e USING (id)
), scope_size AS (
    SELECT count(*)::integer AS n FROM baseline
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
    -- Include out-of-scope hotel mutations, not only desired targets.
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
    -- Current approved selector excludes scope. Illegal non-scope status changes
    -- also alter all products / complete non-scope fingerprints, so cannot evade.
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
    SELECT 'old_hotel_receipts_387', a.id::text, md5(to_jsonb(a)::text)
    FROM admin_audit_logs a WHERE a.action = 'hotel_catalog_evidence_review'
      AND a.target LIKE ANY(ARRAY[
        'hotel-review-all-20260908:%','hotel-review-followup-20260909:%',
        'hotel-review-remaining-20260909:%','hotel-review-redirects-20260909:%'
      ])
), group_specs(name, expected_count) AS (
    SELECT 'all_hotel_products',60
    UNION ALL SELECT 'non_scope_hotel_options',360-n FROM scope_size
    UNION ALL SELECT 'baseline_approved',319
    UNION ALL SELECT 'travel_service_config',NULL::integer
    UNION ALL SELECT 'provider_configs_full',NULL::integer
    UNION ALL SELECT 'provider_configs_stable',NULL::integer
    UNION ALL SELECT 'brands_all',NULL::integer
    UNION ALL SELECT 'hotel_offers',0
    UNION ALL SELECT 'destination_hotel_offers',0
    UNION ALL SELECT 'hotel_booking_clicks_all',0
    UNION ALL SELECT 'affiliate_clicks_hotel',0
    UNION ALL SELECT 'all_historical_audits',NULL::integer
    UNION ALL SELECT 'old_hotel_receipts_387',387
), protected_groups AS (
    SELECT g.name, count(p.id) AS count, g.expected_count,
           CASE WHEN g.expected_count IS NULL THEN NULL ELSE count(p.id) = g.expected_count END AS count_matches,
           md5(coalesce(string_agg(p.row_md5, '' ORDER BY p.id)
               FILTER (WHERE p.id IS NOT NULL), '')) AS rows_md5
    FROM group_specs g LEFT JOIN protected_rows p USING(name) GROUP BY g.name,g.expected_count
), scope_rows AS (
    SELECT b.id, b.parent_id, b.provider AS baseline_provider, b.version AS before_version,
           o.provider, o.status, o.version, o.row_md5,
           o.property_id IS NULL AS property_id_null,
           o.url IS NULL AS url_null, o.evidence_url IS NULL AS evidence_url_null,
           b.before_url IS NULL AS before_url_null,
           b.before_evidence_url IS NULL AS before_evidence_url_null,
           o.url IS NOT DISTINCT FROM b.before_url AS before_url_matches_baseline,
           o.evidence_url IS NOT DISTINCT FROM b.before_evidence_url AS before_evidence_url_matches_baseline,
           o.product_id::text = b.parent_id AS parent_match,
           o.provider IS NOT DISTINCT FROM b.provider AS provider_match,
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
        CASE WHEN :'phase'='before' THEN s.status='pending' AND s.version=s.before_version
                 AND s.before_url_matches_baseline AND s.before_evidence_url_matches_baseline
                 AND s.property_id_null AND s.parent_match AND s.provider_match
             WHEN r.m->>'outcome'='approved' THEN s.status='approved' AND s.version=s.before_version+2
                 AND s.url_matches_manifest AND s.evidence_url_matches_manifest AND s.property_id_null
                 AND s.parent_match AND s.provider_match
                 AND (r.m->>'before_version')::integer=s.before_version
                 AND (r.m->>'after_version')::integer=s.before_version+2
             WHEN r.m->>'outcome'='hold' THEN s.status='pending' AND s.version=s.before_version
                 AND s.before_url_matches_baseline AND s.before_evidence_url_matches_baseline
                 AND s.property_id_null AND s.parent_match AND s.provider_match
                 AND r.m->>'before_hash' IS NOT DISTINCT FROM r.m->>'after_hash'
                 AND (r.m->>'before_version')::integer=s.before_version
                 AND (r.m->>'after_version')::integer=s.before_version
             ELSE false END AS row_transition_valid
    FROM scope_rows s LEFT JOIN receipts r ON r.target=:'tag' || ':option:' || s.id
)
SELECT jsonb_build_object(
    'schema_version',1,'tag',:'tag','phase',:'phase','baseline_hash',:'baseline_hash',
    'baseline_at',:'baseline_at','completed_with','ROLLBACK',
    'expected',jsonb_build_object('scope_count',(SELECT n FROM scope_size),'receipts',
        CASE WHEN :'phase'='before' THEN 0 ELSE (SELECT n FROM scope_size) END,
        'approved',:'expected_approved'::integer,'edits',:'expected_approved'::integer,
        'holds',CASE WHEN :'phase'='before' THEN 0 ELSE (SELECT n FROM scope_size)-:'expected_approved'::integer END),
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
    'interpretation','MD5s are comparison fingerprints, not authorization hashes. Compare every protected group across phases and all hold scope row_md5 values to before, including the existing Daiwa URL slot; recompute entry SHA256 from full manifest and before/after SHA256 from full local snapshots. No private metadata or URLs are emitted.'
) AS report
\gset
ROLLBACK;
\echo :report
