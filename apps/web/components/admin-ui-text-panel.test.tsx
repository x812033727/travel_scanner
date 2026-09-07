import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { EditableNamespace } from "@/lib/ui-text";
import { AdminUiTextPanel } from "./admin-ui-text-panel";

const { routerPush, routerRefresh } = vi.hoisted(() => ({
  routerPush: vi.fn(),
  routerRefresh: vi.fn(),
}));

vi.mock("@/i18n/navigation", () => ({
  Link: ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  ),
  usePathname: () => "/admin/ui-text",
  useRouter: () => ({ push: routerPush, refresh: routerRefresh, replace: vi.fn() }),
}));

const defaults = {
  save: "儲存",
  greeting: "你好，{name}",
  days: "{count, plural, one {# day} other {# days}}",
  separator: ", ",
};

const referenceDefaults = { save: "Save", greeting: "Hello, {name}" };

const overrideEntry = {
  namespace: "common",
  key: "save",
  locale: "ja",
  value: "保存する",
  default_snapshot: "儲存",
  updated_at: "2026-09-07T01:00:00Z",
  updated_by_email: "admin@example.com",
};

const orphanEntry = {
  ...overrideEntry,
  key: "gone.key",
  value: "孤兒",
  updated_by_email: null,
};

function snapshot(entries: unknown[]) {
  return { locale: "ja", namespace: "common", version: "v1", entries };
}

function ok(body: unknown) {
  return new Response(JSON.stringify(body), { status: 200 });
}

function renderPanel(
  namespaces: { namespace: EditableNamespace; keyCount: number }[] = [
    { namespace: "common", keyCount: 4 },
  ],
) {
  return render(
    <AdminUiTextPanel
      namespace="common"
      locale="ja"
      referenceLocale="zh-TW"
      defaults={defaults}
      referenceDefaults={referenceDefaults}
      namespaces={namespaces}
    />,
  );
}

let fetchMock: ReturnType<typeof vi.fn>;

beforeEach(() => {
  fetchMock = vi.fn().mockResolvedValue(ok(snapshot([overrideEntry, orphanEntry])));
  vi.stubGlobal("fetch", fetchMock);
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  routerPush.mockReset();
  routerRefresh.mockReset();
});

