import { AdminNav } from "@/components/admin-nav";
import { AdminUsersPanel } from "@/components/admin-users-panel";
import { SiteHeader } from "@/components/site-header";

export default function AdminUsersPage() {
  return <><SiteHeader /><main className="mx-auto max-w-7xl px-5 pb-16 pt-8 md:px-8"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-4xl font-bold">會員與使用次數</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">搜尋會員、管理帳號與管理員權限，並透過可稽核帳本增加或扣除使用次數。</p><AdminNav current="users" /><AdminUsersPanel /></main></>;
}
