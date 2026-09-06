import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "@/lib/api";
import en from "../messages/en/alerts.json";
import ja from "../messages/ja/alerts.json";
import ko from "../messages/ko/alerts.json";
import zhCN from "../messages/zh-CN/alerts.json";
import zhTW from "../messages/zh-TW/alerts.json";
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

  // The bot answers only three exact Traditional Chinese phrases, listed in
  // apps/api/app/line/router.py. Translating the keyword would tell a Japanese or Korean
  // reader to send a word the bot ignores, and they would have no way to tell that apart from
  // the account simply not linking. Both sentences that carry it must therefore take it as a
  // parameter rather than spell it out.
  it.each([
    ["en", en],
    ["ja", ja],
    ["ko", ko],
    ["zh-CN", zhCN],
    ["zh-TW", zhTW],
  ])("keeps the LINE keyword a parameter in %s", (_locale, catalog) => {
    for (const sentence of [catalog.line.keywordHint, catalog.line.blocked]) {
      expect(sentence).toContain("{keyword}");
      expect(sentence).not.toContain("綁定");
    }
  });
});
