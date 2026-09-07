import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { CommunityGate } from "./shell";
import { Tabs } from "./ui";
import { Rules } from "./pets";
import { PetRulesEditor } from "./pet-admin";
import { PostEditor } from "./editor";
import { ProfileEditor } from "./profile";
import { TranslateText } from "./post";
import { catchUpMessages } from "./messages";
import { CommunityAdmin } from "./admin";
import { AppBottomNav } from "../app-bottom-nav";
import { unknownPetRule } from "@/lib/community/types";
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
