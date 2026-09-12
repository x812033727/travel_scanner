import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { TripDayPartnerOffers, TripPartnerNextSteps } from "./trip-day-partner-offers";

const mounts = vi.hoisted(() => ({ count: 0, last: undefined as Record<string, unknown> | undefined }));
vi.mock("@/components/destination-affiliate-options", () => ({
  DestinationAffiliateOptions: (props: Record<string, unknown>) => {
    mounts.count += 1;
    mounts.last = props;
    return <div data-testid="affiliate" data-placement={String(props.placement)} data-modules={(props.modules as string[]).join(",")} />;
  },
}));

describe("TripDayPartnerOffers", () => {
  it("mounts the partner panel only while the member holds the block open", () => {
    mounts.count = 0;
    render(<TripDayPartnerOffers destinationId="tokyo" modules={["transport", "connectivity"]} kind="arrival" destinationLabel="東京" />);
    const summary = screen.getByText("抵達後的安排");
    const details = summary.closest("details")!;
    expect(details.open).toBe(false);
    expect(screen.queryByTestId("affiliate")).toBeNull();
    expect(mounts.count).toBe(0);

    details.open = true;
    fireEvent(details, new Event("toggle"));
    expect(screen.getByTestId("affiliate").getAttribute("data-placement")).toBe("trip");
    expect(screen.getByTestId("affiliate").getAttribute("data-modules")).toBe("transport,connectivity");
    expect(mounts.last?.destinationId).toBe("tokyo");

    details.open = false;
    fireEvent(details, new Event("toggle"));
    expect(screen.queryByTestId("affiliate")).toBeNull();
  });

  it("names the block after the day it ends", () => {
    render(<TripDayPartnerOffers destinationId="tokyo" modules={["activities"]} kind="day" />);
    expect(screen.getByText("門票與一日遊")).toBeTruthy();
    render(<TripDayPartnerOffers destinationId="tokyo" modules={["transport"]} kind="departure" />);
    expect(screen.getByText("回程前的安排")).toBeTruthy();
  });

  it("renders nothing when no module is ready", () => {
    const { container } = render(<TripDayPartnerOffers destinationId="tokyo" modules={[]} kind="day" />);
    expect(container.innerHTML).toBe("");
  });
});

describe("TripPartnerNextSteps", () => {
  it("mounts the panel at once and goes away on dismiss", () => {
    const onDismiss = vi.fn();
    render(<TripPartnerNextSteps destinationId="tokyo" modules={["activities"]} destinationLabel="東京" onDismiss={onDismiss} />);
    const card = screen.getByRole("region", { name: "接下來可以預訂" });
    expect(card.textContent).toContain("AI 已排好地點");
    expect(screen.getByTestId("affiliate").getAttribute("data-placement")).toBe("trip");
    fireEvent.click(screen.getByRole("button", { name: "關閉" }));
    expect(onDismiss).toHaveBeenCalledTimes(1);
  });
});
