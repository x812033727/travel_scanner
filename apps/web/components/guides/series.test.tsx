import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen, within } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup } from "@testing-library/react";
import { GeminiSeriesIndex } from "./series-index";
import { SeriesNavigation } from "./gemini-series-navigation";
import { GuideCodeBlock } from "@/components/guide-code-block";
import { geminiSeries } from "@/lib/gemini-series";
import { ContentBlocks } from "@/components/content-blocks";
import { siteUrl } from "@/lib/seo";

afterEach(cleanup);

describe("Gemini learning series", () => {
  it("server-renders all 50 lessons without JavaScript", () => {
    const html = renderToStaticMarkup(<GeminiSeriesIndex />);
    for (const article of geminiSeries.articles) expect(html).toContain(`/zh-TW/life/${article.slug}`);
    expect(geminiSeries.articles).toHaveLength(50);
    expect(new Set(geminiSeries.articles.map((article) => article.slug)).size).toBe(50);
  });
  it.each(["MD", "GEMINI.md", "手機", "CLI", "/memory", "NotebookLM"])("finds lessons for %s", (query) => {
    render(<GeminiSeriesIndex />);
    fireEvent.change(screen.getByRole("searchbox"), { target: { value: query } });
    expect(within(screen.getByTestId("series-lessons")).getAllByRole("link").length).toBeGreaterThan(0);
  });
  it("combines filters, handles empty results, and resets", () => {
    render(<GeminiSeriesIndex />);
    fireEvent.change(screen.getByLabelText("主題分類"), { target: { value: "F" } });
    expect(within(screen.getByTestId("series-lessons")).getAllByRole("link")).toHaveLength(6);
    fireEvent.change(screen.getByRole("searchbox"), { target: { value: "不存在的功能xyz" } });
    expect(screen.getByText(/沒有符合的教學/)).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "清除篩選" }));
    expect(within(screen.getByTestId("series-lessons")).getAllByRole("link")).toHaveLength(50);
  });
  it("handles the first and last lesson without circular next links", () => {
    const { rerender } = render(<SeriesNavigation article={geminiSeries.articles[0]} position="bottom" />);
    expect(screen.queryByRole("link", { name: /上一篇/ })).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: /下一篇/ })).toHaveAttribute("href", expect.stringContaining(geminiSeries.articles[1].slug));
    rerender(<SeriesNavigation article={geminiSeries.articles[49]} position="bottom" />);
    expect(screen.queryByRole("link", { name: /下一篇/ })).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: "返回 Gemini 教學總目錄" })).toHaveAttribute("href", "/zh-TW/life/gemini-guide");
  });
  it("keeps prose links inline, opens same-site links in place, and escapes code", () => {
    const { container } = render(<ContentBlocks blocks={[{ type: "rich_paragraph", inlines: [{ type: "text", text: "先讀 " }, { type: "link", text: "MD", url: `${siteUrl}/zh-TW/life/gemini-cli-gemini-md` }, { type: "text", text: " 再繼續" }] }, { type: "code", label: "example", language: "text", code: '<script>alert("x")</script>' }]} />);
    expect(screen.getByRole("link", { name: "MD" }).parentElement?.textContent).toBe("先讀 MD 再繼續");
    expect(screen.getByRole("link", { name: "MD" })).not.toHaveAttribute("target");
    expect(container.querySelector("script")).toBeNull();
    expect(container.querySelector("code")?.textContent).toContain("<script>");
  });
  it("copies the original indentation and reports a clipboard failure", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { configurable: true, value: { writeText } });
    const code = "if True:\n\tprint('hello')\n";
    render(<GuideCodeBlock block={{ type: "code", label: "example", language: "text", code }} labels={{ copy: "複製", copied: "已複製", copyFailed: "請手動複製" }} />);
    fireEvent.click(screen.getByRole("button", { name: "複製" }));
    expect(await screen.findByText("已複製")).toBeInTheDocument();
    expect(writeText).toHaveBeenCalledWith(code);
    writeText.mockRejectedValue(new Error("denied"));
    fireEvent.click(screen.getByRole("button", { name: "複製" }));
    expect(await screen.findByText("請手動複製")).toBeInTheDocument();
  });
});
