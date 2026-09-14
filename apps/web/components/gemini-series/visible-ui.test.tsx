import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it } from "vitest";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { renderToStaticMarkup } from "react-dom/server";
import { GeminiDirectory } from "./directory";
import { GeminiNavigation } from "./navigation";
import { fixtureSeries } from "./fixture.test-data";
import { geminiSeriesCopy as copy } from "@/lib/gemini-series-copy";

afterEach(cleanup);
const lessonLinks = () => within(screen.getByTestId("series-lessons")).queryAllByRole("link");

describe("visible Gemini UI", () => {
  it.each([false, true])("renders every allowed lesson and route on the server (advanced=%s)", advanced => {
    const series = fixtureSeries(advanced);
    const html = renderToStaticMarkup(<GeminiDirectory series={series} copy={copy} />);
    for (const article of series.articles) expect(html).toContain(`/zh-TW/life/${article.slug}`);
    render(<GeminiDirectory series={series} copy={copy} />);
    expect(lessonLinks()).toHaveLength(advanced ? 86 : 50);
    expect(screen.getByLabelText(copy.path).querySelectorAll("option")).toHaveLength(advanced ? 12 : 6);
    expect(screen.getAllByRole("link").every(link => !link.hasAttribute("target"))).toBe(true);
  });
  it("never serializes hidden paths in the initial HTML or boundary navigation", () => {
    const series = fixtureSeries();
    const html = renderToStaticMarkup(<><GeminiDirectory series={series} copy={copy} /><GeminiNavigation series={series} number={50} position="bottom" copy={copy} /></>);
    for (const article of fixtureSeries(true).articles.slice(50)) expect(html + JSON.stringify(series)).not.toContain(article.slug);
    expect(html).not.toContain('rel="next"');
    expect(html).not.toContain("python batch.py");
    expect(html).not.toContain(copy.track);
  });
  it.each(["MD", "GEMINI.md", "手機", "CLI", "/memory", "NotebookLM"])("searches %s and resets", query => {
    render(<GeminiDirectory series={fixtureSeries(true)} copy={copy} />);
    fireEvent.change(screen.getByRole("searchbox"), { target: { value: query } });
    expect(lessonLinks().length).toBeGreaterThan(0);
    fireEvent.click(screen.getByRole("button", { name: copy.clear }));
    expect(lessonLinks()).toHaveLength(86);
  });
  it("intersects stage, track, route and keyword filters without keeping unrelated commands", () => {
    const series = fixtureSeries(true);
    render(<GeminiDirectory series={series} copy={copy} />);
    fireEvent.change(screen.getByLabelText(copy.stage), { target: { value: "2" } });
    expect(lessonLinks()).toHaveLength(36);
    fireEvent.change(screen.getByLabelText(copy.track), { target: { value: "md" } });
    expect(lessonLinks()).toHaveLength(6);
    expect(screen.getByText(copy.noCommands)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(copy.path), { target: { value: "advanced-md" } });
    expect(lessonLinks()).toHaveLength(6);
    expect(screen.getAllByText(/實作約 60 分鐘/).length).toBeGreaterThan(0);
    fireEvent.change(screen.getByRole("searchbox"), { target: { value: "不存在功能xyz" } });
    expect(lessonLinks()).toHaveLength(0);
    expect(screen.getByText(copy.noResults)).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: copy.clear }));
    expect(lessonLinks()).toHaveLength(86);
  });
  it("preserves full advanced routes, including their base prerequisites before filtering", () => {
    const series = fixtureSeries(true);
    render(<GeminiDirectory series={series} copy={copy} />);
    fireEvent.change(screen.getByLabelText(copy.path), { target: { value: "advanced-md" } });
    expect(lessonLinks()).toHaveLength(18);
    const route = screen.getByRole("navigation", { name: copy.suggestedPaths });
    expect(within(route).getAllByRole("link")).toHaveLength(18);
    expect(within(route).getAllByRole("link")[0]).toHaveAttribute("href", expect.stringContaining(series.articles[34].slug));
  });
  it("keeps boundaries, cross-stage next links and hidden current lessons correct", () => {
    const series = fixtureSeries(true);
    const { rerender, container } = render(<GeminiNavigation series={series} number={50} position="bottom" copy={copy} />);
    expect(container.querySelector('[rel="next"]')).toHaveAttribute("href", `/zh-TW/life/${series.articles[50].slug}`);
    rerender(<GeminiNavigation series={series} number={86} position="bottom" copy={copy} />);
    expect(container.querySelector('[rel="next"]')).toBeNull();
    expect(container.querySelector('[rel="prev"]')).toHaveAttribute("href", `/zh-TW/life/${series.articles[84].slug}`);
    rerender(<GeminiNavigation series={series} number={1} position="bottom" copy={copy} />);
    expect(container.querySelector('[rel="prev"]')).toBeNull();
    rerender(<GeminiNavigation series={fixtureSeries()} number={51} position="bottom" copy={copy} />);
    expect(container).toBeEmptyDOMElement();
  });
});
