export type AdminNavGroup = "overview" | "content" | "community" | "operations" | "system";

export type AdminNavigationItem = {
  key: string;
  href: string;
  group: AdminNavGroup;
  label?: string;
  capability?: string;
  badge_count?: number;
  badge_key?: string;
};

export type AdminServiceState = {
  status: "healthy" | "degraded" | "unavailable" | "disabled" | "unknown";
  label?: string;
  detail?: string;
};

export type AdminBootstrap = {
  user?: { id?: string; email?: string };
  admin_roles: string[];
  admin_capabilities: string[];
  navigation: AdminNavigationItem[];
  pending_counts: Record<string, number>;
  system_status: Record<string, AdminServiceState>;
  environment: string;
  can_deploy: boolean;
  can_manage_database: boolean;
};

export const fallbackAdminNavigation: AdminNavigationItem[] = [
  { key: "dashboard", href: "/admin", group: "overview", capability: "dashboard.read" },
  { key: "hotspots", href: "/admin/hotspots", group: "content", capability: "content.read" },
  { key: "foods", href: "/admin/foods", group: "content", capability: "content.read" },
  { key: "hotels", href: "/admin/hotels", group: "content", capability: "content.read" },
  { key: "catalogReview", href: "/admin/catalog-review", group: "content", capability: "content.read" },
  { key: "travelServices", href: "/admin/travel-services", group: "content", capability: "content.read" },
  { key: "community", href: "/admin/community", group: "community", capability: "community.read" },
  { key: "pets", href: "/admin/pet-friendly", group: "community", capability: "community.read" },
  { key: "partners", href: "/admin/partners", group: "operations", capability: "content.read" },
  { key: "analytics", href: "/admin/analytics", group: "operations", capability: "analytics.read" },
  { key: "users", href: "/admin/users", group: "operations", capability: "users.read" },
  { key: "usage", href: "/admin/usage-settings", group: "operations", capability: "settings.read" },
  { key: "layout", href: "/admin/layout-settings", group: "operations", capability: "settings.read" },
  { key: "uiText", href: "/admin/ui-text", group: "operations", capability: "settings.read" },
  { key: "system", href: "/admin/system-settings", group: "system", capability: "settings.read" },
  { key: "providers", href: "/admin/settings", group: "operations", capability: "settings.read" },
  { key: "database", href: "/admin/database", group: "system", capability: "database.read" },
  { key: "deployments", href: "/admin/deployments", group: "system", capability: "deploy.read" },
  { key: "audit", href: "/admin/audit", group: "system", capability: "audit.read" },
];

const validGroups = new Set<AdminNavGroup>(["overview", "content", "community", "operations", "system"]);

function stringArray(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((entry): entry is string => typeof entry === "string") : [];
}

function recordOfNumbers(value: unknown): Record<string, number> {
  if (!value || typeof value !== "object") return {};
  return Object.fromEntries(Object.entries(value).filter((entry): entry is [string, number] => typeof entry[1] === "number"));
}

function navigation(value: unknown): AdminNavigationItem[] {
  if (!Array.isArray(value)) return [];
  return value.flatMap((entry) => {
    if (!entry || typeof entry !== "object") return [];
    const row = entry as Record<string, unknown>;
    const rawKey = typeof row.label_key === "string" ? row.label_key : typeof row.key === "string" ? row.key : row.id;
    const aliases: Record<string, string> = {
      travel_services: "travelServices", catalog_review: "catalogReview", pet_friendly: "pets",
      provider_settings: "providers", usage_settings: "usage", layout_settings: "layout",
      ui_text: "uiText", system_settings: "system", petFriendly: "pets",
      providerSettings: "providers", usageSettings: "usage", layoutSettings: "layout",
      systemSettings: "system",
    };
    const key = typeof rawKey === "string" ? aliases[rawKey] ?? rawKey : rawKey;
    if (typeof key !== "string" || typeof row.href !== "string" || !row.href.startsWith("/admin")) return [];
    const group = typeof row.group === "string" && validGroups.has(row.group as AdminNavGroup)
      ? row.group as AdminNavGroup
      : "operations";
    return [{
      key,
      href: row.href,
      group,
      label: typeof row.label === "string" ? row.label : undefined,
      capability: typeof row.capability === "string" ? row.capability : undefined,
      badge_count: typeof row.badge_count === "number" ? row.badge_count : undefined,
      badge_key: typeof row.badge_key === "string" ? row.badge_key : undefined,
    }];
  });
}

