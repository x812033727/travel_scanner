import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { StrictMode } from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { requestNavigation, useNavigationGuard } from "./navigation-guard";

let states: unknown[];
let position: number;
beforeEach(() => {
  vi.useFakeTimers(); states = [{ previous: true }, { __NA: true, tree: "preserved" }]; position = 1;
  vi.spyOn(window.history, "state", "get").mockImplementation(() => states[position]);
  vi.spyOn(window.history, "pushState").mockImplementation((state) => { states.splice(position + 1); states.push(state); position++; });
  vi.spyOn(window.history, "back").mockImplementation(() => { if (position > 0) { position--; window.dispatchEvent(new PopStateEvent("popstate", { state: states[position] })); } });
});
afterEach(() => { cleanup(); vi.useRealTimers(); vi.restoreAllMocks(); });

function Guard({ enabled = true, request }: { enabled?: boolean; request: (proceed: () => void) => boolean }) {
  useNavigationGuard(enabled, request); return <a href="/pricing">Plans</a>;
}

describe("draft navigation guard", () => {
  it("defers programmatic writes until confirmation and consumes its own history entry", () => {
    let confirm: (() => void) | undefined; const navigate = vi.fn();
    render(<Guard request={(proceed) => { confirm = proceed; return false; }} />);
    act(() => vi.runOnlyPendingTimers());
    expect(window.history.state).toMatchObject({ __NA: true, tree: "preserved" });
    act(() => { expect(requestNavigation(navigate)).toBe(false); });
    expect(navigate).not.toHaveBeenCalled();
    act(() => confirm?.()); expect(navigate).toHaveBeenCalledTimes(1); expect(position).toBe(1);
  });

  it("keeps the draft in place after Back is cancelled and allows the requested Back after discard", () => {
    let confirm: (() => void) | undefined; const request = vi.fn((proceed: () => void) => { confirm = proceed; return false; });
    render(<Guard request={request} />); act(() => vi.runOnlyPendingTimers());
    act(() => window.history.back());
    expect(request).toHaveBeenCalledTimes(1); expect(position).toBe(2);
    act(() => confirm?.()); expect(position).toBe(0);
  });

  it("lets a child history layer close before requesting to leave the draft", () => {
    const request = vi.fn(() => false); render(<Guard request={request} />); act(() => vi.runOnlyPendingTimers());
    window.history.pushState({ ...window.history.state, hotelBooking: "child" }, "", window.location.href);
    act(() => window.history.back()); expect(request).not.toHaveBeenCalled();
    act(() => window.history.back()); expect(request).toHaveBeenCalledTimes(1);
  });

  it("blocks ordinary links but leaves new-tab and already-handled clicks alone", () => {
    const request = vi.fn(() => false); render(<Guard request={request} />);
    fireEvent.click(screen.getByRole("link")); expect(request).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getByRole("link"), { ctrlKey: true }); expect(request).toHaveBeenCalledTimes(1);
  });

  it("does not leave duplicate guard entries after Strict Mode or a clean save", () => {
    const request = vi.fn(() => false); const view = render(<StrictMode><Guard request={request} /></StrictMode>);
    act(() => vi.runOnlyPendingTimers()); expect(position).toBe(2);
    view.rerender(<StrictMode><Guard request={request} enabled={false} /></StrictMode>);
    expect(position).toBe(1); expect(request).not.toHaveBeenCalled();
    const navigate = vi.fn(); requestNavigation(navigate); expect(navigate).toHaveBeenCalledOnce();
  });
});
