export const KINDS = ["hotel", "transfer", "tour", "esim"] as const;
export const CITIES = ["tokyo", "osaka", "kyoto", "seoul", "busan", "taipei"] as const;
export type Kind = typeof KINDS[number];
