import { act, cleanup, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { DestinationAffiliateOptions } from "./destination-affiliate-options";

const ok = (value: unknown) =>
  new Response(JSON.stringify(value), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("DestinationAffiliateOptions", () => {
  it("requests only the selected category, cancels old requests and ignores late results", async () => {
    const pending: { url: string; signal: AbortSignal; resolve: (value: Response) => void }[] = [];
    vi.stubGlobal("fetch", vi.fn((input: RequestInfo | URL, init: RequestInit) => new Promise<Response>((resolve) => {
      pending.push({ url: String(input), signal: init.signal as AbortSignal, resolve });
    })));
    const response = (destination: string, module: string, name: string) => ok({ destination_id: destination, module, disclosure: "Disclosure", options: [{ id: name, cta: name, clickout_url: "/api/travel/affiliates/destination-offers/verified/clickout" }] });
    const view = render(<DestinationAffiliateOptions destinationId="tokyo" modules={["hotel"]} contextual />);
    expect(pending[0].url).toContain("destination_id=tokyo&module=hotel");
    view.rerender(<DestinationAffiliateOptions destinationId="seoul" modules={["transport"]} contextual />);
    expect(pending[0].signal.aborted).toBe(true);
    expect(pending[1].url).toContain("destination_id=seoul&module=transport");
    await act(async () => { pending[1].resolve(response("seoul", "transport", "Seoul transfer")); });
    expect(await screen.findByRole("button", { name: /Seoul transfer/ })).toBeTruthy();
    await act(async () => { pending[0].resolve(response("tokyo", "hotel", "Old Tokyo hotel")); });
    expect(screen.queryByRole("button", { name: /Old Tokyo hotel/ })).toBeNull();
    view.rerender(<DestinationAffiliateOptions destinationId="tokyo" modules={["activities"]} contextual />);
    expect(screen.queryByRole("button", { name: /Seoul transfer/ })).toBeNull();
    expect(pending).toHaveLength(3);
    expect(pending.every(({ url }) => !url.includes("hotel-quotes"))).toBe(true);
  });
  it("shows verified brand names without exposing Travelpayouts", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((input: RequestInfo | URL) => {
        const url = String(input);
        const serviceModule = new URL(
          url,
          "https://mokaair.test",
        ).searchParams.get("module");
        return Promise.resolve(
          ok({
            destination_id: "tokyo",
            module: serviceModule,
            disclosure: "透過合作連結預訂，價格不因此增加。",
            options:
              serviceModule === "activities"
                ? [
                    {
                      id: "offer-1",
                      brand: "klook",
                      display_name: "Klook",
                      destination_id: "tokyo",
                      module: serviceModule,
                      cta: "到 Klook 查看",
                      clickout_url:
                        "/api/travel/affiliates/destination-offers/offer-1/clickout",
                    },
                  ]
                : [],
          }),
        );
      }),
    );

    render(<DestinationAffiliateOptions destinationId="tokyo" />);

    const section = await screen.findByRole("region", {
      name: "這個目的地的合作平台",
    });
    const button = within(section).getByRole("button", { name: /Klook/ });
    expect(button).toBeTruthy();
    expect(section.textContent).not.toContain("Travelpayouts");
    const form = button.closest("form");
    expect(form?.getAttribute("method")).toBe("post");
    expect(form?.getAttribute("target")).toBe("_blank");
    expect(form?.getAttribute("rel")).toBe("noopener noreferrer");
    expect(form?.getAttribute("action")).toContain("destination-offers");
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(5));
  });

  it("renders nothing when no reviewed destination offer is public", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        ok({
          destination_id: "tokyo",
          module: "hotel",
          disclosure: "",
          options: [],
        }),
      ),
    );
    const { container } = render(
      <DestinationAffiliateOptions destinationId="tokyo" />,
    );
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(5));
    expect(container.innerHTML).toBe("");
  });
});
