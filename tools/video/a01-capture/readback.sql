-- Exact A01 projection and global nonterminal jobs. SELECT only.
BEGIN TRANSACTION READ ONLY;
SELECT json_build_object(
  'series', (
    SELECT json_build_object('id', s.id::text, 'slug', s.slug, 'kind', s.kind,
      'status', s.status, 'title', s.title, 'premise', s.premise, 'note', s.note,
      'target_minutes', s.target_minutes, 'planned_episodes', s.planned_episodes,
      'episodes_per_day', s.episodes_per_day, 'image_model', s.image_model,
      'look', s.look, 'style_preset', s.style_preset, 'hands_off', s.hands_off,
      'visual_tier', s.visual_tier, 'compilation', s.compilation)
    FROM video_drama_series s JOIN video_drama_episodes e ON e.series_id = s.id
    WHERE e.slug = 'story-rolling-suitcase-v2'
  ),
  'episode', (
    SELECT json_build_object('id', e.id::text, 'series_id', e.series_id::text,
      'number', e.number, 'slug', e.slug, 'status', e.status)
    FROM video_drama_episodes e WHERE e.slug = 'story-rolling-suitcase-v2'
  ),
  'project', (
    SELECT json_build_object('slug', p.slug, 'format', p.format,
      'series_slug', p.series_slug, 'episode_number', p.episode_number,
      'stage', p.stage, 'retry_request_id', p.retry_request_id::text,
      'retry_acknowledged_id', p.retry_acknowledged_id::text)
    FROM video_projects p WHERE p.slug = 'story-rolling-suitcase-v2'
  ),
  'a01_stage_jobs', (
    SELECT coalesce(json_agg(json_build_object('id', j.id::text,
      'status', j.status, 'request_hash', j.request_hash,
      'input_hash', j.input_hash) ORDER BY j.created_at, j.id), '[]'::json)
    FROM video_stage_jobs j
    WHERE j.request_json->>'slug' = 'story-rolling-suitcase-v2'
  ),
  'a01_media_jobs', (
    SELECT coalesce(json_agg(json_build_object('id', m.id::text,
      'status', m.status, 'kind', m.kind,
      'operation_id', m.request->>'pilot_budget_operation_id')
      ORDER BY m.created_at, m.id), '[]'::json)
    FROM video_media_jobs m WHERE m.slug = 'story-rolling-suitcase-v2'
  ),
  'global_nonterminal_stage_jobs', (
    SELECT coalesce(json_agg(json_build_object('id', j.id::text,
      'status', j.status, 'slug', j.request_json->>'slug')
      ORDER BY j.created_at, j.id), '[]'::json)
    FROM video_stage_jobs j
    -- An uncertain vendor outcome is unresolved even if the queue treats it as terminal.
    WHERE j.status IS NULL OR j.status NOT IN ('succeeded', 'failed', 'canceled', 'cancelled')
  ),
  'global_nonterminal_media_jobs', (
    SELECT coalesce(json_agg(json_build_object('id', m.id::text,
      'status', m.status, 'slug', m.slug)
      ORDER BY m.created_at, m.id), '[]'::json)
    FROM video_media_jobs m
    WHERE m.status IN ('queued', 'submitted')
  )
);
ROLLBACK;
