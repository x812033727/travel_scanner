import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { TEXT_SIZE_STORAGE_KEY } from "@/lib/text-size";
import { TextSizeSwitcher } from "./text-size-switcher";

beforeEach(() => {
  localStorage.clear();
  delete document.documentElement.dataset.textSize;
});

describe("TextSizeSwitcher", () => {
  it("restores and persists the stored size", async () => {
    localStorage.setItem(TEXT_SIZE_STORAGE_KEY, "large");
    render(<TextSizeSwitcher />);

    const select = screen.getByRole("combobox", { name: "文字大小" });
    await waitFor(() => expect((select as HTMLSelectElement).value).toBe("large"));

    fireEvent.change(select, { target: { value: "largest" } });
    expect(document.documentElement.dataset.textSize).toBe("largest");
    expect(localStorage.getItem(TEXT_SIZE_STORAGE_KEY)).toBe("largest");
  });

  it("offers the three sizes as buttons in the phone menu", async () => {
    render(<TextSizeSwitcher variant="expanded" />);

    const standard = screen.getByRole("radio", { name: "標準" });
    await waitFor(() => expect(standard.getAttribute("aria-checked")).toBe("true"));

    fireEvent.click(screen.getByRole("radio", { name: "特大" }));
    expect(document.documentElement.dataset.textSize).toBe("largest");
    expect(screen.getByRole("radio", { name: "特大" }).getAttribute("aria-checked")).toBe("true");
    expect(standard.getAttribute("aria-checked")).toBe("false");
  });

  it("keeps a second copy of the control in step", async () => {
    render(<><TextSizeSwitcher /><TextSizeSwitcher variant="expanded" /></>);
    await waitFor(() => expect(screen.getByRole("radio", { name: "標準" }).getAttribute("aria-checked")).toBe("true"));

    fireEvent.change(screen.getByRole("combobox", { name: "文字大小" }), { target: { value: "large" } });

    // The phone sheet and the desktop header both mount one; without the shared
    // event they would disagree about what the reader picked.
    await waitFor(() => expect(screen.getByRole("radio", { name: "大" }).getAttribute("aria-checked")).toBe("true"));
  });

  it("still applies the size when storage is unavailable", async () => {
    const original = Object.getOwnPropertyDescriptor(window, "localStorage");
    Object.defineProperty(window, "localStorage", {
      configurable: true,
      get() {
        throw new Error("blocked");
      },
    });
    try {
      render(<TextSizeSwitcher variant="expanded" />);
      await waitFor(() => expect(screen.getByRole("radio", { name: "標準" }).getAttribute("aria-checked")).toBe("true"));
      fireEvent.click(screen.getByRole("radio", { name: "大" }));
      expect(document.documentElement.dataset.textSize).toBe("large");
    } finally {
      if (original) Object.defineProperty(window, "localStorage", original);
    }
  });
});
