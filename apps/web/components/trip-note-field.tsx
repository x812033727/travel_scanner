"use client";

import { Check, Loader2 } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";

type SaveState = "idle" | "saving" | "saved" | "failed";

/**
 * A self-saving note box.
 *
 * Notes are the one thing in the planner a traveller writes rather than picks,
 * so losing keystrokes is worse than saving a little late: the box owns its own
 * text, commits ~1.2s after typing stops (and immediately on blur), and never
 * takes the value back from the server while it is dirty.
 */
export function TripNoteField({
  value,
  placeholder,
  label,
  rows = 3,
  onSave,
}: {
  value: string;
  placeholder: string;
  label: string;
  rows?: number;
  onSave: (next: string) => Promise<void>;
}) {
  const t = useTranslations("trips");
  const [draft, setDraft] = useState(value);
  const [state, setState] = useState<SaveState>("idle");
  const committed = useRef(value);
  const pending = useRef<number | undefined>(undefined);

  useEffect(() => {
    // Accept a server value only when the box has nothing unsaved in it,
    // otherwise a background refresh would wipe what is being typed.
    if (draft === committed.current && value !== committed.current) {
      committed.current = value;
      setDraft(value);
    }
  }, [draft, value]);

  useEffect(() => () => window.clearTimeout(pending.current), []);

  async function commit(next: string) {
    window.clearTimeout(pending.current);
    if (next === committed.current) return;
    setState("saving");
    try {
      await onSave(next);
      committed.current = next;
      setState("saved");
      window.setTimeout(() => setState((current) => (current === "saved" ? "idle" : current)), 2_000);
    } catch {
      setState("failed");
    }
  }

  return (
    <div className="grid gap-1.5">
      <label className="grid gap-1.5 text-sm font-semibold">
        <span>{label}</span>
        <textarea
          value={draft}
          rows={rows}
          maxLength={4000}
          placeholder={placeholder}
          onChange={(event) => {
            const next = event.target.value;
            setDraft(next);
            setState("idle");
            window.clearTimeout(pending.current);
            pending.current = window.setTimeout(() => void commit(next), 1_200);
          }}
          onBlur={() => void commit(draft)}
          className="w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm font-normal text-[var(--ink)] outline-none transition focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]"
        />
      </label>
      <p aria-live="polite" className="min-h-5 text-xs text-[var(--muted)]">
        {state === "saving" && <span className="inline-flex items-center gap-1.5"><Loader2 size={13} className="animate-spin" />{t("notesSaving")}</span>}
        {state === "saved" && <span className="inline-flex items-center gap-1.5 text-[var(--teal)]"><Check size={13} />{t("notesSaved")}</span>}
        {state === "failed" && <span role="alert" className="text-red-700">{t("notesFailed")}</span>}
      </p>
    </div>
  );
}
