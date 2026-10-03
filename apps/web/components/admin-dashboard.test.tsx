import { render, screen, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminDashboard } from "./admin-dashboard";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { api } from "@/lib/api";
import adminCopy from "../messages/zh-TW/admin.json";
import type { AdminBootstrap } from "@/lib/admin-operations";

vi.mock("@/lib/api", () => ({ api: vi.fn() }));

const knownPending = {
  hotspots_pending: 2,
  guides_pending: 0,
  foods_pending: 0,
  merchants_pending: 0,
  hotels_pending: 0,
  news_review_pending: 7,
  video_reviews_pending: 0,
};
const allCatalogs = ["hotspots", "foods", "hotels", "news", "videos"];

function bootstrapFor(catalogs: string[], pendingCounts: Record<string, number>): AdminBootstrap {
  return {
    admin_roles: ["content_editor"],
    admin_capabilities: ["admin.access", "dashboard.read", "content.read"],
    navigation: [
      { key: "dashboard", href: "/admin", group: "overview" },
      ...catalogs.map((key) => ({ key, href: `/admin/${key}`, group: "content" as const })),
    ],
    pending_counts: pendingCounts,
    system_status: {},
    environment: "test",
    can_deploy: false,
    can_manage_database: false,
  };
}

async function expectPendingTotal(value: string) {
  const summary = await screen.findByRole("region", { name: "營運摘要" });
  const total = within(summary).getByRole("link", { name: /待處理/ });
  expect(within(total).getByText(value)).toBeTruthy();
  expect(total.getAttribute("href")).toBe("#admin-review-queues");
  expect(screen.getByRole("region", { name: "內容目錄" }).id).toBe("admin-review-queues");
}

