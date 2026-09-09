"use client";

import { useEffect, useRef, useState } from "react";
import { useLocale } from "next-intl";
import { Link } from "@/i18n/navigation";
import { ApiError, api } from "@/lib/api";

export const stay22Providers = ["booking", "agoda", "expedia"] as const;
export type Stay22Provider = typeof stay22Providers[number];
export type Stay22Config = {
  enabled: boolean; aid: string; enabled_providers: Stay22Provider[];
  integration_mode?: "allez" | "script"; lma_id?: string | null;
};
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

const moduleCopy = {
  "zh-TW": {
    enabled: "啟用 Stay22 導流模組",
    description: "原生 Allez 保留既有分潤優先；完整 Script 在公開住宿頁轉換支援的原始連結。兩種方式皆不提供即時房價，與住宿地圖開關獨立。",
    module: "導流模組", savedMode: "已儲存模式", previewMode: "未儲存預覽", original: "原始渠道",
    integration: "Stay22 整合方式", allez: "Allez 精確連結", script: "完整 Script ＋原生 Allez",
    off: "關閉後恢復既有分潤／普通連結政策；AID、Script ID 與平台選擇會保留。",
    on: "Allez 保留既有分潤優先，只對已審核且勾選的平台補上 Stay22。",
    scope: "完整 Script 在獨立公開住宿頁運作，包含七平台 LinkSwap、Spark、Nova；不在管理後台或私人旅程頁載入，也不在同一文件載入 Travelpayouts Drive。",
    native: "下方平台選擇只控制原生按鈕的 Allez。Script 的七平台、Spark、Nova 由 Stay22 Hub 管理，不受這三個勾選框限制。",
    directPolicy: "Script 需要同時開啟普通飯店連結，讓程式被阻擋時仍可使用原網址；普通連結關閉時 Script 不會載入，原生 Allez 仍依原設定運作。",
    reloadScript: "關閉設定不能撤回已執行的第三方程式；已開啟的 Script 頁必須重新載入。設定失敗、非正式網域或 DNT／GPC 下不載入 Script。",
    invalidScript: "請填寫 24 碼十六進位的 LMA Script ID。", hub: "開啟 Stay22 Script Builder",
  },
  "zh-CN": {
    enabled: "启用 Stay22 导流模块",
    description: "原生 Allez 保留现有分佣优先；完整 Script 在公开住宿页面转换支持的原始链接。两种方式均不提供实时房价，与住宿地图开关独立。",
    module: "导流模块", savedMode: "已保存模式", previewMode: "未保存预览", original: "原始渠道",
    integration: "Stay22 集成方式", allez: "Allez 精确链接", script: "完整 Script ＋原生 Allez",
    off: "关闭后恢复现有分佣／普通链接规则；保留 AID、Script ID 和平台选择。",
    on: "Allez 保留现有分佣优先，仅为已审核且选中的平台补充 Stay22。",
    scope: "完整 Script 在独立公开住宿页面运行，包括七平台 LinkSwap、Spark、Nova；不在后台或私人行程页加载，也不在同一文档加载 Travelpayouts Drive。",
    native: "下方平台选择仅控制原生按钮的 Allez。Script 的七平台、Spark、Nova 由 Stay22 Hub 管理，不受这三个选框限制。",
    directPolicy: "Script 需要同时开启普通酒店链接，以便程序被阻止时仍可使用原网址；普通链接关闭时不加载 Script，原生 Allez 仍按原设置运行。",
    reloadScript: "关闭设置无法撤回已执行的第三方程序；已打开的 Script 页面需要重新加载。设置失败、非正式域名或 DNT／GPC 下不加载 Script。",
    invalidScript: "请输入 24 位十六进制 LMA Script ID。", hub: "打开 Stay22 Script Builder",
  },
  en: {
    enabled: "Enable Stay22 clickout module",
    description: "Native Allez preserves existing-affiliate priority; full Script converts supported original links on public hotel pages. Neither provides live prices; accommodation maps remain independent.",
    module: "Clickout module", savedMode: "Saved mode", previewMode: "Unsaved preview", original: "Original channels",
    integration: "Stay22 integration", allez: "Allez exact links", script: "Full Script + native Allez",
    off: "Off restores existing affiliate and ordinary-link policies. AID, Script ID and platform choices are retained.",
    on: "Allez preserves existing-affiliate priority and fills gaps for reviewed, selected platforms.",
    scope: "The full Script runs in a separate public hotel document with seven-platform LinkSwap, Spark and Nova. It is not loaded in admin or private itinerary pages, or alongside Travelpayouts Drive in the same document.",
    native: "Platform selections below control native Allez buttons only. The Script's seven platforms, Spark and Nova are controlled by Stay22 Hub, not these three checkboxes.",
    directPolicy: "Script also requires ordinary hotel links to be enabled, so original URLs remain usable if the SDK is blocked. With ordinary links off, Script does not load; native Allez keeps its existing settings.",
    reloadScript: "Disabling cannot undo third-party code already executed; reload open Script pages. Configuration failures, non-production origins and DNT/GPC prevent loading.",
    invalidScript: "Enter a 24-character hexadecimal LMA Script ID.", hub: "Open Stay22 Script Builder",
  },
  ja: {
    enabled: "Stay22 送客モジュールを有効化",
    description: "既存ボタンの Allez は従来の提携を優先します。完全な Script は公開宿泊ページの対応する元リンクを変換します。リアルタイム料金は取得せず、宿泊地図とは独立しています。",
    module: "送客モジュール", savedMode: "保存済みモード", previewMode: "未保存のプレビュー", original: "元のチャネル",
    integration: "Stay22 連携方式", allez: "Allez 施設直接リンク", script: "完全な Script ＋既存ボタンの Allez",
    off: "無効にすると既存の提携・通常リンクの方針に戻ります。AID、Script ID、選択先は保持します。",
    on: "Allez は既存提携を優先し、審査済みの選択先を Stay22 で補完します。",
    scope: "完全な Script は独立した公開宿泊ページで動作し、7 社の LinkSwap、Spark、Nova を含みます。管理・非公開旅程ページでは読み込まず、同じ文書で Travelpayouts Drive を読み込みません。",
    native: "下の選択は既存ボタンの Allez のみを制御します。Script の7社、Spark、Nova は Stay22 Hub で管理し、この3つの選択では制限できません。",
    directPolicy: "Script には通常のホテルリンクの有効化も必要です。SDK が遮断されても元の URL を使用できるためです。通常リンクが無効なら Script は読み込まず、既存の Allez 設定を維持します。",
    reloadScript: "無効化しても実行済みの外部コードは取り消せません。開いている Script ページを再読み込みしてください。設定エラー、正式サイト以外、DNT／GPC では読み込みません。",
    invalidScript: "24 桁の16進数の LMA Script ID を入力してください。", hub: "Stay22 Script Builder を開く",
  },
  ko: {
    enabled: "Stay22 제휴 모듈 사용",
    description: "기존 버튼 Allez는 기존 제휴를 우선하며 전체 Script는 공개 숙박 페이지의 지원 원본 링크를 변환합니다. 실시간 가격은 제공하지 않으며 숙박 지도와 별개입니다.",
    module: "제휴 이동 모듈", savedMode: "저장된 모드", previewMode: "저장 전 미리보기", original: "기존 채널",
    integration: "Stay22 연동 방식", allez: "Allez 호텔 직접 링크", script: "전체 Script ＋기존 버튼 Allez",
    off: "끄면 기존 제휴 및 일반 링크 정책으로 돌아갑니다. AID, Script ID와 플랫폼 선택은 유지됩니다.",
    on: "Allez는 기존 제휴를 우선하며 검토된 선택 플랫폼에 Stay22를 보완합니다.",
    scope: "전체 Script는 별도의 공개 숙박 문서에서 7개 플랫폼 LinkSwap, Spark, Nova를 실행합니다. 관리 및 비공개 여행 페이지에서 로드하지 않으며 같은 문서에서 Travelpayouts Drive를 함께 로드하지 않습니다.",
    native: "아래 플랫폼 선택은 기존 Allez 버튼만 제어합니다. Script의 7개 플랫폼, Spark, Nova는 Stay22 Hub에서 관리하며 이 세 체크박스로 제한되지 않습니다.",
    directPolicy: "SDK가 차단되어도 원래 URL을 사용할 수 있도록 일반 호텔 링크도 켜야 합니다. 일반 링크를 끄면 Script는 로드되지 않으며 기존 Allez 설정은 유지됩니다.",
    reloadScript: "비활성화해도 이미 실행된 외부 코드는 취소되지 않습니다. 열린 Script 페이지를 새로 고치세요. 설정 오류, 운영 도메인 외부, DNT／GPC에서는 로드하지 않습니다.",
    invalidScript: "24자리 16진수 LMA Script ID를 입력하세요.", hub: "Stay22 Script Builder 열기",
  },
} as const;

