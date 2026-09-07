"use client";

import { useId, useState, type FormEvent } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible } from "@/lib/site-features";
import { api } from "@/lib/api";
import { defaultPet, type Media, type Page, type PetPlace, type PetRequirements, type PetRule } from "@/lib/community/types";
import { useCommunity } from "./provider";
import { CollectButton } from "./post";
import { ImageUpload } from "./upload";
import { PetRulesEditor } from "./pet-rules-editor";
import { Button, CommunityImage, Dialog, Empty, ErrorNotice, fieldClass, panelClass } from "./ui";
import { useResource } from "./use-resource";

export function PetRequirementFields({ value, onChange }: { value: PetRequirements; onChange: (value: PetRequirements) => void }) {
  const t = useTranslations("community");
  const speciesId = useId();
  const checks = ["ground_required", "has_leash", "has_carrier", "has_stroller", "has_diaper", "overnight"] as const;
  return <fieldset className="space-y-4"><legend className="mb-3 font-bold">{t("petCompanion")}</legend><div className="grid gap-3 sm:grid-cols-4">
    <div><label className="block text-sm font-semibold">{t("species")}<input required list={speciesId} className={fieldClass} maxLength={40} value={value.species} onChange={(e) => onChange({ ...value, species: e.target.value })} /></label><datalist id={speciesId}><option value="dog">{t("dog")}</option><option value="cat">{t("cat")}</option></datalist></div>
    <label className="text-sm font-semibold">{t("petCount")}<input required type="number" min={1} max={20} className={fieldClass} value={value.count} onChange={(e) => onChange({ ...value, count: Number(e.target.value) })} /></label>
    <label className="text-sm font-semibold">{t("petWeight")}<input required type="number" min={0.01} max={200} step="0.01" className={fieldClass} value={value.weight_kg} onChange={(e) => onChange({ ...value, weight_kg: Number(e.target.value) })} /></label>
    <label className="text-sm font-semibold">{t("area")}<select className={fieldClass} value={value.area} onChange={(e) => onChange({ ...value, area: e.target.value as PetRequirements["area"] })}>{["any", "indoor", "outdoor"].map((key) => <option value={key} key={key}>{t(`areas.${key}`)}</option>)}</select></label>
  </div><div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">{checks.map((key) => <label key={key} className="flex min-h-11 items-center gap-2 text-sm"><input type="checkbox" checked={value[key]} onChange={(e) => onChange({ ...value, [key]: e.target.checked })} />{t(`requirements.${key}`)}</label>)}</div></fieldset>;
}

