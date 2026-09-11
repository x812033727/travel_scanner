import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterAll, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";
import { AdminGuidesPanel } from "@/components/admin-guides-panel";
import { ApiError } from "@/lib/api";

const mocks = vi.hoisted(() => ({ api: vi.fn(), guard: vi.fn() }));
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: mocks.api };
});
vi.mock("@/components/admin-action-guard", () => ({
  useAdminActionGuard: mocks.guard,
  AdminReadOnlyNotice: ({ capability }: { capability: string }) =>
    mocks.guard().allowed ? null : <p role="note">{capability}</p>,
}));
vi.mock("@/lib/navigation-guard", () => ({ useNavigationGuard: vi.fn() }));

// jsdom has no native top-layer, and the shared Dialog opens through showModal. This
// establishes the component contract only; browser top-layer behaviour is covered by the
// Playwright suites.
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
const summary = {
  id: "a1", slug: "narita-to-tokyo", kind: "howto", destination_id: "tokyo",
  destination_label: "東京", topics, valid_until: null, expired: false, featured: false,
  display_order: 100, is_active: true, version: 1, updated_at: "2026-09-01T00:00:00Z",
  locales: [{
    locale: "zh-TW", version: 2, published_version: null, published_at: null,
    title: "怎麼走", updated_at: "2026-09-01T00:00:00Z",
  }],
};
const detail = {
  ...summary, locale: "zh-TW",
  draft: { title: "怎麼走", description: "三種選擇", blocks: [{ type: "paragraph", text: "Skyliner。" }], sources: [] },
  published: null,
  revisions: [{ id: "r1", version: 1, action: "created", created_at: "2026-09-01T00:00:00Z" }],
};

function route(path: string, init?: { method?: string; body?: string }) {
  if (path.startsWith("/admin/guides/topics")) return Promise.resolve({ topics });
  if (path.startsWith("/admin/guides?")) return Promise.resolve({ articles: [summary] });
  if (path.includes("/publish")) {
    return Promise.resolve({
      ...detail,
      locales: [{ ...detail.locales[0], version: 3, published_version: 3, published_at: "2026-09-11T00:00:00Z" }],
    });
  }
  if (init?.method === "PUT") return Promise.resolve({ ...detail, draft: JSON.parse(init.body!).document });
  return Promise.resolve(detail);
}

async function open() {
  render(<AdminGuidesPanel />);
  await screen.findByRole("option", { name: /narita-to-tokyo/ });
  fireEvent.change(screen.getByLabelText("文章列表"), { target: { value: "a1" } });
  await screen.findByDisplayValue("怎麼走");
}

beforeEach(() => {
  vi.clearAllMocks();
  mocks.guard.mockReturnValue({ allowed: true });
  mocks.api.mockImplementation(route);
});

describe("permissions", () => {
  it("asks for content.manage, not the settings capability", async () => {
    render(<AdminGuidesPanel />);
    await waitFor(() => expect(mocks.guard).toHaveBeenCalledWith("content.manage"));
  });

  it("leaves a read-only administrator unable to write", async () => {
    mocks.guard.mockReturnValue({ allowed: false });
    await open();
    expect((screen.getByRole("button", { name: "儲存草稿" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "建立新文章" }) as HTMLButtonElement).disabled).toBe(true);
  });
});

describe("publishing", () => {
  it("refuses to publish until a reason is given and the box is ticked", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "發布" }));
    const confirm = await screen.findByRole("button", { name: "確認發布" });
    expect((confirm as HTMLButtonElement).disabled).toBe(true);

    fireEvent.change(screen.getByLabelText("原因"), { target: { value: "內容已查證" } });
    expect((screen.getByRole("button", { name: "確認發布" }) as HTMLButtonElement).disabled).toBe(true);

    fireEvent.click(screen.getByLabelText("我已閱讀並確認這次操作"));
    expect((screen.getByRole("button", { name: "確認發布" }) as HTMLButtonElement).disabled).toBe(false);
  });

  it("sends the version it last read, so a stale tab cannot overwrite", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "發布" }));
    await screen.findByRole("button", { name: "確認發布" });
    fireEvent.change(screen.getByLabelText("原因"), { target: { value: "內容已查證" } });
    fireEvent.click(screen.getByLabelText("我已閱讀並確認這次操作"));
    fireEvent.click(screen.getByRole("button", { name: "確認發布" }));

    await waitFor(() => {
      const call = mocks.api.mock.calls.find(([path]) => String(path).includes("/publish"));
      expect(call).toBeTruthy();
      expect(JSON.parse(call![1].body)).toEqual({ expected_version: 2, confirmed: true, reason: "內容已查證" });
    });
  });

  it("offers withdrawal only once a locale is actually published", async () => {
    await open();
    expect(screen.queryByRole("button", { name: "撤下" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "發布" }));
    await screen.findByRole("button", { name: "確認發布" });
    fireEvent.change(screen.getByLabelText("原因"), { target: { value: "內容已查證" } });
    fireEvent.click(screen.getByLabelText("我已閱讀並確認這次操作"));
    fireEvent.click(screen.getByRole("button", { name: "確認發布" }));
    expect(await screen.findByRole("button", { name: "撤下" })).toBeTruthy();
  });
});

describe("conflicts", () => {
  it("tells the editor to reload rather than showing a raw error code", async () => {
    await open();
    mocks.api.mockRejectedValueOnce(new ApiError("conflict", 409, "guide_version_conflict"));
    fireEvent.change(screen.getByLabelText("標題"), { target: { value: "改過的標題" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存草稿" }));
    expect((await screen.findByRole("alert")).textContent).toContain("這篇文章已被更新，請重新載入後再操作。");
  });
});

describe("a language nobody has started", () => {
  it("offers to start it instead of reporting a failure", async () => {
    mocks.api.mockImplementation((path: string) => {
      if (path.startsWith("/admin/guides/topics")) return Promise.resolve({ topics });
      if (path.startsWith("/admin/guides?")) return Promise.resolve({ articles: [summary] });
      return Promise.reject(new ApiError("missing", 404, "guide_locale_not_found"));
    });
    render(<AdminGuidesPanel />);
    await screen.findByRole("option", { name: /narita-to-tokyo/ });
    fireEvent.change(screen.getByLabelText("文章列表"), { target: { value: "a1" } });
    expect(await screen.findByRole("button", { name: "新增這個語言的草稿" })).toBeTruthy();
    expect(screen.queryByRole("alert")).toBeNull();
  });
});

describe("preview", () => {
  it("draws the draft through the reader's renderer", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "預覽" }));
    const dialog = await screen.findByRole("dialog");
    expect(dialog.textContent).toContain("Skyliner。");
    expect(dialog.textContent).toContain("三種選擇");
  });
});
