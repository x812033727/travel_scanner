import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { addDays, formatTripDay, monthTitle, weekdayLabels } from "@/lib/calendar";
import newTrip from "@/messages/zh-TW/newTrip.json";
import { DateRangePicker, type DateRange } from "./date-range-picker";

const intl = vi.hoisted(() => ({ locale: "zh-TW" }));
vi.mock("next-intl", () => ({
  useLocale: () => intl.locale,
  useTranslations: (namespace: string) => (key: string, values?: Record<string, string | number>) => {
    let node: unknown = { newTrip };
    for (const part of [...namespace.split("."), ...key.split(".")]) {
      node = node && typeof node === "object" ? (node as Record<string, unknown>)[part] : undefined;
    }
    let text = typeof node === "string" ? node : key;
    for (const [name, replacement] of Object.entries(values || {})) text = text.replaceAll(`{${name}}`, String(replacement));
    return text;
  },
}));

const TODAY = "2026-09-05";

function Harness({ maxDays = 61 }: { maxDays?: number }) {
  const [range, setRange] = useState<DateRange>({ start: "", end: "" });
  return <>
    <DateRangePicker start={range.start} end={range.end} today={TODAY} maxDays={maxDays} onChange={setRange} />
    <p data-testid="range">{range.start}|{range.end}</p>
  </>;
}

function day(iso: string) {
  const button = document.querySelector<HTMLButtonElement>(`[data-date="${iso}"]`);
  if (!button) throw new Error(`day ${iso} is not rendered`);
  return button;
}

const rangeText = () => screen.getByTestId("range").textContent;
const statusText = () => screen.getByRole("status").textContent;
const gridNamed = (month: string) => screen.getByRole("grid", { name: monthTitle(intl.locale, month) });

