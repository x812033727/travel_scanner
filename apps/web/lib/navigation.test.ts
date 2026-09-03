import { describe, expect, it } from "vitest";
import { loginPath, safeExternalHref, safeNextPath } from "./navigation";

describe("safeNextPath", () => {
  it("keeps local routes and rejects protocol-relative or external routes", () => {
    expect(safeNextPath("/search?destination=NRT")).toBe("/search?destination=NRT");
    expect(safeNextPath("//evil.example/path")).toBe("/");
    expect(safeNextPath("/\\evil.example/path")).toBe("/");
    expect(safeNextPath("https://evil.example/path")).toBe("/");
    expect(loginPath("/alerts")).toBe("/login?next=%2Falerts");
  });
});

describe("safeExternalHref", () => {
  it("passes ordinary web links through unchanged", () => {
    expect(safeExternalHref("https://www.booking.com/hotel?id=1")).toBe("https://www.booking.com/hotel?id=1");
    expect(safeExternalHref("http://example.com/")).toBe("http://example.com/");
  });

  it("drops script, data, relative, and malformed values", () => {
    expect(safeExternalHref("javascript:alert(1)")).toBeUndefined();
    expect(safeExternalHref("JaVaScRiPt:alert(1)")).toBeUndefined();
    expect(safeExternalHref("data:text/html,<script>")).toBeUndefined();
    expect(safeExternalHref("/relative/path")).toBeUndefined();
    expect(safeExternalHref("not a url")).toBeUndefined();
    expect(safeExternalHref(null)).toBeUndefined();
    expect(safeExternalHref(undefined)).toBeUndefined();
  });

  it("only allows custom app schemes when the caller opts in", () => {
    expect(safeExternalHref("nmap://route/car?dlat=37.5")).toBeUndefined();
    expect(safeExternalHref("nmap://route/car?dlat=37.5", ["nmap:"])).toBe("nmap://route/car?dlat=37.5");
    expect(safeExternalHref("javascript:alert(1)", ["nmap:"])).toBeUndefined();
  });
});
