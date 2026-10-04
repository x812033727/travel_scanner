import { render, screen, within } from "@testing-library/react";
import type { ReactNode } from "react";
import { describe, expect, it, vi } from "vitest";
import { GuideArticle, type GuideArticleLabels } from "./article";
import { AD_CLEARANCE_BLOCKS, MIN_BLOCKS_BETWEEN, type AdsenseConfig } from "@/lib/adsense";
import { fixtureSeries } from "@/components/gemini-series/fixture.test-data";
import type { VisibleGeminiSeries } from "@/lib/gemini-series-projection";

vi.mock("@/components/ads/article-ad-slot", () => ({
  ArticleAdSlot: (props: { publisherId: string; slotId: string; label: string; cmpEnabled: boolean; lazy?: boolean }) => (
    <div data-testid="ad-slot" data-publisher={props.publisherId} data-slot={props.slotId} data-cmp={String(props.cmpEnabled)} data-lazy={String(Boolean(props.lazy))}>{props.label}</div>
  ),
}));

vi.mock("@/components/destination-affiliate-options", () => ({
  DestinationAffiliateOptions: (props: { destinationId: string; modules?: string[]; placement?: string; contextual?: boolean; destinationLabel?: string; article?: string }) => (
    <div
      data-testid="affiliate"
      data-destination={props.destinationId}
      data-modules={(props.modules ?? []).join(",")}
      data-placement={props.placement}
      data-contextual={String(Boolean(props.contextual))}
      data-label={props.destinationLabel ?? ""}
      data-article={props.article ?? ""}
    />
  ),
}));

const labels = {
  intel: "情報", howto: "攻略", life: "生活分享",
  updated: "更新", sources: "來源", checkedOn: "查核日", destination: "目的地",
  contents: "目錄", adLabel: "廣告", disclosure: "透過合作連結預訂，本站可能獲得分潤。",
  partnerDisclosure: "本文含合作連結，透過連結購買或訂閱，本站可能獲得分潤。",
  partner: { badge: "合作連結", newTab: "另開新分頁" },
  blocks: { imageCredit: "圖片：", tip: "小提醒", warning: "注意", info: "補充" },
};

const document = {
  title: "東京 eSIM 怎麼選",
  description: "三家方案比較",
  version: 1,
  published_at: "2026-09-10T00:00:00Z",
  blocks: [{ type: "paragraph" as const, text: "先看流量。" }],
  sources: [],
};

function draw(
  overrides: Record<string, unknown> = {},
  extra: { readingTime?: string; adsense?: AdsenseConfig; labels?: Partial<GuideArticleLabels>; geminiSeries?: VisibleGeminiSeries | null; related?: ReactNode } = {},
) {
  return render(
    <GuideArticle
      labels={{ ...labels, ...extra.labels }}
      readingTime={extra.readingTime}
      adsense={extra.adsense}
      geminiSeries={extra.geminiSeries}
      related={extra.related}
      state={{
        slug: "tokyo-esim", kind: "howto", locale: "zh-TW", status: "published",
        destination_id: "tokyo", destination_label: "東京",
        topics: [{ slug: "connectivity", label: "網路通訊" }], valid_until: null, expired: false,
        document, published_locales: ["zh-TW"],
        ...overrides,
      }}
    />,
  );
}

describe("GuideArticle Gemini navigation", () => {
  it("uses the existing Gemini navigation once in zh-TW and the API navigation in another locale", () => {
    const gemini = fixtureSeries();
    const first = gemini.articles[0];
    const series = {
      slug: "gemini",
      hub: { kind: "life" as const, slug: gemini.hubSlug, title: "API hub" },
      current: {
        kind: "life" as const, slug: first.slug, title: first.title,
        number: first.number, group: first.group, level: first.level,
        platforms: [...first.platforms], aliases: [], description: first.purpose,
        minutes: first.minutes,
      },
      previous: null, next: null, prerequisites: [], related: [],
    };
    const article = { slug: first.slug, kind: "life", destination_id: null, destination_label: null, series };
    const result = draw(article, { geminiSeries: gemini });
    expect(screen.queryByRole("link", { name: /API hub/ })).toBeNull();
    result.unmount();
    draw({ ...article, locale: "en" });
    expect(screen.getByRole("link", { name: /API hub/ })).toBeTruthy();
  });
});

