import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { DiscoveryItem } from "@/lib/discovery";
import { getDiscoveryCopy } from "@/lib/discovery-copy";
import { DiscoveryCard, contentLanguageName } from "./card";

const mock = vi.hoisted(() => ({ locale: "zh-TW" }));
vi.mock("next-intl", () => ({ useLocale: () => mock.locale, useTranslations: () => (key: string) => key }));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams("destination=kyoto") }));
vi.mock("@/i18n/navigation", () => ({
  usePathname: () => "/explore",
  Link: ({ href, children, scroll, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string; scroll?: boolean }) => {
    void scroll; return <a href={href} {...props}>{children}</a>;
  },
}));
vi.mock("@/components/community/provider", () => ({ useCommunity: () => ({ flags: { enabled: false } }) }));
vi.mock("./saved-content-action", () => ({ SavedContentAction: () => <button>Save fixture</button> }));
vi.mock("@/components/travel-card-actions", () => ({ TravelPlanAction: () => <button>Plan fixture</button> }));

const item: DiscoveryItem = {
  id: "guide:22222222-2222-4222-8222-222222222222", kind: "article", title: "錦市場の朝", summary: "Existing public content",
  locale: "ja", href: "/explore?content=guide%3A22222222-2222-4222-8222-222222222222",
  destination: { id: "kyoto", name: "京都" }, source: { kind: "editorial", label: "City guide", url: null },
  published_at: null, updated_at: null, thumbnail_url: null,
};
// What the platform itself calls a language, so the assertions never carry a second table.
const cldr = (reader: string, content: string) => new Intl.DisplayNames(reader, { type: "language" }).of(content)!;
const sourceText = (reader: string) => `${getDiscoveryCopy(reader).sourceKinds.editorial} · City guide`;
/** The source line (source kind, publisher, date): the only place the badge may appear. */
const sourceLine = () => screen.getByText(/City guide/);
const badge = () => sourceLine().querySelector("span");

beforeEach(() => { mock.locale = "zh-TW"; });
afterEach(cleanup);

describe("content language badge", () => {
  it.each([["zh-TW", "zh-TW"], ["ja", "ja"], ["en", "en"], ["zh-TW", "zh-tw"], ["ko", " ko "]])("adds nothing when a %s reader opens %j content", (reader, locale) => {
    mock.locale = reader;
    render(<DiscoveryCard item={{ ...item, locale }} />);
    expect(sourceLine().textContent).toBe(sourceText(reader));
    expect(badge()).toBeNull();
    expect(screen.queryByText(cldr(reader, reader))).toBeNull();
  });
  it("names Japanese content 日文 for a zh-TW reader, at the end of the source line", () => {
    const { container } = render(<DiscoveryCard item={{ ...item, published_at: "2026-09-01T00:00:00Z" }} />);
    const name = within(sourceLine()).getByText("日文");
    const pill = name.parentElement!;
    expect(pill.textContent).toBe(`${getDiscoveryCopy("zh-TW").language}: 日文`); // screen readers hear what the label means
    expect(pill.parentElement).toBe(sourceLine());
    expect(sourceLine().lastElementChild).toBe(pill);
    expect(sourceLine().querySelector("time")?.nextElementSibling).toBe(pill);
    expect(container.querySelector("article p")?.textContent).toBe(`京都·${getDiscoveryCopy("zh-TW").kinds.article}`); // the topic line is untouched
    expect(screen.getAllByRole("link")).toHaveLength(1); // the badge is not a filter or a link
  });
  it("names Japanese content Japanese for an en reader", () => {
    mock.locale = "en";
    render(<DiscoveryCard item={item} />);
    expect(within(sourceLine()).getByText("Japanese")).toBeTruthy();
    expect(badge()?.textContent).toBe("Content language: Japanese");
  });
  it.each([
    ["zh-TW", "ko"], ["zh-CN", "ja"], ["en", "zh-TW"], ["ja", "zh-TW"], ["ko", "ja"],
    ["zh-TW", "zh-CN"], // the two Chinese locales are separate site locales, and the feed orders them apart too
  ])("lets CLDR name the language for a %s reader of %s content", (reader, locale) => {
    mock.locale = reader;
    render(<DiscoveryCard item={{ ...item, locale }} />);
    expect(within(sourceLine()).getByText(cldr(reader, locale))).toBeTruthy();
    expect(badge()?.textContent).toBe(`${getDiscoveryCopy(reader).language}: ${cldr(reader, locale)}`);
  });
  it.each(["", "   ", "xx", "und", "x", "not a locale!", undefined, null])("adds nothing and keeps rendering for a content locale of %j", (locale) => {
    render(<DiscoveryCard item={{ ...item, locale: locale as unknown as string }} />);
    expect(sourceLine().textContent).toBe(sourceText("zh-TW"));
    expect(badge()).toBeNull();
    expect(screen.getByRole("link", { name: item.title })).toBeTruthy();
  });
});

describe("contentLanguageName", () => {
  it("reads the tag case-insensitively and trimmed, and never throws", () => {
    expect(contentLanguageName("zh-TW", "JA")).toBe("日文");
    expect(contentLanguageName("zh-TW", " ja ")).toBe("日文");
    expect(contentLanguageName("zh-TW", "ZH-tw")).toBeNull();
    expect(contentLanguageName("not a locale!", "ja")).toBeNull();
    expect(contentLanguageName("zh-TW", "ja_JP")).toBeNull();
    expect(contentLanguageName("zh-TW", 7 as unknown as string)).toBeNull();
  });
  it("shares one formatter per reader locale and returns the same answer every time", () => {
    const first = contentLanguageName("en", "ko");
    expect(first).toBe("Korean");
    expect(contentLanguageName("en", "ko")).toBe(first);
  });
});
