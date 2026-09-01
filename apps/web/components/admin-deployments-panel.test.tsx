import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminDeploymentsPanel } from "./admin-deployments-panel";

const sha = "b".repeat(40);
const run = { id: "run-1", requested_by_email: "deploy@example.com", status: "queued", stage: "queued", target_sha: sha, created_at: "2026-09-01T00:00:00Z", updated_at: "2026-09-01T00:00:00Z", events: [] };
const overview = { enabled: true, agent_connected: true, deployed_sha: "a".repeat(40), target_sha: sha, target_commit_subject: "Add deployment center", update_available: true, ci_status: "success", ci_url: "https://github.com/x812033727/travel_scanner/actions/runs/1", commits: [{ sha, subject: "Add deployment center" }], checks: [{ name: "docker", status: "ok", detail: "可用" }] };

function response(value: unknown, status = 200) {
  return Promise.resolve(new Response(JSON.stringify(value), { status, headers: { "Content-Type": "application/json" } }));
}

afterEach(() => vi.unstubAllGlobals());

describe("AdminDeploymentsPanel", () => {
  it("shows the green target and requires password plus exact SHA confirmation", async () => {
    const fetchMock = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/admin/deployments/overview")) return response(overview);
      if (url.includes("/admin/deployments?")) return response({ items: [] });
      if (url.endsWith("/admin/deployments") && init?.method === "POST") return response(run, 202);
      throw new Error(`unexpected ${url}`);
    });
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminDeploymentsPanel />);
    const deploy = await screen.findByRole("button", { name: "部署最新版本" });
    expect(screen.getAllByText("bbbbbbb").length).toBeGreaterThan(0);
    fireEvent.click(deploy);
    const submit = screen.getByRole("button", { name: "確認並開始部署" });
    expect((submit as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(screen.getByLabelText("目前密碼"), { target: { value: "correct password" } });
    fireEvent.change(screen.getByLabelText(/輸入 DEPLOY/), { target: { value: "DEPLOY bbbbbbb" } });
    expect((submit as HTMLButtonElement).disabled).toBe(false);
    fireEvent.click(submit);
    await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(
      "/api/travel/admin/deployments",
      expect.objectContaining({ method: "POST", headers: expect.objectContaining({ "Idempotency-Key": expect.stringMatching(/^deploy-/) }) }),
    ));
    const post = fetchMock.mock.calls.find(([, init]) => init?.method === "POST");
    expect(JSON.parse(String(post?.[1]?.body))).toEqual({ expected_target_sha: sha, password: "correct password", confirmation: "DEPLOY bbbbbbb" });
  });

  it("explains why deploy is disabled", async () => {
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL) => String(input).includes("overview") ? response({ ...overview, update_available: false, target_sha: overview.deployed_sha }) : response({ items: [] })));
    render(<AdminDeploymentsPanel />);
    expect(await screen.findByText("目前已是最新綠燈版本")).toBeTruthy();
    expect((screen.getByRole("button", { name: "部署最新版本" }) as HTMLButtonElement).disabled).toBe(true);
  });
});
