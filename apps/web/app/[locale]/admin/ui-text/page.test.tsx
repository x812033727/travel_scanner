import { cleanup, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { EDITABLE_NAMESPACES } from "@/lib/ui-text";
import AdminUiTextPage from "./page";

// The panel is where the editing lives; this file is about what the page resolves out of
// the query string and which catalog it hands over.
vi.mock("@/components/admin-ui-text-panel", () => ({
  AdminUiTextPanel: ({
    namespace,
    locale,
    referenceLocale,
    defaults,
    referenceDefaults,
    namespaces,
  }: {
    namespace: string;
    locale: string;
    referenceLocale: string;
    defaults: Record<string, string>;
    referenceDefaults: Record<string, string>;
    namespaces: { namespace: string; keyCount: number }[];
  }) => (
    <div
      data-testid="panel"
      data-selection={`${namespace}/${locale}/${referenceLocale}`}
      data-keys={Object.keys(defaults).length}
      data-reference-keys={Object.keys(referenceDefaults).length}
      data-namespaces={namespaces.length}
      data-sample={JSON.stringify(Object.entries(defaults)[0] ?? null)}
    />
  ),
}));

async function renderPage(query: Record<string, string | string[] | undefined>) {
  // Several cases render more than once; Testing Library only cleans up between tests.
  cleanup();
  render(await AdminUiTextPage({ searchParams: Promise.resolve(query) }));
  return screen.getByTestId("panel");
}

describe("AdminUiTextPage", () => {
  it("defaults to the shared namespace in the site's own locale", async () => {
    const panel = await renderPage({});

    expect(panel.getAttribute("data-selection")).toBe("common/zh-TW/en");
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("前台文案");
    // The bundled catalog is the source of the defaults, because the API has no copy.
    expect(Number(panel.getAttribute("data-keys"))).toBeGreaterThan(0);
    // Every editable namespace is offered; check-i18n keeps that list and the catalog
    // directory in step, so this only has to agree with the list itself.
    expect(Number(panel.getAttribute("data-namespaces"))).toBe(EDITABLE_NAMESPACES.length);
  });

  it("passes a valid selection straight through", async () => {
    const panel = await renderPage({ ns: "search", locale: "ja", ref: "ko" });
    expect(panel.getAttribute("data-selection")).toBe("search/ja/ko");
    expect(Number(panel.getAttribute("data-reference-keys"))).toBe(
      Number(panel.getAttribute("data-keys")),
    );
  });

  it("falls back silently rather than redirecting on a stale or hostile query", async () => {
    // legacy is locked everywhere, and an unknown locale must not reach a dynamic import.
    expect((await renderPage({ ns: "legacy", locale: "xx" })).getAttribute("data-selection")).toBe(
      "common/zh-TW/en",
    );
    expect(
      (await renderPage({ ns: "../../etc/passwd" })).getAttribute("data-selection"),
    ).toBe("common/zh-TW/en");
  });

  it("never uses one locale as its own reference", async () => {
    expect((await renderPage({ locale: "en", ref: "en" })).getAttribute("data-selection")).toBe(
      "common/en/zh-TW",
    );
    expect((await renderPage({ locale: "ja" })).getAttribute("data-selection")).toBe(
      "common/ja/zh-TW",
    );
  });

  it("reads repeated query parameters as their first value", async () => {
    const panel = await renderPage({ ns: ["search", "trips"], locale: ["ja"] });
    expect(panel.getAttribute("data-selection")).toBe("search/ja/zh-TW");
  });
});
