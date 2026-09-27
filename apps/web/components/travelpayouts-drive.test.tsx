import { act, render, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { resetThirdPartyAudience, setThirdPartyAudience } from "@/lib/third-party-audience";

const navigation = vi.hoisted(() => ({ pathname: "/zh-TW" }));
vi.mock("next/navigation", () => ({ usePathname: () => navigation.pathname }));
vi.mock("next/script", () => ({
  default: (props: Record<string, string>) => <script data-testid="drive-script" {...props} />,
}));

import { TravelpayoutsDrive } from "./travelpayouts-drive";
import { TRAVELPAYOUTS_DRIVE_SCRIPT_URL, isTravelpayoutsDriveOrigin } from "@/lib/travelpayouts-drive";

describe("TravelpayoutsDrive", () => {
  beforeEach(() => {
    // A signed-out reader, unless a case says otherwise.
    setThirdPartyAudience("allowed");
  });

  afterEach(() => {
    Object.defineProperty(navigator, "doNotTrack", { configurable: true, value: null });
    Object.defineProperty(navigator, "globalPrivacyControl", { configurable: true, value: undefined });
    navigation.pathname = "/zh-TW";
    resetThirdPartyAudience();
  });

  it("waits while the reader's role is unknown and never loads for an administrator", async () => {
    resetThirdPartyAudience();
    const { queryByTestId } = render(<TravelpayoutsDrive enabled />);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(queryByTestId("drive-script")).toBeNull();

    act(() => setThirdPartyAudience("blocked"));
    // Final for the document: a later "allowed" (signing out in place) does not let it in.
    act(() => setThirdPartyAudience("allowed"));
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(queryByTestId("drive-script")).toBeNull();
  });

  it("loads once a signed-in reader turns out not to be an administrator", async () => {
    resetThirdPartyAudience();
    const { getByTestId } = render(<TravelpayoutsDrive enabled />);
    act(() => setThirdPartyAudience("allowed"));
    await waitFor(() => getByTestId("drive-script"));
  });

  it("only enables the project script on Mokaair HTTPS production origins", () => {
    expect(isTravelpayoutsDriveOrigin("https://mokaair.com")).toBe(true);
    expect(isTravelpayoutsDriveOrigin("https://www.mokaair.com/path")).toBe(true);
    expect(isTravelpayoutsDriveOrigin("http://mokaair.com")).toBe(false);
    expect(isTravelpayoutsDriveOrigin("https://preview.mokaair.com")).toBe(false);
    expect(isTravelpayoutsDriveOrigin("not-a-url")).toBe(false);
  });

  it("loads the exact Travelpayouts project script with its required attributes", async () => {
    const { getByTestId } = render(<TravelpayoutsDrive enabled />);
    const script = await waitFor(() => getByTestId("drive-script"));
    expect(script.getAttribute("src")).toBe(TRAVELPAYOUTS_DRIVE_SCRIPT_URL);
    expect(script.getAttribute("data-cmp-ab")).toBe("2");
    expect(script.getAttribute("data-cfasync")).toBe("false");
    expect(script.getAttribute("data-no-defer")).toBe("1");
  });

  it("does not load when DNT or GPC is enabled", async () => {
    Object.defineProperty(navigator, "doNotTrack", { configurable: true, value: "1" });
    const { queryByTestId, rerender } = render(<TravelpayoutsDrive enabled />);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(queryByTestId("drive-script")).toBeNull();

    Object.defineProperty(navigator, "doNotTrack", { configurable: true, value: null });
    Object.defineProperty(navigator, "globalPrivacyControl", { configurable: true, value: true });
    rerender(<TravelpayoutsDrive enabled={false} />);
    rerender(<TravelpayoutsDrive enabled />);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(queryByTestId("drive-script")).toBeNull();
  });

  it.each([
    "/zh-TW/share/AbCdEfGhIjKlMnOpQrStUv",
    "/zh-TW/trips/550e8400-e29b-41d4-a716-446655440000",
    "/zh-TW/admin/users",
    "/en/login",
  ])("does not load on the private page %s", async (pathname) => {
    navigation.pathname = pathname;
    const { queryByTestId } = render(<TravelpayoutsDrive enabled />);
    await new Promise((resolve) => setTimeout(resolve, 0));
    expect(queryByTestId("drive-script")).toBeNull();
  });
});
