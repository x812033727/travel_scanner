import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { api } from "@/lib/api";
import { AdminDatabasePanel } from "./admin-database-panel";

vi.mock("@/lib/api", () => ({ api: vi.fn() }));

afterEach(() => vi.clearAllMocks());

describe("AdminDatabasePanel", () => {
  it("renders an unavailable snapshot without dereferencing nullable database fields", async () => {
    vi.mocked(api).mockImplementation(async (path) => {
      if (path === "/admin/database/overview") return { status: "unavailable", checked_at: "2026-09-09T00:00:00Z", postgres: null, schema_info: null, agent: null, active_operation: null, maintenance_enabled: false, retention_count: 7 };
      return { items: [] };
    });
    render(<AdminDatabasePanel />);
    expect((await screen.findAllByText("不可用")).length).toBeGreaterThan(0);
    expect(screen.getByText("0 / 0")).toBeTruthy();
  });

  it("uses schema_info, maximum connections, and persisted top-level operation state", async () => {
    vi.mocked(api).mockImplementation(async (path) => {
      if (path === "/admin/database/overview") return {
        status: "ok", checked_at: "2026-09-09T00:00:00Z",
        postgres: { version: "PostgreSQL 17", database_size_bytes: 1024, connections: { active: 3, idle: 2, waiting: 1, maximum: 40 }, long_transactions: 0, lock_waits: 0, cache_hit_ratio: 0.99 },
        schema_info: { current_revision: "0068_admin_operations_center", expected_revision: "0068_admin_operations_center", is_current: true },
        agent: { connected: true, available: true },
        active_operation: { id: "op-1", operation_type: "backup", status: "succeeded", created_at: "2026-09-09T00:00:00Z", updated_at: "2026-09-09T00:00:01Z" },
        maintenance_enabled: true, retention_count: 7,
      };
      if (path === "/admin/database/tables") return { items: [{ name: "users", estimated_rows: 12, data_bytes: 100, index_bytes: 20, total_bytes: 120, dead_rows: 1, last_autovacuum: "2026-09-08T00:00:00Z", last_autoanalyze: "2026-09-08T01:00:00Z" }] };
      return { items: [] };
    });
    render(<AdminDatabasePanel />);
    await waitFor(() => expect(api).toHaveBeenCalledTimes(3));
    expect(screen.getByText("PostgreSQL 17")).toBeTruthy();
    expect(screen.getByText("3 / 40")).toBeTruthy();
    expect(screen.getByText("0.99%")).toBeTruthy();
    expect(screen.getByText("0068_admin_operations_center")).toBeTruthy();
    expect(screen.getByRole("columnheader", { name: "最近 Vacuum" })).toBeTruthy();
  });

  it("keeps a usable overview when a secondary database section fails", async () => {
    vi.mocked(api).mockImplementation(async (path) => {
      if (path === "/admin/database/overview") return {
        status: "ok", checked_at: "2026-09-09T00:00:00Z",
        postgres: { version: "PostgreSQL 17", database_size_bytes: 2048, connections: { active: 1, maximum: 20 }, cache_hit_ratio: 0.75 },
        schema_info: { current_revision: "0068_admin_operations_center", expected_revision: "0068_admin_operations_center", is_current: true },
        agent: { connected: true, available: true }, active_operation: null, maintenance_enabled: true, retention_count: 7,
      };
      if (path === "/admin/database/tables") throw new Error("tables offline");
      return { items: [] };
    });
    render(<AdminDatabasePanel />);
    expect(await screen.findByText("PostgreSQL 17")).toBeTruthy();
    expect(screen.getByText("0.75%")).toBeTruthy();
    expect(screen.getByText("tables offline")).toBeTruthy();
  });
});
