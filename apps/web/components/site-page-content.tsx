import { ContentBlocks } from "@/components/content-blocks";
import { requirementKeys, type SitePageDocument } from "@/lib/site-pages";

export function SitePageContent({ document, labels }: {
  document: SitePageDocument;
  labels: Record<typeof requirementKeys[number], string> & { effectiveDate: string };
}) {
  return <article className="space-y-6 break-words [overflow-wrap:anywhere]">
    <header><h1 className="text-3xl font-bold">{document.title}</h1>
      <p className="mt-3 leading-7 text-[var(--muted)]">{document.description}</p>
      {document.effective_date && <p className="mt-3 text-sm text-[var(--muted)]">{labels.effectiveDate}: <time dateTime={document.effective_date}>{document.effective_date}</time></p>}
    </header>
    <ContentBlocks blocks={document.blocks} />
    {requirementKeys.some((key) => document.requirements[key].trim()) && <dl className="space-y-4 border-t border-[var(--line)] pt-6">{requirementKeys.filter((key) => document.requirements[key].trim()).map((key) => <div key={key}><dt className="font-semibold">{labels[key]}</dt><dd className="mt-1 whitespace-pre-wrap leading-7">{document.requirements[key]}</dd></div>)}</dl>}
  </article>;
}
