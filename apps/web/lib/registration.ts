export type RegistrationAvailability = "open" | "closed" | "unavailable";

export async function getRegistrationAvailability(): Promise<RegistrationAvailability> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${apiBase}/api/v1/auth/registration-status`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (!response.ok) return "unavailable";
    const payload: unknown = await response.json();
    if (
      typeof payload !== "object" ||
      payload === null ||
      typeof (payload as { registration_enabled?: unknown }).registration_enabled !== "boolean"
    ) return "unavailable";
    return (payload as { registration_enabled: boolean }).registration_enabled ? "open" : "closed";
  } catch {
    return "unavailable";
  }
}
