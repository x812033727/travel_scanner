import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
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
// `?article=` only accepts a UUID, so the fixture id has to be one.
const id = "00000000-0000-4000-8000-0000000000a1";
const summary = {
  id, slug: "narita-to-tokyo", kind: "howto", destination_id: "tokyo",
  destination_label: "東京", topics, valid_until: null, expired: false, featured: false,
  display_order: 100, is_active: true, status: "draft", version: 1, updated_at: "2026-09-01T00:00:00Z",
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
const facets = { status: [{ code: "published", count: 0 }, { code: "draft", count: 1 }, { code: "hidden", count: 0 }, { code: "expired", count: 0 }], kind: [{ code: "intel", count: 0 }, { code: "howto", count: 1 }] };

function route(path: string, init?: { method?: string; body?: string }) {
  if (path.startsWith("/admin/guides/topics")) return Promise.resolve({ topics });
  if (path.startsWith("/admin/guides?")) return Promise.resolve({ articles: [summary], total: 1, page: 1, pages: 1, facets });
  if (path.includes("/publish")) {
    return Promise.resolve({
      ...detail,
      locales: [{ ...detail.locales[0], version: 3, published_version: 3, published_at: "2026-09-11T00:00:00Z" }],
    });
  }
  if (path.includes("/hide")) return Promise.resolve({ ...summary, is_active: false, status: "hidden", version: 2 });
  if (init?.method === "PUT") return Promise.resolve({ ...detail, draft: JSON.parse(init.body!).document });
  return Promise.resolve(detail);
}

async function open() {
  window.history.replaceState(null, "", `/zh-TW/admin/guides?article=${id}&lang=zh-TW`);
  render(<AdminGuidesPanel />);
  await screen.findByDisplayValue("怎麼走");
}

beforeEach(() => {
  vi.clearAllMocks();
  window.history.replaceState(null, "", "/zh-TW/admin/guides");
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
    expect((screen.getByRole("button", { name: "隱藏文章" }) as HTMLButtonElement).disabled).toBe(true);
  });
});

describe("the workspace", () => {
  it("starts on the list and opens an article through the URL", async () => {
    render(<AdminGuidesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "怎麼走" }));
    await waitFor(() => expect(window.location.search).toContain(`article=${id}`));
    await screen.findByDisplayValue("怎麼走");
    expect(screen.getByRole("button", { name: "返回清單" })).toBeTruthy();
  });

  it("goes back to the list by dropping the article from the URL", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "返回清單" }));
    await waitFor(() => expect(window.location.search).not.toContain("article="));
    expect(await screen.findByRole("button", { name: "怎麼走" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "儲存草稿" })).toBeNull();
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

describe("hiding", () => {
  it("sends the article version with a reason and then blocks publishing", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "隱藏文章" }));
    const dialog = await screen.findByRole("dialog");
    expect((within(dialog).getByRole("button", { name: "確認隱藏" }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(within(dialog).getByLabelText("原因"), { target: { value: "票價已變" } });
    fireEvent.click(within(dialog).getByLabelText("我已閱讀並確認這次操作"));
    fireEvent.click(within(dialog).getByRole("button", { name: "確認隱藏" }));

    await waitFor(() => {
      const call = mocks.api.mock.calls.find(([path]) => String(path).startsWith(`/admin/guides/${id}/hide`));
      expect(call).toBeTruthy();
      expect(JSON.parse(call![1].body)).toEqual({ expected_version: 1, confirmed: true, reason: "票價已變" });
    });
    expect(await screen.findByRole("button", { name: "恢復上架" })).toBeTruthy();
    expect((screen.getByRole("button", { name: "發布" }) as HTMLButtonElement).disabled).toBe(true);
    expect(screen.getByText(/這篇文章已隱藏/)).toBeTruthy();
  });

  it("never sends visibility inside the classification form", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "儲存分類" }));
    await waitFor(() => {
      const call = mocks.api.mock.calls.find(([path, init]) => String(path).startsWith(`/admin/guides/${id}?`) && init?.method === "PUT");
      expect(call).toBeTruthy();
      expect(JSON.parse(call![1].body)).not.toHaveProperty("is_active");
    });
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
      return Promise.reject(new ApiError("missing", 404, "guide_locale_not_found"));
    });
    window.history.replaceState(null, "", `/zh-TW/admin/guides?article=${id}&lang=ja`);
    render(<AdminGuidesPanel />);
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

