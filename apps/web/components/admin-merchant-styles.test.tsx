import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "@/lib/api";
import { AdminMerchantStyles } from "./admin-merchant-styles";

vi.mock("@/lib/api", () => ({ api: vi.fn() }));
const call = vi.mocked(api);
const review = { style: "instagrammable", status: "pending", evidence_url: "https://shop.example/design",
  evidence_title: "Branch design", rationale: "Floral greenhouse interior at this branch", checked_on: "2026-09-08",
  updated_at: "2026-09-08T00:00:00+00:00", reviewed_at: null };
async function open() {
  render(<AdminMerchantStyles merchantId="merchant-1" />);
  expect(call).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole("button", { name: "風格新增與審核" }));
  await waitFor(() => expect((screen.getByLabelText("來源標題") as HTMLInputElement).disabled).toBe(false));
}
describe("merchant style review", () => {
  beforeEach(() => { vi.resetAllMocks(); });
  it("loads evidence, retains drafts across styles and saves only the chosen review", async () => {
    call.mockResolvedValueOnce({ items: [review] }).mockResolvedValueOnce({ ...review, status: "approved" });
    await open();
    await screen.findByDisplayValue("Branch design");
    fireEvent.change(screen.getByLabelText("來源標題"), { target: { value: "Checked branch design" } });
    fireEvent.change(screen.getByLabelText("店家風格"), { target: { value: "artsy" } });
    expect((screen.getByLabelText("來源標題") as HTMLInputElement).value).toBe("");
    fireEvent.change(screen.getByLabelText("店家風格"), { target: { value: "instagrammable" } });
    expect((screen.getByLabelText("來源標題") as HTMLInputElement).value).toBe("Checked branch design");
    fireEvent.change(screen.getByLabelText("審核狀態"), { target: { value: "approved" } });
    const save = screen.getByRole("button", { name: "儲存此風格審核" }) as HTMLButtonElement;
    expect(save.disabled).toBe(true);
    fireEvent.change(screen.getByLabelText("本次審核原因"), { target: { value: "已比對此分店來源" } });
    fireEvent.click(save);
    expect(await screen.findByText("風格審核已儲存；店家發布狀態未變更。")).toBeTruthy();
    const options = call.mock.calls[1][1];
    const payload = JSON.parse(String(options?.body));
    expect(options?.method).toBe("PUT");
    expect(payload.expected_updated_at).toBe(review.updated_at);
    expect(payload.review.status).toBe("approved");
    expect(payload.review.evidence_title).toBe("Checked branch design");
    expect(payload.review).not.toHaveProperty("reviewed_at");
    expect(payload).not.toHaveProperty("is_active");
  });
  it("keeps failed loads disabled and allows retry", async () => {
    call.mockRejectedValueOnce(new Error("讀取失敗")).mockResolvedValueOnce({ items: [] });
    render(<AdminMerchantStyles merchantId="merchant-1" />);
    fireEvent.click(screen.getByRole("button", { name: "風格新增與審核" }));
    expect(await screen.findByRole("alert")).toHaveProperty("textContent", "讀取失敗");
    expect(screen.getByLabelText("來源標題").closest("fieldset")?.disabled).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "重新載入（捨棄草稿）" }));
    await waitFor(() => expect(screen.getByLabelText("來源標題").closest("fieldset")?.disabled).toBe(false));
  });
  it("shows save failures without discarding review input", async () => {
    call.mockResolvedValueOnce({ items: [review] }).mockRejectedValueOnce(new Error("資料已變更"));
    await open();
    await screen.findByDisplayValue("Branch design");
    fireEvent.change(screen.getByLabelText("本次審核原因"), { target: { value: "重新確認" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存此風格審核" }));
    expect(await screen.findByRole("alert")).toHaveProperty("textContent", "資料已變更");
    expect((screen.getByLabelText("本次審核原因") as HTMLInputElement).value).toBe("重新確認");
  });
});
