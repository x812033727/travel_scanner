import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { HubHero } from "./hub-hero";

const labels = { label: "搜尋關鍵字", placeholder: "輸入關鍵字", submit: "搜尋" };

describe("the hub hero", () => {
  it("names the section, scopes the search form to it, and lists the figures it knows", () => {
    render(
      <HubHero
        title="旅遊情報與攻略" intro="我們自己整理的旅遊情報與攻略" section="travel"
        action="/zh-TW/search/articles" stats={["146 篇文章", null, "12 個主題"]} labels={labels}
      />,
    );
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("旅遊情報與攻略");
    // The results page's own GET form: a query has a URL and works with JavaScript off.
    const form = screen.getByRole("search");
    expect(form.getAttribute("action")).toBe("/zh-TW/search/articles");
    expect(form.getAttribute("method")).toBe("get");
    expect(form.querySelector('input[name="section"]')?.getAttribute("value")).toBe("travel");
    expect(screen.getByRole("searchbox", { name: "搜尋關鍵字" })).toBeTruthy();
    // A figure the page could not learn is left out, not shown as zero.
    expect(screen.getByTestId("hub-stats").textContent).toBe("146 篇文章12 個主題");
  });

  it("draws no figures line at all when none is known", () => {
    render(<HubHero title="生活分享" intro="與旅行無關的分享" section="life" action="/zh-TW/search/articles" stats={[null, null]} labels={labels} />);
    expect(screen.queryByTestId("hub-stats")).toBeNull();
    expect(screen.getByRole("search").querySelector('input[name="section"]')?.getAttribute("value")).toBe("life");
  });
});
