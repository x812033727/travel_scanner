"use client";

import { Check, EyeOff, KeyRound, LoaderCircle, PlugZap, Save, ShieldCheck, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Scalar = string | number | boolean;
type SecretState = { configured: boolean; masked?: string | null; source: string };
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
};
type Audit = { id: string; action: string; target: string; metadata: Record<string, unknown>; created_at: string };
type Snapshot = { providers: ProviderView[]; audit: Audit[]; encryption_source: string };
type Draft = { enabled: boolean; config: Record<string, string>; secrets: Record<string, string>; clearSecrets: string[] };
type FieldMeta = { label: string; type?: "text" | "number" | "url"; options?: Array<{ value: string; label: string }>; help?: string };

const fieldMeta: Record<string, FieldMeta> = {
  travel_provider_mode: { label: "旅遊資料供應商", options: [{ value: "amadeus", label: "Amadeus" }, { value: "mock", label: "Mock（僅開發）" }, { value: "disabled", label: "停用" }] },
  flight_provider_mode: { label: "航班供應商", options: [{ value: "auto", label: "自動選擇" }, { value: "skyscanner", label: "Skyscanner" }, { value: "amadeus", label: "Amadeus" }, { value: "mock", label: "Mock（僅開發）" }, { value: "disabled", label: "停用" }] },
  provider_timeout_seconds: { label: "供應商逾時（秒）", type: "number", help: "單次外部請求等待上限。" },
  provider_failure_threshold: { label: "斷路器失敗門檻", type: "number" },
  provider_circuit_seconds: { label: "斷路器暫停秒數", type: "number" },
  route_cache_ttl_seconds: { label: "路線快取秒數", type: "number" },
  amadeus_env: { label: "Amadeus 環境", options: [{ value: "test", label: "Test" }, { value: "production", label: "Production" }] },
  skyscanner_base_url: { label: "API Base URL", type: "url" },
  skyscanner_market: { label: "市場代碼" },
  skyscanner_locale: { label: "語系" },
  skyscanner_currency: { label: "顯示幣別" },
  skyscanner_poll_attempts: { label: "輪詢次數", type: "number" },
  skyscanner_poll_interval_seconds: { label: "輪詢間隔（秒）", type: "number" },
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
  booking_demand_api_base_url: { label: "Demand API Base URL", type: "url" },
  skyscanner_affiliate_url_template: { label: "Impact Affiliate 合作連結", type: "url" },
  skyscanner_affiliate_allowed_hosts: { label: "允許跳轉網域" },
};

const secretLabels: Record<string, { label: string; help?: string }> = {
  google_maps_api_key: { label: "伺服器 API Key", help: "啟用 Places API (New) 與 Routes API；建議限制主機出口 IP。" },
  next_public_google_maps_browser_key: { label: "瀏覽器 Embed Key", help: "只用於 Maps Embed，必須限制 travelscanner.aibubu.cloud HTTP referrer。" },
  amadeus_client_id: { label: "Client ID" },
  amadeus_client_secret: { label: "Client Secret" },
  skyscanner_api_key: { label: "API Key" },
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
      return <section key={provider.provider} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5 shadow-sm md:p-7">
        <div className="flex flex-wrap items-start justify-between gap-4"><div className="max-w-2xl"><div className="flex flex-wrap items-center gap-2"><h2 className="text-xl font-bold">{provider.label}</h2><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${statusClass(provider.status)}`}>{provider.status === "ready" ? "已設定" : provider.status === "disabled" ? "已停用" : "待設定"}</span></div><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{provider.description}</p><p className="mt-1 text-xs font-semibold text-[var(--teal)]">{provider.status_message}</p></div>{provider.provider !== "runtime" && <label className="flex items-center gap-2 rounded-full bg-[var(--paper)] px-4 py-2 text-sm font-semibold"><input type="checkbox" checked={draft.enabled} onChange={(event) => patchDraft(provider.provider, { enabled: event.target.checked })} />啟用</label>}</div>

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
