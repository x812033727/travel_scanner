import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { CommunityGate } from "./shell";
import { Tabs } from "./ui";
import { PetDetails, PetRequirementFields, Rules, TripPetPanel } from "./pets";
import { PetAdmin, PetRulesEditor } from "./pet-admin";
import { PostEditor } from "./editor";
import { ProfileEditor } from "./profile";
import { TranslateText } from "./post";
import { catchUpMessages } from "./messages";
import { CommunityAdmin } from "./admin";
import { AppBottomNav } from "../app-bottom-nav";
import { defaultPet, unknownPetRule } from "@/lib/community/types";
const mock = vi.hoisted(() => ({
  api: vi.fn(), refreshFlags:vi.fn(), profile:{id:"member",handle:"traveler",display_name:"Traveler",bio:"",languages:["en"],destinations:[],avatar_id:null},
  state:{status:"ready" as string,flags:{enabled:true,posting_enabled:true,comments_enabled:true,messaging_enabled:true,translation_enabled:true,pet_reports_enabled:true},verified:true,restricted:false},
  session:{status:"authenticated",user:{id:"member",email:"private@example.test",is_admin:true}},
}));
vi.mock("@/lib/api",async(importOriginal)=>({...await importOriginal<typeof import("@/lib/api")>(),api:mock.api}));
vi.mock("@/components/header-session",()=>({useHeaderSession:()=>mock.session}));
vi.mock("./provider",()=>({useCommunity:()=>({...mock.state,me:{profile:mock.profile,verified:mock.state.verified,restricted:mock.state.restricted,notification_preferences:{}},loading:false,error:null,unread:0,refresh:vi.fn(),refreshFlags:mock.refreshFlags})}));
beforeEach(()=>{
 mock.api.mockReset();mock.refreshFlags.mockReset();
 mock.state.status="ready";mock.state.flags.enabled=true;mock.state.flags.posting_enabled=true;
 mock.state.verified=true;mock.state.restricted=false;mock.session.status="authenticated";
 mock.api.mockImplementation(async(path:string)=>path==="/trips"?[]:{items:[]});
 HTMLDialogElement.prototype.showModal=vi.fn(function(this:HTMLDialogElement){this.setAttribute("open","");});
});
afterEach(cleanup);

