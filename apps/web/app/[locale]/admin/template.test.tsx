import { render, screen } from "@testing-library/react";
import type { AnchorHTMLAttributes, ReactNode } from "react";
import { describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "@/components/admin-operations-provider";
import type { AdminBootstrap } from "@/lib/admin-operations";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";
import AdminTemplate from "./template";

const route = vi.hoisted(() => ({ pathname: "/admin" }));
vi.mock("@/i18n/navigation", () => ({
  Link: ({ href, children, ...props }: AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => <a href={href} {...props}>{children}</a>,
  usePathname: () => route.pathname,
}));

const copy = adminOperationsCopy("zh-TW");
const support: AdminBootstrap = {
  admin_roles: ["support"],
  admin_capabilities: ["admin.access", "dashboard.read", "users.read"],
  navigation: [
    { key: "dashboard", href: "/admin", group: "overview" },
    { key: "users", href: "/admin/users", group: "operations" },
  ],
  pending_counts: {},
  system_status: {},
  environment: "test",
  can_deploy: false,
  can_manage_database: false,
};

function Tree({ bootstrap = support, children }: { bootstrap?: AdminBootstrap; children: ReactNode }) {
  return <AdminOperationsProvider bootstrap={bootstrap}><AdminTemplate>{children}</AdminTemplate></AdminOperationsProvider>;
}

describe("admin template", () => {
  it("renders the pages the role's navigation lists", () => {
    route.pathname = "/admin/users/member-id";
    render(<Tree><p>Member detail</p></Tree>);
    expect(screen.getByText("Member detail")).toBeTruthy();
    expect(screen.queryByRole("heading", { name: copy.forbiddenTitle })).toBeNull();
  });

  it("refuses a page outside the role after a soft navigation the layout does not see", () => {
    // Next keeps admin/layout.tsx mounted across a client-side navigation, so its full-load
    // check never runs for the second path. Only this re-render does.
    route.pathname = "/admin/users";
    const view = render(<Tree><p>Users</p></Tree>);
    expect(screen.getByText("Users")).toBeTruthy();

    route.pathname = "/admin/hotspots";
    view.rerender(<Tree><p>Hotspot review</p></Tree>);
    expect(screen.queryByText("Hotspot review")).toBeNull();
    expect(screen.getByRole("heading", { name: copy.forbiddenTitle })).toBeTruthy();
  });
});
