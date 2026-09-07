import { afterEach, describe, expect, it, vi } from "vitest";

import { loadUiTextOverrides } from "./ui-text.server";

afterEach(() => vi.unstubAllGlobals());

const unavailable = { status: "unavailable", version: null, entries: {} };

describe("loadUiTextOverrides", () => {
  it("asks the API for one locale and does not cache the response", async () => {
    const payload = { locale: "ja", version: "3f9c2b7d", entries: { "navigation.home": "ホーム" } };
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify(payload), { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    await expect(loadUiTextOverrides("ja")).resolves.toEqual({
      status: "ready",
      version: "3f9c2b7d",
      entries: { "navigation.home": "ホーム" },
    });
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/v1/runtime/ui-text?locale=ja",
      expect.objectContaining({ cache: "no-store" }),
    );
  });

  it("escapes the locale it is given", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ locale: "zh-TW", version: "a", entries: {} }), { status: 200 }),
    );
    vi.stubGlobal("fetch", fetchMock);

    await loadUiTextOverrides("zh-TW");
    expect(fetchMock.mock.calls[0][0]).toBe(
      "http://localhost:8000/api/v1/runtime/ui-text?locale=zh-TW",
    );
  });

  it("fails open so the bundled catalogs still render", async () => {
    // Every failure mode returns the same empty state: the catalogs are the default, so an
    // API that is down costs the overrides, never the page.
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    await expect(loadUiTextOverrides("en")).resolves.toEqual(unavailable);

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("{}", { status: 503 })));
    await expect(loadUiTextOverrides("en")).resolves.toEqual(unavailable);

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("not json", { status: 200 })));
    await expect(loadUiTextOverrides("en")).resolves.toEqual(unavailable);

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ locale: "en", version: "a", entries: { "a.b": 7 } }), {
        status: 200,
      }),
    ));
    await expect(loadUiTextOverrides("en")).resolves.toEqual(unavailable);
  });
});
