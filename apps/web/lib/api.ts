export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly code?: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

const FIELD_LABELS: Record<string, string> = {
  name: "旅程名稱",
  destination_name: "目的地",
  destination_place_id: "目的地",
  start_date: "開始日期",
  end_date: "結束日期",
  route_preference: "大眾運輸偏好",
  search_id: "搜尋結果",
  plan_id: "行程方案",
};

function validationMessage(issue: unknown): string {
  if (!issue || typeof issue !== "object") return "輸入內容格式不正確";
  const item = issue as { loc?: unknown; msg?: unknown; type?: unknown };
  const location = Array.isArray(item.loc) ? item.loc : [];
  const field = [...location].reverse().find((part): part is string => typeof part === "string" && part !== "body");
  const label = field ? FIELD_LABELS[field] || field : "輸入內容";
  const type = typeof item.type === "string" ? item.type : "";
  const rawMessage = typeof item.msg === "string" ? item.msg : "輸入內容格式不正確";
  let message = rawMessage.replace(/^Value error,\s*/i, "");

  if (type === "missing" || /field required/i.test(rawMessage)) message = "必填";
  else if (type.includes("date") || /valid date/i.test(rawMessage)) message = "請選擇有效日期";
  else if (type === "string_too_short") message = "內容太短";
  else if (type === "string_too_long") message = "內容太長";

  return `${label}：${message}`;
}

export function apiProblemMessage(problem: unknown, status: number): string {
  if (problem && typeof problem === "object") {
    const detail = (problem as { detail?: unknown }).detail;
    if (typeof detail === "string" && detail.trim()) return detail;
    if (Array.isArray(detail) && detail.length > 0) return detail.map(validationMessage).join("；");
    if (detail && typeof detail === "object") {
      const message = (detail as { message?: unknown }).message;
      if (typeof message === "string" && message.trim()) return message;
    }
  }
  return `請求失敗（HTTP ${status}）`;
}

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/travel${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!response.ok) {
    const problem: unknown = await response.json().catch(() => undefined);
    const code = problem && typeof problem === "object" && typeof (problem as { code?: unknown }).code === "string"
      ? (problem as { code: string }).code
      : undefined;
    throw new ApiError(
      apiProblemMessage(problem, response.status),
      response.status,
      code,
    );
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export function isUsageInsufficient(reason: unknown): boolean {
  return reason instanceof ApiError && reason.code === "insufficient_uses";
}

export const twd = new Intl.NumberFormat("zh-TW", { style: "currency", currency: "TWD", maximumFractionDigits: 0 });

