export type CatalogReviewScope = "all" | "hotspots" | "foods";
type ReviewCopy = {
  scopes: Record<CatalogReviewScope, string>;
  historyOnly: string;
  sharedQuota: string;
  activeElsewhere: string;
  openHistory: string;
  discovery: string;
  startDiscovery: string;
  hotspotCounts: string;
  foodCounts: string;
};

export const ADMIN_REVIEW_COPY: Record<string, ReviewCopy> = {
  "zh-TW": {
    scopes: { all: "跨領域（舊版混合）", hotspots: "景點", foods: "美食與店家" },
    historyOnly: "此處保留所有範圍的工作歷史，可續跑或套用既有結果。新審核請從景點或美食工作區開始。",
    sharedQuota: "所有領域共用 Gemini 預算，且同時僅執行一個審核工作。",
    activeElsewhere: "{scope}工作正在執行；目前領域須等候完成，不會另啟重複工作。",
    openHistory: "查看執行中工作",
    discovery: "尋找 {count} 筆新候選", startDiscovery: "開始尋找 {count} 筆候選",
    hotspotCounts: "僅景點 40 筆；不包含料理或店家。",
    foodCounts: "料理 20 筆 · 店家 40 筆；不包含景點。",
  },
  "zh-CN": {
    scopes: { all: "跨领域（旧版混合）", hotspots: "景点", foods: "美食与店家" },
    historyOnly: "此处保留所有范围的工作历史，可继续执行或应用现有结果。新审核请从景点或美食工作区开始。",
    sharedQuota: "所有领域共用 Gemini 预算，且同时仅执行一个审核工作。",
    activeElsewhere: "{scope}工作正在执行；当前领域须等待完成，不会另启重复工作。",
    openHistory: "查看执行中的工作",
    discovery: "寻找 {count} 个新候选", startDiscovery: "开始寻找 {count} 个候选",
    hotspotCounts: "仅景点 40 个；不包含料理或店家。",
    foodCounts: "料理 20 个 · 店家 40 个；不包含景点。",
  },
  en: {
    scopes: { all: "Mixed domains (legacy)", hotspots: "Attractions", foods: "Food and merchants" },
    historyOnly: "History includes all scopes. Resume or apply existing results here; start new reviews in the Attractions or Food workspace.",
    sharedQuota: "All domains share the Gemini budget. Only one review runs at a time.",
    activeElsewhere: "A {scope} review is running. This domain must wait; no duplicate job will start.",
    openHistory: "View the running review",
    discovery: "Discover {count} new candidates", startDiscovery: "Find {count} candidates",
    hotspotCounts: "40 attractions only; no dishes or merchants.",
    foodCounts: "20 dishes and 40 merchants; no attractions.",
  },
  ja: {
    scopes: { all: "複数分野（旧形式）", hotspots: "観光スポット", foods: "料理・店舗" },
    historyOnly: "全分野の実行履歴です。既存の処理の再開や結果の適用ができます。新規審査は観光スポットまたはグルメの管理画面から開始してください。",
    sharedQuota: "全分野で Gemini の予算を共有し、同時に実行できる審査は1件です。",
    activeElsewhere: "{scope}の審査が実行中です。完了までこの分野の新規処理は待機し、重複して開始しません。",
    openHistory: "実行中の審査を確認",
    discovery: "新規候補を{count}件探す", startDiscovery: "候補{count}件の検索を開始",
    hotspotCounts: "観光スポット40件のみ。料理・店舗は対象外です。",
    foodCounts: "料理20件・店舗40件。観光スポットは対象外です。",
  },
  ko: {
    scopes: { all: "여러 분야 (이전 형식)", hotspots: "명소", foods: "음식 및 매장" },
    historyOnly: "모든 범위의 작업 기록입니다. 기존 작업을 재개하거나 결과를 적용할 수 있습니다. 새 검토는 명소 또는 음식 작업 공간에서 시작하세요.",
    sharedQuota: "모든 분야가 Gemini 예산을 공유하며 검토는 한 번에 하나만 실행됩니다.",
    activeElsewhere: "{scope} 검토가 실행 중입니다. 완료될 때까지 기다리며 중복 작업을 시작하지 않습니다.",
    openHistory: "실행 중인 검토 보기",
    discovery: "새 후보 {count}개 찾기", startDiscovery: "후보 {count}개 검색 시작",
    hotspotCounts: "명소 40개만 검토합니다. 음식 및 매장은 제외됩니다.",
    foodCounts: "음식 20개 및 매장 40개입니다. 명소는 제외됩니다.",
  },
};

export function adminReviewCopy(locale: string): ReviewCopy {
  return ADMIN_REVIEW_COPY[locale] ?? ADMIN_REVIEW_COPY.en;
}
