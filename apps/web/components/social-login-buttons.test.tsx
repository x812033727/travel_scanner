import { cleanup, render, screen, waitFor } from "@testing-library/react";
import { NextIntlClientProvider } from "next-intl";
import { afterEach, describe, expect, it, vi } from "vitest";
import { api } from "@/lib/api";
import en from "@/messages/en/auth.json";
import ja from "@/messages/ja/auth.json";
import ko from "@/messages/ko/auth.json";
import zhCN from "@/messages/zh-CN/auth.json";
import zhTW from "@/messages/zh-TW/auth.json";
import { SocialLoginButtons } from "./social-login-buttons";

vi.unmock("next-intl");
vi.mock("@/lib/api", () => ({ api: vi.fn() }));
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

const catalogs = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

function renderButtons(providers: { google: boolean; line: boolean; apple: boolean }, locale: keyof typeof catalogs = "zh-TW") {
  vi.mocked(api).mockResolvedValue({ providers });
  return render(
    <NextIntlClientProvider locale={locale} messages={{ auth: catalogs[locale] }} timeZone="UTC">
      <SocialLoginButtons nextPath="/" />
    </NextIntlClientProvider>,
  );
}

describe("SocialLoginButtons", () => {
  // LINE's email permission requires a screen that tells people their email is collected and why.
  it.each(Object.keys(catalogs) as Array<keyof typeof catalogs>)("tells %s readers what a social sign-in shares", async (locale) => {
    renderButtons({ google: true, line: true, apple: false }, locale);
    expect(await screen.findByText(catalogs[locale].socialEmailNotice)).toBeTruthy();
    expect(screen.getAllByRole("link").map((link) => link.textContent)).toEqual([
      expect.stringContaining(catalogs[locale].continueWith.google),
      expect.stringContaining(catalogs[locale].continueWith.line),
    ]);
  });

  it("stays silent when no provider is configured", async () => {
    renderButtons({ google: false, line: false, apple: false });
    await waitFor(() => expect(api).toHaveBeenCalledWith("/auth/oauth/providers"));
    expect(screen.queryByText(zhTW.socialEmailNotice)).toBeNull();
    expect(screen.queryByRole("link")).toBeNull();
  });
});
