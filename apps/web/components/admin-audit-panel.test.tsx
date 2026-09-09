import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { api } from "@/lib/api";
import { AdminAuditPanel } from "./admin-audit-panel";

vi.mock("@/lib/api", () => ({ api: vi.fn() }));
vi.mock("next/navigation", () => ({ useSearchParams: () => new URLSearchParams(window.location.search) }));

afterEach(() => {
  window.history.replaceState(null, "", "/admin/audit");
  vi.clearAllMocks();
});

describe("AdminAuditPanel", () => {
  it("uses the API result vocabulary and sends date-only URL filters as explicit UTC boundaries", async () => {
    window.history.replaceState(null, "", "/admin/audit?result=succeeded&date_from=2026-09-01&date_to=2026-09-09");
    vi.mocked(api).mockResolvedValue({ items: [], total: 0, page: 1, limit: 25, pages: 1 });
    render(<AdminAuditPanel />);

    await waitFor(() => expect(api).toHaveBeenCalledTimes(1));
    const request = new URL(String(vi.mocked(api).mock.calls[0][0]), "https://mokaair.test");
    expect(request.searchParams.get("result")).toBe("succeeded");
    expect(request.searchParams.get("date_from")).toBe("2026-09-01T00:00:00.000Z");
    expect(request.searchParams.get("date_to")).toBe("2026-09-09T23:59:59.999Z");
    expect((screen.getByLabelText("結果") as HTMLSelectElement).value).toBe("succeeded");
  });

  it("restores filter drafts when browser history changes the URL", async () => {
    vi.mocked(api).mockResolvedValue({ items: [], total: 0, page: 1, limit: 25, pages: 1 });
    const view = render(<AdminAuditPanel />);
    await waitFor(() => expect(api).toHaveBeenCalledTimes(1));

    window.history.pushState(null, "", "/admin/audit?actor=owner%40example.test&action=user.suspended");
    view.rerender(<AdminAuditPanel />);

    await waitFor(() => {
      expect((screen.getByLabelText("操作者") as HTMLInputElement).value).toBe("owner@example.test");
      expect((screen.getByLabelText("動作") as HTMLInputElement).value).toBe("user.suspended");
    });

    window.history.replaceState(null, "", "/admin/audit");
    view.rerender(<AdminAuditPanel />);
    await waitFor(() => expect((screen.getByLabelText("操作者") as HTMLInputElement).value).toBe(""));
  });

  it("loads an older audit event directly when a shared deep link is outside the current page", async () => {
    const eventId = "00000000-0000-4000-8000-000000000099";
    window.history.replaceState(null, "", `/admin/audit?page=9&event=${eventId}`);
    vi.mocked(api).mockImplementation(async (path) => {
      if (String(path) === `/admin/audit/${eventId}`) {
        return {
          id: eventId,
          actor_email: "operator@example.test",
          action: "database.operation.succeeded",
          target: "fixture-operation",
          result: "succeeded",
          metadata: { status: "succeeded" },
          created_at: "2026-09-01T08:00:00Z",
        };
      }
      return { items: [], total: 201, page: 9, limit: 25, pages: 9 };
    });

    render(<AdminAuditPanel />);

    expect(await screen.findByRole("dialog", { name: "稽核事件" })).toBeTruthy();
    expect(await screen.findByText("database.operation.succeeded")).toBeTruthy();
    expect(screen.getByText("operator@example.test")).toBeTruthy();
    expect(vi.mocked(api).mock.calls.some(([path]) => path === `/admin/audit/${eventId}`)).toBe(true);
  });
});