export function stay22AdminCopy(locale: string) {
  const key = locale in copy ? locale as keyof typeof copy : "en";
  return { ...copy[key], ...moduleCopy[key] };
}
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
  const [persisted, setPersisted] = useState<Stay22Config>(value ?? stay22Default);
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
      setPersisted(value ?? stay22Default);
      setBaseVersion(version);
      acceptedVersion.current = version;
    }
  }, [value, version]);
  function change(next: Stay22Config) {
    dirtyRef.current = true; setDirty(true); setDraft(next); setMessage("");
  }
  async function save() {
    if (!allowed || busy) return;
    if (draft.integration_mode === "script" && draft.enabled && !/^[a-f0-9]{24}$/.test(draft.lma_id ?? "")) {
      setError(t.invalidScript); return;
    }
    if (!/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(draft.aid) || draft.enabled && draft.integration_mode !== "script" && !draft.enabled_providers.length) {
      setError(t.invalid); return;
    }
    setBusy(true); setError(""); setMessage(""); setRefreshFailed(false);
    try {
      const result = await api<{ version: number }>("/admin/hotels/config", { method: "PATCH", body: JSON.stringify({ version: baseVersion, stay22: draft }) });
      dirtyRef.current = false; setDirty(false); setConflict(false); setBaseVersion(result.version);
      acceptedVersion.current = result.version;
      setPersisted(draft);
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
  const modeName = (config: Stay22Config) => !config.enabled ? t.original : config.integration_mode === "script" ? t.script : t.allez;
  return <form aria-label={t.title} onSubmit={(event) => { event.preventDefault(); void save(); }} className="min-w-0 space-y-4 rounded-2xl border border-[var(--line)] bg-[var(--surface-raised)] p-5">
    <div><h3 className="text-lg font-semibold">{t.title}</h3><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t.description}</p></div>
    <p role="note" className="rounded-xl bg-[var(--teal-soft)] p-3 text-sm leading-6">{t.unverified}</p>
    {!allowed && <p role="note" className="text-sm text-[var(--muted)]">{t.permission}</p>}
    <section aria-label={t.module} className="min-w-0 space-y-2 rounded-xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm">
      <dl className="flex flex-wrap items-center gap-x-3 gap-y-2"><dt>{t.savedMode}</dt><dd className="rounded-full bg-[var(--teal-soft)] px-3 py-1 font-semibold">{modeName(persisted)}</dd></dl>
      {dirty && <p>{t.previewMode}：{modeName(draft)}</p>}
      <p className="leading-6 text-[var(--muted)]">{t.off}</p><p className="leading-6 text-[var(--muted)]">{t.on}</p>
    </section>
    <fieldset disabled={!allowed || busy} className="space-y-4">
      <label className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={draft.enabled} onChange={(event) => change({ ...draft, enabled: event.target.checked })} />{t.enabled}</label>
      <label className="grid max-w-lg gap-2 text-sm">{t.integration}<select className={field} value={draft.integration_mode ?? "allez"} onChange={(event) => change({ ...draft, integration_mode: event.target.value as "allez" | "script" })}>
        <option value="allez">{t.allez}</option><option value="script">{t.script}</option>
      </select></label>
      {draft.integration_mode === "script" && <div className="min-w-0 space-y-3 rounded-xl border border-[var(--line)] p-4 text-sm leading-6">
        <p>{t.scope}</p><p className="text-[var(--muted)]">{t.native}</p><p className="text-[var(--muted)]">{t.directPolicy}</p>
        <label className="grid max-w-lg gap-2">LMA Script ID<input className={field} autoComplete="off" value={draft.lma_id ?? ""} maxLength={24} pattern="[a-f0-9]{24}" onChange={(event) => change({ ...draft, lma_id: event.target.value.trim().toLowerCase() || null })} /></label>
        <p className="text-[var(--muted)]">{t.reloadScript}</p>
        <a className="inline-flex min-h-11 items-center underline" href="https://hub.stay22.com/en/lma-script-builder" target="_blank" rel="noopener noreferrer">{t.hub}</a>
      </div>}
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
