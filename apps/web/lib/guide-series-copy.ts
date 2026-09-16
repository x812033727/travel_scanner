import type { Locale } from "@/i18n/routing";

const zhTW = {
  hub: "Claude Code 教學目錄", search: "搜尋教學、指令或檔名", group: "主題", level: "程度", platform: "平台",
  all: "全部", clear: "清除篩選", paths: "推薦學習路線", contents: "本篇目錄", previous: "上一篇", next: "下一篇",
  back: "回總目錄", prerequisites: "先備知識", related: "延伸閱讀", empty: "沒有符合條件的教學，試試其他關鍵字或清除篩選。",
  unavailable: "暫時無法載入教學目錄，請稍後重試。", retry: "重新載入", minutes: "分鐘", filtered: "已更新篩選結果",
  entry: "從安裝、MD 設定到進階實作，依平台或指令找到下一篇教學。",
  copy: "複製", copied: "已複製", copyFailed: "無法自動複製，請選取下方文字複製。",
  rich_paragraph: "段落與文字連結", code: "程式碼範例", text: "文字", inlineCode: "行內程式碼",
  external: "外部連結", article: "站內文章", add: "加入片段", remove: "移除", up: "上移", down: "下移",
  slug: "文章短網址", kind: "文章類型", url: "網址", label: "輸入位置或檔名", language: "範例語言",
  beginner: "入門", intermediate: "實作", advanced: "進階",
};
type Copy = { [K in keyof typeof zhTW]: string };
const en: Copy = {
  hub: "Claude Code tutorials", search: "Search tutorials, commands or files", group: "Topic", level: "Level", platform: "Platform",
  all: "All", clear: "Clear filters", paths: "Learning paths", contents: "On this page", previous: "Previous", next: "Next",
  back: "Back to directory", prerequisites: "Before you start", related: "Related tutorials", empty: "No matching tutorials. Try another search or clear the filters.",
  unavailable: "The tutorial directory is temporarily unavailable.", retry: "Reload", minutes: "min", filtered: "Filter updated",
  entry: "Find tutorials by platform or command, from installation and Markdown to advanced workflows.",
  copy: "Copy", copied: "Copied", copyFailed: "Copy failed. Select the code below and copy it manually.",
  rich_paragraph: "Paragraph with links", code: "Code example", text: "Text", inlineCode: "Inline code", external: "External link", article: "Article reference",
  add: "Add segment", remove: "Remove", up: "Move up", down: "Move down", slug: "Article slug", kind: "Article type", url: "URL", label: "Input location or filename", language: "Language",
  beginner: "Beginner", intermediate: "Practical", advanced: "Advanced",
};
const copies: Record<Locale, Copy> = {
  "zh-TW": zhTW, en,
  "zh-CN": { ...zhTW, hub: "Claude Code 教学目录", search: "搜索教程、命令或文件名", group: "主题", platform: "平台", clear: "清除筛选", paths: "推荐学习路线", contents: "本篇目录", back: "回总目录", prerequisites: "预备知识", related: "相关阅读", empty: "没有符合条件的教程，请尝试其他关键词。", unavailable: "暂时无法加载教程目录。", retry: "重新加载", minutes: "分钟", filtered: "已更新筛选结果", entry: "从安装、MD 设置到进阶实践，按平台或命令查找教程。", copy: "复制", copied: "已复制", copyFailed: "无法自动复制，请选择下方文字复制。", rich_paragraph: "段落与文字链接", code: "代码示例", inlineCode: "行内代码", external: "外部链接", article: "站内文章", add: "加入片段", remove: "移除", slug: "文章短网址", kind: "文章类型", url: "网址", label: "输入位置或文件名", language: "示例语言", intermediate: "实践", advanced: "进阶" },
  ja: { ...en, hub: "Claude Code チュートリアル", search: "記事・コマンド・ファイル名を検索", group: "テーマ", level: "難易度", platform: "環境", all: "すべて", clear: "絞り込みを解除", paths: "学習コース", contents: "この記事の目次", previous: "前の記事", next: "次の記事", back: "総目次へ", prerequisites: "事前に読む記事", related: "関連記事", empty: "該当する記事がありません。検索条件を変更してください。", unavailable: "目次を読み込めませんでした。", retry: "再読み込み", minutes: "分", filtered: "絞り込みを更新しました", entry: "インストール、MD 設定、実践的な操作を環境やコマンドで探せます。", copy: "コピー", copied: "コピーしました", copyFailed: "コピーできませんでした。下のコードを選択してコピーしてください。", rich_paragraph: "リンク付き段落", code: "コード例", text: "テキスト", inlineCode: "インラインコード", external: "外部リンク", article: "記事リンク", add: "要素を追加", remove: "削除", up: "上へ", down: "下へ", slug: "記事スラッグ", kind: "記事の種類", url: "URL", label: "入力場所・ファイル名", language: "言語", beginner: "入門", intermediate: "実践", advanced: "上級" },
  ko: { ...en, hub: "Claude Code 사용 안내", search: "글, 명령어, 파일명 검색", group: "주제", level: "난이도", platform: "환경", all: "전체", clear: "필터 초기화", paths: "추천 학습 순서", contents: "이 글의 목차", previous: "이전 글", next: "다음 글", back: "전체 목차", prerequisites: "먼저 읽을 글", related: "관련 글", empty: "검색 결과가 없습니다. 검색 조건을 변경하세요.", unavailable: "목차를 불러올 수 없습니다.", retry: "새로고침", minutes: "분", filtered: "필터를 업데이트했습니다", entry: "설치, MD 설정부터 고급 사용법까지 환경이나 명령어로 찾아보세요.", copy: "복사", copied: "복사됨", copyFailed: "복사하지 못했습니다. 아래 코드를 선택해 복사하세요.", rich_paragraph: "링크가 있는 문단", code: "코드 예제", text: "텍스트", inlineCode: "인라인 코드", external: "외부 링크", article: "글 링크", add: "요소 추가", remove: "삭제", up: "위로", down: "아래로", slug: "글 슬러그", kind: "글 유형", url: "URL", label: "입력 위치 또는 파일명", language: "언어", beginner: "입문", intermediate: "실습", advanced: "고급" },
};
export function seriesCopy(locale: string): Copy { return copies[locale as Locale] ?? en; }
export function platformLabel(value: string): string {
  return ({ cli: "CLI", desktop: "Desktop", web: "Web", windows: "Windows", macos: "macOS", linux: "Linux / WSL", ios: "iOS / iPadOS", android: "Android", ide: "VS Code / JetBrains" } as Record<string, string>)[value] ?? value;
}
