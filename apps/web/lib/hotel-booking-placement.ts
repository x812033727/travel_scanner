/** Public entry labels only, mirrored by the API's BookingPlacement contract. `guide` is a
 *  travel article, `city` a destination page, `share` a read-only shared trip and `life` a
 *  lifestyle article; all four are first-party content surfaces. */
export const hotelBookingPlacements = [
  "destination", "hotspot", "trip", "stay", "checklist", "discovery", "guide", "city", "share",
  "life",
] as const;

export type HotelBookingPlacement = typeof hotelBookingPlacements[number];
