"use client";
import { useState, type FormEvent } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import { Link } from "@/i18n/navigation";
import { type Page, type PetPlace, type PetRule } from "@/lib/community/types";
import { AdminGate, ReasonAction } from "./admin";
import { Rules } from "./pets";
import { Button, CommunityImage, Dialog, Empty, ErrorNotice, fieldClass, panelClass, Tabs } from "./ui";
import { useResource } from "./use-resource";
import { PetRulesEditor } from "./pet-rules-editor";
export { PetRulesEditor } from "./pet-rules-editor";
export function PetAdmin() {
 const t=useTranslations("community");
 const [tab,setTab]=useState("places");
 return <AdminGate><div className="space-y-6"><h1 className="text-3xl font-bold">{t("adminPets")}</h1><Tabs label={t("adminPets")} value={tab} onChange={setTab} items={["places","reports","coverage"].map((value)=>({value,label:t(`petAdminTabs.${value}`)}))}>{tab==="places" && <PlacesReview />}{tab==="reports" && <PetReportReview />}{tab==="coverage" && <Coverage />}</Tabs></div></AdminGate>;
}
function PlacesReview() {
 const t=useTranslations("community");
 const [state,setState]=useState("pending");
 const data=useResource<Page<PetPlace>>(`/admin/pet-friendly/places?state=${state}`);
 const [selected,setSelected]=useState<PetPlace>();
 const [history,setHistory]=useState<string>();
 return <div className="space-y-4"><label className="block max-w-xs font-semibold">{t("status")}<select className={fieldClass} value={state} onChange={(e)=>setState(e.target.value)}>{["pending","approved","rejected","disabled","all"].map((key)=><option key={key} value={key}>{t(`states.${key}`)}</option>)}</select></label><ErrorNotice error={data.error} />{data.data?.items.length===0 && <Empty>{t("queueEmpty")}</Empty>}{data.data?.items.map((row)=><article key={row.id} className={`${panelClass} flex flex-wrap justify-between gap-3`}><div><h2 className="font-bold">{row.name} · {row.destination}</h2><p className="text-sm">{row.address}</p><p className="text-sm">{t(row.verification_current ? "verifiedRules":"needsConfirmation")}</p></div><div className="flex gap-2"><Button onClick={()=>setSelected(row)}>{t("reviewRules")}</Button><Button secondary onClick={()=>setHistory(row.id)}>{t("history")}</Button></div></article>)}{selected && <Dialog title={t("reviewRules")} onClose={()=>setSelected(undefined)}><ReviewPlace place={selected} onDone={async()=>{setSelected(undefined);await data.reload();}} /></Dialog>}{history && <Dialog title={t("history")} onClose={()=>setHistory(undefined)}><PlaceHistory id={history} /></Dialog>}</div>;
}
function ReviewPlace({place,onDone}: {place:PetPlace;onDone:()=>Promise<void>}) {
 const t=useTranslations("community");
 const [rules,setRules]=useState(place.policies);
 const [references,setReferences]=useState(place.references || []);
 const [status,setStatus]=useState(place.status==="pending" ? "approved":place.status||"approved");
 const [source,setSource]=useState(place.source_url||place.official_url||"");
 const [identity,setIdentity]=useState(place.identity_key||"");
 const [latitude,setLatitude]=useState(place.latitude===null ? "":String(place.latitude));
 const [longitude,setLongitude]=useState(place.longitude===null ? "":String(place.longitude));
 const [coordinateSource,setCoordinateSource]=useState(place.coordinate_source_url||"");
 const [reason,setReason]=useState("");
 const [busy,setBusy]=useState(false);
 const [error,setError]=useState<unknown>();
 async function submit(e:FormEvent) {e.preventDefault();setBusy(true);try {await api(`/admin/pet-friendly/places/${place.id}`,{method:"PUT",body:JSON.stringify({version:place.version,status,policies:rules,references,source_url:source,identity_key:identity||null,latitude:latitude==="" ? null:Number(latitude),longitude:longitude==="" ? null:Number(longitude),coordinate_source_url:coordinateSource||null,reason})});await onDone();}catch(error){setError(error);}finally{setBusy(false);}}
 return <form onSubmit={submit} className="space-y-5"><h3 className="text-xl font-bold">{place.name}</h3><p className="text-sm">{t("reviewPetNotice")}</p><label className="block font-semibold">{t("status")}<select className={fieldClass} value={status} onChange={(e)=>setStatus(e.target.value)}>{["approved","rejected","disabled"].map((key)=><option key={key} value={key}>{t(`states.${key}`)}</option>)}</select></label><PetRulesEditor rules={rules} onChange={setRules} /><ReferenceEditor references={references} onChange={setReferences} /><label className="block font-semibold">{t("ruleSource")}<input required type="url" maxLength={2048} className={fieldClass} value={source} onChange={(e)=>setSource(e.target.value)} /></label><label className="block font-semibold">{t("canonicalIdentity")}<input maxLength={200} className={fieldClass} value={identity} onChange={(e)=>setIdentity(e.target.value)} /></label><div className="grid gap-3 sm:grid-cols-2"><label className="font-semibold">{t("latitude")}<input type="number" step="any" min={-90} max={90} className={fieldClass} value={latitude} onChange={(e)=>setLatitude(e.target.value)} /></label><label className="font-semibold">{t("longitude")}<input type="number" step="any" min={-180} max={180} className={fieldClass} value={longitude} onChange={(e)=>setLongitude(e.target.value)} /></label></div><label className="block font-semibold">{t("coordinateSource")}<input type="url" required={latitude!==""||longitude!==""} className={fieldClass} value={coordinateSource} onChange={(e)=>setCoordinateSource(e.target.value)} /></label><label className="block font-semibold">{t("reason")}<textarea required minLength={3} maxLength={1000} className={fieldClass} value={reason} onChange={(e)=>setReason(e.target.value)} /></label><ErrorNotice error={error} /><Button type="submit" disabled={busy}>{t("saveReview")}</Button></form>;
}
function PlaceHistory({id}:{id:string}) {
 const t=useTranslations("community");
 const data=useResource<Page<{id:string;actor_id:string;before:{policies?:PetRule[]};after:{policies?:PetRule[]};reason:string;created_at:string}>>(`/admin/pet-friendly/places/${id}/history`);
 return <div className="space-y-4"><ErrorNotice error={data.error} />{data.data?.items.map((row)=><details key={row.id} className={panelClass}><summary>{row.created_at} · {row.reason}</summary><p className="my-3 break-all text-sm">{t("actor")}: {row.actor_id}</p><h3 className="my-3 font-semibold">{t("before")}</h3><Rules rules={row.before.policies||[]} /><h3 className="my-3 font-semibold">{t("after")}</h3><Rules rules={row.after.policies||[]} /><pre className="mt-3 overflow-x-auto whitespace-pre-wrap break-words text-xs">{JSON.stringify({before:row.before,after:row.after},null,2)}</pre></details>)}</div>;
}
function PetReportReview() {
 const t=useTranslations("community");
 const data=useResource<Page<{id:string;place_id:string;body:string;source_url:string|null;visited_on:string|null;media_ids:string[];proposed_policies:PetRule[]}>>("/admin/pet-friendly/reports");
 const [action,setAction]=useState<{id:string;status:string;flag_conflict?:boolean}>();
 return <div className="space-y-4"><ErrorNotice error={data.error} />{data.data?.items.length===0 && <Empty>{t("queueEmpty")}</Empty>}{data.data?.items.map((row)=><article key={row.id} className={`${panelClass} space-y-3`}><Link href={`/pet-friendly/${row.place_id}`} className="underline">{t("viewRules")}</Link><p className="whitespace-pre-wrap break-words">{row.body}</p>{row.visited_on && <p>{t("visitedOn")}: {row.visited_on}</p>}{row.source_url && <a href={row.source_url} target="_blank" rel="noopener noreferrer" className="underline">{t("ruleSource")}</a>}<div className="grid grid-cols-2 gap-3">{row.media_ids.map((id)=><CommunityImage key={id} id={id} alt={t("visitPhoto")} review />)}</div><Rules rules={row.proposed_policies} /><p className="text-sm">{t("experienceNotice")}</p><div className="flex gap-2">{["resolved","dismissed"].map((status)=><Button key={status} secondary onClick={()=>setAction({id:row.id,status})}>{t(`states.${status}`)}</Button>)}<Button secondary onClick={()=>setAction({id:row.id,status:"resolved",flag_conflict:true})}>{t("flagConflict")}</Button></div></article>)}{action && <ReasonAction title={t(`states.${action.status}`)} onClose={()=>setAction(undefined)} onSubmit={async(reason)=>{await api(`/admin/pet-friendly/reports/${action.id}`,{method:"PUT",body:JSON.stringify({...action, id:undefined,reason})});await data.reload();}} />}</div>;
}
function Coverage() {
 const t=useTranslations("community");
 const data=useResource<{approved:number;verified_current:number;validity_rate:number|null;verification_days:number}>("/admin/pet-friendly/coverage");
 return <div className="space-y-4"><ErrorNotice error={data.error} />{data.data && <dl className="grid gap-4 sm:grid-cols-2">{(["approved","verified_current","validity_rate","verification_days"] as const).map((key)=><div key={key} className={panelClass}><dt>{t(`coverage.${key}`)}</dt><dd className="mt-2 text-3xl font-bold">{key==="validity_rate" ? data.data![key]===null ? t("unknown"):`${Math.round(data.data![key]!*100)}%` : data.data![key]}</dd></div>)}</dl>}<Link href="/admin/community" className="underline">{t("changeVerificationPeriod")}</Link></div>;
}

