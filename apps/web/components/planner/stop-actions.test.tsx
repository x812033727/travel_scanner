import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { StopActions } from "./stop-actions";
import { OptionalStop } from "./optional-stop";
import { PlannerToolSections } from "./tool-sections";

describe("progressive planner controls", () => {
  it("closes card actions after an action, outside click and Escape, returning keyboard focus", () => {
    const action = vi.fn();
    const { container } = render(<StopActions label="Place options"><button onClick={action}>Move</button></StopActions>);
    const details = container.querySelector("details")!;
    const summary = screen.getByLabelText("Place options");
    details.open = true;
    fireEvent.click(screen.getByRole("button", { name: "Move" }));
    expect(action).toHaveBeenCalledOnce();
    expect(details.open).toBe(false);
    expect(summary).toHaveFocus();
    details.open = true;
    fireEvent.keyDown(summary, { key: "Escape" });
    expect(details.open).toBe(false);
    details.open = true;
    fireEvent.pointerDown(document.body);
    expect(details.open).toBe(false);
  });
  it("keeps pending system content available on demand without hiding a configured stop", () => {
    const { rerender, container } = render(<OptionalStop collapsed kind="hotel" title="Stay" hint="Not arranged"><button>Choose hotel</button></OptionalStop>);
    expect(container.querySelector("details")).not.toHaveAttribute("open");
    expect(screen.getByText("Choose hotel")).not.toBeVisible();
    rerender(<OptionalStop collapsed={false} kind="hotel" title="Stay" hint="Not arranged"><button>Choose hotel</button></OptionalStop>);
    expect(screen.getByRole("button", { name: "Choose hotel" })).toBeVisible();
  });
  it("does not mount supporting services until their category is opened", () => {
    const mount = vi.fn();
    function SupportingService() { mount(); return <p>Forecast</p>; }
    render(<PlannerToolSections locale="en" preparation={<SupportingService />} settings={<p>Settings form</p>} sharing={<p>Share form</p>} />);
    expect(mount).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: /Travel essentials/ }));
    expect(screen.getByText("Forecast")).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Back" }));
    expect(screen.queryByText("Forecast")).toBeNull();
  });
});
