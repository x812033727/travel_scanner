"use client";

import { Play } from "lucide-react";
import { useState } from "react";
import type { VideoKind } from "@/lib/videos";

/**
 * Hero player for `/videos/[slug]`: loads only the YouTube thumbnail (with high LCP priority)
 * until the reader presses play, then mounts the `youtube-nocookie.com` embed iframe.
 */
export function VideoWatchPlayer({
  youtubeVideoId,
  title,
  kind,
  playLabel,
}: {
  youtubeVideoId: string;
  title: string;
  kind: VideoKind;
  playLabel: string;
}) {
  const [playing, setPlaying] = useState(false);
  const shorts = kind === "shorts";

  return (
    <div
      className={
        shorts
          ? "mx-auto aspect-[9/16] max-h-[34rem] overflow-hidden rounded-2xl bg-black shadow-[var(--shadow-md)]"
          : "aspect-video w-full overflow-hidden rounded-2xl bg-black shadow-[var(--shadow-md)]"
      }
    >
      {playing ? (
        <iframe
          title={title}
          src={`https://www.youtube-nocookie.com/embed/${youtubeVideoId}?autoplay=1&rel=0`}
          allow="autoplay; encrypted-media; picture-in-picture; fullscreen"
          allowFullScreen
          referrerPolicy="strict-origin-when-cross-origin"
          className="h-full w-full border-0"
        />
      ) : (
        <button
          type="button"
          onClick={() => setPlaying(true)}
          aria-label={playLabel}
          className="group relative block h-full w-full focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]"
        >
          {/* eslint-disable-next-line @next/next/no-img-element -- a remote YouTube thumbnail */}
          <img
            src={`https://i.ytimg.com/vi/${youtubeVideoId}/hqdefault.jpg`}
            alt={title}
            loading="eager"
            fetchPriority="high"
            className="h-full w-full object-cover"
          />
          <span
            aria-hidden
            className="absolute inset-0 grid place-items-center bg-black/25 transition group-hover:bg-black/40"
          >
            <span className="grid h-16 w-16 place-items-center rounded-full bg-white/95 text-[var(--teal)] shadow-lg">
              <Play size={30} />
            </span>
          </span>
        </button>
      )}
    </div>
  );
}
