import {
  contentBlockLink,
  contentImageSrc,
  licenseUrl,
  type CalloutTone,
  type ImageCredit,
  type RichContentBlock,
} from "@/lib/content-blocks";
import { siteUrl } from "@/lib/seo";
import { GuideImage } from "@/components/guides/guide-image";
import { GuideCodeBlock, type CodeLabels } from "@/components/guide-code-block";
import { TermLink, type TermLinkLabels } from "@/components/guides/term-link";
import type { ArticleReference } from "@/lib/guide-series";

/** The words the renderer cannot invent: a credit prefix and one name per callout tone. A
 *  caller that renders only the four shared blocks (the legal pages) passes nothing. */
export type ContentBlockLabels = {
  imageCredit: string;
  /** The toggle over an image's folded long description. Without it the disclosure is named
   *  after the picture (its alt) rather than drawn blank. */
  imageDescription?: string;
  tip: string;
  warning: string;
  info: string;
  code?: CodeLabels;
  /** The headings over a summary card and a FAQ section drawn in the body (the admin
   *  preview); the article page hoists both out and names them itself. */
  summary?: string;
  faq?: string;
};

/** The width a 1600px-wide diagram is drawn at so its smallest label reaches the reader.
 *  `pack_ingest.MIN_LABEL_PX` is 15, and 15 * 1180/1600 = 11.1 CSS px; below about 11 a
 *  Han or Hangul glyph stops resolving. A diagram authored narrower keeps its own width. */
const DIAGRAM_READABLE_WIDTH = 1180;

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

/** The article's answer, as a card: the two to five sentences a reader takes away. `id` is
 *  the article page's, so its speakable selector points here; the preview passes none. */
export function SummaryCard({ items, heading, id }: { items: readonly string[]; heading?: string; id?: string }) {
  return (
    <aside id={id} aria-label={heading} className="app-summary-card rounded-2xl p-4 md:p-5">
      {heading ? <p className="text-xs font-bold uppercase tracking-wide text-[var(--muted)]">{heading}</p> : null}
      <ul className="mt-2 list-disc space-y-1.5 pl-5">
        {items.map((item, index) => <li key={index}>{item}</li>)}
      </ul>
    </aside>
  );
}

/** Questions readers ask, each answered in place. A native disclosure per question: the
 *  answers are in the HTML for a crawler and a reader without JavaScript, folded for one
 *  scanning the list. */
