import { contentBlockLink, type ContentBlock } from "@/lib/content-blocks";

/**
 * One renderer for every structured body on the site. The admin preview and the public page
 * both draw through this, which is the only reason a preview can be trusted to match what a
 * reader will actually see.
 */
export function ContentBlocks({ blocks }: { blocks: ContentBlock[] }) {
  return <>{blocks.map((block, index) => {
    if (block.type === "heading") {
      return block.level === 2
        ? <h2 key={index} className="pt-4 text-xl font-bold">{block.text}</h2>
        : <h3 key={index} className="pt-2 text-lg font-semibold">{block.text}</h3>;
    }
    if (block.type === "paragraph") return <p key={index} className="whitespace-pre-wrap leading-8">{block.text}</p>;
    if (block.type === "list") {
      const List = block.ordered ? "ol" : "ul";
      return <List key={index} className={`space-y-2 pl-6 leading-8 ${block.ordered ? "list-decimal" : "list-disc"}`}>{block.items.map((text, i) => <li key={i}>{text}</li>)}</List>;
    }
    const href = contentBlockLink(block.url);
    return href ? <p key={index}><a href={href} target={href.startsWith("mailto:") ? undefined : "_blank"} rel="noopener noreferrer" className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{block.text}</a></p> : null;
  })}</>;
}
