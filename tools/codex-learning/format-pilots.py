"""One-time editorial formatting of explicit pilot sources; safe to rerun."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2] / "docs/codex-learning/deep"
tables = {
    10: {
        "zh-TW": "| 範圍 | 位置 | 本篇的處理 |\n| --- | --- | --- |\n| 全域 | CODEX_HOME，預設為使用者的 .codex | 先保留原設定 |\n| 專案 | codex-practice/AGENTS.md | 新增並用新工作階段驗證 |\n| 同層替代 | AGENTS.override.md | 檢查是否優先選入 |",
        "en": "| Scope | Location | Treatment here |\n| --- | --- | --- |\n| Global | CODEX_HOME, default user .codex | Preserve existing settings |\n| Project | codex-practice/AGENTS.md | Add and verify in a new session |\n| Same-level override | AGENTS.override.md | Check whether it takes precedence |",
        "ja": "| 範囲 | 場所 | 今回の扱い |\n| --- | --- | --- |\n| 全体 | CODEX_HOME、既定はホームの .codex | 既存設定を残す |\n| プロジェクト | codex-practice/AGENTS.md | 追加して新規セッションで確認 |\n| 同階層の優先候補 | AGENTS.override.md | 優先されていないか確認 |",
        "ko": "| 범위 | 위치 | 이번 처리 |\n| --- | --- | --- |\n| 전역 | CODEX_HOME, 기본 사용자 .codex | 기존 설정 보존 |\n| 프로젝트 | codex-practice/AGENTS.md | 추가 후 새 세션에서 확인 |\n| 같은 위치의 우선 파일 | AGENTS.override.md | 우선 선택 여부 확인 |",
    },
    4: {
        "zh-TW": "| 工作位置 | 提供什麼 | 如何核對 |\n| --- | --- | --- |\n| 手機 | 需求、追問、核准 | Remote 中選中的主機與任務 |\n| Mac / Windows 主機 | 專案檔案與本機工具 | 實際工作目錄與檔案內容 |\n| 雲端環境 | 另外設定的程式與依賴 | 雲端任務的環境與分支 |",
        "en": "| Location | Supplies | Verification |\n| --- | --- | --- |\n| Phone | Prompts, follow-ups, approvals | Selected Remote host and task |\n| Mac / Windows host | Project files and local tools | Actual directory and file contents |\n| Cloud environment | Separately configured code and dependencies | Cloud task environment and branch |",
        "ja": "| 場所 | 提供するもの | 確認方法 |\n| --- | --- | --- |\n| スマートフォン | 依頼、追問、承認 | Remote で選んだホストとタスク |\n| Mac / Windows ホスト | ファイルとローカルツール | 実パスと内容 |\n| クラウド環境 | 別設定のコードと依存関係 | クラウドタスクの環境とブランチ |",
        "ko": "| 위치 | 제공 항목 | 확인 방법 |\n| --- | --- | --- |\n| 휴대전화 | 요청, 후속 질문, 승인 | 선택한 Remote 호스트와 작업 |\n| Mac / Windows 호스트 | 파일과 로컬 도구 | 실제 경로와 파일 내용 |\n| 클라우드 환경 | 별도로 설정한 코드와 의존성 | 클라우드 작업 환경과 브랜치 |",
    },
    23: {
        "zh-TW": "| 狀態 | 可以證明什麼 | 尚不能證明什麼 |\n| --- | --- | --- |\n| 格式有效 | 必要欄位可以解析 | 會被選到 |\n| 已發現 | 選單找到正確名稱與路徑 | 已讀取完整流程 |\n| 已採用 | 任務讀取技能內容 | 所有檢查都完成 |\n| 已驗證 | 有實際測試或畫面結果 | 已經發布網站 |",
        "en": "| State | Evidence establishes | Does not establish |\n| --- | --- | --- |\n| Valid format | Required metadata parses | Selection will occur |\n| Discovered | Selector shows correct name and path | Full workflow was read |\n| Selected | Task reads the instructions | Every check completed |\n| Verified | Actual test or browser observations | Website publication |",
        "ja": "| 状態 | 証明できること | まだ証明できないこと |\n| --- | --- | --- |\n| 形式が有効 | 必須項目を解析可能 | 選択されること |\n| 発見済み | 名前とパスが一覧にある | 全文を読んだこと |\n| 採用済み | タスクが指示を読む | 全検査の完了 |\n| 検証済み | 実テストや画面の観察 | サイトの公開 |",
        "ko": "| 상태 | 증명하는 것 | 아직 증명하지 않는 것 |\n| --- | --- | --- |\n| 유효한 형식 | 필수 항목 해석 가능 | 선택될 것 |\n| 발견됨 | 목록의 올바른 이름과 경로 | 전체 절차를 읽음 |\n| 선택됨 | 작업이 지침을 읽음 | 모든 검사 완료 |\n| 검증됨 | 실제 테스트나 화면 관찰 | 사이트 공개 |",
    },
}
diagram = {
    "zh-TW": "圖中的 01 是系統終端機，02 是 Codex 互動輸入，03 是需要核對的結果。",
    "en": "In the diagram, 01 is the system terminal, 02 is Codex interactive input, and 03 is the result to verify.",
    "ja": "図の 01 はシステム端末、02 は Codex の対話入力、03 は確認する結果です。",
    "ko": "그림의 01은 시스템 터미널, 02는 Codex 대화 입력, 03은 확인할 결과입니다.",
}
for locale in ["zh-TW", "en", "ja", "ko"]:
    for lesson in [3, 4, 10, 11, 23]:
        path = ROOT / locale / f"{lesson:02d}.md"
        text = path.read_text(encoding="utf-8")
        first = re.search(r"^## [^\n]+\n\n([^\n]+)", text, re.M)
        if first and not first.group(1).startswith(">"):
            text = text[:first.start(1)] + "> " + text[first.start(1):]
        table = tables.get(lesson, {}).get(locale)
        if table and table not in text:
            index = text.rfind("\n## ")
            text = text[:index] + "\n\n" + table + "\n" + text[index:]
        if lesson == 11 and diagram[locale] not in text:
            index = text.rfind("\n## ")
            text = text[:index] + "\n\n" + diagram[locale] + "\n" + text[index:]
        path.write_text(text, encoding="utf-8")