describe("AdminUiTextPanel", () => {
  it("joins the bundled defaults with the stored overrides", async () => {
    renderPanel();

    const save = (await screen.findByRole("textbox", { name: "save" })) as HTMLTextAreaElement;
    expect(save.value).toBe("保存する");
    const greeting = screen.getByRole("textbox", { name: "greeting" }) as HTMLTextAreaElement;
    expect(greeting.value).toBe("");
    expect(greeting.placeholder).toBe("你好，{name}");
    // The filter pill carries the same word, so the badges are counted by their element.
    expect(screen.getAllByText("已覆寫", { selector: "span" })).toHaveLength(2);
    expect(screen.getByText("含複數規則", { selector: "span" })).toBeTruthy();
    expect(screen.getByText("孤兒覆寫", { selector: "span" })).toBeTruthy();
    expect(screen.getByText(/程式裡已經沒有這個鍵/)).toBeTruthy();
    // Formatted with the panel's own formatter: a literal string here would assert the
    // runner's timezone, which passes on UTC+8 and fails on CI's UTC.
    const when = new Intl.DateTimeFormat("zh-TW", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(overrideEntry.updated_at));
    expect(screen.getByText(`admin@example.com 於 ${when} 更新`)).toBeTruthy();
    // The reference locale is shown so an editor can see what the source language says.
    expect(screen.getByText(/Hello, \{name\}/)).toBeTruthy();
    expect(fetchMock.mock.calls[0][0]).toBe(
      "/api/travel/admin/ui-text?namespace=common&locale=ja",
    );
  });

  it("narrows the list by filter and by search", async () => {
    renderPanel();
    await screen.findByRole("textbox", { name: "save" });

    fireEvent.click(screen.getByRole("button", { name: /已覆寫/ }));
    expect(screen.queryByRole("textbox", { name: "greeting" })).toBeNull();
    expect(screen.getByRole("textbox", { name: "save" })).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: /孤兒覆寫/ }));
    expect(screen.queryByRole("textbox", { name: "save" })).toBeNull();
    expect(screen.getByRole("textbox", { name: "gone.key" })).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: /^全部/ }));
    fireEvent.change(screen.getByRole("searchbox", { name: "搜尋鍵名或文字" }), {
      target: { value: "greeting" },
    });
    expect(screen.getByRole("textbox", { name: "greeting" })).toBeTruthy();
    expect(screen.queryByRole("textbox", { name: "save" })).toBeNull();
  });

  it("blocks a save whose placeholders no longer match the default", async () => {
    renderPanel();
    const greeting = await screen.findByRole("textbox", { name: "greeting" });

    fireEvent.change(greeting, { target: { value: "こんにちは" } });
    expect(screen.getByText("參數必須與預設相同：name")).toBeTruthy();
    expect(
      (screen.getByRole("button", { name: "請先修正 1 筆錯誤" }) as HTMLButtonElement).disabled,
    ).toBe(true);

    fireEvent.change(greeting, { target: { value: "こんにちは、{name}" } });
    expect(screen.queryByText("參數必須與預設相同：name")).toBeNull();
    expect(screen.getByRole("button", { name: "儲存 1 筆變更" })).toBeTruthy();
  });

  it("blocks a plural override that lost a closing brace", async () => {
    renderPanel();
    const days = await screen.findByRole("textbox", { name: "days" });

    fireEvent.change(days, { target: { value: "{count, plural, one {# 日}" } });
    expect(screen.getByText("大括號沒有成對。")).toBeTruthy();
  });

  it("saves the dirty rows as one batch and reports the propagation delay", async () => {
    renderPanel();
    const greeting = await screen.findByRole("textbox", { name: "greeting" });
    fireEvent.change(greeting, { target: { value: "こんにちは、{name}" } });

    const saved = { ...overrideEntry, key: "greeting", value: "こんにちは、{name}" };
    fetchMock.mockResolvedValueOnce(ok(snapshot([overrideEntry, orphanEntry, saved])));
    fireEvent.click(screen.getByRole("button", { name: "儲存 1 筆變更" }));

    await screen.findByText("已儲存 1 筆變更，前台下一次載入即生效。");
    const [url, init] = fetchMock.mock.calls[1];
    expect(url).toBe("/api/travel/admin/ui-text/batch");
    expect(init?.method).toBe("POST");
    expect(JSON.parse(String(init?.body))).toEqual({
      locale: "ja",
      namespace: "common",
      entries: [{ key: "greeting", value: "こんにちは、{name}", default_value: "你好，{name}" }],
    });
    expect(routerRefresh).toHaveBeenCalled();
  });

  it("sends a null value to restore a default, orphans included", async () => {
    renderPanel();
    await screen.findByRole("textbox", { name: "save" });

    fireEvent.click(screen.getByRole("button", { name: "還原預設：save" }));
    fireEvent.click(screen.getByRole("button", { name: "還原預設：gone.key" }));
    expect(screen.getAllByText("儲存後還原預設")).toHaveLength(2);

    fetchMock.mockResolvedValueOnce(ok(snapshot([])));
    fireEvent.click(screen.getByRole("button", { name: "儲存 2 筆變更" }));

    await screen.findByText("已儲存 2 筆變更，前台下一次載入即生效。");
    expect(JSON.parse(String(fetchMock.mock.calls[1][1]?.body)).entries).toEqual([
      { key: "save", value: null, default_value: "儲存" },
      // An orphan has no default left, and the API skips validation when the value is null.
      { key: "gone.key", value: null, default_value: null },
    ]);
  });

  it("keeps unsaved text and reloads the truth when a save fails", async () => {
    renderPanel();
    const greeting = await screen.findByRole("textbox", { name: "greeting" });
    fireEvent.change(greeting, { target: { value: "こんにちは、{name}" } });

    fetchMock.mockResolvedValueOnce(
      new Response(JSON.stringify({ detail: "壞掉了", code: "ui_text_value_empty" }), {
        status: 422,
      }),
    );
    fetchMock.mockResolvedValueOnce(ok(snapshot([overrideEntry, orphanEntry])));
    fireEvent.click(screen.getByRole("button", { name: "儲存 1 筆變更" }));

    await screen.findByText(/有變更沒有儲存成功/);
    expect(
      (screen.getByRole("textbox", { name: "greeting" }) as HTMLTextAreaElement).value,
    ).toBe("こんにちは、{name}");
  });

  it("confirms before navigating away from unsaved work", async () => {
    renderPanel([
      { namespace: "common", keyCount: 4 },
      { namespace: "search", keyCount: 9 },
    ]);
    const greeting = await screen.findByRole("textbox", { name: "greeting" });
    fireEvent.change(greeting, { target: { value: "こんにちは、{name}" } });

    const confirm = vi.spyOn(window, "confirm").mockReturnValue(false);
    fireEvent.change(screen.getByLabelText("文案群組"), { target: { value: "search" } });
    expect(confirm).toHaveBeenCalledWith("還有 1 筆未儲存的變更，切換後會遺失。確定切換？");
    expect(routerPush).not.toHaveBeenCalled();

    confirm.mockReturnValue(true);
    fireEvent.change(screen.getByLabelText("文案群組"), { target: { value: "search" } });
    expect(routerPush).toHaveBeenCalledWith("/admin/ui-text?ns=search&locale=ja&ref=zh-TW");
  });

  it("tells an administrator without the role what to do, and offers no retry", async () => {
    fetchMock.mockReset();
    fetchMock.mockResolvedValue(
      new Response(JSON.stringify({ detail: "此功能僅限系統管理員使用", code: "admin_required" }), {
        status: 403,
      }),
    );
    renderPanel();

    await screen.findByText("此功能僅限系統管理員使用");
    expect(screen.getByText(/ADMIN_EMAILS/)).toBeTruthy();
    expect(screen.queryByRole("button", { name: "重新載入" })).toBeNull();
  });

  it("offers a retry when the API cannot be reached at all", async () => {
    fetchMock.mockReset();
    fetchMock.mockRejectedValueOnce(new TypeError("Failed to fetch"));
    renderPanel();

    const retry = await screen.findByRole("button", { name: "重新載入" });
    fetchMock.mockResolvedValueOnce(ok(snapshot([overrideEntry])));
    fireEvent.click(retry);
    expect(await screen.findByRole("textbox", { name: "save" })).toBeTruthy();
  });

  it("pages a long namespace fifty rows at a time", async () => {
    const many = Object.fromEntries(
      Array.from({ length: 60 }, (_, index) => [`key${index}`, `文字 ${index}`]),
    );
    fetchMock.mockResolvedValue(ok(snapshot([])));
    render(
      <AdminUiTextPanel
        namespace="common"
        locale="ja"
        referenceLocale="zh-TW"
        defaults={many}
        referenceDefaults={{}}
        namespaces={[{ namespace: "common", keyCount: 60 }]}
      />,
    );

    await screen.findByRole("textbox", { name: "key0" });
    expect(screen.getAllByRole("textbox")).toHaveLength(50);
    expect(screen.getByText("第 1 / 2 頁，共 60 則")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "下一頁" }));
    expect(screen.getAllByRole("textbox")).toHaveLength(10);
    expect(screen.getByRole("textbox", { name: "key59" })).toBeTruthy();
  });

  it("shows the key counts next to each namespace so a group can be judged before opening it", async () => {
    renderPanel([
      { namespace: "common", keyCount: 4 },
      { namespace: "trips", keyCount: 727 },
    ]);
    await screen.findByRole("textbox", { name: "save" });

    const select = screen.getByLabelText("文案群組");
    expect(within(select).getByRole("option", { name: /共用文字（common・4 則）/ })).toBeTruthy();
    expect(within(select).getByRole("option", { name: /旅程規劃（trips・727 則）/ })).toBeTruthy();
  });
});
