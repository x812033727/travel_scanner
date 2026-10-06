import type { SiteFeature } from "@/lib/site-features";

// One list for every navigation surface. The desktop header, the mobile menu
// sheet and the bottom tab bar must never disagree about what this site has.
export const primaryNavLinks: Array<{
  key: "guides" | "life" | "hotspots" | "foods" | "trips" | "alerts" | "flightStatus" | "airlines" | "pricing";
  href: string;
  feature?: SiteFeature;
}> = [
  // No `feature`: the guides section is first-party content with no provider cost and
  // no switch behind it, so it must not disappear when a catalog module is closed.
  { key: "guides", href: "/guides" },
  // The lifestyle section shares the guides' article system and the same reasoning: first-party
  // content, no switch. The community surfaces that render this list as "travel tools" filter
  // it out themselves, because it is the one entry here that is not about travel.
  { key: "life", href: "/life" },
  { key: "hotspots", href: "/hotspots", feature: "hotspots" },
  { key: "foods", href: "/foods" },
  { key: "trips", href: "/trips", feature: "trips" },
  { key: "alerts", href: "/alerts", feature: "alerts" },
  { key: "flightStatus", href: "/flights/status", feature: "flight_status" },
  { key: "airlines", href: "/labs/airlines", feature: "airline_fares" },
  { key: "pricing", href: "/pricing", feature: "pricing" },
];

export type NavGroupItem = { key: string; href: string; feature?: SiteFeature };
export type NavGroup = {
  /** The group's label in `navigation`, and the id its menu is known by. */
  key: "guides" | "ai" | "life" | "tools" | "videos";
  /** Where the label itself goes: the group's hub. Null for a group that is only a menu. */
  href: string | null;
  items: NavGroupItem[];
  /** Shown only in the plain header; discovery and community modes carry their own tools. */
  travelToolsOnly?: boolean;
};

/**
 * The header, the phone menu and the footer, grouped the way a reader looks for things:
 * where to go, what AI can do, the rest of tech and money, the travel tools, and the videos.
 * One list for every surface, for the reason `primaryNavLinks` gives; that list stays for the
 * community panels that offer the travel tools as a flat grid.
 *
 * Item labels live in `navigation` as `item_<key>`; a group's label is its own key there, so
 * the guides and lifestyle labels read exactly as they did before the menus existed.
 */
export const navGroups: readonly NavGroup[] = [
  {
    key: "guides", href: "/guides", items: [
      { key: "howto", href: "/guides/howto" },
      { key: "intel", href: "/guides/intel" },
      { key: "destinations", href: "/destinations" },
      { key: "hotspots", href: "/hotspots", feature: "hotspots" },
      { key: "foods", href: "/foods" },
    ],
  },
  {
    key: "ai", href: "/ai", items: [
      { key: "aiNews", href: "/life/topics/ai-news" },
      { key: "aiPlans", href: "/life/topics/ai-plans" },
      { key: "aiChat", href: "/life/topics/ai-chat" },
      { key: "claudeCode", href: "/life/topics/claude-code" },
      { key: "codex", href: "/life/topics/codex" },
      { key: "aiCreate", href: "/life/topics/ai-create" },
      { key: "aiWork", href: "/life/topics/ai-work" },
      { key: "aiTerms", href: "/life/topics/ai-terms" },
    ],
  },
  {
    key: "life", href: "/life", items: [
      { key: "software", href: "/life/topics/software" },
      { key: "website", href: "/life/topics/website" },
      { key: "marketing", href: "/life/topics/marketing" },
      { key: "gadgets", href: "/life/topics/gadgets" },
      { key: "finance", href: "/life/topics/finance" },
      { key: "crypto", href: "/life/topics/crypto" },
    ],
  },
  {
    key: "tools", href: null, travelToolsOnly: true, items: [
      { key: "trips", href: "/trips", feature: "trips" },
      { key: "alerts", href: "/alerts", feature: "alerts" },
      { key: "flightStatus", href: "/flights/status", feature: "flight_status" },
      { key: "airlines", href: "/labs/airlines", feature: "airline_fares" },
      { key: "pricing", href: "/pricing", feature: "pricing" },
    ],
  },
  { key: "videos", href: "/videos", items: [] },
];

/** The item's label key in `navigation`. The travel tools reuse the keys they always had. */
export function navItemLabelKey(group: NavGroup["key"], item: string): string {
  return group === "tools" || item === "hotspots" || item === "foods" ? item : `item_${item}`;
}
