import type { Locale } from "@/i18n/routing";

const labels = {
  "zh-TW": ["基本概念", "安裝與電腦", "手機與跨裝置", "MD 與設定", "指令與工作階段", "日常開發", "Skills 與 Plugins", "工具與平行工作", "自動化與輸出", "實戰與維護"],
  "zh-CN": ["基本概念", "安装与电脑", "手机与跨设备", "MD 与设置", "命令与会话", "日常开发", "Skills 与 Plugins", "工具与并行工作", "自动化与输出", "实战与维护"],
  en: ["Foundations", "Setup and computers", "Mobile and devices", "MD and configuration", "Commands and sessions", "Everyday development", "Skills and Plugins", "Tools and parallel work", "Automation and output", "Workshops and maintenance"],
  ja: ["基本概念", "導入とパソコン", "モバイルと端末連携", "MD と設定", "コマンドとセッション", "日常の開発", "Skills と Plugins", "ツールと並行作業", "自動化と出力", "実践と保守"],
  ko: ["기본 개념", "설치와 컴퓨터", "모바일과 기기 연결", "MD와 설정", "명령과 세션", "일상 개발", "Skills와 Plugins", "도구와 병렬 작업", "자동화와 출력", "실전과 유지보수"],
} satisfies Record<Locale, string[]>;

export function learningUnits(locale: Locale) {
  return labels[locale].map((title, index) => ({ id: String.fromCharCode(65 + index), title }));
}

export function depthCopy(locale: Locale) {
  const value = {
    "zh-TW": ["單元", "建議閱讀順序", "先備教學", "閱讀", "操作", "待補教學"],
    "zh-CN": ["单元", "建议阅读顺序", "前置教程", "阅读", "操作", "待补教程"],
    en: ["Unit", "Suggested reading order", "Prerequisites", "Read", "Practice", "Planned lesson"],
    ja: ["単元", "おすすめの読む順序", "前提レッスン", "読む", "操作", "作成予定"],
    ko: ["단원", "추천 학습 순서", "선행 학습", "읽기", "실습", "작성 예정"],
  }[locale];
  return { unit: value[0], order: value[1], prerequisites: value[2], read: value[3], practice: value[4], pending: value[5] };
}
