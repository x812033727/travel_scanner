import { AdminNav } from "@/components/admin-nav";
import { SiteHeader } from "@/components/site-header";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return <><SiteHeader /><div className="admin-app-shell mx-auto max-w-[96rem] px-4 pb-16 pt-5 md:px-7"><AdminNav /><div className="min-w-0">{children}</div></div></>;
}
