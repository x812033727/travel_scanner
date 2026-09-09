export type CommunityFlags = {
  enabled: boolean; posting_enabled: boolean; comments_enabled: boolean;
  messaging_enabled: boolean; translation_enabled: boolean; pet_reports_enabled: boolean;
};
export type CommunityState = { status: "ready" | "unavailable"; flags: CommunityFlags };
export const closedCommunity: CommunityState = { status: "unavailable", flags: {
  enabled: false, posting_enabled: false, comments_enabled: false, messaging_enabled: false,
  translation_enabled: false, pet_reports_enabled: false,
} };
export type PublicProfile = {
  id: string; handle: string; display_name: string; bio: string; languages: string[];
  destinations: string[]; avatar_id: string | null; followers?: number;
  following?: boolean; can_message?: boolean;
};
export type CommunityMe = { profile: PublicProfile | null; verified: boolean; restricted: boolean;
  creator_invited?: boolean; can_publish?: boolean; invitation_required?: boolean;
  notification_preferences: Record<string, boolean> };
export type Media = { id: string; alt: string; width: number; height: number };
export type CatalogPlace = { id: string; kind: "pet_place" | "hotspot" | "merchant";
  name: string; names?: Record<string, string>; destination: string; href: string };
export type PublicItinerary = { destination: string; timezone: string; days: number; stops: Array<{
  day: number; position: number; title: string; location_name: string; item_type: string;
  duration_minutes: number | null; names: Record<string, string>;
}> };
export type Post = {
  video_refs?: import("@/lib/discovery").DiscoveryVideo[];
  id: string; revision_id: string; author: PublicProfile; title: string; body: string;
  locale: string; destination: string; kind: "story" | "guide" | "pet_visit"; topics: string[];
  place_ids: string[]; places?: CatalogPlace[]; media: Media[]; itinerary: PublicItinerary | null; allow_fork: boolean;
  published_at: string | null; featured: boolean; likes: number; saves: number; liked: boolean;
  saved: boolean; version?: number; state?: "draft" | "pending" | "published" | "hidden";
  pending_revision_id?: string | null;
};
export type Page<T> = { items: T[]; next_cursor?: string | number | null };
export type Comment = { id: string; body: string; locale: string; author: PublicProfile;
  parent_id: string | null; created_at: string; deleted?: boolean; hidden?: boolean };
export type Notice = { id: number; kind: string; target: string; read: boolean; created_at: string;
  actor: PublicProfile | null };
export type Conversation = { id: string; other: PublicProfile | null; unread: number; can_send: boolean };
export type Message = { id: number; body: string; sender_id: string | null; created_at: string;
  mine: boolean; card_unavailable: boolean; card: { id: string; title: string } | null };
export type PetRequirements = { species: string; count: number; weight_kg: number;
  area: "any" | "indoor" | "outdoor"; ground_required: boolean; has_leash: boolean;
  has_carrier: boolean; has_stroller: boolean; has_diaper: boolean; overnight: boolean };
export const defaultPet: PetRequirements = { species: "dog", count: 1, weight_kg: 5, area: "any",
  ground_required: false, has_leash: true, has_carrier: false, has_stroller: false,
  has_diaper: false, overnight: false };
export type PetRule = { species: string; status: "allowed" | "conditional" | "not_allowed" | "unknown";
  weight_limit: "unknown" | "none" | "limited"; max_weight_kg: number | null;
  count_limit: "unknown" | "none" | "limited"; max_count: number | null;
  ground_allowed: boolean | null; leash_required: boolean | null; carrier_required: boolean | null;
  stroller_required: boolean | null; stroller_allowed: boolean | null; diaper_required: boolean | null;
  indoor_allowed: boolean | null; outdoor_allowed: boolean | null; reservation_required: boolean | null;
  overnight_allowed: boolean | null; fee_amount: number | null; fee_currency: string | null; notes: string };
export const unknownPetRule: PetRule = { species: "dog", status: "unknown", weight_limit: "unknown", max_weight_kg: null,
  count_limit: "unknown", max_count: null, ground_allowed: null, leash_required: null, carrier_required: null,
  stroller_required: null, stroller_allowed: null, diaper_required: null, indoor_allowed: null,
  outdoor_allowed: null, reservation_required: null, overnight_allowed: null,
  fee_amount: null, fee_currency: null, notes: "" };
export type PetPlace = { id: string; name: string; names: Record<string, string>; kind: string; country: string;
  destination: string; address: string; official_url: string | null; policies: PetRule[];
  source_url: string | null; verified_at: string | null; verification_current: boolean;
  disputed: boolean; conflicts?: string[]; latitude: number | null; longitude: number | null;
  coordinate_source_url: string | null; status?: string; version?: number; identity_key?: string | null;
  references?: Array<{kind: string; id: string}>;
  experiences?: Array<{ id: string; body: string; source_url: string | null; visited_on: string | null;
    media_ids: string[]; author: { handle: string; display_name: string } }> };
