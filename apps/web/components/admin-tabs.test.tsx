import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { AdminTabPanel, AdminTabs, useHashTab } from "./admin-tabs";

const keys = ["first", "second", "third"] as const;

function Harness() {
  const [active, select] = useHashTab(keys, "first");
  return (
    <>
      <AdminTabs
        idPrefix="demo"
        label="示範工作區"
        mobileLabel="選擇分頁"
        tabs={keys.map((key) => ({ key, label: `分頁 ${key}` }))}
        active={active}
        onSelect={select}
      />
      {keys.map((key) => (
        <AdminTabPanel key={key} idPrefix="demo" tabKey={key} active={active}>
          <p>內容 {key}</p>
        </AdminTabPanel>
      ))}
    </>
  );
}

function panelHidden(text: string) {
  return screen.getByText(text).closest("[role='tabpanel']")?.hasAttribute("hidden");
}

describe("AdminTabs", () => {
  afterEach(() => {
    window.history.replaceState(null, "", window.location.pathname);
  });

  it("opens the tab named in the hash and hides the other panels", () => {
    window.history.replaceState(null, "", "#second");
    render(<Harness />);
    expect(screen.getByRole("tab", { name: "分頁 second" }).getAttribute("aria-selected")).toBe("true");
    expect(panelHidden("內容 second")).toBe(false);
    expect(panelHidden("內容 first")).toBe(true);
    expect(panelHidden("內容 third")).toBe(true);
  });

  it("falls back to the default tab for unknown hashes", () => {
    window.history.replaceState(null, "", "#nope");
    render(<Harness />);
    expect(screen.getByRole("tab", { name: "分頁 first" }).getAttribute("aria-selected")).toBe("true");
    expect(panelHidden("內容 first")).toBe(false);
  });

  it("updates the hash when a tab is clicked or picked on mobile", () => {
    render(<Harness />);
    fireEvent.click(screen.getByRole("tab", { name: "分頁 third" }));
    expect(window.location.hash).toBe("#third");
    expect(panelHidden("內容 third")).toBe(false);
    expect(panelHidden("內容 first")).toBe(true);

    fireEvent.change(screen.getByLabelText("選擇分頁"), { target: { value: "second" } });
    expect(window.location.hash).toBe("#second");
    expect((screen.getByLabelText("選擇分頁") as HTMLSelectElement).value).toBe("second");
    expect(panelHidden("內容 second")).toBe(false);
  });

  it("moves between tabs with the keyboard", () => {
    render(<Harness />);
    fireEvent.keyDown(screen.getByRole("tab", { name: "分頁 first" }), { key: "ArrowRight" });
    expect(window.location.hash).toBe("#second");
    fireEvent.keyDown(screen.getByRole("tab", { name: "分頁 second" }), { key: "End" });
    expect(window.location.hash).toBe("#third");
    fireEvent.keyDown(screen.getByRole("tab", { name: "分頁 third" }), { key: "ArrowRight" });
    expect(window.location.hash).toBe("#first");
    fireEvent.keyDown(screen.getByRole("tab", { name: "分頁 first" }), { key: "ArrowLeft" });
    expect(window.location.hash).toBe("#third");
    fireEvent.keyDown(screen.getByRole("tab", { name: "分頁 third" }), { key: "Home" });
    expect(window.location.hash).toBe("#first");
    expect(screen.getByRole("tab", { name: "分頁 first" }).getAttribute("aria-selected")).toBe("true");
  });
});
