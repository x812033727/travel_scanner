import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { GuideArticle } from "./article";

vi.mock("@/components/destination-affiliate-options", () => ({
  DestinationAffiliateOptions: (props: { destinationId: string; modules?: string[]; placement?: string; contextual?: boolean; destinationLabel?: string }) => (
    <div
      data-testid="affiliate"
      data-destination={props.destinationId}
      data-modules={(props.modules ?? []).join(",")}
      data-placement={props.placement}
      data-contextual={String(Boolean(props.contextual))}
      data-label={props.destinationLabel ?? ""}
    />
  ),
}));

const labels = {
  intel: "情報", howto: "攻略", life: "生活分享",
  published: "發布", updated: "更新", expiredNotice: "已過期", validUntil: "有效至",
  sources: "來源", checkedOn: "查核日", destination: "目的地", otherLanguages: "其他語言",
  contents: "目錄", disclosure: "透過合作連結預訂，本站可能獲得分潤。",
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

function draw(overrides: Record<string, unknown> = {}, extra: { readingTime?: string } = {}) {
  return render(
    <GuideArticle
      labels={labels}
      readingTime={extra.readingTime}
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

describe("GuideArticle partner buttons", () => {
  it("ends a destination article with the modules its topics point at, labelled as the guide surface", () => {
    draw();
    const panel = screen.getByTestId("affiliate");
    expect(panel.getAttribute("data-destination")).toBe("tokyo");
    expect(panel.getAttribute("data-modules")).toBe("connectivity");
    expect(panel.getAttribute("data-placement")).toBe("guide");
    expect(panel.getAttribute("data-contextual")).toBe("true");
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

  it("shows nothing under an expired notice", () => {
    draw({ kind: "intel", expired: true, valid_until: "2026-09-01", topics: [{ slug: "deal", label: "優惠" }] });
    expect(screen.getByRole("status")).toBeTruthy();
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

  it("drops every button, inline ones included, under an expired notice", () => {
    draw({ document: withOffer, topics, kind: "intel", expired: true, valid_until: "2026-09-01" });
    expect(screen.queryByTestId("affiliate")).toBeNull();
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
