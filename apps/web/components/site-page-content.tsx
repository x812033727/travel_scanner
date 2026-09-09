import { requirementKeys, sitePageLink, type SitePageDocument } from "@/lib/site-pages";

export function SitePageContent({ document, labels }: {
  document: SitePageDocument;
  labels: Record<typeof requirementKeys[number], string> & { effectiveDate: string };
}) {
  return <article className="space-y-6 break-words [overflow-wrap:anywhere]">
    <header><h1 className="text-3xl font-bold">{document.title}</h1>
      <p className="mt-3 leading-7 text-[var(--muted)]">{document.description}</p>
      {document.effective_date && <p className="mt-3 text-sm text-[var(--muted)]">{labels.effectiveDate}: <time dateTime={document.effective_date}>{document.effective_date}</time></p>}
    </header>
    {document.blocks.map((block, index) => {
      if (block.type === "heading") return block.level === 2 ? <h2 key={index} className="pt-4 text-xl font-bold">{block.text}</h2> : <h3 key={index} className="pt-2 text-lg font-semibold">{block.text}</h3>;
      if (block.type === "paragraph") return <p key={index} className="whitespace-pre-wrap leading-8">{block.text}</p>;
      if (block.type === "list") {
        const List = block.ordered ? "ol" : "ul";
        return <List key={index} className={`space-y-2 pl-6 leading-8 ${block.ordered ? "list-decimal" : "list-disc"}`}>{block.items.map((text, i) => <li key={i}>{text}</li>)}</List>;
      }
      const href = sitePageLink(block.url);
      return href ? <p key={index}><a href={href} target={href.startsWith("mailto:") ? undefined : "_blank"} rel="noopener noreferrer" className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{block.text}</a></p> : null;
    })}
    {requirementKeys.some((key) => document.requirements[key].trim()) && <dl className="space-y-4 border-t border-[var(--line)] pt-6">{requirementKeys.filter((key) => document.requirements[key].trim()).map((key) => <div key={key}><dt className="font-semibold">{labels[key]}</dt><dd className="mt-1 whitespace-pre-wrap leading-7">{document.requirements[key]}</dd></div>)}</dl>}
  </article>;
}
