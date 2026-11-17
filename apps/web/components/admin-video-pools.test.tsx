import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { PoolEpisodePage, PoolExpansions, PoolOverview, PoolTheme, PoolThemeDetail, PoolThemePage } from "./admin-video-pools";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoReviews } from "./admin-video-reviews";
import { api } from "@/lib/api";
import { videoPoolsCopy } from "@/lib/video-pools-copy";

vi.mock("@/lib/api", () => ({ api: vi.fn() }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));
const copy = videoPoolsCopy("zh-TW");
const counts = { raw_records: 1868, selected: 1512, themes: 155, long_themes: 155, producible: 77, long_reserve: 78, scored: 155, improved: 114 };
const overview: PoolOverview = { series: [
  { key: "curio", name: "奇聞檔案局", revision: "2026-11-13-curio-pool-1512", audience_min: 6.5, themes_sha256: "a".repeat(64), counts },
  { key: "so-thats-why", name: "原來如此事務所", revision: "2026-11-13-pool-5125", audience_min: 6.5, themes_sha256: "b".repeat(64), counts: { ...counts, producible: 95 } },
] };
const audience = { score: 7.08, rank: 3, of: 155, click: 7, hook: 7.5, surprise: 7, payoff: 7, share: 7, demand: 7.75, base: 6.95, comment: "鬼故事對史書很過癮", reviewed_on: "2026-11-14", rounds: [{ score: 4.51, comment: "太冷門", changes: "片名改成問句", reviewed_on: "2026-11-14" }] };
const theme = (fields: Partial<PoolTheme> = {}): PoolTheme => ({ id: "T78", title: "鬼故事裡的人名都是真的？", category: "G-靈異與超自然公案", core_question: "筆記裡的鬼拿實錄一對會怎樣？", target_minutes: 10, long: true, producible: true, material: { verdict: "ready", missing: null }, candidates: 3, audience, ...fields });
const detail: PoolThemeDetail = { ...theme(), chapters: [{ title: "開場：一本筆記", seconds: 60, new_information: "筆記裡的鬼有名有姓" }], boredom_risk: "三段結構重複", drop_if: "來源對不上就刪章", evidence_gaps: "實錄卷數待補" };
const themes = (items = [theme()]): PoolThemePage => ({ items, total: items.length, page: 1, page_size: 25, categories: [{ category: "G-靈異與超自然公案", count: 1 }] });
const expansions: PoolExpansions = { expansions: [{ batch_id: "wave52-20261113", created_on: "2026-11-13", scope: "第五十二批新題", candidates: 20, selected: 20, not_added: 38, sources: 183 }], checkpoints: [] };
const episodes: PoolEpisodePage = { total: 2, published: 1, unpublished: 1, items: [
  { key: "sothatswhy-p14-sky-colors", code: "P14", title: "天空為什麼是藍的", category: "地球天氣與太空", slugs: ["sothatswhy-p14-sky-colors"], candidate_ids: ["LEG-S02"], published: true, youtube_id: "5xf1VoDNXWo", youtube_url: "https://www.youtube.com/watch?v=5xf1VoDNXWo", youtube_source: "site", site_slug: "sothatswhy-p14-sky-colors", publish_at: "2026-11-20T10:00:00Z", stage: "published", dropped: false, privacy: null },
  { key: "P04", code: "P04", title: "P04", category: null, slugs: [], candidate_ids: ["LEG-S48"], published: false, youtube_id: null, youtube_url: null, youtube_source: null, site_slug: null, publish_at: null, stage: null, dropped: false, privacy: null },
] };
const provider = { admin_roles: [], admin_capabilities: ["content.read"], navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
const renderAt = (url: string) => {
  window.history.replaceState(null, "", url);
  return render(<AdminOperationsProvider bootstrap={provider}><AdminVideoReviews /></AdminOperationsProvider>);
};
const calls = () => vi.mocked(api).mock.calls.filter(([path]) => String(path).startsWith("/admin/video-pools"));
afterEach(() => {
  vi.mocked(api).mockReset();
  window.history.replaceState(null, "", "/");
});

function respond(themePage = themes()) {
  vi.mocked(api).mockImplementation(async (path) => {
    const value = String(path);
    if (value === "/admin/video-pools") return overview;
    if (value.includes("/expansions")) return expansions;
    if (value.includes("/episodes?")) return value.includes("status=unpublished") ? { ...episodes, items: [episodes.items[1]], total: 1 } : episodes;
    if (/\/themes\/[^?]+$/.test(value)) return detail;
    if (value.includes("/themes?")) return themePage;
    throw new Error(`unexpected ${value}`);
  });
}

describe("topic pools in video admin", () => {
  it("shows producible themes with counts, scores and the score history, read-only", async () => {
    respond();
    renderAt("/zh-TW/admin/videos?tab=pools");
    expect(await screen.findByRole("heading", { name: theme().title })).toBeTruthy();
    expect(screen.getByRole("tab", { name: copy.tab }).getAttribute("aria-selected")).toBe("true");
    expect(await screen.findByText("77")).toBeTruthy();
    expect(screen.getByText("7.08")).toBeTruthy();
    expect(screen.getByText("第 3／155 名")).toBeTruthy();
    expect(calls().some(([path]) => String(path) === "/admin/video-pools/curio/themes?status=producible&page=1&page_size=25")).toBe(true);
    fireEvent.click(screen.getByText(copy.details));
    expect(await screen.findByText("筆記裡的鬼有名有姓")).toBeTruthy();
    expect(screen.getByText(/2026-11-14.4\.51 分：太冷門/)).toBeTruthy();
    expect(screen.getByText("之後改了：片名改成問句")).toBeTruthy();
    expect(calls().every(([, options]) => !options?.method || options.method === "GET")).toBe(true);
  });

  it("keeps series, filters and view in the URL", async () => {
    respond();
    renderAt("/zh-TW/admin/videos?tab=pools&pool_series=so-thats-why&pool_status=reserve&pool_min=7");
    await screen.findByRole("heading", { name: theme().title });
    expect(calls().some(([path]) => String(path).startsWith("/admin/video-pools/so-thats-why/themes?status=reserve") && String(path).includes("min_score=7"))).toBe(true);
    fireEvent.change(screen.getByRole("combobox", { name: copy.viewLabel }), { target: { value: "expansions" } });
    await waitFor(() => expect(new URL(window.location.href).searchParams.get("pool_view")).toBe("expansions"));
    expect(await screen.findByText("新增 20 題，入選 20，未收 38，來源 183 筆")).toBeTruthy();
  });

  it("says so when nothing matches", async () => {
    respond(themes([]));
    renderAt("/zh-TW/admin/videos?tab=pools&pool_q=zzz");
    expect(await screen.findByText(copy.empty)).toBeTruthy();
  });

  it("lists produced episodes with their YouTube id and filters by published status", async () => {
    respond();
    renderAt("/zh-TW/admin/videos?tab=pools&pool_series=so-thats-why&pool_view=published");
    const link = await screen.findByRole("link", { name: "5xf1VoDNXWo" });
    expect(link.getAttribute("href")).toBe("https://www.youtube.com/watch?v=5xf1VoDNXWo");
    expect(screen.getByText("題號：LEG-S02")).toBeTruthy();
    expect(screen.getByText("預定公開：2026-11-20")).toBeTruthy();
    expect(calls().some(([path]) => String(path) === "/admin/video-pools/so-thats-why/episodes?status=published")).toBe(true);
    fireEvent.change(screen.getByRole("combobox", { name: copy.publishedLabel }), { target: { value: "unpublished" } });
    await waitFor(() => expect(new URL(window.location.href).searchParams.get("pool_published")).toBe("unpublished"));
    expect(await screen.findByRole("heading", { name: "P04" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "5xf1VoDNXWo" })).toBeNull();
  });
});
