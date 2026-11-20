"use client";

import { ExternalLink, Play } from "lucide-react";
import { useState } from "react";
import { Link } from "@/i18n/navigation";
import { videoArticleHref, type PublicVideo } from "@/lib/videos";

export type VideoCardLabels = { play: string; watchOnYoutube: string; readArticle: string; category?: string | null };

/**
 * One video: its thumbnail until the reader presses play, then the youtube-nocookie player.
 * Nothing from YouTube but the thumbnail image loads before that press, the same promise the
 * community and discovery players make.
 */
export function VideoCard({ video, labels, date }: { video: PublicVideo; labels: VideoCardLabels; date: string }) {
  const [playing, setPlaying] = useState(false);
  const id = video.youtube_video_id;
  const article = videoArticleHref(video);
  const shorts = video.kind === "shorts";
  return (
    <li id={`video-${video.slug}`} className="portal-card-surface flex min-w-0 flex-col overflow-hidden rounded-2xl">
      <div className={shorts ? "mx-auto aspect-[9/16] max-h-[28rem] w-full bg-black" : "aspect-video bg-black"}>
        {playing ? (
          <iframe
            title={video.title}
            src={`https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`}
            allow="autoplay; encrypted-media; picture-in-picture; fullscreen"
            allowFullScreen
            referrerPolicy="strict-origin-when-cross-origin"
            className="h-full w-full border-0"
          />
        ) : (
          <button
            type="button"
            onClick={() => setPlaying(true)}
            aria-label={labels.play}
            className="group relative block h-full w-full focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]"
          >
            {/* eslint-disable-next-line @next/next/no-img-element -- a remote thumbnail, not a site asset */}
            <img
              src={`https://i.ytimg.com/vi/${id}/hqdefault.jpg`}
              alt=""
              width={480}
              height={360}
              loading="lazy"
              decoding="async"
              className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-[1.02]"
            />
            <span aria-hidden className="absolute inset-0 grid place-items-center bg-black/20 transition group-hover:bg-black/35">
              <span className="grid h-14 w-14 place-items-center rounded-full bg-white/90 text-[var(--teal)] shadow-lg"><Play size={26} /></span>
            </span>
          </button>
        )}
      </div>
      <div className="flex flex-1 flex-col gap-2 p-4 sm:p-5">
        {labels.category ? (
          <p className="text-[length:var(--text-xs)] font-semibold uppercase tracking-wide">
            <span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-0.5 text-[var(--teal-dark)]">{labels.category}</span>
          </p>
        ) : null}
        <h3 className="text-lg font-bold leading-7 tracking-tight">{video.title}</h3>
        <p className="text-sm text-[var(--muted)]"><time dateTime={video.published_at}>{date}</time></p>
        <div className="mt-auto flex flex-wrap gap-x-4 pt-1">
          {article ? (
            <Link href={article} className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline underline-offset-4">{labels.readArticle}</Link>
          ) : null}
          <a href={`https://www.youtube.com/watch?v=${id}`} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center gap-1.5 text-[var(--muted)] underline underline-offset-4 hover:text-[var(--teal)]">
            <ExternalLink size={15} aria-hidden />{labels.watchOnYoutube}
          </a>
        </div>
      </div>
    </li>
  );
}
