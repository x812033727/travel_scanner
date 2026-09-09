"use client";

import { useEffect, useRef, useState } from "react";
import { useLocale } from "next-intl";
import { Link } from "@/i18n/navigation";
import { ApiError, api } from "@/lib/api";

export const stay22Providers = ["booking", "agoda", "expedia"] as const;
export type Stay22Provider = typeof stay22Providers[number];
export type Stay22Config = { enabled: boolean; aid: string; enabled_providers: Stay22Provider[] };
export const stay22Default: Stay22Config = { enabled: false, aid: "mokaair", enabled_providers: [] };
export const readinessStates = ["existing_affiliate", "stay22_capable", "missing_link", "review_expired", "blocked"] as const;
export type Stay22Readiness = { provider: Stay22Provider } & Record<typeof readinessStates[number], number>;
const providerName: Record<Stay22Provider, string> = { booking: "Booking.com", agoda: "Agoda", expedia: "Expedia" };
const copy = {
  "zh-TW": {
    title: "Stay22 飯店直達分潤", description: "既有分潤優先，Stay22 補缺。只使用已審核的精確飯店連結；不提供即時房價，與住宿地圖開關獨立。",
    enabled: "啟用 Allez 直達分潤", aid: "Stay22 AID", providers: "啟用平台", save: "儲存 Stay22 設定", saving: "正在儲存…",
    saved: "Stay22 設定已儲存", permission: "修改分潤設定需要系統設定管理權限。", unverified: "設定完成不代表分潤追蹤已驗證。請先以帳號少量人工確認落地飯店、日期與 Stay22 Hub 點擊歸屬，再逐平台開啟。",
    refreshFailed: "設定已儲存，但重新載入畫面失敗。請重新載入設定，不必再次儲存。",
    invalid: "請填寫有效 AID，啟用時至少選擇一個平台。", failed: "無法儲存，設定內容已保留，請稍後重試。", conflict: "設定已被其他操作更新。你的輸入已保留，請重新載入最新設定後再修改。",
    reload: "重新載入設定", discard: "重新載入會放棄尚未儲存的 Stay22 變更，是否繼續？", readiness: "平台連結準備度", counts: "以下統計是資料準備度，不是已驗證訂單或佣金；停用開關不影響「可接」統計。",
    existing_affiliate: "既有分潤", stay22_capable: "Stay22 可接", missing_link: "缺少連結", review_expired: "審核過期", blocked: "待審核／需更正", clear: "清除平台篩選", filter: "目前平台篩選", dirty: "Stay22 設定有未儲存的變更。",
  },
  "zh-CN": {
    title: "Stay22 酒店直达分佣", description: "现有分佣优先，Stay22 补缺。仅使用已审核的精确酒店链接；不提供实时房价，与住宿地图开关独立。",
    enabled: "启用 Allez 直达分佣", aid: "Stay22 AID", providers: "启用平台", save: "保存 Stay22 设置", saving: "正在保存…",
    saved: "Stay22 设置已保存", permission: "修改分佣设置需要系统设置管理权限。", unverified: "设置完成不代表分佣追踪已验证。请先通过账号人工确认落地酒店、日期与 Stay22 Hub 点击归属，再逐平台开启。",
    refreshFailed: "设置已保存，但重新加载页面失败。请重新加载设置，无需再次保存。",
    invalid: "请填写有效 AID，启用时至少选择一个平台。", failed: "无法保存，设置内容已保留，请稍后重试。", conflict: "设置已被其他操作更新。你的输入已保留，请重新加载最新设置后再修改。",
    reload: "重新加载设置", discard: "重新加载将放弃尚未保存的 Stay22 更改，是否继续？", readiness: "平台链接准备度", counts: "以下统计是数据准备度，不是已验证订单或佣金；停用开关不影响可接统计。",
    existing_affiliate: "现有分佣", stay22_capable: "Stay22 可接", missing_link: "缺少链接", review_expired: "审核过期", blocked: "待审核／需更正", clear: "清除平台筛选", filter: "当前平台筛选", dirty: "Stay22 设置有未保存的更改。",
  },
  en: {
    title: "Stay22 direct hotel links", description: "Existing affiliates take priority; Stay22 fills gaps using reviewed, exact property links. No live prices; independent of accommodation maps.",
    enabled: "Enable Allez affiliate links", aid: "Stay22 AID", providers: "Enabled platforms", save: "Save Stay22 settings", saving: "Saving…",
    saved: "Stay22 settings saved", permission: "Affiliate changes require settings management capability.", unverified: "Configuration is not tracking verification. Manually confirm the property, dates and click attribution in Stay22 Hub before enabling each platform.",
    refreshFailed: "Settings were saved, but the page could not refresh. Reload the settings; do not save again.",
    invalid: "Enter a valid AID and select at least one platform when enabled.", failed: "Could not save. Your entries are preserved; please retry.", conflict: "Another action updated the settings. Your entries are preserved; reload the latest settings before editing again.",
    reload: "Reload settings", discard: "Reloading discards your unsaved Stay22 changes. Continue?", readiness: "Platform link readiness", counts: "These counts show data readiness, not verified bookings or commissions. Potential coverage is counted even while disabled.",
    existing_affiliate: "Existing affiliate", stay22_capable: "Stay22 eligible", missing_link: "Missing link", review_expired: "Review expired", blocked: "Review or correction needed", clear: "Clear platform filters", filter: "Current platform filter", dirty: "There are unsaved Stay22 changes.",
  },
  ja: {
    title: "Stay22 ホテル直接リンク", description: "既存の提携先を優先し、Stay22 で補完します。審査済みの正確な施設リンクのみ使用します。リアルタイム料金は取得せず、宿泊地図とは独立しています。",
    enabled: "Allez 提携リンクを有効化", aid: "Stay22 AID", providers: "有効なプラットフォーム", save: "Stay22 設定を保存", saving: "保存中…",
    saved: "Stay22 設定を保存しました", permission: "提携設定の変更にはシステム設定管理権限が必要です。", unverified: "設定完了は追跡確認を意味しません。各社を有効にする前に施設・日付・Stay22 Hub のクリック帰属を手動で確認してください。",
    refreshFailed: "設定は保存されましたが、画面を更新できませんでした。再保存せず、設定を再読み込みしてください。",
    invalid: "有効な AID を入力し、有効化する場合はプラットフォームを選択してください。", failed: "保存できませんでした。入力は保持しています。再試行してください。", conflict: "別の操作で設定が変更されました。入力は保持しています。最新の設定を読み込んでから再編集してください。",
    reload: "設定を再読み込み", discard: "未保存の Stay22 設定を破棄して再読み込みしますか？", readiness: "プラットフォーム別リンク状況", counts: "件数はデータの準備状況であり、予約や報酬の確認ではありません。無効時も対応可能な件数を表示します。",
    existing_affiliate: "既存の提携", stay22_capable: "Stay22 対応可能", missing_link: "リンクなし", review_expired: "審査期限切れ", blocked: "審査・修正が必要", clear: "絞り込みを解除", filter: "現在の絞り込み", dirty: "Stay22 設定に未保存の変更があります。",
  },
  ko: {
    title: "Stay22 호텔 바로가기 제휴", description: "기존 제휴를 우선하고 Stay22로 보완합니다. 검토된 정확한 호텔 링크만 사용하며 실시간 가격은 제공하지 않습니다. 숙박 지도와 별도로 설정합니다.",
    enabled: "Allez 제휴 링크 사용", aid: "Stay22 AID", providers: "사용할 플랫폼", save: "Stay22 설정 저장", saving: "저장 중…",
    saved: "Stay22 설정을 저장했습니다", permission: "제휴 설정을 변경하려면 시스템 설정 관리 권한이 필요합니다.", unverified: "설정 완료는 추적 검증을 의미하지 않습니다. 플랫폼별 활성화 전에 호텔, 날짜 및 Stay22 Hub 클릭 귀속을 직접 확인하세요.",
    refreshFailed: "설정은 저장했지만 화면을 새로 고치지 못했습니다. 다시 저장하지 말고 설정을 다시 불러오세요.",
    invalid: "올바른 AID를 입력하고 활성화 시 플랫폼을 하나 이상 선택하세요.", failed: "저장하지 못했습니다. 입력은 유지되며 다시 시도할 수 있습니다.", conflict: "다른 작업으로 설정이 변경되었습니다. 입력은 유지됩니다. 최신 설정을 다시 불러온 후 수정하세요.",
    reload: "설정 다시 불러오기", discard: "저장하지 않은 Stay22 변경을 버리고 다시 불러올까요?", readiness: "플랫폼 링크 준비 상태", counts: "이 수치는 데이터 준비 상태이며 예약이나 수수료 검증이 아닙니다. 비활성 상태에서도 연결 가능 수치를 표시합니다.",
    existing_affiliate: "기존 제휴", stay22_capable: "Stay22 연결 가능", missing_link: "링크 없음", review_expired: "검토 만료", blocked: "검토 또는 수정 필요", clear: "플랫폼 필터 해제", filter: "현재 플랫폼 필터", dirty: "저장하지 않은 Stay22 변경이 있습니다.",
  },
} as const;

