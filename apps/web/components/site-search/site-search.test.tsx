import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError } from "@/lib/api";
import { SiteSearch } from "./site-search";

const mock = vi.hoisted(() => ({ api: vi.fn(), push: vi.fn() }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/i18n/navigation", () => ({ useRouter: () => ({ push: mock.push }), usePathname: () => "/" }));

const summary = (slug: string, title: string, kind: "intel" | "howto" | "life" = "life") => ({
  slug, kind, destination_id: null, destination_label: null, topics: [], title, description: "描述",
  published_at: "2026-09-01T00:00:00Z", valid_until: null, featured: false, snippet: "", matched: [],
});
const answer = (results: unknown[], best_match: unknown = null) => ({
  query: "codex", total: results.length, offset: 0, limit: 6, results, best_match, next_offset: null,
});

/** Type, then let the debounce and the promise settle. */
async function type(value: string) {
  fireEvent.change(screen.getByRole("combobox"), { target: { value } });
  await act(async () => { await vi.advanceTimersByTimeAsync(250); });
}

beforeEach(() => {
  vi.useFakeTimers();
  vi.clearAllMocks();
  mock.api.mockResolvedValue(answer([summary("codex-cli", "Codex CLI 入門"), summary("codex-ide", "Codex 在 IDE", "howto")]));
});
afterEach(() => { cleanup(); vi.useRealTimers(); });

describe("SiteSearch", () => {
  it("is a GET form to the results page that works before any script runs", () => {
    render(<SiteSearch variant="inline" />);
    const form = screen.getByRole("search");
    expect(form.getAttribute("method")).toBe("get");
    expect(form.getAttribute("action")).toBe("/zh-TW/search/articles");
    const input = screen.getByRole("combobox");
    expect(input.getAttribute("name")).toBe("q");
    expect(input.getAttribute("aria-expanded")).toBe("false");
    expect(mock.api).not.toHaveBeenCalled();
  });

  it("asks the API once per pause, only from two characters, in the page's language", async () => {
    render(<SiteSearch variant="inline" />);
    await type("c");
    expect(mock.api).not.toHaveBeenCalled();
    fireEvent.change(screen.getByRole("combobox"), { target: { value: "co" } });
    fireEvent.change(screen.getByRole("combobox"), { target: { value: "cod" } });
    await act(async () => { await vi.advanceTimersByTimeAsync(250); });
    expect(mock.api).toHaveBeenCalledTimes(1);
    const [path, init] = mock.api.mock.calls[0];
    expect(path).toBe("/guides/search?locale=zh-TW&q=cod&limit=6");
    expect(init.signal).toBeInstanceOf(AbortSignal);
  });

  it("lists the hits with their section, the best match first, and a row for all results", async () => {
    mock.api.mockResolvedValue(answer([summary("codex-cli", "Codex CLI 入門"), summary("codex-ide", "Codex 在 IDE", "howto")], summary("codex-hub", "Codex")));
    render(<SiteSearch variant="inline" />);
    await type("codex");
    const list = screen.getByRole("listbox", { name: "搜尋建議" });
    const rows = within(list).getAllByRole("option").map((row) => row.textContent);
    expect(rows).toEqual(["Codex最符合", "Codex CLI 入門生活分享", "Codex 在 IDE攻略", "查看「codex」的全部結果"]);
    expect(screen.getByRole("combobox").getAttribute("aria-expanded")).toBe("true");
  });

  it("walks the list with the arrows and follows the marked row on Enter", async () => {
    render(<SiteSearch variant="inline" />);
    await type("codex");
    const input = screen.getByRole("combobox");
    fireEvent.keyDown(input, { key: "ArrowDown" });
    fireEvent.keyDown(input, { key: "ArrowDown" });
    const options = screen.getAllByRole("option");
    expect(options[1].getAttribute("aria-selected")).toBe("true");
    expect(input.getAttribute("aria-activedescendant")).toBe(options[1].id);
    fireEvent.keyDown(input, { key: "ArrowUp" });
    fireEvent.keyDown(input, { key: "ArrowUp" });
    // Wraps from the top to the bottom row.
    expect(screen.getAllByRole("option").at(-1)?.getAttribute("aria-selected")).toBe("true");
    fireEvent.keyDown(input, { key: "ArrowDown" });
    fireEvent.submit(screen.getByRole("search"));
    expect(mock.push).toHaveBeenCalledWith("/life/codex-cli");
    expect(screen.getByRole("combobox").getAttribute("aria-expanded")).toBe("false");
  });

  it("submits to the results page when no row is marked, and on a click follows the row", async () => {
    const onNavigate = vi.fn();
    render(<SiteSearch variant="dialog" onNavigate={onNavigate} />);
    await type("codex");
    fireEvent.submit(screen.getByRole("search"));
    expect(mock.push).toHaveBeenCalledWith("/search/articles?q=codex");
    expect(onNavigate).toHaveBeenCalledTimes(1);
    // Submitting closed the list; coming back to the box reopens the answer it still holds.
    fireEvent.focus(screen.getByRole("combobox"));
    fireEvent.click(screen.getByRole("option", { name: /Codex 在 IDE/ }));
    expect(mock.push).toHaveBeenLastCalledWith("/guides/howto/codex-ide");
    expect(onNavigate).toHaveBeenCalledTimes(2);
  });

  it("closes the list on Escape and marks the event handled, leaving what is around it open", async () => {
    render(<SiteSearch variant="dialog" />);
    await type("codex");
    const input = screen.getByRole("combobox");
    const escape = new KeyboardEvent("keydown", { key: "Escape", bubbles: true, cancelable: true });
    act(() => { input.dispatchEvent(escape); });
    expect(escape.defaultPrevented).toBe(true);
    expect(input.getAttribute("aria-expanded")).toBe("false");
    // A second Escape, with nothing to close here, is left for the sheet.
    const again = new KeyboardEvent("keydown", { key: "Escape", bubbles: true, cancelable: true });
    act(() => { input.dispatchEvent(again); });
    expect(again.defaultPrevented).toBe(false);
  });

  it("does not react to keys typed through an IME composition", async () => {
    render(<SiteSearch variant="inline" />);
    await type("codex");
    const input = screen.getByRole("combobox");
    fireEvent.keyDown(input, { key: "ArrowDown", isComposing: true });
    expect(screen.getAllByRole("option").every((row) => row.getAttribute("aria-selected") === "false")).toBe(true);
  });

  it("says when nothing matched, treats a refused query as no match, and says when search is down", async () => {
    mock.api.mockResolvedValue(answer([]));
    render(<SiteSearch variant="inline" />);
    await type("zzzz");
    expect(screen.getByRole("status").textContent).toBe("沒有符合的文章");
    mock.api.mockRejectedValue(new ApiError("refused", 422, "guide_search_query_invalid"));
    await type("zzzzz");
    expect(screen.getByRole("status").textContent).toBe("沒有符合的文章");
    mock.api.mockRejectedValue(new ApiError("down", 503));
    await type("zzzzzz");
    expect(screen.getByRole("status").textContent).toBe("搜尋暫時無法使用");
  });

  it("shows the loading state while the answer is in flight and the older answer never overwrites a newer one", async () => {
    let resolveSlow: (value: unknown) => void = () => {};
    mock.api.mockImplementationOnce(() => new Promise((resolve) => { resolveSlow = resolve; }));
    render(<SiteSearch variant="inline" />);
    await type("slow");
    expect(screen.getByRole("status").textContent).toBe("搜尋中…");
    mock.api.mockResolvedValueOnce(answer([summary("fast", "快的答案")]));
    await type("fast");
    expect(screen.getByRole("option", { name: /快的答案/ })).toBeTruthy();
    await act(async () => { resolveSlow(answer([summary("slow", "慢的答案")])); await Promise.resolve(); });
    expect(screen.queryByRole("option", { name: /慢的答案/ })).toBeNull();
  });
});
