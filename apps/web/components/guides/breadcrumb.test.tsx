import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { Breadcrumb } from "./breadcrumb";

afterEach(cleanup);

describe("Breadcrumb", () => {
  it("shows the trail without the home crumb, links every step and leaves the current page as text", () => {
    render(
      <Breadcrumb
        label="頁面路徑"
        current="機器學習是什麼"
        trail={[
          { name: "首頁", path: "/" },
          { name: "生活分享", path: "/life" },
          { name: "AI", path: "/life/topics/ai" },
          { name: "AI 名詞解釋", path: "/life/topics/ai-terms" },
        ]}
      />,
    );
    const nav = screen.getByRole("navigation", { name: "頁面路徑" });
    expect(within(nav).queryByRole("link", { name: "首頁" })).toBeNull();
    expect(within(nav).getAllByRole("link").map((link) => [link.textContent, link.getAttribute("href")])).toEqual([
      ["生活分享", "/life"], ["AI", "/life/topics/ai"], ["AI 名詞解釋", "/life/topics/ai-terms"],
    ]);
    const current = within(nav).getByText("機器學習是什麼");
    expect(current.getAttribute("aria-current")).toBe("page");
    expect(current.tagName).toBe("LI");
  });
});