export function stay22AdminCopy(locale: string) { return copy[locale as keyof typeof copy] ?? copy.en; }
const field = "min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] px-3 py-2";
const button = "min-h-11 rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-50";

export function Stay22ReadinessPanel({ rows, provider, readiness, destination, status }: {
  rows: Stay22Readiness[]; provider?: string; readiness?: string; destination?: string; status?: string;
}) {
  const t = stay22AdminCopy(useLocale());
  const filters = new URLSearchParams();
  if (destination) filters.set("destination_id", destination);
  if (status) filters.set("status", status);
  const suffix = filters.size ? `&${filters}` : "";
  return <section className="min-w-0 space-y-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
    <h3 className="font-semibold">{t.readiness}</h3><p className="text-sm text-[var(--muted)]">{t.counts}</p>
    {provider && <p className="flex flex-wrap items-center gap-2 text-sm">{t.filter}: {providerName[provider as Stay22Provider] ?? provider} {t[readiness as typeof readinessStates[number]] ?? ""}
      <Link href={`/admin/hotels?tab=review&section=platforms${suffix}`} className={`${button} inline-flex items-center`}>{t.clear}</Link>
    </p>}
    <div className="grid gap-3 lg:grid-cols-3">{rows.map((row) => <article key={row.provider} className="min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] p-3">
      <h4 className="font-semibold">{providerName[row.provider]}</h4><dl className="mt-2 space-y-1">{readinessStates.map((state) => <div key={state} className="flex min-h-11 items-center justify-between gap-2 text-sm">
        <dt>{t[state]}</dt><dd><Link aria-label={`${providerName[row.provider]} · ${t[state]}: ${row[state]}`} className="inline-flex min-h-11 min-w-11 items-center justify-center rounded-lg px-2 font-semibold text-[var(--teal-dark)] underline"
          href={`/admin/hotels?tab=review&section=platforms&booking_provider=${row.provider}&booking_readiness=${state}${suffix}`}>{row[state]}</Link></dd>
      </div>)}</dl>
    </article>)}</div>
  </section>;
}

