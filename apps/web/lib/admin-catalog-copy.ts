const en = {
  identityEditor: "Manage exact location",
  identityHint: "Place identity and permanent coordinates are managed together in the location editor.",
  automationEnabled: "Automatic restaurant scans are enabled",
  automationDisabled: "Automatic restaurant scans are paused",
  automationUnknown: "Loading automatic scan status",
  automationSettings: "Manage automatic scans in food settings",
  filteredLocation: "Showing the selected location",
  missingLocation: "Showing locations with missing coordinates",
  showAllLocations: "Show all locations",
};
type Copy = typeof en;
const copies: Record<string, Copy> = {
  en,
  "zh-TW": {
    identityEditor: "管理精準地點",
    identityHint: "地點識別與永久座標統一在地點編輯器管理。",
    automationEnabled: "餐廳自動掃描已啟用",
    automationDisabled: "餐廳自動掃描已暫停",
    automationUnknown: "正在載入自動掃描狀態",
    automationSettings: "前往美食設定管理自動掃描",
    filteredLocation: "目前顯示指定地點",
    missingLocation: "目前顯示缺少座標的地點",
    showAllLocations: "顯示全部地點",
  },
  "zh-CN": {
    identityEditor: "管理精准地点",
    identityHint: "地点标识与永久坐标统一在地点编辑器管理。",
    automationEnabled: "餐厅自动扫描已启用",
    automationDisabled: "餐厅自动扫描已暂停",
    automationUnknown: "正在加载自动扫描状态",
    automationSettings: "前往美食设置管理自动扫描",
    filteredLocation: "当前显示指定地点",
    missingLocation: "当前显示缺少坐标的地点",
    showAllLocations: "显示全部地点",
  },
  ja: {
    identityEditor: "正確な場所を管理",
    identityHint: "場所の識別情報と永続的な座標は、場所編集画面で一元管理します。",
    automationEnabled: "レストランの自動スキャンは有効です",
    automationDisabled: "レストランの自動スキャンは停止中です",
    automationUnknown: "自動スキャンの状態を読み込み中",
    automationSettings: "グルメ設定で自動スキャンを管理",
    filteredLocation: "選択した場所を表示しています",
    missingLocation: "座標が未設定の場所を表示しています",
    showAllLocations: "すべての場所を表示",
  },
  ko: {
    identityEditor: "정확한 장소 관리",
    identityHint: "장소 식별 정보와 영구 좌표는 장소 편집기에서 함께 관리합니다.",
    automationEnabled: "음식점 자동 스캔이 활성화되었습니다",
    automationDisabled: "음식점 자동 스캔이 일시 중지되었습니다",
    automationUnknown: "자동 스캔 상태를 불러오는 중",
    automationSettings: "음식 설정에서 자동 스캔 관리",
    filteredLocation: "선택한 장소를 표시합니다",
    missingLocation: "좌표가 없는 장소를 표시합니다",
    showAllLocations: "모든 장소 보기",
  },
};
export function adminCatalogCopy(locale: string): Copy { return copies[locale] ?? en; }

export function hotspotIdentityHref(hotspotId: string): string {
  return `/admin/hotspots?${new URLSearchParams({ tab: "places", section: "identity", hotspot_id: hotspotId })}`;
}

export function hotspotIdentityListHref(search: { toString(): string } | null): string {
  const params = new URLSearchParams(search?.toString());
  params.set("tab", "places");
  params.set("section", "identity");
  params.delete("hotspot_id");
  params.delete("missing_location");
  return `/admin/hotspots?${params}`;
}