function ReferenceEditor({ references, onChange }: {
  references: Array<{kind: string; id: string}>;
  onChange: (value: Array<{kind: string; id: string}>) => void;
}) {
  const t = useTranslations("community");
  return <fieldset className="space-y-3"><legend className="font-semibold">{t("placeReferences")}</legend><p className="text-sm">{t("referenceHelp")}</p>
    {references.map((reference, index) => <div key={index} className="grid gap-3 sm:grid-cols-[1fr_2fr_auto]">
      <label>{t("referenceKind")}<select className={fieldClass} value={reference.kind} onChange={(e) => onChange(references.map((row, i) => i === index ? {...row, kind:e.target.value} : row))}>
        {["hotspot","merchant","restaurant","hotel"].map((kind) => <option key={kind} value={kind}>{t(`referenceKinds.${kind}`)}</option>)}</select></label>
      <label>{t("referenceId")}<input className={fieldClass} required maxLength={160} value={reference.id} onChange={(e) => onChange(references.map((row, i) => i === index ? {...row,id:e.target.value} : row))} /></label>
      <Button secondary onClick={() => onChange(references.filter((_, i) => i !== index))}>{t("remove")}</Button>
    </div>)}
    <Button secondary disabled={references.length >= 20} onClick={() => onChange([...references,{kind:"hotspot",id:""}])}>{t("addReference")}</Button>
  </fieldset>;
}
