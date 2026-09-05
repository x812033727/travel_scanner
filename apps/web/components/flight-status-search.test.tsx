import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { FlightStatusSearch } from "./flight-status-search";

const { session } = vi.hoisted(() => ({
  session: { status: "authenticated" as "loading" | "authenticated" | "signed_out" | "unavailable" },
}));
vi.mock("@/i18n/navigation", () => ({
  usePathname: () => "/flights/status",
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => <a href={href} {...props}>{children}</a>,
}));
vi.mock("@/components/saved-items-provider", () => ({
  useSavedItems: () => ({ status: session.status, isSaved: () => false, setSaved: async () => undefined, toggle: async () => false }),
}));

afterEach(() => {
  session.status = "authenticated";
});

describe("FlightStatusSearch", () => {
  it("sends a visitor to sign in instead of showing a live charge button", () => {
    session.status = "signed_out";
    render(<FlightStatusSearch />);
    const link = screen.getByRole("link", { name: "登入後查詢 · 消耗 1 次" });
    expect(link.getAttribute("href")).toBe("/login?next=%2Fflights%2Fstatus");
    expect(screen.queryByRole("button", { name: /^查詢 · / })).toBeNull();
  });

  it("keeps the priced lookup button for a signed-in member", () => {
    render(<FlightStatusSearch />);
    expect(screen.getByRole("button", { name: "查詢 · 消耗 1 次" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: /登入後查詢/ })).toBeNull();
  });

  it("still shows the button when the session probe failed for another reason", () => {
    session.status = "unavailable";
    render(<FlightStatusSearch />);
    expect(screen.getByRole("button", { name: "查詢 · 消耗 1 次" })).toBeTruthy();
  });
});
