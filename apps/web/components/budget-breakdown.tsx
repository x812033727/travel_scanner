import { AlertTriangle, CircleDollarSign } from "lucide-react";
import { twd } from "@/lib/api";

type CostComponent = {
  category: string;
  label: string;
  amount: string | number;
  confidence: string;
};

export type BudgetCost = {
  confirmed_cost: string | number;
  estimated_cost: string | number;
  total_cost: string | number;
  components: CostComponent[];
};

export function BudgetBreakdown({ cost, budget }: { cost: BudgetCost; budget?: number }) {
  const total = Number(cost.total_cost);
  const confirmed = Number(cost.confirmed_cost);
  const estimated = Number(cost.estimated_cost);
  const denominator = budget || total || 1;
  const confirmedWidth = Math.min(100, (confirmed / denominator) * 100);
  const estimatedWidth = Math.min(100 - confirmedWidth, (estimated / denominator) * 100);
  const difference = budget ? budget - total : undefined;

  return (
    <div className="mt-3 rounded-2xl bg-[var(--paper)] p-3.5">
      {difference !== undefined && (
        <p className={`flex items-center gap-2 text-sm font-semibold ${difference >= 0 ? "text-[var(--teal-dark)]" : "text-red-700"}`}>
          {difference >= 0 ? <CircleDollarSign size={16} /> : <AlertTriangle size={16} />}
          {difference >= 0 ? `預算尚餘 ${twd.format(difference)}` : `超出預算 ${twd.format(Math.abs(difference))}`}
        </p>
      )}
      <div
        className="mt-3 flex h-2.5 overflow-hidden rounded-full bg-[#dfe7e2]"
        role="img"
        aria-label={budget ? `已使用總預算的 ${Math.round((total / budget) * 100)}%` : "報價與估算費用比例"}
      >
        <span className="bg-[var(--teal)]" style={{ width: `${confirmedWidth}%` }} />
        <span className="bg-[var(--coral)]" style={{ width: `${estimatedWidth}%` }} />
      </div>
      <div className="mt-2 flex flex-wrap justify-between gap-2 text-xs text-[var(--muted)]">
        <span>報價項目 {twd.format(confirmed)}</span>
        <span>估算項目 {twd.format(estimated)}</span>
      </div>
      <details className="mt-2 text-xs">
        <summary className="cursor-pointer font-semibold text-[var(--teal-dark)]">查看完整費用拆解</summary>
        <dl className="mt-2 space-y-1.5 border-t border-[var(--line)] pt-2">
          {cost.components.map((component) => (
            <div key={`${component.category}-${component.label}`} className="flex justify-between gap-3">
              <dt>{component.label}{component.confidence === "estimated" ? "（估算）" : ""}</dt>
              <dd className="font-medium">{twd.format(Number(component.amount))}</dd>
            </div>
          ))}
        </dl>
      </details>
    </div>
  );
}
