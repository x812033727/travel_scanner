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

  it("does not hold an existing member to the new-password rule", () => {
    apiMock.mockResolvedValue({ providers: {} });
    render(<AuthForm mode="login" nextPath="/" />);

    // A member whose password predates the ten-character rule got no message at all:
    // the browser refused to submit the form and the button looked like it did nothing.
    const password = screen.getByLabelText(/^密碼/) as HTMLInputElement;
    expect(password.hasAttribute("minlength")).toBe(false);
    expect(screen.queryByText("至少 10 個字元")).toBeNull();
  });

  it("states the length rule where it applies, on the register form", () => {
    apiMock.mockResolvedValue({ providers: {} });
    render(<AuthForm mode="register" nextPath="/" />);

    const password = screen.getByLabelText(/^密碼/) as HTMLInputElement;
    expect(password.getAttribute("minlength")).toBe("10");
    expect(screen.getByText("至少 10 個字元")).toBeTruthy();
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
