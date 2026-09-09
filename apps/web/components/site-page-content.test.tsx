import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { SitePageContent } from "./site-page-content";
import type { SitePageDocument } from "@/lib/site-pages";

const labels = { operator: "Operator", location: "Location", contact: "Contact", retention: "Retention", legal: "Legal", effectiveDate: "Effective date" };
const document: SitePageDocument = { title: "Policy", description: "Description", effective_date: "2026-09-09", requirements: { operator: "Mokaair operator", location: "", contact: "", retention: "", legal: "" }, blocks: [{ type: "paragraph", text: "<script>alert(1)</script>" }, { type: "heading", level: 2, text: "Purpose" }, { type: "list", items: ["One", "Two"], ordered: true }, { type: "link", text: "Official contact", url: "https://example.com/contact" }] };
afterEach(cleanup);
describe("published page rendering", () => {
  it("renders structured content as text without executing markup", () => {
    const { container } = render(<SitePageContent document={document} labels={labels} />);
    expect(container.querySelector("script")).toBeNull();
    expect(screen.getByText("<script>alert(1)</script>")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Purpose", level: 2 })).toBeTruthy();
    expect(container.querySelector("ol")?.children).toHaveLength(2);
    expect(screen.getByText("Mokaair operator")).toBeTruthy();
    expect(screen.queryByText("Retention")).toBeNull();
    const link = screen.getByRole("link", { name: "Official contact" });
    expect(link.getAttribute("target")).toBe("_blank"); expect(link.getAttribute("rel")).toBe("noopener noreferrer");
  });
  it("omits unsafe links even if a malformed document is supplied", () => {
    render(<SitePageContent document={{ ...document, blocks: [{ type: "link", text: "Unsafe", url: "javascript:alert(1)" }] }} labels={labels} />);
    expect(screen.queryByRole("link")).toBeNull();
  });
});
