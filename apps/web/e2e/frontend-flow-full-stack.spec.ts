import { expect, request, test, type APIRequestContext, type Page } from "@playwright/test";
import { getFrontendFlowCopy } from "../lib/frontend-flow-copy";
import { getDiscoveryCopy } from "../lib/discovery-copy";
import { frontendCopy } from "../lib/frontend-navigation";
import { newTripCopy } from "../components/planner/new-trip-copy";

// The fixture is seeded only in the isolated acceptance DB. All reads and writes
// below use normal BFF/API/browser paths; no intercepts, injected tokens or providers.
test.skip(process.env.DISCOVERY_E2E !== "1", "Requires isolated PostgreSQL/Redis/Mailpit acceptance services");
const id="55000000-0000-4000-8000-000000000001", title="Frontend flow fixture Tokyo river";
const origin=new URL(process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000").origin;
async function json(client:APIRequestContext,method:string,path:string,data?:unknown) {
  const response=await client.fetch(`/api/travel${path}`,{method,data,headers:{Origin:origin,"X-Travel-Locale":"en"}});
  expect(response.ok(),`${method} ${path}: ${await response.text()}`).toBe(true);
  return response.status()===204 ? null : response.json();
}
async function verifyMail(page:Page,email:string) {
  await json(page.request,"POST","/auth/request-verification");
  let link="";
  await expect.poll(async()=>{
    const messages=await page.request.get(`http://127.0.0.1:8025/api/v1/search?query=${encodeURIComponent(`to:${email}`)}`);
    const mailId=(await messages.json()).messages?.[0]?.ID;
    if(!mailId) return false;
    const message=await page.request.get(`http://127.0.0.1:8025/api/v1/message/${mailId}`);
    link=(await message.json()).Text.match(/https?:\/\/[^\s]+#token=[A-Za-z0-9_-]+/)?.[0] || "";
    return Boolean(link);
  },{timeout:45_000,intervals:[500,1000,2000]}).toBe(true);
  const url=new URL(link); await page.goto(url.pathname+url.search+url.hash);
  await page.getByRole("button",{name:/^(Confirm|確認)$/}).click();
  await expect.poll(async()=>(await json(page.request,"GET","/auth/me")).email_verified).toBe(true);
}

test("public idea → real login → saved/list → create trip → explicit add → persisted",async({page},info)=>{
  test.setTimeout(240_000);
  const f=getFrontendFlowCopy("en"), c=getDiscoveryCopy("en"), n=frontendCopy("en"), form=newTripCopy("en");
  const admin=await request.newContext({baseURL:origin});
  try {
    await json(admin,"POST","/auth/login",{email:"discovery-admin@example.com",password:"discovery-ci-password-123"});
    const existing=await json(admin,"GET","/admin/community/settings");
    await json(admin,"PUT","/admin/community/settings",{settings:{...existing.settings,enabled:false},reason:"Isolated frontend acceptance with community disabled"});
  } finally { await admin.dispose(); }
  expect((await json(page.request,"GET","/community/status")).enabled).toBe(false);
  const email=`frontend${Date.now()}${info.workerIndex}@example.com`,password="frontend-fixture-password-123";
  await json(page.request,"POST","/auth/register",{email,password,preferred_locale:"en"});
  await verifyMail(page,email);
  await json(page.request,"POST","/auth/logout");
  const mutations:string[]=[];
  page.on("request",request=>{if(["PUT","POST","DELETE","PATCH"].includes(request.method())) mutations.push(new URL(request.url()).pathname);});
  await page.goto(`/en/explore?q=${encodeURIComponent(title)}&category=hotspots`);
  await page.getByRole("link",{name:title,exact:true}).click();
  const detail=page.getByRole("dialog",{name:c.details,exact:true});
  await expect(detail.getByRole("heading",{name:title,exact:true})).toBeVisible();
  await detail.getByRole("link",{name:f.saveItem,exact:true}).click();
  await expect(page).toHaveURL(/\/login\?next=/);
  await expect(page.getByLabel("Email",{exact:true})).toBeEnabled();
  await page.getByLabel("Email",{exact:true}).fill(email);
  await page.getByLabel("Password",{exact:true}).fill(password);
  await page.getByRole("button",{name:"Sign in",exact:true}).click();
  const save=page.getByRole("dialog",{name:f.confirmSave,exact:true});
  await expect(save).toBeVisible();
  expect(mutations.filter(path=>path.includes(`/saved-items/hotspot/${id}`))).toHaveLength(0);
  await save.getByRole("button",{name:f.confirmSave,exact:true}).click();
  await expect(save).toHaveCount(0);
  expect((await json(page.request,"GET","/saved-items/all?limit=24")).items).toHaveLength(1);
  await detail.getByRole("button",{name:`${f.organize}: ${title}`,exact:true}).click();
  const organize=page.getByRole("dialog",{name:`${f.organize}: ${title}`,exact:true});
  await organize.getByLabel(f.listName,{exact:true}).fill("Next spring");
  await organize.getByRole("button",{name:f.createList,exact:true}).click();
  await expect(organize.getByText("Next spring",{exact:true})).toBeVisible();
  await page.keyboard.press("Escape");
  await detail.getByRole("button",{name:n.plan,exact:true}).click();
  let plan=page.getByRole("dialog",{name:n.plan,exact:true});
  await plan.getByRole("button",{name:n.create,exact:true}).click();
  await expect(page).toHaveURL(/\/trips\/new\?resume_plan=1/);
  await expect(page.locator("#trip-destination")).toBeEnabled();
  await page.locator("#trip-destination").fill("Tokyo");
  await page.getByRole("group",{name:"Trip dates",exact:true}).getByRole("button").click();
  const start=new Date();start.setUTCDate(start.getUTCDate()+40);
  const end=new Date(start);end.setUTCDate(end.getUTCDate()+2);
  const startDay=start.toISOString().slice(0,10),endDay=end.toISOString().slice(0,10);
  for(const day of [startDay,endDay]) {
    for(let i=0;i<12 && !(await page.locator(`[data-date="${day}"]`).count());i++) await page.getByRole("button",{name:"Next month",exact:true}).click();
    await page.locator(`[data-date="${day}"]`).click();
  }
  await expect(page.getByRole("button",{name:form.closeCalendar,exact:true})).toHaveCount(0);
  await page.getByRole("button",{name:form.submit,exact:true}).click();
  await expect(page).toHaveURL(/resume_trip=/);
  const tripId=new URL(page.url()).searchParams.get("resume_trip")!;
  plan=page.getByRole("dialog",{name:n.plan,exact:true});
  await expect(plan.getByRole("combobox",{name:n.chooseTrip,exact:true})).toHaveValue(tripId);
  expect(mutations.filter(path=>path.endsWith("/trip-selections"))).toHaveLength(0);
  await plan.getByRole("button",{name:n.confirm,exact:true}).click();
  await expect(plan).toHaveCount(0);
  const trip=await json(page.request,"GET",`/trips/${tripId}`);
  expect(trip.start_date).toBe(startDay);
  expect(trip.end_date).toBe(endDay);
  expect(JSON.stringify(trip.items)).toContain(id);
  await page.goto("/en/explore/collections");await page.reload();
  await expect(page.getByRole("link",{name:title,exact:true})).toHaveCount(1);
  await page.screenshot({path:info.outputPath("full-stack-saved-to-trip.png"),fullPage:true});
  const lists=await json(page.request,"GET","/saved-items/collections");
  const list=lists.items.find((entry:{name:string})=>entry.name==="Next spring");
  await json(page.request,"DELETE",`/saved-items/collections/${list.id}`);
  expect((await json(page.request,"GET","/saved-items/all?limit=24")).items).toHaveLength(1);
  expect((await json(page.request,"POST","/saved-items/states",{keys:[`hotspot:${id}`]})).items[0].collection_ids).toEqual([]);
});
