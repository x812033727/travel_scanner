import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DiscoverySearch } from "./explorer";

vi.mock("@/lib/discovery", async (original) => ({ ...await original<object>(), useDiscoveryResource: (path: string | null) => ({ data: path ? { query: "coffee", items: [{ label: "Coffee walk", query: "coffee walk" }, { label: "Coffee shops", query: "coffee shops" }] } : undefined, loading: false }) }));
beforeEach(() => vi.useFakeTimers());
afterEach(() => { cleanup(); vi.useRealTimers(); });
function open() { const input = screen.getByRole("searchbox"); input.focus(); fireEvent.change(input, { target: { value: "coffee" } }); act(() => vi.advanceTimersByTime(300)); return input; }

describe("discovery search suggestions", () => {
  it("closes on outside pointer and focus leaving, while a suggestion remains selectable", () => {
    const search = vi.fn(); render(<><DiscoverySearch initial="" onSearch={search} /><button>Outside</button></>);
    const input = open(); expect(screen.getByRole("button", { name: "Coffee walk" })).toBeTruthy();
    fireEvent.pointerDown(screen.getByRole("button", { name: "Outside" })); expect(screen.queryByText("Coffee walk")).toBeNull();
    fireEvent.focus(input); fireEvent.click(screen.getByRole("button", { name: "Coffee walk" }));
    expect(search).toHaveBeenCalledWith("coffee walk");
    fireEvent.change(input, { target: { value: "coffee" } }); act(() => vi.advanceTimersByTime(300));
    fireEvent.blur(input, { relatedTarget: screen.getByRole("button", { name: "Outside" }) }); expect(screen.queryByText("Coffee walk")).toBeNull();
  });

  it("supports keyboard suggestions and consumes only the first Escape", () => {
    const outer = vi.fn(); render(<div onKeyDown={outer}><DiscoverySearch initial="" onSearch={vi.fn()} /></div>);
    const input = open(); fireEvent.keyDown(input, { key: "ArrowDown" });
    const suggestion = screen.getByRole("button", { name: "Coffee walk" }); expect(document.activeElement).toBe(suggestion);
    outer.mockClear(); fireEvent.keyDown(suggestion, { key: "Escape" });
    expect(document.activeElement).toBe(input); expect(screen.queryByText("Coffee walk")).toBeNull(); expect(outer).not.toHaveBeenCalled();
    fireEvent.keyDown(input, { key: "Escape" }); expect(outer).toHaveBeenCalledOnce();
  });
});
