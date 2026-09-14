import type { Locale } from "@/i18n/routing";

const localeIndex: Record<Locale, number> = { "zh-TW": 0, "zh-CN": 1, en: 2, ja: 3, ko: 4 };
// Terminal commands, interactive slash commands and configuration files are separate surfaces.
const rows = [
  [5, "Terminal", "npm install -g @openai/codex", ["安裝或更新 CLI", "安装或更新 CLI", "Install or update the CLI", "CLI をインストール・更新", "CLI 설치 또는 업데이트"]],
  [5, "Terminal", "codex", ["在目前資料夾啟動", "在当前文件夹启动", "Start in the current directory", "現在のフォルダーで起動", "현재 폴더에서 시작"]],
  [11, "Terminal", "codex --help", ["查閱此版本支援的命令", "查看此版本支持的命令", "Inspect commands supported by this version", "現在のバージョンのコマンドを確認", "현재 버전의 명령 확인"]],
  [11, "Terminal", "codex resume", ["恢復既有工作階段", "恢复现有会话", "Resume an existing session", "既存セッションを再開", "기존 세션 재개"]],
  [8, "CLI / interactive", "/plan", ["進入規劃模式", "进入规划模式", "Enter Plan mode", "計画モードに入る", "계획 모드 시작"]],
  [11, "CLI / interactive", "/status", ["查看工作階段狀態", "查看会话状态", "Inspect session status", "セッションの状態を確認", "세션 상태 확인"]],
  [17, "CLI / interactive", "/model", ["選擇可用模型與推理設定", "选择可用模型与推理设置", "Choose an available model and reasoning setting", "利用可能なモデルと推論設定を選択", "사용 가능한 모델과 추론 설정 선택"]],
  [18, "CLI / interactive", "/permissions", ["檢查權限設定", "检查权限设置", "Inspect permission settings", "権限設定を確認", "권한 설정 확인"]],
  [21, "CLI / interactive", "/review", ["檢查程式碼差異", "检查代码差异", "Review code changes", "コードの差分をレビュー", "코드 변경 검토"]],
  [22, "CLI / interactive", "/compact", ["整理目前上下文", "整理当前上下文", "Compact the current context", "現在のコンテキストを整理", "현재 컨텍스트 압축"]],
  [25, "CLI / interactive", "/mcp", ["查看工具連線", "查看工具连接", "Inspect tool connections", "ツール接続を確認", "도구 연결 확인"]],
  [11, "CLI / interactive", "/quit", ["離開互動工作階段", "退出交互会话", "Exit the interactive session", "対話セッションを終了", "대화형 세션 종료"]],
  [30, "Terminal", "codex exec -o report.txt \"Summarize this repository without changing files.\"", ["非互動執行並儲存回覆", "非交互执行并保存回复", "Run non-interactively and save the answer", "非対話で実行し回答を保存", "비대화형 실행 후 답변 저장"]],
  [10, "File", "AGENTS.md", ["設定專案長期規則", "设置项目长期规则", "Define persistent project rules", "プロジェクトの継続的なルールを設定", "프로젝트의 지속 규칙 설정"]],
  [16, "File", "config.toml", ["設定 Codex 行為", "设置 Codex 行为", "Configure Codex behavior", "Codex の動作を設定", "Codex 동작 설정"]],
  [23, "File", "SKILL.md", ["定義可重用技能", "定义可复用技能", "Define a reusable skill", "再利用可能なスキルを定義", "재사용할 스킬 정의"]],
] as const;

export function commandEntries(locale: Locale) {
  return rows.map(([lesson, surface, example, purpose]) => ({ lesson, surface, example, purpose: purpose[localeIndex[locale]] }));
}
