import { describe, expect, it } from "vitest";
import { loginPath, safeNextPath } from "./navigation";

describe("safeNextPath", () => {
  it("keeps local routes and rejects protocol-relative or external routes", () => {
    expect(safeNextPath("/search?destination=NRT")).toBe("/search?destination=NRT");
    expect(safeNextPath("//evil.example/path")).toBe("/");
    expect(safeNextPath("/\\evil.example/path")).toBe("/");
    expect(safeNextPath("https://evil.example/path")).toBe("/");
    expect(loginPath("/alerts")).toBe("/login?next=%2Falerts");
  });
});
