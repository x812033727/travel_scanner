"use client";

import { Check, EyeOff, Gauge, KeyRound, LoaderCircle, PlugZap, RefreshCw, Save, ShieldCheck, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Scalar = string | number | boolean;
type SecretState = { configured: boolean; masked?: string | null; source: string };
type ProviderUsage = {
  period: string;
  period_start: string;
  period_end: string;
  used?: number | null;
  monthly_limit: number;
  remaining?: number | null;
  percentage?: number | null;
  breakdown: Record<string, number>;
  tracking_started_at?: string | null;
  observed_at: string;
  available: boolean;
  scope: string;
};
type ProviderView = {
  provider: string;
  label: string;
  description: string;
  enabled: boolean;
  configured: boolean;
  status: string;
  status_message: string;
  config: Record<string, Scalar | null>;
  config_sources: Record<string, string>;
  secrets: Record<string, SecretState>;
  last_tested_at?: string | null;
  last_test_status?: string | null;
  last_test_message?: string | null;
  updated_at?: string | null;
  usage?: ProviderUsage | null;
  requests_24h?: number;
  errors_24h?: number;
  last_error_at?: string | null;
};
type Audit = { id: string; action: string; target: string; metadata: Record<string, unknown>; created_at: string };
type Snapshot = { providers: ProviderView[]; audit: Audit[]; encryption_source: string };
type Draft = { enabled: boolean; config: Record<string, string>; secrets: Record<string, string>; clearSecrets: string[] };
type FieldMeta = { label: string; type?: "text" | "number" | "url"; options?: Array<{ value: string; label: string }>; help?: string };

const fieldMeta: Record<string, FieldMeta> = {
  ai_planner_mode: { label: "AI 行程來源", options: [{ value: "auto", label: "自動備援" }, { value: "openai", label: "OpenAI／ChatGPT" }, { value: "anthropic", label: "Claude" }, { value: "minimax", label: "MiniMax" }, { value: "fallback", label: "只用內建備援" }, { value: "disabled", label: "停用真實 AI" }] },
  ai_planner_priority: { label: "自動備援順序", help: "用逗號分隔，例如 openai,anthropic,minimax。" },
  ai_planner_timeout_seconds: { label: "每家 AI 逾時（秒）", type: "number" },
  ai_planner_total_timeout_seconds: { label: "整體 AI 逾時（秒）", type: "number" },
  ai_planner_max_output_tokens: { label: "最大輸出 Tokens", type: "number" },
  openai_api_base_url: { label: "OpenAI API Base URL", type: "url" },
  openai_model: { label: "OpenAI 模型" },
  anthropic_api_base_url: { label: "Claude API Base URL", type: "url" },
  anthropic_model: { label: "Claude 模型" },
  minimax_api_base_url: { label: "MiniMax API Base URL", type: "url" },
  minimax_model: { label: "MiniMax 模型" },
  travel_provider_mode: { label: "旅遊資料供應商", options: [{ value: "amadeus", label: "Amadeus" }, { value: "mock", label: "Mock（僅開發）" }, { value: "disabled", label: "停用" }] },
  flight_provider_mode: { label: "航空查詢來源", options: [{ value: "auto", label: "自動：Skyscanner → Duffel → Amadeus" }, { value: "skyscanner", label: "Skyscanner" }, { value: "duffel", label: "Duffel" }, { value: "amadeus", label: "Amadeus" }, { value: "mock", label: "Mock（僅開發）" }, { value: "disabled", label: "停用" }], help: "混合模式會依序補查，直到行程組數達到門檻；追加來源不另扣搜尋次數。" },
  flight_search_strategy: { label: "航空搜尋策略", options: [{ value: "hybrid", label: "混合節流" }, { value: "single", label: "只查首選來源" }] },
  flight_min_result_count: { label: "自動補查門檻", type: "number", help: "去重後少於此行程組數時查詢下一家。" },
  hotel_provider_mode: { label: "飯店查詢來源", options: [{ value: "auto", label: "自動：Booking.com → Amadeus" }, { value: "booking", label: "Booking.com Demand API" }, { value: "amadeus", label: "Amadeus" }, { value: "mock", label: "Mock（僅開發）" }, { value: "disabled", label: "停用" }], help: "自動模式會在 Booking.com Demand API 尚未核准時先使用 Amadeus。" },
  provider_timeout_seconds: { label: "供應商逾時（秒）", type: "number", help: "單次外部請求等待上限。" },
  provider_failure_threshold: { label: "斷路器失敗門檻", type: "number" },
  provider_circuit_seconds: { label: "斷路器暫停秒數", type: "number" },
  route_cache_ttl_seconds: { label: "路線快取秒數", type: "number" },
  google_maps_monthly_request_limit: { label: "每月免費額度參考值", type: "number", help: "預設 10,000 次；用於後臺進度提示，不會自動阻擋 Google API 請求。" },
  amadeus_env: { label: "Amadeus 環境", options: [{ value: "test", label: "Test" }, { value: "production", label: "Production" }] },
  skyscanner_base_url: { label: "API Base URL", type: "url" },
  skyscanner_market: { label: "市場代碼" },
  skyscanner_locale: { label: "語系" },
  skyscanner_currency: { label: "顯示幣別" },
  skyscanner_poll_attempts: { label: "輪詢次數", type: "number" },
  skyscanner_poll_interval_seconds: { label: "輪詢間隔（秒）", type: "number" },
  duffel_env: { label: "Duffel 環境", options: [{ value: "test", label: "Test" }, { value: "live", label: "Live" }] },
  duffel_base_url: { label: "Duffel API Base URL", type: "url" },
  duffel_supplier_timeout_ms: { label: "供應商等待上限（毫秒）", type: "number" },
  flightaware_base_url: { label: "AeroAPI Base URL", type: "url" },
  flightaware_enrich_offer_limit: { label: "自動補充最便宜行程組", type: "number" },
  flightaware_cache_ttl_seconds: { label: "航班動態快取秒數", type: "number" },
  flightaware_track_cache_ttl_seconds: { label: "航跡快取秒數", type: "number" },
  google_travel_impact_base_url: { label: "Travel Impact API Base URL", type: "url" },
  travel_impact_cache_ttl_seconds: { label: "碳排快取秒數", type: "number" },
  navitime_api_base_url: { label: "API Base URL", type: "url" },
  travelpayouts_api_base_url: { label: "Partner Links API Base URL", type: "url" },
  travelpayouts_marker: { label: "Marker" },
  travelpayouts_project_id: { label: "Project ID" },
  travelpayouts_static_url_template: { label: "安全備援合作連結", type: "url", help: "Partner Links API 失敗時才使用；可包含 {destination}、{departure_date}、{return_date}、{sub_id}。" },
  travelpayouts_flight_target_url: { label: "航班原始目標網址", type: "url" },
  travelpayouts_hotel_target_url: { label: "住宿原始目標網址", type: "url" },
  travelpayouts_activities_target_url: { label: "活動原始目標網址", type: "url" },
  travelpayouts_transport_target_url: { label: "交通原始目標網址", type: "url" },
  travelpayouts_allowed_hosts: { label: "允許跳轉網域", help: "以逗號分隔；只允許 HTTPS 且符合清單的網址。" },
  kkday_cid: { label: "KKpartners CID" },
  kkday_affiliate_url_template: { label: "合作連結範本", type: "url" },
  kkday_allowed_hosts: { label: "允許跳轉網域" },
  kkday_api_base_url: { label: "核准後 API Base URL", type: "url" },
  klook_affiliate_url_template: { label: "合作連結範本", type: "url" },
  klook_allowed_hosts: { label: "允許跳轉網域" },
  klook_api_base_url: { label: "核准後 API Base URL", type: "url" },
  airalo_affiliate_url_template: { label: "Impact／Affiliate 合作連結", type: "url" },
  airalo_allowed_hosts: { label: "允許跳轉網域" },
  trip_com_affiliate_url_template: { label: "後台產生的完整合作連結", type: "url", help: "系統不會覆寫既有 Trip.com 追蹤參數。" },
  trip_com_allowed_hosts: { label: "允許跳轉網域" },
  agoda_cid: { label: "Agoda CID" },
  agoda_affiliate_url_template: { label: "合作連結範本", type: "url" },
  agoda_allowed_hosts: { label: "允許跳轉網域" },
  agoda_api_base_url: { label: "核准後 API Base URL", type: "url" },
  booking_affiliate_id: { label: "Booking.com Affiliate ID" },
  booking_affiliate_url_template: { label: "合作連結範本", type: "url" },
  booking_allowed_hosts: { label: "允許跳轉網域" },
  booking_demand_env: { label: "Demand API 環境", options: [{ value: "sandbox", label: "Sandbox" }, { value: "production", label: "Production" }], help: "切換 production 後請儲存並重新執行連線測試。" },
  booking_demand_api_base_url: { label: "Demand API v3.1 Base URL", type: "url", help: "僅允許 Booking.com 官方 sandbox 或 production 網域。" },
  booking_demand_affiliate_id: { label: "Demand API Affiliate ID", help: "與分潤導流 ID 分開保存；留空時才沿用 Affiliate 區塊的 ID。" },
  booking_booker_country: { label: "Booker 國家代碼", help: "兩碼小寫國家代碼；台灣使用 tw。" },
  booking_language: { label: "Booking 回傳語系", help: "例如 zh-tw 或 en-gb。" },
  booking_location_cache_ttl_seconds: { label: "目的地 ID 快取秒數", type: "number" },
  skyscanner_affiliate_url_template: { label: "Impact Affiliate 合作連結", type: "url" },
  skyscanner_affiliate_allowed_hosts: { label: "允許跳轉網域" },
};

const secretLabels: Record<string, { label: string; help?: string }> = {
  openai_api_key: { label: "OpenAI API Key", help: "只在伺服器端加密保存，不會傳到瀏覽器。" },
  anthropic_api_key: { label: "Anthropic API Key", help: "用於 Claude Messages API。" },
  minimax_api_key: { label: "MiniMax API Key", help: "用於 MiniMax Responses API。" },
  google_maps_api_key: { label: "伺服器 API Key", help: "啟用 Places API (New) 與 Routes API；建議限制主機出口 IP。" },
  next_public_google_maps_browser_key: { label: "瀏覽器 Embed Key", help: "只用於 Maps Embed，必須限制 travelscanner.aibubu.cloud HTTP referrer。" },
  amadeus_client_id: { label: "Client ID" },
  amadeus_client_secret: { label: "Client Secret" },
  skyscanner_api_key: { label: "API Key" },
  duffel_access_token: { label: "Access Token" },
  flightaware_api_key: { label: "AeroAPI Key" },
  google_travel_impact_api_key: { label: "Travel Impact API Key" },
  navitime_client_id: { label: "Client ID" },
  navitime_api_key: { label: "API Key" },
  travelpayouts_api_token: { label: "API Token" },
  kkday_api_key: { label: "核准後 API Key" },
  klook_api_key: { label: "核准後 API Key" },
  agoda_api_key: { label: "核准後 API Key" },
  booking_demand_api_token: { label: "Demand API Bearer Token" },
};

const sourceLabel: Record<string, string> = { database: "後台加密設定", environment: "主機環境", none: "未設定", disabled: "已停用" };
const auditActionLabel: Record<string, string> = {
  provider_settings_updated: "更新供應商設定",
  provider_connection_tested: "執行連線測試",
  "admin_role.updated": "更新管理員權限",
};
const dateTime = new Intl.DateTimeFormat("zh-TW", { dateStyle: "medium", timeStyle: "short" });
const dateOnly = new Intl.DateTimeFormat("zh-TW", { dateStyle: "medium", timeZone: "UTC" });
const usageOperationLabel: Record<string, string> = {
  places_autocomplete: "地點自動完成",
  place_details: "地點詳細資料",
  places_text_search: "地點文字搜尋",
  places_photo: "地點照片",
  routes: "路線計算",
};

function auditSummary(metadata: Record<string, unknown>): string {
  for (const field of ["status", "enabled", "is_admin"]) {
    if (field in metadata) return String(metadata[field]);
  }
  return "";
}

function makeDrafts(snapshot: Snapshot): Record<string, Draft> {
  return Object.fromEntries(snapshot.providers.map((provider) => [provider.provider, {
    enabled: provider.enabled,
    config: Object.fromEntries(Object.entries(provider.config).map(([key, value]) => [key, value == null ? "" : String(value)])),
    secrets: Object.fromEntries(Object.keys(provider.secrets).map((key) => [key, ""])),
    clearSecrets: [],
  }]));
}

function valueForApi(key: string, value: string): Scalar {
  return fieldMeta[key]?.type === "number" ? Number(value) : value;
}

function statusClass(status: string) {
  if (status === "ready" || status === "success") return "bg-emerald-50 text-emerald-800";
  if (status === "disabled") return "bg-slate-100 text-slate-700";
  return "bg-amber-50 text-amber-800";
}

export function AdminSettingsPanel() {
  const [snapshot, setSnapshot] = useState<Snapshot>();
  const [drafts, setDrafts] = useState<Record<string, Draft>>({});
  const [loadError, setLoadError] = useState<string>();
  const [busyProvider, setBusyProvider] = useState<string>();
  const [notice, setNotice] = useState<string>();
  const [actionError, setActionError] = useState<string>();
  const [usageRefreshing, setUsageRefreshing] = useState(false);

  useEffect(() => {
    let active = true;
    api<Snapshot>("/admin/provider-settings")
      .then((result) => {
        if (!active) return;
        setSnapshot(result);
        setDrafts(makeDrafts(result));
      })
      .catch((reason: Error) => { if (active) setLoadError(reason.message); });
    return () => { active = false; };
  }, []);

  function patchDraft(provider: string, patch: Partial<Draft>) {
    setDrafts((current) => ({ ...current, [provider]: { ...current[provider], ...patch } }));
  }

  function patchConfig(provider: string, field: string, value: string) {
    const draft = drafts[provider];
    patchDraft(provider, { config: { ...draft.config, [field]: value } });
  }

  function patchSecret(provider: string, field: string, value: string) {
    const draft = drafts[provider];
    patchDraft(provider, {
      secrets: { ...draft.secrets, [field]: value },
      clearSecrets: draft.clearSecrets.filter((item) => item !== field),
    });
  }

  function clearSecret(provider: string, field: string) {
    const draft = drafts[provider];
    patchDraft(provider, {
      secrets: { ...draft.secrets, [field]: "" },
      clearSecrets: [...new Set([...draft.clearSecrets, field])],
    });
  }

  async function refreshUsage() {
    setUsageRefreshing(true); setActionError(undefined);
    try {
      setSnapshot(await api<Snapshot>("/admin/provider-settings"));
    } catch (reason) { setActionError((reason as Error).message); }
    finally { setUsageRefreshing(false); }
  }

  async function save(provider: ProviderView) {
    const draft = drafts[provider.provider];
    setBusyProvider(provider.provider); setActionError(undefined); setNotice(undefined);
    const secrets: Record<string, string | null> = {};
    for (const [key, value] of Object.entries(draft.secrets)) if (value.trim()) secrets[key] = value.trim();
    for (const key of draft.clearSecrets) secrets[key] = null;
    try {
      const result = await api<Snapshot>(`/admin/provider-settings/${provider.provider}`, {
        method: "PUT",
        body: JSON.stringify({
          enabled: provider.provider === "runtime" ? true : draft.enabled,
          config: Object.fromEntries(Object.entries(draft.config).map(([key, value]) => [key, value.trim() === "" ? null : valueForApi(key, value)])),
          secrets,
        }),
      });
      setSnapshot(result); setDrafts(makeDrafts(result));
      setNotice(`${provider.label} 設定已加密儲存並立即套用。`);
    } catch (reason) { setActionError((reason as Error).message); }
    finally { setBusyProvider(undefined); }
  }

  async function testConnection(provider: ProviderView) {
    setBusyProvider(provider.provider); setActionError(undefined); setNotice(undefined);
    try {
      const result = await api<{ status: string; message: string; latency_ms: number }>(`/admin/provider-settings/${provider.provider}/test`, { method: "POST" });
      const resultMessage = `${result.message}（${result.latency_ms} ms）`;
      if (result.status === "success") setNotice(resultMessage);
      else setActionError(resultMessage);
      const refreshed = await api<Snapshot>("/admin/provider-settings");
      setSnapshot(refreshed); setDrafts(makeDrafts(refreshed));
    } catch (reason) { setActionError((reason as Error).message); }
    finally { setBusyProvider(undefined); }
  }

  if (loadError) return <div className="mt-8 rounded-2xl bg-red-50 p-5 text-red-800"><strong>無法開啟管理後台</strong><p className="mt-1 text-sm">{loadError}</p><p className="mt-2 text-xs">請先在主機設定 ADMIN_EMAILS，或將帳號的 is_admin 設為 true。</p></div>;
  if (!snapshot) return <p className="mt-8 flex items-center gap-2 text-[var(--muted)]"><LoaderCircle className="animate-spin" size={18} />正在讀取加密設定…</p>;

  return <div className="mt-8 space-y-6">
    <section className="grid gap-4 rounded-[1.75rem] border border-[var(--line)] bg-[var(--ink)] p-6 text-white md:grid-cols-[auto_1fr] md:items-center"><ShieldCheck size={32} className="text-emerald-200" /><div><h2 className="font-bold">秘密資料不會回傳前端</h2><p className="mt-1 text-sm leading-6 text-white/70">資料庫只保存 Fernet 加密內容；畫面只顯示末四碼。此次使用 {snapshot.encryption_source} 衍生加密金鑰，正式環境建議固定設定 SETTINGS_ENCRYPTION_KEY。</p></div></section>
    {notice && <p role="status" className="flex items-center gap-2 rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800"><Check size={17} />{notice}</p>}
    {actionError && <p role="alert" className="rounded-xl bg-red-50 p-4 text-sm text-red-800">{actionError}</p>}

    <div className="grid gap-6">{snapshot.providers.map((provider) => {
      const draft = drafts[provider.provider];
      const busy = busyProvider === provider.provider;
      const usage = provider.usage;
      const usageWidth = Math.min(100, Math.max(0, usage?.percentage || 0));
      return <section key={provider.provider} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm md:p-7">
        <div className="flex flex-wrap items-start justify-between gap-4"><div className="max-w-2xl"><div className="flex flex-wrap items-center gap-2"><h2 className="text-xl font-bold">{provider.label}</h2><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${statusClass(provider.status)}`}>{provider.status === "ready" ? "已設定" : provider.status === "disabled" ? "已停用" : provider.status === "test_required" ? "待測試" : provider.status === "error" ? "連線失敗" : "待設定"}</span></div><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{provider.description}</p><p className="mt-1 text-xs font-semibold text-[var(--teal)]">{provider.status_message}</p>{provider.provider !== "runtime" && <p className="mt-2 text-xs text-[var(--muted)]">近 24 小時：{provider.requests_24h || 0} 次呼叫 · {provider.errors_24h || 0} 次失敗{provider.last_error_at ? ` · 最近失敗 ${dateTime.format(new Date(provider.last_error_at))}` : ""}</p>}</div>{provider.provider !== "runtime" && <label className="flex items-center gap-2 rounded-full bg-[var(--paper)] px-4 py-2 text-sm font-semibold"><input type="checkbox" checked={draft.enabled} onChange={(event) => patchDraft(provider.provider, { enabled: event.target.checked })} />啟用</label>}</div>

        {provider.provider === "google_maps" && usage && <div className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5" aria-label="Google Maps 本月用量">
          <div className="flex flex-wrap items-start justify-between gap-4"><div><p className="flex items-center gap-2 text-sm font-bold text-[var(--teal)]"><Gauge size={17} />本月 Google API 用量</p>{usage.available ? <p className="mt-2 text-3xl font-bold tabular-nums">{usage.used?.toLocaleString("zh-TW")} <span className="text-base font-medium text-[var(--muted)]">/ {usage.monthly_limit.toLocaleString("zh-TW")} 次</span></p> : <p className="mt-2 font-semibold text-amber-800">目前無法讀取用量計數</p>}</div><button type="button" onClick={refreshUsage} disabled={usageRefreshing} className="flex items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50"><RefreshCw size={15} className={usageRefreshing ? "animate-spin" : ""} />重新整理用量</button></div>
          {usage.available && <><div className="mt-4 h-2.5 overflow-hidden rounded-full bg-white" role="progressbar" aria-label="Google Maps 月用量" aria-valuemin={0} aria-valuemax={usage.monthly_limit} aria-valuenow={usage.used || 0}><div className={`h-full rounded-full ${usageWidth >= 90 ? "bg-red-500" : usageWidth >= 75 ? "bg-amber-500" : "bg-[var(--teal)]"}`} style={{ width: `${usageWidth}%` }} /></div><div className="mt-2 flex flex-wrap justify-between gap-2 text-xs text-[var(--muted)]"><span>已使用 {usage.percentage?.toLocaleString("zh-TW")}%</span><span>剩餘 {(usage.remaining || 0).toLocaleString("zh-TW")} 次</span></div><dl className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-5">{Object.entries(usage.breakdown).map(([operation, count]) => <div key={operation} className="rounded-xl bg-white px-3 py-2"><dt className="text-[.68rem] text-[var(--muted)]">{usageOperationLabel[operation] || operation}</dt><dd className="mt-0.5 font-bold tabular-nums">{count.toLocaleString("zh-TW")}</dd></div>)}</dl></>}
          <p className="mt-4 text-xs leading-5 text-[var(--muted)]">統計期間：{dateOnly.format(new Date(`${usage.period_start}T00:00:00Z`))} 至 {dateOnly.format(new Date(`${usage.period_end}T00:00:00Z`))}。此為本站自導入計數後送出的伺服器 API 請求，不含瀏覽器 Embed 地圖與 Google Cloud 控制台既有歷史；Google 官方帳單仍以 Cloud Console 為準。</p>
        </div>}

        {Object.keys(provider.config).length > 0 && <div className="mt-6 grid gap-4 md:grid-cols-2">{Object.entries(provider.config).map(([field]) => {
          const meta = fieldMeta[field] || { label: field };
          return <label key={field} className="text-sm font-semibold">{meta.label}<span className="ml-2 text-[.65rem] font-normal text-[var(--muted)]">{provider.config_sources[field] === "database" ? "後台值" : "環境預設"}</span>{meta.options ? <select value={draft.config[field]} onChange={(event) => patchConfig(provider.provider, field, event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-normal">{meta.options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select> : <input type={meta.type || "text"} step={meta.type === "number" ? "any" : undefined} value={draft.config[field]} onChange={(event) => patchConfig(provider.provider, field, event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] px-3 py-3 font-normal" />}{meta.help && <span className="mt-1 block text-xs font-normal text-[var(--muted)]">{meta.help}</span>}</label>;
        })}</div>}

        {Object.keys(provider.secrets).length > 0 && <div className="mt-6"><h3 className="flex items-center gap-2 text-sm font-bold"><KeyRound size={16} className="text-[var(--teal)]" />API 金鑰與憑證</h3><div className="mt-3 grid gap-4 md:grid-cols-2">{Object.entries(provider.secrets).map(([field, secret]) => { const meta = secretLabels[field] || { label: field }; const clearing = draft.clearSecrets.includes(field); return <div key={field} className="rounded-2xl bg-[var(--paper)] p-4"><label className="text-sm font-semibold">{meta.label}<input type="password" autoComplete="off" value={draft.secrets[field]} onChange={(event) => patchSecret(provider.provider, field, event.target.value)} placeholder={secret.masked || "貼上新金鑰"} className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-mono text-sm font-normal" /></label><div className="mt-2 flex items-center justify-between gap-3 text-xs text-[var(--muted)]"><span className="flex items-center gap-1"><EyeOff size={13} />{clearing ? "儲存後清除後台值" : sourceLabel[secret.source] || secret.source}</span>{secret.source === "database" && !clearing && <button type="button" onClick={() => clearSecret(provider.provider, field)} className="flex items-center gap-1 font-semibold text-red-700"><Trash2 size={13} />清除</button>}</div>{meta.help && <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{meta.help}</p>}</div>; })}</div></div>}

        <div className="mt-6 flex flex-wrap items-center gap-3"><button type="button" onClick={() => save(provider)} disabled={Boolean(busyProvider)} className="flex items-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 text-sm font-semibold text-white disabled:opacity-50">{busy ? <LoaderCircle size={16} className="animate-spin" /> : <Save size={16} />}儲存設定</button>{provider.provider !== "runtime" && <button type="button" onClick={() => testConnection(provider)} disabled={Boolean(busyProvider) || !draft.enabled} className="flex items-center gap-2 rounded-xl border border-[var(--line)] px-5 py-3 text-sm font-semibold disabled:opacity-40"><PlugZap size={16} />測試連線</button>}<span className="text-xs text-[var(--muted)]">空白金鑰不會覆蓋現有值；清除後會改用主機環境設定。</span></div>
        {provider.last_tested_at && <p className={`mt-4 rounded-xl px-4 py-3 text-sm ${statusClass(provider.last_test_status || "")}`}>上次測試：{dateTime.format(new Date(provider.last_tested_at))} · {provider.last_test_message}</p>}
      </section>;
    })}</div>

    <section className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 md:p-7"><h2 className="text-xl font-bold">最近管理紀錄</h2><p className="mt-1 text-sm text-[var(--muted)]">只記錄變更欄位名稱、操作者與測試結果，不記錄金鑰內容。</p>{snapshot.audit.length ? <ol className="mt-5 divide-y divide-[var(--line)]">{snapshot.audit.map((item) => <li key={item.id} className="grid gap-1 py-3 text-sm md:grid-cols-[10rem_1fr_auto]"><time className="text-[var(--muted)]">{dateTime.format(new Date(item.created_at))}</time><span className="font-semibold">{auditActionLabel[item.action] || item.action} · {item.target}</span><code className="text-xs text-[var(--muted)]">{auditSummary(item.metadata)}</code></li>)}</ol> : <p className="mt-5 rounded-xl bg-[var(--paper)] p-5 text-sm text-[var(--muted)]">尚無管理操作紀錄。</p>}</section>
  </div>;
}
