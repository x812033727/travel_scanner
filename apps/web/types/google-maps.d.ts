export {};

declare global {
  interface Window {
    gm_authFailure?: () => void;
    mokaairGoogleMapsAuthFailed?: boolean;
    __mokaairGoogleMapsReady?: () => void;
    google?: {
      maps: {
        RenderingType?: { RASTER: string };
        event?: { clearInstanceListeners(instance: unknown): void };
        Map: new (element: HTMLElement, options: Record<string, unknown>) => {
          fitBounds(bounds: unknown, padding?: number | Record<string, number>): void;
          /** Used to switch gestureHandling when the map expands to fill the screen. */
          setOptions?(options: Record<string, unknown>): void;
        };
        LatLngBounds: new () => {
          extend(point: { lat: number; lng: number }): void;
        };
        Marker: new (options: Record<string, unknown>) => {
          setMap(map: unknown | null): void;
        };
        Polyline: new (options: Record<string, unknown>) => {
          setMap(map: unknown | null): void;
          addListener(eventName: string, handler: () => void): void;
        };
      };
    };
  }
}