describe("GuideArticle partner buttons", () => {
  it("ends a destination article with the modules its topics point at, labelled as the guide surface", () => {
    draw();
    const panel = screen.getByTestId("affiliate");
    expect(panel.getAttribute("data-destination")).toBe("tokyo");
    expect(panel.getAttribute("data-modules")).toBe("connectivity");
    expect(panel.getAttribute("data-placement")).toBe("guide");
    expect(panel.getAttribute("data-contextual")).toBe("true");
    // The click is attributed to this article, not just to the guide surface.
    expect(panel.getAttribute("data-article")).toBe("tokyo-esim");
  });

  it("folds Kyoto into the shared Osaka-Kyoto catalog destination", () => {
    draw({ destination_id: "kyoto", topics: [{ slug: "itinerary", label: "行程" }] });
    expect(screen.getByTestId("affiliate").getAttribute("data-destination")).toBe("osaka-kyoto");
    expect(screen.getByTestId("affiliate").getAttribute("data-modules")).toBe("activities");
  });

  it("shows nothing for a cross-destination article", () => {
    draw({ destination_id: null, destination_label: null });
    expect(screen.queryByTestId("affiliate")).toBeNull();
  });

  it("shows nothing when no topic has an honest module", () => {
    draw({ topics: [{ slug: "etiquette", label: "禮儀" }, { slug: "safety", label: "安全" }] });
    expect(screen.queryByTestId("affiliate")).toBeNull();
  });

  it("shows nothing on an expired notice, which says nothing about being expired", () => {
    draw({ kind: "intel", expired: true, valid_until: "2026-09-01", topics: [{ slug: "deal", label: "優惠" }] });
    expect(screen.queryByRole("status")).toBeNull();
    expect(screen.queryByTestId("affiliate")).toBeNull();
  });

  it("still renders the body and topics around the panel", () => {
    draw();
    expect(screen.getByText("先看流量。")).toBeTruthy();
    expect(screen.getByRole("link", { name: "網路通訊" })).toBeTruthy();
  });
});

describe("GuideArticle partner buttons placed by the editor", () => {
  const withOffer = {
    ...document,
    blocks: [
      { type: "heading" as const, level: 2 as const, text: "怎麼買票" },
      { type: "paragraph" as const, text: "先決定住哪一區。" },
      { type: "offer" as const, module: "transport" as const, destination_id: null, heading: "先買車票" },
      { type: "heading" as const, level: 2 as const, text: "怎麼搭" },
      { type: "paragraph" as const, text: "跟著指標走。" },
    ],
  };
  const topics = [{ slug: "transport", label: "交通" }, { slug: "itinerary", label: "行程" }];

  it("draws the button where the editor put it and leaves that module out of the end panel", () => {
    draw({ document: withOffer, topics });
    const panels = screen.getAllByTestId("affiliate");
    expect(panels).toHaveLength(2);
    expect(panels[0].getAttribute("data-modules")).toBe("transport");
    expect(panels[0].getAttribute("data-destination")).toBe("tokyo");
    expect(panels[0].getAttribute("data-label")).toBe("東京");
    expect(panels[1].getAttribute("data-modules")).toBe("activities");
    // Inline and end panel both attribute their clicks to the article.
    expect(panels.map((panel) => panel.getAttribute("data-article"))).toEqual(["tokyo-esim", "tokyo-esim"]);
    // The body around it is intact, and the editor's heading sits above the buttons.
    expect(screen.getByRole("heading", { level: 3, name: "先買車票" })).toBeTruthy();
    expect(screen.getByText("跟著指標走。")).toBeTruthy();
  });

  it("discloses before the first button, and only when the body carries one", () => {
    draw({ document: withOffer, topics });
    expect(screen.getByRole("note").textContent).toBe(labels.disclosure);
    draw({ topics });
    expect(screen.getAllByRole("note")).toHaveLength(1);
  });

  it("lets a cross-destination notice point a block at its own city", () => {
    const blocks = [
      { type: "paragraph" as const, text: "京都的見頃。" },
      { type: "offer" as const, module: "activities" as const, destination_id: "osaka-kyoto", heading: "" },
    ];
    draw({ document: { ...document, blocks }, destination_id: null, destination_label: null, topics: [{ slug: "season", label: "季節" }] });
    const panels = screen.getAllByTestId("affiliate");
    expect(panels).toHaveLength(1);
    expect(panels[0].getAttribute("data-destination")).toBe("osaka-kyoto");
    // Not the article's label: the block names a city the article as a whole is not about.
    expect(panels[0].getAttribute("data-label")).toBe("");
  });

  it("draws nothing for a block whose city is not in the catalog, and no end panel either", () => {
    const blocks = [{ type: "offer" as const, module: "activities" as const, destination_id: "atlantis", heading: "" }];
    draw({ document: { ...document, blocks }, destination_id: null, destination_label: null, topics: [{ slug: "season", label: "季節" }] });
    expect(screen.queryByTestId("affiliate")).toBeNull();
    expect(screen.queryByRole("note")).toBeNull();
  });

  it("drops every button, inline ones included, on an expired notice", () => {
    draw({ document: withOffer, topics, kind: "intel", expired: true, valid_until: "2026-09-01" });
    expect(screen.queryByTestId("affiliate")).toBeNull();
  });
});

