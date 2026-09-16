import type { Locale } from "@/i18n/routing";

const rows = {
  "zh-TW": ["Codex 學習中心", "從第一個任務到進階整合，依程度、平台與需求找教學。", "搜尋教學或指令", "程度", "平台", "需求", "全部", "零基礎", "日常使用", "進階整合", "桌面版", "手機", "CLI", "IDE", "雲端", "安裝", "MD 設定", "指令", "除錯", "Git", "自動化", "規劃中", "尚未發布", "暫時無法確認發布狀態", "沒有符合條件的教學", "返回 Codex 教學總目錄", "上一篇", "下一篇", "相關教學", "指令索引", "複製", "已複製", "請選取程式碼手動複製", "分鐘", "更新", "清除篩選", "已更新篩選結果"],
  "zh-CN": ["Codex 学习中心", "从第一个任务到进阶集成，按程度、平台和需求查找教程。", "搜索教程或命令", "程度", "平台", "需求", "全部", "零基础", "日常使用", "进阶集成", "桌面版", "手机", "CLI", "IDE", "云端", "安装", "MD 设置", "命令", "调试", "Git", "自动化", "规划中", "尚未发布", "暂时无法确认发布状态", "没有符合条件的教程", "返回 Codex 教程总目录", "上一篇", "下一篇", "相关教程", "命令索引", "复制", "已复制", "请选择代码手动复制", "分钟", "更新", "清除筛选", "已更新筛选结果"],
  en: ["Codex learning hub", "Find your next tutorial by experience, platform, or goal, from your first task to advanced integrations.", "Search tutorials or commands", "Experience", "Platform", "Goal", "All", "Beginner", "Everyday work", "Advanced", "Desktop", "Mobile", "CLI", "IDE", "Cloud", "Setup", "MD configuration", "Commands", "Debugging", "Git", "Automation", "Planned", "Not published", "Publication status temporarily unavailable", "No matching tutorials", "Back to the Codex learning hub", "Previous", "Next", "Related tutorials", "Command index", "Copy", "Copied", "Select and copy the code manually", "min", "Updated", "Clear filters", "Filter updated"],
  ja: ["Codex 学習ガイド", "最初のタスクから高度な連携まで、習熟度・環境・目的で探せます。", "チュートリアルやコマンドを検索", "習熟度", "環境", "目的", "すべて", "初心者", "日常の作業", "高度な連携", "デスクトップ", "モバイル", "CLI", "IDE", "クラウド", "セットアップ", "MD 設定", "コマンド", "デバッグ", "Git", "自動化", "企画中", "未公開", "公開状況を一時的に確認できません", "該当する記事がありません", "Codex 学習ガイドに戻る", "前の記事", "次の記事", "関連記事", "コマンド索引", "コピー", "コピーしました", "コードを選択して手動でコピーしてください", "分", "更新", "絞り込みを解除", "絞り込みを更新しました"],
  ko: ["Codex 학습 센터", "첫 작업부터 고급 연동까지 수준, 플랫폼, 목표에 따라 튜토리얼을 찾으세요.", "튜토리얼 또는 명령 검색", "수준", "플랫폼", "목표", "전체", "입문", "일상 작업", "고급 연동", "데스크톱", "모바일", "CLI", "IDE", "클라우드", "설치", "MD 설정", "명령", "디버깅", "Git", "자동화", "기획 중", "미게시", "게시 상태를 일시적으로 확인할 수 없습니다", "일치하는 튜토리얼이 없습니다", "Codex 학습 목차로 돌아가기", "이전 글", "다음 글", "관련 튜토리얼", "명령 색인", "복사", "복사됨", "코드를 선택하여 직접 복사하세요", "분", "업데이트", "필터 초기화", "필터를 업데이트했습니다"],
} satisfies Record<Locale, string[]>;

export function learningCopy(locale: Locale) {
  const r = rows[locale];
  return { title: r[0], intro: r[1], search: r[2], level: r[3], platform: r[4], goal: r[5], all: r[6], levels: r.slice(7, 10), platforms: r.slice(10, 15), goals: r.slice(15, 21), planned: r[21], unpublished: r[22], unavailable: r[23], empty: r[24], back: r[25], previous: r[26], next: r[27], related: r[28], commands: r[29], copy: r[30], copied: r[31], copyFailed: r[32], minutes: r[33], updated: r[34], clear: r[35], filtered: r[36] };
}

export function editorBlockCopy(locale: Locale) {
  return ({
    "zh-TW": { code: "程式碼", rich_paragraph: "含連結段落", language: "程式語言", addText: "新增文字", addLink: "新增連結" },
    "zh-CN": { code: "代码", rich_paragraph: "含链接段落", language: "编程语言", addText: "添加文字", addLink: "添加链接" },
    en: { code: "Code", rich_paragraph: "Linked paragraph", language: "Code language", addText: "Add text", addLink: "Add link" },
    ja: { code: "コード", rich_paragraph: "リンク付き段落", language: "コード言語", addText: "テキストを追加", addLink: "リンクを追加" },
    ko: { code: "코드", rich_paragraph: "링크가 있는 문단", language: "코드 언어", addText: "텍스트 추가", addLink: "링크 추가" },
  })[locale];
}