export function PetDirectory() {
  const t = useTranslations("community");
  const locale = useLocale();
  const { flags, me } = useCommunity();
  const [q, setQ] = useState("");
  const [destination, setDestination] = useState("");
  const [kind, setKind] = useState("");
  const [withPet, setWithPet] = useState(false);
  const [pet, setPet] = useState(defaultPet);
  const [uncertain, setUncertain] = useState(false);
  const [query, setQuery] = useState("");
  const [suggest, setSuggest] = useState(false);
  const [extra, setExtra] = useState<PetPlace[]>([]);
  const [cursor, setCursor] = useState<string | number | null>();
  const [error, setError] = useState<unknown>();
  const places = useResource<Page<PetPlace>>(`/pet-friendly/places?${query}`);
  const [loaded, setLoaded] = useState(places.data);
  if (loaded !== places.data) { setLoaded(places.data); setExtra([]); setCursor(places.data?.next_cursor); }
  function submit(e: FormEvent) {
    e.preventDefault();
    const params = new URLSearchParams({ q, destination, include_uncertain: String(uncertain) });
    if (kind) params.set("kind", kind);
    if (withPet) Object.entries(pet).forEach(([key, value]) => params.set(key, String(value)));
    setQuery(params.toString());
  }
  async function more() {
    try { const page = await api<Page<PetPlace>>(`/pet-friendly/places?${query}&cursor=${encodeURIComponent(cursor || "")}`); setExtra((rows) => [...rows, ...page.items]); setCursor(page.next_cursor); }
    catch (reason) { setError(reason); }
  }
  return <div className="space-y-6"><p className="max-w-3xl leading-7 text-[var(--muted)]">{t("petIntroduction")}</p>
    <form onSubmit={submit} className={`${panelClass} space-y-4`}><div className="grid gap-3 sm:grid-cols-3"><label className="text-sm font-semibold">{t("search")}<input className={fieldClass} maxLength={160} value={q} onChange={(e) => setQ(e.target.value)} /></label><label className="text-sm font-semibold">{t("destination")}<input className={fieldClass} maxLength={160} value={destination} onChange={(e) => setDestination(e.target.value)} /></label><label className="text-sm font-semibold">{t("placeKind")}<select className={fieldClass} value={kind} onChange={(e) => setKind(e.target.value)}><option value="">{t("all")}</option>{["restaurant", "cafe", "shop", "lodging", "attraction"].map((key) => <option key={key} value={key}>{t(`placeKinds.${key}`)}</option>)}</select></label></div>
      <label className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={withPet} onChange={(e) => setWithPet(e.target.checked)} />{t("matchMyPet")}</label>{withPet && <PetRequirementFields value={pet} onChange={setPet} />}
      <label className="flex min-h-11 items-center gap-3 text-sm"><input type="checkbox" checked={uncertain} onChange={(e) => setUncertain(e.target.checked)} />{t("includeUncertain")}</label><Button type="submit">{t("filter")}</Button>
    </form>
    <ErrorNotice error={error || places.error} />{places.loading && !places.data && <Empty>{t("loading")}</Empty>}
    <div className="grid gap-4 md:grid-cols-2">{[...(places.data?.items || []), ...extra].map((place) => <article key={place.id} className={`${panelClass} space-y-3`}><span className="text-sm font-semibold text-[var(--teal)]">{t(`placeKinds.${place.kind}`)} · {place.destination}</span><h2 className="text-xl font-bold"><Link href={`/pet-friendly/${place.id}`}>{place.names[locale] || place.name}</Link></h2><p className="text-sm text-[var(--muted)]">{place.address}</p><p className="text-sm">{place.verification_current ? t("verifiedRules") : t("needsConfirmation")}</p>{place.conflicts?.length ? <ConflictList conflicts={place.conflicts} /> : null}<Link href={`/pet-friendly/${place.id}`} className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{t("viewRules")}</Link></article>)}</div>
    {!places.loading && !places.error && !places.data?.items.length && <Empty>{t("noPetPlaces")}</Empty>}
    {cursor && <Button secondary onClick={() => void more()}>{t("loadMore")}</Button>}
    {flags.pet_reports_enabled && <Button disabled={!me?.verified} onClick={() => setSuggest(true)}>{t("suggestPlace")}</Button>}
    {suggest && <Dialog title={t("suggestPlace")} onClose={() => setSuggest(false)}><SuggestPlace onDone={() => { setSuggest(false); }} /></Dialog>}
  </div>;
}

export function ConflictList({ conflicts }: { conflicts: string[] }) {
  const t = useTranslations("community");
  return <ul className="list-disc space-y-1 rounded-xl bg-[var(--paper)] p-4 pl-8 text-sm">{conflicts.map((conflict) => <li key={conflict}>{t.has(`conflicts.${conflict}`) ? t(`conflicts.${conflict}`) : t("needsConfirmation")}</li>)}</ul>;
}

