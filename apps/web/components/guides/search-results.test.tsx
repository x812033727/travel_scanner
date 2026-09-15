import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { Highlighted, SearchResultCard, SearchResults } from "./search-results";

const labels = { intel: "情報", howto: "攻略", life: "生活分享" };
const hit = {
  slug: "jr-pass", kind: "howto" as const, destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }, { slug: "budget", label: "預算" }, { slug: "extra", label: "多的" }],
  title: "JR Pass 值得買嗎", description: "算給你看。",
  hero: { src: "/guides/jr-pass/hero.jpg", alt: "月台", width: 1600, height: 900, credit: null },
  published_at: "2026-09-01T00:00:00Z", valid_until: null, featured: false,
  snippet: "…東京到大阪來回就回本，JR PASS 七日券…", matched: ["jr pass"],
};

afterEach(cleanup);

describe("Highlighted", () => {
  it("marks each run that matches, case and width aside, and nothing else", () => {
    render(<p><Highlighted text="ＪＲ Pass 與 jr pass" terms={["jr pass"]} /></p>);
    const marks = screen.getAllByText(/pass/i, { selector: "mark" });
    expect(marks.map((mark) => mark.textContent)).toEqual(["ＪＲ Pass", "jr pass"]);
  });

  it("renders text with no match untouched", () => {
    render(<p><Highlighted text="沒有命中" terms={["jr"]} /></p>);
    expect(screen.queryByText(/./, { selector: "mark" })).toBeNull();
    expect(screen.getByText("沒有命中")).toBeTruthy();
  });
});

describe("SearchResultCard", () => {
  it("links the article, marks the terms in the title and the passage, and keeps the card scannable", () => {
    render(<ol><SearchResultCard hit={hit} labels={labels} /></ol>);
    expect(screen.getByRole("link", { name: "JR Pass 值得買嗎" }).getAttribute("href")).toBe("/guides/howto/jr-pass");
    expect(screen.getAllByText("JR Pass", { selector: "mark" })).toHaveLength(1);
    expect(screen.getAllByText("JR PASS", { selector: "mark" })).toHaveLength(1);
    expect(screen.getByText("攻略")).toBeTruthy();
    expect(screen.getByText("東京")).toBeTruthy();
    // Two topics at most: the card is a result, not the article's taxonomy.
    expect(screen.queryByText("多的")).toBeNull();
    // The hero is decorative here: the title next to it says what it is.
    expect(screen.getByRole("presentation", { hidden: true }).getAttribute("src")).toContain("/guides/jr-pass/hero.jpg");
  });

  it("falls back to the description when the API sent no passage", () => {
    render(<ol><SearchResultCard hit={{ ...hit, snippet: "" }} labels={labels} /></ol>);
    expect(screen.getByText("算給你看。")).toBeTruthy();
  });
});

describe("SearchResults", () => {
  it("is an ordered list, since the order is the ranking, and draws nothing for no hits", () => {
    const { container } = render(<SearchResults hits={[hit, { ...hit, slug: "second", title: "第二篇" }]} labels={labels} />);
    expect(container.querySelector("ol")).toBeTruthy();
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
    cleanup();
    render(<SearchResults hits={[]} labels={labels} />);
    expect(screen.queryByRole("list")).toBeNull();
  });
});
