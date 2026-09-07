import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminHotspotIntroGenerator } from "./admin-hotspot-intro-generator";

type Coverage = { locale: string; id: string | null; status: string | null };

function coverage(rows: Partial<Coverage>[] = []): Coverage[] {
  const base = ["zh-TW", "zh-CN", "en", "ja", "ko"];
  return base.map((locale) => {
    const found = rows.find((row) => row.locale === locale);
    return { locale, id: found?.id ?? null, status: found?.status ?? null };
  });
}

function respond(url: string, coverageRows: Coverage[], run?: object) {
  if (url.includes("/intros/runs/")) return new Response(JSON.stringify(run));
  if (url.includes("/intros/generate")) return new Response(JSON.stringify(run), { status: 202 });
  return new Response(JSON.stringify({ hotspot_id: "h1", locales: coverageRows }));
}

function queuedRun(overrides: object = {}) {
  return {
    run_id: "run-1",
    status: "queued",
    provider: "minimax",
    model: "minimax-m2",
    requested_locales: ["en"],
    result: null,
    error_code: null,
    error_message: null,
    ...overrides,
  };
}

async function open(fetchMock: ReturnType<typeof vi.fn>) {
  render(<AdminHotspotIntroGenerator hotspotId="h1" hotspotName="淺草寺" />);
  fireEvent.click(screen.getByRole("button", { name: "為「淺草寺」產生介紹" }));
  await waitFor(() => expect(fetchMock).toHaveBeenCalled());
  return screen.findByRole("dialog");
}

describe("AdminHotspotIntroGenerator", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("asks only for the languages that have nothing yet", async () => {
    // Filling gaps is the common case, and asking for a locale that is already written
    // spends a model call to say the same thing again.
    const rows = coverage([
      { locale: "zh-TW", id: "a", status: "approved" },
      { locale: "ja", id: "b", status: "pending" },
    ]);
    const fetchMock = vi.fn<typeof fetch>(async (input) =>
      respond(String(input), rows, queuedRun()),
    );
    vi.stubGlobal("fetch", fetchMock);

    const dialog = await open(fetchMock);
    const boxes = within(dialog).getAllByRole("checkbox");
    const byLabel = (code: string) =>
      boxes.find((box) => box.closest("label")?.textContent?.startsWith(code)) as HTMLInputElement;

    expect(byLabel("zh-CN").checked).toBe(true);
    expect(byLabel("en").checked).toBe(true);
    expect(byLabel("ko").checked).toBe(true);
    expect(byLabel("zh-TW").checked).toBe(false);
    expect(byLabel("ja").checked).toBe(false);
    expect(within(dialog).getAllByText("還沒有").length).toBe(3);
  });

  it("leaves approved paragraphs alone unless replacing them is ticked", async () => {
    const rows = coverage([{ locale: "zh-TW", id: "a", status: "approved" }]);
    const fetchMock = vi.fn<typeof fetch>(async (input) =>
      respond(String(input), rows, queuedRun()),
    );
    vi.stubGlobal("fetch", fetchMock);

    const dialog = await open(fetchMock);
    const replace = within(dialog).getByLabelText(/連已核准的也重寫/) as HTMLInputElement;
    expect(replace.checked).toBe(false);

    fireEvent.click(within(dialog).getByRole("button", { name: "開始產生" }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    const [, init] = fetchMock.mock.calls[1];
    expect(JSON.parse(String(init?.body)).force).toBe(false);
    expect(String(init?.method)).toBe("POST");
    // Without a key the API cannot dedupe a double-click into one paid run.
    expect((init?.headers as Record<string, string>)["Idempotency-Key"]).toBeTruthy();
  });

  it("offers replacement only when something is actually approved", async () => {
    const fetchMock = vi.fn<typeof fetch>(async (input) =>
      respond(String(input), coverage(), queuedRun()),
    );
    vi.stubGlobal("fetch", fetchMock);

    const dialog = await open(fetchMock);
    expect(within(dialog).queryByLabelText(/連已核准的也重寫/)).toBeNull();
  });

  it("reports what the finished run wrote, kept and refused", async () => {
    const finished = queuedRun({
      status: "partial",
      result: {
        created: ["en", "ja"],
        kept_approved: ["zh-TW"],
        rejected: [{ locale: "ko", reason: "hours" }],
      },
    });
    const fetchMock = vi.fn<typeof fetch>(async (input) => {
      const url = String(input);
      if (url.includes("/intros/runs/")) return new Response(JSON.stringify(finished));
      if (url.includes("/generate"))
        return new Response(JSON.stringify(queuedRun({ status: "running" })), { status: 202 });
      return new Response(JSON.stringify({ hotspot_id: "h1", locales: coverage() }));
    });
    vi.stubGlobal("fetch", fetchMock);
    vi.useFakeTimers({ shouldAdvanceTime: true });

    const dialog = await open(fetchMock);
    fireEvent.click(within(dialog).getByRole("button", { name: "開始產生" }));
    // "產生中" is on the button too, so match the status line's own shape.
    await waitFor(() =>
      expect(within(dialog).getByText("產生中 · minimax / minimax-m2")).toBeTruthy(),
    );

    await vi.advanceTimersByTimeAsync(1600);
    await waitFor(() =>
      expect(within(dialog).getByText("部分完成 · minimax / minimax-m2")).toBeTruthy(),
    );
    expect(within(dialog).getByText("已寫入待審：en、ja")).toBeTruthy();
    expect(within(dialog).getByText("已核准，未更動：zh-TW")).toBeTruthy();
    // A refused draft is reported, not silently dropped: a plausible invented fact is
    // worse than a missing paragraph, and the editor should know one was thrown away.
    expect(within(dialog).getByText("ko 被退回：hours")).toBeTruthy();
    vi.useRealTimers();
  });

  it("surfaces the API's own message when the vendor is not configured", async () => {
    const fetchMock = vi.fn<typeof fetch>(async (input) => {
      const url = String(input);
      if (url.includes("/generate"))
        return new Response(
          JSON.stringify({ code: "hotspot_guide_ai_provider_not_configured", detail: "所選 AI 供應商尚未設定" }),
          { status: 503 },
        );
      return new Response(JSON.stringify({ hotspot_id: "h1", locales: coverage() }));
    });
    vi.stubGlobal("fetch", fetchMock);

    const dialog = await open(fetchMock);
    fireEvent.click(within(dialog).getByRole("button", { name: "開始產生" }));
    await waitFor(() => expect(within(dialog).getByRole("alert")).toBeTruthy());
  });
});
