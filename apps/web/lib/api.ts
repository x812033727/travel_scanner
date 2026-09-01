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
  adults: "成人數",
  children: "兒童數",
  rooms: "房間數",
  budget_twd: "整趟總預算",
  hotel_min_nightly_twd: "每晚最低價格",
  hotel_max_nightly_twd: "每晚最高價格",
  hotel_min_rating: "最低星級",
  hotel_min_review_score: "最低住客評分",
  hotel_min_review_count: "最低評論數",
  max_station_walk_minutes: "車站步行上限",
  notes: "其他補充",
  search_id: "搜尋結果",
  plan_id: "行程方案",
  email: "Email",
  password: "密碼",
  target_price: "目標價格",
  resource_id: "追蹤項目",
  resource_type: "追蹤類型",
};

const CODE_MESSAGES: Record<string, string> = {
  authentication_required: "請先登入後再繼續",
  invalid_credentials: "Email 或密碼不正確",
  email_exists: "這個 Email 已經註冊",
  invalid_token: "登入狀態已失效，請重新登入",
  inactive_user: "這個帳號目前無法使用",
  alert_exists: "這個項目已經建立價格通知",
  alert_not_found: "找不到這筆價格通知",
  alert_resource_not_found: "找不到可追蹤的價格項目",
  alert_limit_reached: "已達價格通知數量上限",
  alert_update_empty: "請至少修改一個價格通知欄位",
  line_not_configured: "LINE 價格通知尚未啟用",
  line_not_linked: "尚未連結 LINE 帳號",
  line_friend_required: "請重新加入 LINE 官方帳號好友",
  line_delivery_failed: "LINE 測試訊息暫時無法送出",
  invalid_line_link_token: "LINE 連結已失效，請重新綁定",
  trip_not_found: "找不到這個旅程",
  weather_not_configured: "Google Weather 尚未設定",
  weather_api_not_enabled: "Google Weather API 尚未啟用或金鑰權限不足",
  weather_location_unavailable: "旅程尚無可用座標，請先確認行程地點",
  weather_rate_limited: "Google Weather 查詢額度暫時不足",
  weather_provider_unavailable: "Google Weather 暫時無法回應",
  search_not_found: "找不到這次搜尋",
  rate_limited: "操作太頻繁，請稍後再試",
  rate_limit_exceeded: "操作太頻繁，請稍後再試",
  rate_limit_unavailable: "限流服務暫時無法使用，請稍後再試",
  insufficient_uses: "可用次數不足，請先取得更多次數",
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
  else if (field === "email" || /valid email|email address/i.test(rawMessage)) message = "格式不正確";
  else if (field === "password" && (type === "string_too_short" || /at least/i.test(rawMessage))) message = "至少需要 10 個字元";
  else if (type.includes("date") || /valid date/i.test(rawMessage)) message = "請選擇有效日期";
  else if (type === "string_too_short") message = "內容太短";
  else if (type === "string_too_long") message = "內容太長";

  return `${label}：${message}`;
}

export function apiProblemMessage(problem: unknown, status: number): string {
  if (problem && typeof problem === "object") {
    const code = (problem as { code?: unknown }).code;
    if (typeof code === "string" && CODE_MESSAGES[code]) return CODE_MESSAGES[code];
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

