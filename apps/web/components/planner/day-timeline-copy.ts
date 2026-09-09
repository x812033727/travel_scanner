import { normalizeLocale, type Locale } from "@/i18n/routing";

type TimelineCopy = { pending: string; estimated: string; stale: string; details: string; query: string; requery: string; queryHint: string; outdated: string };
const copies: Record<Locale, TimelineCopy> = {
  "zh-TW": { pending: "交通待確認", estimated: "約 {minutes} 分", stale: "路線待更新", details: "查看交通", query: "查詢交通方案", requery: "重新查詢", queryHint: "選好交通方式與緩衝後再查詢；切換選項不會自動查詢。", outdated: "設定已變更，請重新查詢後再套用。" },
  "zh-CN": { pending: "交通待确认", estimated: "约 {minutes} 分", stale: "路线待更新", details: "查看交通", query: "查询交通方案", requery: "重新查询", queryHint: "选好交通方式与缓冲后再查询；切换选项不会自动查询。", outdated: "设置已变更，请重新查询后再应用。" },
  en: { pending: "Travel time pending", estimated: "About {minutes} min", stale: "Route needs updating", details: "View transport", query: "Find transport options", requery: "Search again", queryHint: "Choose a mode and buffer, then search. Changing options does not run a search.", outdated: "Settings changed. Search again before applying." },
  ja: { pending: "移動時間は未確認", estimated: "約{minutes}分", stale: "経路の更新が必要", details: "交通手段を表示", query: "交通手段を検索", requery: "再検索", queryHint: "交通手段と余裕時間を選んでから検索してください。選択変更では自動検索しません。", outdated: "設定が変更されました。適用前に再検索してください。" },
  ko: { pending: "이동 시간 확인 필요", estimated: "약 {minutes}분", stale: "경로 업데이트 필요", details: "교통 보기", query: "교통편 검색", requery: "다시 검색", queryHint: "교통수단과 여유 시간을 선택한 뒤 검색하세요. 옵션 변경 시 자동 검색하지 않습니다.", outdated: "설정이 변경되었습니다. 적용 전에 다시 검색하세요." },
};
export function dayTimelineCopy(locale: string): TimelineCopy { return copies[normalizeLocale(locale)]; }
