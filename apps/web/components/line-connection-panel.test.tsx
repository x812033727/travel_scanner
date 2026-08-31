import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "@/lib/api";
import { LineConnectionPanel } from "./line-connection-panel";

vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: vi.fn() };
});
const apiMock = vi.mocked(api);

describe("LineConnectionPanel", () => {
  beforeEach(() => apiMock.mockReset());

  it("shows the official account and binding instruction", async () => {
    apiMock.mockResolvedValueOnce({ configured: true, status: "unlinked", official_account_id: "@travel", add_friend_url: "https://line.me/R/ti/p/@travel" });
    render(<LineConnectionPanel />);
    expect(await screen.findByText(/官方帳號 @travel/)).toBeTruthy();
    expect(screen.getByRole("link", { name: "加入 LINE 好友" }).getAttribute("href")).toContain("@travel");
  });

  it("sends a test message for the linked account", async () => {
    apiMock.mockResolvedValueOnce({ configured: true, status: "linked", display_name: "小明", masked_user_id: "U12••••7890" });
    apiMock.mockResolvedValueOnce(undefined);
    render(<LineConnectionPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "傳送測試" }));
    await screen.findByText("測試訊息已送到 LINE。");
    await waitFor(() => expect(apiMock).toHaveBeenCalledWith("/line/test-message", { method: "POST" }));
  });
});
