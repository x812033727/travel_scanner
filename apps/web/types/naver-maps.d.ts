export {};

declare global {
  interface Window {
    naver?: {
      maps: {
        Map: new (element: HTMLElement, options: Record<string, unknown>) => {
          fitBounds(bounds: unknown, margin?: Record<string, number>): void;
          destroy?(): void;
        };
        LatLng: new (latitude: number, longitude: number) => unknown;
        LatLngBounds: new (southWest?: unknown, northEast?: unknown) => unknown;
        Marker: new (options: Record<string, unknown>) => { setMap(map: unknown | null): void };
        Polyline: new (options: Record<string, unknown>) => { setMap(map: unknown | null): void };
        Event: {
          addListener(target: unknown, eventName: string, handler: () => void): void;
        };
      };
    };
  }
}
