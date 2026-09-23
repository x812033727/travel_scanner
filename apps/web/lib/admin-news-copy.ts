const english = {
  nav: "AI News", title: "AI hourly news", description: "Review sources, five-language drafts, evidence, Jev decisions and guarded publication.",
  review: "Review queue", sources: "Sources", settings: "Settings", runs: "Runs", loading: "Loading…",
  empty: "No candidates need attention.", pending: "Pending", failed: "Failed", published: "Published",
  source: "Source", evidence: "Evidence", firstParty: "First party", leadOnly: "Lead only",
  claims: "Claim ledger", checks: "Hard checks", assessments: "Assessments", preview: "Five-language preview", reason: "Required reason",
  retry: "Run again", reject: "Reject", publish: "Publish five locales", verify: "Re-verify", openEditor: "Open guide editor",
  enable: "Enable scanner", shadow: "Shadow", automatic: "Automatic", save: "Save settings",
  addSource: "Add source", sourceName: "Source name", sourceUrl: "HTTPS feed or page URL", format: "Format",
  role: "Role", vertical: "Vertical", interval: "Interval (minutes)", add: "Add", scanNow: "Scan now", validate: "Validate source",
  enabled: "Enabled", disabled: "Disabled", gate: "Activation gate", eligible: "Eligible", notEligible: "Not eligible",
  confidence: "Confidence", status: "Status", error: "Could not complete the request.", saved: "Saved.",
  majorError: "Major factual or licensing error", incident: "Report published major error", noDocument: "No draft exists for this locale.",
};
type Copy = typeof english;
const catalog: Record<string, Copy> = {
  en: english,
  "zh-TW": {
    nav: "AI 自動新聞", title: "AI 每小時自動新聞", description: "管理來源、五語草稿、證據、Jev 判斷與受控發布。",
    review: "人工審查", sources: "來源", settings: "設定", runs: "執行紀錄", loading: "載入中…",
    empty: "目前沒有需要處理的候選。", pending: "待審", failed: "失敗", published: "已發布",
    source: "來源", evidence: "證據", firstParty: "第一方", leadOnly: "僅供發現",
    claims: "Claim ledger", checks: "硬性檢查", assessments: "判斷紀錄", preview: "五語預覽", reason: "必填原因",
    retry: "重新執行", reject: "退件", publish: "五語發布", verify: "重新查核", openEditor: "開啟文章編輯器",
    enable: "啟用掃描", shadow: "影子模式", automatic: "自動模式", save: "儲存設定",
    addSource: "新增來源", sourceName: "來源名稱", sourceUrl: "HTTPS feed 或頁面網址", format: "格式",
    role: "角色", vertical: "分類", interval: "間隔（分鐘）", add: "新增", scanNow: "立即掃描", validate: "驗證來源",
    enabled: "啟用", disabled: "停用", gate: "啟用門檻", eligible: "已達標", notEligible: "未達標",
    confidence: "信心", status: "狀態", error: "操作未完成。", saved: "已儲存。",
    majorError: "重大事實或授權錯誤", incident: "回報發布後重大錯誤", noDocument: "這個語系尚無草稿。",
  },
  "zh-CN": {
    ...english, nav: "AI 自动新闻", title: "AI 每小时自动新闻", description: "管理来源、五语草稿、证据、Jev 判断与受控发布。",
    review: "人工审核", sources: "来源", settings: "设置", runs: "运行记录", loading: "加载中…", empty: "当前没有需要处理的候选。",
    pending: "待审", failed: "失败", published: "已发布", source: "来源", evidence: "证据", firstParty: "第一方", leadOnly: "仅供发现",
    claims: "主张台账", checks: "硬性检查", assessments: "判断记录", preview: "五语预览", reason: "必填原因", retry: "重新运行", reject: "退回", publish: "发布五语版本",
    verify: "重新核查", openEditor: "打开文章编辑器", enable: "启用扫描", shadow: "影子模式", automatic: "自动模式",
    save: "保存设置", addSource: "新增来源", sourceName: "来源名称", sourceUrl: "HTTPS feed 或页面网址", format: "格式",
    role: "角色", vertical: "分类", interval: "间隔（分钟）", add: "新增", scanNow: "立即扫描", validate: "验证来源", enabled: "启用", disabled: "停用",
    gate: "启用门槛", eligible: "已达标", notEligible: "未达标", confidence: "置信度", status: "状态", error: "操作未完成。",
    saved: "已保存。", majorError: "重大事实或授权错误", incident: "报告发布后重大错误", noDocument: "此语言尚无草稿。",
  },
  ja: {
    ...english, nav: "AI 自動ニュース", title: "AI 時間別自動ニュース", description: "情報源、5言語原稿、証拠、Jev判断、安全な公開を管理します。",
    review: "手動レビュー", sources: "情報源", settings: "設定", runs: "実行履歴", loading: "読み込み中…", empty: "確認待ちの候補はありません。",
    pending: "保留", failed: "失敗", published: "公開済み", source: "情報源", evidence: "証拠", firstParty: "一次情報", leadOnly: "発見専用",
    claims: "主張台帳", checks: "必須チェック", assessments: "判定履歴", preview: "5言語プレビュー", reason: "理由（必須）", retry: "再実行", reject: "却下",
    publish: "5言語を公開", verify: "再検証", openEditor: "記事エディターを開く", enable: "スキャナーを有効化", shadow: "シャドーモード",
    automatic: "自動モード", save: "設定を保存", addSource: "情報源を追加", sourceName: "情報源名", sourceUrl: "HTTPS feed またはページURL",
    format: "形式", role: "役割", vertical: "分類", interval: "間隔（分）", add: "追加", scanNow: "今すぐスキャン", validate: "情報源を検証", enabled: "有効", disabled: "無効",
    gate: "有効化ゲート", eligible: "達成", notEligible: "未達", confidence: "信頼度", status: "状態", error: "処理を完了できませんでした。",
    saved: "保存しました。", majorError: "重大な事実・ライセンス誤り", incident: "公開後の重大エラーを報告", noDocument: "この言語の原稿はありません。",
  },
  ko: {
    ...english, nav: "AI 자동 뉴스", title: "AI 시간별 자동 뉴스", description: "소스, 5개 언어 초안, 근거, Jev 판단과 안전한 게시를 관리합니다.",
    review: "수동 검토", sources: "소스", settings: "설정", runs: "실행 기록", loading: "불러오는 중…", empty: "검토할 후보가 없습니다.",
    pending: "대기", failed: "실패", published: "게시됨", source: "소스", evidence: "근거", firstParty: "1차 출처", leadOnly: "발견 전용",
    claims: "주장 원장", checks: "필수 검사", assessments: "판단 기록", preview: "5개 언어 미리보기", reason: "필수 사유", retry: "다시 실행", reject: "거절",
    publish: "5개 언어 게시", verify: "다시 검증", openEditor: "기사 편집기 열기", enable: "스캐너 활성화", shadow: "섀도 모드",
    automatic: "자동 모드", save: "설정 저장", addSource: "소스 추가", sourceName: "소스 이름", sourceUrl: "HTTPS feed 또는 페이지 URL",
    format: "형식", role: "역할", vertical: "분류", interval: "간격(분)", add: "추가", scanNow: "지금 스캔", validate: "소스 검증", enabled: "활성", disabled: "비활성",
    gate: "활성화 기준", eligible: "충족", notEligible: "미충족", confidence: "신뢰도", status: "상태", error: "요청을 완료하지 못했습니다.",
    saved: "저장했습니다.", majorError: "중대한 사실 또는 라이선스 오류", incident: "게시 후 중대 오류 신고", noDocument: "이 언어 초안이 없습니다.",
  },
};

export function adminNewsCopy(locale: string): Copy {
  return catalog[locale] ?? english;
}
