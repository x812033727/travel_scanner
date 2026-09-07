"use client";

import { useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import type { Media } from "@/lib/community/types";
import { Button, CommunityImage, ErrorNotice, fieldClass } from "./ui";

export function ImageUpload({ images, onChange, max = 10, disabled = false, onBusyChange }: {
  images: Media[]; onChange: (images: Media[]) => void; max?: number; disabled?: boolean; onBusyChange?: (busy: boolean) => void;
}) {
  const t = useTranslations("community");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>();
  const [alt, setAlt] = useState("");
  useEffect(() => { onBusyChange?.(busy); }, [busy, onBusyChange]);
  async function upload(files: FileList | null) {
    if (!files?.length) return;
    if (files.length + images.length > max || [...files].some((file) => file.size > 10 * 1024 * 1024 || !["image/jpeg", "image/png", "image/webp"].includes(file.type))) {
      setError(new Error()); return;
    }
    setBusy(true); setError(undefined);
    const uploaded = [...images];
    try {
      for (const file of files) {
        const created = await api<{ id: string; upload: { url: string; fields: Record<string, string> } }>("/community/media/uploads", {
          method: "POST", body: JSON.stringify({ content_type: file.type, size: file.size, alt }),
        });
        const form = new FormData();
        Object.entries(created.upload.fields).forEach(([key, value]) => form.append(key, value));
        form.append("file", file);
        const sent = await fetch(created.upload.url, { method: "POST", body: form, credentials: "omit", redirect: "error" });
        if (!sent.ok) throw new Error();
        const media = await api<Media>(`/community/media/${created.id}/complete`, { method: "POST" });
        uploaded.push(media);
        onChange([...uploaded]);
      }
    } catch (reason) { setError(reason); }
    finally { setBusy(false); }
  }
  return <fieldset disabled={disabled || busy} className="space-y-3">
    <legend className="font-semibold">{t("images")}</legend>
    <p className="text-sm text-[var(--muted)]">{t("imageRules", { count: max })}</p>
    <label className="block text-sm">{t("imageDescription")}<input value={alt} onChange={(e) => setAlt(e.target.value)} maxLength={300} className={fieldClass} /></label>
    <input type="file" accept="image/jpeg,image/png,image/webp" multiple={max > 1} aria-label={t("upload")} disabled={busy || images.length >= max || disabled}
      onChange={(e) => { void upload(e.target.files); e.target.value = ""; }} className="block w-full text-sm file:mr-3 file:min-h-11 file:rounded-xl file:border-0 file:bg-[var(--teal)] file:px-4 file:text-white" />
    {busy && <p role="status">{t("uploading")}</p>}<ErrorNotice error={error} />
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">{images.map((image) => <div key={image.id} className="space-y-2"><CommunityImage id={image.id} alt={image.alt || t("imageDescription")} thumbnail /><Button secondary onClick={() => onChange(images.filter((other) => other.id !== image.id))}>{t("remove")}</Button></div>)}</div>
  </fieldset>;
}
