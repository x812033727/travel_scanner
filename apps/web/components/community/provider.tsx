"use client";
import { createContext, useCallback, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import { usePathname } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { api } from "@/lib/api";
import { closedCommunity, type CommunityFlags, type CommunityMe, type CommunityState } from "@/lib/community/types";
type Value = CommunityState & { me: CommunityMe | null; loading: boolean; error: unknown; unread: number;
  refresh: () => Promise<void>; refreshFlags: () => Promise<void> };
const Context = createContext<Value>({ ...closedCommunity, me: null, loading: false, error: null,
  unread: 0, refresh: async () => {}, refreshFlags: async () => {} });
function validFlags(flags: CommunityFlags) {
  return Object.keys(closedCommunity.flags).every((key) => typeof flags[key as keyof CommunityFlags] === "boolean");
}
export function CommunityProvider({ state, children }: { state: CommunityState; children: ReactNode }) {
  const {user} = useHeaderSession();
  // Do not remount the entire application when /auth/me finishes: that cancels
  // registration-resumed searches and loses confirmation-token form state.
  // CommunityGate and resource keys isolate only community-owned private state.
  return <SessionCommunity state={state} userId={user?.id}>{children}</SessionCommunity>;
}
function SessionCommunity({state, userId, children}: {state:CommunityState;userId?:string;children:ReactNode}) {
  const [current, setCurrent] = useState(state);
  const [source, setSource] = useState(state);
  if (source !== state) { setSource(state); setCurrent(state); }
  const [identity, setIdentity] = useState<{userId:string;me:CommunityMe|null;error?:unknown}>();
  const [unread, setUnread] = useState<{userId:string;count:number}>();
  const identityRequest = useRef(0);
  const flagsRequest = useRef(0);
  const pathname = usePathname();
  const enabled = current.flags.enabled;
  const refreshFlags = useCallback(async () => {
    const generation = ++flagsRequest.current;
    return api<CommunityFlags>("/community/status")
      .then((flags) => { if (generation === flagsRequest.current) setCurrent(validFlags(flags) ? {status:"ready",flags} : closedCommunity); })
      .catch(() => { if (generation === flagsRequest.current) setCurrent(closedCommunity); });
  }, []);
  const refresh = useCallback(async () => {
    const generation = ++identityRequest.current;
    if (!userId || !enabled) return;
    return api<CommunityMe>("/community/me")
      .then((me) => { if (generation === identityRequest.current) setIdentity({userId,me}); })
      .catch((error) => { if (generation === identityRequest.current) setIdentity({userId,me:null,error}); });
  }, [userId,enabled]);
  useEffect(() => { void refresh(); return () => { identityRequest.current += 1; }; }, [refresh]);
  useEffect(() => {
    const update = () => { void refreshFlags(); void refresh(); };
    window.addEventListener("focus",update);
    return () => window.removeEventListener("focus",update);
  }, [refreshFlags,refresh]);
  useEffect(() => { void refreshFlags(); }, [pathname,refreshFlags]);
  const currentIdentity = identity?.userId === userId ? identity : undefined;
  const me = enabled ? currentIdentity?.me || null : null;
  const profileId = me?.profile?.id;
  const restricted = me?.restricted;
  useEffect(() => {
    if (!userId || !profileId || restricted || !enabled || typeof EventSource === "undefined") return;
    let disposed=false;
    let stream:EventSource|undefined;
    let timer:ReturnType<typeof setTimeout>|undefined;
    let lastCursor=0;
    const update = () => {
      void api<{unread:number}>("/community/notifications").then((data)=>{if(!disposed)setUnread({userId,count:data.unread});}).catch(()=>{});
      window.dispatchEvent(new Event("community-refresh"));
    };
    const connect = () => {
      if(disposed)return;
      stream=new EventSource(`/api/travel/community/events?after=${lastCursor}`);
      stream.onmessage=(event)=>{lastCursor=Math.max(lastCursor,Number(event.lastEventId)||0);update();};
      stream.addEventListener("policy",(event)=>{
        try {const flags=JSON.parse((event as MessageEvent).data) as CommunityFlags;setCurrent(validFlags(flags)?{status:"ready",flags}:closedCommunity);}
        catch {void refreshFlags();}
      });
      stream.addEventListener("unavailable",()=>{
        stream?.close();
        void refreshFlags(); void refresh();
        // Bound outage retries; keep the cursor instead of skipping to the newest event.
        timer=setTimeout(connect,5000);
      });
      // Network reconnects use EventSource's Last-Event-ID for durable catch-up.
    };
    void api<{cursor:number}>("/community/events/cursor").then(({cursor})=>{
      if(disposed)return;lastCursor=cursor;update();connect();
    }).catch(()=>{if(!disposed){update();timer=setTimeout(connect,5000);}});
    return ()=>{disposed=true;stream?.close();if(timer)clearTimeout(timer);};
  }, [userId,profileId,restricted,enabled,refresh,refreshFlags]);
  return <Context.Provider value={{...current,me,loading:Boolean(userId&&enabled&&!currentIdentity),error:currentIdentity?.error,unread:enabled&&unread?.userId===userId?unread?.count || 0:0,refresh,refreshFlags}}>{children}</Context.Provider>;
}
export const useCommunity = () => useContext(Context);
