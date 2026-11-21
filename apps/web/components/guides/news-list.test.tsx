import { render, screen, within } from "@testing-library/react";
import * as intl from "next-intl";
import { afterEach, describe, expect, it, vi } from "vitest";
import { locales } from "@/i18n/routing";
import type { GuideSummary } from "@/lib/guides";
import { NewsList } from "./news-list";

const story = (slug: string, title: string, news_date: string | null, published_at = "2026-09-16T05:00:00Z"): GuideSummary => ({
  slug, kind: "life", destination_id: null, destination_label: null, topics: [],
  title, description: `${title}的描述`, published_at, valid_until: null, news_date, featured: false,
});

describe("the news list", () => {
  afterEach(() => vi.restoreAllMocks());

  it.each(locales)("links channel, lead and compact rows to the %s article documents", (locale) => {
    vi.spyOn(intl, "useLocale").mockReturnValue(locale);
    const articles: GuideSummary[] = [
      story("story", "Story", "2026-11-18"),
      { ...story("report", "Report", "2026-11-17"), kind: "intel" },
      { ...story("explainer", "Explainer", null), kind: "howto" },
    ];
    const hrefs = () => screen.getAllByRole("link").map((link) => link.getAttribute("href"));
    const expected = [`/${locale}/life/story`, `/${locale}/guides/intel/report`, `/${locale}/guides/howto/explainer`];
    const { rerender } = render(<NewsList articles={articles} channelFront />);
    expect(hrefs()).toEqual(expected);
    rerender(<NewsList articles={articles} leadHeading="h3" />);
    expect(hrefs()).toEqual(expected);
  });

  it("draws one line per story: the day the news happened, then the title as a link, in the order given", () => {
    render(
      <NewsList
        articles={[
          story("ai-news-siri-20260914", "Siri AI 隨 iOS 27 推出", "2026-09-14"),
          story("ai-news-pace-20260912", "Amodei 呼籲放慢前沿 AI", "2026-09-12"),
        ]}
      />,
    );
    const rows = within(screen.getByTestId("news-list")).getAllByRole("listitem");
    expect(rows).toHaveLength(2);
    expect(rows.map((row) => row.querySelector("time")?.getAttribute("dateTime"))).toEqual(["2026-09-14", "2026-09-12"]);
    expect(rows[0].querySelector("time")?.textContent).toBe("2026-09-14");
    expect(within(rows[0]).getByRole("link", { name: "Siri AI 隨 iOS 27 推出" }).getAttribute("href")).toBe("/zh-TW/life/ai-news-siri-20260914");
  });

  it("shows the news day, never the publication time, and no description or position", () => {
    // Imported in one batch: both stories published in the same minute.
    render(<NewsList articles={[story("a", "甲", "2026-07-01", "2026-09-16T05:00:00Z")]} />);
    const list = screen.getByTestId("news-list");
    expect(list.textContent).toContain("2026-07-01");
    expect(list.textContent).not.toContain("2026-09-16");
    expect(list.textContent).not.toContain("甲的描述");
    expect(list.tagName).toBe("OL");
  });

  it("keeps an undated piece on its own line without a date", () => {
    render(<NewsList articles={[story("a", "甲", "2026-09-14"), story("sources", "資訊來源", null)]} />);
    const rows = within(screen.getByTestId("news-list")).getAllByRole("listitem");
    expect(rows[1].querySelector("time")).toBeNull();
    expect(within(rows[1]).getByRole("link", { name: "資訊來源" })).toBeTruthy();
  });

  it("draws nothing without a story", () => {
    const { container } = render(<NewsList articles={[]} />);
    expect(container.innerHTML).toBe("");
  });

  it("previews the first story and only shows artwork suitable for readers", () => {
    const first = story("first", "First story", "2026-11-18");
    const second = story("second", "Second story", "2026-11-17");
    const hero = { src: "/guides/first/hero.jpg", width: 640, height: 360, alt: "Editorial diagram", credit: null };
    const { rerender } = render(<NewsList articles={[{ ...first, hero }, second]} leadHeading="h3" />);
    const link = screen.getByRole("link", { name: first.title });
    expect(within(link).getByRole("heading", { level: 3 }).textContent).toBe(first.title);
    expect(within(link).getByText(first.description)).toBeTruthy();
    expect(link.querySelector("img")?.getAttribute("src")).toBe(hero.src);
    expect(screen.queryByText(second.description)).toBeNull();

    rerender(<NewsList articles={[{ ...first, hero: { ...hero, src: "/guides/news-assets/placeholder.jpg" } }]} leadHeading="h3" />);
    expect(screen.getByRole("link", { name: first.title }).querySelector("img")).toBeNull();
    rerender(<NewsList articles={[{ ...first, news_date: null }]} leadHeading="h3" />);
    expect(screen.queryByRole("heading")).toBeNull();
  });

  it("gives a photo-free channel a lead and two supporting headlines while keeping its full chronological wire", () => {
    const stories = [
      story("lead", "頭條", "2026-11-18"),
      story("second", "第二則", "2026-11-17"),
      story("third", "第三則", "2026-11-17"),
      story("fourth", "第四則", "2026-11-16"),
      story("sources", "資料來源", null),
    ];
    const { rerender } = render(<NewsList articles={stories} channelFront showDescription />);
    const list = within(screen.getByRole("list"));
    expect(list.getAllByRole("heading").map((heading) => [heading.tagName, heading.textContent])).toEqual([
      ["H2", "頭條"], ["H3", "第二則"], ["H3", "第三則"],
    ]);
    expect(list.getAllByRole("link").map((link) => link.textContent)).toEqual(stories.map((item) => item.title));
    expect(list.queryByRole("img")).toBeNull();
    for (const item of stories) expect(list.getByText(item.description)).toBeTruthy();

    rerender(<NewsList articles={stories} channelFront />);
    expect(screen.queryByText(stories[3].description)).toBeNull();
    expect(screen.getByText(stories[1].description)).toBeTruthy();
  });

  it("uses each headline's own editorial image with its dimensions and suppresses synthetic covers", () => {
    const lead = story("lead", "Lead", "2026-11-18");
    const second = story("second", "Second", "2026-11-17");
    const third = story("third", "Third", "2026-11-16");
    const cover = { src: "/guides/lead/chart.jpg", alt: "Weekly price chart", width: 1600, height: 900, credit: null };
    const otherCover = { ...cover, src: "/guides/second/camera.png", alt: "Camera module", width: 1280, height: 720 };
    render(<NewsList channelFront articles={[
      { ...lead, hero: cover },
      { ...second, hero: otherCover },
      { ...third, hero: { ...cover, src: "/guides/news-assets/third-hero.webp" } },
    ]} />);
    const images = screen.getAllByRole("img");
    expect(images.map((image) => [image.getAttribute("src"), image.getAttribute("alt"),
      image.getAttribute("width"), image.getAttribute("height"), image.getAttribute("loading")])).toEqual([
      [cover.src, cover.alt, "1600", "900", "eager"],
      [otherCover.src, otherCover.alt, "1280", "720", "lazy"],
    ]);
    expect(screen.getAllByRole("link")).toHaveLength(3);
  });

  it("keeps undated rows intact and promotes only dated headlines for a mixed or older list", () => {
    const reference = story("sources", "資料來源", null);
    const later = story("story", "最新消息", "2026-11-18");
    const { rerender } = render(<NewsList articles={[reference, later]} channelFront />);
    expect(screen.getByRole("heading", { level: 2 }).textContent).toBe(later.title);
    expect(screen.getAllByRole("link").map((link) => link.textContent)).toEqual([reference.title, later.title]);
    rerender(<NewsList articles={[reference, { ...later, news_date: undefined }]} channelFront />);
    expect(screen.queryByRole("heading")).toBeNull();
    expect(screen.queryByText(reference.description)).toBeNull();
  });
});
