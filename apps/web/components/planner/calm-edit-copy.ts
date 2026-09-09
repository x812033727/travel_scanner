const copies = {
  "zh-TW": {
    choose: "選擇", chosen: "已選擇「{title}」，確認加入後才會更新行程。", mapSearch: "搜尋地圖",
    searchLabel: "搜尋地點", catalogHint: "搜尋站內已收錄的地點；切換來源會保留關鍵字。", mapHint: "搜尋 Google Maps／NAVER，選擇地點後仍可修改。",
    cancel: "取消", save: "儲存", saving: "儲存中…", unsaved: "尚未儲存", saved: "已儲存", saveFailed: "儲存失敗，內容已保留，請重試。",
    departureTime: "出發時間", departureLabel: "每天從飯店出發的時間", departureApplies: "儲存後套用到每一天",
  },
  "zh-CN": {
    choose: "选择", chosen: "已选择“{title}”，确认添加后才会更新行程。", mapSearch: "搜索地图",
    searchLabel: "搜索地点", catalogHint: "搜索站内已收录的地点；切换来源会保留关键词。", mapHint: "搜索 Google Maps／NAVER，选择地点后仍可修改。",
    cancel: "取消", save: "保存", saving: "保存中…", unsaved: "尚未保存", saved: "已保存", saveFailed: "保存失败，内容已保留，请重试。",
    departureTime: "出发时间", departureLabel: "每天从酒店出发的时间", departureApplies: "保存后应用到每一天",
  },
  en: {
    choose: "Choose", chosen: '“{title}” selected. Confirm Add to update your itinerary.', mapSearch: "Search maps",
    searchLabel: "Search places", catalogHint: "Search our place catalog. Your keywords stay when you switch sources.", mapHint: "Search Google Maps / NAVER. You can still edit your selection before adding it.",
    cancel: "Cancel", save: "Save", saving: "Saving…", unsaved: "Unsaved changes", saved: "Saved", saveFailed: "Could not save. Your text is still here; please try again.",
    departureTime: "Departure time", departureLabel: "Daily departure time from your hotel", departureApplies: "Applies to every day when saved",
  },
  ja: {
    choose: "選択", chosen: "「{title}」を選択しました。追加を確定すると旅程に反映されます。", mapSearch: "地図を検索",
    searchLabel: "場所を検索", catalogHint: "登録済みの場所を検索します。検索先を切り替えてもキーワードは残ります。", mapHint: "Google Maps／NAVER を検索します。選択後も追加前に編集できます。",
    cancel: "キャンセル", save: "保存", saving: "保存中…", unsaved: "未保存の変更", saved: "保存しました", saveFailed: "保存できませんでした。入力内容は保持されています。もう一度お試しください。",
    departureTime: "出発時刻", departureLabel: "毎日のホテル出発時刻", departureApplies: "保存すると全日程に適用されます",
  },
  ko: {
    choose: "선택", chosen: "‘{title}’을 선택했습니다. 추가를 확정하면 일정에 반영됩니다.", mapSearch: "지도 검색",
    searchLabel: "장소 검색", catalogHint: "등록된 장소를 검색합니다. 검색 출처를 바꿔도 검색어는 유지됩니다.", mapHint: "Google Maps / NAVER를 검색합니다. 선택한 후에도 추가 전에 수정할 수 있습니다.",
    cancel: "취소", save: "저장", saving: "저장 중…", unsaved: "저장하지 않은 변경 사항", saved: "저장됨", saveFailed: "저장하지 못했습니다. 입력 내용은 유지됩니다. 다시 시도해 주세요.",
    departureTime: "출발 시간", departureLabel: "매일 호텔에서 출발하는 시간", departureApplies: "저장하면 모든 날짜에 적용됩니다",
  },
};

export function calmEditCopy(locale: string) {
  return copies[locale as keyof typeof copies] ?? copies["zh-TW"];
}
