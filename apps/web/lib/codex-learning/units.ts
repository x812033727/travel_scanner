import type { Locale } from "@/i18n/routing";

import labels from "./units.json";

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
