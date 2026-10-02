import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminVideoPlans, type VideoPlan, type VideoPlanPage } from "./admin-video-plans";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { AdminVideoReviews } from "./admin-video-reviews";
import { api } from "@/lib/api";
import { videoPlansCopy } from "@/lib/video-plans-copy";

vi.mock("@/lib/api", () => ({ api: vi.fn() }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: null, sessionIdentity: null, status: undefined }) }));
const copy = videoPlansCopy("zh-TW");
const plan = (fields: Partial<VideoPlan> = {}): VideoPlan => ({
  catalog: "season2", id: "B28", title: "2018年Saks，為何把美妝搬到二樓？", video_slug: "sothatswhy-b28",
  stage: "REVIEWED_OUTLINE_NOT_MEDIA", source_status: "reviewed", target_duration_seconds: 600, min_duration_seconds: 480,
  source_path: "docs/videos/so-thats-why/season2/dispositions.json", source_sha256: "a".repeat(64), source_record_sha256: "b".repeat(64),
  source_package_path: null, source_package_sha256: null, details: [{ label: "effective_inputs", text: "Source-bound narrative premise" }], ...fields,
});
const page = (items = [plan()], fields: Partial<VideoPlanPage> = {}): VideoPlanPage => ({
  items, total: 473, page: 1, page_size: 25, catalog_total: 473, plans_sha256: "c".repeat(64),
  catalogs: [{ catalog: "season1", count: 100 }, { catalog: "season2", count: 92 }, { catalog: "season3", count: 100 }, { catalog: "brand-stories", count: 100 }, { catalog: "ai-terms", count: 81 }], ...fields,
});
const calls = () => vi.mocked(api).mock.calls.filter(([path]) => path.startsWith("/admin/video-plans"));
afterEach(() => {
  vi.mocked(api).mockReset();
  window.history.replaceState(null, "", "/");
});

