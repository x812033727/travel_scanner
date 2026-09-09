import { expect, test, type Page } from "@playwright/test";
import { getDiscoveryCopy } from "../lib/discovery-copy";
import { getFrontendFlowCopy } from "../lib/frontend-flow-copy";
import { frontendCopy } from "../lib/frontend-navigation";
import type { DiscoveryItem } from "../lib/discovery";

const id = "11000000-0000-4000-8000-000000000001";
const tripId = "22000000-0000-4000-8000-000000000001";
const userId = "33000000-0000-4000-8000-000000000001";
const listId = "44000000-0000-4000-8000-000000000001";
const item: DiscoveryItem = { id:`hotspot:${id}`, kind:"hotspot", title:"Tokyo riverside · UX fixture", summary:"Reviewed test content. No invented place photography or provider requests.", locale:"en", href:`/hotspots?hotspot=${id}`, destination:{id:"tokyo",name:"Tokyo"}, source:{label:"Isolated editorial fixture",url:null,kind:"editorial"}, published_at:null, updated_at:null, thumbnail_url:null, collection_ref:{kind:"hotspot",id}, detail:{guides:[], merchants:[], intro:{body:"A quiet place to begin a travel plan. This is isolated test data.",locale:"en",source:"fixture"}, planning:{kind:"hotspot",id,destination_id:"tokyo",selection_path:`/hotspots/${id}/trip-selections`,merchants:[]}} };

async function fixtures(page: Page, signedIn = false) {
  let authenticated = signedIn, saved = false, collected = false, version = 3;
  let list: {id:string;name:string} | undefined;
  const writes: Array<{path:string;method:string;body:Record<string,unknown>}> = [];
  const authenticate = async () => { authenticated = true; await page.context().addCookies([{name:"travel_access",value:"isolated-fixture-not-a-token",url:new URL(page.url()).origin}]); };
  if (signedIn) await page.context().addCookies([{name:"travel_access",value:"isolated-fixture-not-a-token",url:process.env.PLAYWRIGHT_BASE_URL || `http://127.0.0.1:${process.env.PLAYWRIGHT_PORT || "3137"}`}]);
  await page.route("**/api/travel/**", async (route) => {
    const request = route.request(), url = new URL(request.url()), path = url.pathname.replace("/api/travel", ""), method = request.method();
    const send = (body:unknown,status=200) => route.fulfill({status,contentType:"application/json",body:JSON.stringify(body)});
    const state = {key:item.id,saved,collection_ids:collected ? [listId] : []};
    if (path === "/discovery/status") return send({enabled:true});
    if (path === "/community/status") return send({enabled:false});
    if (path === "/analytics/config") return send({first_party_enabled:false,ga4_enabled:false});
    if (path === "/auth/me") return authenticated ? send({id:userId,email:"fixture@example.test",email_verified:true}) : send({},401);
    if (path === "/auth/providers") return send({providers:[]});
    if (path === "/runtime/site-visibility") return send({hotspots_enabled:true,trips_enabled:true,alerts_enabled:true,flight_status_enabled:true,airline_fares_enabled:true,pricing_enabled:true});
    if (path === "/discovery/suggestions") return send({query:url.searchParams.get("q"),items:[],destinations:[{id:"tokyo",name:"Tokyo"}],topics:[]});
    if (["/discovery/feed","/discovery/search"].includes(path)) return send({enabled:true,query:url.searchParams.get("q") || "",items:[item],next_cursor:null,filters:{kinds:[],destinations:[],topics:[]}});
    if (path === `/discovery/content/hotspot/${id}`) return send(item);
    if (!authenticated && path.startsWith("/saved-items")) return send({},401);
    if (path === "/saved-items") return send({items:saved ? [{type:"hotspot",id}] : []});
    if (path === "/saved-items/states") return send({items:[state]});
    if (path === "/saved-items/all") return send({items:saved ? [{...state,type:"hotspot",id,saved_at:"2026-09-09T00:00:00Z",unavailable:false,discovery:item}] : [],total:saved ? 1 : 0,has_more:false,next_cursor:null});
    if (method !== "GET") writes.push({path,method,body:request.postData() ? request.postDataJSON() : {}});
    if (path === `/saved-items/hotspot/${id}`) { saved = method === "PUT"; return method === "DELETE" ? route.fulfill({status:204}) : send({...state,type:"hotspot",id,saved}); }
    if (path === "/saved-items/collections") {
      if (method === "POST") { list = {id:listId,name:request.postDataJSON().name}; return send(list); }
      return send({items:list ? [list] : []});
    }
    if (path === `/saved-items/collections/${listId}/items`) { collected = true; return send({id:"membership"}); }
    if (path === "/trips/options") return send({items:[{trip_id:tripId,name:"Autumn Tokyo",destination_id:"tokyo",destination_name:"東京",version,start_date:"2027-04-08",end_date:"2027-04-10"}],count:1,limit:20,can_create:true});
    if (path.endsWith("/trip-selections")) { version++; return send({version}); }
    if (path === "/trips") return send([]);
    return send({code:"fixture_endpoint_unavailable"},404);
  });
  return {writes,authenticate};
}

