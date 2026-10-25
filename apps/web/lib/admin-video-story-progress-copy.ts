type ProgressCopy = {
  title: string;
  loading: string;
  unavailable: string;
  explanation: string;
  plans: string;
  approved: string;
  pending: string;
  markdown: string;
  finished: string;
  rowPlan: string;
  rowPlanMissing: string;
  rowApproved: string;
  rowPending: string;
  rowScriptMissing: string;
  rowMarkdown: string;
  rowMarkdownMissing: string;
  rowUnavailable: string;
};

const zhTW: ProgressCopy = {
  title: "前期製作進度",
  loading: "正在讀取前期進度…",
  unavailable: "前期進度目前無法取得，不能將未取得的數字當作 0。",
  explanation: "企劃、劇本與原稿分開計數；原稿可核對不代表已有成片或已上架。",
  plans: "完整企劃",
  approved: "劇本已核准",
  pending: "劇本待審",
  markdown: "Markdown 原稿可核對",
  finished: "成片完成",
  rowPlan: "企劃完整",
  rowPlanMissing: "企劃待補",
  rowApproved: "劇本已核准",
  rowPending: "劇本待審",
  rowScriptMissing: "劇本未匯入",
  rowMarkdown: "原稿可核對",
  rowMarkdownMissing: "原稿未核對",
  rowUnavailable: "這集的前期資料無法對應",
};

const en: ProgressCopy = {
  title: "Preproduction progress",
  loading: "Loading preproduction progress…",
  unavailable: "Preproduction progress is unavailable. Missing data is not zero progress.",
  explanation: "Plans, scripts and source files are counted separately. A verifiable source file does not mean the film is finished or published.",
  plans: "Complete plans",
  approved: "Approved scripts",
  pending: "Scripts awaiting review",
  markdown: "Verifiable Markdown sources",
  finished: "Finished films",
  rowPlan: "Plan complete",
  rowPlanMissing: "Plan incomplete",
  rowApproved: "Script approved",
  rowPending: "Script awaiting review",
  rowScriptMissing: "Script not imported",
  rowMarkdown: "Source verifiable",
  rowMarkdownMissing: "Source not verified",
  rowUnavailable: "Preproduction data cannot be matched to this episode",
};

const zhCN: ProgressCopy = {
  title: "前期制作进度",
  loading: "正在读取前期进度…",
  unavailable: "前期进度目前无法获取，不能将缺失的数据当作 0。",
  explanation: "企划、剧本和原稿分别计数；原稿可核对不代表已有成片或已发布。",
  plans: "完整企划",
  approved: "剧本已核准",
  pending: "剧本待审",
  markdown: "Markdown 原稿可核对",
  finished: "成片完成",
  rowPlan: "企划完整",
  rowPlanMissing: "企划待补",
  rowApproved: "剧本已核准",
  rowPending: "剧本待审",
  rowScriptMissing: "剧本未导入",
  rowMarkdown: "原稿可核对",
  rowMarkdownMissing: "原稿未核对",
  rowUnavailable: "这集的前期数据无法对应",
};

const ja: ProgressCopy = {
  title: "制作前の進捗",
  loading: "制作前の進捗を読み込み中…",
  unavailable: "制作前の進捗を取得できません。未取得のデータを 0 として扱いません。",
  explanation: "企画、台本、原稿を別々に集計します。原稿を照合できても、映像の完成や公開を意味しません。",
  plans: "完成した企画",
  approved: "承認済み台本",
  pending: "審査待ち台本",
  markdown: "照合可能な Markdown 原稿",
  finished: "完成した映像",
  rowPlan: "企画完成",
  rowPlanMissing: "企画未完成",
  rowApproved: "台本承認済み",
  rowPending: "台本審査待ち",
  rowScriptMissing: "台本未登録",
  rowMarkdown: "原稿照合可能",
  rowMarkdownMissing: "原稿未照合",
  rowUnavailable: "このエピソードの制作前データを照合できません",
};

const ko: ProgressCopy = {
  title: "사전 제작 진행 상황",
  loading: "사전 제작 진행 상황을 불러오는 중…",
  unavailable: "사전 제작 진행 상황을 가져올 수 없습니다. 누락된 데이터를 0으로 표시하지 않습니다.",
  explanation: "기획, 대본, 원고를 별도로 집계합니다. 원고를 확인할 수 있어도 영상 완성이나 게시를 뜻하지 않습니다.",
  plans: "완성된 기획",
  approved: "승인된 대본",
  pending: "검토 대기 대본",
  markdown: "확인 가능한 Markdown 원고",
  finished: "완성된 영상",
  rowPlan: "기획 완료",
  rowPlanMissing: "기획 미완료",
  rowApproved: "대본 승인됨",
  rowPending: "대본 검토 대기",
  rowScriptMissing: "대본 미등록",
  rowMarkdown: "원고 확인 가능",
  rowMarkdownMissing: "원고 미확인",
  rowUnavailable: "이 에피소드의 사전 제작 데이터를 연결할 수 없습니다",
};

const copies: Record<string, ProgressCopy> = { "zh-TW": zhTW, "zh-CN": zhCN, en, ja, ko };

export function adminVideoStoryProgressCopy(locale: string): ProgressCopy {
  return copies[locale] ?? en;
}