describe("rich blocks", () => {
  const savedDocument = () => {
    const call = mocks.api.mock.calls.find(([path, init]) => String(path).endsWith("/zh-TW/draft") && init?.method === "PUT");
    return call ? JSON.parse(call[1].body).document : null;
  };

  it("adds a table typed as text and previews it as a table", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "新增區塊 · 表格" }));
    const editor = screen.getByLabelText("第一行是表頭，欄位用 | 分隔，一行一列。");
    fireEvent.change(editor, { target: { value: "方式|時間\nSkyliner|41 分\n" } });
    // The raw text stays exactly as typed, trailing newline included, so the next row can be started.
    expect((editor as HTMLTextAreaElement).value).toBe("方式|時間\nSkyliner|41 分\n");

    fireEvent.click(screen.getByRole("button", { name: "預覽" }));
    const dialog = await screen.findByRole("dialog");
    expect(within(dialog).getAllByRole("columnheader").map((cell) => cell.textContent)).toEqual(["方式", "時間"]);
    expect(within(dialog).getAllByRole("cell").map((cell) => cell.textContent)).toEqual(["Skyliner", "41 分"]);
  });

  it("sends a hero and a partner block in the draft it saves", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "加入主圖" }));
    fireEvent.change(screen.getByLabelText("圖片路徑"), { target: { value: "/guides/narita-to-tokyo/hero.jpg" } });
    fireEvent.change(screen.getByLabelText("替代文字"), { target: { value: "Skyliner 停在月台" } });
    fireEvent.change(screen.getByLabelText("作者"), { target: { value: "Mokaair" } });
    fireEvent.change(screen.getByLabelText("授權"), { target: { value: "© Mokaair" } });

    fireEvent.click(screen.getByRole("button", { name: "新增區塊 · 合作連結" }));
    fireEvent.change(screen.getByLabelText("合作模組"), { target: { value: "transport" } });
    fireEvent.change(screen.getByLabelText("區塊標題（可留空）"), { target: { value: "先買車票" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存草稿" }));

    await waitFor(() => expect(savedDocument()).toBeTruthy());
    const saved = savedDocument();
    expect(saved.hero).toEqual({
      src: "/guides/narita-to-tokyo/hero.jpg", alt: "Skyliner 停在月台", width: 1600, height: 900,
      credit: { author: "Mokaair", license: "© Mokaair", source_url: null },
    });
    expect(saved.blocks.at(-1)).toEqual({ type: "offer", module: "transport", destination_id: null, heading: "先買車票" });
  });

  it("shows a partner block in the preview as a placeholder rather than fetching offers", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "新增區塊 · 合作連結" }));
    fireEvent.click(screen.getByRole("button", { name: "預覽" }));
    const dialog = await screen.findByRole("dialog");
    expect(within(dialog).getByRole("note").textContent).toContain("合作連結區塊（發布後才會顯示按鈕）");
    expect(mocks.api.mock.calls.some(([path]) => String(path).includes("/affiliates/"))).toBe(false);
  });

  it("drops the hero again from the draft when it is removed", async () => {
    await open();
    fireEvent.click(screen.getByRole("button", { name: "加入主圖" }));
    fireEvent.click(screen.getByRole("button", { name: "移除主圖" }));
    expect(screen.queryByLabelText("圖片路徑")).toBeNull();
    expect(screen.getByRole("button", { name: "加入主圖" })).toBeTruthy();
  });
});
