const en = {
  restoreMeal: "Restore meal", skipMeal: "Skip meal",
  extras: "Optional arrangements", extrasHint: "Add flights, stays or meals when you are ready. Empty slots do not affect your route.",
  save: "Save changes", saving: "Saving…", cancel: "Cancel", discard: "Discard changes", keep: "Keep editing",
  dirtyTitle: "Keep your changes?", dirtyHint: "Your draft has not been applied. Discard it or continue editing.",
  draftHint: "Draft · your itinerary changes only when you save", conflict: "This trip changed while you were editing. Your draft is kept. Review the latest itinerary before saving again.",
  details: "Place details", pendingTime: "Time pending", review: "Review this day", query: "Check routes", preferencesHint: "Changes take effect when you save. Route searches run only when you request them.",
  continueAdding: "Save and add another", previewFirst: "Preview · no charge", routeOnly: "Reorder existing places", preflight: "Planning checks",
};
type Copy = typeof en;
const copies: Record<string, Copy> = {
  en,
  "zh-TW": {
    restoreMeal: "恢復用餐", skipMeal: "略過用餐",
    extras: "補充安排", extrasHint: "需要時再加入航班、住宿或用餐。空白項目不影響動線。",
    save: "儲存修改", saving: "儲存中…", cancel: "取消", discard: "捨棄修改", keep: "繼續編輯",
    dirtyTitle: "保留這次修改嗎？", dirtyHint: "草稿尚未套用。你可以繼續編輯，或捨棄這次修改。",
    draftHint: "編輯草稿・儲存後才會修改行程", conflict: "編輯期間旅程已有更新。草稿已保留，請先查看最新行程後再儲存。",
    details: "地點詳情", pendingTime: "時間待確認", review: "檢查這一天", query: "查詢路線", preferencesHint: "儲存後才套用設定；需要時再主動查詢路線。",
    continueAdding: "儲存並繼續新增", previewFirst: "預覽・不扣次", routeOnly: "只順路排序", preflight: "規劃前檢查",
  },
  "zh-CN": {
    restoreMeal: "恢复用餐", skipMeal: "跳过用餐",
    extras: "补充安排", extrasHint: "需要时再加入航班、住宿或用餐。空白项目不影响路线。",
    save: "保存修改", saving: "保存中…", cancel: "取消", discard: "放弃修改", keep: "继续编辑",
    dirtyTitle: "保留这次修改吗？", dirtyHint: "草稿尚未应用。你可以继续编辑，或放弃这次修改。",
    draftHint: "编辑草稿・保存后才会修改行程", conflict: "编辑期间行程已有更新。草稿已保留，请先查看最新行程后再保存。",
    details: "地点详情", pendingTime: "时间待确认", review: "检查这一天", query: "查询路线", preferencesHint: "保存后才应用设置；需要时再主动查询路线。",
    continueAdding: "保存并继续新增", previewFirst: "预览・不扣次数", routeOnly: "只优化顺序", preflight: "规划前检查",
  },
  ja: {
    restoreMeal: "食事を復元", skipMeal: "食事をスキップ",
    extras: "追加の予定", extrasHint: "航空便・宿泊・食事は後から追加できます。未設定の枠は移動に影響しません。",
    save: "変更を保存", saving: "保存中…", cancel: "キャンセル", discard: "変更を破棄", keep: "編集を続ける",
    dirtyTitle: "変更を残しますか？", dirtyHint: "下書きは未適用です。編集を続けるか、変更を破棄できます。",
    draftHint: "編集中・保存するまで旅程は変わりません", conflict: "編集中に旅程が更新されました。下書きは保持しています。最新の旅程を確認してください。",
    details: "場所の詳細", pendingTime: "時刻は未確定", review: "この日を確認", query: "経路を検索", preferencesHint: "保存後に設定を適用します。経路検索は明示的に実行した時だけ行います。",
    continueAdding: "保存して次を追加", previewFirst: "プレビュー・利用回数なし", routeOnly: "現在の場所を並べ替え", preflight: "計画前の確認",
  },
  ko: {
    restoreMeal: "식사 복원", skipMeal: "식사 건너뛰기",
    extras: "추가 일정", extrasHint: "항공편, 숙소, 식사는 나중에 추가하세요. 빈 항목은 동선에 영향을 주지 않습니다.",
    save: "변경 저장", saving: "저장 중…", cancel: "취소", discard: "변경 버리기", keep: "계속 편집",
    dirtyTitle: "변경 내용을 유지할까요?", dirtyHint: "초안은 아직 적용되지 않았습니다. 계속 편집하거나 변경을 버릴 수 있습니다.",
    draftHint: "초안 편집 중 · 저장해야 일정이 변경됩니다", conflict: "편집 중 일정이 변경되었습니다. 초안은 유지됩니다. 최신 일정을 먼저 확인하세요.",
    details: "장소 상세", pendingTime: "시간 미확정", review: "이 날 확인", query: "경로 검색", preferencesHint: "저장해야 설정이 적용됩니다. 경로 검색은 직접 요청할 때만 실행됩니다.",
    continueAdding: "저장하고 계속 추가", previewFirst: "미리보기 · 차감 없음", routeOnly: "기존 장소 순서만 조정", preflight: "계획 전 확인",
  },
};
export function calmCopy(locale: string): Copy { return copies[locale] || en; }
