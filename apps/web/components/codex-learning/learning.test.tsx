import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { useEffect, useState, type ReactNode } from "react";
import { SearchParamsContext } from "next/dist/shared/lib/hooks-client-context.shared-runtime";
import { LearningHub } from "./hub";
import { GuideCodeBlock } from "@/components/guide-code-block";
import { lessons, learningEntries, filterLessons } from "@/lib/codex-learning";
import type { GuideSummary } from "@/lib/guides";
import { ContentBlocks } from "@/components/content-blocks";
import { learningFilterUrl, readLearningFilters } from "@/lib/codex-learning/filters";
import type { Locale } from "@/i18n/routing";

const published = (index: number): GuideSummary => ({ slug: lessons[index].slug, kind: "life", title: lessons[index].locales.en.title, description: lessons[index].locales.en.description, destination_id: null, destination_label: null, topics: [], published_at: "2026-09-14T00:00:00Z", valid_until: null, featured: false });

// Supply Next's URL context in jsdom. Real router timing and rapid Back are
// covered by history-browser.mjs, which reproduced the pre-fix failure.
function RouterHarness({ children }: { children: ReactNode }) {
  const [search, setSearch] = useState(window.location.search);
  useEffect(() => {
    const sync = () => setSearch(window.location.search);
    const push = window.history.pushState.bind(window.history);
    const replace = window.history.replaceState.bind(window.history);
    const pushSpy = vi.spyOn(window.history, "pushState").mockImplementation((...args) => { push(...args); sync(); });
    const replaceSpy = vi.spyOn(window.history, "replaceState").mockImplementation((...args) => { replace(...args); sync(); });
    window.addEventListener("popstate", sync);
    return () => { pushSpy.mockRestore(); replaceSpy.mockRestore(); window.removeEventListener("popstate", sync); };
  }, []);
  return <SearchParamsContext.Provider value={new URLSearchParams(search)}>{children}</SearchParamsContext.Provider>;
}

