import { GeminiDirectory } from "@/components/gemini-series/directory";
import { geminiSeriesCopy } from "@/lib/gemini-series-copy";
import type { VisibleGeminiSeries } from "@/lib/gemini-series-projection";

export function GeminiSeriesIndex({ series }: { series: VisibleGeminiSeries }) {
  return <GeminiDirectory series={series} copy={geminiSeriesCopy} />;
}
