"use client";

/**
 * Same reason as `not-found.tsx` in this folder: a route group does not inherit the
 * neighbouring group's error boundary, so without this an uncaught render error on an
 * article page replaces the document with Next's default English application-error screen.
 */
export { default } from "@/app/[locale]/error";
