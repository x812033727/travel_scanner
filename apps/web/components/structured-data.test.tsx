import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { StructuredData } from "@/components/structured-data";

const html = (data: object | null | ReadonlyArray<object | null>) => renderToStaticMarkup(<StructuredData data={data} />);
const payload = (markup: string) => JSON.parse(markup.replace(/^<script[^>]*>/, "").replace(/<\/script>$/, ""));

describe("StructuredData", () => {
  it("emits a JSON-LD data block", () => {
    const markup = html({ "@type": "Organization" });
    expect(markup).toContain('type="application/ld+json"');
    expect(payload(markup)).toEqual({ "@type": "Organization" });
  });

  it("accepts a graph of several objects", () => {
    expect(payload(html([{ "@type": "Organization" }, { "@type": "WebSite" }]))).toHaveLength(2);
  });

  it("does not let a name containing a closing tag end the element", () => {
    // Merchant names, hotspot names and post titles all reach these graphs.
    const markup = html({ name: "Ramen </script><script>alert(1)</script>" });
    expect(markup.match(/<\/script>/g)).toHaveLength(1);
    expect(markup).not.toContain("<script>alert");
    expect(payload(markup).name).toBe("Ramen </script><script>alert(1)</script>");
  });
});

describe("StructuredData empty input", () => {
  it("renders nothing rather than a null graph", () => {
    expect(html(null)).toBe("");
    expect(html([])).toBe("");
    expect(html([null, null])).toBe("");
  });

  it("drops the nulls and keeps the rest", () => {
    expect(payload(html([null, { "@type": "WebSite" }]))).toEqual({ "@type": "WebSite" });
  });
});
