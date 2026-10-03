import { describe, expect, it } from "vitest";
import { fareLabCopy, fareLabText, fareLabWarnings } from "./fare-lab-copy";

const LOCALES = ["en", "zh-TW", "zh-CN", "ja", "ko"];

describe("fare lab copy", () => {
  it.each(LOCALES)("has every key, nonempty, with the same placeholders as en in %s", (locale) => {
    const reference = fareLabCopy("en");
    const copy = fareLabCopy(locale);
    expect(Object.keys(copy).sort()).toEqual(Object.keys(reference).sort());
    for (const key of Object.keys(reference) as (keyof typeof reference)[]) {
      expect(copy[key].trim().length, key).toBeGreaterThan(0);
      expect((copy[key].match(/\{\w+\}/g) || []).sort(), key).toEqual((reference[key].match(/\{\w+\}/g) || []).sort());
    }
  });

  it("falls back to English and leaves a placeholder it was not given", () => {
    expect(fareLabCopy("unknown")).toEqual(fareLabCopy("en"));
    expect(fareLabText("{a} and {b}", { a: 1 })).toBe("1 and {b}");
  });
});

describe("fare lab warnings", () => {
  // What the API writes since 2026-09-11-fare-lab-warnings-and-copy; see
  // apps/api/app/crawlers/back_to_back.py and app/providers/live_back_to_back.py.
  const cached = [
    "fare_page_unavailable?airline=CI&page=reverse&reason=source_unavailable",
    "fare_not_cached_nearest?airline=JX&flex_days=7&nearest=2026-12-12%E2%80%932026-12-17&role=conventional_second",
    "stale_exchange_rate?currency=JPY",
    "open_jaw_baseline_only",
  ];

  it("names the airline, page and ticket in the reader's language", () => {
    expect(fareLabWarnings(cached, fareLabCopy("zh-TW"), "ticketRole")).toEqual([
      "中華航空 外站始發：票價頁暫時無法讀取。",
      "星宇航空：第二趟一般票在指定日期前後 7 天內沒有公開快取票價；公開頁最接近的是 2026-12-12–2026-12-17",
      "JPY 使用七日內的舊匯率估算 TWD。",
      "兩次目的地不同：完整倒買比較需要開口票票價來源；目前只顯示可驗證的一般買法基準。",
    ]);
    expect(fareLabWarnings(cached.slice(0, 2), fareLabCopy("en"), "ticketRole")).toEqual([
      "China Airlines from abroad: the fare page cannot be read right now.",
      "STARLUX Airlines: Second-trip regular ticket — no cached public fare within 7 days of the chosen dates; the nearest on the public page is 2026-12-12–2026-12-17",
    ]);
  });

  it("uses the live comparison's own ticket names", () => {
    const live = ["live_fare_failed?role=middle_two_segment", "live_fare_missing?role=conventional_first"];
    expect(fareLabWarnings(live, fareLabCopy("zh-TW"), "liveRole")).toEqual([
      "外站始發兩段票：即時票價查詢失敗",
      "第一趟一般來回：沒有可用即時票價",
    ]);
    expect(fareLabWarnings(live, fareLabCopy("ja"), "liveRole")).toEqual([
      "海外発 2 区間航空券：リアルタイム運賃の検索に失敗しました",
      "1 回目の通常往復：利用できるリアルタイム運賃がありません",
    ]);
  });

  it.each(LOCALES)("preserves old cached text and drops unknown codes in %s", (locale) => {
    // Old idempotent replays retain their original sentences in every locale.
    expect(fareLabWarnings(["長榮航空：依政策暫停抓取", "fare_from_the_future?airline=CI"], fareLabCopy(locale), "ticketRole"))
      .toEqual(["長榮航空：依政策暫停抓取"]);
    expect(fareLabWarnings(undefined, fareLabCopy("en"), "ticketRole")).toEqual([]);
  });

  it("falls back to the value when it has no name for it", () => {
    expect(fareLabWarnings(["fare_source_paused?airline=ZZ"], fareLabCopy("en"), "ticketRole"))
      .toEqual(["ZZ: reading its official fare pages is paused under the fail-closed policy."]);
  });
});

describe("structured comparison details and public crawler warnings", () => {
  it.each(LOCALES)("names modes, strategies and each missing ticket in %s", (locale) => {
    const copy = fareLabCopy(locale);
    const labels: Record<string, string> = copy;
    const details = fareLabWarnings([
      "fare_comparison_missing?mode=mixed_airlines&roles=conventional_first%2Chead_one_way",
      "fare_comparison_cheaper?mode=same_airline&strategy=reverse_two_segment",
      "live_comparison_missing?roles=middle_two_segment%2Ctail_one_way",
      "live_comparison_complete",
    ], copy, "ticketRole");
    expect(details).toHaveLength(4);
    expect(details[0]).toContain(copy["mode.mixed_airlines"]);
    expect(details[0]).toContain(copy["ticketRole.conventional_first"] + copy["b2b.listSeparator"] + labels["ticketRole.head_one_way"]);
    expect(details[1]).toContain(copy["mode.same_airline"]);
    expect(details[1]).toContain(copy["b2b.strategy.reverse_two_segment"]);
    const live = fareLabWarnings(["live_comparison_missing?roles=middle_two_segment%2Ctail_one_way"], copy, "liveRole");
    expect(live).toHaveLength(1);
    expect(live[0]).toContain(copy["liveRole.middle_two_segment"] + copy["b2b.listSeparator"] + copy["liveRole.tail_one_way"]);
    expect(details[3]).toBe(labels["warning.live_comparison_complete"]);
    expect([...details, ...live].join(" ")).not.toMatch(/\{\w+\}|fare_comparison_|live_comparison_|mixed_airlines|reverse_two_segment|middle_two_segment|head_one_way|tail_one_way/);
  });

  it.each(LOCALES)("localizes public errors without rendering their diagnostic reason in %s", (locale) => {
    const copy = fareLabCopy(locale);
    const warnings = fareLabWarnings([
      "fare_public_empty?airline=CI",
      "fare_public_blocked?airline=BR&reason=private_reason_code",
      "fare_public_unavailable?airline=JX&reason=private_reason_code",
    ], copy, "ticketRole");
    expect(warnings).toHaveLength(3);
    for (const [index, airline] of ["CI", "BR", "JX"].entries()) {
      expect(warnings[index]).toContain(copy[("airline." + airline) as keyof typeof copy]);
    }
    expect(warnings.join(" ")).not.toMatch(/fare_public_|private_reason_code|\{\w+\}/);
  });

  it("renders every remaining comparison outcome and preserves an old detail verbatim", () => {
    const codes = [
      "fare_comparison_regular_cheaper?mode=mixed_airlines",
      "fare_comparison_equal?mode=same_airline",
      "fare_comparison_unavailable?mode=mixed_airlines",
      "fare_comparison_incompatible?mode=same_airline",
      "fare_comparison_open_jaw?mode=mixed_airlines",
      "live_comparison_incomplete",
    ];
    const rendered = fareLabWarnings(codes, fareLabCopy("en"), "ticketRole");
    expect(rendered).toHaveLength(codes.length);
    expect(rendered.every((detail) => detail.trim().length > 0)).toBe(true);
    expect(rendered.join(" ")).not.toMatch(/fare_comparison_|live_comparison_|\{\w+\}/);
    const oldDetail = "缺少第一趟一般票的公開快取票價，這不是 0% 節省。";
    expect(fareLabWarnings([oldDetail], fareLabCopy("en"), "ticketRole")).toEqual([oldDetail]);
  });
});