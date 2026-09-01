import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { closedSiteVisibility, openSiteVisibility, type SiteVisibilityState } from "@/lib/site-features";
import { PublicFeatureGate } from "./public-feature-gate";

const getSiteVisibility = vi.fn<() => Promise<SiteVisibilityState>>();

vi.mock("@/lib/site-visibility.server", () => ({
  getSiteVisibility: () => getSiteVisibility(),
}));

vi.mock("@/components/site-header", () => ({
  SiteHeader: () => <div>header</div>,
}));

beforeEach(() => getSiteVisibility.mockReset());

describe("PublicFeatureGate", () => {
  it("renders content when the feature is open", async () => {
    getSiteVisibility.mockResolvedValue({ status: "ready", features: openSiteVisibility });
    render(await PublicFeatureGate({ feature: "trips", children: <div>trip content</div> }));
    expect(screen.getByText("trip content")).toBeTruthy();
  });

  it("replaces closed content with a localized paused page", async () => {
    getSiteVisibility.mockResolvedValue({ status: "ready", features: closedSiteVisibility });
    render(await PublicFeatureGate({ feature: "trips", children: <div>trip content</div> }));
    expect(screen.getByRole("heading", { name: "我的旅行目前暫停開放" })).toBeTruthy();
    expect(screen.queryByText("trip content")).toBeNull();
  });

  it("shows an unavailable state when visibility cannot be confirmed", async () => {
    getSiteVisibility.mockResolvedValue({ status: "unavailable", features: closedSiteVisibility });
    render(await PublicFeatureGate({ feature: "pricing", children: <div>pricing content</div> }));
    expect(screen.getByRole("heading", { name: "暫時無法確認方案與次數包狀態" })).toBeTruthy();
    expect(screen.queryByText("pricing content")).toBeNull();
  });
});
