/** Public entry labels only, mirrored by the API's BookingPlacement contract. `guide` is an
 *  article, `city` a destination page, `share` a read-only shared trip; all three are
 *  first-party content surfaces. */
export const hotelBookingPlacements = [
  "destination", "hotspot", "trip", "stay", "checklist", "discovery", "guide", "city", "share",
] as const;

export type HotelBookingPlacement = typeof hotelBookingPlacements[number];