describe("Codex learning", () => {
  beforeEach(() => window.history.replaceState(null, "", "/en/life/codex-learning-hub"));
  it("finds command aliases and intersects all filters", () => {
    const entries = learningEntries("en", []);
    expect(filterLessons(entries, "AGENTS.md", "0", "2", "1").map((r) => r.id)).toContain(10);
    expect(filterLessons(entries, "/plan", "2", "", "")).toEqual([]);
  });
  it("links only published articles and clears filters", () => {
    render(<LearningHub locale="en" entries={learningEntries("en", [published(0)])} available />, { wrapper: RouterHarness });
    expect(screen.getByRole("link", { name: published(0).title })).toBeTruthy();
    expect(screen.queryByRole("link", { name: lessons[1].locales.en.title })).toBeNull();
    fireEvent.change(screen.getByRole("searchbox"), { target: { value: "does-not-exist" } });
    expect(screen.getByText("No matching tutorials")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Clear filters" }));
    expect(screen.getByRole("link", { name: published(0).title })).toBeTruthy();
  });
  it.each([
    ["zh-TW", "指令索引", "規劃中", "尚未發布", "暫時無法確認發布狀態"],
    ["zh-CN", "命令索引", "规划中", "尚未发布", "暂时无法确认发布状态"],
    ["en", "Command index", "Planned", "Not published", "Publication status temporarily unavailable"],
    ["ja", "コマンド索引", "企画中", "未公開", "公開状況を一時的に確認できません"],
    ["ko", "명령 색인", "기획 중", "미게시", "게시 상태를 일시적으로 확인할 수 없습니다"],
  ])("distinguishes unavailable, planned and unpublished command targets in %s", (locale, name, planned, unpublished, unavailable) => {
    const row = learningEntries(locale as Locale, []).find((entry) => entry.id === 10)!;
    const { rerender } = render(<LearningHub locale={locale as Locale} entries={[row]} available={false} />, { wrapper: RouterHarness });
    for (const [available, ready, expected] of [[false, true, unavailable], [false, false, unavailable], [true, false, planned], [true, true, unpublished]] as const) {
      rerender(<LearningHub locale={locale as Locale} entries={[{ ...row, ready }]} available={available} />);
      const commands = within(screen.getByRole("region", { name }));
      expect(commands.getByText(`${row.title} · ${expected}`)).toBeTruthy();
      expect(commands.queryAllByRole("link")).toEqual([]);
    }
    rerender(<LearningHub locale={locale as Locale} entries={[{ ...row, published: true, updated: "2026-09-14" }]} available />);
    expect(within(screen.getByRole("region", { name })).getByRole("link", { name: row.title })).toBeTruthy();
  });
  it("hydrates shared filters, keeps them in URLs, and responds to browser history", () => {
    window.history.replaceState(null, "", "/en/life/codex-learning-hub?unit=D&q=AGENTS.md&utm_source=shared#lessons");
    render(<LearningHub locale="en" entries={learningEntries("en", [])} available />, { wrapper: RouterHarness });
    expect((screen.getByRole("searchbox") as HTMLInputElement).value).toBe("AGENTS.md");
    expect((screen.getByLabelText("Unit") as HTMLSelectElement).value).toBe("D");
    fireEvent.change(screen.getByLabelText("Unit"), { target: { value: "E" } });
    expect(window.location.search).toContain("unit=E");
    expect(window.location.search).toContain("utm_source=shared");
    expect(window.location.hash).toBe("#lessons");
    act(() => { window.history.replaceState(null, "", "?unit=D&q=AGENTS.md"); window.dispatchEvent(new PopStateEvent("popstate")); });
    expect((screen.getByLabelText("Unit") as HTMLSelectElement).value).toBe("D");
    fireEvent.click(screen.getByRole("button", { name: "Clear filters" }));
    expect(window.location.search).toBe("");
  });
  it("rejects invalid filter enums, bounds searches and preserves unrelated URL data", () => {
    const filters = readLearningFilters(`?level=-1&platform=99&goal=NaN&unit=K&q=${"a".repeat(250)}`);
    expect(filters).toEqual({ level: "", platform: "", goal: "", unit: "", q: "a".repeat(200) });
    expect(learningFilterUrl("https://mokaair.com/en/life/codex-learning-hub?ref=1#x", { ...filters, q: "a & b", unit: "D" })).toBe("/en/life/codex-learning-hub?ref=1&q=a+%26+b&unit=D#x");
  });
  it("renders code as inert text and copies exact whitespace", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { configurable: true, value: { writeText } });
    const code = "<script>alert(1)</script>\n\tvalue = 2\n";
    const { container } = render(<GuideCodeBlock block={{ type: "code", label: "HTML", language: "html", code }} />);
    expect(container.querySelector("script")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Copy" }));
    await waitFor(() => expect(writeText).toHaveBeenCalledWith(code));
    await screen.findByText("Copied");
  });
  it("shows a recoverable clipboard error", async () => {
    Object.defineProperty(navigator, "clipboard", { configurable: true, value: { writeText: vi.fn().mockRejectedValue(new Error("denied")) } });
    render(<GuideCodeBlock block={{ type: "code", label: "Input", language: "text", code: "test" }} />);
    fireEvent.click(screen.getByRole("button", { name: "Copy" }));
    await screen.findByText("Copy failed. Select the code and copy it manually.");
  });
  it("preserves inline spaces and does not interpret legacy Markdown", () => {
    const { container } = render(<ContentBlocks blocks={[{ type: "rich_paragraph", inlines: [{ type: "text", text: "Read " }, { type: "link", text: "guide", url: "https://example.com" }, { type: "text", text: " now." }] }, { type: "paragraph", text: "[literal](url)" }]} />);
    expect(container.querySelector("p")?.textContent).toBe("Read guide now.");
    expect(screen.getByText("[literal](url)")).toBeTruthy();
  });
});
