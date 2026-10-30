import { describe, expect, it } from "vitest";
import { runpodCopy, runpodField, runpodSecret } from "./runpod-copy";

const LOCALES = ["en", "ja", "ko", "zh-CN", "zh-TW"];

function keys(value: unknown, prefix = ""): string[] {
  if (!value || typeof value !== "object") return [prefix];
  return Object.entries(value).flatMap(([key, child]) => keys(child, prefix ? `${prefix}.${key}` : key)).sort();
}

describe("runpodCopy", () => {
  it("has the same keys in every locale, with nothing left empty", () => {
    const english = keys(runpodCopy("en"));
    for (const locale of LOCALES) {
      expect(keys(runpodCopy(locale))).toEqual(english);
      for (const path of english) {
        const text = path.split(".").reduce<unknown>((node, key) => (node as Record<string, unknown>)[key], runpodCopy(locale));
        expect(typeof text === "string" && text.trim().length > 0, `${locale} ${path}`).toBe(true);
      }
    }
  });

  it("names every RunPod field and the key, and falls back to English", () => {
    const copy = runpodCopy("zh-TW");
    expect(runpodField(copy, "runpod_image")?.label).toBe("容器映像");
    expect(runpodField(copy, "gpu_route_default")?.options?.auto).toBe("自動");
    expect(runpodField(copy, "pexels_api_base_url")).toBeUndefined();
    expect(runpodSecret(copy, "runpod_api_key")?.label).toBe("RunPod API 金鑰");
    expect(runpodCopy("fr")).toBe(runpodCopy("en"));
  });
});
