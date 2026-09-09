"use client";
import { useState } from "react";
import { useLocale } from "next-intl";
import { Play, ExternalLink } from "lucide-react";
import { getDiscoveryCopy } from "@/lib/discovery-copy";
import type { DiscoveryVideo } from "@/lib/discovery";
import { Button } from "@/components/community/ui";

export function DiscoveryVideoPlayer({ video }: { video: DiscoveryVideo }) {
  return <Video key={`${video.video_id}:${video.status}:${video.embed_url}`} video={video} />;
}
function Video({ video }: { video: DiscoveryVideo }) {
  const c = getDiscoveryCopy(useLocale());
  const [loaded, setLoaded] = useState(false);
  if (!/^[A-Za-z0-9_-]{11}$/.test(video.video_id)) return null;
  const source = `https://www.youtube.com/watch?v=${video.video_id}`;
  const embed = `https://www.youtube-nocookie.com/embed/${video.video_id}`;
  const canEmbed = video.status === "embeddable" && video.embed_url === embed;
  return <section className="min-w-0 space-y-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4" aria-label={c.video}>
    {loaded && canEmbed ? <iframe title={c.video} src={`${embed}?autoplay=0&rel=0`} allow="encrypted-media; picture-in-picture; fullscreen" allowFullScreen referrerPolicy="strict-origin-when-cross-origin" className="aspect-video min-h-[200px] min-w-[200px] w-full rounded-xl border-0" /> : <div className="flex min-h-[200px] flex-col items-center justify-center gap-3 text-center">
      <Play size={32} className="text-[var(--teal)]" aria-hidden />
      <p className="max-w-md text-sm leading-6 text-[var(--muted)]">{canEmbed ? c.videoPrivacy : c.videoFallback}</p>
      {canEmbed && <Button onClick={() => setLoaded(true)}>{c.loadVideo}</Button>}
    </div>}
    <a href={source} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center gap-2 rounded-lg font-semibold text-[var(--teal)] underline focus-visible:outline focus-visible:outline-2"><ExternalLink size={16} aria-hidden />{c.source}</a>
  </section>;
}
