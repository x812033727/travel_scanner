import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeAll, afterAll, beforeEach, describe, expect, it, vi } from "vitest";
import { AdminGuidesList } from "@/components/admin-guides-list";
import { ApiError } from "@/lib/api";

const mocks = vi.hoisted(() => ({ api: vi.fn(), guard: vi.fn() }));
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: mocks.api };
});
vi.mock("@/components/admin-action-guard", () => ({ useAdminActionGuard: mocks.guard }));

const nativeShowModal = Object.getOwnPropertyDescriptor(HTMLDialogElement.prototype, "showModal");
const nativeClose = Object.getOwnPropertyDescriptor(HTMLDialogElement.prototype, "close");
beforeAll(() => {
  Object.defineProperty(HTMLDialogElement.prototype, "showModal", {
    configurable: true, value: function (this: HTMLDialogElement) { this.open = true; },
  });
  Object.defineProperty(HTMLDialogElement.prototype, "close", {
    configurable: true, value: function (this: HTMLDialogElement) { this.open = false; },
  });
});
afterAll(() => {
  for (const [name, descriptor] of [["showModal", nativeShowModal], ["close", nativeClose]] as const) {
    if (descriptor) Object.defineProperty(HTMLDialogElement.prototype, name, descriptor);
    else Reflect.deleteProperty(HTMLDialogElement.prototype, name);
  }
});

const topics = [{ slug: "transport", label: "交通" }];
const live = {
  id: "a1", slug: "narita-to-tokyo", kind: "howto", destination_id: "tokyo", destination_label: "東京",
  topics, valid_until: null, expired: false, featured: true, display_order: 100, is_active: true,
  status: "published", version: 3, updated_at: "2026-09-01T00:00:00Z",
  locales: [
    { locale: "zh-TW", version: 2, published_version: 2, published_at: "2026-09-01T00:00:00Z", title: "怎麼走", updated_at: "2026-09-01T00:00:00Z" },
    { locale: "ja", version: 1, published_version: null, published_at: null, title: "行き方", updated_at: "2026-09-01T00:00:00Z" },
  ],
};
const hidden = {
  ...live, id: "a2", slug: "jr-pass", kind: "intel", is_active: false, status: "hidden", version: 5, featured: false,
  locales: [{ locale: "zh-TW", version: 1, published_version: 1, published_at: "2026-09-01T00:00:00Z", title: "JR Pass 漲價", updated_at: "2026-09-01T00:00:00Z" }],
};
const facets = { status: [{ code: "published", count: 1 }, { code: "draft", count: 0 }, { code: "hidden", count: 1 }, { code: "expired", count: 0 }], kind: [{ code: "intel", count: 1 }, { code: "howto", count: 1 }] };

function listing(path: string) {
  const url = new URL(path, "http://admin.test");
  const status = url.searchParams.get("status");
  const articles = [live, hidden].filter((article) => !status || article.status === status);
  return { articles, total: articles.length, page: 1, pages: 1, facets };
}

function route(path: string, init?: { method?: string; body?: string }) {
  if (path.startsWith("/admin/guides/topics")) return Promise.resolve({ topics });
  if (path.startsWith("/admin/guides?")) return Promise.resolve(listing(path));
  if (path.startsWith("/admin/guides/batch")) return Promise.resolve({ updated: 2, skipped: 0, status: "hidden", articles: [] });
  if (init?.method === "POST") return Promise.resolve({ ...live, is_active: false, status: "hidden", version: 4 });
  return Promise.reject(new ApiError("unexpected", 500, "unexpected"));
}

async function confirmDialog(name: string, reason = "內容有誤") {
  const dialog = await screen.findByRole("dialog");
  const confirm = within(dialog).getByRole("button", { name });
  expect((confirm as HTMLButtonElement).disabled).toBe(true);
  fireEvent.change(within(dialog).getByLabelText("原因"), { target: { value: reason } });
  expect((within(dialog).getByRole("button", { name }) as HTMLButtonElement).disabled).toBe(true);
  fireEvent.click(within(dialog).getByLabelText("我已閱讀並確認這次操作"));
  fireEvent.click(within(dialog).getByRole("button", { name }));
}

beforeEach(() => {
  vi.clearAllMocks();
  window.history.replaceState(null, "", "/zh-TW/admin/guides");
  mocks.guard.mockReturnValue({ allowed: true });
  mocks.api.mockImplementation(route);
});

