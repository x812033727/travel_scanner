import { render, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { resetThirdPartyAudience, useThirdPartyAudience } from "@/lib/third-party-audience";

const session = vi.hoisted(() => ({
  value: { status: "loading", user: null } as { status: string; user: { is_admin?: boolean } | null },
}));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => session.value }));

import { ThirdPartyAudience } from "./third-party-audience";

describe("ThirdPartyAudience", () => {
  afterEach(() => {
    resetThirdPartyAudience();
    session.value = { status: "loading", user: null };
  });

  function audience() {
    return renderHook(() => useThirdPartyAudience()).result.current;
  }

  it.each([
    ["loading", null, "pending"],
    ["unavailable", null, "pending"],
    ["signed_out", null, "allowed"],
    ["authenticated", { is_admin: false }, "allowed"],
    ["authenticated", {}, "allowed"],
    ["authenticated", { is_admin: true }, "blocked"],
  ])("a %s reader %j is %s", (status, user, expected) => {
    session.value = { status, user };
    render(<ThirdPartyAudience />);
    expect(audience()).toBe(expected);
  });

  it("blocks a document that cannot ask who the signed-in reader is", () => {
    session.value = { status: "signed_out", user: null };
    render(<ThirdPartyAudience unknownRole />);
    expect(audience()).toBe("blocked");
  });

  it("keeps an administrator's document blocked after signing out in place", () => {
    session.value = { status: "authenticated", user: { is_admin: true } };
    const first = render(<ThirdPartyAudience />);
    expect(audience()).toBe("blocked");
    // Signing out remounts the session provider, and this component with it.
    first.unmount();
    session.value = { status: "signed_out", user: null };
    render(<ThirdPartyAudience />);
    expect(audience()).toBe("blocked");
  });
});
