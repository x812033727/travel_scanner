"use client";

import { createContext, useContext, type ReactNode } from "react";

export type BookingContext = {
  check_in?: string | null;
  check_out?: string | null;
  adults?: number | null;
  children?: number | null;
  rooms?: number | null;
  children_ages?: number[] | null;
};

const Stay22BookingContext = createContext<BookingContext | null>(null);

export function Stay22BookingContextProvider({ value, children }: { value?: BookingContext | null; children: ReactNode }) {
  return <Stay22BookingContext.Provider value={value ?? null}>{children}</Stay22BookingContext.Provider>;
}

export function useStay22BookingContext() {
  return useContext(Stay22BookingContext);
}
