/** Public entry labels only, mirrored by the API's BookingPlacement contract. `guide` is an
 *  article, `city` a destination page; both are first-party content surfaces. */
export const hotelBookingPlacements = [
  "destination", "hotspot", "trip", "stay", "checklist", "discovery", "guide", "city",
] as const;

export type HotelBookingPlacement = typeof hotelBookingPlacements[number];
