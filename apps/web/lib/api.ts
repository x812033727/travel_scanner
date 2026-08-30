export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/travel${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!response.ok) {
    const problem = await response.json().catch(() => ({ detail: "發生未知錯誤" }));
    throw new Error(problem.detail || `Request failed (${response.status})`);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const twd = new Intl.NumberFormat("zh-TW", { style: "currency", currency: "TWD", maximumFractionDigits: 0 });

