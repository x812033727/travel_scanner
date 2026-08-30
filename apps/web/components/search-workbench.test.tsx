import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { SearchWorkbench } from "./search-workbench";

const { push } = vi.hoisted(() => ({ push: vi.fn() }));

vi.mock("next/navigation", () => ({ useRouter: () => ({ push }) }));

describe("SearchWorkbench", () => {
  it("builds a complete Thailand family-search query", () => {
    render(<SearchWorkbench />);

    fireEvent.click(screen.getByRole("button", { name: /泰國/ }));
    fireEvent.click(screen.getByRole("button", { name: /^普吉/ }));
    fireEvent.change(screen.getByLabelText("兒童人數"), { target: { value: "2" } });
    fireEvent.change(screen.getByLabelText("第 2 位兒童年齡"), { target: { value: "12" } });
    fireEvent.click(screen.getByRole("button", { name: "海灘／跳島" }));
    fireEvent.click(screen.getByRole("button", { name: /比較完整旅程/ }));

    expect(push).toHaveBeenCalledOnce();
    const url = new URL(push.mock.calls[0][0], "https://travel.test");
    expect(url.pathname).toBe("/search");
    expect(url.searchParams.get("country")).toBe("TH");
    expect(url.searchParams.get("destination")).toBe("HKT");
    expect(url.searchParams.get("children_ages")).toBe("8,12");
    expect(url.searchParams.get("interests")).toContain("beach");
    expect(url.searchParams.get("preferred_area")).toBe("普吉老城");
  });
});
