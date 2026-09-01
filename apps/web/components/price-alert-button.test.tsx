import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { closedSiteVisibility } from "@/lib/site-features";
import { PriceAlertButton } from "./price-alert-button";
import { SiteVisibilityProvider } from "./site-visibility-provider";

describe("PriceAlertButton", () => {
  it("hides the create-alert operation when alerts are closed", () => {
    render(
      <SiteVisibilityProvider state={{ status: "ready", features: closedSiteVisibility }}>
        <PriceAlertButton resourceType="flight" resourceId="flight-1" />
      </SiteVisibilityProvider>,
    );
    expect(screen.queryByRole("button", { name: "建立價格通知" })).toBeNull();
  });
});
