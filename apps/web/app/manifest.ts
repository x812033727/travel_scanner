import type { MetadataRoute } from "next";

/**
 * The installable app.
 *
 * `share_target` is Android's only way to hand a link to an installed web app: sharing a
 * place from Google Maps lands on /share-target, which reads the shared text and asks
 * which trip it belongs to. iOS has no equivalent, so that page also takes a paste — and
 * says so, rather than leaving iPhone users looking for a share sheet that will not come.
 */
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Mokaair",
    short_name: "Mokaair",
    description: "Plan a trip, compare the whole journey, and carry the day with you.",
    start_url: "/",
    scope: "/",
    display: "standalone",
    orientation: "portrait",
    background_color: "#ffffff",
    theme_color: "#177c78",
    icons: [
      { src: "/brand/mokaair-monogram.png", sizes: "512x512", type: "image/png", purpose: "any" },
      { src: "/brand/mokaair-monogram.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
      { src: "/apple-icon.png", sizes: "180x180", type: "image/png" },
    ],
    share_target: {
      action: "/share-target",
      method: "GET",
      params: { title: "title", text: "text", url: "url" },
    },
  };
}
