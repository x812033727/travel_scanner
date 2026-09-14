import { isValidElement, type ReactElement } from "react";
import { describe, expect, it } from "vitest";
import { CommunityPage, communityMetadata } from "./page";

/**
 * The four public community routes were `noindex` shells: one shared title per section and
 * no server-rendered content under it. These are the two halves of that the helper owns --
 * what a page is allowed to say about itself, and how many `<h1>` elements it ships.
 */

/** The children `CommunityPage` returns, without mounting `CommunityGate` and the four
 *  providers it reads. What is asserted here is the shape of the tree, not its rendering. */
async function childrenOf(element: Promise<ReactElement>) {
  const fragment = await element;
  const children = (fragment.props as { children: unknown }).children;
  return (Array.isArray(children) ? children : [children]).filter(isValidElement);
}

describe("communityMetadata", () => {
  it("keeps a page out of the index unless it is asked otherwise", async () => {
    // The admin consoles and the post editor call this with no options at all, and every one
    // of them has to stay noindex without being touched.
    await expect(communityMetadata("adminCommunity")).resolves.toEqual({
      title: "社群管理 | Mokaair",
      robots: { index: false, follow: true },
    });
    expect((await communityMetadata("editPost")).robots).toEqual({ index: false, follow: true });
    expect((await communityMetadata("post", {})).robots).toEqual({ index: false, follow: true });
  });

  it("titles a page after the record it is showing", async () => {
    await expect(communityMetadata("post", {
      index: true, name: "京都三日", description: "秋天的京都",
    })).resolves.toEqual({
      title: "京都三日 | Mokaair",
      description: "秋天的京都",
      robots: { index: true, follow: true },
    });
  });

  it("falls back to the section name when the record has none to give", async () => {
    // A record whose display name is blank must not produce " | Mokaair".
    expect((await communityMetadata("profile", { index: true, name: "   " })).title).toBe("公開個人頁 | Mokaair");
    expect((await communityMetadata("pets", { index: true })).title).toBe("寵物友善 | Mokaair");
  });

  it("omits the description rather than publishing an empty one", async () => {
    expect(await communityMetadata("post", { index: true, name: "京都三日" })).not.toHaveProperty("description");
    expect(await communityMetadata("post", { index: true, description: "" })).not.toHaveProperty("description");
  });

  it("always lets a crawler follow the links out", async () => {
    for (const metadata of [await communityMetadata("post"), await communityMetadata("post", { index: true })]) {
      expect(metadata.robots).toMatchObject({ follow: true });
    }
  });
});

describe("CommunityPage", () => {
  it("heads a directory with its section name", async () => {
    const [heading] = await childrenOf(CommunityPage({ title: "pets", children: null }));
    expect(heading.type).toBe("h1");
    expect((heading.props as { children: string }).children).toBe("寵物友善");
  });

  it("leaves the only h1 to the record on a detail route", async () => {
    // PetDetails, PostDetails and ProfileView each render the record's own name as an h1.
    // With the section label on, those pages shipped two, the first identical on every
    // record in the section.
    const children = await childrenOf(CommunityPage({ title: "pets", children: null, heading: false }));
    expect(children.filter((child) => child.type === "h1")).toHaveLength(0);
    expect(children).toHaveLength(1);
  });

  it("still gates the content when the heading is off", async () => {
    const detail = await childrenOf(CommunityPage({ title: "post", children: null, heading: false }));
    const directory = await childrenOf(CommunityPage({ title: "pets", children: null }));
    // Same gate component in both cases: turning the label off must not open a member route.
    expect(detail[0].type).toBe(directory[1].type);
  });

  it("passes the membership requirements through to the gate", async () => {
    const [, gate] = await childrenOf(CommunityPage({ title: "post", children: null, member: true, verified: true }));
    expect(gate.props).toMatchObject({ member: true, verified: true });
  });
});
