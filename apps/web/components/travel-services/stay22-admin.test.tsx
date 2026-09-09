import { afterEach, expect, it, vi } from "vitest";
import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { ApiError } from "@/lib/api";
import { Stay22Admin, Stay22ReadinessPanel, stay22Default, type Stay22Config } from "./stay22-admin";

const { request } = vi.hoisted(() => ({ request: vi.fn() }));
vi.mock("next-intl", () => ({ useLocale: () => "zh-TW" }));
vi.mock("@/lib/api", async (original) => ({ ...(await original<typeof import("@/lib/api")>()), api: request }));
vi.mock("@/i18n/navigation", () => ({ Link: (props: React.AnchorHTMLAttributes<HTMLAnchorElement>) => <a {...props} /> }));
afterEach(() => { cleanup(); vi.clearAllMocks(); });

it("is default-off, separates tracking verification, and respects backend capability", () => {
  render(<Stay22Admin version={1} allowed={false} onSaved={vi.fn()} />);
  expect(screen.getByLabelText("Stay22 AID")).toHaveValue("mokaair");
  expect(screen.getByLabelText("啟用 Allez 直達分潤")).not.toBeChecked();
  expect(screen.getByLabelText("啟用 Allez 直達分潤")).toBeDisabled();
  expect(screen.getByRole("button", { name: "儲存 Stay22 設定" })).toBeDisabled();
  expect(screen.getByText(/設定完成不代表分潤追蹤已驗證/)).toBeVisible();
  expect(screen.getByText(/需要系統設定管理權限/)).toBeVisible();
  expect(request).not.toHaveBeenCalled();
});

it("saves only Stay22 fields using captured version and never makes a probe", async () => {
  request.mockResolvedValue({ version: 9 });
  const saved = vi.fn().mockResolvedValue(undefined);
  render(<Stay22Admin version={8} allowed onSaved={saved} />);
  fireEvent.click(screen.getByLabelText("啟用 Allez 直達分潤"));
  fireEvent.click(screen.getByLabelText("Booking.com"));
  fireEvent.click(screen.getByRole("button", { name: "儲存 Stay22 設定" }));
  await waitFor(() => expect(saved).toHaveBeenCalledOnce());
  expect(request).toHaveBeenCalledTimes(1);
  expect(request.mock.calls[0][0]).toBe("/admin/hotels/config");
  expect(JSON.parse(request.mock.calls[0][1].body)).toEqual({ version: 8, stay22: { enabled: true, aid: "mokaair", enabled_providers: ["booking"] } });
  expect(screen.getByRole("status")).toHaveTextContent("Stay22 設定已儲存");
});

it("keeps a dirty form and original version when another form refreshes config", async () => {
  request.mockRejectedValue(new ApiError("conflict", 409, "service_version_conflict"));
  const saved = vi.fn();
  const initial = render(<Stay22Admin version={2} allowed value={stay22Default} onSaved={saved} />);
  fireEvent.change(screen.getByLabelText("Stay22 AID"), { target: { value: "my-campaign" } });
  initial.rerender(<Stay22Admin version={3} allowed value={{ ...stay22Default, aid: "someone-else" }} onSaved={saved} />);
  expect(screen.getByLabelText("Stay22 AID")).toHaveValue("my-campaign");
  fireEvent.click(screen.getByRole("button", { name: "儲存 Stay22 設定" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("你的輸入已保留");
  expect(JSON.parse(request.mock.calls[0][1].body).version).toBe(2);
  expect(screen.getByLabelText("Stay22 AID")).toHaveValue("my-campaign");
  expect(saved).not.toHaveBeenCalled();
});

it("preserves input on service failure and validates enabled platform before requesting", async () => {
  request.mockRejectedValue(new ApiError("down", 503));
  render(<Stay22Admin version={1} allowed onSaved={vi.fn()} />);
  fireEvent.click(screen.getByLabelText("啟用 Allez 直達分潤"));
  fireEvent.click(screen.getByRole("button", { name: "儲存 Stay22 設定" }));
  expect(screen.getByRole("alert")).toHaveTextContent("至少選擇一個平台");
  expect(request).not.toHaveBeenCalled();
  fireEvent.click(screen.getByLabelText("Agoda"));
  fireEvent.click(screen.getByRole("button", { name: "儲存 Stay22 設定" }));
  await waitFor(() => expect(screen.getByRole("alert")).toHaveTextContent("設定內容已保留"));
  expect(screen.getByLabelText("Agoda")).toBeChecked();
});

it("updates clean form after config reload", () => {
  const view = render(<Stay22Admin version={1} allowed onSaved={vi.fn()} />);
  const value: Stay22Config = { enabled: true, aid: "new-aid", enabled_providers: ["expedia"] };
  view.rerender(<Stay22Admin version={2} allowed value={value} onSaved={vi.fn()} />);
  expect(screen.getByLabelText("Stay22 AID")).toHaveValue("new-aid");
  expect(screen.getByLabelText("Expedia")).toBeChecked();
});

it("links readiness counts to real provider and state filters", () => {
  render(<Stay22ReadinessPanel rows={[{ provider: "booking", existing_affiliate: 1, stay22_capable: 3, missing_link: 2, review_expired: 4, blocked: 5 }]} provider="booking" readiness="missing_link" />);
  expect(screen.getByRole("link", { name: "Booking.com · Stay22 可接: 3" })).toHaveAttribute("href", "/admin/hotels?tab=review&section=platforms&booking_provider=booking&booking_readiness=stay22_capable");
  expect(screen.getByRole("link", { name: "清除平台篩選" })).toHaveAttribute("href", "/admin/hotels?tab=review&section=platforms");
  expect(screen.getByText(/不是已驗證訂單或佣金/)).toBeVisible();
});

it("keeps the destination and status scope in readiness links", () => {
  render(<Stay22ReadinessPanel rows={[{ provider: "agoda", existing_affiliate: 0, stay22_capable: 2, missing_link: 0, review_expired: 0, blocked: 0 }]} destination="tokyo" status="approved" />);
  expect(screen.getByRole("link", { name: "Agoda · Stay22 可接: 2" })).toHaveAttribute("href", "/admin/hotels?tab=review&section=platforms&booking_provider=agoda&booking_readiness=stay22_capable&destination_id=tokyo&status=approved");
});