const ruleBooleans = ["ground_allowed", "leash_required", "carrier_required", "stroller_required", "stroller_allowed", "diaper_required", "indoor_allowed", "outdoor_allowed", "reservation_required", "overnight_allowed"] as const;
export function Rules({ rules }: { rules: PetRule[] }) {
  const t = useTranslations("community");
  return <div className="space-y-4">{rules.length === 0 && <Empty>{t("unknown")}</Empty>}{rules.map((rule) => <section key={rule.species} className={panelClass}><h3 className="text-lg font-bold">{rule.species === "dog" ? t("dog") : rule.species === "cat" ? t("cat") : rule.species} · {t(`petStatus.${rule.status}`)}</h3><dl className="mt-4 grid grid-cols-2 gap-x-4 gap-y-3 text-sm">
    <dt>{t("petFields.weight_limit")}</dt><dd>{rule.weight_limit === "limited" ? t("kgLimit", { count: rule.max_weight_kg || 0 }) : t(rule.weight_limit === "none" ? "unlimited" : "unknown")}</dd>
    <dt>{t("petFields.count_limit")}</dt><dd>{rule.count_limit === "limited" ? t("countLimit", { count: rule.max_count || 0 }) : t(rule.count_limit === "none" ? "unlimited" : "unknown")}</dd>
    {ruleBooleans.map((key) => <div className="contents" key={key}><dt>{t(`petFields.${key}`)}</dt><dd>{t(rule[key] === null ? "unknown" : rule[key] ? "yes" : "no")}</dd></div>)}
    <dt>{t("petFields.fee")}</dt><dd>{rule.fee_amount === null ? t("unknown") : `${rule.fee_amount} ${rule.fee_currency}`}</dd>
  </dl>{rule.notes && <p className="mt-4 whitespace-pre-wrap break-words text-sm leading-6">{rule.notes}</p>}</section>)}</div>;
}

export function PetDetails({ id }: { id: string }) {
  const t = useTranslations("community");
  const locale = useLocale();
  const { flags, me } = useCommunity();
  const visibility = useSiteVisibility();
  const place = useResource<PetPlace>(`/pet-friendly/places/${id}`);
  const [report, setReport] = useState(false);
  const [add, setAdd] = useState(false);
  if (place.error) return <ErrorNotice error={place.error} />;
  if (!place.data) return <Empty>{t("loading")}</Empty>;
  const row = place.data;
  return <article className="space-y-6"><header className="space-y-3"><p className="text-sm font-semibold text-[var(--teal)]">{t(`placeKinds.${row.kind}`)} · {row.destination}</p><h1 className="text-3xl font-bold">{row.names[locale] || row.name}</h1><p>{row.address}</p></header>
    <div className={`${panelClass} space-y-3`}><h2 className="text-xl font-bold">{row.verification_current ? t("verifiedRules") : t("needsConfirmation")}</h2><p className="text-sm leading-6 text-[var(--muted)]">{t("petUncertaintyNotice")}</p>{row.verified_at && <p>{t("lastChecked", { date: new Intl.DateTimeFormat(locale, { dateStyle: "medium" }).format(new Date(row.verified_at)) })}</p>}{row.source_url && <a href={row.source_url} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{t("ruleSource")}</a>}</div>
    <Rules rules={row.policies} />
    <div className="flex flex-wrap gap-3"><CollectButton kind="pet_place" target={id} />{featureVisible(visibility, "trips") && <Button disabled={!me?.profile} onClick={() => setAdd(true)}>{t("addToTrip")}</Button>}{flags.pet_reports_enabled && <Button secondary disabled={!me?.verified} onClick={() => setReport(true)}>{t("reportVisit")}</Button>}<Button secondary onClick={() => void navigator.clipboard?.writeText(id)}>{t("copyPlaceId")}</Button></div>
    <section className="space-y-4"><h2 className="text-2xl font-bold">{t("travelerExperiences")}</h2><p className="text-sm text-[var(--muted)]">{t("experienceNotice")}</p>{row.experiences?.map((experience) => <article key={experience.id} className={`${panelClass} space-y-3`}><Link href={`/community/profiles/${experience.author.handle}`} className="font-semibold text-[var(--teal)]">{experience.author.display_name}</Link><p className="whitespace-pre-wrap break-words">{experience.body}</p>{experience.visited_on && <p className="text-sm">{t("visitedOn")} {experience.visited_on}</p>}<div className="grid grid-cols-2 gap-3">{experience.media_ids.map((media) => <CommunityImage key={media} id={media} alt={t("visitPhoto")} thumbnail />)}</div></article>)}{!row.experiences?.length && <Empty>{t("noExperiences")}</Empty>}</section>
    {report && <Dialog title={t("reportVisit")} onClose={() => setReport(false)}><VisitReport placeId={id} onDone={() => setReport(false)} /></Dialog>}
    {add && <Dialog title={t("addToTrip")} onClose={() => setAdd(false)}><AddPetPlace placeId={id} onDone={() => setAdd(false)} /></Dialog>}
  </article>;
}

