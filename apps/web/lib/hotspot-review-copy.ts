const en = {
  category: "Attraction category",
  qid: "Wikidata ID",
  qidHint: "Fill a missing ID only after checking the exact entity. Existing IDs are protected; saving does not approve an attraction.",
  reason: "Review rationale and sources",
  batchReason: "Rationale and sources for this selection",
  reasonHint: "Record the evidence and source URLs supporting your decision (up to 500 characters).",
  discard: "Discard the unsaved changes to this attraction?",
  conflict: "This attraction has changed. Your draft is kept. Reload the latest record and compare before saving again.",
  refresh: "Reload latest record",
  required: "Enter a review rationale and source before changing the category or Wikidata ID.",
};
type Copy = typeof en;
const copies: Record<string, Copy> = {
  en,
  "zh-TW": {
    category: "景點分類", qid: "Wikidata ID",
    qidHint: "核對同一景點後才能補上缺少的 ID。既有 ID 受保護；儲存資料不會自動核准景點。",
    reason: "審核理由與來源", batchReason: "本次審核理由與來源",
    reasonHint: "記錄判斷依據與來源網址，最多 500 字。",
    discard: "要放棄這筆景點尚未儲存的修改嗎？",
    conflict: "這筆景點已被更新。草稿已保留，請重新載入最新資料並比對後再儲存。",
    refresh: "重新載入最新資料", required: "修改分類或 Wikidata ID 前，請填寫審核理由與來源。",
  },
  "zh-CN": {
    category: "景点分类", qid: "Wikidata ID",
    qidHint: "核对同一景点后才能补上缺少的 ID。现有 ID 受保护；保存资料不会自动批准景点。",
    reason: "审核理由与来源", batchReason: "本次审核理由与来源",
    reasonHint: "记录判断依据与来源网址，最多 500 字。",
    discard: "要放弃此景点尚未保存的修改吗？",
    conflict: "此景点已被更新。草稿已保留，请重新加载最新资料并比较后再保存。",
    refresh: "重新加载最新资料", required: "修改分类或 Wikidata ID 前，请填写审核理由与来源。",
  },
  ja: {
    category: "観光スポットの分類", qid: "Wikidata ID",
    qidHint: "同一の場所を確認してから未設定の ID を入力してください。既存 ID は保護され、保存だけでは承認されません。",
    reason: "審査理由と出典", batchReason: "選択した項目の審査理由と出典",
    reasonHint: "判断の根拠と出典 URL を記録してください（500 文字以内）。",
    discard: "この場所の未保存の変更を破棄しますか？",
    conflict: "この場所は更新されています。下書きは保持されています。最新情報を読み込み、比較してから保存してください。",
    refresh: "最新情報を再読み込み", required: "分類または Wikidata ID を変更する前に、審査理由と出典を入力してください。",
  },
  ko: {
    category: "관광지 분류", qid: "Wikidata ID",
    qidHint: "동일한 장소를 확인한 후 누락된 ID를 입력하세요. 기존 ID는 보호되며 저장만으로 관광지가 승인되지 않습니다.",
    reason: "검토 사유 및 출처", batchReason: "선택한 항목의 검토 사유 및 출처",
    reasonHint: "판단 근거와 출처 URL을 기록하세요(최대 500자).",
    discard: "이 관광지의 저장하지 않은 변경 사항을 버릴까요?",
    conflict: "이 관광지가 변경되었습니다. 초안은 유지됩니다. 최신 정보를 불러와 비교한 후 다시 저장하세요.",
    refresh: "최신 정보 다시 불러오기", required: "분류 또는 Wikidata ID를 변경하기 전에 검토 사유와 출처를 입력하세요.",
  },
};
export function hotspotReviewCopy(locale: string): Copy { return copies[locale] ?? en; }
