import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminOperationsProvider } from "./admin-operations-provider";
import { GB, type ReviewStoreView, sizeText, VideoReviewStoreCard, wholeGb } from "./admin-video-review-store";
import type { AdminBootstrap } from "@/lib/admin-operations";
import { fill } from "@/lib/video-backup-copy";
import { videoReviewStoreCopy } from "@/lib/video-review-store-copy";

const copy = videoReviewStoreCopy("zh-TW");
const store: ReviewStoreView = { used_bytes: 30 * GB, max_total_bytes: 60 * GB, max_file_bytes: 1.5 * GB, disk_free_bytes: 120 * GB, disk_total_bytes: 200 * GB };

function bootstrap(manage: boolean): AdminBootstrap {
  return { admin_roles: [], admin_capabilities: ["content.read", "settings.read", ...(manage ? ["settings.manage"] : [])], navigation: [], pending_counts: {}, system_status: {}, environment: "test", can_deploy: false, can_manage_database: false };
}

/** The store readout, the provider settings snapshot, and the PUT that saves the cap. */
function site({ view = store, stamp = "2026-11-19T01:00:00Z" as string | null, put = () => Response.json({ provider: "video_reviews" }) }: { view?: ReviewStoreView; stamp?: string | null; put?: () => Response } = {}) {
  let current = view;
  const puts: { url: string; body: Record<string, unknown> }[] = [];
  vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init: RequestInit = {}) => {
    const url = String(input);
    if (init.method === "PUT") {
      const body = JSON.parse(String(init.body)) as Record<string, unknown>;
      puts.push({ url, body });
      const answer = put();
      if (answer.ok) current = { ...current, max_total_bytes: (body.config as Record<string, number>).video_review_max_total_bytes };
      return Promise.resolve(answer);
    }
    if (url.includes("/admin/videos/store")) return Promise.resolve(Response.json(current));
    if (url.includes("/admin/provider-settings")) {
      return Promise.resolve(Response.json({ providers: stamp === null ? [] : [{ provider: "video_reviews", updated_at: stamp }] }));
    }
    return Promise.resolve(Response.json({}));
  }));
  return { puts };
}

async function mount(manage = true) {
  render(<AdminOperationsProvider bootstrap={bootstrap(manage)}><VideoReviewStoreCard /></AdminOperationsProvider>);
  const card = await screen.findByRole("region", { name: copy.title });
  await within(card).findByText(fill(copy.used, { used: "30 GB", limit: "60 GB", percent: 50 }));
  return within(card);
}

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("review storage card", () => {
  it("keeps the five catalogs aligned", () => {
    const keys = Object.keys(videoReviewStoreCopy("en")).sort();
    for (const locale of ["zh-TW", "zh-CN", "ja", "ko"]) expect(Object.keys(videoReviewStoreCopy(locale)).sort()).toEqual(keys);
    for (const locale of ["en", "zh-TW", "zh-CN", "ja", "ko"]) {
      const names = (text: string) => [...text.matchAll(/\{(\w+)\}/g)].map((match) => match[1]).sort();
      const catalog = videoReviewStoreCopy(locale) as Record<string, string>;
      for (const [key, text] of Object.entries(videoReviewStoreCopy("en"))) expect(names(catalog[key]), `${locale}.${key}`).toEqual(names(text));
    }
  });

  it("reads a whole number of gigabytes from 1 to 500 only", () => {
    expect([wholeGb("80"), wholeGb(" 1 "), wholeGb("500")]).toEqual([80, 1, 500]);
    for (const bad of ["0", "501", "80.5", "-3", "", "eighty"]) expect(wholeGb(bad), bad).toBeNull();
    expect([sizeText(80 * GB), sizeText(1_500_000_000), sizeText(512), sizeText(2_000_000_000_000)]).toEqual(["80 GB", "1.5 GB", "512 B", "2.0 TB"]);
  });

  it("shows what the store holds, its cap and the host disk, and saves 80 GB as bytes with the row's stamp", async () => {
    const { puts } = site();
    const card = await mount();
    expect(card.getByRole("progressbar").getAttribute("aria-valuenow")).toBe("50");
    expect(card.getByText(fill(copy.disk, { free: "120 GB", total: "200 GB" }))).toBeTruthy();
    const input = card.getByRole("spinbutton", { name: copy.limitLabel }) as HTMLInputElement;
    expect(input.value).toBe("60");
    expect(card.getByRole("button", { name: copy.save })).toHaveProperty("disabled", true);
    fireEvent.change(input, { target: { value: "80" } });
    fireEvent.click(card.getByRole("button", { name: copy.save }));
    await waitFor(() => expect(puts).toHaveLength(1));
    expect(puts[0].url).toContain("/admin/provider-settings/video_reviews");
    expect(puts[0].body).toEqual({ expected_updated_at: "2026-11-19T01:00:00Z", config: { video_review_max_total_bytes: 80 * GB } });
    await card.findByText(fill(copy.saved, { limit: "80 GB" }));
  });

  it("sends a null stamp when nothing was saved yet, warns past the disk, and says so on a conflict", async () => {
    const { puts } = site({ stamp: null, put: () => Response.json({ code: "provider_setting_conflict" }, { status: 409 }) });
    const card = await mount();
    const input = card.getByRole("spinbutton", { name: copy.limitLabel });
    fireEvent.change(input, { target: { value: "200" } });
    expect(card.getByText(copy.overDisk)).toBeTruthy();
    fireEvent.change(input, { target: { value: "120" } });
    expect(card.queryByText(copy.overDisk)).toBeNull();
    fireEvent.click(card.getByRole("button", { name: copy.save }));
    await card.findByText(copy.conflict);
    expect(puts[0].body.expected_updated_at).toBeNull();
  });

  it("flags a nearly full store and lets a reader see it without a way to change it", async () => {
    site({ view: { ...store, used_bytes: 50 * GB } });
    render(<AdminOperationsProvider bootstrap={bootstrap(false)}><VideoReviewStoreCard /></AdminOperationsProvider>);
    const card = within(await screen.findByRole("region", { name: copy.title }));
    await card.findByText(copy.nearlyFull);
    expect(card.getByText(copy.readOnly)).toBeTruthy();
    expect(card.queryByRole("spinbutton")).toBeNull();
    expect(card.queryByRole("button", { name: copy.save })).toBeNull();
  });
});
