import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { GuideCard } from "./card";

const labels = { intel: "情報", howto: "攻略", life: "生活分享" };
const article = {
  slug: "narita-to-tokyo", kind: "howto" as const, destination_id: "tokyo", destination_label: "東京",
  topics: [{ slug: "transport", label: "交通" }], title: "成田機場到東京", description: "三種方式比較",
  hero: { src: "/img/narita.jpg", alt: "成田機場", width: 1600, height: 900, credit: null },
  published_at: "2026-09-01T00:00:00Z", valid_until: null, featured: true,
};

describe("a guide card", () => {
  it("shows the hero lazily, the badge, the title as the link, the description and the topics", () => {
    const { container } = render(<ul><GuideCard article={article} labels={labels} /></ul>);
    expect(screen.getByRole("link", { name: "成田機場到東京" }).getAttribute("href")).toBe("/guides/howto/narita-to-tokyo");
    expect(screen.getByRole("img", { name: "成田機場" }).getAttribute("loading")).toBe("lazy");
    expect(screen.getByText("攻略")).toBeTruthy();
    expect(screen.getByText("交通")).toBeTruthy();
    expect(container.querySelector("li")?.getAttribute("data-variant")).toBe("default");
  });

  it("drops the hero and the topics when compact, keeping the title and a clamped description", () => {
    const { container } = render(<ul><GuideCard article={article} labels={labels} variant="compact" /></ul>);
    expect(screen.queryByRole("img")).toBeNull();
    expect(screen.queryByText("交通")).toBeNull();
    expect(screen.getByRole("link", { name: "成田機場到東京" })).toBeTruthy();
    expect(screen.getByText("三種方式比較").className).toContain("line-clamp-2");
    expect(container.querySelector("li")?.getAttribute("data-variant")).toBe("compact");
  });

  it("spans the grid and loads its hero eagerly when featured, since it leads the page", () => {
    const { container } = render(<ul><GuideCard article={article} labels={labels} variant="featured" /></ul>);
    const card = container.querySelector("li")!;
    expect(card.className).toContain("sm:col-span-2");
    expect(screen.getByRole("img", { name: "成田機場" }).getAttribute("loading")).toBe("eager");
    expect(card.querySelector("h3")?.className).toContain("text-2xl");
  });
});
