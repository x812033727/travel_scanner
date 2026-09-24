import type { GuideDocument } from "@/lib/guides";

export const newsLocales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
export type NewsLocale = typeof newsLocales[number];
export type NewsVertical = "ai" | "tech" | "crypto";

export type NewsSource = {
  id: string; name: string; url: string; format: "rss" | "atom" | "json" | "api" | "html";
  role: "evidence" | "lead_only"; vertical: NewsVertical | "mixed"; is_first_party: boolean;
  enabled: boolean; scan_interval_minutes: number; allowed_redirect_hosts: string[];
  config: Record<string, unknown>; etag: string | null; last_modified: string | null;
  last_scanned_at: string | null; next_scan_at: string; last_status: string;
  last_error: string | null; consecutive_failures: number; created_at: string; updated_at: string;
};

export type NewsGate = {
  vertical: NewsVertical; days: number; labelled_candidates: number; agreements: number;
  agreement_rate: number; serious_false_positives: number; eligible: boolean; reasons: string[];
};

export const newsProviders = ["openai", "anthropic", "minimax", "gemini"] as const;
export type NewsProvider = typeof newsProviders[number];
// Vendor and product names; the same in every locale.
export const newsProviderLabels: Record<NewsProvider, string> = {
  openai: "OpenAI", anthropic: "Anthropic Claude", minimax: "MiniMax", gemini: "Google Gemini",
};

// One entry of the server's model catalog (app/ai/catalog.py), filtered to the models the
// vendor's news adapter can drive.
export type NewsModelOption = {
  value: string; label: string; description: string | null; status: "stable" | "preview" | "retired";
};

export type NewsSettings = {
  enabled: boolean; mode: "shadow" | "automatic";
  writer_provider: NewsProvider; writer_model: string | null;
  verifier_provider: NewsProvider; verifier_model: string | null;
  global_concurrency: number; per_vertical_concurrency: number; min_shadow_days: number;
  min_shadow_candidates: number; min_human_agreement: number; jev_act_confidence: number;
  auto_publish_ai: boolean; auto_publish_tech: boolean; auto_publish_crypto: boolean;
  prompt_version: string; policy_version: string; gates: Record<NewsVertical, NewsGate>;
  // Read-only: the dropdown options and the model an empty choice runs on.
  model_options?: Partial<Record<NewsProvider, NewsModelOption[]>>;
  default_models?: Partial<Record<NewsProvider, string>>;
  updated_at: string;
};

export type NewsCandidateSummary = {
  id: string; vertical: NewsVertical; status: string; source_title: string; canonical_url: string;
  event_date: string | null; would_publish: boolean | null; human_decision: "publish" | "reject" | null;
  error_code: string | null; error_detail: string | null; guide_article_id: string | null;
  created_at: string; updated_at: string;
};

export type NewsCandidatePage = {
  candidates: NewsCandidateSummary[]; total: number; page: number; pages: number;
};

export type NewsEvidence = {
  id: string; role: "evidence" | "lead_only"; is_first_party: boolean; url: string;
  title: string; retrieved_at: string; source_date: string | null; content_hash: string; excerpt: string;
};

export type NewsAssessment = {
  id: string; assessment_type: string; locale: NewsLocale | null; verdict: string;
  confidence: number | null; provider: string | null; model: string | null;
  reasons: string[]; details: Record<string, unknown>; created_at: string;
};

export type NewsRun = {
  id: string; stage: string; status: string; attempt: number; provider: string | null;
  model: string | null; input_tokens: number; output_tokens: number; error_code: string | null;
  error_detail: string | null; metadata: Record<string, unknown>; started_at: string;
  finished_at: string | null;
};

export type NewsCandidate = NewsCandidateSummary & {
  evidence: NewsEvidence[]; assessments: NewsAssessment[]; runs: NewsRun[];
  documents: Partial<Record<NewsLocale, GuideDocument>>; claim_ledger: Array<Record<string, unknown>>;
  lint: Record<string, string[]>; human_reason: string | null; human_major_error: boolean;
};

export type NewsStats = {
  pending_review: number; failed: number; published: number; queue_by_status: Record<string, number>;
  pipeline_runs: number; pipeline_failures: number; input_tokens: number; output_tokens: number;
};
