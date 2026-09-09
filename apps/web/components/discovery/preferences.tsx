"use client";
import { useState, type FormEvent } from "react";
import { useLocale } from "next-intl";
import { ApiError, api } from "@/lib/api";
import { getDiscoveryCopy, getDiscoveryFeedback } from "@/lib/discovery-copy";
import { useDiscoveryResource, type DiscoveryPreferences } from "@/lib/discovery";
import { Button, Dialog } from "@/components/community/ui";

export function DiscoveryPreferenceEditor({ onClose, onSaved }: { onClose: () => void; onSaved: () => void }) {
  const c = getDiscoveryCopy(useLocale());
  const result = useDiscoveryResource<DiscoveryPreferences>("/discovery/preferences");
  const [revision, setRevision] = useState(0);
  return <Dialog title={c.preferences} onClose={onClose}>{result.error ? <p role="alert">{c.unavailable}</p> : result.data ? <PreferenceForm key={`${result.data.version}:${revision}`} initial={result.data} onSaved={onSaved} onReload={() => { result.reload(); setRevision((value) => value + 1); }} /> : <p role="status">{c.loading}</p>}</Dialog>;
}
function PreferenceForm({ initial, onSaved, onReload }: { initial: DiscoveryPreferences; onSaved: () => void; onReload: () => void }) {
  const locale = useLocale();
  const c = getDiscoveryCopy(locale);
  const feedback = getDiscoveryFeedback(locale);
  const [destinations, setDestinations] = useState(initial.destinations.join(", "));
  const [topics, setTopics] = useState(initial.topics.join(", "));
  const [saved, setSaved] = useState(initial.include_saved);
  const [following, setFollowing] = useState(initial.include_following);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>();
  const options = useDiscoveryResource<{ destinations: Array<{ id: string; name: string }>; topics?: Array<{ id: string; label: string }> }>("/discovery/suggestions?q=");
  function toggle(value: string, id: string, enabled: boolean) { const ids = value.split(/,\s*/).filter(Boolean); return (enabled ? [...new Set([...ids, id])] : ids.filter((item) => item !== id)).join(", "); }
  async function submit(event?: FormEvent) {
    event?.preventDefault(); setBusy(true); setError(undefined);
    const list = (value: string) => [...new Set(value.split(/[,，\n]/).map((item) => item.trim()).filter(Boolean))];
    try { await api(`/discovery/preferences${event ? "" : `?version=${initial.version}`}`, event ? { method: "PUT", body: JSON.stringify({ version: initial.version, destinations: list(destinations), topics: list(topics), include_saved: saved, include_following: following }) } : { method: "DELETE" }); onSaved(); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  return <form onSubmit={(event) => void submit(event)} className="space-y-5"><p className="text-sm leading-7 text-[var(--muted)]">{c.preferenceHelp}</p>
    <fieldset><legend className="mb-2 font-semibold">{c.destination}</legend><div className="flex max-h-64 flex-wrap gap-2 overflow-y-auto">{options.data?.destinations?.map((item) => <label key={item.id} className="flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] px-3 text-sm"><input type="checkbox" checked={destinations.split(/,\s*/).includes(item.id)} onChange={(event) => setDestinations(toggle(destinations, item.id, event.target.checked))} />{item.name}</label>)}</div></fieldset>
    <fieldset><legend className="mb-2 font-semibold">{c.topic}</legend><div className="flex flex-wrap gap-2">{options.data?.topics?.map((item) => <label key={item.id} className="flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] px-3 text-sm"><input type="checkbox" checked={topics.split(/,\s*/).includes(item.id)} onChange={(event) => setTopics(toggle(topics, item.id, event.target.checked))} />{item.label}</label>)}</div></fieldset>
    {options.loading && <p role="status">{c.loading}</p>}{Boolean(options.error) && <p role="alert">{c.unavailable}</p>}
    <label className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={saved} onChange={(event) => setSaved(event.target.checked)} />{c.savedSignal}</label>
    <label className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={following} onChange={(event) => setFollowing(event.target.checked)} />{c.followingSignal}</label>
    {Boolean(error) && <div role="alert" className="space-y-3"><p>{error instanceof ApiError && error.status === 409 ? feedback.conflict : c.unavailable}</p>{error instanceof ApiError && error.status === 409 && <Button secondary onClick={() => { if (window.confirm(feedback.discard)) onReload(); }}>{feedback.reload}</Button>}</div>}<div className="flex flex-wrap gap-3"><Button type="submit" disabled={busy}>{c.save}</Button><Button secondary disabled={busy} onClick={() => { if (window.confirm(c.reset)) void submit(); }}>{c.reset}</Button></div>
  </form>;
}
