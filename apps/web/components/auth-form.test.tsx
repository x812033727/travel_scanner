import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError } from "@/lib/api";
import { AuthForm } from "./auth-form";

const apiMock = vi.fn();
const pushMock = vi.fn();
const refreshMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});
vi.mock("@/i18n/navigation", () => ({ useRouter: () => ({ push: pushMock, refresh: refreshMock }) }));

describe("AuthForm", () => {
  beforeEach(() => { apiMock.mockReset(); pushMock.mockReset(); refreshMock.mockReset(); });

  it("keeps email, clears password and shows Chinese authentication errors", async () => {
    apiMock.mockRejectedValue(new ApiError("Email 或密碼不正確", 401, "invalid_credentials"));
    render(<AuthForm mode="login" nextPath="/search?destination=NRT" />);
    fireEvent.change(screen.getByLabelText("Email"), { target: { value: "traveler@example.com" } });
    fireEvent.change(screen.getByLabelText(/^密碼/), { target: { value: "wrong-password" } });
    fireEvent.click(screen.getByRole("button", { name: "登入" }));
    await screen.findByRole("alert");
    expect((screen.getByLabelText("Email") as HTMLInputElement).value).toBe("traveler@example.com");
    expect((screen.getByLabelText(/^密碼/) as HTMLInputElement).value).toBe("");
    expect(screen.getByText("Email 或密碼不正確")).toBeTruthy();
  });

  it("keeps all fields on service failures and returns to a safe local path", async () => {
    apiMock.mockRejectedValueOnce(new ApiError("服務暫時無法使用", 503));
    const { rerender } = render(<AuthForm mode="login" nextPath="//evil.example" />);
    fireEvent.change(screen.getByLabelText("Email"), { target: { value: "traveler@example.com" } });
    fireEvent.change(screen.getByLabelText(/^密碼/), { target: { value: "correct-password" } });
    fireEvent.click(screen.getByRole("button", { name: "登入" }));
    await screen.findByRole("alert");
    expect((screen.getByLabelText(/^密碼/) as HTMLInputElement).value).toBe("correct-password");
    apiMock.mockResolvedValueOnce({});
    rerender(<AuthForm mode="login" nextPath="//evil.example" />);
    fireEvent.click(screen.getByRole("button", { name: "登入" }));
    await waitFor(() => expect(pushMock).toHaveBeenCalledWith("/", { locale: "zh-TW" }));
  });
});
