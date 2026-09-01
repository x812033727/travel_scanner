import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { usageOperations } from "@/lib/usage-catalog";
import { AdminUsageSettingsPanel } from "./admin-usage-settings-panel";

const packageItem = {
  id: "c9c56ba1-dd4a-40a3-9e64-f3c0ec936ecb",
  code: "PACK_30",
  localized_names: {
    "zh-TW": "常用包", "zh-CN": "常用包", en: "Standard pack", ja: "スタンダードパック", ko: "스탠다드 팩",
  },
  uses: 30,
  price_twd: 499,
  display_order: 20,
  is_active: true,
  is_featured: true,
};

const snapshot = {
  trial_uses: 3,
  packages: [packageItem],
  operation_costs: usageOperations.map((operation) => ({ operation, uses: 1, source: "database" })),
  audit: [],
};

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("AdminUsageSettingsPanel", () => {
  it("loads all four tabs and saves trial and operation costs", async () => {
    const trialUpdated = { ...snapshot, trial_uses: 8 };
    const costsUpdated = {
      ...trialUpdated,
      operation_costs: trialUpdated.operation_costs.map((item) => (
        item.operation === "flight_status_lookup" ? { ...item, uses: 0 } : item
      )),
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(trialUpdated), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(costsUpdated), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsageSettingsPanel />);

    expect((await screen.findByRole("tab", { name: "註冊體驗" })).getAttribute("aria-selected")).toBe("true");
    expect(screen.getAllByRole("tab")).toHaveLength(4);
    fireEvent.change(screen.getByLabelText("新會員贈送次數"), { target: { value: "8" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    expect(await screen.findByText("註冊體驗次數已更新。")).toBeTruthy();

    fireEvent.click(screen.getByRole("tab", { name: "功能扣次" }));
    expect(screen.getAllByRole("spinbutton")).toHaveLength(12);
    fireEvent.change(screen.getByLabelText("航班動態查詢"), { target: { value: "0" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存全部扣次" }));
    expect(await screen.findByText("功能扣次設定已更新。")).toBeTruthy();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(3));
    expect(JSON.parse(String(fetchMock.mock.calls[2][1]?.body)).costs.flight_status_lookup).toBe(0);
  });

  it("confirms before archiving a public package", async () => {
    const archived = {
      ...snapshot,
      packages: [{ ...packageItem, is_active: false, is_featured: false }],
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(archived), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(window, "confirm").mockReturnValue(true);
    render(<AdminUsageSettingsPanel />);

    fireEvent.click(await screen.findByRole("tab", { name: "公開方案" }));
    fireEvent.click(screen.getByRole("button", { name: "封存 常用包" }));
    expect(await screen.findByText("方案已封存。")).toBeTruthy();
    expect(window.confirm).toHaveBeenCalledWith(expect.stringContaining("常用包"));
    expect(JSON.parse(String(fetchMock.mock.calls[1][1]?.body))).toMatchObject({
      is_active: false,
      is_featured: false,
    });
  });

  it("creates and edits a five-locale featured package without exposing code editing", async () => {
    const custom = {
      ...packageItem,
      id: "a063010c-f498-4c48-b24f-9682a3a1fc18",
      code: "PACK_IMMUTABLE",
      localized_names: {
        "zh-TW": "自訂包", "zh-CN": "自定义包", en: "Custom pack", ja: "カスタムパック", ko: "맞춤 팩",
      },
      uses: 55,
      price_twd: 880,
      display_order: 8,
    };
    const created = { ...snapshot, packages: [{ ...packageItem, is_featured: false }, custom] };
    const edited = {
      ...created,
      packages: created.packages.map((item) => item.id === custom.id
        ? { ...item, localized_names: { ...item.localized_names, "zh-TW": "更新包" } }
        : item),
    };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify(snapshot), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(created), { status: 201 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(edited), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminUsageSettingsPanel />);

    fireEvent.click(await screen.findByRole("tab", { name: "公開方案" }));
    fireEvent.click(screen.getByRole("button", { name: "新增方案" }));
    for (const [label, value] of [
      ["繁體中文名稱", "自訂包"], ["簡體中文名稱", "自定义包"],
      ["英文名稱", "Custom pack"], ["日文名稱", "カスタムパック"], ["韓文名稱", "맞춤 팩"],
    ]) fireEvent.change(screen.getByLabelText(label), { target: { value } });
    fireEvent.change(screen.getByLabelText("包含次數"), { target: { value: "55" } });
    fireEvent.change(screen.getByLabelText("價格（TWD）"), { target: { value: "880" } });
    fireEvent.change(screen.getByLabelText("顯示順序"), { target: { value: "8" } });
    fireEvent.click(screen.getByLabelText("推薦方案"));
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const createRequest = JSON.parse(String(fetchMock.mock.calls[1][1]?.body));
    expect(createRequest).toMatchObject({ uses: 55, price_twd: 880, is_featured: true });
    expect(createRequest.localized_names).toEqual(custom.localized_names);
    expect(createRequest.code).toBeUndefined();

    fireEvent.click(screen.getByRole("button", { name: "編輯 自訂包" }));
    fireEvent.change(screen.getByLabelText("繁體中文名稱"), { target: { value: "更新包" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存設定" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(3));
    expect(fetchMock.mock.calls[2][0]).toContain(`/packages/${custom.id}`);
    expect(JSON.parse(String(fetchMock.mock.calls[2][1]?.body)).localized_names["zh-TW"]).toBe("更新包");
  });
});
