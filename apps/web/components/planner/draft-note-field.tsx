"use client";

import { useEffect, useRef, useState } from "react";
import { useLocale } from "next-intl";
import { calmEditCopy } from "./calm-edit-copy";

/** A local note draft: only Save writes. Key by trip/day when changing owners. */
export function DraftNoteField({ value, placeholder, label, rows = 3, onSave, onDirtyChange, onBusyChange }: {
  value: string; placeholder: string; label: string; rows?: number;
  onSave: (next: string) => Promise<void>;
  onDirtyChange?: (dirty: boolean) => void;
  onBusyChange?: (busy: boolean) => void;
}) {
  const copy = calmEditCopy(useLocale());
  const [editor, setEditor] = useState({ base: value, text: value });
  const [received, setReceived] = useState(value);
  const [state, setState] = useState<"idle" | "saving" | "saved" | "failed">("idle");
  const busy = useRef(false);
  const generation = useRef(0);
  const dirty = editor.text !== editor.base;
  // A background refresh may update an untouched box, never an unsaved draft.
  if (value !== received) {
    setReceived(value);
    if (!dirty && state !== "saving") setEditor({ base: value, text: value });
  }
  useEffect(() => { onDirtyChange?.(dirty); }, [dirty, onDirtyChange]);
  useEffect(() => () => { generation.current += 1; }, []);

  async function save() {
    if (busy.current || !dirty) return;
    const next = editor.text;
    const owner = generation.current;
    busy.current = true; setState("saving"); onBusyChange?.(true);
    try {
      await onSave(next);
      if (owner !== generation.current) return;
      setEditor({ base: next, text: next }); setState("saved"); onDirtyChange?.(false);
    } catch {
      if (owner === generation.current) setState("failed");
    } finally {
      busy.current = false;
      if (owner === generation.current) onBusyChange?.(false);
    }
  }
  return <div className="calm-draft-note grid gap-2">
    <label className="grid gap-1.5 text-sm font-semibold">
      <span>{label}</span>
      <textarea value={editor.text} rows={rows} maxLength={4000} placeholder={placeholder} disabled={state === "saving"}
        onChange={(event) => { setEditor({ ...editor, text: event.target.value }); setState("idle"); }}
        className="w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 py-2.5 text-sm font-normal text-[var(--ink)] outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]" />
    </label>
    {state === "failed" && <p role="alert" className="text-sm text-red-700">{copy.saveFailed}</p>}
    <div className="calm-note-actions flex items-center justify-end gap-3">
      <span role="status" className="mr-auto text-xs text-[var(--muted)]">{state === "saving" ? copy.saving : dirty ? copy.unsaved : state === "saved" ? copy.saved : ""}</span>
      <button type="button" disabled={state === "saving" || !dirty} onClick={() => {
        setEditor({ base: value, text: value }); setState("idle"); onDirtyChange?.(false);
      }} className="rounded-lg border border-[var(--line)] px-3 py-2 text-sm font-semibold">{copy.cancel}</button>
      <button type="button" disabled={state === "saving" || !dirty} aria-busy={state === "saving"} onClick={() => { void save(); }} className="rounded-lg bg-[var(--teal-dark)] px-3 py-2 text-sm font-semibold text-white">{copy.save}</button>
    </div>
  </div>;
}
