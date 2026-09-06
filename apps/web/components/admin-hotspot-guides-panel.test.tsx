import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminHotspotGuidesPanel } from "./admin-hotspot-guides-panel";

const coverage = {
  items: [
    {
      id: "11111111-1111-1111-1111-111111111111",
      name: "淺草寺",
      complete: false,
      coverage: Object.fromEntries(
        ["en", "ja", "ko", "zh-TW", "zh-CN"].map((locale) => [
          locale,
          { article: 0, video: 0 },
        ]),
      ),
    },
  ],
  total: 1,
  complete: 0,
  quotas: {
    youtube: { used: 3, automatic_limit: 80 },
    brave: { used: 2, limit: 30 },
  },
  ai_search: {
    enabled: true,
    default_provider: "minimax",
    providers: { minimax: true, openai: false, anthropic: true },
    models: { minimax: "minimax-model-a", openai: "openai-model-a", anthropic: "claude-model-a" },
    sources: { brave: true, youtube: true },
    quota: { runs_used: 1, runs_limit: 10, calls_used: 4, calls_limit: 60 },
  },
};

function response(body: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(body), { status }));
}

afterEach(() => vi.unstubAllGlobals());

describe("AdminHotspotGuidesPanel AI research", () => {
  it("selects every visible guide candidate for batch review", async () => {
    const candidates = ["淺草寺介紹", "淺草寺影片"].map((title, index) => ({
      id: `22222222-2222-2222-2222-22222222222${index}`,
      hotspot_name: "淺草寺",
      type: index ? "video" : "article",
      provider: "manual",
      locale: "zh-TW",
      title,
      creator_name: "官方觀光",
      url: `https://example.com/${index}`,
      language_confidence: 1,
      status: "pending",
      discovery_method: "manual",
      ai_provider: null,
      relevance_score: null,
      quality_score: null,
      recommendation_reason: null,
      search_query: null,
    }));
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/guides/coverage")) return response(coverage);
      if (init?.method === "POST" && url.endsWith("/guides/review"))
        return response({ updated: 2 });
      return response({ items: candidates, total: 2, page: 1, pages: 1 });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotGuidesPanel />);
    const selectAll = await screen.findByRole("button", { name: "全選目前項目" });
    await waitFor(() =>
      expect(selectAll.hasAttribute("disabled")).toBe(false),
    );
    fireEvent.click(selectAll);
    expect(await screen.findByText("已選 2 筆")).toBeTruthy();
    expect(
      screen
        .getByRole("button", { name: "取消全選" })
        .getAttribute("aria-pressed"),
    ).toBe("true");
    fireEvent.click(screen.getByRole("button", { name: "核准" }));

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        "/api/travel/admin/hotspots/guides/review",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            ids: candidates.map((item) => item.id),
            action: "approve",
          }),
        }),
      ),
    );
  });

  it("opens with MiniMax deep five-language defaults and submits an idempotent job", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/guides/coverage")) return response(coverage);
      if (init?.method === "POST" && url.endsWith("/guides/ai-search")) {
        return response(
          {
            run_id: "run-1",
            status: "queued",
            progress: 0,
            current: {},
            usage: {},
            result: {},
            error_code: null,
          },
          202,
        );
      }
      return response({ items: [], total: 0, page: 1, pages: 0 });
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotGuidesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "AI 搜尋" }));

    expect(screen.getByRole("dialog").textContent).toContain("淺草寺");
    expect(
      (screen.getByLabelText("AI 供應商") as HTMLSelectElement).value,
    ).toBe("minimax");
    expect((screen.getByLabelText("搜尋深度") as HTMLSelectElement).value).toBe(
      "deep",
    );
    expect(screen.getByRole("dialog").textContent).toContain("25");
    fireEvent.click(screen.getByRole("button", { name: "開始 AI 深度搜尋" }));

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        "/api/travel/admin/hotspots/guides/ai-search",
        expect.objectContaining({ method: "POST" }),
      ),
    );
    const post = fetchMock.mock.calls.find(
      ([, init]) => init?.method === "POST",
    );
    expect(post?.[1]?.headers).toEqual(
      expect.objectContaining({ "Idempotency-Key": expect.any(String) }),
    );
    expect(JSON.parse(String(post?.[1]?.body))).toEqual(
      expect.objectContaining({
        provider: "minimax",
        depth: "deep",
        only_missing: true,
        locales: ["en", "ja", "ko", "zh-TW", "zh-CN"],
        content_types: ["article", "video"],
      }),
    );
  });

  it("shows unavailable providers without silently switching", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL) =>
        String(input).includes("/guides/coverage")
          ? response(coverage)
          : response({ items: [], total: 0, page: 1, pages: 0 }),
      ),
    );
    render(<AdminHotspotGuidesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "AI 搜尋" }));
    expect(screen.getByRole("option", { name: "MiniMax · minimax-model-a" })).toBeTruthy();
    const openAI = screen.getByRole("option", { name: "OpenAI · openai-model-a · 未設定" });
    expect((openAI as HTMLOptionElement).disabled).toBe(true);
    expect(
      (screen.getByLabelText("AI 供應商") as HTMLSelectElement).value,
    ).toBe("minimax");
  });
});

