import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { GuideArticle } from "./article";

vi.mock("@/components/destination-affiliate-options", () => ({
  DestinationAffiliateOptions: (props: { destinationId: string; modules?: string[]; placement?: string; contextual?: boolean }) => (
    <div
      data-testid="affiliate"
      data-destination={props.destinationId}
      data-modules={(props.modules ?? []).join(",")}
      data-placement={props.placement}
      data-contextual={String(Boolean(props.contextual))}
    />
  ),
}));

const labels = {
  intel: "情報", howto: "攻略", life: "生活分享",
  published: "發布", updated: "更新", expiredNotice: "已過期", validUntil: "有效至",
  sources: "來源", checkedOn: "查核日", destination: "目的地", otherLanguages: "其他語言",
};

const document = {
  title: "東京 eSIM 怎麼選",
  description: "三家方案比較",
  version: 1,
  published_at: "2026-09-10T00:00:00Z",
  blocks: [{ type: "paragraph" as const, text: "先看流量。" }],
  sources: [],
};

function draw(overrides: Record<string, unknown> = {}) {
  return render(
    <GuideArticle
      labels={labels}
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
