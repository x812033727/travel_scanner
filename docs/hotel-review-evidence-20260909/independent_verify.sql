-- Mixed hotel evidence continuation; no network or write statement.
-- psql -X -q -v phase=before -v expected_approved=0 \
--   -v 'expected_entries_json=[...]' -f independent_verify.sql > independent-before.json
-- Repeat after / after-replay with identical projection and ACTUAL total approvals.
-- Projection entries: {kind,id,version,before_hash,entry_hash,option_patch OR facts_patch}.
-- Only a nonempty subset of the 19 pinned candidates is accepted. Every requested
-- approval requires normal edit + review (+2 versions); rollback holds change no row.
-- Recompute full manifest entry SHA256 and snapshot row SHA256 independently offline.
-- Raw settings, actor UUID, URLs, reasons and private metadata are never output.
-- All database JSON columns are explicitly cast to JSONB before JSON comparisons.
-- Success JSON is emitted only after ROLLBACK, never from an incomplete transaction.
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
\set tag 'hotel-review-evidence-20260909'
\set baseline_at '2026-09-09 00:32:08.141514+00:00'
\set baseline_hash '342aee9610db65e78626d950efef368919a7d8e4cfcf55d06a32b64e26c5adee'
\set root_id '5d18ecd2-bec0-45ac-84b3-02a13a5cbd6a'
\set baseline_candidates '[{"id":"1a23cbe8-1cd1-4a1d-932a-f3955f567ee4","kind":"option","parent_id":"29a7720d-11c2-46ae-abe2-001cd69ac301","provider":"rakuten","version":1,"before_hash":"dc5675170926dbb6f49a26d9c325a34c52aef6d6671124a43711a0421f388f43","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:osaka:vischio-osaka","destination_id":"osaka","parent_status":"approved"},{"id":"42a3558d-bb99-4312-abe8-e06e080c09a3","kind":"option","parent_id":"50f2d47d-24fe-4b07-85a2-3e1c7671e452","provider":"expedia","version":1,"before_hash":"528f6e3d3f9b33188ea09f76d7ce01ab5dfce19059f712405d83327440b7b49f","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:kyoto:westin-miyako-kyoto","destination_id":"kyoto","parent_status":"pending"},{"id":"545a7eaf-00c9-45a0-b6c2-c1622c210260","kind":"option","parent_id":"a725fc3d-60bc-4f4b-9ca5-00a87ee6af6a","provider":"rakuten","version":1,"before_hash":"4de66b2dee11a833272fea058473067b56b5eb08137e5b0d5f809347aa27bc56","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:osaka:monterey-lasoeur-osaka","destination_id":"osaka","parent_status":"approved"},{"id":"5e832165-9b06-45f3-88c3-ed4c991ea9ff","kind":"option","parent_id":"0a47515c-1b5a-4750-9790-1b7969048e30","provider":"expedia","version":1,"before_hash":"7fe89ab5c35efb07551b133eb0a2fa96a9ab4c937a69a5a40310e81815a60d30","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:kyoto:daiwa-roynet-terrace-hachijo","destination_id":"kyoto","parent_status":"pending"},{"id":"7189583a-865d-4ec6-a4f0-3adcab3b1132","kind":"option","parent_id":"7f1b1d18-215a-4ae8-939b-c106ce224d6f","provider":"expedia","version":1,"before_hash":"c518fca4617dd2d6e8b0c7188ad21543bce4d431644d4432f7878b366d020de4","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:kyoto:mitsui-garden-kyoto-shijo","destination_id":"kyoto","parent_status":"pending"},{"id":"7c0adcfd-3f12-47f4-ac34-9cccd9b940d4","kind":"option","parent_id":"ca55d588-a5dd-4dd9-9c84-72c5e687c48f","provider":"agoda","version":1,"before_hash":"1ea542e79a747a9ab1a9ef242be7b1399d7dafd47d3a90f76352c4d51481cd42","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:tokyo:gracery-asakusa","destination_id":"tokyo","parent_status":"approved"},{"id":"90621e6c-4556-40a6-b08e-6b81b467dfbb","kind":"option","parent_id":"352d2cf2-2a1b-48a4-ad94-3bfaa1a88303","provider":"rakuten","version":1,"before_hash":"987420029ac045f7655b764364aea5c8fc0861f3be3074ce71ab69f2c2dfcdc2","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:osaka:swissotel-nankai-osaka","destination_id":"osaka","parent_status":"approved"},{"id":"93d82747-9209-4d79-88e8-ed51e280e934","kind":"option","parent_id":"028e3657-62f8-4636-9033-ee80ad8fc7f1","provider":"expedia","version":1,"before_hash":"c89c605e8b2d9f02a8388523fbb7489af6b4506dc70145986d18f3c43eab6bac","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:kyoto:royal-park-kyoto-sanjo","destination_id":"kyoto","parent_status":"pending"},{"id":"952a280b-b3d0-465a-a141-8390783df7e6","kind":"option","parent_id":"6b6f2564-93f4-4aff-aa97-bfe34d456cad","provider":"rakuten","version":1,"before_hash":"0998b2f527cf63c7c9ca40e26f018c219bb84f8aedf665521759769a5c4237da","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:osaka:granvia-osaka","destination_id":"osaka","parent_status":"approved"},{"id":"a3c846cd-b509-4dbe-a4eb-f19b388e6268","kind":"option","parent_id":"f4dc5d28-5de4-4e81-b79f-f8471f1e4863","provider":"rakuten","version":1,"before_hash":"145d667bde251ce9f871455ff1ead8b0681e1b4a0cb1c95031d855cd302b6b43","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:osaka:hankyu-respire-osaka","destination_id":"osaka","parent_status":"approved"},{"id":"bf9172d0-5aef-4b36-a1b8-4d4588a8d1f6","kind":"option","parent_id":"a124dc1e-7f75-44ff-b12d-080da031b3b9","provider":"expedia","version":1,"before_hash":"e59805514680c0bd588909b9ee084815123b2ad14c5ff7df6e195ab7691f9044","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:kyoto:granvia-kyoto","destination_id":"kyoto","parent_status":"pending"},{"id":"c59c981f-bf73-4f33-9e79-09c670114a71","kind":"option","parent_id":"a5336bb9-321b-40a0-9d87-cf9d1e6d9d9b","provider":"rakuten","version":1,"before_hash":"df1e19388e5dc87aee148b5b0321c004731d42d6067edb2c9b1d4ce04a1914d5","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:osaka:sotetsu-grand-fresa-osaka-namba","destination_id":"osaka","parent_status":"approved"},{"id":"d1e93ed9-480d-41ba-9ce6-5de4e9d139f1","kind":"option","parent_id":"9cd0788a-a853-4755-bbd4-3e6f64ac0c57","provider":"expedia","version":1,"before_hash":"4ccfa245893c4ca2816c8f2e8faa01dd59f3aea88319c1a732c1be711af1e6bd","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:kyoto:cross-kyoto","destination_id":"kyoto","parent_status":"pending"},{"id":"e5da18b7-0b5e-4e1d-8c38-d76d8b795ac8","kind":"option","parent_id":"b79582da-592f-4a33-aa22-6457cf815094","provider":"agoda","version":1,"before_hash":"42c6f4282130a1166ddff544e38188132bd1b6b0ad328efdb57111a8d8d4813f","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:tokyo:henn-na-premier-tawaramachi","destination_id":"tokyo","parent_status":"approved"},{"id":"f4865301-ce56-442c-b336-5370142f9b49","kind":"option","parent_id":"434dec94-7909-4556-863a-bee68788b642","provider":"expedia","version":1,"before_hash":"8d24a3d2821dbc8e32c73a31d33b06b11abedfbbd65e7361be09c3b8078f890f","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:kyoto:celestine-kyoto-gion","destination_id":"kyoto","parent_status":"pending"},{"id":"fa1dcd2e-db55-4c4f-bac1-009bdacca6b6","kind":"option","parent_id":"c74448b6-1fa7-426e-b5af-17b7d0953382","provider":"rakuten","version":1,"before_hash":"d7d0ea4dc288079e81b5738eecfd6cfb8ea05dbb4ca48b6806033e8e700d7c16","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:osaka:royal-classic-osaka","destination_id":"osaka","parent_status":"approved"},{"id":"fac9680a-a241-4827-8b9e-70ef8758f760","kind":"option","parent_id":"ab8d3a45-10b9-477d-a523-07fc7e2036db","provider":"expedia","version":1,"before_hash":"478dfd953ff21fe7893a93aed1e6f7b3c54b07fd12f7dc1d65c097bcd5be304f","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:kyoto:vischio-kyoto","destination_id":"kyoto","parent_status":"pending"},{"id":"fc367f21-cc02-4999-a159-1f0ecb662faa","kind":"option","parent_id":"758907f4-4870-421e-bf6c-6243cdcc30c4","provider":"expedia","version":1,"before_hash":"cc41ab85bb4550e7765e6861e8d6bc17eb298794cdd227df53fb26641736cdda","before_url":null,"before_evidence_url":null,"before_discovery_status":"unconfirmed","source_key":"editorial:kyoto:miyako-kyoto-hachijo","destination_id":"kyoto","parent_status":"pending"},{"id":"50f2d47d-24fe-4b07-85a2-3e1c7671e452","kind":"product","parent_id":null,"provider":null,"version":1,"before_hash":"39eaef5356258ef4f6e615f3ea5653424193ecdb24b0d1eaca5d7ac8320b515e","before_url":null,"before_evidence_url":null,"before_discovery_status":null,"source_key":"editorial:kyoto:westin-miyako-kyoto","destination_id":"kyoto","parent_status":null}]'
\set westin_before_facts '{"source_credits":[{"title":"旅館業法に基づく許可施設及び施設外玄関帳場一覧（令和８年７月末時点）","publisher":"京都市 保健福祉局 医療衛生推進室 医療衛生センター","url":"https://data.city.kyoto.lg.jp/dataset/00039/","license_name":"CC BY 4.0","license_url":"https://creativecommons.org/licenses/by/4.0/deed.ja","changes":"Mokaair 摘錄京都市 2026 年 7 月底許可清單中的飯店名稱與地址，依官網核對身份並整理住宿區域。原始資料不含座標，未自行猜測或搬用地圖／訂房平台座標、照片、評分、評論及價格；不代表京都市推薦。"}],"country_codes":["JP"],"area_code":"higashiyama","latitude":null,"longitude":null,"coordinate_source_url":null,"google_place_id":null,"naver_map_url":null,"map_verified":false,"facilities":[],"airport":null,"direction":null,"passengers":null,"luggage":null,"languages":[],"attraction_ids":[],"meeting_point":null,"duration_minutes":null,"available_start":null,"available_end":null,"validity_days":null,"data_gb":null,"unlimited":null,"tethering":null,"reference_price":null,"currency":null,"price_checked_at":null}'
\set westin_facts_patch '{"latitude":35.00886111,"longitude":135.78794444,"coordinate_source_url":"https://www.wikidata.org/wiki/Special:EntityData/Q11288502.json?revision=2434981201","source_credits":[{"title":"旅館業法に基づく許可施設及び施設外玄関帳場一覧（令和８年７月末時点）","publisher":"京都市 保健福祉局 医療衛生推進室 医療衛生センター","url":"https://data.city.kyoto.lg.jp/dataset/00039/","license_name":"CC BY 4.0","license_url":"https://creativecommons.org/licenses/by/4.0/deed.ja","changes":"Mokaair 摘錄京都市 2026 年 7 月底許可清單中的飯店名稱與地址，依官網核對身份並整理住宿區域。原始資料不含座標，未自行猜測或搬用地圖／訂房平台座標、照片、評分、評論及價格；不代表京都市推薦。"},{"title":"Wikidata Q11288502 P625 representative hotel point","publisher":"Wikidata contributors","url":"https://www.wikidata.org/wiki/Special:EntityData/Q11288502.json?revision=2434981201","license_name":"CC0-1.0","license_url":"https://creativecommons.org/publicdomain/zero/1.0/","changes":"Selected P625 claim Q11288502$5AB1D2CD-AE18-4CED-892C-97B7269B056A, revision 2434981201; P143 imported from Japanese Wikipedia (Q177837). Alternative P248 Skyscanner (Q1319169) claims excluded. Representative hotel point, not a surveyed entrance; original municipal name/address credit retained."}],"google_place_id":"ChIJN1AzAd8IAWAR2hJ9wcsW4TE","map_verified":true}'

BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
SET LOCAL TIME ZONE 'UTC';
WITH expected AS (
    SELECT * FROM jsonb_to_recordset(:'expected_entries_json'::jsonb)
        AS e(id text, kind text, version integer, before_hash text, entry_hash text,
             option_patch jsonb, facts_patch jsonb)
), candidates AS (
    SELECT * FROM jsonb_to_recordset(:'baseline_candidates'::jsonb)
        AS b(id text, kind text, parent_id text, provider text, version integer,
             before_hash text, before_url text, before_evidence_url text,
             before_discovery_status text, source_key text, destination_id text,
             parent_status text)
)
SELECT (
    :'phase' IN ('before', 'after', 'after-replay')
    AND (SELECT count(*) FROM expected) BETWEEN 1 AND 19
    AND (SELECT count(DISTINCT id) FROM expected) = (SELECT count(*) FROM expected)
    AND :'expected_approved'::integer BETWEEN 0 AND (SELECT count(*) FROM expected)
    AND (:'phase' <> 'before' OR :'expected_approved'::integer = 0)
    AND NOT EXISTS (
        SELECT 1 FROM expected e LEFT JOIN candidates b USING (id)
        WHERE b.id IS NULL OR e.kind IS DISTINCT FROM b.kind
          OR e.version IS DISTINCT FROM b.version OR e.before_hash IS DISTINCT FROM b.before_hash
          OR e.entry_hash IS NULL OR e.entry_hash !~ '^[0-9a-f]{64}$'
          OR (e.kind = 'option' AND (
              jsonb_typeof(e.option_patch) IS DISTINCT FROM 'object'
              OR e.option_patch - ARRAY['url','evidence_url'] <> '{}'::jsonb
              OR jsonb_typeof(e.option_patch->'url') IS DISTINCT FROM 'string'
              OR jsonb_typeof(e.option_patch->'evidence_url') IS DISTINCT FROM 'string'
              OR e.option_patch->>'url' NOT LIKE 'https://%'
              OR e.option_patch->>'evidence_url' NOT LIKE 'https://%'
              OR coalesce(e.facts_patch,'null'::jsonb) <> 'null'::jsonb
          ))
          OR (e.kind = 'product' AND (
              e.id <> '50f2d47d-24fe-4b07-85a2-3e1c7671e452'
              OR e.facts_patch IS DISTINCT FROM :'westin_facts_patch'::jsonb
              OR coalesce(e.option_patch,'null'::jsonb) <> 'null'::jsonb
          ))
    )
    AND NOT EXISTS (
        SELECT 1 FROM jsonb_array_elements(:'expected_entries_json'::jsonb) e
        WHERE e - ARRAY['id','kind','version','before_hash','entry_hash',
                        'option_patch','facts_patch'] <> '{}'::jsonb
          OR jsonb_typeof(e->'version') IS DISTINCT FROM 'number'
    )
) AS inputs_valid
\gset
\if :inputs_valid
\else
SELECT 1 / 0 AS invalid_verification_inputs;
\endif

