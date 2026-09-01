import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminHotspotGuidesPanel } from "./admin-hotspot-guides-panel";

const coverage = {
  items: [{
    id: "11111111-1111-1111-1111-111111111111",
    name: "淺草寺",
    complete: false,
    coverage: Object.fromEntries(
      ["en", "ja", "ko", "zh-TW", "zh-CN"].map((locale) => [locale, { article: 0, video: 0 }]),
    ),
  }],
  total: 1,
  complete: 0,
  quotas: { youtube: { used: 3, automatic_limit: 80 }, brave: { used: 2, limit: 30 } },
  ai_search: {
    enabled: true,
    default_provider: "minimax",
    providers: { minimax: true, openai: false, anthropic: true },
    sources: { brave: true, youtube: true },
    quota: { runs_used: 1, runs_limit: 10, calls_used: 4, calls_limit: 60 },
  },
};

function response(body: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(body), { status }));
}

afterEach(() => vi.unstubAllGlobals());

describe("AdminHotspotGuidesPanel AI research", () => {
  it("opens with MiniMax deep five-language defaults and submits an idempotent job", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/guides/coverage")) return response(coverage);
      if (init?.method === "POST" && url.endsWith("/guides/ai-search")) {
        return response({
          run_id: "run-1", status: "queued", progress: 0, current: {}, usage: {}, result: {},
          error_code: null,
        }, 202);
      }
      return response({ items: [], total: 0, page: 1, pages: 0 });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotGuidesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "AI 搜尋" }));

    expect(screen.getByRole("dialog").textContent).toContain("淺草寺");
    expect((screen.getByLabelText("AI 供應商") as HTMLSelectElement).value).toBe("minimax");
    expect((screen.getByLabelText("搜尋深度") as HTMLSelectElement).value).toBe("deep");
    expect(screen.getByRole("dialog").textContent).toContain("25");
    fireEvent.click(screen.getByRole("button", { name: "開始 AI 深度搜尋" }));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(
      "/api/travel/admin/hotspots/guides/ai-search",
      expect.objectContaining({ method: "POST" }),
    ));
    const post = fetchMock.mock.calls.find(([, init]) => init?.method === "POST");
    expect(post?.[1]?.headers).toEqual(expect.objectContaining({ "Idempotency-Key": expect.any(String) }));
    expect(JSON.parse(String(post?.[1]?.body))).toEqual(expect.objectContaining({
      provider: "minimax", depth: "deep", only_missing: true,
      locales: ["en", "ja", "ko", "zh-TW", "zh-CN"],
      content_types: ["article", "video"],
    }));
  });

  it("shows unavailable providers without silently switching", async () => {
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => String(input).includes("/guides/coverage")
      ? response(coverage) : response({ items: [], total: 0, page: 1, pages: 0 })));
    render(<AdminHotspotGuidesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "AI 搜尋" }));
    const openAI = screen.getByRole("option", { name: /OpenAI.*未設定/ });
    expect((openAI as HTMLOptionElement).disabled).toBe(true);
    expect((screen.getByLabelText("AI 供應商") as HTMLSelectElement).value).toBe("minimax");
  });
});
