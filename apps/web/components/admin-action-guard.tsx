"use client";

import { Eye, LockKeyhole } from "lucide-react";
import { useLocale } from "next-intl";
import { useAdminOperations } from "@/components/admin-operations-provider";
import { adminCan } from "@/lib/admin-operations";

const copy = {
  "zh-TW": {
    title: "目前為唯讀模式",
    detail: "你可以查看資料與使用篩選，但現有管理員角色沒有這個頁面的修改權限。",
    action: "此操作需要額外管理權限",
  },
  "zh-CN": {
    title: "当前为只读模式",
    detail: "你可以查看数据和使用筛选，但当前管理员角色没有该页面的修改权限。",
    action: "此操作需要额外管理权限",
  },
  en: {
    title: "Read-only mode",
    detail: "You can inspect data and use filters, but your current admin roles cannot make changes on this page.",
    action: "This action requires an additional admin capability",
  },
  ja: {
    title: "読み取り専用モード",
    detail: "データの確認とフィルターは使用できますが、現在の管理者ロールではこのページを変更できません。",
    action: "この操作には追加の管理権限が必要です",
  },
  ko: {
    title: "읽기 전용 모드",
    detail: "데이터 조회와 필터는 사용할 수 있지만 현재 관리자 역할로는 이 페이지를 변경할 수 없습니다.",
    action: "이 작업에는 추가 관리 권한이 필요합니다",
  },
} as const;

function localeCopy(locale: string) {
  return copy[locale as keyof typeof copy] ?? copy.en;
}

/**
 * Capability source for legacy admin panels. A missing provider remains
 * permissive so isolated stories/tests and any non-admin reuse keep working;
 * every real admin route is wrapped by AdminOperationsProvider.
 */
export function useAdminActionGuard(capability: string) {
  const operations = useAdminOperations();
  const localized = localeCopy(useLocale());
  const allowed = !operations || adminCan(operations.bootstrap, capability);
  return {
    allowed,
    disabledReason: localized.action,
    disabledProps: allowed ? {} : { disabled: true, "aria-disabled": true, title: localized.action },
  } as const;
}

export function AdminReadOnlyNotice({ capability, className = "" }: { capability: string; className?: string }) {
  const operations = useAdminOperations();
  const localized = localeCopy(useLocale());
  if (!operations || adminCan(operations.bootstrap, capability)) return null;
  return <aside role="note" className={`rounded-2xl border border-sky-200 bg-sky-50 p-4 text-sm text-sky-950 ${className}`}>
    <p className="flex items-center gap-2 font-bold"><Eye aria-hidden size={17} />{localized.title}</p>
    <p className="mt-1 flex items-start gap-2 leading-6"><LockKeyhole aria-hidden className="mt-1 shrink-0" size={15} />{localized.detail}</p>
  </aside>;
}
