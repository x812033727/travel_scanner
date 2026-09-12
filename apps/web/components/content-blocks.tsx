import {
  contentBlockLink,
  contentImageSrc,
  licenseUrl,
  type CalloutTone,
  type ImageCredit,
  type RichContentBlock,
} from "@/lib/content-blocks";
import { siteUrl } from "@/lib/seo";

/** The words the renderer cannot invent: a credit prefix and one name per callout tone. A
 *  caller that renders only the four shared blocks (the legal pages) passes nothing. */
export type ContentBlockLabels = {
  imageCredit: string;
  tip: string;
  warning: string;
  info: string;
};

const TONE_CLASSES: Record<CalloutTone, string> = {
  tip: "border-[var(--teal)]",
  warning: "border-[var(--warning,#b45309)]",
  info: "border-[var(--muted)]",
};

/** Links back into this site open in the same tab; only genuinely external ones open a new one. */
function sameSite(href: string): boolean {
  try {
    return new URL(href).host === new URL(siteUrl).host;
  } catch {
    return false;
  }
}

/** "圖片：Author (CC BY-SA 4.0)", with the author linked to the source page and the licence
 *  to its deed where one exists. Shared with the article hero, so the two credits agree. */
export function ImageCreditLine({ credit, prefix }: { credit: ImageCredit; prefix: string }) {
  const source = credit.source_url ? contentBlockLink(credit.source_url) : null;
  const terms = licenseUrl(credit.license);
  return (
    <span>
      {prefix}
      {source ? (
        <a href={source} target="_blank" rel="noopener noreferrer" className="underline">{credit.author}</a>
      ) : credit.author}
      {" ("}
      {terms ? (
        <a href={terms} target="_blank" rel="noopener noreferrer" className="underline">{credit.license}</a>
      ) : credit.license}
      {")"}
    </span>
  );
}

/**
 * One renderer for every structured body on the site. The admin preview and the public page
 * both draw through this, which is the only reason a preview can be trusted to match what a
 * reader will actually see.
 *
 * `headingStart` numbers the level-2 headings (`section-1`, `section-2`, ...) so an article's
 * table of contents can point at them; a caller that renders the body in slices passes each
 * slice the count that precedes it. Left out, headings carry no ids, which is what the legal
 * pages want.
 */
export function ContentBlocks({
  blocks, labels, headingStart,
}: {
  blocks: readonly RichContentBlock[];
  labels?: ContentBlockLabels;
  headingStart?: number;
}) {
  let sections = headingStart ?? 0;
  return <>{blocks.map((block, index) => {
    if (block.type === "heading") {
      if (block.level === 3) return <h3 key={index} className="pt-2 text-lg font-semibold">{block.text}</h3>;
      const id = headingStart === undefined ? undefined : `section-${++sections}`;
      return <h2 key={index} id={id} className="scroll-mt-24 pt-4 text-xl font-bold">{block.text}</h2>;
    }
    if (block.type === "paragraph") return <p key={index} className="whitespace-pre-wrap leading-8">{block.text}</p>;
    if (block.type === "list") {
      const List = block.ordered ? "ol" : "ul";
      return <List key={index} className={`space-y-2 pl-6 leading-8 ${block.ordered ? "list-decimal" : "list-disc"}`}>{block.items.map((text, i) => <li key={i}>{text}</li>)}</List>;
    }
    if (block.type === "image") {
      const src = contentImageSrc(block.src);
      if (!src) return null;
      const caption = block.caption?.trim() ?? "";
      return (
        <figure key={index} className="my-2">
          {/* Plain <img>: no image optimizer in the standalone build; the stored size reserves the box. */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={src} alt={block.alt} width={block.width} height={block.height} loading="lazy" decoding="async" className="h-auto w-full rounded-2xl" />
          {caption || block.credit ? (
            <figcaption className="mt-2 text-sm leading-6 text-[var(--muted)]">
              {caption}
              {caption && block.credit ? " · " : null}
              {block.credit ? <ImageCreditLine credit={block.credit} prefix={labels?.imageCredit ?? ""} /> : null}
            </figcaption>
          ) : null}
        </figure>
      );
    }
    if (block.type === "table") {
      const caption = block.caption?.trim() ?? "";
      // A wide table scrolls inside its own box; the page must never scroll sideways for it.
      return (
        <div key={index} className="overflow-x-auto">
          <table className="w-full border-collapse text-sm">
            {caption ? <caption className="caption-bottom pt-2 text-left text-[var(--muted)]">{caption}</caption> : null}
            <thead>
              <tr>{block.header.map((cell, i) => <th key={i} scope="col" className="border-b-2 border-[var(--line)] px-3 py-2 text-left font-semibold">{cell}</th>)}</tr>
            </thead>
            <tbody>
              {block.rows.map((row, r) => (
                <tr key={r}>{row.map((cell, c) => <td key={c} className="border-b border-[var(--line)] px-3 py-2 align-top leading-6">{cell}</td>)}</tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }
    if (block.type === "callout") {
      const title = block.title?.trim() ?? "";
      const tone = labels?.[block.tone] ?? "";
      const heading = [tone, title].filter(Boolean).join(" · ");
      return (
        <aside key={index} role="note" className={`rounded-2xl border border-l-4 border-[var(--line)] bg-[var(--paper)] px-4 py-3 leading-7 ${TONE_CLASSES[block.tone]}`}>
          {heading ? <p className="text-sm font-semibold">{heading}</p> : null}
          <p className="whitespace-pre-wrap">{block.text}</p>
        </aside>
      );
    }
    const href = contentBlockLink(block.url);
    if (!href) return null;
    const external = !href.startsWith("mailto:") && !sameSite(href);
    return <p key={index}><a href={href} target={external ? "_blank" : undefined} rel={external ? "noopener noreferrer" : undefined} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{block.text}</a></p>;
  })}</>;
}
