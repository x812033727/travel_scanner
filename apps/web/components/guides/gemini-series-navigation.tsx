import { GeminiNavigation } from "@/components/gemini-series/navigation";
import { geminiSeriesCopy } from "@/lib/gemini-series-copy";
import type { VisibleGeminiSeries } from "@/lib/gemini-series-projection";

export function SeriesNavigation({ series, number, position }: { series: VisibleGeminiSeries; number: number; position: "top" | "bottom" }) {
  return <GeminiNavigation series={series} number={number} position={position} copy={geminiSeriesCopy} />;
}
