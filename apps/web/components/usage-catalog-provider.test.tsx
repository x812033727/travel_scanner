import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { UsageCatalogProvider, useOperationCharge } from "./usage-catalog-provider";
import { defaultUsageCatalog } from "@/lib/usage-catalog";

function Probe() {
  const charge = useOperationCharge("flight_status_lookup");
  return <><button disabled={charge.status !== "ready"}>{charge.label}</button><p>{charge.unavailableHelp}</p></>;
}

describe("UsageCatalogProvider", () => {
  it("renders a zero-cost operation as free", () => {
    render(<UsageCatalogProvider state={{
      status: "ready",
      catalog: {
        ...defaultUsageCatalog,
        operation_costs: { ...defaultUsageCatalog.operation_costs, flight_status_lookup: 0 },
      },
    }}><Probe /></UsageCatalogProvider>);
    expect(screen.getByRole("button", { name: "免費" }).hasAttribute("disabled")).toBe(false);
  });

  it("disables metered actions when the catalog cannot be confirmed", () => {
    render(<UsageCatalogProvider state={{ status: "unavailable", catalog: null }}><Probe /></UsageCatalogProvider>);
    expect(screen.getByRole("button", { name: "暫時無法確認扣次" }).hasAttribute("disabled")).toBe(true);
    expect(screen.getByText(/請稍後再試/)).toBeTruthy();
  });
});