export function Stay22Admin({ value, version, allowed, onSaved }: {
  value?: Stay22Config; version: number; allowed: boolean; onSaved: () => Promise<void>;
}) {
  const t = stay22AdminCopy(useLocale());
  const [draft, setDraft] = useState<Stay22Config>(value ?? stay22Default);
  const [baseVersion, setBaseVersion] = useState(version);
  const [dirty, setDirty] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [conflict, setConflict] = useState(false);
  const [refreshFailed, setRefreshFailed] = useState(false);
  const dirtyRef = useRef(false);
  const acceptedVersion = useRef(version);
  useEffect(() => {
    if (!dirtyRef.current && version >= acceptedVersion.current) {
      setDraft(value ?? stay22Default);
      setBaseVersion(version);
      acceptedVersion.current = version;
    }
  }, [value, version]);
  function change(next: Stay22Config) {
    dirtyRef.current = true; setDirty(true); setDraft(next); setMessage("");
  }
  async function save() {
    if (!allowed || busy) return;
    if (!/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(draft.aid) || draft.enabled && !draft.enabled_providers.length) {
      setError(t.invalid); return;
    }
    setBusy(true); setError(""); setMessage(""); setRefreshFailed(false);
    try {
      const result = await api<{ version: number }>("/admin/hotels/config", { method: "PATCH", body: JSON.stringify({ version: baseVersion, stay22: draft }) });
      dirtyRef.current = false; setDirty(false); setConflict(false); setBaseVersion(result.version);
      acceptedVersion.current = result.version;
      setMessage(t.saved);
    } catch (reason) {
      const changed = reason instanceof ApiError && reason.code === "service_version_conflict";
      setConflict(changed); setError(changed ? t.conflict : t.failed);
      setBusy(false); return;
    }
    // A failed read cannot undo a successful PATCH or require a second mutation.
    try { await onSaved(); }
    catch { setRefreshFailed(true); setError(t.refreshFailed); }
    finally { setBusy(false); }
  }
  async function reload() {
    if (busy) return;
    if (conflict) {
      if (!window.confirm(t.discard)) return;
      setDraft(value ?? stay22Default); setBaseVersion(version);
      acceptedVersion.current = version; dirtyRef.current = false; setDirty(false);
    }
    setBusy(true);
    try { await onSaved(); setConflict(false); setRefreshFailed(false); setError(""); }
    catch { setError(refreshFailed ? t.refreshFailed : t.failed); }
    finally { setBusy(false); }
  }
  return <form aria-label={t.title} onSubmit={(event) => { event.preventDefault(); void save(); }} className="min-w-0 space-y-4 rounded-2xl border border-[var(--line)] bg-[var(--surface-raised)] p-5">
    <div><h3 className="text-lg font-semibold">{t.title}</h3><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t.description}</p></div>
    <p role="note" className="rounded-xl bg-[var(--teal-soft)] p-3 text-sm leading-6">{t.unverified}</p>
    {!allowed && <p role="note" className="text-sm text-[var(--muted)]">{t.permission}</p>}
    <fieldset disabled={!allowed || busy} className="space-y-4">
      <label className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={draft.enabled} onChange={(event) => change({ ...draft, enabled: event.target.checked })} />{t.enabled}</label>
      <label className="grid max-w-md gap-2 text-sm">{t.aid}<input className={field} autoComplete="off" value={draft.aid} maxLength={128} pattern="[A-Za-z0-9][A-Za-z0-9_-]*" onChange={(event) => change({ ...draft, aid: event.target.value })} /></label>
      <fieldset><legend className="text-sm font-semibold">{t.providers}</legend><div className="mt-2 flex flex-wrap gap-x-5 gap-y-1">{stay22Providers.map((provider) => <label key={provider} className="flex min-h-11 items-center gap-2 text-sm">
        <input type="checkbox" checked={draft.enabled_providers.includes(provider)} onChange={(event) => change({ ...draft, enabled_providers: event.target.checked ? [...draft.enabled_providers, provider] : draft.enabled_providers.filter((item) => item !== provider) })} />{providerName[provider]}
      </label>)}</div></fieldset>
    </fieldset>
    {dirty && <p className="text-sm text-[var(--muted)]">{t.dirty}</p>}
    {error && <p role="alert" className="rounded-xl bg-[var(--coral-soft)] p-3 text-sm">{error}</p>}
    {message && <p role="status" className="text-sm text-[var(--teal-dark)]">{message}</p>}
    <div className="flex flex-wrap gap-2"><button type="submit" disabled={!allowed || busy || !dirty} className={`${button} bg-[var(--teal-soft)] text-[var(--teal-dark)]`}>{busy ? t.saving : t.save}</button>
      {(conflict || refreshFailed) && <button type="button" disabled={busy} className={button} onClick={() => void reload()}>{t.reload}</button>}
    </div>
  </form>;
}
