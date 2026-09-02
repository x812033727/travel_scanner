import { AdminUsersPanel } from "@/components/admin-users-panel";

export default function AdminUsersPage() {
  return <main className="admin-page"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">會員與使用次數</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">搜尋會員、管理帳號與管理員權限，並透過可稽核帳本增加或扣除使用次數。</p><AdminUsersPanel /></main>;
}
