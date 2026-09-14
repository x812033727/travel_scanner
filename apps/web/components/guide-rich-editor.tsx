"use client";

import { codeLanguages, type CodeBlock, type InlineNode, type RichParagraphBlock } from "@/lib/content-blocks";
import { seriesCopy } from "@/lib/guide-series-copy";

export function GuideRichEditor({ block, onChange, locale }: {
  block: CodeBlock | RichParagraphBlock; onChange: (block: CodeBlock | RichParagraphBlock) => void; locale: string;
}) {
  const copy = seriesCopy(locale);
  const control = "min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] p-2";
  if (block.type === "code") return <div className="space-y-3">
    <label className="grid gap-2">{copy.label}<input className={control} value={block.label} onChange={e => onChange({ ...block, label: e.target.value })} /></label>
    <label className="grid gap-2">{copy.language}<select className={control} value={block.language} onChange={e => onChange({ ...block, language: e.target.value as CodeBlock["language"] })}>
      {codeLanguages.map(language => <option key={language}>{language}</option>)}
    </select></label>
    <label className="grid gap-2">{copy.code}<textarea spellCheck={false} className={`${control} font-mono`} rows={10} value={block.code} onChange={e => onChange({ ...block, code: e.target.value })} /></label>
  </div>;
  function replace(index: number, node: InlineNode) {
    if (block.type !== "rich_paragraph") return;
    onChange({ ...block, inlines: block.inlines.map((item, i) => i === index ? node : item) });
  }
  function move(index: number, delta: number) {
    if (block.type !== "rich_paragraph") return;
    const inlines = [...block.inlines];
    [inlines[index], inlines[index + delta]] = [inlines[index + delta], inlines[index]];
    onChange({ ...block, inlines });
  }
  return <div className="space-y-3">{block.inlines.map((node, index) => <fieldset key={index} className="space-y-3 rounded-xl border border-[var(--line)] p-3">
    <legend>{index + 1}</legend>
    <select aria-label={`${copy.kind} ${index + 1}`} className={control} value={node.type} onChange={e => {
      const type = e.target.value as InlineNode["type"];
      replace(index, type === "article" ? { type, text: node.text, kind: "life", slug: "" }
        : type === "link" ? { type, text: node.text, url: "" } : { type, text: node.text });
    }}>
      <option value="text">{copy.text}</option><option value="code">{copy.inlineCode}</option><option value="article">{copy.article}</option><option value="link">{copy.external}</option>
    </select>
    <label className="grid gap-2">{copy.text}<textarea className={control} value={node.text} onChange={e => replace(index, { ...node, text: e.target.value })} /></label>
    {node.type === "article" ? <>
      <label className="grid gap-2">{copy.kind}<select className={control} value={node.kind} onChange={e => replace(index, { ...node, kind: e.target.value as typeof node.kind })}>
        <option value="life">life</option><option value="howto">howto</option><option value="intel">intel</option>
      </select></label>
      <label className="grid gap-2">{copy.slug}<input className={control} value={node.slug} onChange={e => replace(index, { ...node, slug: e.target.value })} /></label>
    </> : null}
    {node.type === "link" ? <label className="grid gap-2">{copy.url}<input className={control} value={node.url} onChange={e => replace(index, { ...node, url: e.target.value })} /></label> : null}
    <div className="flex flex-wrap gap-2">
      <button type="button" className="min-h-11 px-2" disabled={index === 0} onClick={() => move(index, -1)}>{copy.up}</button>
      <button type="button" className="min-h-11 px-2" disabled={index === block.inlines.length - 1} onClick={() => move(index, 1)}>{copy.down}</button>
      <button type="button" className="min-h-11 px-2" disabled={block.inlines.length === 1} onClick={() => onChange({ ...block, inlines: block.inlines.filter((_, i) => i !== index) })}>{copy.remove}</button>
    </div>
  </fieldset>)}
    <button type="button" className="min-h-11 rounded-lg border border-[var(--line)] px-3" onClick={() => onChange({ ...block, inlines: [...block.inlines, { type: "text", text: "" }] })}>{copy.add}</button>
  </div>;
}
