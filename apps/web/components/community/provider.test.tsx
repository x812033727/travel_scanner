import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { useEffect, useState } from "react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { CommunityProvider, useCommunity } from "./provider";
import { useResource } from "./use-resource";
import { closedCommunity, type CommunityMe, type CommunityState } from "@/lib/community/types";

const mock = vi.hoisted(() => ({
  user: null as { id: string } | null,
  api: vi.fn(), mounts: vi.fn(),
}));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: mock.user }) }));
vi.mock("@/lib/api", () => ({ api: mock.api }));
const state: CommunityState = { status: "ready", flags: { ...closedCommunity.flags, enabled: true } };
beforeEach(() => {
  mock.user = null; mock.api.mockReset(); mock.mounts.mockReset();
  mock.api.mockImplementation(async (path: string) => path === "/community/status" ? state.flags : {});
});
afterEach(cleanup);
function CoreForm() {
  const [value, setValue] = useState("");
  useEffect(() => { mock.mounts(); }, []);
  return <input aria-label="Core travel form" value={value} onChange={(event) => setValue(event.target.value)} />;
}
function Identity() {
  const { me } = useCommunity();
  return <p>{me?.profile?.display_name || "No identity"}</p>;
}
const identity = (name: string): CommunityMe => ({ verified: true, restricted: false,
  notification_preferences: {}, profile: { id: name, handle: name, display_name: name,
    bio: "", languages: [], destinations: [], avatar_id: null } });

it("keeps existing travel state mounted when the shared login request finishes", async () => {
  const view = render(<CommunityProvider state={state}><CoreForm /></CommunityProvider>);
  fireEvent.change(screen.getByLabelText("Core travel form"), { target: { value: "Resumed search" } });
  mock.user = { id: "signed-in" };
  view.rerender(<CommunityProvider state={state}><CoreForm /></CommunityProvider>);
  await waitFor(() => expect(mock.api).toHaveBeenCalledWith("/community/me"));
  expect(screen.getByDisplayValue("Resumed search")).toBeTruthy();
  expect(mock.mounts).toHaveBeenCalledTimes(1);
});

it("never releases a delayed profile from the previous signed-in account", async () => {
  let finishFirst!: (value: CommunityMe) => void;
  mock.user = { id: "first" };
  mock.api.mockImplementation((path: string) => path === "/community/status" ? Promise.resolve(state.flags)
    : path === "/community/me" ? mock.user?.id === "first"
      ? new Promise((done) => { finishFirst = done; }) : Promise.resolve(identity("second"))
      : Promise.resolve({ cursor: 0, unread: 0 }));
  const view = render(<CommunityProvider state={state}><Identity /></CommunityProvider>);
  mock.user = { id: "second" };
  view.rerender(<CommunityProvider state={state}><Identity /></CommunityProvider>);
  await screen.findByText("second");
  await act(async () => { finishFirst(identity("first")); });
  expect(screen.queryByText("first")).toBeNull();
  expect(screen.getByText("second")).toBeTruthy();
});

it("binds resource caches to the current account without remounting core pages", async () => {
  function PrivateResource() {
    const { data } = useResource<{ value: string }>("/community/private");
    return <p>{data?.value || "Loading private data"}</p>;
  }
  mock.user = { id: "first" };
  let finishSecond!: (data: { value: string }) => void;
  mock.api.mockResolvedValueOnce({ value: "First account secret" })
    .mockImplementationOnce(() => new Promise((done) => { finishSecond = done; }));
  const view = render(<PrivateResource />);
  await screen.findByText("First account secret");
  mock.user = { id: "second" };
  view.rerender(<PrivateResource />);
  expect(screen.queryByText("First account secret")).toBeNull();
  await act(async () => { finishSecond({ value: "Second account data" }); });
  expect(screen.getByText("Second account data")).toBeTruthy();
});
