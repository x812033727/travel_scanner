import { GeminiDirectory } from "@/components/gemini-series/directory";
import { GeminiNavigation } from "@/components/gemini-series/navigation";
import { GuideCodeBlock } from "@/components/guide-code-block";
import type { VisibleGeminiSeries } from "@/lib/gemini-series-projection";
import type { GeminiSeriesCopy } from "@/lib/gemini-series-copy";

export type Props = { series: VisibleGeminiSeries; number?: number; copy: GeminiSeriesCopy };
export const sample = 'if True:\n\tprint("原始縮排 <script>只顯示文字</script>")\n' + '#'.repeat(160);

/** Isolated component fixture, never a route or API of the product. */
export function Page({ series, number, copy }: Props) {
  const article = series.articles.find(entry => entry.number === number);
  return <main className="mx-auto min-w-0 max-w-4xl space-y-6 p-4 sm:p-8">
    <h1 className="text-2xl font-bold [overflow-wrap:anywhere]">{article?.title ?? series.title}</h1>
    {number ? <>
      <GeminiNavigation series={series} number={number} position="top" copy={copy} />
      <h2 id="section-3">測試用章節</h2>
      <GuideCodeBlock block={{ type: "code", language: "python", label: "example.py", code: sample }} labels={{ copy: "複製", copied: "已複製", copyFailed: "請手動複製" }} />
      <GeminiNavigation series={series} number={number} position="bottom" copy={copy} />
    </> : <GeminiDirectory series={series} copy={copy} />}
  </main>;
}
