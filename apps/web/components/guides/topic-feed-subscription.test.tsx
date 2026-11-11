import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TopicFeedSubscription } from "./topic-feed-subscription";
import { topicFeedCopy } from "@/lib/topic-feed";
import { locales } from "@/i18n/routing";

const href = "https://mokaair.com/zh-TW/life/topics/ai-news/feed.xml";
afterEach(() => vi.unstubAllGlobals());

describe("topic feed subscription", () => {
  it.each(locales)("offers an actual feed address and accurate copy in %s", (locale) => {
    const copy = topicFeedCopy(locale);
    const localized = href.replace("zh-TW", locale);
    render(<TopicFeedSubscription locale={locale} href={localized} />);
    fireEvent.click(screen.getByText(copy.title));
    expect(screen.getByRole("link", { name: copy.open }).getAttribute("href")).toBe(localized);
    expect((screen.getByRole("textbox", { name: copy.url }) as HTMLInputElement).value).toBe(localized);
    expect(screen.getByText(copy.help)).toBeTruthy();
    expect(screen.getByText(copy.limit.replace("{limit}", "30"))).toBeTruthy();
  });

  it("copies only on a reader action and announces success", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    vi.stubGlobal("navigator", { clipboard: { writeText } });
    const copy = topicFeedCopy("zh-TW");
    render(<TopicFeedSubscription locale="zh-TW" href={href} />);
    expect(writeText).not.toHaveBeenCalled();
    fireEvent.click(screen.getByText(copy.title));
    fireEvent.click(screen.getByRole("button", { name: copy.copy }));
    expect((await screen.findByRole("status")).textContent).toBe(copy.copied);
    expect(writeText).toHaveBeenCalledWith(href);
  });

  it.each(["missing", "denied"])("keeps a selectable address when clipboard is %s", async (failure) => {
    vi.stubGlobal("navigator", failure === "missing" ? {} : { clipboard: { writeText: vi.fn().mockRejectedValue(new Error("denied")) } });
    const copy = topicFeedCopy("zh-TW");
    render(<TopicFeedSubscription locale="zh-TW" href={href} />);
    fireEvent.click(screen.getByText(copy.title));
    fireEvent.click(screen.getByRole("button", { name: copy.copy }));
    expect((await screen.findByRole("status")).textContent).toBe(copy.copyFailed);
    const address = screen.getByRole("textbox", { name: copy.url }) as HTMLInputElement;
    expect(address.readOnly).toBe(true);
    fireEvent.focus(address);
    expect(address.selectionStart).toBe(0);
    expect(address.selectionEnd).toBe(href.length);
  });

  it("keeps all five catalog keys and interpolation parameters aligned", () => {
    const baseline = topicFeedCopy("en");
    for (const locale of locales) {
      const catalog = topicFeedCopy(locale);
      expect(Object.keys(catalog).sort()).toEqual(Object.keys(baseline).sort());
      for (const key of Object.keys(baseline) as (keyof typeof baseline)[]) {
        expect(catalog[key].match(/\{\w+\}/g) ?? []).toEqual(baseline[key].match(/\{\w+\}/g) ?? []);
      }
    }
  });
});