const localeCodes = ["en", "ja", "ko", "zh-TW", "zh-CN"];

function coverageItem(id: string, name: string, complete = false) {
  return {
    id,
    name,
    complete,
    coverage: Object.fromEntries(
      localeCodes.map((locale) => [
        locale,
        { article: complete ? 1 : 0, video: complete ? 1 : 0 },
      ]),
    ),
  };
}

function run(overrides: Record<string, unknown> = {}) {
  return {
    run_id: "run-1",
    status: "queued",
    progress: 0,
    current: {},
    usage: {},
    result: {},
    error_code: null,
    error_message: null,
    retryable: false,
    ...overrides,
  };
}

function emptyList() {
  return response({ items: [], total: 0, page: 1, pages: 0 });
}

function postCalls(fetchMock: ReturnType<typeof vi.fn>) {
  return fetchMock.mock.calls.filter(
    ([, init]) => (init as RequestInit | undefined)?.method === "POST",
  );
}

describe("AdminHotspotGuidesPanel feedback", () => {
  it("shows the failure reason and re-runs with a fresh idempotency key", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/guides/coverage")) return response(coverage);
      if (init?.method === "POST" && url.endsWith("/guides/ai-search"))
        return response(run(), 202);
      if (url.endsWith("/guides/ai-search/run-1"))
        return response(
          run({
            status: "failed",
            progress: 100,
            error_code: "ai_search_failed",
            error_message: "MiniMax 回應 400: bad json",
            retryable: true,
          }),
        );
      return emptyList();
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotGuidesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "AI 搜尋" }));
    fireEvent.click(screen.getByRole("button", { name: "開始 AI 深度搜尋" }));

    await screen.findByText("MiniMax 回應 400: bad json", undefined, {
      timeout: 4000,
    });
    expect(screen.getByText("AI 搜尋失敗")).toBeTruthy();
    expect(screen.queryByText(/已評估/)).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "重新執行" }));
    await waitFor(() => expect(postCalls(fetchMock)).toHaveLength(2));
    const keys = postCalls(fetchMock).map(
      ([, init]) =>
        ((init as RequestInit).headers as Record<string, string>)["Idempotency-Key"],
    );
    expect(keys[0]).toBeTruthy();
    expect(keys[0]).not.toBe(keys[1]);
  });

  it("explains non-retryable failures and lets Escape close the sheet", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.includes("/guides/coverage")) return response(coverage);
        if (init?.method === "POST" && url.endsWith("/guides/ai-search"))
          return response(
            run({
              status: "failed",
              progress: 100,
              error_code: "queue_unavailable",
              retryable: false,
            }),
            202,
          );
        return emptyList();
      }),
    );

    render(<AdminHotspotGuidesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "AI 搜尋" }));
    fireEvent.click(screen.getByRole("button", { name: "開始 AI 深度搜尋" }));

    await screen.findByText("搜尋佇列暫時無法使用");
    expect(screen.queryByRole("button", { name: "重新執行" })).toBeNull();
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  it("renders partial runs with translated per-locale issues", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.includes("/guides/coverage")) return response(coverage);
        if (init?.method === "POST" && url.endsWith("/guides/ai-search"))
          return response(
            run({
              status: "partial",
              progress: 100,
              result: {
                evaluated: 10,
                created: 2,
                errors: [
                  { locale: "ja", code: "youtube_quota_exhausted" },
                  {
                    locale: "ko",
                    code: "brave_search_failed",
                    detail: "HTTP 429 from api.search.brave.com: rate limited",
                  },
                ],
                notices: [
                  {
                    locale: "en",
                    code: "no_new_candidates",
                    detail: "3 筆搜尋結果已在候選清單中",
                  },
                ],
              },
            }),
            202,
          );
        return emptyList();
      }),
    );

    render(<AdminHotspotGuidesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "AI 搜尋" }));
    fireEvent.click(screen.getByRole("button", { name: "開始 AI 深度搜尋" }));

    expect(await screen.findByText("已評估 10 筆，新增 2 筆待審候選")).toBeTruthy();
    expect(screen.getByText("部分語系未完成，請查看下方錯誤明細")).toBeTruthy();
    expect(screen.getByText("ja：YouTube 搜尋額度已用完")).toBeTruthy();
    expect(
      screen.getByText("ko：Brave 搜尋失敗 — HTTP 429 from api.search.brave.com: rate limited"),
    ).toBeTruthy();
    expect(
      screen.getByText("en：搜尋結果都已在候選清單中 — 3 筆搜尋結果已在候選清單中"),
    ).toBeTruthy();
    expect(screen.queryByRole("button", { name: "重新執行" })).toBeNull();
  });

  it("submits a manual article with approval and reports the result", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes("/guides/coverage")) return response(coverage);
      if (init?.method === "POST" && url.endsWith("/guides/manual"))
        return response({
          created: 1,
          guide_id: "g-1",
          review_status: "approved",
          locale: "ja",
        });
      return emptyList();
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminHotspotGuidesPanel />);
    await screen.findByRole("button", { name: "AI 搜尋" });

    fireEvent.change(screen.getByLabelText("語系"), { target: { value: "ja" } });
    fireEvent.change(screen.getByPlaceholderText("HTTPS 連結"), {
      target: { value: "https://blog.example/asakusa" },
    });
    fireEvent.change(screen.getByPlaceholderText("標題"), {
      target: { value: "淺草寺散步" },
    });
    fireEvent.change(screen.getByPlaceholderText("創作者／網站"), {
      target: { value: "blog.example" },
    });
    fireEvent.change(screen.getByLabelText(/^摘要/), {
      target: { value: "一日遊路線" },
    });
    expect((screen.getByLabelText(/立即核准/) as HTMLInputElement).checked).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "新增並核准" }));

    expect(await screen.findByText("已新增並核准（ja）")).toBeTruthy();
    const [post] = postCalls(fetchMock);
    expect(JSON.parse(String((post[1] as RequestInit).body))).toEqual({
      hotspot_id: "11111111-1111-1111-1111-111111111111",
      locale: "ja",
      content_type: "article",
      url: "https://blog.example/asakusa",
      title: "淺草寺散步",
      creator_name: "blog.example",
      summary: "一日遊路線",
      approve: true,
    });
    expect((screen.getByPlaceholderText("HTTPS 連結") as HTMLInputElement).value).toBe("");
    expect((screen.getByLabelText("語系") as HTMLSelectElement).value).toBe("ja");
  });

  it("reports an updated duplicate that stays pending when approval is off", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.includes("/guides/coverage")) return response(coverage);
        if (init?.method === "POST" && url.endsWith("/guides/manual"))
          return response({
            created: 0,
            guide_id: "g-1",
            review_status: "pending",
            locale: "zh-TW",
          });
        return emptyList();
      }),
    );

    render(<AdminHotspotGuidesPanel />);
    await screen.findByRole("button", { name: "AI 搜尋" });
    fireEvent.click(screen.getByLabelText(/立即核准/));
    fireEvent.change(screen.getByPlaceholderText("HTTPS 連結"), {
      target: { value: "https://blog.example/asakusa" },
    });
    fireEvent.change(screen.getByPlaceholderText("標題"), {
      target: { value: "淺草寺散步" },
    });
    fireEvent.change(screen.getByPlaceholderText("創作者／網站"), {
      target: { value: "blog.example" },
    });
    fireEvent.click(screen.getByRole("button", { name: "建立候選" }));

    expect(
      await screen.findByText("這個連結已存在，已更新資料（zh-TW）"),
    ).toBeTruthy();
  });

  it("filters the manual hotspot picker and auto-selects the first match", async () => {
    const many = {
      ...coverage,
      items: [
        coverageItem("a", "東京鐵塔"),
        coverageItem("b", "淺草寺"),
        coverageItem("c", "上野公園"),
      ],
      total: 3,
    };
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL) =>
        String(input).includes("/guides/coverage") ? response(many) : emptyList(),
      ),
    );

    render(<AdminHotspotGuidesPanel />);
    await screen.findAllByRole("button", { name: "AI 搜尋" });

    fireEvent.change(screen.getByLabelText("篩選景點名稱"), {
      target: { value: "淺草" },
    });
    const picker = screen.getByLabelText("景點") as HTMLSelectElement;
    expect(picker.value).toBe("b");
    expect(
      within(picker).getAllByRole("option").map((option) => option.textContent),
    ).toEqual(["淺草寺"]);
  });

  it("shows incomplete hotspots first and can reveal every hotspot", async () => {
    const items = Array.from({ length: 14 }, (_, index) =>
      coverageItem(`id-${index}`, `景點 ${String(index).padStart(2, "0")}`, index === 0),
    );
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL) =>
        String(input).includes("/guides/coverage")
          ? response({ ...coverage, items, total: 14, complete: 1 })
          : emptyList(),
      ),
    );

    render(<AdminHotspotGuidesPanel />);
    await screen.findAllByRole("button", { name: "AI 搜尋" });
    const headings = () =>
      screen
        .getAllByRole("heading", { level: 3, name: /^景點 / })
        .map((heading) => heading.textContent);

    expect(screen.getAllByRole("button", { name: "AI 搜尋" })).toHaveLength(12);
    expect(headings()[0]).toBe("景點 01");
    fireEvent.click(screen.getByRole("button", { name: "顯示全部 14 個" }));
    expect(screen.getAllByRole("button", { name: "AI 搜尋" })).toHaveLength(14);
    expect(headings().at(-1)).toBe("景點 00");
    expect(screen.getByRole("button", { name: "只顯示前 12 個" })).toBeTruthy();
  });

  it("reports what standard discovery actually did", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.includes("/guides/coverage")) return response(coverage);
        if (init?.method === "POST" && url.endsWith("/guides/discover"))
          return response({
            reports: [
              {
                hotspot_id: "11111111-1111-1111-1111-111111111111",
                created: 3,
                providers: { youtube: "quota_exhausted", brave: "ready" },
                errors: [{ provider: "brave", locale: "ko", error: "ReadTimeout" }],
              },
            ],
          });
        return emptyList();
      }),
    );

    render(<AdminHotspotGuidesPanel />);
    fireEvent.click(await screen.findByRole("button", { name: "一般搜尋" }));

    expect(
      await screen.findByText("一般探索完成：新增 3 筆｜部分來源未能搜尋"),
    ).toBeTruthy();
    expect(screen.getByText("YouTube 今日額度已用完")).toBeTruthy();
    expect(screen.getByText("Brave（ko）：ReadTimeout")).toBeTruthy();
  });
});
