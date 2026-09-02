import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import LoginPage from "./page";

const registrationState = vi.hoisted(() => ({ value: "open" as "open" | "closed" | "unavailable" }));

vi.mock("@/lib/registration", () => ({
  getRegistrationAvailability: () => Promise.resolve(registrationState.value),
}));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => <header>Mokaair</header> }));
vi.mock("@/components/auth-form", () => ({
  AuthForm: ({ mode }: { mode: string }) => <form data-testid={`${mode}-form`} />,
}));

async function renderPage() {
  render(await LoginPage({ searchParams: Promise.resolve({ next: "/trips" }) }));
}

describe("login registration entry", () => {
  beforeEach(() => { registrationState.value = "open"; });

  it("links to free registration when open", async () => {
    await renderPage();
    expect(screen.getByRole("link", { name: "免費註冊" }).getAttribute("href")).toBe("/register?next=%2Ftrips");
  });

  it("replaces the registration link with a paused notice when closed", async () => {
    registrationState.value = "closed";
    await renderPage();
    expect(screen.getByText("目前暫停開放註冊")).toBeTruthy();
    expect(screen.queryByRole("link", { name: "免費註冊" })).toBeNull();
  });

  it("shows the unavailable state without exposing a registration link", async () => {
    registrationState.value = "unavailable";
    await renderPage();
    expect(screen.getByText("暫時無法確認註冊狀態")).toBeTruthy();
    expect(screen.queryByRole("link", { name: "免費註冊" })).toBeNull();
  });
});