describe("the list", () => {
  it("shows one status per article and one badge per language", async () => {
    render(<AdminGuidesList onOpen={vi.fn()} onCreate={vi.fn()} />);
    const rows = await screen.findAllByRole("row");
    const first = rows[1];
    expect(within(first).getByRole("button", { name: "怎麼走" })).toBeTruthy();
    expect(within(first).getByText("已發布", { selector: "span" })).toBeTruthy();
    expect(within(first).getByText(/zh-TW · 已發布/)).toBeTruthy();
    expect(within(first).getByText(/ja · 草稿/)).toBeTruthy();
    expect(within(first).getByText(/en · 未建立/)).toBeTruthy();
    expect(within(rows[2]).getByText("已隱藏", { selector: "span" })).toBeTruthy();
    expect(within(rows[2]).getByRole("button", { name: "恢復上架" })).toBeTruthy();
  });

  it("filters by status through the URL and asks the API again", async () => {
    render(<AdminGuidesList onOpen={vi.fn()} onCreate={vi.fn()} />);
    await screen.findAllByRole("row");
    fireEvent.click(screen.getByRole("button", { name: /已隱藏/ }));
    await waitFor(() => expect(window.location.search).toContain("status=hidden"));
    await waitFor(() => {
      const calls = mocks.api.mock.calls.map(([path]) => String(path));
      expect(calls.some((path) => path.startsWith("/admin/guides?") && path.includes("status=hidden"))).toBe(true);
    });
    await waitFor(() => expect(screen.queryByRole("button", { name: "怎麼走" })).toBeNull());
  });

  it("opens an article through the caller, never by itself", async () => {
    const onOpen = vi.fn();
    render(<AdminGuidesList onOpen={onOpen} onCreate={vi.fn()} />);
    fireEvent.click(await screen.findByRole("button", { name: "怎麼走" }));
    expect(onOpen).toHaveBeenCalledWith("a1");
  });
});

describe("hiding", () => {
  it("needs a reason and an explicit tick, then sends the article version", async () => {
    render(<AdminGuidesList onOpen={vi.fn()} onCreate={vi.fn()} />);
    const rows = await screen.findAllByRole("row");
    fireEvent.click(within(rows[1]).getByRole("button", { name: "隱藏文章" }));
    await confirmDialog("確認隱藏");
    await waitFor(() => {
      const call = mocks.api.mock.calls.find(([path]) => String(path).startsWith("/admin/guides/a1/hide"));
      expect(call).toBeTruthy();
      expect(JSON.parse(call![1].body)).toEqual({ expected_version: 3, confirmed: true, reason: "內容有誤" });
    });
    expect((await screen.findByRole("status")).textContent).toContain("已隱藏");
  });

  it("sends every selected row with its own version to the batch endpoint", async () => {
    render(<AdminGuidesList onOpen={vi.fn()} onCreate={vi.fn()} />);
    await screen.findAllByRole("row");
    fireEvent.click(screen.getByLabelText("全選這一頁"));
    fireEvent.click(screen.getByRole("button", { name: /隱藏所選/ }));
    await confirmDialog("確認隱藏", "季節結束");
    await waitFor(() => {
      const call = mocks.api.mock.calls.find(([path]) => String(path).startsWith("/admin/guides/batch"));
      expect(call).toBeTruthy();
      expect(JSON.parse(call![1].body)).toEqual({
        items: [{ id: "a1", expected_version: 3 }, { id: "a2", expected_version: 5 }],
        action: "hide", confirmed: true, reason: "季節結束",
      });
    });
  });

  it("tells the editor to reload on a version conflict", async () => {
    render(<AdminGuidesList onOpen={vi.fn()} onCreate={vi.fn()} />);
    const rows = await screen.findAllByRole("row");
    mocks.api.mockRejectedValueOnce(new ApiError("conflict", 409, "guide_version_conflict"));
    fireEvent.click(within(rows[1]).getByRole("button", { name: "隱藏文章" }));
    await confirmDialog("確認隱藏");
    expect((await screen.findByRole("alert")).textContent).toContain("請重新載入");
  });

  it("keeps a read-only administrator from hiding anything", async () => {
    mocks.guard.mockReturnValue({ allowed: false });
    render(<AdminGuidesList onOpen={vi.fn()} onCreate={vi.fn()} />);
    const rows = await screen.findAllByRole("row");
    expect((within(rows[1]).getByRole("button", { name: "隱藏文章" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: /隱藏所選/ }) as HTMLButtonElement).disabled).toBe(true);
  });
});
