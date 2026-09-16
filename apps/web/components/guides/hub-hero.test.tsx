import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { HubHero } from "./hub-hero";

const labels = { label: "搜尋關鍵字", placeholder: "輸入關鍵字", submit: "搜尋" };

describe("the hub hero", () => {
  it("names the section and scopes the search form to it", () => {
    render(
      <HubHero
        title="旅遊情報與攻略" intro="我們自己整理的旅遊情報與攻略" section="travel"
        action="/zh-TW/search/articles" labels={labels}
      />,
    );
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("旅遊情報與攻略");
    // The results page's own GET form: a query has a URL and works with JavaScript off.
    const form = screen.getByRole("search");
    expect(form.getAttribute("action")).toBe("/zh-TW/search/articles");
    expect(form.getAttribute("method")).toBe("get");
    expect(form.querySelector('input[name="section"]')?.getAttribute("value")).toBe("travel");
    expect(screen.getByRole("searchbox", { name: "搜尋關鍵字" })).toBeTruthy();
  });

  it("says nothing about how big the section is", () => {
    render(
      <HubHero
        title="生活分享" intro="與旅行無關的分享" section="life"
        action="/zh-TW/search/articles" labels={labels}
      />,
    );
    // The section grows every week, so any figure here would be stale between deploys.
    expect(document.body.textContent).not.toMatch(/\d/);
    expect(screen.getByRole("search").querySelector('input[name="section"]')?.getAttribute("value")).toBe("life");
  });
});