describe("GuideArticle partner links placed by the editor", () => {
  const url = "https://www.hostinger.com/tw/vps-hosting?aff_id=12345";
  const resolved = { key: "0123456789abcdef", partner: "hostinger", display_name: "Hostinger", url };
  const withPartner = {
    ...document,
    blocks: [
      { type: "heading" as const, level: 2 as const, text: "選一台主機" },
      { type: "paragraph" as const, text: "年繳方案才划算。" },
      { type: "partner_link" as const, partner: "hostinger", url, label: "看 VPS 方案", note: "本站就架在這裡" },
      { type: "paragraph" as const, text: "接著部署。" },
    ],
  };
  const life = {
    kind: "life" as const, slug: "claude-code-vps", destination_id: null, destination_label: null,
    topics: [{ slug: "ai", label: "AI 工具" }],
  };

  it("draws the link where the editor put it, after a disclosure worded for buying, not booking", () => {
    draw({ ...life, document: withPartner, partner_links: [resolved] });
    const link = screen.getByRole("link", { name: /看 VPS 方案/ });
    expect(link.getAttribute("href")).toBe(url);
    expect(link.getAttribute("rel")).toContain("sponsored");
    const note = screen.getByRole("note");
    expect(note.textContent).toBe(labels.partnerDisclosure);
    // The disclosure precedes the first partner link in the document, not only visually.
    expect(note.compareDocumentPosition(link) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    // The paragraphs on either side are intact and in order around it.
    const before = screen.getByText("年繳方案才划算。");
    const after = screen.getByText("接著部署。");
    expect(before.compareDocumentPosition(link) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(link.compareDocumentPosition(after) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(within(link.closest("aside")!).getByText("本站就架在這裡")).toBeTruthy();
  });

  it("draws nothing, disclosure included, for a link the API did not resolve", () => {
    draw({ ...life, document: withPartner, partner_links: [] });
    expect(screen.queryByRole("link", { name: /看 VPS 方案/ })).toBeNull();
    expect(screen.queryByRole("note")).toBeNull();
    // Nor is its label or URL drawn some other way, as plain text or an ordinary link.
    expect(screen.queryByText("看 VPS 方案")).toBeNull();
    expect(screen.queryAllByRole("link").some((anchor) => anchor.getAttribute("href") === url)).toBe(false);
  });

  it("does not trust a resolved entry for a different URL than the block holds", () => {
    draw({ ...life, document: withPartner, partner_links: [{ ...resolved, url: "https://www.hostinger.com/tw" }] });
    expect(screen.queryByRole("link", { name: /看 VPS 方案/ })).toBeNull();
  });

  it("reads a state without partner links, from an older API, as having none", () => {
    draw({ ...life, document: withPartner });
    expect(screen.queryByRole("link", { name: /看 VPS 方案/ })).toBeNull();
  });

  it("drops the link under an expired notice", () => {
    draw({ ...life, document: withPartner, partner_links: [resolved], expired: true, valid_until: "2026-09-01" });
    expect(screen.queryByRole("link", { name: /看 VPS 方案/ })).toBeNull();
  });

  it("keeps the booking wording when the body carries only offer buttons", () => {
    const blocks = [...withPartner.blocks.slice(0, 2), { type: "offer" as const, module: "hotel" as const, destination_id: "tokyo", heading: "" }];
    draw({ ...life, document: { ...document, blocks }, partner_links: [resolved] });
    expect(screen.getByRole("note").textContent).toBe(labels.disclosure);
  });
});

describe("GuideArticle artwork, dates and contents", () => {
  const hero = {
    src: "/guides/tokyo-esim/hero.jpg", alt: "成田機場的 SIM 卡販賣機", width: 1600, height: 900,
    credit: { author: "Someone", license: "CC BY 4.0", source_url: "https://commons.wikimedia.org/wiki/File:Sim.jpg" },
  };

  it("opens with the hero, eagerly, and credits it", () => {
    draw({ document: { ...document, hero } });
    const image = screen.getByRole("img", { name: hero.alt });
    expect(image.getAttribute("src")).toBe(hero.src);
    expect(image.getAttribute("loading")).toBe("eager");
    expect(image.getAttribute("fetchpriority")).toBe("high");
    expect(screen.getByRole("link", { name: "Someone" }).getAttribute("href")).toBe(hero.credit.source_url);
  });

  it("dates nothing by itself: no first publication, and no date an expired notice applied until", () => {
    const fresh = draw();
    expect(screen.queryByText(/2026-09-10/)).toBeNull();
    expect(fresh.container.querySelector("time")).toBeNull();
    const expired = draw({ kind: "intel", expired: true, valid_until: "2026-09-01" });
    expect(screen.queryByText(/2026-09-01/)).toBeNull();
    expect(expired.container.querySelector("time")).toBeNull();
  });

  it("shows the update date only once the article was corrected after publication", () => {
    draw();
    expect(screen.queryByText("更新:")).toBeNull();
    draw({ document: { ...document, modified_at: "2026-09-10T08:00:00Z" } });
    expect(screen.queryByText(/更新:/)).toBeNull();
    draw({ document: { ...document, modified_at: "2026-09-12T08:00:00Z" } });
    expect(screen.getByText(/更新:/).textContent).toContain("2026-09-12");
  });

  it("shows the reading time the page worded", () => {
    draw({}, { readingTime: "閱讀時間約 4 分鐘" });
    expect(screen.getByText("閱讀時間約 4 分鐘")).toBeTruthy();
  });

  it("offers a table of contents once there are three sections, pointing at the renderer's ids", () => {
    const blocks = [
      { type: "heading" as const, level: 2 as const, text: "一" },
      { type: "paragraph" as const, text: "x" },
      { type: "heading" as const, level: 2 as const, text: "二" },
      { type: "heading" as const, level: 3 as const, text: "二之一" },
      { type: "heading" as const, level: 2 as const, text: "三" },
    ];
    draw({ document: { ...document, blocks } });
    const contents = screen.getByRole("navigation", { name: "目錄" });
    const links = contents.querySelectorAll("a");
    expect([...links].map((link) => link.getAttribute("href"))).toEqual(["#section-1", "#section-2", "#section-3"]);
    expect(screen.getAllByRole("heading", { level: 2 }).map((heading) => heading.id)).toEqual(["section-1", "section-2", "section-3"]);
  });

  it("skips the table of contents for a short article", () => {
    draw();
    expect(screen.queryByRole("navigation")).toBeNull();
  });
});

describe("GuideArticle in the lifestyle section", () => {
  const life = {
    kind: "life" as const,
    topics: [{ slug: "ai", label: "AI 工具" }],
  };

  it("offers every module under its own surface once the editor names a destination", () => {
    draw(life);
    const panel = screen.getByTestId("affiliate");
    expect(panel.getAttribute("data-destination")).toBe("tokyo");
    expect(panel.getAttribute("data-modules")).toBe("flight,hotel,activities,transport,connectivity");
    expect(panel.getAttribute("data-placement")).toBe("life");
    // Not "contextual": the heading must name the destination's partners rather than invite
    // the reader to keep exploring a place the article was never about.
    expect(panel.getAttribute("data-contextual")).toBe("false");
  });

  it("shows no partner buttons at all without a destination, which is the usual case", () => {
    draw({ ...life, destination_id: null, destination_label: null });
    expect(screen.queryByTestId("affiliate")).toBeNull();
  });

  it("labels the badge with its own section name", () => {
    draw(life);
    expect(screen.getByText("生活分享")).toBeTruthy();
  });

  it("links its topic chips at the lifestyle listing, not a /guides one", () => {
    draw(life);
    expect(screen.getByRole("link", { name: "AI 工具" }).getAttribute("href")).toBe("/life?topic=ai");
  });

  it("renders whatever the page handed it to read next", () => {
    render(
      <GuideArticle
        labels={labels}
        related={<p>最新旅遊情報攻略</p>}
        state={{
          slug: "ai-notes", kind: "life", locale: "zh-TW", status: "published",
          destination_id: null, destination_label: null,
          topics: [{ slug: "ai", label: "AI 工具" }], valid_until: null, expired: false,
          document, published_locales: ["zh-TW"],
        }}
      />,
    );
    expect(screen.getByText("最新旅遊情報攻略")).toBeTruthy();
  });
});

describe("GuideArticle advertising", () => {
  const enabled: AdsenseConfig = {
    enabled: true, publisher_id: "ca-pub-4140966684432854", slot_id: "1234567890",
    cmp_enabled: false,
  };
  const heading = { type: "heading" as const, text: "先看流量", level: 2 as const };
  const para = (text: string) => ({ type: "paragraph" as const, text });
  const articleHero = {
    src: "/guides/tokyo-esim/hero.jpg", alt: "成田機場的 SIM 卡販賣機", width: 1600, height: 900,
  };
  const longBody = {
    ...document,
    hero: articleHero,
    blocks: [heading, para("開頭"), ...Array.from({ length: 6 }, (_, i) => para(`段落 ${i}`))],
  };

  it("renders nothing at all — not even reserved space — when advertising is off", () => {
    const { container } = draw({ document: longBody });
    expect(screen.queryByTestId("ad-slot")).toBeNull();
    expect(container.querySelector("aside")).toBeNull();
  });

  it("places one labelled slot inside the body, never above the hero", () => {
    draw({ document: longBody }, { adsense: enabled });
    const slot = screen.getByTestId("ad-slot");
    expect(slot.getAttribute("data-publisher")).toBe("ca-pub-4140966684432854");
    expect(slot.getAttribute("data-slot")).toBe("1234567890");
    expect(slot.textContent).toBe("廣告");
    expect(slot.getAttribute("data-cmp")).toBe("false");
    expect(screen.getAllByTestId("ad-slot")).toHaveLength(1);
    // The only unit on the page asks for its ad straight away.
    expect(slot.getAttribute("data-lazy")).toBe("false");
    // After the first heading and its paragraph, so the hero (the LCP element) is untouched.
    const rendered = Array.from(slot.parentElement!.children).map((node) => node.textContent);
    expect(rendered.indexOf("廣告")).toBeGreaterThan(rendered.indexOf("開頭"));
  });

  it("gives a long article more units, spaced out, with only the first requested on load", () => {
    const sections = Array.from({ length: 4 }, (_, s) => [
      { type: "heading" as const, text: `第 ${s + 1} 節`, level: 2 as const },
      ...Array.from({ length: 10 }, (_, i) => para(`${s + 1}-${i}`)),
    ]).flat();
    draw({ document: { ...longBody, blocks: sections } }, { adsense: enabled });
    const slots = screen.getAllByTestId("ad-slot");
    expect(slots).toHaveLength(3);
    expect(slots.map((slot) => slot.getAttribute("data-lazy"))).toEqual(["false", "true", "true"]);
    // Every block still drawn exactly once, and the table of contents still lines up.
    expect(screen.getAllByRole("heading", { level: 2 }).map((node) => node.id))
      .toEqual(["section-1", "section-2", "section-3", "section-4"]);
    const rendered = Array.from(slots[0].parentElement!.children).map((node) => node.textContent);
    const at = rendered.flatMap((text, index) => (text === "廣告" ? [index] : []));
    at.slice(1).forEach((index, i) => expect(index - at[i]).toBeGreaterThan(MIN_BLOCKS_BETWEEN));
  });

  it("keeps its distance from the editor's partner buttons", () => {
    // The first section is too short to hold a unit clear of the button that ends it, so the
    // unit moves past the button, and still leaves room after it. Policy forbids an ad beside
    // an interactive element, and those buttons are the revenue.
    const { container, unmount } = draw({
      document: {
        ...document,
        blocks: [
          heading, para("開頭"), para("一段"),
          { type: "offer" as const, module: "connectivity", destination_id: null, heading: null },
          ...Array.from({ length: 12 }, (_, i) => para(`後段 ${i}`)),
        ],
      },
    }, { adsense: enabled });
    const children = Array.from(container.querySelector("article")!.children);
    const button = children.findIndex((node) => node.querySelector("[data-testid='affiliate']"));
    const slot = children.findIndex((node) => node.getAttribute("data-testid") === "ad-slot");
    expect(button).toBeGreaterThan(-1);
    expect(slot - button - 1).toBe(AD_CLEARANCE_BLOCKS);
    unmount();
    // Too little body after the button and the unit is simply left out.
    draw({
      document: {
        ...document,
        blocks: [
          heading, para("開頭"), para("一段"),
          { type: "offer" as const, module: "connectivity", destination_id: null, heading: null },
          ...Array.from({ length: 8 }, (_, i) => para(`再一次 ${i}`)),
        ],
      },
    }, { adsense: enabled });
    expect(screen.queryByTestId("ad-slot")).toBeNull();
  });

  it("keeps more of the article above the slot when there is no hero", () => {
    // The hero is most of what separates the headline from the first section. Without one
    // this body no longer has room for the clearance the slot needs, so it carries no ad —
    // rather than putting one in the reader's opening viewport.
    draw({ document: { ...longBody, hero: null } }, { adsense: enabled });
    expect(screen.queryByTestId("ad-slot")).toBeNull();
    // Long enough to afford the clearance, and it comes back.
    draw({
      document: {
        ...longBody, hero: null,
        blocks: [heading, para("開頭"), ...Array.from({ length: 8 }, (_, i) => para(`段落 ${i}`))],
      },
    }, { adsense: enabled });
    expect(screen.getAllByTestId("ad-slot")).toHaveLength(1);
  });

  it("keeps the same distance from a partner link, which ends the first slice just like a button", () => {
    const url = "https://www.hostinger.com/tw/vps-hosting?aff_id=12345";
    draw({
      kind: "life",
      destination_id: null,
      destination_label: null,
      partner_links: [{ key: "0123456789abcdef", partner: "hostinger", display_name: "Hostinger", url }],
      document: {
        ...document,
        blocks: [
          heading, para("開頭"), para("一段"),
          { type: "partner_link" as const, partner: "hostinger", url, label: "看方案" },
          ...Array.from({ length: 8 }, (_, i) => para(`後段 ${i}`)),
        ],
      },
    }, { adsense: enabled });
    expect(screen.getByRole("link", { name: /看方案/ })).toBeTruthy();
    expect(screen.queryByTestId("ad-slot")).toBeNull();
  });

  it("leaves a short article alone", () => {
    draw({ document: { ...document, blocks: [heading, para("只有兩段"), para("就這樣")] } },
      { adsense: enabled });
    expect(screen.queryByTestId("ad-slot")).toBeNull();
  });

  it("still numbers the headings the table of contents points at", () => {
    const withContents = {
      ...document,
      blocks: [
        heading, para("開頭"), para("一"), para("一之二"),
        { type: "heading" as const, text: "再看價格", level: 2 as const }, para("二"), para("二之二"),
        { type: "heading" as const, text: "最後看涵蓋", level: 2 as const }, para("三"), para("三之二"),
      ],
    };
    draw({ document: withContents }, { adsense: enabled });
    expect(screen.getByTestId("ad-slot")).toBeTruthy();
    // Split rendering must not restart the numbering: the contents links would go nowhere.
    const links = screen.getAllByRole("link").filter((a) => a.getAttribute("href")?.startsWith("#"));
    expect(links.map((a) => a.getAttribute("href"))).toEqual(["#section-1", "#section-2", "#section-3"]);
    // The second heading is drawn by the slice after the slot: without a continued count it
    // would restart at section-1 and every contents link below the ad would go nowhere.
    expect(screen.getAllByRole("heading", { level: 2 }).map((node) => node.id))
      .toEqual(["section-1", "section-2", "section-3"]);
  });
});

describe("GuideArticle consent message", () => {
  const withCmp: AdsenseConfig = {
    enabled: true, publisher_id: "ca-pub-4140966684432854", slot_id: "1234567890",
    cmp_enabled: true,
  };
  const heading = { type: "heading" as const, text: "先看流量", level: 2 as const };
  const para = (text: string) => ({ type: "paragraph" as const, text });
  const articleHero = {
    src: "/guides/tokyo-esim/hero.jpg", alt: "成田機場的 SIM 卡販賣機", width: 1600, height: 900,
  };
  const longBody = {
    ...document,
    hero: articleHero,
    blocks: [heading, para("開頭"), ...Array.from({ length: 6 }, (_, i) => para(`段落 ${i}`))],
  };

  it("tells the slot when a certified consent message decides personalisation", () => {
    draw({ document: longBody }, { adsense: withCmp });
    // Without this the loader forces non-personalised ads and the consent answer is ignored.
    expect(screen.getByTestId("ad-slot").getAttribute("data-cmp")).toBe("true");
  });
});

describe("GuideArticle translations", () => {
  it("ends at the sources: a translated article never lists its other languages", () => {
    const { container } = draw({
      published_locales: ["zh-TW", "en", "ja", "ko", "zh-CN"],
      document: { ...document, sources: [{ title: "來源", url: "https://example.com/", checked_on: "2026-09-01" }] },
    });
    // The set is still declared to search engines in `alternates.languages`; the reader
    // switches language from the header, not from a list under the article.
    expect(container.querySelector("a[hreflang]")).toBeNull();
    expect(screen.queryByText("English")).toBeNull();
    expect(screen.queryByText("日本語")).toBeNull();
    const sections = container.querySelectorAll("section");
    expect(sections[sections.length - 1]!.textContent).toContain("來源");
  });
});

describe("GuideArticle summary and FAQ", () => {
  const faq = { type: "faq" as const, items: [{ question: "要實體 SIM 嗎？", answer: "不用。" }, { question: "多少錢？", answer: "看方案。" }] };

  it("draws the summary under the description and keeps FAQ answers before the related reading and sources", () => {
    const { container } = draw({
      document: {
        ...document,
        blocks: [
          { type: "summary", items: ["先買 eSIM。", "落地就能上網。"] },
          ...document.blocks,
          faq,
        ],
        sources: [{ title: "來源", url: "https://example.com/", checked_on: "2026-09-01" }],
      },
    }, { related: <section aria-label="延伸閱讀">下一篇文章</section>, labels: { faq: "常見問題" } });
    const summary = container.querySelector("#article-summary")!;
    expect(summary).not.toBeNull();
    expect(summary.textContent).toContain("先買 eSIM。");
    const description = screen.getByText(document.description);
    expect(description.compareDocumentPosition(summary) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    const answers = container.querySelector("#article-faq")!;
    const sources = screen.getByRole("heading", { name: "來源" });
    const related = screen.getByRole("region", { name: "延伸閱讀" });
    expect(answers.compareDocumentPosition(related) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(answers.compareDocumentPosition(sources) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(answers.querySelectorAll("details")).toHaveLength(2);
    // Once each: the body renders around them.
    expect(screen.getAllByText("先買 eSIM。")).toHaveLength(1);
    expect(screen.getAllByText("要實體 SIM 嗎？")).toHaveLength(1);
  });

  it.each(["常見問題", "Reader questions", "よくある質問", "자주 묻는 질문", "常见问题"])("keeps an authored %s heading and its contents link beside the answers", (title) => {
    const { container } = draw({
      document: { ...document, blocks: [
        { type: "heading", level: 2, text: "First section" },
        { type: "paragraph", text: "Start here." },
        { type: "heading", level: 2, text: title },
        faq,
        { type: "callout", tone: "info", title: "After the answers", text: "Check the provider." },
        { type: "heading", level: 2, text: "Next steps" },
        { type: "paragraph", text: "Then continue." },
      ] },
    }, { labels: { faq: "Automatic FAQ heading" } });
    const heading = screen.getByRole("heading", { name: title });
    const answers = container.querySelector("#article-faq")!;
    expect(heading.id).toBe("section-2");
    expect(heading.nextElementSibling).toBe(answers);
    expect(answers.querySelectorAll("details")).toHaveLength(2);
    expect(screen.queryByRole("heading", { name: "Automatic FAQ heading" })).toBeNull();
    const contents = screen.getByRole("navigation", { name: "目錄" });
    const link = within(contents).getByRole("link", { name: `2. ${title}` });
    expect(link.getAttribute("href")).toBe(`#${heading.id}`);
    expect(answers.compareDocumentPosition(screen.getByText("Check the provider.")) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(screen.getAllByRole("heading", { level: 2 }).map((node) => node.id)).toEqual(["section-1", "section-2", "section-3"]);
  });

  it("preserves a separate section and its introduction before an unheaded FAQ", () => {
    const { container } = draw({ document: { ...document, blocks: [
      { type: "heading", level: 2, text: "Booking details" },
      { type: "paragraph", text: "Read these conditions first." },
      faq,
      { type: "paragraph", text: "Keep your confirmation." },
    ] } }, { labels: { faq: "Frequently asked questions" } });
    const heading = screen.getByRole("heading", { name: "Booking details" });
    expect(heading.id).toBe("section-1");
    expect(heading.nextElementSibling?.textContent).toBe("Read these conditions first.");
    const answers = container.querySelector("#article-faq")!;
    expect(within(answers as HTMLElement).getByRole("heading", { name: "Frequently asked questions" })).toBeTruthy();
    expect(screen.getByText("Read these conditions first.").compareDocumentPosition(answers) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(answers.compareDocumentPosition(screen.getByText("Keep your confirmation.")) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  it("keeps introductory prose under a localized FAQ heading without adding the heading again", () => {
    const { container } = draw({ locale: "en", document: { ...document, blocks: [
      { type: "heading", level: 2, text: "FREQUENTLY ASKED QUESTIONS" },
      { type: "paragraph", text: "Here are the booking answers." },
      faq,
    ] } }, { labels: { faq: "Frequently asked questions" } });
    expect(screen.getAllByRole("heading", { name: /frequently asked questions/i })).toHaveLength(1);
    expect(screen.getByRole("heading", { name: "FREQUENTLY ASKED QUESTIONS" }).id).toBe("section-1");
    const introduction = screen.getByText("Here are the booking answers.");
    expect(introduction.nextElementSibling).toBe(container.querySelector("#article-faq"));
  });

  it("keeps multiple older FAQ blocks once each with distinct section ids in their original order", () => {
    const secondFaq = { type: "faq" as const, items: [{ question: "Can I cancel?", answer: "Check your fare." }] };
    const { container } = draw({ document: { ...document, blocks: [
      faq,
      { type: "paragraph", text: "The cancellation rules differ." },
      { type: "heading", level: 2, text: "Cancellation questions" },
      secondFaq,
      { type: "paragraph", text: "Finish here." },
    ] } }, { labels: { faq: "FAQ" }, related: <p>Read another article.</p> });
    const first = container.querySelector("#article-faq")!;
    const second = container.querySelector("#article-faq-2")!;
    expect(first.querySelectorAll("details")).toHaveLength(2);
    expect(second.querySelectorAll("details")).toHaveLength(1);
    expect(screen.getAllByText("要實體 SIM 嗎？")).toHaveLength(1);
    expect(screen.getAllByText("Can I cancel?")).toHaveLength(1);
    const between = screen.getByText("The cancellation rules differ.");
    expect(first.compareDocumentPosition(between) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(between.compareDocumentPosition(second) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(second.compareDocumentPosition(screen.getByText("Read another article.")) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Cancellation questions" }).nextElementSibling).toBe(second);
    expect(screen.getAllByRole("heading", { name: "FAQ" })).toHaveLength(1);
  });

  it("continues the existing subsection anchors across an inline FAQ", () => {
    const { container } = draw({ document: { ...document, blocks: [
      { type: "heading", level: 2, text: "Prices" },
      { type: "heading", level: 3, text: "Before booking" },
      { type: "paragraph", text: "Compare the total." },
      faq,
      { type: "heading", level: 3, text: "After booking" },
      { type: "paragraph", text: "Save the receipt." },
    ] } }, { labels: { faq: "FAQ" } });
    expect(screen.getAllByRole("heading", { level: 3 }).map((node) => node.id)).toEqual(["section-1-1", "section-1-2"]);
    const answers = container.querySelector("#article-faq")!;
    expect(answers.compareDocumentPosition(screen.getByRole("heading", { name: "After booking" })) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  });

  it("keeps the FAQ identity and heading association after partner and advertising slices", () => {
    const paragraphs = Array.from({ length: 20 }, (_, index) => ({ type: "paragraph" as const, text: `Detail ${index}` }));
    const url = "https://www.hostinger.com/tw/vps-hosting?aff_id=12345";
    const { container } = draw({
      kind: "life",
      destination_id: null,
      destination_label: null,
      partner_links: [{ key: "0123456789abcdef", partner: "hostinger", display_name: "Hostinger", url }],
      document: { ...document, hero: { src: "/guides/tokyo-esim/hero.jpg", alt: "Hero", width: 1600, height: 900 }, blocks: [
        { type: "heading", level: 2, text: "Introduction" },
        { type: "paragraph", text: "Opening paragraph." },
        { type: "partner_link", partner: "hostinger", url, label: "View hosting" },
        ...paragraphs,
        { type: "heading", level: 2, text: "Reader questions" },
        faq,
      ] },
    }, { labels: { faq: "Automatic FAQ heading" }, adsense: {
      enabled: true, publisher_id: "ca-pub-4140966684432854", slot_id: "1234567890", cmp_enabled: false,
    } });
    expect(screen.getAllByTestId("ad-slot").length).toBeGreaterThan(0);
    const partner = screen.getByRole("link", { name: /View hosting/ });
    const answers = container.querySelector("#article-faq")!;
    expect(answers.querySelectorAll("details")).toHaveLength(2);
    expect(screen.getByRole("heading", { name: "Reader questions" }).id).toBe("section-2");
    expect(screen.getByRole("heading", { name: "Reader questions" }).nextElementSibling).toBe(answers);
    expect(partner.compareDocumentPosition(answers) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "Automatic FAQ heading" })).toBeNull();
  });

  it("does not remove a FAQ-like heading or any prose when the source has no FAQ block", () => {
    const { container } = draw({ document: { ...document, blocks: [
      { type: "heading", level: 2, text: "常見問題" },
      { type: "paragraph", text: "These answers are ordinary prose." },
    ] } }, { labels: { faq: "常見問題" } });
    expect(screen.getByRole("heading", { name: "常見問題" }).id).toBe("section-1");
    expect(screen.getByText("These answers are ordinary prose.")).toBeTruthy();
    expect(container.querySelector("#article-faq")).toBeNull();
  });
});

describe("GuideArticle reader support", () => {
  it("draws no support line while the owner has not set a tip page", () => {
    draw({}, { labels: { support: { text: "如果這篇文章對你有幫助，歡迎小額支持本站繼續更新。", action: "支持 Mokaair", newTab: "另開新分頁" } } });
    expect(screen.queryByText("支持 Mokaair")).toBeNull();
    expect(screen.queryByText(/歡迎小額支持/)).toBeNull();
  });
});