WITH candidates AS (
    SELECT * FROM jsonb_to_recordset(:'baseline_candidates'::jsonb)
        AS b(id text, kind text, parent_id text, provider text, version integer,
             before_hash text, before_url text, before_evidence_url text,
             before_discovery_status text, source_key text, destination_id text,
             parent_status text)
), expected AS (
    SELECT * FROM jsonb_to_recordset(:'expected_entries_json'::jsonb)
        AS e(id text, kind text, version integer, before_hash text, entry_hash text,
             option_patch jsonb, facts_patch jsonb)
), baseline AS (
    SELECT b.* FROM candidates b JOIN expected e USING (id,kind)
), scope_size AS (
    SELECT count(*)::integer AS n,
           count(*) FILTER (WHERE kind='product')::integer AS product_n,
           count(*) FILTER (WHERE kind='option')::integer AS option_n FROM baseline
), root_actor AS (
    SELECT r.actor_user_id, r.mode, u.is_active,
        (SELECT count(*) FROM admin_audit_logs a
         WHERE a.action='catalog_review_requested'
           AND a.target='catalog-review:' || :'root_id'
           AND a.actor_user_id=r.actor_user_id) AS requested_audits
    FROM catalog_review_runs r JOIN users u ON u.id=r.actor_user_id
    WHERE r.id=:'root_id'::uuid
), products AS (
    SELECT p.*, to_jsonb(p) AS row_json, md5(to_jsonb(p)::text) AS row_md5
    FROM travel_service_products p WHERE p.kind='hotel'
), options AS (
    SELECT o.*, to_jsonb(o) AS row_json, md5(to_jsonb(o)::text) AS row_md5
    FROM hotel_booking_options o JOIN products p ON p.id=o.product_id
), receipts AS (
    SELECT a.id,a.target,a.actor_user_id,a.created_at,a.metadata_json::jsonb AS m,
           md5(to_jsonb(a)::text) AS row_md5
    FROM admin_audit_logs a
    WHERE a.action='hotel_catalog_evidence_review' AND a.target LIKE :'tag' || ':%'
), normal_audits AS (
    -- Include every hotel normal mutation since the baseline, even out of scope.
    SELECT a.id,a.action,a.target,a.actor_user_id,a.created_at,
           md5(to_jsonb(a)::text) AS row_md5,
           EXISTS (SELECT 1 FROM baseline b WHERE b.id=a.target
             AND b.kind=CASE WHEN a.action IN (
                 'travel_services.hotel_option_edit','travel_services.hotel_option_review'
             ) THEN 'option' ELSE 'product' END) AS in_scope
    FROM admin_audit_logs a WHERE a.created_at >= :'baseline_at'::timestamptz
      AND (
        (a.action IN ('travel_services.hotel_option_edit','travel_services.hotel_option_review')
          AND EXISTS (SELECT 1 FROM options o WHERE o.id::text=a.target))
        OR (a.action IN ('travel_services.product_edit','travel_services.product_review')
          AND EXISTS (SELECT 1 FROM products p WHERE p.id::text=a.target))
      )
), protected_rows AS (
    SELECT 'non_scope_hotel_products' AS name,p.id::text AS id,p.row_md5 FROM products p
    WHERE NOT EXISTS (SELECT 1 FROM baseline b WHERE b.kind='product' AND b.id=p.id::text)
    UNION ALL
    SELECT 'non_scope_hotel_options',o.id::text,o.row_md5 FROM options o
    WHERE NOT EXISTS (SELECT 1 FROM baseline b WHERE b.kind='option' AND b.id=o.id::text)
    UNION ALL
    -- Any illegal non-scope status change also alters the complete non-scope hash.
    SELECT 'baseline_approved','product:' || p.id::text,p.row_md5 FROM products p
    WHERE p.status='approved'
      AND NOT EXISTS (SELECT 1 FROM baseline b WHERE b.kind='product' AND b.id=p.id::text)
    UNION ALL
    SELECT 'baseline_approved','option:' || o.id::text,o.row_md5 FROM options o
    WHERE o.status='approved'
      AND NOT EXISTS (SELECT 1 FROM baseline b WHERE b.kind='option' AND b.id=o.id::text)
    UNION ALL
    SELECT 'travel_service_config',c.id::text,md5(to_jsonb(c)::text) FROM travel_service_config c
    UNION ALL
    SELECT 'provider_configs_full',c.id::text,md5(to_jsonb(c)::text) FROM provider_configs c
    UNION ALL
    SELECT 'provider_configs_stable',c.id::text,md5((to_jsonb(c) - ARRAY[
        'created_at','updated_at','last_tested_at','last_test_status','last_test_message'
    ])::text) FROM provider_configs c
    UNION ALL
    -- to_jsonb includes every deployed brand column, including new 0064 channels.
    SELECT 'brands_all',b.id::text,md5(to_jsonb(b)::text) FROM travel_service_brands b
    UNION ALL
    SELECT 'hotel_offers',o.id::text,md5(to_jsonb(o)::text)
    FROM travel_service_offers o JOIN products p ON p.id=o.product_id
    UNION ALL
    SELECT 'destination_hotel_offers',o.id::text,md5(to_jsonb(o)::text)
    FROM destination_affiliate_offers o WHERE o.module='hotel'
    UNION ALL
    SELECT 'hotel_booking_clicks_all',c.id::text,md5(to_jsonb(c)::text) FROM hotel_booking_clicks c
    UNION ALL
    SELECT 'affiliate_clicks_hotel',c.id::text,md5(to_jsonb(c)::text)
    FROM affiliate_clicks c WHERE c.service_type='hotel' OR c.module='hotel'
    UNION ALL
    SELECT 'all_historical_audits',a.id::text,md5(to_jsonb(a)::text)
    FROM admin_audit_logs a WHERE a.created_at < :'baseline_at'::timestamptz
    UNION ALL
    SELECT 'old_hotel_receipts_408',a.id::text,md5(to_jsonb(a)::text)
    FROM admin_audit_logs a WHERE a.action='hotel_catalog_evidence_review'
      AND a.target LIKE ANY(ARRAY[
        'hotel-review-all-20260908:%','hotel-review-followup-20260909:%',
        'hotel-review-remaining-20260909:%','hotel-review-redirects-20260909:%',
        'hotel-review-platforms-20260909:%'
      ])
), group_specs(name,expected_count) AS (
    SELECT 'non_scope_hotel_products',60-product_n FROM scope_size
    UNION ALL SELECT 'non_scope_hotel_options',360-option_n FROM scope_size
    UNION ALL SELECT 'baseline_approved',340
    UNION ALL SELECT 'travel_service_config',NULL::integer
    UNION ALL SELECT 'provider_configs_full',NULL::integer
    UNION ALL SELECT 'provider_configs_stable',NULL::integer
    UNION ALL SELECT 'brands_all',NULL::integer
    UNION ALL SELECT 'hotel_offers',0
    UNION ALL SELECT 'destination_hotel_offers',0
    UNION ALL SELECT 'hotel_booking_clicks_all',0
    UNION ALL SELECT 'affiliate_clicks_hotel',0
    UNION ALL SELECT 'all_historical_audits',NULL::integer
    UNION ALL SELECT 'old_hotel_receipts_408',408
), protected_groups AS (
    SELECT g.name,count(p.id) AS count,g.expected_count,
           CASE WHEN g.expected_count IS NULL THEN NULL
                ELSE count(p.id)=g.expected_count END AS count_matches,
           md5(coalesce(string_agg(p.row_md5,'' ORDER BY p.id)
               FILTER (WHERE p.id IS NOT NULL),'')) AS rows_md5
    FROM group_specs g LEFT JOIN protected_rows p USING(name) GROUP BY g.name,g.expected_count
), scope_rows AS (
    SELECT b.id,b.kind,b.parent_id,b.provider AS baseline_provider,b.version AS before_version,
           b.before_hash,b.source_key AS baseline_source_key,b.destination_id AS baseline_destination_id,
           b.parent_status AS baseline_parent_status,
           o.provider,coalesce(o.status,p.status) AS status,coalesce(o.version,p.version) AS version,
           coalesce(o.row_md5,p.row_md5) AS row_md5,
           CASE WHEN b.kind='option' THEN md5((o.row_json - ARRAY[
               'url','evidence_url','discovery_status','identity_note','status','version',
               'verified_at','checked_at','health_status','updated_at'])::text)
             ELSE md5(((p.row_json - ARRAY['facts','status','version','verified_at','updated_at'])
               || jsonb_build_object('facts',p.facts::jsonb - ARRAY[
                   'google_place_id','map_verified','latitude','longitude',
                   'coordinate_source_url','source_credits']))::text) END AS immutable_fields_md5,
           CASE WHEN b.kind='option' THEN o.property_id IS NULL END AS property_id_null,
           CASE WHEN b.kind='option' THEN o.url IS NULL END AS url_null,
           CASE WHEN b.kind='option' THEN o.evidence_url IS NULL END AS evidence_url_null,
           CASE WHEN b.kind='option' THEN b.before_url IS NULL END AS before_url_null,
           CASE WHEN b.kind='option' THEN b.before_evidence_url IS NULL END AS before_evidence_url_null,
           CASE WHEN b.kind='option' THEN o.url IS NOT DISTINCT FROM b.before_url END AS before_url_matches_baseline,
           CASE WHEN b.kind='option' THEN o.evidence_url IS NOT DISTINCT FROM b.before_evidence_url END AS before_evidence_url_matches_baseline,
           CASE WHEN b.kind='option' THEN o.discovery_status IS NOT DISTINCT FROM b.before_discovery_status END AS before_discovery_matches_baseline,
           CASE WHEN b.kind='option' THEN o.product_id::text=b.parent_id END AS parent_match,
           CASE WHEN b.kind='option' THEN o.provider IS NOT DISTINCT FROM b.provider END AS provider_match,
           parent.status AS parent_status,parent.destination_id AS parent_destination_id,
           EXISTS (SELECT 1 FROM baseline bp WHERE bp.kind='product' AND bp.id=b.parent_id) AS parent_in_scope,
           CASE WHEN b.kind='option' THEN o.url IS NOT DISTINCT FROM e.option_patch->>'url' END AS url_matches_manifest,
           CASE WHEN b.kind='option' THEN o.evidence_url IS NOT DISTINCT FROM e.option_patch->>'evidence_url' END AS evidence_url_matches_manifest,
           CASE WHEN b.kind='option' THEN o.discovery_status='found' END AS discovery_found,
           o.health_status,
           CASE WHEN b.kind='product' THEN p.kind='hotel' AND p.source_key=b.source_key
               AND p.destination_id=b.destination_id END AS product_identity_matches_baseline,
           CASE WHEN b.kind='product' THEN p.facts::jsonb=:'westin_before_facts'::jsonb END AS before_facts_matches_baseline,
           CASE WHEN b.kind='product' THEN p.facts::jsonb=(
               :'westin_before_facts'::jsonb || e.facts_patch) END AS facts_patch_matches_manifest,
           CASE WHEN b.kind='product' THEN (p.facts::jsonb - ARRAY[
               'google_place_id','map_verified','latitude','longitude','coordinate_source_url','source_credits'])
             = (:'westin_before_facts'::jsonb - ARRAY[
               'google_place_id','map_verified','latitude','longitude','coordinate_source_url','source_credits'])
             END AS non_patch_facts_match
    FROM baseline b JOIN expected e ON e.id=b.id AND e.kind=b.kind
    LEFT JOIN options o ON b.kind='option' AND o.id::text=b.id
    LEFT JOIN products p ON b.kind='product' AND p.id::text=b.id
    LEFT JOIN products parent ON b.kind='option' AND parent.id::text=b.parent_id
), receipt_details AS (
    SELECT r.id AS receipt_id,r.target,r.created_at,r.row_md5,
           r.actor_user_id=(SELECT actor_user_id FROM root_actor) AS actor_root_match,
           r.actor_user_id IS NULL AS actor_null,
           r.m->>'kind' AS kind,r.m->>'target_id' AS target_id,
           r.m->>'requested_decision' AS requested_decision,r.m->>'outcome' AS outcome,
           r.m->>'guard_code' AS guard_code,r.m->>'entry_hash' AS entry_hash,
           r.m->>'before_hash' AS before_hash,r.m->>'after_hash' AS after_hash,
           (r.m->>'before_version')::integer AS before_version,
           (r.m->>'after_version')::integer AS after_version,
           r.m->>'browser_verified' AS browser_verified,
           r.m->>'tag' IS NOT DISTINCT FROM :'tag'
             AND r.m->>'root_run_id' IS NOT DISTINCT FROM :'root_id'
             AND r.m->>'baseline_hash' IS NOT DISTINCT FROM :'baseline_hash' AS provenance_match,
           e.id IS NOT NULL AND r.target=:'tag' || ':' || e.kind || ':' || e.id
             AND r.m->>'kind'=e.kind AS scope_match,
           r.m->>'entry_hash' IS NOT DISTINCT FROM e.entry_hash AS entry_hash_match,
           r.m->>'before_hash' IS NOT DISTINCT FROM b.before_hash AS before_hash_match,
           coalesce(r.m->'option_patch','null'::jsonb)
             IS NOT DISTINCT FROM coalesce(e.option_patch,'null'::jsonb) AS option_patch_match,
           CASE WHEN e.kind='option' THEN coalesce(r.m->'evidence','null'::jsonb)='null'::jsonb
             ELSE
               r.m#>>'{evidence,map,place_id}'=e.facts_patch->>'google_place_id'
               AND r.m#>>'{evidence,map,identity_verified}'='true'
               AND r.m#>>'{evidence,map,method}'='iab'
               AND r.m#>>'{evidence,coordinates,url}'=e.facts_patch->>'coordinate_source_url'
               AND r.m#>>'{evidence,coordinates,license_url}'='https://creativecommons.org/publicdomain/zero/1.0/'
               AND r.m#>>'{evidence,coordinates,non_google}'='true'
               AND r.m#>>'{evidence,coordinates,qid}'='Q11288502'
               AND r.m#>>'{evidence,coordinates,claim_id}'='Q11288502$5AB1D2CD-AE18-4CED-892C-97B7269B056A'
               AND r.m#>>'{evidence,coordinates,revision}'='2434981201'
               AND r.m#>>'{evidence,coordinates,reference}'='P143:Q177837'
             END AS evidence_binding_match,
           r.m->>'after_hash' ~ '^[0-9a-f]{64}$' AS after_hash_valid
    FROM receipts r LEFT JOIN expected e
      ON e.id=r.m->>'target_id' AND e.kind=r.m->>'kind'
    LEFT JOIN baseline b ON b.id=e.id AND b.kind=e.kind
), entry_checks AS (
    SELECT s.id,s.kind,
        (SELECT count(*) FROM receipts r WHERE r.target=:'tag' || ':' || s.kind || ':' || s.id) AS receipt_count,
        (SELECT count(*) FROM normal_audits a WHERE a.target=s.id
          AND a.action=CASE WHEN s.kind='option' THEN 'travel_services.hotel_option_edit'
            ELSE 'travel_services.product_edit' END) AS edit_audit_count,
        (SELECT count(*) FROM normal_audits a WHERE a.target=s.id
          AND a.action=CASE WHEN s.kind='option' THEN 'travel_services.hotel_option_review'
            ELSE 'travel_services.product_review' END) AS review_audit_count,
        r.m->>'outcome' AS outcome,
        CASE WHEN :'phase'='before' THEN s.status='pending' AND s.version=s.before_version
               AND CASE WHEN s.kind='option' THEN s.before_url_matches_baseline
                 AND s.before_evidence_url_matches_baseline AND s.before_discovery_matches_baseline
                 AND s.property_id_null AND s.parent_match AND s.provider_match
                 ELSE s.before_facts_matches_baseline AND s.product_identity_matches_baseline END
             WHEN r.m->>'outcome'='approved' THEN s.status='approved' AND s.version=s.before_version+2
               AND (r.m->>'before_version')::integer=s.before_version
               AND (r.m->>'after_version')::integer=s.before_version+2
               AND CASE WHEN s.kind='option' THEN s.url_matches_manifest
                 AND s.evidence_url_matches_manifest AND s.property_id_null
                 AND s.parent_match AND s.provider_match AND s.discovery_found
                 AND s.health_status NOT IN ('unsafe','unavailable')
                 ELSE s.product_identity_matches_baseline AND s.facts_patch_matches_manifest
                   AND s.non_patch_facts_match END
             WHEN r.m->>'outcome'='hold' THEN s.status='pending' AND s.version=s.before_version
               AND r.m->>'before_hash' IS NOT DISTINCT FROM r.m->>'after_hash'
               AND (r.m->>'before_version')::integer=s.before_version
               AND (r.m->>'after_version')::integer=s.before_version
               AND CASE WHEN s.kind='option' THEN s.before_url_matches_baseline
                 AND s.before_evidence_url_matches_baseline AND s.before_discovery_matches_baseline
                 AND s.property_id_null AND s.parent_match AND s.provider_match
                 ELSE s.before_facts_matches_baseline AND s.product_identity_matches_baseline END
             ELSE false END AS row_transition_valid
    FROM scope_rows s LEFT JOIN receipts r ON r.target=:'tag' || ':' || s.kind || ':' || s.id
)
SELECT jsonb_build_object(
    'schema_version',1,'tag',:'tag','phase',:'phase','baseline_hash',:'baseline_hash',
    'baseline_at',:'baseline_at','completed_with','ROLLBACK',
    'expected',jsonb_build_object('scope_count',(SELECT n FROM scope_size),
        'product_scope_count',(SELECT product_n FROM scope_size),
        'option_scope_count',(SELECT option_n FROM scope_size),
        'receipts',CASE WHEN :'phase'='before' THEN 0 ELSE (SELECT n FROM scope_size) END,
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
    'scope_rows',(SELECT jsonb_agg(to_jsonb(s) ORDER BY kind,id) FROM scope_rows s),
    'receipts',coalesce((SELECT jsonb_agg(to_jsonb(r) ORDER BY target,receipt_id)
        FROM receipt_details r),'[]'::jsonb),
    'receipt_totals',jsonb_build_object('count',(SELECT count(*) FROM receipts),
        'distinct_targets',(SELECT count(DISTINCT target) FROM receipts),
        'approved',(SELECT count(*) FROM receipts WHERE m->>'outcome'='approved'),
        'approved_products',(SELECT count(*) FROM receipts WHERE m->>'outcome'='approved' AND m->>'kind'='product'),
        'approved_options',(SELECT count(*) FROM receipts WHERE m->>'outcome'='approved' AND m->>'kind'='option'),
        'holds',(SELECT count(*) FROM receipts WHERE m->>'outcome'='hold'),
        'rows_md5',(SELECT md5(coalesce(string_agg(row_md5,'' ORDER BY id),'')) FROM receipts)),
    'normal_audits',coalesce((SELECT jsonb_agg(jsonb_build_object(
        'audit_id',a.id,'action',a.action,'target',a.target,'created_at',a.created_at,
        'row_md5',a.row_md5,'in_scope',a.in_scope,
        'actor_root_match',a.actor_user_id=(SELECT actor_user_id FROM root_actor),
        'actor_null',a.actor_user_id IS NULL) ORDER BY a.target,a.action,a.id)
        FROM normal_audits a),'[]'::jsonb),
    'entry_checks',(SELECT jsonb_agg(to_jsonb(e) ORDER BY kind,id) FROM entry_checks e),
    'interpretation','MD5s are comparison fingerprints, not authorization hashes. Compare all protected groups across phases, all scope immutable_fields_md5 across phases and each hold row_md5 against before. Recompute full manifest entry SHA256 and complete snapshot row SHA256 offline. Product facts_patch is NOT stored in core receipts: exact facts are checked from the row and evidence binds the receipt to map/CC0 provenance. No private metadata or URLs are emitted.'
) AS report
\gset
ROLLBACK;
\echo :report