for (const locale of ["zh-TW","zh-CN","en","ja","ko"]) {
  test(`editorial ${locale}: first card, four destinations, dark/large/reduced motion`, async ({page,isMobile}, info) => {
    await fixtures(page); const c = getDiscoveryCopy(locale), f = getFrontendFlowCopy(locale), n = frontendCopy(locale);
    await page.goto(`/${locale}`);
    await expect(page.getByRole("heading", {name:f.editorial,exact:true})).toBeVisible();
    const title = page.getByRole("link",{name:item.title,exact:true});
    await expect(title).toBeVisible();
    if (isMobile) {
      const box = await title.boundingBox(); expect(box!.y + box!.height).toBeLessThan(page.viewportSize()!.height - 60);
      const nav = page.locator(".app-bottom-nav"); await expect(nav.getByRole("link")).toHaveCount(4);
      await expect(nav.getByRole("link",{name:n.trips,exact:true})).toBeVisible();
      for (const link of await nav.getByRole("link").all()) expect((await link.boundingBox())!.height).toBeGreaterThanOrEqual(44);
    }
    await expect(page.locator("#trip-search")).toHaveCount(0);
    await page.screenshot({path:info.outputPath(`after-home-${locale}.png`),fullPage:true});
    await page.goto(`/${locale}/explore?destination=tokyo`);
    await expect(page.getByRole("link",{name:item.title,exact:true})).toBeVisible();
    if(isMobile) { const box = await page.getByRole("link",{name:item.title,exact:true}).boundingBox(); expect(box!.y).toBeLessThan(page.viewportSize()!.height - 60); }
    await page.emulateMedia({colorScheme:"dark",reducedMotion:"reduce"});
    await page.evaluate(() => { document.documentElement.dataset.theme="dark"; document.documentElement.dataset.textSize="large"; });
    expect(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)).toBe(false);
    await page.screenshot({path:info.outputPath(`after-explore-dark-large-${locale}.png`),fullPage:true});
    await page.getByRole("link",{name:item.title,exact:true}).click();
    await expect(page.getByRole("dialog",{name:c.details,exact:true})).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.getByRole("dialog")).toHaveCount(0);
    await expect(page).toHaveURL(/destination=tokyo/);
  });
}

test("guest reading → confirmed sign-in return → save → organize → trip → reload", async ({page}, info) => {
  const {writes,authenticate} = await fixtures(page); const c=getDiscoveryCopy("en"), f=getFrontendFlowCopy("en"), n=frontendCopy("en");
  await page.goto("/en/explore?q=Tokyo&destination=tokyo");
  await page.getByRole("link",{name:item.title,exact:true}).click();
  const detail=page.getByRole("dialog",{name:c.details,exact:true});
  await expect(detail).toContainText("A quiet place");
  const login=detail.getByRole("link",{name:f.saveItem,exact:true});
  const next=new URL((await login.getAttribute("href"))!,page.url()).searchParams.get("next")!;
  expect(writes).toHaveLength(0);
  // Controlled authentication fixture, not proof of the real login endpoint (see full-stack test).
  await authenticate(); await page.goto(`/en${next}`);
  const confirmation=page.getByRole("dialog",{name:f.confirmSave,exact:true});
  await expect(confirmation).toBeVisible(); expect(writes).toHaveLength(0);
  await confirmation.getByRole("button",{name:f.confirmSave,exact:true}).click();
  await expect(confirmation).toHaveCount(0);
  expect(writes.filter((entry)=>entry.method==="PUT")).toHaveLength(1);
  await detail.getByRole("button",{name:`${f.organize}: ${item.title}`,exact:true}).click();
  const organizer=page.getByRole("dialog",{name:`${f.organize}: ${item.title}`,exact:true});
  await organizer.getByLabel(f.listName,{exact:true}).fill("Spring ideas");
  await organizer.getByRole("button",{name:f.createList,exact:true}).click();
  await expect(organizer.getByText("Spring ideas",{exact:true})).toBeVisible();
  await page.keyboard.press("Escape"); await expect(detail).toBeVisible();
  await detail.getByRole("button",{name:n.plan,exact:true}).click();
  const planning=page.getByRole("dialog",{name:n.plan,exact:true});
  await expect(planning.getByLabel(n.chooseTrip,{exact:true})).toHaveValue(tripId);
  expect(writes.filter((entry)=>entry.path.endsWith("/trip-selections"))).toHaveLength(0);
  await planning.getByRole("button",{name:n.confirm,exact:true}).click();
  await expect(planning).toHaveCount(0);
  expect(writes.find((entry)=>entry.path.endsWith("/trip-selections"))?.body).toMatchObject({trip_id:tripId,version:3,day_date:"2027-04-08"});
  await page.goto("/en/explore/collections"); await page.reload();
  await expect(page.getByRole("link",{name:item.title,exact:true})).toHaveCount(1);
  await page.screenshot({path:info.outputPath("saved-organized-after-reload.png"),fullPage:true});
});

test("legacy search anchor leads to the opt-in search form", async ({page}) => {
  const {writes}=await fixtures(page);
  await page.goto("/en#trip-search");
  await expect(page).toHaveURL(/\/en\/search\/new$/);
  await expect(page.getByRole("button",{name:frontendCopy("en").query})).toBeVisible();
  expect(writes.filter((entry)=>entry.path.includes("search"))).toHaveLength(0);
});

test("production before capture is read-only and opt-in", async ({page},info) => {
  test.skip(process.env.FRONTEND_CAPTURE_BASELINE !== "1", "Opt-in public production screenshot only");
  await page.goto("https://mokaair.com/zh-TW");
  await expect(page.locator("#trip-search")).toBeVisible();
  await page.screenshot({path:info.outputPath("before-production-home.png"),fullPage:true});
});
