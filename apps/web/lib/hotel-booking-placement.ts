/** Public entry labels only, mirrored by the API's BookingPlacement contract. */
export const hotelBookingPlacements = [
  "destination", "hotspot", "trip", "stay", "checklist", "discovery",
] as const;

export type HotelBookingPlacement = typeof hotelBookingPlacements[number];
