import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { LineLinkPanel } from "./line-link-panel";

vi.mock("@/i18n/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
  Link: ({ href, children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement> & { href: string }) => <a href={href} {...props}>{children}</a>,
}));

describe("LineLinkPanel", () => {
  it("gives an expired link a way out instead of one sentence", () => {
    render(<LineLinkPanel />);
    expect(screen.getByRole("alert").textContent).toContain("連結已失效");
    // The binding exists for price alerts, so that is where a stuck reader can go.
    expect(screen.getByRole("link", { name: "價格通知" }).getAttribute("href")).toBe("/alerts");
  });

  it("offers the sign-in path while a usable token is present", () => {
    render(<LineLinkPanel linkToken="abc123" />);
    expect(screen.getByRole("button", { name: "確認連結 LINE" })).toBeTruthy();
    expect(screen.getByRole("link", { name: /尚未登入/ }).getAttribute("href"))
      .toBe("/login?next=%2Fline%2Flink%3FlinkToken%3Dabc123");
  });
});
