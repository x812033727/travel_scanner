import { cleanup, render, screen, waitFor } from "@testing-library/react";
import { renderToString } from "react-dom/server";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DiscoveryExplorer } from "./explorer";
import type { DiscoveryItem } from "@/lib/discovery";

/**
 * What `/explore` puts in the response body.
 *
 * `useDiscoveryStatus` is deliberately NOT mocked here: its server snapshot is a fixed
 * `{ loading: true }`, which is exactly the thing these cases exist to cover. The switch and
 * the feed's first page arrive as props from the server render instead, and the assertions
 * below are on the HTML a crawler with no JavaScript receives.
 */

const mock = vi.hoisted(() => ({ api: vi.fn(), push: vi.fn(), query: "" }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams(mock.query) }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, status: "signed_out", sessionIdentity: null }) }));
vi.mock("@/components/community/provider", () => ({ useCommunity: () => ({ flags: { enabled: false }, me: null }) }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, scroll, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string; scroll?: boolean }) => {
    void scroll; return <a href={href} {...props}>{children}</a>;
  },
  usePathname: () => "/explore",
  useRouter: () => ({ push: mock.push, replace: mock.push, back: mock.push }),
}));

const item: DiscoveryItem = {
  id: "guide:11111111-1111-4111-8111-111111111111", kind: "article", title: "東京散步攻略",
  summary: "從官方步道資料開始", locale: "ja", href: "/hotspots",
  destination: { id: "tokyo", name: "東京" },
  source: { kind: "editorial", label: "City guide", url: "https://example.org/guide" },
  published_at: "2026-09-01T00:00:00Z", updated_at: null, thumbnail_url: null,
  collection_ref: { kind: "guide", id: "11111111-1111-4111-8111-111111111111" },
};
/** The skeleton's own accessible name, from `lib/frontend-flow-copy.ts`. */
const SKELETON = "正在載入旅行靈感";
const feedPath = "/discovery/feed?mode=recommended";
const initialFeed = { path: feedPath, page: { enabled: true, items: [item], next_cursor: null, query: "", filters: { kinds: [], destinations: [], topics: [] } } };

beforeEach(() => {
  mock.api.mockReset(); mock.query = "";
  mock.api.mockImplementation(async (path: string) => path.includes("/status") ? { enabled: true }
    : path.includes("/suggestions") ? { query: "", items: [], destinations: [], topics: [] }
    : initialFeed.page);
});
afterEach(cleanup);

describe("what /explore sends before any JavaScript runs", () => {
  it("carries the feed's first page, not a skeleton", () => {
    const html = renderToString(<DiscoveryExplorer initialEnabled initialFeed={initialFeed} />);
    expect(html).toContain("東京散步攻略");
    expect(html).toContain("<h1");
    // The skeleton's own label is what readers used to get for the first second or two.
    expect(html).not.toContain(SKELETON);
  });

  it("renders the closed state directly when the switch is off, instead of a skeleton first", () => {
    // Production runs with discovery off, so this is what /explore actually serves today.
    const html = renderToString(<DiscoveryExplorer initialEnabled={false} />);
    expect(html).toContain("<h1");
    expect(html).toContain("/hotspots");
    expect(html).not.toContain("東京散步攻略");
  });

  it("still sends a skeleton when the server could not resolve the switch", () => {
    // No prop: the request failed, or the component is rendered from somewhere that has no
    // server read. The client store answers after hydration, as it always did.
    const html = renderToString(<DiscoveryExplorer />);
    expect(html).toContain(SKELETON);
    expect(html).not.toContain("東京散步攻略");
  });
});

describe("what the browser does with a page the server already fetched", () => {
  it("shows the server's rows immediately and does not fetch them again", async () => {
    render(<DiscoveryExplorer initialEnabled initialFeed={initialFeed} />);
    expect(screen.getByText("東京散步攻略")).toBeTruthy();
    // The status poll and the filter suggestions still go out; the feed does not.
    await waitFor(() => expect(mock.api).toHaveBeenCalled());
    expect(mock.api.mock.calls.map(([path]) => String(path)).some((path) => path.startsWith("/discovery/feed"))).toBe(false);
  });

  it("fetches when the reader's URL asks for something else than the server prefetched", async () => {
    mock.query = "mode=latest";
    render(<DiscoveryExplorer initialEnabled initialFeed={initialFeed} />);
    await waitFor(() => expect(mock.api.mock.calls.some(([path]) => String(path).includes("mode=latest"))).toBe(true));
  });
});
