import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { SocialLoginButtons } from "./social-login-buttons";

afterEach(() => vi.unstubAllGlobals());

function stubProviders(providers: Partial<Record<"google" | "line" | "apple", boolean>>) {
  vi.stubGlobal("fetch", vi.fn(async () => new Response(
    JSON.stringify({ providers: { google: false, line: false, apple: false, ...providers } }),
    { status: 200, headers: { "content-type": "application/json" } },
  )));
}

describe("SocialLoginButtons", () => {
  it("offers only the providers the server reports as configured", async () => {
    stubProviders({ google: true, line: true });
    render(<SocialLoginButtons nextPath="/" />);

    expect(await screen.findByRole("link", { name: "使用 Google 繼續" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "使用 LINE 繼續" })).toBeTruthy();
    // Apple is implemented but needs a paid developer account, so it stays off
    // until it is configured; an unconfigured provider must not be offered.
    expect(screen.queryByRole("link", { name: "使用 Apple 繼續" })).toBeNull();
  });

  it("carries the intent, locale and return path into the start URL", async () => {
    stubProviders({ google: true });
    render(<SocialLoginButtons nextPath="/trips?sort=new" intent="link" />);

    const href = (await screen.findByRole("link", { name: "使用 Google 繼續" })).getAttribute("href");
    expect(href).toBe("/api/auth/oauth/google/start?intent=link&locale=zh-TW&next=%2Ftrips%3Fsort%3Dnew");
  });

  it("renders nothing but the email divider's absence when no provider is configured", async () => {
    stubProviders({});
    render(<SocialLoginButtons nextPath="/" />);

    // The placeholder must not harden into a permanent gap above the email form.
    await waitFor(() => expect(document.querySelector("[aria-hidden='true']")).toBeNull());
    expect(screen.queryByRole("link")).toBeNull();
    expect(screen.queryByText("或使用 Email")).toBeNull();
  });

  it("holds the space while the provider list is still unknown", () => {
    vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));
    const { container } = render(<SocialLoginButtons nextPath="/" />);

    expect(container.querySelector(".animate-pulse")).toBeTruthy();
  });

  it("survives a failed provider lookup instead of blocking the email form", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response("nope", { status: 503 })));
    const { container } = render(<SocialLoginButtons nextPath="/" />);

    await waitFor(() => expect(container.querySelector(".animate-pulse")).toBeNull());
    expect(screen.queryByRole("link")).toBeNull();
  });

  it("explains a known callback failure and falls back for an unknown one", async () => {
    stubProviders({ google: true });
    const known = render(<SocialLoginButtons nextPath="/" oauthError="oauth_account_exists" />);
    expect(screen.getByRole("alert").textContent).toContain("此 Email 已有會員");
    known.unmount();

    // A provider could return anything; an unrecognised code must not be shown raw.
    render(<SocialLoginButtons nextPath="/" oauthError="something-we-do-not-know" />);
    expect(screen.getByRole("alert").textContent).toBe("第三方身份驗證失敗，請稍後重試。");
  });
});
