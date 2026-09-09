import { describe, expect, it } from "vitest";
import { contentSavedReference, parseSavedKey, savedReference } from "./saved-items";
describe("canonical saved references", () => {
  it("shares hotel/service and article/video/guide identity", () => {
    expect(savedReference("hotel", "ABCD")).toEqual(savedReference("service", "abcd"));
    expect(contentSavedReference({ id: "guide:ABCD", kind: "article", title: "Guide" })?.key).toBe("guide:abcd");
    expect(contentSavedReference({ id: "video:ABCD", kind: "video", title: "Video" })?.key).toBe("guide:abcd");
    expect(contentSavedReference({ id: "hotel:wrong", title: "Hotel", collection_ref: { kind: "hotel", id: "RIGHT" } })?.key).toBe("service:right");
    expect(savedReference("itinerary", "A")?.key).toBe("post:a");
  });
  it("preserves case-sensitive Google Place IDs and rejects unknown kinds", () => {
    expect(parseSavedKey("restaurant:ChIJAb:CDef")?.id).toBe("ChIJAb:CDef");
    expect(parseSavedKey("unknown:1")).toBeNull();
    expect(savedReference("pet_place", "legacy")).toBeNull();
    expect(parseSavedKey("hotspot:")).toBeNull();
  });
  it("normalizes legacy UUID hex membership targets for guides, posts and hotel aliases", () => {
    const hex = "ABCDEF1234567890ABCDEF1234567890";
    const id = "abcdef12-3456-7890-abcd-ef1234567890";
    for (const type of ["guide", "article", "video", "post", "hotel", "service"]) expect(savedReference(type, hex)).toEqual(savedReference(type, id));
    expect(savedReference("restaurant", hex)?.id).toBe(hex);
  });
});
