import { normalizeLocale, type Locale } from "@/i18n/routing";

type OverlayCopy = {
  close: string; back: string; expand: string; collapse: string;
  advanced: string; advancedHint: string; routeDetails: string; routeDetailsHint: string; closeManual: string;
};

const copy: Record<Locale, OverlayCopy> = {
  "zh-TW": {
    close: "關閉", back: "返回上一層", expand: "展開面板", collapse: "縮小面板",
    advanced: "進階路線設定", advancedHint: "調整轉乘緩衝或自行設定交通時間",
    routeDetails: "路線與站點明細", routeDetailsHint: "展開查看步行、轉乘與月台資訊", closeManual: "取消自訂時間",
  },
  "zh-CN": {
    close: "关闭", back: "返回上一层", expand: "展开面板", collapse: "缩小面板",
    advanced: "进阶路线设置", advancedHint: "调整换乘缓冲或自行设置交通时间",
    routeDetails: "路线与站点明细", routeDetailsHint: "展开查看步行、换乘与站台信息", closeManual: "取消自定义时间",
  },
  en: {
    close: "Close", back: "Go back", expand: "Expand panel", collapse: "Collapse panel",
    advanced: "Advanced route settings", advancedHint: "Adjust transfer buffer or enter your own travel time",
    routeDetails: "Route and stop details", routeDetailsHint: "Expand for walking, transfers and platforms", closeManual: "Cancel custom time",
  },
  ja: {
    close: "閉じる", back: "前に戻る", expand: "パネルを広げる", collapse: "パネルを縮める",
    advanced: "経路の詳細設定", advancedHint: "乗り換えの余裕時間や移動時間を設定",
    routeDetails: "経路と停車駅の詳細", routeDetailsHint: "徒歩・乗り換え・ホーム情報を表示", closeManual: "手動の時間設定をキャンセル",
  },
  ko: {
    close: "닫기", back: "이전으로", expand: "패널 펼치기", collapse: "패널 축소",
    advanced: "경로 상세 설정", advancedHint: "환승 여유 시간을 조정하거나 이동 시간을 직접 입력하세요",
    routeDetails: "경로 및 정류장 상세", routeDetailsHint: "도보, 환승 및 승강장 정보를 펼쳐 보기", closeManual: "직접 입력 취소",
  },
};

export function plannerOverlayCopy(locale: string): OverlayCopy {
  return copy[normalizeLocale(locale)];
}
