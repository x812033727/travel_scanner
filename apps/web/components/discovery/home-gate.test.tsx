import { cleanup, render, screen } from "@testing-library/react";
import { renderToString } from "react-dom/server";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { ReactNode } from "react";
import { Link } from "@/i18n/navigation";
import { DiscoveryHomeGate } from "./explorer";

const state = vi.hoisted(() => ({ enabled: false, loading: true }));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams() }));
vi.mock("@/lib/discovery", async (original) => ({
  ...await original<typeof import("@/lib/discovery")>(),
  useDiscoveryStatus: () => state,
  useDiscoveryResource: () => ({ data: null, loading: false, error: null }),
}));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: "anonymous" }) }));
vi.mock("@/components/community/provider", () => ({ useCommunity: () => ({ flags: { enabled: false } }) }));
vi.mock("./detail-drawer", () => ({ DiscoveryDetailBoundary: ({ children }: { children: ReactNode }) => children }));

const marketing = <main><h1>Travel inspiration</h1><Link href="/en/destinations/tokyo">Tokyo guide</Link></main>;
beforeEach(() => { state.enabled = false; state.loading = true; });
afterEach(cleanup);

describe("DiscoveryHomeGate server snapshot", () => {
  it("includes real marketing HTML when the server resolves off, even while the store is loading", () => {
    const html = renderToString(<DiscoveryHomeGate initialEnabled={false}>{marketing}</DiscoveryHomeGate>);
    expect(html).toContain("<h1>Travel inspiration</h1>");
    expect(html).toContain('href="/en/destinations/tokyo"');
  });

  it("does not substitute the marketing page for enabled discovery during its initial load", () => {
    const html = renderToString(<DiscoveryHomeGate initialEnabled>{marketing}</DiscoveryHomeGate>);
    expect(html).not.toContain("Travel inspiration");
    expect(html).toContain("<main");
  });

  it("still switches to discovery after an off or failed server snapshot, and back when disabled", () => {
    const view = render(<DiscoveryHomeGate initialEnabled={false}>{marketing}</DiscoveryHomeGate>);
    expect(screen.getByRole("heading", { name: "Travel inspiration" })).toBeTruthy();
    state.enabled = true; state.loading = false;
    view.rerender(<DiscoveryHomeGate initialEnabled={false}>{marketing}</DiscoveryHomeGate>);
    expect(screen.queryByRole("heading", { name: "Travel inspiration" })).toBeNull();
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    state.enabled = false;
    view.rerender(<DiscoveryHomeGate initialEnabled={false}>{marketing}</DiscoveryHomeGate>);
    expect(screen.getByRole("heading", { name: "Travel inspiration" })).toBeTruthy();
  });
});