describe("long-form plans in video admin", () => {
  it("opens from the URL for a content reader, keeps the production title and exposes no production action", async () => {
    vi.mocked(api).mockResolvedValue(page());
    window.history.replaceState(null, "", "/zh-TW/admin/videos?tab=plans");
    render(<AdminOperationsProvider bootstrap={{ admin_roles: [], admin_capabilities: ["content.read"], navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false }}><AdminVideoReviews /></AdminOperationsProvider>);
    expect(await screen.findByText("五類共 473 筆企劃")).toBeTruthy();
    expect(screen.getByRole("tab", { name: copy.tab }).getAttribute("aria-selected")).toBe("true");
    expect(screen.getByRole("heading", { name: plan().title })).toBeTruthy();
    expect(screen.getByText(copy.stages.REVIEWED_OUTLINE_NOT_MEDIA)).toBeTruthy();
    expect(screen.getByText(copy.minimum)).toBeTruthy();
    const catalog = screen.getByRole("combobox", { name: copy.catalog });
    expect(within(catalog).getAllByRole("option").map((option) => option.textContent))
      .toEqual(["全部分類 (473)", "原來如此事務所・第一季 (100)", "原來如此事務所・第二季 (92)", "原來如此事務所・第三季 (100)", "品牌故事 (100)", "AI 名詞 (81)"]);
    fireEvent.click(screen.getByText(copy.details));
    expect(screen.getByText("Source-bound narrative premise")).toBeTruthy();
    expect(screen.getByText(copy.historical)).toBeTruthy();
    expect(calls().every(([, options]) => !options?.method || options.method === "GET")).toBe(true);
  });

  it("persists catalog, search and pagination in the URL and resets the page when narrowing", async () => {
    vi.mocked(api).mockImplementation(async (path) => {
      const params = new URL(path, "http://test.invalid").searchParams;
      const searched = Boolean(params.get("q"));
      return page([plan({ catalog: "season3", id: "B51", stage: "CHECKED_CANDIDATE_REQUIRES_OUTLINE", source_status: "checked" })], {
        total: searched ? 1 : 100, page: Number(params.get("page")),
      });
    });
    window.history.replaceState(null, "", "/zh-TW/admin/videos?tab=plans&keep=yes");
    const view = render(<AdminVideoPlans />);
    await screen.findByText("五類共 473 筆企劃");
    fireEvent.change(screen.getByRole("combobox", { name: copy.catalog }), { target: { value: "season3" } });
    await waitFor(() => expect(calls().at(-1)?.[0]).toContain("catalog=season3"));
    expect(await screen.findByText(copy.stages.CHECKED_CANDIDATE_REQUIRES_OUTLINE)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: copy.next }));
    await screen.findByText("第 2 頁，共 4 頁");
    expect(window.location.search).toContain("plan_page=2");
    fireEvent.change(screen.getByRole("searchbox", { name: copy.search }), { target: { value: "B51" } });
    fireEvent.click(screen.getByRole("button", { name: copy.searchButton }));
    await screen.findByText("符合條件的企劃：1 筆");
    const params = new URLSearchParams(window.location.search);
    expect(params.get("plan_q")).toBe("B51");
    expect(params.has("plan_page")).toBe(false);
    expect(params.get("tab")).toBe("plans");
    expect(params.get("keep")).toBe("yes");
    view.unmount();
    render(<AdminVideoPlans />);
    await screen.findByText("符合條件的企劃：1 筆");
    expect((screen.getByRole("searchbox", { name: copy.search }) as HTMLInputElement).value).toBe("B51");
    fireEvent.click(screen.getByRole("button", { name: copy.clear }));
    await waitFor(() => expect(new URLSearchParams(window.location.search).has("plan_catalog")).toBe(false));
    expect((screen.getByRole("searchbox", { name: copy.search }) as HTMLInputElement).value).toBe("");
    expect(calls().every(([, options]) => !options?.method || options.method === "GET")).toBe(true);
  });

  it("retains covered references and the longer brand target without making them production status", async () => {
    vi.mocked(api).mockResolvedValue(page([
      plan({ catalog: "ai-terms", id: "ai-agent", title: "AI Agent", stage: "COVERED_DO_NOT_REMAKE", source_status: "covered" }),
      plan({ catalog: "brand-stories", id: "B28", title: "Brand narrative", stage: "REVIEWED_STORY_PLAN_NOT_MEDIA", source_status: "reviewed-plan", target_duration_seconds: 780 }),
    ], { total: 2 }));
    render(<AdminVideoPlans />);
    const reference = await screen.findByText(copy.stages.COVERED_DO_NOT_REMAKE);
    expect(within(reference.closest("article")!).queryByText("製作目標：10 分鐘")).toBeNull();
    expect(screen.getByText("製作目標：13 分鐘")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Brand narrative" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "AI Agent" })).toBeTruthy();
  });

  it("discards unsent search text when history returns to an earlier query", async () => {
    vi.mocked(api).mockResolvedValue(page());
    render(<AdminVideoPlans />);
    await screen.findByText("五類共 473 筆企劃");
    const input = screen.getByRole("searchbox", { name: copy.search });
    fireEvent.change(input, { target: { value: "B28" } });
    fireEvent.click(screen.getByRole("button", { name: copy.searchButton }));
    fireEvent.change(screen.getByRole("searchbox", { name: copy.search }), { target: { value: "unsent draft" } });
    act(() => {
      window.history.replaceState(null, "", "/?tab=plans");
      window.dispatchEvent(new PopStateEvent("popstate"));
    });
    expect((screen.getByRole("searchbox", { name: copy.search }) as HTMLInputElement).value).toBe("");
  });

  it("retries failed reads and ignores a response for a filter that has been left", async () => {
    let resolveOld: (value: VideoPlanPage) => void = () => {};
    vi.mocked(api).mockRejectedValueOnce(new Error("unavailable")).mockImplementationOnce(() => new Promise((resolve) => { resolveOld = resolve; })).mockResolvedValue(page([], { total: 0 }));
    render(<AdminVideoPlans />);
    await screen.findByText(copy.error);
    fireEvent.click(screen.getByRole("button", { name: copy.retry }));
    await waitFor(() => expect(calls()).toHaveLength(2));
    fireEvent.change(screen.getByRole("combobox", { name: copy.catalog }), { target: { value: "season1" } });
    await screen.findByText(copy.empty);
    await act(async () => { resolveOld(page()); });
    expect(screen.queryByRole("heading", { name: plan().title })).toBeNull();
    expect(calls()[1][1]?.signal?.aborted).toBe(true);
  });
});
