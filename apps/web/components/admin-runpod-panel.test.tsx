import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminRunpodPanel, type RunpodPod } from "./admin-runpod-panel";

const ENDPOINT = "/api/travel/admin/provider-settings/runpod/sessions";
const pod: RunpodPod = {
  session_id: "5f0f3b2e-0000-4000-8000-000000000001",
  pod_id: "pod123",
  label: "e031 pilot",
  slug: "zhong-tian-e031",
  gpu: "NVIDIA RTX 6000 Ada Generation",
  cloud_type: "SECURE",
  data_center_id: "EU-RO-1",
  cost_per_hr: "1.0300",
  started_at: "2026-10-30T02:30:00Z",
  last_heartbeat_at: "2026-10-30T02:59:00Z",
  stopped_at: null,
  stop_reason: null,
  usd: "0.5150",
  token_prefix: "mkv_abcd",
};

function json(value: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(value), { status, headers: { "Content-Type": "application/json" } }));
}

describe("AdminRunpodPanel", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("shows the running pod and the month against the cap, and stops only after a second click", async () => {
    const calls: string[] = [];
    let stopped = false;
    vi.stubGlobal("fetch", vi.fn((url: string, init?: RequestInit) => {
      expect(url).toContain(ENDPOINT);
      calls.push(`${init?.method ?? "GET"} ${url}`);
      if (init?.method === "POST") {
        stopped = true;
        return json({ ...pod, stopped_at: "2026-10-30T03:00:00Z", stop_reason: "manual" });
      }
      return json({
        running: stopped ? [] : [pod],
        recent: stopped ? [{ ...pod, stopped_at: "2026-10-30T03:00:00Z", stop_reason: "manual" }] : [],
        month_usd: "12.5000",
        monthly_usd_cap: 50,
        configured: true,
      });
    }));
    render(<AdminRunpodPanel canManage />);
    expect(await screen.findByTestId("runpod-running")).toBeTruthy();
    expect(screen.getByRole("meter").getAttribute("aria-valuenow")).toBe("12.5");
    expect(document.body.textContent).toContain("US$12.50");
    expect(document.body.textContent).toContain("US$1.03/h");

    fireEvent.click(screen.getByRole("button", { name: /停止|stop/i }));
    expect(calls.some((call) => call.startsWith("POST"))).toBe(false);
    fireEvent.click(screen.getByRole("button", { name: /確定停止|stop this pod/i }));
    await waitFor(() => expect(calls).toContain(`POST ${ENDPOINT}/${pod.session_id}/stop`));
    await waitFor(() => expect(screen.queryByTestId("runpod-running")).toBeNull());
  });

  it("has no stop button for a settings viewer and warns while the card is incomplete", async () => {
    vi.stubGlobal("fetch", vi.fn(() => json({ running: [pod], recent: [], month_usd: "0", monthly_usd_cap: 50, configured: false })));
    render(<AdminRunpodPanel canManage={false} />);
    expect(await screen.findByTestId("runpod-running")).toBeTruthy();
    expect(screen.queryByRole("button")).toBeNull();
    expect(document.body.textContent).toMatch(/還沒填完|not filled in/);
  });
});
