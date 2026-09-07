import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { CommunityImage } from "./ui";
import { ApiError } from "@/lib/api";

const mock = vi.hoisted(() => ({ api: vi.fn() }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
beforeEach(() => { mock.api.mockReset(); });
afterEach(cleanup);

it("lets a reader retry a failed image authorization", async () => {
  mock.api.mockRejectedValueOnce(new Error("storage temporarily unavailable"))
    .mockResolvedValueOnce({ url: "https://media.example.com/new-authorization" });
  render(<CommunityImage id="photo" alt="Trip photo" />);
  fireEvent.click(await screen.findByRole("button", { name: "重試" }));
  const image = await screen.findByRole("img", { name: "Trip photo" });
  expect(image.getAttribute("src")).toBe("https://media.example.com/new-authorization");
  expect(mock.api.mock.calls.map(([url]) => url)).toEqual(["/community/media/photo", "/community/media/photo"]);
});

it("requires fresh permission after a signed URL expires and hides withdrawn media", async () => {
  mock.api.mockResolvedValueOnce({ url: "https://media.example.com/expired-authorization" });
  render(<CommunityImage id="photo" alt="Withdrawn photo" />);
  fireEvent.error(await screen.findByRole("img", { name: "Withdrawn photo" }));
  mock.api.mockRejectedValueOnce(new ApiError("Unavailable", 404, "community_not_found"));
  fireEvent.click(await screen.findByRole("button", { name: "重試" }));
  await waitFor(() => expect(mock.api).toHaveBeenCalledTimes(2));
  await screen.findByRole("alert");
  expect(screen.queryByRole("img")).toBeNull();
});
