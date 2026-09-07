import type { ReactNode } from "react";
import { SiteHeader } from "@/components/site-header";
import { CommunityGate, CommunityLinks } from "@/components/community/shell";
export default function CommunityLayout({ children }: { children: ReactNode }) {
  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 py-8 pb-24"><CommunityGate><CommunityLinks />{children}</CommunityGate></main></>;
}