describe("DateRangePicker", () => {
  afterEach(() => { intl.locale = "zh-TW"; vi.unstubAllGlobals(); });

  it("renders the current month with today marked and past days unavailable", () => {
    render(<Harness />);
    const headers = within(gridNamed("2026-09")).getAllByRole("columnheader");
    expect(headers).toHaveLength(7);
    expect(headers[0].textContent).toBe(weekdayLabels("zh-TW", 7)[0].short);
    expect(headers[0].getAttribute("abbr")).toBe(weekdayLabels("zh-TW", 7)[0].long);
    expect(document.querySelectorAll("[data-date]")).toHaveLength(30);
    expect(day("2026-09-05").getAttribute("aria-current")).toBe("date");
    expect(day("2026-09-04").getAttribute("aria-disabled")).toBe("true");
    expect(day("2026-09-05").getAttribute("aria-disabled")).toBeNull();
    expect(document.querySelectorAll('[data-date][tabindex="0"]')).toHaveLength(1);
    expect(day("2026-09-05").tabIndex).toBe(0);
    expect(statusText()).toBe("請先點選開始日期。");
    expect(screen.getByRole("button", { name: "上個月" }).hasAttribute("disabled")).toBe(true);
  });

  it("selects a continuous range with two taps", () => {
    render(<Harness />);
    fireEvent.click(day("2026-09-10"));
    expect(rangeText()).toBe("2026-09-10|");
    expect(statusText()).toBe(`再點選結束日期（最晚 ${formatTripDay("zh-TW", addDays("2026-09-10", 60))}）。`);
    fireEvent.click(day("2026-09-15"));
    expect(rangeText()).toBe("2026-09-10|2026-09-15");
    expect(day("2026-09-10").getAttribute("data-range")).toBe("edge");
    expect(day("2026-09-15").getAttribute("data-range")).toBe("edge");
    for (const iso of ["2026-09-11", "2026-09-12", "2026-09-13", "2026-09-14"]) {
      expect(day(iso).getAttribute("data-range")).toBe("inside");
      expect(day(iso).getAttribute("aria-pressed")).toBe("true");
    }
    expect(day("2026-09-16").getAttribute("aria-pressed")).toBe("false");
    expect(day("2026-09-16").getAttribute("data-range")).toBeNull();
    expect(statusText()).toBe(`${formatTripDay("zh-TW", "2026-09-10")} → ${formatTripDay("zh-TW", "2026-09-15")}・共 6 天`);
  });

  it("moves the start when an earlier day is tapped and restarts after a full range", () => {
    render(<Harness />);
    fireEvent.click(day("2026-09-15"));
    fireEvent.click(day("2026-09-10"));
    expect(rangeText()).toBe("2026-09-10|");
    fireEvent.click(day("2026-09-15"));
    expect(rangeText()).toBe("2026-09-10|2026-09-15");
    fireEvent.click(day("2026-09-20"));
    expect(rangeText()).toBe("2026-09-20|");
    expect(day("2026-09-12").getAttribute("aria-pressed")).toBe("false");
  });

  it("allows a one-day trip by tapping the same day twice", () => {
    render(<Harness />);
    fireEvent.click(day("2026-09-10"));
    fireEvent.click(day("2026-09-10"));
    expect(rangeText()).toBe("2026-09-10|2026-09-10");
    expect(statusText()).toContain("共 1 天");
  });

  it("keeps past days and days beyond the maximum length unavailable", () => {
    render(<Harness maxDays={3} />);
    fireEvent.click(day("2026-09-04"));
    expect(rangeText()).toBe("|");
    fireEvent.click(day("2026-09-10"));
    expect(statusText()).toBe(`再點選結束日期（最晚 ${formatTripDay("zh-TW", "2026-09-12")}）。`);
    expect(day("2026-09-13").getAttribute("aria-disabled")).toBe("true");
    expect(day("2026-09-12").getAttribute("aria-disabled")).toBeNull();
    expect(day("2026-09-08").getAttribute("aria-disabled")).toBeNull();
    fireEvent.click(day("2026-09-13"));
    expect(rangeText()).toBe("2026-09-10|");
    fireEvent.click(day("2026-09-12"));
    expect(rangeText()).toBe("2026-09-10|2026-09-12");
    expect(day("2026-09-13").getAttribute("aria-disabled")).toBeNull();
  });

  it("previews the range on hover without marking days as selected", () => {
    render(<Harness />);
    fireEvent.click(day("2026-09-10"));
    fireEvent.mouseEnter(day("2026-09-14"));
    for (const iso of ["2026-09-11", "2026-09-12", "2026-09-13", "2026-09-14"]) {
      expect(day(iso).getAttribute("data-range")).toBe("preview");
      expect(day(iso).getAttribute("aria-pressed")).toBe("false");
    }
    fireEvent.mouseLeave(screen.getByRole("grid"));
    expect(day("2026-09-12").getAttribute("data-range")).toBeNull();
    fireEvent.mouseEnter(day("2026-09-08"));
    expect(day("2026-09-09").getAttribute("data-range")).toBeNull();
    fireEvent.click(day("2026-09-14"));
    fireEvent.mouseEnter(day("2026-09-20"));
    expect(day("2026-09-18").getAttribute("data-range")).toBeNull();
  });

  it("navigates months and never goes before the current month", () => {
    render(<Harness />);
    const previous = screen.getByRole("button", { name: "上個月" });
    const next = screen.getByRole("button", { name: "下個月" });
    expect(previous.hasAttribute("disabled")).toBe(true);
    fireEvent.click(next);
    expect(gridNamed("2026-10")).toBeTruthy();
    expect(previous.hasAttribute("disabled")).toBe(false);
    fireEvent.click(previous);
    expect(gridNamed("2026-09")).toBeTruthy();
    expect(previous.hasAttribute("disabled")).toBe(true);
  });

  it("moves focus with the keyboard across month boundaries", () => {
    render(<Harness />);
    day("2026-09-30").focus();
    fireEvent.keyDown(day("2026-09-30"), { key: "ArrowRight" });
    expect(gridNamed("2026-10")).toBeTruthy();
    expect(document.activeElement).toBe(day("2026-10-01"));
    expect(day("2026-10-01").tabIndex).toBe(0);
    fireEvent.keyDown(day("2026-10-01"), { key: "ArrowUp" });
    expect(gridNamed("2026-09")).toBeTruthy();
    expect(document.activeElement).toBe(day("2026-09-24"));
    fireEvent.keyDown(day("2026-09-24"), { key: "Home" });
    expect(document.activeElement).toBe(day("2026-09-20"));
    fireEvent.keyDown(day("2026-09-20"), { key: "End" });
    expect(document.activeElement).toBe(day("2026-09-26"));
    fireEvent.keyDown(day("2026-09-26"), { key: "PageDown" });
    expect(document.activeElement).toBe(day("2026-10-26"));
    fireEvent.keyDown(day("2026-10-26"), { key: "PageUp" });
    expect(document.activeElement).toBe(day("2026-09-26"));
    day("2026-09-01").focus();
    fireEvent.keyDown(day("2026-09-01"), { key: "ArrowLeft" });
    expect(document.activeElement).toBe(day("2026-09-01"));
    expect(gridNamed("2026-09")).toBeTruthy();
  });

  it("previews the range from the focused day while choosing the end", () => {
    render(<Harness />);
    fireEvent.click(day("2026-09-10"));
    day("2026-09-10").focus();
    fireEvent.keyDown(day("2026-09-10"), { key: "ArrowDown" });
    expect(document.activeElement).toBe(day("2026-09-17"));
    for (const iso of ["2026-09-11", "2026-09-17"]) expect(day(iso).getAttribute("data-range")).toBe("preview");
    expect(day("2026-09-18").getAttribute("data-range")).toBeNull();
    fireEvent.keyDown(day("2026-09-17"), { key: "Enter" });
    fireEvent.click(day("2026-09-17"));
    expect(rangeText()).toBe("2026-09-10|2026-09-17");
  });

  it("reports the selection and clears it without leaving the month", () => {
    render(<Harness />);
    const clear = screen.getByRole("button", { name: "清除日期" });
    expect(clear.hasAttribute("disabled")).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "下個月" }));
    fireEvent.click(day("2026-10-10"));
    fireEvent.click(day("2026-10-12"));
    expect(clear.hasAttribute("disabled")).toBe(false);
    fireEvent.click(clear);
    expect(rangeText()).toBe("|");
    expect(statusText()).toBe("請先點選開始日期。");
    expect(gridNamed("2026-10")).toBeTruthy();
  });

  it("follows a start date that arrives after mount", () => {
    const noop = () => undefined;
    const { rerender } = render(<DateRangePicker start="" end="" today={TODAY} maxDays={61} onChange={noop} />);
    expect(gridNamed("2026-09")).toBeTruthy();
    rerender(<DateRangePicker start="2026-12-02" end="2026-12-05" today={TODAY} maxDays={61} onChange={noop} />);
    expect(gridNamed("2026-12")).toBeTruthy();
    expect(day("2026-12-02").getAttribute("data-range")).toBe("edge");
    expect(day("2026-12-03").getAttribute("data-range")).toBe("inside");
  });

  it("labels the calendar in the active locale and starts the week on the locale's day", () => {
    intl.locale = "en";
    const english = render(<Harness />);
    expect(screen.getByRole("grid", { name: "September 2026" })).toBeTruthy();
    expect(within(screen.getByRole("grid")).getAllByRole("columnheader")[0].textContent).toBe(weekdayLabels("en", 7)[0].short);
    expect(day("2026-09-10").getAttribute("aria-label")).toBe(formatTripDay("en", "2026-09-10"));
    english.unmount();

    intl.locale = "zh-CN";
    render(<Harness />);
    expect(screen.getByRole("grid", { name: monthTitle("zh-CN", "2026-09") })).toBeTruthy();
    expect(within(screen.getByRole("grid")).getAllByRole("columnheader")[0].textContent).toBe(weekdayLabels("zh-CN", 1)[0].short);
    expect(document.querySelectorAll("[data-date]")).toHaveLength(30);
  });
  it("marks a public holiday, names it in the day's label and shows the source", async () => {
    const calendar = (country: string) => ({
      country,
      country_name: country === "JP" ? "日本" : country,
      locale: "zh-TW",
      coverage_start: "2026-01-01",
      coverage_end: "2027-12-31",
      attribution: country === "JP" ? "出典：内閣府ウェブサイト" : "",
      holidays: country === "JP"
        ? [{ date: "2026-09-22", key: "jp_citizens_holiday", kind: "bridge_holiday", is_working_day: false, name: "國民假日", country, country_name: "日本", source: "cao_go_jp" }]
        : [],
    });
    vi.stubGlobal("fetch", vi.fn((input: unknown) => {
      const country = new URL(String(input), "http://test").searchParams.get("country") || "TW";
      return Promise.resolve(new Response(JSON.stringify(calendar(country)), { status: 200, headers: { "Content-Type": "application/json" } }));
    }));
    render(<Harness />);

    await waitFor(() => expect(day("2026-09-22").getAttribute("data-holiday")).toBe("true"));
    expect(day("2026-09-22").getAttribute("aria-label")).toBe(`${formatTripDay("zh-TW", "2026-09-22")} 日本 國民假日`);
    expect(day("2026-09-21").getAttribute("data-holiday")).toBeNull();
    expect(day("2026-09-21").getAttribute("aria-label")).toBe(formatTripDay("zh-TW", "2026-09-21"));
    expect(screen.getByText("出典：内閣府ウェブサイト")).toBeTruthy();
  });
});