describe("domain overview", () => {
  it("shows independent catalogs and no fabricated publication percentage", async () => {
    vi.mocked(api).mockResolvedValue({ counts: { hotspots_total: 10, foods_total: 4, merchants_total: 6, hotels_total: 3, hotels_pending: 1, hotels_without_options: 2 }, can_deploy: false });
    render(<AdminDashboard />);
    const hotels = await screen.findByRole("region", { name: "飯店" });
    expect(hotels.textContent).toContain("3");
    expect(within(hotels).getByRole("link", { name: /飯店待審/ }).getAttribute("href")).toBe("/admin/hotels?tab=review&section=products&status=pending");
    const food = screen.getByRole("region", { name: "美食" });
    expect(food.textContent).toContain("4");
    expect(screen.queryByText(/%/)).toBeNull();
    expect(api).toHaveBeenCalledWith("/admin/dashboard");
  });

  it("never links a role to dashboard destinations absent from backend navigation", async () => {
    vi.mocked(api).mockResolvedValue({ counts: { users: 8, hotspots_total: 10 }, can_deploy: false });
    const bootstrap = {
      user: { id: "db", email: "db@example.com" }, admin_roles: ["database_operator"], admin_capabilities: ["admin.access", "dashboard.read", "database.read"],
      navigation: [{ key: "dashboard", href: "/admin", group: "overview" as const }, { key: "database", href: "/admin/database", group: "system" as const }],
      pending_counts: {}, system_status: { database: { status: "healthy" as const }, background_jobs: { status: "degraded" as const } }, environment: "test", can_deploy: false, can_manage_database: false,
    };
    render(<AdminOperationsProvider bootstrap={bootstrap}><AdminDashboard /></AdminOperationsProvider>);
    await screen.findByText("系統狀態");
    expect(screen.queryByRole("link", { name: /使用者/ })).toBeNull();
    expect(screen.queryByRole("region", { name: "景點" })).toBeNull();
    expect(screen.queryByRole("region", { name: adminCopy.navigation.news })).toBeNull();
    expect(screen.queryByRole("region", { name: "影片" })).toBeNull();
    expect(screen.queryByRole("link", { name: /待處理/ })).toBeNull();
    expect(screen.getByRole("link", { name: /資料庫/ }).getAttribute("href")).toBe("/admin/database");
    expect(screen.getByText("背景工作")).toBeTruthy();
    expect(screen.getByText("部分異常")).toBeTruthy();
  });

  it("shows the news review and video work queues alongside the catalogs", async () => {
    vi.mocked(api).mockResolvedValue({ counts: knownPending, can_deploy: false });
    render(<AdminDashboard />);

    const news = await screen.findByRole("region", { name: adminCopy.navigation.news });
    expect(within(news).getByRole("heading", { name: adminCopy.navigation.news })).toBeTruthy();
    const newsQueue = within(news).getByRole("link", { name: /新聞待審\s*7$/ });
    expect(newsQueue.getAttribute("href")).toBe("/admin/news?queue=review");
    expect(within(news).getByRole("link", { name: "進入管理" }).getAttribute("href")).toBe("/admin/news");
    const videos = screen.getByRole("region", { name: "影片" });
    expect(within(videos).getByRole("link", { name: /影片待處理\s*0$/ }).getAttribute("href")).toBe("/admin/videos");
  });

  it("sums all seven known queue counts without bootstrap instead of trusting a stale total", async () => {
    vi.mocked(api).mockResolvedValue({ counts: { ...knownPending, pending_total: 999 }, can_deploy: false });
    render(<AdminDashboard />);

    await expectPendingTotal("9");
  });

  it.each([0, 3])("uses bootstrap pending counts over stale dashboard counts, including %i video items", async (videoCount) => {
    vi.mocked(api).mockResolvedValue({
      counts: Object.fromEntries([...Object.keys(knownPending), "pending_total"].map((key) => [key, 100])),
      can_deploy: false,
    });
    const bootstrap = bootstrapFor(allCatalogs, { ...knownPending, video_reviews_pending: videoCount });
    render(<AdminOperationsProvider bootstrap={bootstrap}><AdminDashboard /></AdminOperationsProvider>);

    await expectPendingTotal(String(9 + videoCount));
    expect(screen.getByRole("link", { name: /新聞待審\s*7$/ })).toBeTruthy();
    expect(screen.getByRole("link", { name: new RegExp(`影片待處理\\s*${videoCount}$`) })).toBeTruthy();
  });

  it("hides news and videos without navigation and sums only the visible queues", async () => {
    vi.mocked(api).mockResolvedValue({ counts: { ...knownPending, pending_total: 999 }, can_deploy: false });
    const bootstrap = bootstrapFor(["hotspots", "foods", "hotels"], {
      ...knownPending, news_review_pending: 70, video_reviews_pending: 30,
    });
    render(<AdminOperationsProvider bootstrap={bootstrap}><AdminDashboard /></AdminOperationsProvider>);

    await expectPendingTotal("2");
    expect(screen.queryByRole("region", { name: adminCopy.navigation.news })).toBeNull();
    expect(screen.queryByRole("region", { name: "影片" })).toBeNull();
    expect(screen.queryByRole("link", { name: /新聞待審|影片待處理/ })).toBeNull();
  });

  it.each([
    ["news", "news_review_pending", 7, "新聞待審", "/admin/news?queue=review"],
    ["videos", "video_reviews_pending", 3, "影片待處理", "/admin/videos"],
  ] as const)("shows a pending total with only %s navigation even when hidden counts are missing", async (catalog, countKey, value, label, href) => {
    vi.mocked(api).mockResolvedValue({ counts: {}, can_deploy: false });
    const bootstrap = bootstrapFor([catalog], { [countKey]: value });
    render(<AdminOperationsProvider bootstrap={bootstrap}><AdminDashboard /></AdminOperationsProvider>);

    await expectPendingTotal(String(value));
    expect(screen.getByRole("link", { name: new RegExp(`${label}\\s*${value}$`) }).getAttribute("href")).toBe(href);
    expect(screen.queryByRole("region", { name: "景點" })).toBeNull();
    expect(screen.queryByRole("region", { name: "美食" })).toBeNull();
    expect(screen.queryByRole("region", { name: "飯店" })).toBeNull();
    const hiddenTitle = catalog === "news" ? "影片" : adminCopy.navigation.news;
    expect(screen.queryByRole("region", { name: hiddenTitle })).toBeNull();
  });

  it("keeps the total unknown when the dashboard has no counts", async () => {
    vi.mocked(api).mockResolvedValue({ can_deploy: false });
    render(<AdminDashboard />);

    await expectPendingTotal("—");
  });

  it.each(Object.keys(knownPending))("keeps the total unknown when visible count %s is missing", async (missingKey) => {
    const counts: Record<string, number> = { ...knownPending, pending_total: 999 };
    delete counts[missingKey];
    vi.mocked(api).mockResolvedValue({ counts, can_deploy: false });
    render(<AdminDashboard />);

    await expectPendingTotal("—");
  });

  it("shows zero when every visible queue explicitly has zero pending items", async () => {
    const counts = Object.fromEntries(Object.keys(knownPending).map((key) => [key, 0]));
    vi.mocked(api).mockResolvedValue({ counts, can_deploy: false });
    render(<AdminDashboard />);

    await expectPendingTotal("0");
  });
});
