import type { AdminSettingsScope } from "./admin-settings-ownership";

type SettingsCopy = {
  scopes: Record<AdminSettingsScope, string>;
  managedIn: string;
  shared: string;
  configured: string;
  missing: string;
  unsaved: string;
  leave: string;
  conflict: string;
  reload: string;
  discard: string;
};

const copy: Record<string, SettingsCopy> = {
  "zh-TW": {
    scopes: { providers: "共用供應商設定", system: "系統設定", layout: "版面設定", hotspots: "景點設定", foods: "美食設定", hotels: "飯店設定" },
    managedIn: "此設定統一管理於", shared: "共用服務與憑證（唯讀）", configured: "已設定", missing: "未設定",
    unsaved: "有未儲存的變更；每張卡片分別儲存，其他草稿會保留。", leave: "仍有未儲存的設定。離開此頁並放棄變更？",
    conflict: "這項設定已被其他管理員更新。你的草稿仍保留；請重新載入這張卡片，再套用變更。", reload: "重新載入這張卡片", discard: "重新載入會放棄這張卡片的未儲存變更，其他草稿會保留。繼續？",
  },
  "zh-CN": {
    scopes: { providers: "共享服务商设置", system: "系统设置", layout: "布局设置", hotspots: "景点设置", foods: "美食设置", hotels: "酒店设置" },
    managedIn: "此设置统一管理于", shared: "共享服务与凭证（只读）", configured: "已设置", missing: "未设置",
    unsaved: "有未保存的更改；每张卡片单独保存，其他草稿会保留。", leave: "仍有未保存的设置。离开此页并放弃更改？",
    conflict: "此设置已被其他管理员更新。草稿仍保留；请重新加载此卡片后再应用更改。", reload: "重新加载此卡片", discard: "重新加载会放弃此卡片的未保存更改，其他草稿会保留。继续？",
  },
  en: {
    scopes: { providers: "Shared providers", system: "System settings", layout: "Layout settings", hotspots: "Hotspot settings", foods: "Food settings", hotels: "Hotel settings" },
    managedIn: "Managed in", shared: "Shared services and credentials (read only)", configured: "Configured", missing: "Not configured",
    unsaved: "You have unsaved changes. Save each card separately; other drafts are retained.", leave: "You have unsaved settings. Leave this page and discard your changes?",
    conflict: "Another administrator updated these settings. Your draft is retained. Reload this card before applying your changes.", reload: "Reload this card", discard: "Reloading discards unsaved changes on this card only. Other drafts are retained. Continue?",
  },
  ja: {
    scopes: { providers: "共通プロバイダー設定", system: "システム設定", layout: "レイアウト設定", hotspots: "観光スポット設定", foods: "グルメ設定", hotels: "ホテル設定" },
    managedIn: "管理先", shared: "共通サービスと認証情報（読み取り専用）", configured: "設定済み", missing: "未設定",
    unsaved: "未保存の変更があります。カードごとに保存してください。他の下書きは保持されます。", leave: "未保存の設定があります。変更を破棄してこのページを離れますか？",
    conflict: "別の管理者が設定を更新しました。下書きは保持されています。このカードを再読み込みしてから変更してください。", reload: "このカードを再読み込み", discard: "このカードの未保存の変更のみ破棄されます。他の下書きは保持されます。続行しますか？",
  },
  ko: {
    scopes: { providers: "공유 공급자 설정", system: "시스템 설정", layout: "레이아웃 설정", hotspots: "명소 설정", foods: "맛집 설정", hotels: "호텔 설정" },
    managedIn: "설정 관리 위치", shared: "공유 서비스 및 인증 정보 (읽기 전용)", configured: "설정됨", missing: "미설정",
    unsaved: "저장하지 않은 변경 사항이 있습니다. 각 카드를 따로 저장하며 다른 초안은 유지됩니다.", leave: "저장하지 않은 설정이 있습니다. 변경 사항을 버리고 페이지를 나갈까요?",
    conflict: "다른 관리자가 설정을 업데이트했습니다. 초안은 유지됩니다. 이 카드를 새로 불러온 후 변경 사항을 적용하세요.", reload: "이 카드 새로 불러오기", discard: "이 카드의 저장하지 않은 변경 사항만 삭제됩니다. 다른 초안은 유지됩니다. 계속할까요?",
  },
};

export function adminSettingsCopy(locale: string): SettingsCopy {
  return copy[locale] || copy.en;
}
