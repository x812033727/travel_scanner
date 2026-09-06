import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import RegisterPage from "./page";

const registrationState = vi.hoisted(() => ({ value: "open" as "open" | "closed" | "unavailable" }));

vi.mock("@/lib/registration", () => ({
  getRegistrationAvailability: () => Promise.resolve(registrationState.value),
}));
vi.mock("@/lib/usage-catalog.server", () => ({
  getUsageCatalog: () => Promise.resolve({ status: "ready", catalog: { trial_uses: 7 } }),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => <header>Mokaair</header> }));
vi.mock("@/components/auth-form", () => ({
  AuthForm: ({ mode }: { mode: string }) => <form data-testid={`${mode}-form`} />,
}));

async function renderPage() {
  render(await RegisterPage({ searchParams: Promise.resolve({ next: "/trips" }), params: Promise.resolve({ locale: "zh-TW" }) }));
}

describe("registration page", () => {
  beforeEach(() => { registrationState.value = "open"; });

  it("shows the registration form when registration is open", async () => {
    await renderPage();
    expect(screen.getByRole("heading", { name: "建立你的旅行帳號" })).toBeTruthy();
    expect(screen.getByText("註冊免費取得 7 次")).toBeTruthy();
    expect(screen.getByTestId("register-form")).toBeTruthy();
  });

  it("shows a closed notice and login link without a form", async () => {
    registrationState.value = "closed";
    await renderPage();
    expect(screen.getByRole("heading", { name: "現在還不能建立新帳號" })).toBeTruthy();
    expect(screen.queryByTestId("register-form")).toBeNull();
    expect(screen.getByRole("link", { name: "前往登入" }).getAttribute("href")).toBe("/login?next=%2Ftrips");
  });

  it("fails closed when registration status cannot be confirmed", async () => {
    registrationState.value = "unavailable";
    await renderPage();
    expect(screen.getByRole("heading", { name: "暫時無法確認註冊狀態" })).toBeTruthy();
    expect(screen.queryByTestId("register-form")).toBeNull();
  });
});
