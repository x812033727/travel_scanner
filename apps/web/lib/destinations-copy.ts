import data from "./destinations-copy.json";

type Copy = Record<keyof typeof data.en, string>;
const copies: Record<string, Copy> = data;

export function destinationsCopy(locale: string): Copy {
  return copies[locale] ?? copies.en;
}