function serviceStates(value: unknown): Record<string, AdminServiceState> {
  if (!value || typeof value !== "object") return {};
  return Object.fromEntries(Object.entries(value).flatMap(([key, entry]) => {
    if (!entry || typeof entry !== "object") return [];
    const row = entry as Record<string, unknown>;
    const status = ["healthy", "degraded", "unavailable", "disabled", "unknown"].includes(String(row.status))
      ? row.status as AdminServiceState["status"] : "unknown";
    return [[key, {
      status,
      label: typeof row.label === "string" ? row.label : undefined,
      detail: typeof row.detail === "string" ? row.detail : undefined,
    }]];
  }));
}

/** Accepts the stable contract and tolerates additive/version-skew fields during rolling deploys. */
export function normalizeAdminBootstrap(value: unknown): AdminBootstrap | null {
  if (!value || typeof value !== "object") return null;
  const row = value as Record<string, unknown>;
  const actor = row.actor && typeof row.actor === "object"
    ? row.actor as Record<string, unknown>
    : row.user && typeof row.user === "object" ? row.user as Record<string, unknown> : undefined;
  const capabilities = stringArray(row.admin_capabilities ?? row.capabilities ?? actor?.capabilities);
  const roles = stringArray(row.admin_roles ?? row.roles ?? actor?.roles);
  const nav = navigation(row.navigation ?? row.visible_navigation);
  return {
    user: actor ? {
      id: typeof actor.id === "string" ? actor.id : undefined,
      email: typeof actor.email === "string" ? actor.email : undefined,
    } : undefined,
    admin_roles: roles,
    admin_capabilities: capabilities,
    navigation: nav,
    pending_counts: recordOfNumbers(row.pending_counts ?? row.pending ?? row.counts),
    system_status: serviceStates(row.system_status ?? row.system ?? row.services),
    environment: typeof row.environment === "string" ? row.environment : "production",
    can_deploy: "can_deploy" in row ? row.can_deploy === true : capabilities.includes("deploy.execute"),
    can_manage_database: "can_manage_database" in row
      ? row.can_manage_database === true
      : "can_maintain_database" in row
        ? row.can_maintain_database === true
        : "can_database_maintain" in row
          ? row.can_database_maintain === true
          : capabilities.includes("database.maintain"),
  };
}

export function adminCan(bootstrap: AdminBootstrap | null | undefined, capability: string): boolean {
  if (!bootstrap) return false;
  return bootstrap.admin_capabilities.includes("*")
    || bootstrap.admin_capabilities.includes(capability)
    || bootstrap.admin_capabilities.includes(`admin.${capability}`);
}

export function visibleAdminNavigation(bootstrap: AdminBootstrap): AdminNavigationItem[] {
  if (bootstrap.navigation.length) return bootstrap.navigation;
  return fallbackAdminNavigation.filter((item) => {
    if (item.key === "deployments") return bootstrap.can_deploy;
    if (item.key === "database") return adminCan(bootstrap, "database.read") || bootstrap.can_manage_database;
    return !item.capability || adminCan(bootstrap, item.capability);
  });
}

export function canAccessAdminPath(bootstrap: AdminBootstrap, candidate: string, locale?: string): boolean {
  let pathname = candidate.split(/[?#]/, 1)[0] || "/admin";
  if (locale && pathname.startsWith(`/${locale}/`)) pathname = pathname.slice(locale.length + 1);
  if (!pathname.startsWith("/admin")) return false;
  return visibleAdminNavigation(bootstrap).some((item) => item.href === "/admin"
    ? pathname === "/admin" || pathname === "/admin/"
    : pathname === item.href || pathname.startsWith(`${item.href}/`));
}
