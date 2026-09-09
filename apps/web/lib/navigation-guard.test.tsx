import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { StrictMode } from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { requestNavigation, useNavigationGuard } from "./navigation-guard";

let states: unknown[];
let urls: string[];
let position: number;
let originalUrl: string;
beforeEach(() => {
  vi.useFakeTimers(); states = [{ previous: true }, { __NA: true, tree: "preserved" }]; position = 1;
  originalUrl = window.location.href;
  urls = [new URL("/previous", originalUrl).href, new URL("/editor", originalUrl).href];
  const replaceState = window.history.replaceState.bind(window.history);
  replaceState(states[position], "", urls[position]);
  vi.spyOn(window.history, "state", "get").mockImplementation(() => states[position]);
  vi.spyOn(window.history, "pushState").mockImplementation((state, _unused, url) => {
    states.splice(position + 1); states.push(state);
    urls.splice(position + 1); urls.push(new URL(url?.toString() || window.location.href, window.location.href).href);
    position++;
    replaceState(state, "", urls[position]);
  });
  vi.spyOn(window.history, "go").mockImplementation((delta = 0) => {
    const next = position + delta;
    if (!delta || next < 0 || next >= states.length) return;
    position = next;
    replaceState(states[position], "", urls[position]);
    window.dispatchEvent(new PopStateEvent("popstate", { state: states[position] }));
  });
  vi.spyOn(window.history, "back").mockImplementation(() => window.history.go(-1));
});
afterEach(() => { cleanup(); vi.useRealTimers(); vi.restoreAllMocks(); window.history.replaceState(null, "", originalUrl); });

function Guard({ enabled = true, request }: { enabled?: boolean; request: (proceed: () => void) => boolean }) {
  useNavigationGuard(enabled, request);
  // Exercise document-level native-link interception independently of Next's router.
  // eslint-disable-next-line @next/next/no-html-link-for-pages
  return <a href="/pricing">Plans</a>;
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

  it("stops at the selected history destination after accepting a jump past the guard", () => {
    window.history.pushState({ __NA: true, tree: "editor" }, "", "/editor/deep");
    let confirm: (() => void) | undefined;
    render(<Guard request={(proceed) => { confirm = proceed; return false; }} />);
    act(() => vi.runOnlyPendingTimers());
    // [previous, editor, editor/deep, guard] -> explicitly select editor, not previous.
    act(() => window.history.go(-2));
    expect(window.location.pathname).toBe("/editor/deep");
    act(() => confirm?.());
    expect(window.location.pathname).toBe("/editor");
    expect(position).toBe(1);
  });

  it("retains the editor and draft after a cancelled history jump, then reaches the same target", () => {
    window.history.pushState({ __NA: true, tree: "editor" }, "", "/editor/deep");
    let confirm: (() => void) | undefined;
    const request = vi.fn((proceed: () => void) => { confirm = proceed; return false; });
    render(<><Guard request={request} /><input aria-label="Draft" defaultValue="Unsaved content" /></>);
    act(() => vi.runOnlyPendingTimers());
    act(() => window.history.go(-2));
    expect(request).toHaveBeenCalledTimes(1);
    expect(window.location.pathname).toBe("/editor/deep");
    expect(screen.getByRole("textbox", { name: "Draft" })).toHaveProperty("value", "Unsaved content");
    // Cancelled restoration retains the selected destination behind our new guard.
    // Do not claim that pushState can retain the browser's truncated forward entries.
    act(() => window.history.back());
    expect(request).toHaveBeenCalledTimes(2);
    expect(window.location.pathname).toBe("/editor/deep");
    act(() => confirm?.());
    expect(window.location.pathname).toBe("/editor");
    expect(position).toBe(1);
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
