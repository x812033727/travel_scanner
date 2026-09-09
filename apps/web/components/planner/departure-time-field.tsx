"use client";

import { useEffect, useRef, useState } from "react";
import { Clock3 } from "lucide-react";
import { calmEditCopy } from "./calm-edit-copy";

export function DepartureTimeField({ value, locale, busy = false, onSave, onDirtyChange, onBusyChange }: {
  value: string; locale: string; busy?: boolean;
  onSave: (value: string) => void | Promise<boolean | void>;
  onDirtyChange?: (dirty: boolean) => void;
  onBusyChange?: (busy: boolean) => void;
}) {
  const copy = calmEditCopy(locale);
  const [editor, setEditor] = useState({ base: value, text: value });
  const [received, setReceived] = useState(value);
  const [state, setState] = useState<"idle" | "saving" | "saved" | "failed">("idle");
  const savingRef = useRef(false);
  const generation = useRef(0);
  const dirty = editor.text !== editor.base;
  const saving = busy || state === "saving";
  if (value !== received) {
    setReceived(value);
    if (!dirty && !saving) setEditor({ base: value, text: value });
  }
  useEffect(() => { onDirtyChange?.(dirty); }, [dirty, onDirtyChange]);
  useEffect(() => () => { generation.current += 1; }, []);

  async function save() {
    if (savingRef.current || saving || !dirty || !/^([01]\d|2[0-3]):[0-5]\d$/.test(editor.text)) return;
    const owner = generation.current;
    const next = editor.text;
    savingRef.current = true; setState("saving"); onBusyChange?.(true);
    try {
      const result = await onSave(next);
      if (owner !== generation.current) return;
      if (result === false) { setState("failed"); return; }
      setEditor({ base: next, text: next }); setState("saved"); onDirtyChange?.(false);
    } catch {
      if (owner === generation.current) setState("failed");
    } finally {
      savingRef.current = false;
      if (owner === generation.current) onBusyChange?.(false);
    }
  }
  return <div className="planner-departure-field mt-3 grid gap-2 border-t border-[var(--line)] pt-3 text-xs font-semibold">
    <label className="flex flex-wrap items-center gap-3">
      <span className="flex items-center gap-1.5"><Clock3 size={14} />{copy.departureTime}</span>
      <input type="time" aria-label={copy.departureLabel} value={editor.text} disabled={saving}
        onChange={(event) => { setEditor({ ...editor, text: event.target.value }); setState("idle"); }}
        onKeyDown={(event) => { if (event.key === "Enter") event.preventDefault(); }}
        className="min-h-11 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-2.5 font-bold disabled:opacity-45" />
    </label>
    <p className="font-normal text-[var(--muted)]">{copy.departureApplies}</p>
    {state === "failed" && <p role="alert" className="text-red-700">{copy.saveFailed}</p>}
    <div className="calm-departure-actions flex flex-wrap items-center gap-2">
      <span role="status" className="mr-auto text-[var(--muted)]">{saving ? copy.saving : dirty ? copy.unsaved : state === "saved" ? copy.saved : ""}</span>
      <button type="button" disabled={saving || !dirty} onClick={() => {
        setEditor({ base: value, text: value }); setState("idle"); onDirtyChange?.(false);
      }} className="min-h-11 rounded-xl border border-[var(--line)] px-3">{copy.cancel}</button>
      <button type="button" disabled={saving || !dirty || !/^([01]\d|2[0-3]):[0-5]\d$/.test(editor.text)} aria-busy={saving}
        onClick={() => { void save(); }} className="min-h-11 rounded-xl bg-[var(--teal-dark)] px-3 text-white">{copy.save}</button>
    </div>
  </div>;
}
