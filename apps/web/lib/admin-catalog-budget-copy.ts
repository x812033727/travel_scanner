type CatalogBudgetCopy = {
  settingLabel: string;
  settingHelp: string;
  invalidLimit: string;
  configure: string;
  defaultLimits: string;
  runLimit: string;
  extend: string;
  confirmTitle: string;
  confirmDescription: string;
  oldLimit: string;
  newLimit: string;
  used: string;
  remaining: string;
  dailyLimit: string;
  preservation: string;
  confirm: string;
  resuming: string;
  limitReached: string;
  limitChanged: string;
};

export const ADMIN_CATALOG_BUDGET_COPY: Record<string, CatalogBudgetCopy> = {
  "zh-TW": {
    settingLabel: "目錄審核每個工作累計呼叫上限",
    settingHelp: "預設 80 次，可設定 1–1000 的整數。這是網站的單一審核工作累計限制，不是 Gemini 專案配額；共用每日額度仍獨立計算。儲存只影響新工作，不會自動續跑或提高既有工作的上限。舊工作須回到審核頁確認採用新上限後續跑。",
    invalidLimit: "每個工作呼叫上限必須是 1–1000 的整數。",
    configure: "設定審核呼叫上限",
    defaultLimits: "新工作呼叫上限 {run} 次；共用每日上限 {daily} 次。",
    runLimit: "此工作原有累計上限 {run} 次；已使用 {used} 次。",
    extend: "提高上限並續跑…",
    confirmTitle: "確認提高此工作的呼叫上限並續跑",
    confirmDescription: "僅將目前選取的工作採用已儲存的新上限。確認後會繼續執行，並可能產生 Gemini API 費用。",
    oldLimit: "原有累計上限",
    newLimit: "新的累計上限",
    used: "已累計呼叫",
    remaining: "本工作剩餘最多呼叫",
    dailyLimit: "共用每日上限",
    preservation: "累計呼叫、已完成評估及套用結果不會歸零。共用每日額度與 Gemini 專案配額仍可能讓工作提前停止；不扣一般會員點數。",
    confirm: "確認提高並續跑",
    resuming: "正在續跑…",
    limitReached: "此工作已達累計呼叫上限。可先在設定提高上限，再回到此工作確認採用新上限並續跑；既有計數與評估不會歸零。",
    limitChanged: "呼叫上限已變更或無法提高，請重新確認最新設定與工作進度後再試。",
  },
  "zh-CN": {
    settingLabel: "目录审核每个工作累计调用上限",
    settingHelp: "默认 80 次，可设置 1–1000 的整数。这是网站的单个审核工作累计限制，不是 Gemini 项目配额；共用每日额度仍独立计算。保存只影响新工作，不会自动继续执行或提高现有工作的上限。旧工作须回到审核页确认采用新上限后继续执行。",
    invalidLimit: "每个工作调用上限必须是 1–1000 的整数。",
    configure: "设置审核调用上限",
    defaultLimits: "新工作调用上限 {run} 次；共用每日上限 {daily} 次。",
    runLimit: "此工作原有累计上限 {run} 次；已使用 {used} 次。",
    extend: "提高上限并继续执行…",
    confirmTitle: "确认提高此工作的调用上限并继续执行",
    confirmDescription: "仅让当前选中的工作采用已保存的新上限。确认后会继续执行，并可能产生 Gemini API 费用。",
    oldLimit: "原有累计上限",
    newLimit: "新的累计上限",
    used: "已累计调用",
    remaining: "本工作剩余最多调用",
    dailyLimit: "共用每日上限",
    preservation: "累计调用、已完成评估及应用结果不会归零。共用每日额度与 Gemini 项目配额仍可能让工作提前停止；不扣普通会员点数。",
    confirm: "确认提高并继续执行",
    resuming: "正在继续执行…",
    limitReached: "此工作已达累计调用上限。可先在设置提高上限，再回到此工作确认采用新上限并继续执行；现有计数与评估不会归零。",
    limitChanged: "调用上限已变更或无法提高，请重新确认最新设置与工作进度后重试。",
  },
  en: {
    settingLabel: "Cumulative call limit per catalog review run",
    settingHelp: "Default: 80 calls. Enter a whole number from 1 to 1000. This is the site's limit for one review run, not the Gemini project quota; the shared daily budget is separate. Saving affects new runs only and never automatically resumes or raises an existing run's limit. Return to the review page to explicitly adopt a higher limit and resume an old run.",
    invalidLimit: "The per-run call limit must be a whole number from 1 to 1000.",
    configure: "Configure review call limit",
    defaultLimits: "New-run limit: {run} calls; shared daily limit: {daily} calls.",
    runLimit: "This run's saved cumulative limit: {run} calls; used: {used} calls.",
    extend: "Raise limit and resume…",
    confirmTitle: "Confirm a higher call limit and resume this run",
    confirmDescription: "Apply the saved higher limit only to the selected run. Confirming continues execution and may incur Gemini API charges.",
    oldLimit: "Previous cumulative limit",
    newLimit: "New cumulative limit",
    used: "Calls already used",
    remaining: "Maximum remaining calls for this run",
    dailyLimit: "Shared daily limit",
    preservation: "Cumulative calls, completed assessments and applied results are not reset. The shared daily budget and Gemini project quota may still stop execution early. No regular member credits are charged.",
    confirm: "Confirm increase and resume",
    resuming: "Resuming…",
    limitReached: "This run reached its cumulative call limit. Raise the setting, then return here to explicitly adopt the higher limit and resume. Existing counts and assessments are not reset.",
    limitChanged: "The call limit changed or cannot be raised. Check the latest settings and run progress before trying again.",
  },
  ja: {
    settingLabel: "目録審査の実行ごとの累計呼び出し上限",
    settingHelp: "初期値は80回。1〜1000の整数を設定できます。これはサイト内の1件の審査実行の累計上限であり、Geminiプロジェクトの割り当てではありません。共有の日次予算は別です。保存は新規実行のみに適用され、既存の実行の再開や上限引き上げは行いません。既存の実行は審査画面で新しい上限を確認してから再開してください。",
    invalidLimit: "実行ごとの呼び出し上限は1〜1000の整数にしてください。",
    configure: "審査の呼び出し上限を設定",
    defaultLimits: "新規実行の上限：{run}回、共有の日次上限：{daily}回。",
    runLimit: "この実行の保存済み累計上限：{run}回、使用済み：{used}回。",
    extend: "上限を引き上げて再開…",
    confirmTitle: "この実行の上限引き上げと再開を確認",
    confirmDescription: "選択中の実行のみに保存済みの新しい上限を適用します。確認すると処理を再開し、Gemini API料金が発生する可能性があります。",
    oldLimit: "これまでの累計上限",
    newLimit: "新しい累計上限",
    used: "使用済み呼び出し回数",
    remaining: "この実行の残り最大呼び出し回数",
    dailyLimit: "共有の日次上限",
    preservation: "累計呼び出し数、完了した評価、適用済みの結果はリセットされません。共有の日次予算やGeminiプロジェクトの割り当てにより、途中で停止する場合があります。一般会員のポイントは消費しません。",
    confirm: "引き上げを確認して再開",
    resuming: "再開中…",
    limitReached: "この実行は累計呼び出し上限に達しました。設定で上限を引き上げ、この画面で新しい上限の適用を確認して再開できます。既存の回数と評価はリセットされません。",
    limitChanged: "呼び出し上限が変更されたか、引き上げられません。最新の設定と進捗を確認してから再試行してください。",
  },
  ko: {
    settingLabel: "목록 검토 작업별 누적 호출 한도",
    settingHelp: "기본값은 80회이며 1~1000 사이의 정수를 설정할 수 있습니다. 사이트의 단일 검토 작업 누적 한도로, Gemini 프로젝트 할당량이 아닙니다. 공유 일일 예산은 별도입니다. 저장은 새 작업에만 적용되며 기존 작업을 자동 재개하거나 한도를 높이지 않습니다. 기존 작업은 검토 페이지에서 새 한도 적용을 확인한 후 재개하세요.",
    invalidLimit: "작업별 호출 한도는 1~1000 사이의 정수여야 합니다.",
    configure: "검토 호출 한도 설정",
    defaultLimits: "새 작업 한도: {run}회 · 공유 일일 한도: {daily}회.",
    runLimit: "이 작업에 저장된 누적 한도: {run}회 · 사용: {used}회.",
    extend: "한도를 높이고 재개…",
    confirmTitle: "이 작업의 호출 한도 상향 및 재개 확인",
    confirmDescription: "선택한 작업에만 저장된 새 한도를 적용합니다. 확인하면 실행을 재개하며 Gemini API 요금이 발생할 수 있습니다.",
    oldLimit: "기존 누적 한도",
    newLimit: "새 누적 한도",
    used: "이미 사용한 호출",
    remaining: "이 작업의 최대 남은 호출",
    dailyLimit: "공유 일일 한도",
    preservation: "누적 호출, 완료된 평가 및 적용된 결과는 초기화되지 않습니다. 공유 일일 예산과 Gemini 프로젝트 할당량에 따라 실행이 일찍 중단될 수 있습니다. 일반 회원 포인트는 차감하지 않습니다.",
    confirm: "상향 확인 후 재개",
    resuming: "재개 중…",
    limitReached: "이 작업이 누적 호출 한도에 도달했습니다. 설정에서 한도를 높인 후 이 작업으로 돌아와 새 한도 적용을 확인하고 재개하세요. 기존 횟수와 평가는 초기화되지 않습니다.",
    limitChanged: "호출 한도가 변경되었거나 높일 수 없습니다. 최신 설정과 작업 진행 상황을 확인한 후 다시 시도하세요.",
  },
};

export function adminCatalogBudgetCopy(locale: string): CatalogBudgetCopy {
  return ADMIN_CATALOG_BUDGET_COPY[locale] ?? ADMIN_CATALOG_BUDGET_COPY.en;
}

export function validCatalogCallLimit(value: unknown): value is number {
  return typeof value === "number" && Number.isInteger(value) && value >= 1 && value <= 1000;
}