describe("community reconnect and identity-bound state", () => {
  it("loads every missed message page after reconnect without duplicates", async () => {
    const message = (id:number) => ({id,body:String(id),mine:false,sender_id:"other",card:null,card_unavailable:false,created_at:"2026-09-07"});
    const page = (start:number,end:number,next:number|null) => ({items:Array.from({length:end-start+1},(_,i)=>message(start+i)),next_cursor:next,latest_cursor:end,can_send:true,other_read_id:0});
    mock.api.mockResolvedValueOnce(page(2,51,51)).mockResolvedValueOnce(page(52,101,101)).mockResolvedValueOnce(page(102,131,null));
    const result=await catchUpMessages("/community/conversations/conversation/messages",page(1,1,null));
    expect(result.items.map((row)=>row.id)).toEqual(Array.from({length:131},(_,i)=>i+1));
    expect(mock.api.mock.calls.map((call)=>call[0])).toEqual([
      "/community/conversations/conversation/messages?after=1",
      "/community/conversations/conversation/messages?after=51",
      "/community/conversations/conversation/messages?after=101",
    ]);
  });
  it("initializes an already-loaded public profile without exposing the email", () => {
    render(<ProfileEditor />);
    expect((screen.getByLabelText("暱稱") as HTMLInputElement).value).toBe("Traveler");
    expect(screen.queryByDisplayValue("private@example.test")).toBeNull();
  });
  it("discards a translation which returns after the original text changes", async () => {
    let resolve!: (value:{text:string})=>void;
    mock.api.mockImplementation(()=>new Promise((done)=>{resolve=done;}));
    const view=render(<TranslateText kind="post" id="post" original="Original" sourceLocale="en" />);
    fireEvent.click(screen.getByRole("button",{name:"翻譯"}));
    view.rerender(<TranslateText kind="post" id="post" original="Edited" sourceLocale="en" />);
    resolve({text:"Obsolete translation"});
    await Promise.resolve();
    expect(screen.queryByText("Obsolete translation")).toBeNull();
    expect(screen.getByText("Edited")).toBeTruthy();
  });
});
describe("community availability and accessible controls",()=>{
 it("waits for cookie identity before mounting public filters but does not delay anonymous visitors",()=>{
  mock.session.status="loading";
  const view=render(<CommunityGate><input aria-label="Pet filters" /></CommunityGate>);
  expect(screen.queryByLabelText("Pet filters")).toBeNull();
  mock.session.status="authenticated";
  view.rerender(<CommunityGate><input aria-label="Pet filters" /></CommunityGate>);
  fireEvent.change(screen.getByLabelText("Pet filters"),{target:{value:"cat"}});
  view.rerender(<CommunityGate><input aria-label="Pet filters" /></CommunityGate>);
  expect(screen.getByDisplayValue("cat")).toBeTruthy();
  mock.session.status="signed_out";
  view.rerender(<CommunityGate><input aria-label="Pet filters" /></CommunityGate>);
  expect(screen.getByLabelText("Pet filters")).toBeTruthy();
 });
 it("does not mount content when closed or unavailable",()=>{
  mock.state.flags.enabled=false;
  const view=render(<CommunityGate><input aria-label="private editor"/></CommunityGate>);
  expect(screen.queryByRole("textbox")).toBeNull();
  expect(screen.getByText(/社群目前暫停開放/)).toBeTruthy();
  mock.state.status="unavailable";view.rerender(<CommunityGate><input aria-label="private editor"/></CommunityGate>);
  expect(screen.queryByRole("textbox")).toBeNull();expect(screen.getByText(/暫時無法確認社群狀態/)).toBeTruthy();
 });
 it("requires verification for writing but not public reading",()=>{
  mock.state.verified=false;
  render(<CommunityGate member verified><input aria-label="post editor"/></CommunityGate>);
  expect(screen.queryByRole("textbox")).toBeNull();expect(screen.getByRole("link",{name:/完成 Email 驗證/}).getAttribute("href")).toBe("/account");
 });
 it("uses keyboard-selectable tabs and a mobile select",()=>{
  const change=vi.fn();
  render(<Tabs value="posts" onChange={change} label="Sections" items={[{value:"posts",label:"Posts"},{value:"rules",label:"Rules"}]}>Content</Tabs>);
  fireEvent.keyDown(screen.getByRole("tab",{name:"Posts"}),{key:"ArrowRight"});
  expect(change).toHaveBeenCalledWith("rules");
  fireEvent.change(screen.getByRole("combobox"),{target:{value:"rules"}});
  expect(change).toHaveBeenCalledTimes(2);
 });
 it("uses community mobile destinations and hides publish when paused",()=>{
  const view=render(<AppBottomNav/>);
  expect(screen.getAllByRole("link").map((link)=>link.getAttribute("href"))).toEqual(["/","/community","/community/new","/community/messages","/my"]);
  mock.state.flags.posting_enabled=false;view.rerender(<AppBottomNav/>);
  expect(screen.queryByRole("link",{name:"發佈"})).toBeNull();
 });
});
describe("publishing and moderation",()=>{
 it("sends only typed IDs for selected public places and retains them when editing",async()=>{
  const place={id:"place-id",kind:"hotspot",name:"Public museum",destination:"Tokyo",href:"/hotspots?hotspot=place-id"};
  const post={id:"post-id",version:1,title:"Tokyo walk",body:"My travel experience",destination:"Tokyo",locale:"zh-TW",kind:"story",topics:[],place_ids:[],places:[place],media:[],itinerary:null,allow_fork:false,state:"draft"};
  mock.api.mockImplementation(async(path:string)=>path==="/trips"?[]:post);
  render(<PostEditor id="post-id"/>);
  await screen.findByRole("button",{name:"移除 Public museum"});
  fireEvent.change(screen.getByLabelText("旅行心得"),{target:{value:"Updated experience"}});
  fireEvent.click(screen.getByRole("button",{name:"儲存草稿"}));
  await screen.findByText("已儲存");
  const write=mock.api.mock.calls.find(([,options])=>options?.method==="PUT");
  const payload=JSON.parse(write![1].body);
  expect(payload.places).toEqual([{kind:"hotspot",id:"place-id"}]);
  expect(payload).not.toHaveProperty("place_ids");
  expect(JSON.stringify(payload)).not.toContain("/hotspots?");
 });
 it("saves a real draft and submits its returned version for review",async()=>{
  const post={id:"post-id",version:1,title:"Taipei walk",body:"My travel experience",destination:"Taipei",locale:"zh-TW",kind:"story",topics:[],place_ids:[],media:[],itinerary:null,allow_fork:false,state:"draft"};
  mock.api.mockImplementation(async(path:string)=>path==="/trips"?[]:path.endsWith("/publish")?{...post,version:2,state:"pending",pending_revision_id:"review-id"}:post);
  render(<PostEditor/>);
  fireEvent.change(screen.getByLabelText("標題"),{target:{value:post.title}});
  fireEvent.change(screen.getByLabelText("旅行心得"),{target:{value:post.body}});
  fireEvent.change(screen.getByLabelText("目的地"),{target:{value:post.destination}});
  fireEvent.click(screen.getByRole("button",{name:"儲存草稿"}));
  await screen.findByText("已儲存");
  fireEvent.click(screen.getByRole("button",{name:"發佈"}));
  await screen.findByText("待審核");
  const publish=mock.api.mock.calls.find(([path])=>path==="/community/posts/post-id/publish");
  expect(JSON.parse(publish![1].body)).toEqual({version:1});
  expect(document.body.textContent).not.toContain("private@example.test");
 });
 it("loads and saves administrator switches with a reason",async()=>{
  const settings={enabled:false,posting_enabled:true,comments_enabled:true,messaging_enabled:true,translation_enabled:false,pet_reports_enabled:true,uploads_per_day:50,posts_per_day:10,interactions_per_minute:30,translation_characters_per_month:100000,pet_verification_days:180,risk_terms:[]};
  mock.api.mockImplementation(async(path:string)=>path==="/admin/community/settings"?{settings,sources:{},services:{mail_configured:false,storage_configured:false}}:{items:[]});
  render(<CommunityAdmin/>);
  fireEvent.click(screen.getByRole("tab",{name:"社群設定"}));
  const enabled=await screen.findByRole("checkbox",{name:/開放社群/});
  fireEvent.click(enabled);fireEvent.change(screen.getByLabelText("原因"),{target:{value:"Acceptance complete in test environment"}});
  fireEvent.click(screen.getByRole("button",{name:"儲存"}));
  await screen.findByRole("status");
  const write=mock.api.mock.calls.find(([,options])=>options?.method==="PUT");
  expect(JSON.parse(write![1].body).settings.enabled).toBe(true);
  expect(mock.refreshFlags).toHaveBeenCalledTimes(1);
 });
 it("keeps failed draft saves visible and retryable",async()=>{
  mock.api.mockImplementation(async(path:string)=>{if(path==="/trips")return [];throw new Error("offline");});
  render(<PostEditor/>);
  fireEvent.change(screen.getByLabelText("標題"),{target:{value:"Offline draft"}});
  fireEvent.click(screen.getByRole("button",{name:"儲存草稿"}));
  await screen.findByRole("alert");
  expect((screen.getByLabelText("標題") as HTMLInputElement).value).toBe("Offline draft");
 });
});
describe("pet rule uncertainty",()=>{
 it("binds a conflict confirmation to the original trip version despite background refreshes",async()=>{
  let version=1;
  let writes=0;
  mock.api.mockImplementation(async(path:string,options?:{method:string})=>{
   if(options?.method==="POST") {
    writes+=1;
    if(writes===2) throw new Error("stale trip");
    return {confirmation_required:true,conflicts:["species_unknown"]};
   }
   if(path==="/trips") return [{id:"trip",name:"My trip",version,start_date:"2026-10-01",end_date:"2026-10-02"}];
   return {id:"place",name:"Pet cafe",names:{},kind:"cafe",destination:"Taipei",address:"",policies:[],experiences:[],verification_current:false};
  });
  render(<PetDetails id="place"/>);
  fireEvent.click(await screen.findByRole("button",{name:"加入我的行程"}));
  const dialog=within(screen.getByRole("dialog",{name:"加入我的行程"}));
  await dialog.findByRole("option",{name:"My trip"});
  fireEvent.change(dialog.getByRole("combobox"),{target:{value:"trip"}});
  fireEvent.change(dialog.getByLabelText("日期"),{target:{value:"2026-10-01"}});
  fireEvent.click(dialog.getByRole("button",{name:"加入我的行程"}));
  await dialog.findByText("尚未確認接待這種動物");
  version=2;
  await act(async()=>{window.dispatchEvent(new Event("community-refresh"));});
  fireEvent.click(dialog.getByRole("button",{name:"確認仍要加入"}));
  await dialog.findByRole("alert");
  const calls=mock.api.mock.calls.filter(([,options])=>options?.method==="POST");
  expect(JSON.parse(calls[1][1].body)).toEqual({place_id:"place",day:"2026-10-01",version:1,confirm_conflicts:true});
  fireEvent.change(dialog.getByLabelText("日期"),{target:{value:"2026-10-02"}});
  fireEvent.click(dialog.getByRole("button",{name:"加入我的行程"}));
  await dialog.findByRole("button",{name:"確認仍要加入"});
  const last=mock.api.mock.calls.filter(([,options])=>options?.method==="POST").at(-1)!;
  expect(JSON.parse(last[1].body)).toEqual({place_id:"place",day:"2026-10-02",version:2,confirm_conflicts:false});
 });
 it("waits for pet settings and preserves edits plus their original version across refreshes",async()=>{
  let resolve!: (value:unknown)=>void;
  const path="/community/trips/trip-id/pet-preferences";
  mock.api.mockImplementationOnce(()=>new Promise((done)=>{resolve=done;}));
  render(<TripPetPanel tripId="trip-id"/>);
  fireEvent.click(screen.getByText("寵物同行條件"));
  const checkbox=screen.getByLabelText("這趟旅行有寵物同行");
  expect(checkbox.closest("fieldset")!.disabled).toBe(true);
  await act(async()=>resolve({version:1,requirements:null,conflicts:[]}));
  expect(checkbox.closest("fieldset")!.disabled).toBe(false);
  fireEvent.click(checkbox);
  fireEvent.change(screen.getByLabelText("動物種類",{exact:true}),{target:{value:"cat"}});
  mock.api.mockImplementation(async(_path:string,options?:{method:string})=>{
   if(options?.method==="PUT") throw new Error("version conflict");
   return {version:2,requirements:defaultPet,conflicts:[]};
  });
  await act(async()=>{window.dispatchEvent(new Event("community-refresh"));});
  expect(screen.getByDisplayValue("cat")).toBeTruthy();
  fireEvent.click(screen.getByRole("button",{name:"儲存"}));
  await screen.findByRole("alert");
  const write=mock.api.mock.calls.find(([,options])=>options?.method==="PUT");
  expect(write![0]).toBe(path);
  expect(JSON.parse(write![1].body)).toEqual({version:1,requirements:{...defaultPet,species:"cat"}});
  fireEvent.click(screen.getByRole("button",{name:"重新載入並捨棄未儲存的寵物條件"}));
  await waitFor(()=>expect(screen.queryByDisplayValue("cat")).toBeNull());
  expect(screen.getByDisplayValue("dog")).toBeTruthy();
 });
 it("keeps species suggestions out of the input accessible name",()=>{
  const change=vi.fn();
  render(<PetRequirementFields value={defaultPet} onChange={change}/>);
  const species=screen.getByRole("combobox",{name:"動物種類"});
  expect(screen.getByLabelText("動物種類",{exact:true})).toBe(species);
  fireEvent.change(species,{target:{value:"cat"}});
  expect(change).toHaveBeenCalledWith({...defaultPet,species:"cat"});
 });
 it("lets an administrator review a pending place with explicit dog-only conditions",async()=>{
  const place={id:"candidate",name:"Pet cafe",destination:"Taipei",country:"TW",kind:"cafe",address:"",names:{},
   policies:[],official_url:"https://example.com/pets",source_url:null,latitude:null,longitude:null,
   coordinate_source_url:null,verification_current:false,status:"pending",version:1};
  mock.api.mockImplementation(async()=>({items:[place]}));
  render(<PetAdmin/>);
  fireEvent.click(await screen.findByRole("button",{name:"查核規定"}));
  const review=within(screen.getByRole("dialog",{name:"查核規定"}));
  fireEvent.click(review.getByRole("button",{name:"新增動物種類規定"}));
  const rule=within(review.getByRole("group",{name:"第 1 組動物規定"}));
  fireEvent.change(rule.getByLabelText("狀態"),{target:{value:"conditional"}});
  fireEvent.change(rule.getByRole("combobox",{name:"體重限制"}),{target:{value:"limited"}});
  fireEvent.change(rule.getByRole("spinbutton",{name:"體重限制"}),{target:{value:"10"}});
  fireEvent.change(rule.getByRole("combobox",{name:"數量限制"}),{target:{value:"none"}});
  for(const label of ["須提籠","須推車","須禮貌帶／尿布"])
   fireEvent.change(rule.getByLabelText(label),{target:{value:"false"}});
  fireEvent.change(rule.getByLabelText("須牽繩"),{target:{value:"true"}});
  fireEvent.change(rule.getByLabelText("可進室內"),{target:{value:"true"}});
  fireEvent.change(review.getByLabelText("原因"),{target:{value:"Checked official source"}});
  fireEvent.click(review.getByRole("button",{name:"儲存查核結果"}));
  await screen.findByRole("button",{name:"查核規定"});
  const write=mock.api.mock.calls.find(([,options])=>options?.method==="PUT");
  expect(JSON.parse(write![1].body).policies).toEqual([expect.objectContaining({species:"dog",max_weight_kg:10,
   count_limit:"none",indoor_allowed:true,outdoor_allowed:null})]);
 });
 it("does not display an unknown requirement as unrestricted",()=>{
  render(<Rules rules={[unknownPetRule]}/>);
  expect(screen.getAllByText("未知").length).toBeGreaterThan(5);
  expect(screen.queryByText("已確認無限制")).toBeNull();
 });
 it("requires an explicit tri-state choice for reviewed conditions",()=>{
  const change=vi.fn();
  render(<PetRulesEditor rules={[unknownPetRule]} onChange={change}/>);
  fireEvent.change(screen.getByLabelText("可進室內"),{target:{value:"false"}});
  expect(change.mock.calls[0][0][0].indoor_allowed).toBe(false);
  expect(change.mock.calls[0][0][0].outdoor_allowed).toBeNull();
 });
});