function SuggestPlace({ onDone }: { onDone: () => void }) {
  const t = useTranslations("community");
  const [form, setForm] = useState({ name: "", kind: "cafe", country: "TW", destination: "", address: "", official_url: "" });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>();
  async function submit(e: FormEvent) {
    e.preventDefault(); setBusy(true);
    try { await api("/pet-friendly/places", { method: "POST", body: JSON.stringify({ ...form, official_url: form.official_url || null }) }); onDone(); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  return <form onSubmit={submit} className="space-y-4"><p>{t("candidateNotice")}</p>{(["name", "country", "destination", "address", "official_url"] as const).map((key) => <label key={key} className="block font-semibold">{t(`placeFields.${key}`)}<input type={key === "official_url" ? "url" : "text"} required={["name", "country", "destination"].includes(key)} maxLength={key === "country" ? 2 : key === "official_url" ? 2048 : 160} pattern={key === "country" ? "[A-Z]{2}" : undefined} className={fieldClass} value={form[key]} onChange={(e) => setForm({ ...form, [key]: e.target.value })} /></label>)}<label className="block font-semibold">{t("placeKind")}<select className={fieldClass} value={form.kind} onChange={(e) => setForm({ ...form, kind: e.target.value })}>{["restaurant", "cafe", "shop", "lodging", "attraction"].map((key) => <option value={key} key={key}>{t(`placeKinds.${key}`)}</option>)}</select></label><ErrorNotice error={error} /><Button type="submit" disabled={busy}>{t("submit")}</Button></form>;
}

function VisitReport({ placeId, onDone }: { placeId: string; onDone: () => void }) {
  const t = useTranslations("community");
  const [body, setBody] = useState("");
  const [source, setSource] = useState("");
  const [date, setDate] = useState("");
  const [media, setMedia] = useState<Media[]>([]);
  const [rules, setRules] = useState<PetRule[]>([]);
  const [busy, setBusy] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<unknown>();
  async function submit(e: FormEvent) {
    e.preventDefault(); setBusy(true);
    try { await api(`/pet-friendly/places/${placeId}/reports`, { method: "POST", body: JSON.stringify({ body, source_url: source || null, visited_on: date || null, media_ids: media.map((item) => item.id), proposed_policies: rules }) }); onDone(); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  return <form onSubmit={submit} className="space-y-4"><p>{t("experienceNotice")}</p><label className="block font-semibold">{t("visitExperience")}<textarea required minLength={3} maxLength={2000} rows={4} className={fieldClass} value={body} onChange={(e) => setBody(e.target.value)} /></label><label className="block font-semibold">{t("ruleSource")}<input type="url" className={fieldClass} value={source} onChange={(e) => setSource(e.target.value)} /></label><label className="block font-semibold">{t("visitedOn")}<input type="date" className={fieldClass} value={date} onChange={(e) => setDate(e.target.value)} /></label><details><summary className="cursor-pointer font-semibold">{t("proposedRules")}</summary><div className="mt-4"><PetRulesEditor rules={rules} onChange={setRules} /></div></details><ImageUpload max={5} images={media} onChange={setMedia} onBusyChange={setUploading} /><ErrorNotice error={error} /><Button type="submit" disabled={busy || uploading}>{t("submitForReview")}</Button></form>;
}

function AddPetPlace({ placeId, onDone }: { placeId: string; onDone: () => void }) {
  const t = useTranslations("community");
  const trips = useResource<Array<{ id: string; name: string; version: number; start_date: string; end_date: string }>>("/trips");
  const [id, setId] = useState("");
  const [day, setDay] = useState("");
  const [conflicts, setConflicts] = useState<string[]>([]);
  const [error, setError] = useState<unknown>();
  const [busy, setBusy] = useState(false);
  const trip = trips.data?.find((row) => row.id === id);
  async function submit(e: FormEvent) {
    e.preventDefault(); if (!trip) return;
    setBusy(true); setError(undefined);
    try { const result = await api<{ conflicts: string[]; confirmation_required: boolean }>(`/community/trips/${id}/pet-places`, { method: "POST", body: JSON.stringify({ place_id: placeId, day, version: trip.version, confirm_conflicts: conflicts.length > 0 }) }); if (result.confirmation_required) setConflicts(result.conflicts); else onDone(); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  return <form onSubmit={submit} className="space-y-4"><label className="block font-semibold">{t("chooseTrip")}<select required className={fieldClass} value={id} onChange={(e) => { setId(e.target.value); setConflicts([]); }}><option value="">{t("chooseTrip")}</option>{trips.data?.map((row) => <option key={row.id} value={row.id}>{row.name}</option>)}</select></label><label className="block font-semibold">{t("date")}<input required type="date" min={trip?.start_date} max={trip?.end_date} className={fieldClass} value={day} onChange={(e) => setDay(e.target.value)} /></label>{conflicts.length > 0 && <><ConflictList conflicts={conflicts} /><p className="text-sm">{t("manualConflictNotice")}</p></>}<ErrorNotice error={error || trips.error} /><Button type="submit" disabled={busy || !trip}>{conflicts.length ? t("confirmAddAnyway") : t("addToTrip")}</Button></form>;
}

export function TripPetPanel({ tripId, disabled = false, onSaved }: { tripId: string; disabled?: boolean; onSaved?: (version: number) => void }) {
  const t = useTranslations("community");
  const { flags } = useCommunity();
  const { user } = useHeaderSession();
  const data = useResource<{ version: number; requirements: PetRequirements | null; conflicts: Array<{ item_id: string; title: string; conflicts: string[] }> }>(flags.enabled && user ? `/community/trips/${tripId}/pet-preferences` : null);
  const [enabled, setEnabled] = useState(false);
  const [pet, setPet] = useState(defaultPet);
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<unknown>();
  const [loaded, setLoaded] = useState(data.data);
  if (loaded !== data.data) { setLoaded(data.data); if (data.data) { setEnabled(Boolean(data.data.requirements)); setPet(data.data.requirements || defaultPet); } }
  async function save(e: FormEvent) {
    e.preventDefault(); if (!data.data) return;
    setBusy(true); setError(undefined); setSaved(false);
    try { const result = await api<{ version: number }>(`/community/trips/${tripId}/pet-preferences`, { method: "PUT", body: JSON.stringify({ version: data.data.version, requirements: enabled ? pet : null }) }); onSaved?.(result.version); await data.reload(); setSaved(true); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  if (!flags.enabled || !user) return null;
  return <details className={`${panelClass} my-5`}><summary className="cursor-pointer font-bold">{t("petCompanion")}</summary><form onSubmit={save} className="mt-4 space-y-4"><label className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={enabled} onChange={(e) => setEnabled(e.target.checked)} />{t("travelWithPet")}</label>{enabled && <PetRequirementFields value={pet} onChange={setPet} />}<p className="text-sm text-[var(--muted)]">{t("petAiNotice")}</p><ErrorNotice error={error || data.error} />{saved && <p role="status">{t("saved")}</p>}<Button type="submit" disabled={disabled || busy || !data.data}>{t("save")}</Button></form>
    {data.data?.conflicts.map((item) => <div key={item.item_id} className="mt-4"><h3 className="mb-2 font-semibold">{item.title}</h3><ConflictList conflicts={item.conflicts} /></div>)}
  </details>;
}