export function FaqSection({ items, heading, id }: { items: readonly { question: string; answer: string }[]; heading?: string; id?: string }) {
  return (
    <section id={id} aria-label={heading} className="border-t border-[var(--line)] pt-6">
      {heading ? <h2 className="text-lg font-semibold">{heading}</h2> : null}
      <div className="mt-2 divide-y divide-[var(--line)]">
        {items.map((item, index) => (
          <details key={index} className="py-2">
            <summary className="flex min-h-11 cursor-pointer items-center font-semibold">{item.question}</summary>
            <p className="mt-2 whitespace-pre-wrap leading-7 text-[var(--muted)]">{item.answer}</p>
          </details>
        ))}
      </div>
    </section>
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
  blocks, labels, headingStart, articleLinks = [], locale = "en", termLabels,
}: {
  blocks: readonly RichContentBlock[];
  labels?: ContentBlockLabels;
  headingStart?: number;
  articleLinks?: readonly ArticleReference[];
  locale?: string;
  /** The words of the definition card under a term link; without them a term is a plain link. */
  termLabels?: TermLinkLabels;
}) {
  // Heading ids are decided in one pass before rendering: level-2 headings continue the
  // sequence the caller started, and level-3 headings count within their section
  // (`section-3-2`) so a citation can point at a sub-answer.
  const headingIds = new Map<number, string>();
  if (headingStart !== undefined) {
    let section = headingStart;
    let subsection = 0;
    blocks.forEach((block, index) => {
      if (block.type !== "heading") return;
      if (block.level === 3) {
        headingIds.set(index, `section-${section}-${++subsection}`);
      } else {
        subsection = 0;
        headingIds.set(index, `section-${++section}`);
      }
    });
  }
  return <>{blocks.map((block, index) => {
    if (block.type === "code") return <GuideCodeBlock key={index} block={block} labels={labels?.code} />;
    if (block.type === "rich_paragraph") return <p key={index} className="whitespace-pre-wrap leading-8">{block.inlines.map((node, i) => {
      if (node.type === "code") return <code key={i} className="rounded bg-[var(--paper)] px-1 font-mono text-[0.92em]">{node.text}</code>;
      if (node.type === "article") {
        const target = articleLinks.find(ref => ref.slug === node.slug && ref.kind === node.kind);
        if (!target) return <span key={i}>{node.text}</span>;
        const path = target.kind === "life" ? `/life/${target.slug}` : `/guides/${target.kind}/${target.slug}`;
        const href = `/${locale}${path}`;
        // A target with a published description gets the definition card; one without (an
        // older API, a catalogue reference) stays the plain link it always was.
        if (target.description && termLabels) {
          return <TermLink key={i} href={href} text={node.text} title={target.title} description={target.description} labels={termLabels} />;
        }
        return <a key={i} href={href} className="text-[var(--teal)] underline underline-offset-4">{node.text}</a>;
      }
      if (node.type === "link") {
        const href = contentBlockLink(node.url);
        if (!href) return <span key={i}>{node.text}</span>;
        const external = !sameSite(href);
        const parsed = new URL(href);
        const targetHref = external ? href : parsed.pathname + parsed.search + parsed.hash;
        return <a key={i} href={targetHref} target={external ? "_blank" : undefined} rel={external ? "noopener noreferrer" : undefined} className="text-[var(--teal)] underline underline-offset-4">{node.text}</a>;
      }
      return <span key={i}>{node.text}</span>;
    })}</p>;
    if (block.type === "heading") {
      const id = headingIds.get(index);
      if (block.level === 3) return <h3 key={index} id={id} className="scroll-mt-24 pt-2 text-lg font-semibold">{block.text}</h3>;
      return <h2 key={index} id={id} className="scroll-mt-24 pt-4 text-xl font-bold">{block.text}</h2>;
    }
    if (block.type === "paragraph") return <p key={index} className="whitespace-pre-wrap leading-8">{block.text}</p>;
    if (block.type === "summary") return <SummaryCard key={index} items={block.items} heading={labels?.summary} />;
    if (block.type === "faq") return <FaqSection key={index} items={block.items} heading={labels?.faq} />;
    if (block.type === "list") {
      const List = block.ordered ? "ol" : "ul";
      return <List key={index} className={`space-y-2 pl-6 leading-8 ${block.ordered ? "list-decimal" : "list-disc"}`}>{block.items.map((text, i) => <li key={i}>{text}</li>)}</List>;
    }
    if (block.type === "image") {
      const src = contentImageSrc(block.src);
      if (!src) return null;
      const caption = block.caption?.trim() ?? "";
      // A diagram's long description (its `<desc>`: the fares, times and labels it draws) goes
      // under the caption as a native disclosure, folded. The text is in the HTML for a
      // crawler and a screen reader while first paint stays what it was. Text only: the SVG
      // itself is never inlined, because `contentImageSrc` vets the path, not the file.
      const description = block.description?.trim() ?? "";
      // A diagram is drawn on a 1600x900 canvas, but the article column tops out at 728px at
      // every viewport, so the 15px floor `pack_ingest` enforces reaches the reader at 6.8px
      // on a laptop and 3.1px on a phone. Fitting it to the column is what makes it
      // decorative. Give it its own scroller and a width where that floor clears 11px; a
      // photograph keeps fitting the column, because its detail does not live in 15px text.
      const diagram = src.endsWith(".svg");
      const image = (
        <GuideImage
          src={src} alt={block.alt} width={block.width} height={block.height}
          loading="lazy" decoding="async"
          className={diagram ? "h-auto rounded-2xl" : "h-auto w-full rounded-2xl"}
          // `maxWidth` rides with the width rather than sitting in a class: Tailwind's
          // preflight caps every image at 100% of its box, and a utility that only this
          // branch uses is one dead-code pass away from never reaching the stylesheet.
          style={diagram
            ? { width: Math.min(block.width ?? DIAGRAM_READABLE_WIDTH, DIAGRAM_READABLE_WIDTH), maxWidth: "none" }
            : undefined}
        />
      );
      return (
        <figure key={index} className="my-2">
          {diagram ? (
            // `tabIndex` so the box can be scrolled from the keyboard: it holds no focusable
            // child, and only Firefox focuses a scroll container on its own. It carries no
            // `aria-label`; the image inside already has the alt, and naming the group would
            // read it out twice.
            //
            // `-mx-5 px-5` cancels the article's own gutter (`main` is `px-5`, 20px at every
            // breakpoint) and puts it back inside the scroller. The window into the diagram
            // is then the full 375px of a phone rather than 335, which is what lets a column
            // of the common three-up decoder -- 490 canvas px, 361 on screen -- be seen whole;
            // at 335 none of its three columns ever was. The padding keeps the diagram's left
            // edge lined up with the text at rest, and the right edge running off the screen
            // is the cue that there is more. No `100vw`: it counts the scrollbar and would
            // give the page the sideways scroll this is meant to avoid.
            //
            // From `xl` the window stops being the constraint. `main` is `max-w-3xl` with
            // `px-5`, so the column the figure sits in is 768 - 40 = 728px, and
            // (1180 - 728) / 2 = 226px a side opens the box to the diagram's full width. The
            // gutter inside it goes with it: nothing overflows, so there is nothing to
            // scroll. 1280px is the narrowest breakpoint where that margin is certainly
            // free -- even with a classic 15px scrollbar the page has 268px a side to give
            // and only 226 is taken.
            // The gutter comes back on the left only. That one lines the diagram up with the
            // text before any scrolling; a matching one on the right earns nothing and costs
            // the end of the scroll, which stopped on 20px of blank with the last column's
            // leading edge pushed out of frame.
            <div tabIndex={0} role="group" className="-mx-5 overflow-x-auto pl-5 xl:-mx-[226px] xl:pl-0">{image}</div>
          ) : image}
          {caption || block.credit ? (
            <figcaption className="mt-2 text-sm leading-6 text-[var(--muted)]">
              {caption}
              {caption && block.credit ? " · " : null}
              {block.credit ? <ImageCreditLine credit={block.credit} prefix={labels?.imageCredit ?? ""} /> : null}
            </figcaption>
          ) : null}
          {description ? (
            <details className="text-sm leading-6 text-[var(--muted)]">
              <summary className="cursor-pointer py-2.5 font-semibold">{labels?.imageDescription ?? block.alt}</summary>
              <p className="whitespace-pre-wrap pb-2">{description}</p>
            </details>
          ) : null}
        </figure>
      );
    }
    if (block.type === "table") {
      const caption = block.caption?.trim() ?? "";
      // A wide table scrolls inside its own box; the page must never scroll sideways for it.
      return (
        <div key={index} className="overflow-x-auto">
          <table className="w-full border-collapse text-sm [overflow-wrap:normal]">
            {caption ? <caption className="caption-bottom pt-2 text-left text-[var(--muted)]">{caption}</caption> : null}
            <thead>
              <tr>{block.header.map((cell, i) => <th key={i} scope="col" className="min-w-28 border-b-2 border-[var(--line)] px-3 py-2 text-left font-semibold">{cell}</th>)}</tr>
            </thead>
            <tbody>
              {block.rows.map((row, r) => (
                <tr key={r}>{row.map((cell, c) => <td key={c} className="min-w-28 border-b border-[var(--line)] px-3 py-2 align-top leading-6">{cell}</td>)}</tr>
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
    // Only a link block is drawn as a link. Anything the renderer does not know -- a partner
    // link that escaped `splitGuideBlocks`, a block from a newer API -- draws nothing rather
    // than falling through here and putting its URL on the page unqualified.
    if (block.type !== "link") return null;
    const href = contentBlockLink(block.url);
    if (!href) return null;
    const external = !href.startsWith("mailto:") && !sameSite(href);
    return <p key={index}><a href={href} target={external ? "_blank" : undefined} rel={external ? "noopener noreferrer" : undefined} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{block.text}</a></p>;
  })}</>;
}
