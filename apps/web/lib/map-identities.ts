import { safeExternalHref } from "@/lib/navigation";

export type CatalogMapKind = "hotspot" | "merchant" | "hotel";
export type CatalogMapIdentity = {
  provider: string;
  place_id?: string | null;
  map_url?: string | null;
  status: string;
  verified_at?: string | null;
};
export type CatalogMapRow = {
  kind: CatalogMapKind;
  id: string;
  name: string;
  local_name?: string | null;
  address?: string | null;
  coordinate_source_url?: string | null;
  map_links?: CatalogMapLink[];
  destination_id: string;
  country_code: string;
  revision: number;
  canonical_fingerprint: string;
  google_place_id: string | null;
  map_identities: Record<string, CatalogMapIdentity>;
  review?: {
    candidate_place_ids?: string[];
    status?: string;
    generated_at?: string;
  };
};
export type MapIdentityBatch = {
  id: string;
  status: string;
  total: number;
  processed: number;
  results: { kind: CatalogMapKind; id: string; outcome: string }[];
  created_at: string;
};
export type MapIdentityCandidates = {
  item: CatalogMapRow;
  snapshot_id: string;
  expires_at: string;
  candidates: {
    place_id: string;
    name: string;
    address: string;
    country_code: string;
    latitude?: number | null;
    longitude?: number | null;
    google_maps_url: string;
  }[];
};
export type CatalogMapLink = {
  provider: string;
  label: string;
  url: string;
  primary: boolean;
  kind?: "place" | "position";
};

/** Only render server-provided URLs; never invent or confirm a place identity here. */
export function availableMapLinks(
  links: CatalogMapLink[] | undefined,
): CatalogMapLink[] {
  const seen = new Set<string>();
  return (links ?? [])
    .filter((link) => {
      if (!safeExternalHref(link.url) || seen.has(link.url)) return false;
      seen.add(link.url);
      return true;
    })
    .sort((a, b) => Number(b.primary) - Number(a.primary));
}
