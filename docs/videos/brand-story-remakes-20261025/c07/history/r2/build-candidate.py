#!/usr/bin/env python3
"""Build C07 r2 author files only; no provider/backend/verify."""
from pathlib import Path
import copy, datetime, hashlib, json, re, subprocess
OUT=Path(__file__).resolve().parent
REPO=OUT.parents[3]
R1=OUT/"history"/"r1"
AUDIT=Path("/workspace/work/brand-story-20261025/c07-audit")
NEW=AUDIT/"r2-source-cache"
ROOT=Path("/workspace/work/brand-story-20261025/c07-submission-root")
SLUG="story-everyday-dr-martens-c07-remake-20261025"
DATA=json.loads(r'''
{
  "chapters": [
    {
      "title": "刀伸進了舊靴的鞋邊",
      "rows": [
        {
          "text": "你穿了四年的靴子，底快磨穿了，鞋面還好，現在會想留下哪一半？",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "first paragraph, explicitly attributed in next line",
          "id": "c7r20101",
          "action": "examining a worn lace-up work boot with a thin outsole"
        },
        {
          "text": "二〇二五年七月，一位馬汀靴送修者在公開評論裡，寫下這個難題。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "publishedDate 2025-07-11; four years, upper fine, sole almost worn through",
          "id": "c7r20102",
          "action": "writing on a blank page beside a worn plain boot"
        },
        {
          "text": "星期四，對方把鞋放進舊鞋盒，印好郵寄標籤；隔天，郵差收走了盒子。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "Thursday packed old shoebox and printed prepaid label; next-day collection",
          "id": "c7r20103",
          "action": "placing worn lace-up boots into a used unmarked shoebox"
        },
        {
          "text": "我想跟著它看：修理要拆到哪裡，包裹回來時，又多了什麼？",
          "sources": [
            "T7_repairs_resole",
            "R2_CUSTOMER_6870"
          ],
          "locator": "teardown scope; laces surprise withheld",
          "id": "c7r20104",
          "action": "studying an idle shoe-joining machine beside a closed parcel"
        },
        {
          "text": "今天沿著一雙馬汀靴的三個接合部件，走一趟拆開、接回、送回的旅程。",
          "sources": [
            "T7_repairs_resole",
            "T3_plc_product"
          ],
          "locator": "sole welt stitching; current construction",
          "id": "c7r20105",
          "action": "holding a plain unfinished boot above a repair bench"
        },
        {
          "text": "為了留下你穿慣的鞋面，換掉的到底會有哪些東西？",
          "sources": [
            "T7_repairs_resole",
            "R2_CUSTOMER_6870"
          ],
          "locator": "central question",
          "id": "c7r20106",
          "action": "tracing the seam around a worn work boot"
        }
      ]
    },
    {
      "title": "鞋邊先替它找到修理方式",
      "rows": [
        {
          "text": "鞋盒離手以前，這位送修者已經在網站選過修理，也選了新的配色。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "choose colour of sole/welt/stitching before posting",
          "id": "c7r20201",
          "action": "choosing a plain replacement sole beside a worn boot"
        },
        {
          "text": "對方說，能挑鞋底和縫線的顏色，這件事很有趣。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "customer opinion choosing colours was fun; weld is review's wording",
          "id": "c7r20202",
          "action": "holding a coloured thread spool beside a narrow footwear band"
        },
        {
          "text": "選項裡有一條沿條，可是它在鞋上的哪裡？",
          "sources": [
            "T7_repairs_resole",
            "T8_repairs_welted"
          ],
          "locator": "identification",
          "id": "c7r20203",
          "action": "looking closely at the stitched edge of a work boot"
        },
        {
          "text": "你順著鞋面往下看，鞋邊有一條繞著鞋身的帶子，上面可以看見縫線。",
          "sources": [
            "T8_repairs_welted",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "identification paragraph; 2–4s",
          "id": "c7r20204",
          "action": "pointing to a narrow band below a boot upper"
        },
        {
          "text": "維修方說，有沿條的鞋，會在這個部位露出細小的縫隙。",
          "sources": [
            "T8_repairs_welted"
          ],
          "locator": "small visible gap",
          "id": "c7r20205",
          "action": "touching the small gap along a stitched boot rim"
        },
        {
          "text": "從正上方看，鞋底邊緣還伸出比較寬的一圈，不跟鞋面完全齊平。",
          "sources": [
            "T8_repairs_welted"
          ],
          "locator": "wide profile from birds eye view",
          "id": "c7r20206",
          "action": "examining the wide outline of a boot sole from above"
        },
        {
          "text": "這是送修網站拿來分辨構造的線索，先讓人找到對應的維修項目。",
          "sources": [
            "T5_repairs",
            "T8_repairs_welted"
          ],
          "locator": "welted and non-welted categories",
          "id": "c7r20207",
          "action": "comparing a stitched shoe edge with a separate plain band"
        },
        {
          "text": "我原先會把那圈線看成裝飾；近看才注意，它縫著一個真正的部件。",
          "sources": [
            "T3_plc_product",
            "T8_repairs_welted"
          ],
          "locator": "welt stitched to upper",
          "id": "c7r20208",
          "action": "lifting the edge of a worn boot to inspect its stitching"
        },
        {
          "text": "那條帶子叫做沿條，縫在鞋面下緣；網站把換底和換沿條列成同一項修理。",
          "sources": [
            "T7_repairs_resole",
            "T3_plc_product"
          ],
          "locator": "service name and construction",
          "id": "c7r20209",
          "action": "placing a flexible band beside the lower edge of a boot upper"
        },
        {
          "id": "c7r20234",
          "text": "要把這一雙交出去修，現在頁面標出的費用是多少？",
          "sources": [
            "T7_repairs_resole"
          ],
          "locator": "current listed £79.99 per pair; not reviewer's historical payment",
          "action": "holding a worn pair beside a blank service card at a counter"
        },
        {
          "text": "目前網站的經典換底加換沿條，標價是一雙七十九英鎊九十九便士。",
          "sources": [
            "T7_repairs_resole"
          ],
          "locator": "current listed per-pair price £79.99 at retrieval; no claim this was the reviewer's 2025 payment",
          "id": "c7r20210",
          "action": "examining a blank service card beside a pair of worn boots"
        },
        {
          "text": "這是成對的換底與重做接合；鞋面如果另有補線，需要先看照片，再另外報價。",
          "sources": [
            "T7_repairs_resole"
          ],
          "locator": "service per pair plus separately quoted stitching repairs; no availability claim",
          "id": "c7r20211",
          "action": "holding a phone over a small loose thread on a boot"
        },
        {
          "text": "這雙鞋要換的不只有顏色，還得把穿過的部件，換成能重新接合的部件。",
          "sources": [
            "T7_repairs_resole"
          ],
          "locator": "fresh welt new stitching and chosen sole; editorial description",
          "id": "c7r20212",
          "action": "arranging a replacement sole beside an upright boot upper"
        },
        {
          "text": "這位送修者選擇修理。評論裡說，在對方看來，這比買二手還便宜。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "customer's personal price judgment, not market-wide comparison",
          "id": "c7r20213",
          "action": "considering a worn boot beside a plain secondhand shoe"
        },
        {
          "text": "四年來穿著的上半部還好，腳下的底卻幾乎磨穿，這才把一雙鞋送上兩種去留。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "upper fine sole almost worn through; editorial description",
          "id": "c7r20214",
          "action": "turning a worn boot to inspect its upper and sole"
        },
        {
          "text": "品牌二〇二三年的說明會裡，也有人提過這種請求。",
          "sources": [
            "TEACH_T"
          ],
          "locator": "repair section p13–14",
          "id": "c7r20215",
          "action": "holding an old lace-up boot at a plain lectern"
        },
        {
          "text": "主管梅基克當時說，有人珍惜用了二十年的舊靴，底磨壞了，皮鞋面卻還很好。",
          "sources": [
            "TEACH_T"
          ],
          "locator": "attributed 20-year consumer example; not the 2025 reviewer",
          "id": "c7r20216",
          "action": "examining a well-used boot with an intact upper"
        },
        {
          "text": "鞋面還好，把靴口翻開，裡面若已磨穿，要把整張外皮也換掉嗎？",
          "sources": [
            "R2_UPPER"
          ],
          "locator": "conditional viewer inspection; heel lining described separately from upper",
          "id": "c7r20217",
          "action": "opening the boot shaft to inspect the inner heel"
        },
        {
          "text": "若這裡已經磨穿，維修方提供的是修補，或換上新的皮內裡，不必因此把外皮整張換掉。",
          "sources": [
            "R2_UPPER"
          ],
          "locator": "HEEL LINING REPAIR: repair or replace with new leather; outer upper retained as service explanation",
          "id": "c7r20218",
          "action": "holding a new plain heel-lining patch beside a boot opening"
        },
        {
          "text": "照他們的說法，處理內裡能恢復舒適，也減少上層鞋面進一步受磨。",
          "sources": [
            "R2_UPPER"
          ],
          "locator": "restores comfort and prevents further wear to upper, attributed",
          "id": "c7r20219",
          "action": "touching the inside heel of a plain lace-up boot"
        },
        {
          "text": "你要留下的外皮，和腳在裡面碰到的內裡，在這裡成了能分開處理的部位。",
          "sources": [
            "R2_UPPER"
          ],
          "locator": "explanation of inner lining repair as distinct component; not condition of either filmed or reviewed pair",
          "id": "c7r20220",
          "action": "placing a plain lining sample beside a worn outer upper"
        },
        {
          "text": "現在的英國授權網站，讓穿著者先選修理項目，再把自己的鞋寄給維修方。",
          "sources": [
            "T6_repairs_faq",
            "R2_HOW"
          ],
          "locator": "order and post",
          "id": "c7r20221",
          "action": "choosing a repair item on a blank screen beside a boot"
        },
        {
          "text": "分不清鞋款的人，可以先問維修團隊；需要的項目沒列出來，也能請他們另行報價。",
          "sources": [
            "T6_repairs_faq",
            "R2_CHOOSE"
          ],
          "locator": "contact experts and custom enquiries",
          "id": "c7r20222",
          "action": "holding a boot while consulting a blank phone screen"
        },
        {
          "text": "如果鞋面另有要補的縫線，就先把照片和需求交過去，讓維修方針對那項工作報價。",
          "sources": [
            "T7_repairs_resole"
          ],
          "locator": "bespoke stitching repair with photos",
          "id": "c7r20223",
          "action": "photographing a loose stitch on a plain boot"
        },
        {
          "text": "你交出去的，不只是一個型號；鞋況、想換的部件，都得跟著這雙鞋進入修理。",
          "sources": [
            "T6_repairs_faq",
            "T7_repairs_resole"
          ],
          "locator": "editorial explanation of individual quote and service",
          "id": "c7r20224",
          "action": "laying a worn pair beside a blank repair form"
        },
        {
          "text": "在那則評論裡，送修者把靴子收進舊鞋盒，自己印了預付郵寄標籤。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "old shoebox and printed prepaid label",
          "id": "c7r20225",
          "action": "folding tissue around a pair in a used plain shoebox"
        },
        {
          "text": "對方還特別寫到，這次寄送沒有另付郵資，接著等郵差上門取件。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "individual postage account and next-day Royal Mail collection",
          "id": "c7r20226",
          "action": "placing an unmarked prepaid label beside a closed parcel"
        },
        {
          "text": "網站要求放入訂單確認、姓名和地址；標籤自己印不出來，還能送嗎？",
          "sources": [
            "T6_repairs_faq"
          ],
          "locator": "secure packaging and order confirmation/name/address",
          "id": "c7r20227",
          "action": "adding a blank order slip to a sturdy shoebox"
        },
        {
          "text": "沒有印表機的人，也能把專屬碼帶到郵局，由皇家郵政幫忙印出郵寄標籤。",
          "sources": [
            "T6_repairs_faq",
            "R2_HOW"
          ],
          "locator": "Royal Mail can print label from unique QR code; present service option, not the reviewer's act",
          "id": "c7r20228",
          "action": "presenting a phone with an unreadable code screen at a plain postal counter"
        },
        {
          "text": "如果是我，會先說清楚想留下的地方，再決定要委託換掉哪些部件。",
          "sources": [
            "T7_repairs_resole"
          ],
          "locator": "editorial preference",
          "id": "c7r20229",
          "action": "considering a worn upper beside a replacement sole"
        },
        {
          "text": "鞋送出去，穿著者會先等到什麼消息？",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "first receipt update",
          "id": "c7r20230",
          "action": "looking at a blank notification screen beside an empty shoebox"
        },
        {
          "text": "這位送修者說，維修方收到靴子後，先發來通知，鞋已經到站了。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "update once received boots",
          "id": "c7r20231",
          "action": "reading a blank message screen after posting a parcel"
        },
        {
          "text": "通知讓主人知道包裹到了；工作檯上，接著輪到人把舊接合拆開。",
          "sources": [
            "R2_CUSTOMER_6870",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "editorial transition from reported receipt to separate authorised demonstration",
          "id": "c7r20232",
          "action": "holding a closed shoe parcel at a repair counter"
        },
        {
          "text": "師傅手上的刀，會讓這雙靴子先少掉什麼？",
          "sources": [
            "T7_repairs_resole",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "teardown scope; separate demonstration 5–7s",
          "id": "c7r20233",
          "action": "positioning a worn boot upside down on a repair stand"
        }
      ]
    },
    {
      "title": "舊底拆走，新線繞上鞋面",
      "rows": [
        {
          "text": "示範裡，師傅把一雙舊靴倒放在支架上，刀沿著鞋底上緣走，另一手扶著鞋身。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "5–6s",
          "id": "c7r20301",
          "action": "guiding a plain knife along the upper edge of an old outsole"
        },
        {
          "text": "你還看得到鞋邊舊線，刀口沿著它附近前進，舊接合開始分開。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "5–6s",
          "id": "c7r20302",
          "action": "holding a worn boot steady while opening its old edge seam"
        },
        {
          "text": "接著，靴底已經露出內層，外面原本貼地的整塊底不在了。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "6–7.5s",
          "id": "c7r20303",
          "action": "examining the exposed underside of an intact boot upper"
        },
        {
          "text": "授權換底頁寫明，舊外底、舊沿條和舊縫線，這三樣都會移走。",
          "sources": [
            "T7_repairs_resole"
          ],
          "locator": "old sole, welt, stitching gone",
          "id": "c7r20304",
          "action": "placing a detached sole beside a worn band and loose thread"
        },
        {
          "text": "靴筒和皺折還在，下緣露出接合位置；師傅接著會把這裡送向哪個工具？",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "6–8s",
          "id": "c7r20305",
          "action": "lifting a boot upper with its lower joining edge exposed"
        },
        {
          "text": "我看到的是兩種老去的速度：外底被換下，皮鞋面還能跟著修下去。",
          "sources": [
            "TEACH_T",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "upper still great while outsole worn; repair demonstration",
          "id": "c7r20306",
          "action": "comparing a worn outsole with the retained boot upper"
        },
        {
          "text": "鏡頭接著對準倒過來的靴底，一個噴口靠近露出的底層，師傅用布包住握鞋的手。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "6–7.5s; nozzle near exposed base and cloth at supporting hand; no inferred temperature",
          "id": "c7r20307",
          "action": "holding an inverted boot near a guarded nozzle with a cloth-wrapped hand"
        },
        {
          "text": "鞋底朝上、靴筒朝下，他把上半部整個握在手裡，沒有把皮面拆成一片片。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "6–8s; intact three-dimensional upper after outsole removal",
          "id": "c7r20308",
          "action": "gripping an intact boot upper with its base facing upwards"
        },
        {
          "text": "下方要重新接合，上方仍維持著鞋的形狀；接著，這個留下來的部分才被送向機針。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "7.5–8s transition, retained upper oriented toward sewing machine",
          "id": "c7r20309",
          "action": "moving a retained boot upper toward an idle stitching machine"
        },
        {
          "text": "可是舊底都拿走了，新底要直接縫到這層皮上嗎？",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "welt first stitched to upper",
          "id": "c7r20310",
          "action": "holding a separate sole near the exposed lower edge of an upper"
        },
        {
          "text": "原廠現行工法先處理沿條：把一條聚氯乙烯材料做的帶子，縫上鞋面。",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "PVC welt first stitched to upper",
          "id": "c7r20311",
          "action": "guiding a flexible band along a boot upper at a sewing station"
        },
        {
          "text": "車線先把沿條和上半部連在一起，整塊貼地的外底，還沒有跟著進來。",
          "sources": [
            "T3_plc_product",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "product joining paragraph; 8–12s",
          "id": "c7r20312",
          "action": "holding an upper and stitched band above a separate sole"
        },
        {
          "text": "示範裡，師傅讓靴子沿著機針轉動，新的縫線一段接一段，繞回鞋邊。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "8–12s",
          "id": "c7r20313",
          "action": "turning a boot slowly at a plain heavy sewing machine"
        },
        {
          "text": "機器往前車，他的手也跟著調整位置，帶著這隻立體的靴子走過機針。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "8–12s",
          "id": "c7r20314",
          "action": "supporting the boot body while guiding its curved edge beneath a needle"
        },
        {
          "text": "鞋底朝上，靴筒朝下，一隻手握住鞋身，另一隻手在靠近針的位置扶住邊緣。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "8–12s",
          "id": "c7r20315",
          "action": "holding an inverted boot with one hand near the stitching edge"
        },
        {
          "text": "舊線既然拆掉，新線還一定得是黃色嗎？",
          "sources": [
            "T7_repairs_resole"
          ],
          "locator": "stitching choices",
          "id": "c7r20316",
          "action": "considering a yellow spool beside a dark stitched boot edge"
        },
        {
          "text": "這項服務也能選黑色縫線，配的沿條顏色也可以改。",
          "sources": [
            "T7_repairs_resole"
          ],
          "locator": "black stitching and welt choices",
          "id": "c7r20317",
          "action": "choosing a black thread spool beside a plain band"
        },
        {
          "text": "你可以把穿皺的皮留下，再決定新接縫的顏色；這兩個部位，這次能分開作選擇。",
          "sources": [
            "T7_repairs_resole",
            "TEACH_T"
          ],
          "locator": "rebuilt with fresh welt/stitching; old upper retained",
          "id": "c7r20318",
          "action": "examining creases on a retained upper beside fresh stitching"
        },
        {
          "text": "沿條車好，師傅再把靴底朝向砂帶，轉著鞋身磨修邊緣。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "13–14s",
          "id": "c7r20319",
          "action": "turning an unfinished boot edge toward a guarded sanding belt"
        },
        {
          "text": "淺色的底層朝外，黑色鞋邊靠近機器；新外底還沒接上，就先處理這一圈。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "13–14s",
          "id": "c7r20320",
          "action": "holding an inverted upper with its pale base facing a sanding station"
        },
        {
          "text": "現在沿條和鞋面已經連在一起，新外底仍是另一個部件。",
          "sources": [
            "T3_plc_product",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "welt first stitched; 13–17s",
          "id": "c7r20321",
          "action": "placing a stitched upper beside a separate plain outsole"
        },
        {
          "text": "它會怎麼接上去，讓這隻還露著底層的靴子重新能走路？",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "joining procedure",
          "id": "c7r20322",
          "action": "positioning a loose sole beneath the open base of a boot"
        }
      ]
    },
    {
      "title": "熱刀把新底接了回來",
      "rows": [
        {
          "text": "輪到熱接了。師傅拿起新外底，放到已縫好沿條的鞋面下方。",
          "sources": [
            "T3_plc_product",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "joining paragraph; 15–18s",
          "id": "c7r20401",
          "action": "placing a fresh plain outsole under a stitched upper"
        },
        {
          "text": "公司說，今天多數外底用的是聚氯乙烯合金，也就是常叫PVC的塑膠。",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "majority of outsoles alloy of PVC",
          "id": "c7r20402",
          "action": "examining plain plastic granules beside a moulded sole"
        },
        {
          "text": "一粒粒顆粒先熔融，再成型為鞋底，才有前掌、後跟和腳下的輪廓。",
          "sources": [
            "T3_plc_product",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "granules melted and moulded; 15–17s",
          "id": "c7r20403",
          "action": "lifting a formed sole beside an unmarked mould and granules"
        },
        {
          "text": "你熟悉的氣墊，原廠在Original系列裡，用鞋底的氣穴來解釋舒適和吸震。",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "Original products air pockets comfort and shock absorption",
          "id": "c7r20404",
          "action": "holding a simple section model with visible small sole cavities"
        },
        {
          "text": "他調整鞋底與鞋身的位置，讓這個新部件準備接到剛剛縫好的那圈邊。",
          "sources": [
            "R2_REPAIR_VIDEO",
            "T3_plc_product"
          ],
          "locator": "15–18s; joining paragraph",
          "id": "c7r20405",
          "action": "aligning a replacement sole with a stitched footwear band"
        },
        {
          "text": "我原先以為車線縫好就行，這裡卻改用熱刀；這道接底工序要多熱？",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "two sequential joining methods",
          "id": "c7r20406",
          "action": "examining an idle blade tool beside a shoe-joining station"
        },
        {
          "text": "原廠給這道接底工序的數字，是熱接溫度超過六百五十度。",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "welded at temperature in excess of 650C; manufacturing operation only",
          "id": "c7r20407",
          "action": "positioning an unfinished boot at a guarded heated joining tool"
        },
        {
          "text": "熱刀加熱接合處，滾輪再把沿條和外底壓在一起。",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "hot blade and pressurised rollers force parts together",
          "id": "c7r20408",
          "action": "pressing two plain footwear components together at a joining station"
        },
        {
          "text": "示範中，師傅一直扶著鞋身，隨著接合的位置，轉動這隻靴子。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "18–20s",
          "id": "c7r20409",
          "action": "turning a boot by hand beside a guarded assembly machine"
        },
        {
          "text": "鏡頭裡，接合工具靠近鞋邊時，邊緣透出橙紅的亮光，雙手仍扶在鞋身兩側。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "18–20s; visible glow and hand position, not a temperature reading",
          "id": "c7r20410",
          "action": "supporting a boot beside a narrow warm joining edge"
        },
        {
          "text": "修鞋的人把靴子往另一個方向轉，剛才朝著自己的那段鞋邊，又移到機器前。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "18–20s; hand-fed rotation visible across sampled frames",
          "id": "c7r20411",
          "action": "rotating a partly joined boot toward the next side of the tool"
        },
        {
          "text": "你從側面看，新底上緣貼近沿條，剛才分開的兩個部件，沿著邊緣合攏。",
          "sources": [
            "T3_plc_product",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "welding; 18–20s",
          "id": "c7r20412",
          "action": "examining the meeting edges of a fresh sole and a stitched band"
        },
        {
          "text": "拿開熱接工具之後，還得等什麼，才會接成一件？",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "once cooled",
          "id": "c7r20413",
          "action": "holding a newly joined boot away from the idle tool"
        },
        {
          "text": "原廠說，冷卻後，沿條與外底便形成一件PVC，鞋底就接好了。",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "once cooled two components form one piece of PVC",
          "id": "c7r20414",
          "action": "resting a joined boot on a plain cooling rack"
        },
        {
          "text": "再把鞋側過來，縫線沿著鞋面下緣走，它下方的沿條，已經和新底連在一起。",
          "sources": [
            "T3_plc_product",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "completed joining topology; 20–28s",
          "id": "c7r20415",
          "action": "pointing to the stitched band above a joined outsole"
        },
        {
          "text": "這道接底程序沒有使用黏著劑，原廠把它寫成靠熱接完成的連接。",
          "sources": [
            "T3_plc_product"
          ],
          "locator": "sole attached without adhesives; scope this operation only",
          "id": "c7r20416",
          "action": "holding a finished joint sample beside an untouched plain brush"
        },
        {
          "text": "可是鞋接好了，新底邊緣還得怎麼處理，才輪得到鞋主人重新穿？",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "21–28s",
          "id": "c7r20417",
          "action": "moving a newly soled boot toward an edge-finishing station"
        }
      ]
    },
    {
      "title": "新鞋底被修整，舊鞋面被擦亮",
      "rows": [
        {
          "text": "新外底的邊緣，先被師傅送到另一部機器前，沿著四周修整。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "21–23s",
          "id": "c7r20501",
          "action": "guiding a fresh sole edge against a guarded finishing tool"
        },
        {
          "text": "他握著鞋身，讓鞋底沿著旋轉的工具移動，鞋子也跟著手腕換角度。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "21–23s",
          "id": "c7r20502",
          "action": "turning a boot by the wrist beside a rotating edge tool"
        },
        {
          "text": "我覺得有意思的，是新底外緣正被修齊，上半部的使用痕跡卻還留著。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "before 0–4s and after 24–28s; editorial observation",
          "id": "c7r20503",
          "action": "examining a fresh sole below a creased retained upper"
        },
        {
          "text": "你想留下的舊鞋面，表面那些磨痕，又會怎麼處理？",
          "sources": [
            "R2_REPAIR_VIDEO",
            "R2_CLEAN"
          ],
          "locator": "24–26s; upper cleaning and polishing service",
          "id": "c7r20504",
          "action": "looking closely at scuffs on an old upper above a new sole"
        },
        {
          "text": "師傅在工作檯前拿起布，沿著靴筒和鞋面擦拭，手也跟著鞋身移動。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "24–26s; retained upper",
          "id": "c7r20505",
          "action": "wiping the boot shaft with a plain soft cloth"
        },
        {
          "text": "布移過鞋身側邊，擦到已經彎折過的地方，原本灰暗的鞋面開始有了光澤。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "24–26s; before/after visible",
          "id": "c7r20506",
          "action": "polishing a curved area on a creased boot upper"
        },
        {
          "text": "維修方把清潔、補色和拋光，列成處理鞋面材料的服務，目標是盡可能恢復外觀。",
          "sources": [
            "R2_CLEAN"
          ],
          "locator": "Description cleaning, repainting and polishing, upper material as much as possible",
          "id": "c7r20507",
          "action": "holding a cloth beside a plain bottle and worn boot"
        },
        {
          "text": "同樣是留下舊皮，表面的污漬、顏色和光澤，仍可以交給人重新整理。",
          "sources": [
            "R2_CLEAN"
          ],
          "locator": "cleaning repainting polishing; editorial contrast with full outsole replacement",
          "id": "c7r20508",
          "action": "examining the surface of a worn upper beside a folded cleaning cloth"
        },
        {
          "text": "你看到的是在用過的皮上繼續動手，腳下的底整塊換新，鞋面則採取另一種處理。",
          "sources": [
            "R2_CLEAN",
            "T7_repairs_resole",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "upper care vs replace sole, conceptual comparison of actual services",
          "id": "c7r20509",
          "action": "wiping a retained upper above a clean replacement sole"
        },
        {
          "text": "梅基克在二〇二三年拿出一雙換過底的鞋；新底上面，留下來的是什麼模樣？",
          "sources": [
            "TEACH_T"
          ],
          "locator": "recently resoled demonstration p14",
          "id": "c7r20510",
          "action": "holding a repaired boot at an unmarked presentation table"
        },
        {
          "text": "她指著新的外底，讓聽眾看擦亮、清理過的鞋面。",
          "sources": [
            "TEACH_T"
          ],
          "locator": "recently resoled example p14",
          "id": "c7r20511",
          "action": "pointing to the fresh sole below a polished worn upper"
        },
        {
          "text": "她還說，那雙鞋去過當年的格拉斯頓伯里音樂節，鞋面是使用過後再整理的。",
          "sources": [
            "TEACH_T"
          ],
          "locator": "this year's Glastonbury example p14",
          "id": "c7r20512",
          "action": "examining a muddy boot beside a clean cloth at a simple table"
        },
        {
          "text": "修復的工作因此落在兩邊：腳下要換新，還能用的皮則由人清理、修補。",
          "sources": [
            "TEACH_T",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "new outsole, upper polished clean repaired if needed; 24–28s",
          "id": "c7r20513",
          "action": "holding a cleaned upper next to a fresh outsole"
        },
        {
          "text": "維修方說，修理會盡可能使用原廠部件；其他替代材料，也要經品牌認可。",
          "sources": [
            "T5_repairs"
          ],
          "locator": "original components where possible; alternatives authorised",
          "id": "c7r20514",
          "action": "examining a plain replacement component at a repair bench"
        },
        {
          "text": "要重做這道接合，維修方得備好哪些東西？",
          "sources": [
            "AR26",
            "T5_repairs"
          ],
          "locator": "printed p63 dedicated machinery and expertise; same machines methods materials",
          "id": "c7r20515",
          "action": "studying a guarded joining machine beside a boot"
        },
        {
          "text": "年報說，修這種沿條與熱封的構造，需要專門的機器和技術。",
          "sources": [
            "AR26"
          ],
          "locator": "printed p63 repair bespoke machinery and skills",
          "id": "c7r20516",
          "action": "placing an inverted boot next to a heavy stitching tool"
        },
        {
          "text": "授權維修方把自己的做法寫成相同的機器、相同的方法、相同的材料，接回原來的構造。",
          "sources": [
            "T5_repairs",
            "T3_plc_product"
          ],
          "locator": "Same machines. Same methods. Same materials.; attributed partner statement, not independent equipment audit",
          "id": "c7r20517",
          "action": "arranging a flexible band and fresh sole at an assembly bench"
        },
        {
          "text": "維修方把最後收尾稱為手工完成；你看師傅的手，接著又移到鞋的哪裡？",
          "sources": [
            "T5_repairs"
          ],
          "locator": "authorised partner; all repairs hand finished",
          "id": "c7r20518",
          "action": "hand-finishing a lace-up boot on a plain worktable"
        },
        {
          "text": "示範裡，人的手接著轉向鞋帶孔，把黑色鞋帶一段一段重新穿回。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "26–28s",
          "id": "c7r20519",
          "action": "threading a dark lace through the eyelets of a finished boot"
        },
        {
          "text": "繩子穿過金屬孔，再跨到另一邊，剛才為了施工打開的鞋口，重新收回能穿的樣子。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "26–28s",
          "id": "c7r20520",
          "action": "pulling a lace across two plain metal eyelets"
        },
        {
          "text": "鞋頭和靴筒整理好，師傅把一雙靴子擺回工作檯，旁邊換成了紙箱。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "28–29s",
          "id": "c7r20521",
          "action": "setting a restored pair beside an open unmarked shoebox"
        },
        {
          "text": "這雙鞋怎麼離開工作檯，重新回到送修的人手裡？",
          "sources": [
            "R2_HOW",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "returned to you; 29–34s",
          "id": "c7r20522",
          "action": "lowering a finished pair toward a waiting plain box"
        }
      ]
    },
    {
      "title": "紙箱把這一雙送回去",
      "rows": [
        {
          "text": "師傅把靴子收進紙箱，再把箱蓋折好；拆修的示範，最後停在一個能寄走的包裹。",
          "sources": [
            "R2_REPAIR_VIDEO"
          ],
          "locator": "29–34s",
          "id": "c7r20601",
          "action": "folding the lid of a plain shoebox around a restored pair"
        },
        {
          "text": "而那位在七月留下評論的送修者，也等到了修理完成的通知。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "few days after receipt, completion notification",
          "id": "c7r20602",
          "action": "looking at a blank completion message beside an empty shoe shelf"
        },
        {
          "text": "對方說，維修方收到鞋後幾天，又傳來消息：鞋已修好，正在回程。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "completion and return update",
          "id": "c7r20603",
          "action": "reading a blank return notification at a simple table"
        },
        {
          "text": "星期四裝進盒子的那一雙，經過取件、收鞋和修理，重新離開了維修方。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "sequence Thursday packing, next-day collection, receipt and completion",
          "id": "c7r20604",
          "action": "carrying a closed unmarked shoe parcel away from a repair bench"
        },
        {
          "text": "這位送修者寫，從皇家郵政取走包裹起算，一個星期後，快遞把鞋送了回來。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "one week after Royal Mail collection delivered by UPS; individual account",
          "id": "c7r20605",
          "action": "receiving a plain parcel at a simple doorway"
        },
        {
          "id": "c7r20622",
          "text": "打開包裹，除了修好的鞋，你還會看見什麼？",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "personal account new pair of laces; opening preview callback",
          "action": "lifting the lid of a plain shoe parcel beside a worn upper"
        },
        {
          "text": "盒子一打開，對方先看接合處，覺得接得很好，外底也換好了。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "personal assessment welding great, sole perfect",
          "id": "c7r20606",
          "action": "opening a box to inspect fresh sole edges"
        },
        {
          "text": "接著還發現，裡面多了一組全新的鞋帶。這是評論裡特別高興的一件事。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "even better new pair laces; opening second preview payoff",
          "id": "c7r20607",
          "action": "lifting a new pair of plain laces from a shoebox"
        },
        {
          "text": "我喜歡這個細節：主人送走的是一雙用過的鞋，回來後連重新綁鞋帶，都有了新東西。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "editorial reaction to stated new laces; not a guarantee",
          "id": "c7r20608",
          "action": "holding fresh laces beside a familiar worn boot"
        },
        {
          "text": "對方說，這次對修理和回程速度都很滿意，將來還願意再用這項服務。",
          "sources": [
            "R2_CUSTOMER_6870"
          ],
          "locator": "personal satisfaction and would use again; no summer-workload speculation",
          "id": "c7r20609",
          "action": "placing a restored pair on a shoe shelf"
        },
        {
          "text": "另一位送修者在二〇二五年一月寫下，腳穿回去時，最滿意的是什麼？",
          "sources": [
            "R2_CUSTOMER_677e"
          ],
          "locator": "review published 2025-01-08",
          "id": "c7r20610",
          "action": "writing a blank comment beside a pair of repaired boots"
        },
        {
          "text": "那則評論寫，新底、沿條和縫線看起來很好，像有了一雙新靴，卻不用重新忍受磨合。",
          "sources": [
            "R2_CUSTOMER_677e"
          ],
          "locator": "personal analogy no agony of breaking in; not measured comfort or general promise",
          "id": "c7r20611",
          "action": "sliding a foot into a repaired boot with a creased upper"
        },
        {
          "text": "你會在這種話裡，聽出留下上半部的意思：穿著者想接著用的，是已經跟自己走過路的那一雙。",
          "sources": [
            "R2_CUSTOMER_677e",
            "TEACH_T"
          ],
          "locator": "editorial interpretation of attributed views",
          "id": "c7r20612",
          "action": "standing beside a familiar pair with fresh sole edges"
        },
        {
          "text": "現在送修，網站預估要等多久？目前寫的是，周轉最長約三週。",
          "sources": [
            "R2_HOW"
          ],
          "locator": "expected turnaround up to 3 weeks; current service, not historical review deadline",
          "id": "c7r20613",
          "action": "waiting beside a closed parcel and a plain unmarked calendar"
        },
        {
          "text": "這項現行授權服務接受英國客戶，寄送也接上英國郵政，可以由包裹進出維修方。",
          "sources": [
            "T6_repairs_faq",
            "R2_HOW"
          ],
          "locator": "UK-only service and Royal Mail",
          "id": "c7r20614",
          "action": "placing a shoe parcel on an unmarked postal counter"
        },
        {
          "text": "鞋回來以後，維修方還提醒，先清掉泥土，再按鞋面材料選保養品，定期重新照料。",
          "sources": [
            "R2_CARE"
          ],
          "locator": "Remove dirt; choose right care products; reapply regularly",
          "id": "c7r20615",
          "action": "wiping dirt from a worn boot with a plain cloth"
        },
        {
          "text": "原廠在年報裡說，替舊鞋延長使用時間，也有助於加強顧客對品牌的忠誠。",
          "sources": [
            "AR26"
          ],
          "locator": "printed p63 extending life helps strengthen loyalty, issuer attribution",
          "id": "c7r20616",
          "action": "holding a repaired boot while considering its retained upper"
        },
        {
          "text": "這類修復在英國做了多少？二〇二六年報列的，是一個財年四千兩百八十七雙。",
          "sources": [
            "AR26"
          ],
          "locator": "FY26 4287 UK pairs",
          "id": "c7r20617",
          "action": "placing one restored pair on a workshop shelf"
        },
        {
          "text": "這些送修紀錄裡，維修方重新接回部件，主人重新收到的，則是能繼續穿的鞋。",
          "sources": [
            "T7_repairs_resole",
            "R2_CUSTOMER_6870",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "editorial closing linkage, no universal successful-outcome assertion",
          "id": "c7r20618",
          "action": "handing a closed shoe box across a plain counter"
        },
        {
          "text": "回到開場想留下的上半部：新外底接上去，縫線重新車過，穿慣的鞋面又能跟著走。",
          "sources": [
            "T7_repairs_resole",
            "R2_CUSTOMER_6870",
            "R2_REPAIR_VIDEO"
          ],
          "locator": "specific narrative callback and attributed example outcome",
          "id": "c7r20619",
          "action": "lifting a familiar boot with a fresh sole and new laces"
        },
        {
          "text": "如果是你，會把一雙穿出折痕的鞋留下來換底，還是重新穿一雙新鞋？留言告訴我。",
          "sources": [],
          "locator": "",
          "id": "c7r20620",
          "action": "holding a worn upper beside a new plain shoe"
        },
        {
          "text": "訂閱品牌故事，我們繼續看熟悉的日用品，是怎麼被人做出、用過，再留在生活裡。",
          "sources": [],
          "locator": "",
          "id": "c7r20621",
          "action": "looking toward the viewer beside a finished boot on a bench"
        }
      ]
    }
  ],
  "loops": [
    {
      "setup": "c7r20106",
      "payoff": "c7r20304",
      "what": "主問題：三個被拆除的部件得到明確名稱"
    },
    {
      "setup": "c7r20104",
      "payoff": "c7r20408",
      "what": "開場熱接預告：新底怎麼接到沿條"
    },
    {
      "setup": "c7r20104",
      "payoff": "c7r20607",
      "what": "開場回程預告：包裹裡新增的鞋帶"
    },
    {
      "setup": "c7r20203",
      "payoff": "c7r20204",
      "what": "沿條位置：鞋面下緣可見的帶子與縫線"
    },
    {
      "setup": "c7r20230",
      "payoff": "c7r20231",
      "what": "寄出後的第一個新結果：維修方收到鞋的通知"
    },
    {
      "setup": "c7r20233",
      "payoff": "c7r20303",
      "what": "動刀後的新狀態：露出靴底內層"
    },
    {
      "setup": "c7r20310",
      "payoff": "c7r20311",
      "what": "針先接的是鞋面與沿條，而不是外底"
    },
    {
      "setup": "c7r20316",
      "payoff": "c7r20317",
      "what": "可見選擇：新線能選黑色"
    },
    {
      "setup": "c7r20322",
      "payoff": "c7r20408",
      "what": "新外底經熱刀與滾輪接上，對應章尾的具體動作"
    },
    {
      "setup": "c7r20413",
      "payoff": "c7r20414",
      "what": "熱接後的新結果：冷卻成一件PVC"
    },
    {
      "setup": "c7r20417",
      "payoff": "c7r20502",
      "what": "接底後的新動作：轉動工具修邊"
    },
    {
      "setup": "c7r20504",
      "payoff": "c7r20506",
      "what": "上半部的新結果：布擦拭後呈現光澤"
    },
    {
      "setup": "c7r20522",
      "payoff": "c7r20601",
      "what": "工作檯的出口：完整一雙鞋裝箱"
    },
    {
      "setup": "c7r20234",
      "payoff": "c7r20210",
      "what": "現行網站的成對修理標價，與2025自述當時費用分開"
    },
    {
      "setup": "c7r20406",
      "payoff": "c7r20407",
      "what": "接底工序要多熱，原廠給出的650°C操作數字"
    },
    {
      "setup": "c7r20622",
      "payoff": "c7r20607",
      "what": "回程除了修好的鞋，還有全新的鞋帶"
    }
  ],
  "hooks": [
    {
      "id": "c7r20101",
      "kind": "利害",
      "substance": "四年使用、底近磨穿而鞋面仍好，送修者的選擇"
    },
    {
      "id": "c7r20104",
      "kind": "預告",
      "substance": "拆開範圍及回程多出的東西，兩個結果先收住"
    },
    {
      "id": "c7r20106",
      "kind": "主問題",
      "substance": "三個接合部件將如何拆換"
    },
    {
      "id": "c7r20203",
      "kind": "具體問題",
      "substance": "沿條在鞋上哪裡"
    },
    {
      "id": "c7r20234",
      "kind": "具體問題",
      "substance": "委託前先問目前頁面的成對修理費用"
    },
    {
      "id": "c7r20210",
      "kind": "數字",
      "substance": "現行成對服務的標價，與上半部另修的報價範圍"
    },
    {
      "id": "c7r20213",
      "kind": "人物決定",
      "substance": "送修者比較修理與另買二手，決定把舊鞋送出"
    },
    {
      "id": "c7r20216",
      "kind": "人物請求",
      "substance": "主管轉述20年舊靴的同一種修復需求"
    },
    {
      "id": "c7r20218",
      "kind": "具體選擇",
      "substance": "後跟內裡能另修或換新皮，外皮可分開處理"
    },
    {
      "id": "c7r20224",
      "kind": "委託",
      "substance": "把鞋況及想修的部件交給維修方"
    },
    {
      "id": "c7r20226",
      "kind": "動作",
      "substance": "這位送修者把舊鞋盒交給郵差"
    },
    {
      "id": "c7r20230",
      "kind": "問題",
      "substance": "收到靴子後的第一封通知"
    },
    {
      "id": "c7r20233",
      "kind": "章尾",
      "substance": "刀將先拆走什麼"
    },
    {
      "id": "c7r20304",
      "kind": "結果",
      "substance": "三個部件被拆除的可見範圍"
    },
    {
      "id": "c7r20310",
      "kind": "問題",
      "substance": "先車沿條，外底還不在針下"
    },
    {
      "id": "c7r20316",
      "kind": "選擇",
      "substance": "拆掉舊線後能改線色"
    },
    {
      "id": "c7r20322",
      "kind": "章尾",
      "substance": "新底如何接回"
    },
    {
      "id": "c7r20407",
      "kind": "數字",
      "substance": "原廠現行接底工序的熱接溫度"
    },
    {
      "id": "c7r20413",
      "kind": "問題",
      "substance": "冷卻後才形成一件PVC"
    },
    {
      "id": "c7r20417",
      "kind": "章尾",
      "substance": "接好後還需修邊"
    },
    {
      "id": "c7r20504",
      "kind": "問題",
      "substance": "舊鞋面如何清潔與整理"
    },
    {
      "id": "c7r20510",
      "kind": "具體結果",
      "substance": "另一雙換底實物被展示，新外底與清理過的鞋面同在"
    },
    {
      "id": "c7r20515",
      "kind": "問題",
      "substance": "專門機器、技術與原廠或認可替代部件"
    },
    {
      "id": "c7r20522",
      "kind": "章尾",
      "substance": "裝箱後回到送修者手中"
    },
    {
      "id": "c7r20605",
      "kind": "人物結果",
      "substance": "送修者自述一週後收到修好的鞋"
    },
    {
      "id": "c7r20622",
      "kind": "回程問題",
      "substance": "開盒前回呼開場收住的新增物"
    },
    {
      "id": "c7r20607",
      "kind": "揭曉",
      "substance": "回程多出的全新鞋帶，回收開場第二個預告"
    },
    {
      "id": "c7r20611",
      "kind": "人物感受",
      "substance": "另一位送修者把留下的穿著感形容出來"
    },
    {
      "id": "c7r20613",
      "kind": "現行服務",
      "substance": "網站目前預估的周轉時間，與具歸屬的單次回程分開"
    },
    {
      "id": "c7r20617",
      "kind": "數字",
      "substance": "年報列出的FY26英國修復量"
    },
    {
      "id": "c7r20619",
      "kind": "答案",
      "substance": "新接合讓原來的上半部回到穿著者腳下"
    }
  ],
  "title": "馬汀靴換底，要拆掉哪些東西？｜品牌故事",
  "logline": "跟著一則具歸屬的舊靴送修自述，由鞋盒走到授權示範的拆底、車沿條與熱接，再讓新部件與原來的鞋面一起回到穿著者手裡。",
  "brief": "# C07 馬汀靴 r2｜一雙舊靴拆開再接回\n\n狀態：作者重編稿，HOLD，待新的獨立來源與書面配鏡QA及兩位全新隔離讀者。原R1及其收據保留，沒有新owner批准。\n\n## 問題\n\n一雙有沿條的馬汀靴換底，要拆掉哪些部件，又怎麼讓原來的鞋面繼續穿？\n\n## 一句答案\n\n授權換底加換沿條服務拆走舊外底、沿條和縫線；原廠現行構造先將新沿條縫到鞋面，再把它與新外底熱接，修邊與整理後交回穿著者。\n\n## 站主觀點\n\n我想看的是穿著者交出一雙用過的鞋以後，人如何把仍想留下的部分接回生活。問題由舊鞋盒走到刀口、機針、熱接工具，再走回包裹；每一個提問都接著一個可指認的部件、動作或結果。保留鞋面與更換底下部件是能看見的選擇，影片讓觀眾知道自己說的「換底」實際包含什麼。\n\n## 本次建議\n\n### 選項 A：鞋盒進去，這一雙回來\n\n一位2025年7月公開評論中的送修者自述四年舊靴：底近磨穿、鞋面仍好，選過配色後裝進舊鞋盒，收到收件與完工通知，回程發現多了全新鞋帶。這條具歸屬的前後線索帶動敘事；中間由授權維修方公開示範與原廠現行工法，提供拆底、車沿條、熱接、修邊和整理的可見動作。\n\n公共評論是穿著者自述，平台標記not-verified，沒有交易或成品獨立驗證。示範影片是另一段由維修方發布的工序展示，不能宣稱拍到評論者的實鞋；主管的20年舊靴與音樂節案例也各自保留歸屬。這些限制綁在claims和作者紀錄，不用保單否定句填旁白。\n\n## 六章事件\n\n1. 四年舊靴進鞋盒，開場六句只留拆開範圍與回程新增物兩個未揭結果。\n2. 送修者選修理與配色，鞋邊構造、部件範圍與收件通知把委託送到維修檯。\n3. 師傅拆掉三個舊部件，把新沿條車上留下的鞋面。\n4. 熱刀、滾輪與冷卻把新外底接回，說清楚線縫與熱接各在什麼位置。\n5. 新底修邊，舊鞋面清潔整理，鞋帶重新穿回。\n6. 包裹回到穿著者，新鞋帶回收開場預告；具歸屬的穿著感受回收留下上半部的選擇。\n\n## r1 → r2 實質差分\n\nR1以年代、專利、穿法、權利、製造與修復串章；r2改由委託、拆開、接回、整理與回程推進。1945/1947/1959長回顧、專利槽與耐熱材料替代、外觀權利授權、穿著群體與重複造型清單均退出本稿。原R1三個無明確可感回收的抽象why/同一種鞋問題，被具體的拆除範圍、針先縫誰、熱接後等什麼、鞋面怎麼整理及回程新增物取代。\n\n沿條不是直接縫穿外底的線；原廠現在對多數外底、Original系列與接底工序的範圍照寫。650°C只出現在現行接底熱接操作，不作成鞋耐熱宣稱。沒有1959世界權利結論，也不推導財務動機。\n\n## 長度與節奏\n\n以約3500有效native units作文字規劃尺度，依原件與敘事取捨，實際完整計數見native-initialized-lint.json；未為達整數補材料清單、慢播、停頓或警語。正文12–14分鐘仍待真實Sulafat語音測量，不由紙上units或native估時宣稱達標。每章保留你／我；作者hook計畫使用既有的新數字、人物決定、問題及可見結果，時間間隔只是4.5units/s規劃值，非時間軸。\n\n## 製作規格\n\ncategory story；既有STORY Sulafat voice style保持精確；image-01；look只有cute-mystery。所有圖片是匿名英文概念prompt，不畫品牌、人名、logo、可讀文字或真人，並非客戶或歷史原件重建。每景still配運鏡，native估算不超12秒；插圖規劃占比至少70%，原生收尾卡一張，最多連續三卡。\n\n繁中燒錄字幕與CC；濃縮後5秒正式片頭、敘事後21秒正式v4片尾及bold layout d縮圖仍是待執行規格。沒有製作TTS、SRT、圖片、配樂或成片，也未選擇或修改後台/provider。\n\n## 來源與交接\n\n每句source IDs、來源層級、原始bytes SHA、文字快取SHA、短錨點與影片時間段在claims.json。新原件只存work/c07-audit/r2-source-cache；原研究與舊episode保持。完整canonical context唯讀lint使用c07-submission-root現有初始化字典，只在記憶體替換候選doc/brief/series，結果完整保存，不能當新來源、敘事或owner批准。\n"
}
''')

TOKEN=re.compile(r"[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]")
CJK=re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uac00-\ud7af]")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def shat(s):return hashlib.sha256(s.encode()).hexdigest()
def units(t):return sum(1 if CJK.fullmatch(x) else 2 for x in TOKEN.findall(t))
def norm(t):return re.sub(r"\s+"," ",t).strip()
def bind(p):return {"path":str(p),"bytes":Path(p).stat().st_size,"sha256":sha(p)}
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
receipt=json.loads((R1/"reviews/source-r1-independent.json").read_text())
for name,expected in receipt["input_sha256"].items():
    if sha(R1/name)!=expected:raise ValueError("Frozen R1 changed: "+name)
base=json.loads((R1/"video.json").read_text())
research=json.loads((AUDIT/"claims.json").read_text())
used=list(dict.fromkeys(s for c in DATA["chapters"] for r in c["rows"] for s in r["sources"]))
sources={};texts={}
for s in research["sources"]:
    if s["id"] not in used:continue
    raw=Path(s["raw_path"]);txt=raw.with_suffix(".txt")
    if sha(raw)!=s["sha256"]:raise ValueError("Original raw source changed: "+s["id"])
    if not txt.exists():raise ValueError("Readable original missing: "+str(txt))
    sources[s["id"]]={**s,"raw_binding":bind(raw),"text_cache":bind(txt)}
    texts[s["id"]]=txt.read_text()
titles={"R2_HOW":"How It Works","R2_CHOOSE":"How do I choose the right repair?","R2_CARE":"Caring for your pair","R2_UPPER":"Upper Repair — Welted Footwear","R2_CLEAN":"Cleaning and Conditioning"}
for file in ["fetch-manifest.json","service-fetch-manifest.json"]:
    for s in json.loads((NEW/file).read_text()):
        ident=s["id"]
        if ident not in used:continue
        raw=Path(s["raw_path"]);txt=Path(s["text_path"])
        if sha(raw)!=s["sha256"]:raise ValueError("New raw source changed: "+ident)
        sources[ident]={**s,"title":titles[ident]+" — Dr. Martens Repairs","publication_date":"undated; retrieved 2026-10-25",
          "evidence_level":"authorised_service_partner_current_account",
          "scope_and_limits":"Current partner offering/advice, not proof of this reviewed customer's treatment or a universal outcome.",
          "raw_binding":bind(raw),"text_cache":bind(txt)}
        texts[ident]=txt.read_text()
v=json.loads((NEW/"video-manifest.json").read_text());raw=Path(v["raw_path"])
if sha(raw)!=v["sha256"]:raise ValueError("Demonstration raw changed")
sources["R2_REPAIR_VIDEO"]={**v,"title":"Authorised partner original repair demonstration","url":v["parent_page"],"original_video_url":v["url"],
  "publication_date":"not established; asset URL date not used","evidence_level":"authorised_partner_original_demonstration_video",
  "scope_and_limits":"Separate demonstration, not either public reviewer's pair. No material chemistry, calibration or total labour time inferred from frames.",
  "raw_binding":bind(raw),"duration_seconds":38.144,
  "author_observation":"1 fps across original clip plus six larger detail frames",
  "derived_frame_bindings":[bind(NEW/n) for n in ["repair-frames-01.jpg","repair-frames-02.jpg","repair-detail.jpg"]]}
texts["R2_REPAIR_VIDEO"]=""
rv=json.loads((NEW/"reviews-fetch-manifest.json").read_text());raw=Path(rv["raw_path"])
if sha(raw)!=rv["sha256"]:raise ValueError("Public source page changed")
rd=json.loads((NEW/"R2_CUSTOMER_REVIEWS.next.json").read_text())
reviews={r["id"]:r for r in rd["props"]["pageProps"]["reviews"]}
for ident,rid,title in [
 ("R2_CUSTOMER_6870","6870ffa65d1e329686a3886f","Like new! — public repair self-report"),
 ("R2_CUSTOMER_677e","677eccb811974350caefee64","Brilliant service & quality of repair — public reaction")]:
    r=reviews[rid];texts[ident]=r["text"]
    sources[ident]={"id":ident,"title":title,"url":"https://uk.trustpilot.com/reviews/"+rid,"source_review_id":rid,
      "publication_date":r["dates"]["publishedDate"],"reported_experience_date":r["dates"]["experiencedDate"],
      "evidence_level":"attributed_public_first_person_account","raw_path":str(raw),"raw_binding":bind(raw),
      "raw_page_url":rv["url"],"retrieved_at":rv["retrieved_at_utc"],"extracted_source":bind(NEW/"R2_CUSTOMER_REVIEWS.next.json"),
      "review_text_sha256":shat(r["text"]),"platform_verification":r["labels"]["verification"],
      "scope_and_limits":"Self-report and subjective view only; platform not-verified. Not independent proof of quality, time, comfort or typical price. No name, gender, model, colour, operator, update channel or identity with the demo inferred.",
      "excluded_claims":"Environmental comparison, summer workload speculation, representative consensus and verified-transaction claims."}
if set(used)!=set(sources):raise ValueError("Inventory mismatch: "+repr(set(used)^set(sources)))
quotes={
"T3_plc_product":["a PVC welt is first stitched to the upper of the boot","650°C","Once cooled"],
"T5_repairs":["Same machines. Same methods. Same materials.","All repairs are hand finished"],
"T6_repairs_faq":["we only offer our repairs to UK customers","Royal Mail can print label with QR code","order confirmation, name, and address"],
"T7_repairs_resole":["old sole, welt, stitching, gone.","fresh welts, new stitching","£79.99"],
"T8_repairs_welted":["a small visible gap","wide profile of the sole"],
"TEACH_T":["old outsoles have worn out after 20 years while the leather upper still looks great","this year's Glastonbury"],
"AR26":["require dedicated machinery and expertise","strengthen consumer loyalty.","4,287"],
"R2_HOW":["Expected turnaround time - up to 3 weeks.","Put your old pair or accessory in a secure parcel"],
"R2_CHOOSE":["If you're still unsure please get in contact with our team of experts."],
"R2_CARE":["Remove any dirt","Choose the right care products","Reapply regularly"],
"R2_UPPER":["repair or replace it with new leather","prevents further wear to the upper"],
"R2_CLEAN":["Cleaning, repainting & polishing","as much as possible"],
"R2_CUSTOMER_6870":["the upper is fine, the sole was almost worn through","a brand new pair of laces"],
"R2_CUSTOMER_677e":["without the agony of breaking them in"]}
anchors={}
for ident in used:
    if ident=="R2_REPAIR_VIDEO":
        anchors[ident+"-r2"]={"source_id":ident,"raw_binding":sources[ident]["raw_binding"],"duration_seconds":38.144,
          "sequence":[
            {"seconds":[0,4],"observation":"Worn dark lace-up pair and creased upper close."},
            {"seconds":[5,7.5],"observation":"Inverted boot, knife near sole edge; exposed underside, nozzle, cloth at supporting hand."},
            {"seconds":[8,12],"observation":"Hands guide and rotate upper at a heavy needle machine, stitching around band."},
            {"seconds":[13,14],"observation":"Pale underside and dark rim held against belt/tool."},
            {"seconds":[15,20],"observation":"Separate sole under upper, joining tool at edge, hands rotate boot; orange glow at narrow edge."},
            {"seconds":[21,23],"observation":"Sole edge moved around rotating finishing tool."},
            {"seconds":[24,28],"observation":"Cloth wipes upper; dark laces threaded; finished pair."},
            {"seconds":[29,34],"observation":"Pair boxed and carton folded closed."}],
          "not_inferred":["Chemical composition from image","Temperature from glow","Engineering need for each operation","Total labour time","Identity with a reviewer's pair"]}
        continue
    t=norm(texts[ident]);out=[]
    for q in quotes[ident]:
        pos=t.find(norm(q))
        if pos<0:raise ValueError("Short original anchor absent: "+ident+" "+q)
        out.append({"short_quote":q,"normalised_text_start":pos,"quote_sha256":shat(q)})
    anchors[ident+"-r2"]={"source_id":ident,"raw_binding":sources[ident]["raw_binding"],
      "text_cache":sources[ident].get("text_cache",sources[ident].get("extracted_source")),
      "text_sha256":shat(texts[ident]),"short_exact_anchors":out}

doc=copy.deepcopy(base);doc["slug"]=SLUG;doc["category"]="story";doc["look"]={"preset":"cute-mystery"}
doc["subtitles"]["burn_in"]=True;doc["loops"]=DATA["loops"];doc["assets"]=[]
scenes=[];lines=[];claims=[];chapters=[]
sizes=["Close-up","Medium shot","Overhead view","Low angle close-up","Wide shot"]
places=["at a simple packing table","at a plain shoe-inspection counter","at a repair workbench","at a guarded footwear assembly station","at a finishing table","at a simple parcel table"]
lights=["soft daylight from the left","a gentle work lamp from the right","even workshop light","mild window light from behind the camera"]
cameras=["push in","pan left","pull back","pan right","tilt down","tilt up","hold"]
for ci,c in enumerate(DATA["chapters"]):
    ids=[]
    for li,r in enumerate(c["rows"]):
        sid="c07r2-"+str(ci+1).zfill(2)+"-"+str(li+1).zfill(2)
        prompt=sizes[(ci+li)%len(sizes)]+" "+places[ci]+", one anonymous adult "+r["action"]+", "+lights[(2*ci+li)%len(lights)]+"."
        line={"id":r["id"],"text":r["text"]}
        if li%2==0 or "？" in r["text"]:line["emotion"]="對一個人自然說書，問句輕微上揚，數字清楚，句尾收乾淨"
        scene={"id":sid,"template":"shot","data":{"prompt":prompt,"visual":"still","camera":cameras[(ci*2+li)%len(cameras)]},"lines":[line]}
        if li==0:scene["chapter"]=c["title"]
        scenes.append(scene);lines.append({"id":r["id"],"text":r["text"]});ids.append(r["id"])
        mode=[]
        if any(x.startswith("R2_CUSTOMER") for x in r["sources"]):mode.append("attributed_customer_self_report_or_commentary; not independently verified")
        if "R2_REPAIR_VIDEO" in r["sources"]:mode.append("separate authorised demonstration observation; not reviewer's documented pair")
        if r["text"].startswith(("我","如果是我","你","既然","今天")):mode.append("viewpoint_or_viewer_hypothesis; no first-hand repair claim")
        if not r["sources"]:mode.append("viewer_or_subscription_invitation; not a factual claim")
        claims.append({"id":r["id"],"scene":sid,"chapter":c["title"],"text":r["text"],"source_ids":r["sources"],
          "evidence":[{"source_id":s,"anchor_id":s+"-r2","locator":r["locator"],"url":sources[s]["url"],
            "raw_sha256":sources[s]["raw_binding"]["sha256"],"evidence_level":sources[s]["evidence_level"]} for s in r["sources"]],
          "narrative_mode":mode or ["source_bound_current_account; review pending"],"status":"PENDING_INDEPENDENT_SOURCE_AND_WRITTEN_VISUAL_REVIEW",
          "written_visual":{"scene":sid,"prompt":prompt,"mode":"anonymous concept, not real customer or historical reconstruction","review_state":"NOT_REVIEWED"}})
    chapters.append({"title":c["title"],"line_ids":ids})
close=scenes[-3:];scenes=scenes[:-3]
outro={"id":"c07r2-outro","template":"outro","data":{"title":"舊鞋面留下，新接合回來","cta":"你會留下穿慣的這一雙嗎？"},"lines":[l for s in close for l in s["lines"]]}
scenes.append(outro)
for r in claims[-3:]:
    r["scene"]=outro["id"];r["written_visual"]={"scene":outro["id"],"template":"outro","data":outro["data"],"mode":"native closing card","review_state":"NOT_REVIEWED"}
doc["scenes"]=scenes
doc["youtube"]={**base["youtube"],"title":DATA["title"],
 "description":"一雙四年舊靴，底近磨穿，鞋面仍好。跟著具歸屬的送修者自述，由舊鞋盒走到收件通知；再用授權維修方另一次公開示範與原廠現行說明，看舊外底、沿條與縫線如何拆換，新底怎麼接上，整理好的鞋如何回到穿著者手裡。圖像為匿名概念插圖，公共評論保留自述歸屬。工序溫度只描述原廠現行熱接操作。\n\n原件來源（查閱2026-10-25）\n"+"\n".join(sources[s]["title"]+"\n"+sources[s]["url"] for s in used),
 "tags":["Dr. Martens","馬汀靴","品牌故事","日用品的意外轉身","工作靴","換底","沿條","鞋底","舊靴維修"],"video_id":None}
doc["thumbnail"]={"template":"thumb","data":{"layout":"d","headline":"換底得拆線？","sub":"留下穿慣的鞋面","brand":"DR. MARTENS","tag":"品牌故事","shot":"c07r2-03-01"}}
series=copy.deepcopy(json.loads((R1/"series.json").read_text()))
series["title"]=DATA["title"];series["logline"]=DATA["logline"];series["image_model"]="image-01";series["look"]={"preset":"cute-mystery"}
ids=[r["id"] for r in lines]
if len(set(ids))!=len(ids):raise ValueError("Duplicate ID")
for l in DATA["loops"]:
    if l["setup"] not in ids or l["payoff"] not in ids or ids.index(l["setup"])>=ids.index(l["payoff"]):raise ValueError("Broken ordered payoff")
claim_doc={"schema_version":1,"episode":"C07 Dr. Martens remake r2","status":"AUTHOR_CANDIDATE_PENDING_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_TWO_READERS",
 "research_original_sha256":{n:sha(OUT/n) for n in ["research-original.md","research-original.claims.json"]},
 "original_inputs":research["original_inputs"],"r1_binding":{n:bind(R1/n) for n in ["video.json","script.md","narration-only.json","claims.json"]},
 "source_inventory":[sources[s] for s in used],"source_anchors":anchors,"narration_claims":claims,
 "public_review_scope":"Attributed self-reports, platform not-verified, no typical outcome inferred.",
 "source_video_scope":"Separate original demonstration, not new media output or either customer's pair.",
 "paid_calls":0,"provider_calls":0,"backend_actions":0,"actual_runtime_verified":False,"source_pass_issued":False,"owner_approval_issued":False}
dump("video.json",doc);dump("series.json",series);dump("claims.json",claim_doc)
dump("narration-only.json",{"slug":SLUG,"scope":"r2 narration only; no verdict or source notes","chapters":chapters,"lines":lines})
(OUT/"brief.md").write_text(DATA["brief"])
script=["# "+DATA["title"],"","r2作者附來源稿；未核准。canonical screenplay仍須根代理另以原生工具產生。",""]
for c in DATA["chapters"]:
    script+=["## "+c["title"],""]
    for r in claims:
        if r["chapter"]==c["title"]:script+=["["+r["id"]+"] "+r["text"],"來源："+(", ".join(r["source_ids"]) or "觀眾問題／訂閱邀請"),""]
(OUT/"script.md").write_text("\n".join(script)+"\n")
md=["# C07 r2｜逐句來源、時間段與書面分鏡索引","","作者映射，全部待新獨立來源／書面配鏡QA及兩位新讀者；不繼承R1判定。","","## 原件來源",""]
for s in used:md.append("- "+s+"：["+sources[s]["title"]+"]("+sources[s]["url"]+")；"+sources[s]["evidence_level"]+"；raw SHA "+sources[s]["raw_binding"]["sha256"]+"。")
md+=["","## 逐句錨點","","| ID | 旁白 | 原件 | 定位 |","| --- | --- | --- | --- |"]
for r in claims:md.append("| "+r["id"]+" | "+r["text"].replace("|","／")+" | "+", ".join(r["source_ids"])+" | "+(r["evidence"][0]["locator"] if r["evidence"] else "觀眾邀請")+" |")
md+=["","完整來源層級、原始bytes、文字快取、短摘句、評論ID與平台驗證狀態、影片時間段及每句prompt在claims.json。評論是具歸屬自述，原片是另一段授權示範，不冒稱同一實鞋。"]
(OUT/"claims.md").write_text("\n".join(md)+"\n")

native_code=r"""
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {loadProject,lintProject} from './tools/video/core/state.mjs';
import {spokenText} from './tools/video/core/schema.mjs';
import {spokenUnits,estimateTimeline,FPS,DEFAULT_CPM} from './tools/video/core/timeline.mjs';
import {STORY_VOICE_STYLE} from './tools/video/automation/register.mjs';
const dir=process.argv[1],root=process.argv[2],slug='story-everyday-dr-martens-c07-remake-20261025';
const sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const val=v=>crypto.createHash('sha256').update(JSON.stringify(v)).digest('hex');
const p=loadProject({root,slug});
const context={root,slug,canonical_file:p.file,canonical_sha256:sha(p.file),initialized_terms:Object.keys(p.lexicon.terms??{}).length,
 lexicon_sha256:val(p.lexicon),shelf_lexicon_sha256:val(p.shelfLexicon),preserved_fields:['lexicon','shelfLexicon','translations','others','pack','file','dir']};
p.doc=JSON.parse(fs.readFileSync(path.join(dir,'video.json'),'utf8'));
p.brief=fs.readFileSync(path.join(dir,'brief.md'),'utf8');
p.series=JSON.parse(fs.readFileSync(path.join(dir,'series.json'),'utf8'));
const result=lintProject(p),d=p.doc,flat=d.scenes.flatMap(s=>s.lines??[]);
const sum=rs=>rs.reduce((n,l)=>n+spokenUnits(spokenText(l)),0),cs=[];
for(const s of d.scenes){if(s.chapter)cs.push({name:s.chapter,lines:[]});cs.at(-1).lines.push(...s.lines??[])}
const total=sum(flat),opening=sum(cs[0].lines),closing=sum(d.scenes.at(-1).lines),t=estimateTimeline(d);
console.log(JSON.stringify({scope:'author read-only native lint in actual initialized canonical context; not verify or independent approval',
 input_sha256:Object.fromEntries(['video.json','script.md','narration-only.json','claims.json','claims.md','brief.md','series.json','build-candidate.py'].map(f=>[f,sha(path.join(dir,f))])),
 context_binding:context,voice_exact_native_story_style:d.voice.style===STORY_VOICE_STYLE,
 native_units:{total,opening,body_after_opening:total-opening,closing_card:closing,body_excluding_opening_and_closing:total-opening-closing,
 chapters:cs.map(c=>({name:c.name,lines:c.lines.length,spoken_units:sum(c.lines)}))},
 native_estimate:{default_cpm:DEFAULT_CPM,minutes:t.total_frames/FPS/60,not_actual_audio:true},
 scene_estimates:t.scenes.map(s=>({id:s.id,seconds:(s.end_frame-s.start_frame)/FPS})),result,
 paid_calls:0,provider_calls:0,backend_actions:0,actual_duration_measured:false}));
"""
run=subprocess.run(["node","--input-type=module","-e",native_code,str(OUT),str(ROOT)],cwd=REPO,capture_output=True,text=True,check=True)
native=json.loads(run.stdout);dump("native-initialized-lint.json",native)
if native["result"]["errors"]:raise ValueError("Native initialized context errors: "+json.dumps(native["result"]["errors"],ensure_ascii=False))
if not native["voice_exact_native_story_style"]:raise ValueError("STORY voice style differs")
old={l["id"]:l["text"] for s in base["scenes"] for l in s.get("lines",[])}
current={r["id"]:r["text"] for r in lines};ends={};acc=0
for r in lines:acc+=units(r["text"]);ends[r["id"]]=acc
hooks=[];prev=0
for h in DATA["hooks"]:
    end=ends[h["id"]]
    if end<prev:raise ValueError("Hook out of narration order")
    hooks.append({**h,"end_spoken_units":end,"gap_units":end-prev,"planned_gap_seconds_at_4_5":round((end-prev)/4.5,2)});prev=end
ci=[]
for c in DATA["chapters"]:
    text="".join(r["text"] for r in c["rows"]);row={"title":c["title"],"you":text.count("你"),"i":text.count("我"),"units":sum(units(r["text"]) for r in c["rows"])}
    if not row["you"] or not row["i"]:raise ValueError("Missing you/I")
    ci.append(row)
shots=sum(units(l["text"]) for s in scenes if s["template"]=="shot" for l in s.get("lines",[]))
total=sum(units(l["text"]) for s in scenes for l in s.get("lines",[]))
notes={"schema_version":1,"revision":"C07 r2","status":"HOLD_PENDING_NEW_INDEPENDENT_SOURCE_WRITTEN_VISUAL_AND_TWO_FRESH_READERS",
 "author":"/root/c03_review_ko_es","role":"narrative_editor_and_author_not_reviewer","created_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "r1_core_bindings":{n:bind(R1/n) for n in ["video.json","script.md","narration-only.json","claims.json","brief.md","series.json","author-notes.json","build-candidate.py"]},
 "r1_feedback_bindings":[bind(R1/"reviews"/n) for n in ["source-r1-independent.json","narrative-r1-a.raw.json","narrative-r1-b.raw.json","narrative-r1.json","narrative-r1-binding.json"]],
 "research_original_sha256":claim_doc["research_original_sha256"],"source_inputs":{s:sources[s]["raw_binding"] for s in used},
 "new_source_manifests":[bind(NEW/n) for n in ["fetch-manifest.json","service-fetch-manifest.json","video-manifest.json","reviews-fetch-manifest.json"]],
 "narrative_delta":{"old_lines":len(old),"new_lines":len(current),"exact_ids_and_text_retained":[i for i in old if current.get(i)==old[i]],
   "retained_ids_with_changed_text":[i for i in old if i in current and current[i]!=old[i]],"retired_line_ids":[i for i in old if i not in current],
   "introduced_line_ids":[i for i in current if i not in old],"old_scenes":len(base["scenes"]),"new_scenes":len(scenes),
   "shared_r1_hold_response":{"chapters_link":"Replace 1945 jump with sender's service choice, receipt notification, knife, new welt, heat join, finish, return.",
     "payoffs":"Concrete new actions/results replace abstract identity and ungrounded why questions.",
     "no_recap":"Remove guarantee denial and repeated outfits;20-year example appears once with attribution.",
     "no_detour":"Retire long patent mechanics/heat-material substitutions, IP and subculture outfit/group branches."},
   "source_advisories":{"650C":"Current joining operation only, no finished-boot heat resistance.","1959":"Entire rights section retired; no global patent ownership conclusion."},
   "case_boundary":"Public self-report supplies before/after; separate video supplies demonstration. No shared filmed pair, model, owner, colour or chemical material inferred.",
   "current_price_boundary":"2026 listing is not claimed as either reviewer's 2025 payment or checkout/stock check.","no_financial_motive_inferred":True},
 "counts":{"narration_lines":len(lines),"scenes":len(scenes),"chapters":len(chapters),"illustration_shots":sum(s["template"]=="shot" for s in scenes),"cards":1,
  "loops":len(DATA["loops"]),"unique_loop_payoffs":len(set(l["payoff"] for l in DATA["loops"]))},
 "native_units":native["native_units"],"length_plan":{"rough_target_units":3500,"actual_total_units":total,"difference_from_rough_total_target":total-3500,
  "actual_tts_body_minutes_target":[12,14],"actual_audio_unmeasured":True,"no_slowing_pauses_or_filler_added":True,
  "basis":"Approximate text target; source-bound journey governs. All actual counts disclosed separately. No length approval issued."},
 "chapter_you_i":ci,"substantive_hook_plan":hooks,"max_planned_hook_gap_seconds_at_4_5":max(h["planned_gap_seconds_at_4_5"] for h in hooks),
 "opening":{"lines":6,"forward_previews":[{"setup":DATA["chapters"][0]["rows"][3]["id"],"topic":"拆開和接回"},{"setup":DATA["chapters"][0]["rows"][3]["id"],"topic":"回程新增物"}],
  "promise_scale":"one pair, three joining components"},
 "loop_plan":DATA["loops"],"visual_plan":{"look":{"preset":"cute-mystery"},"image_model":"image-01","all_shots_still":True,
   "illustrated_spoken_units":shots,"total_spoken_units":total,"planned_illustration_share":round(shots/total,4),"new_media_created":False,
   "prompts":"anonymous English concepts; no names/brands/logos/readable text/added style","thumbnail_layout":"d","actual_timing_verified":False},
 "branding_plan":{"intro_seconds":5,"intro_after_opening":True,"outro_version":"formal v4","outro_seconds":21,"selected_assets":None,"not_runtime_evidence":True},
 "subtitles_plan":{"burn_in_zh_TW":True,"CC_zh_TW":True,"timed_srt_created":False},
 "native_initialized_context_lint":{"path":str(OUT/"native-initialized-lint.json"),"sha256":sha(OUT/"native-initialized-lint.json"),"error_count":len(native["result"]["errors"]),
  "warning_count":len(native["result"]["warnings"]),"not_an_independent_verdict":True},
 "source_pass_issued":False,"written_visual_pass_issued":False,"native_narrative_pass_issued":False,"owner_approval_issued":False,
 "independent_source_and_written_visual_review":"PENDING_NEW_R2","fresh_isolated_readers_required":2,"actual_audio_measured":False,"candidate_media_reviewed":False,
 "translations_written":False,"source_video_observed":True,"verification_pipeline_run":False,"paid_calls":0,"provider_calls":0,"backend_actions":0,"git_actions":0,
 "source_files_sha256":{n:sha(OUT/n) for n in ["video.json","script.md","narration-only.json","claims.json","claims.md","brief.md","series.json","build-candidate.py","native-initialized-lint.json"]}}
dump("author-notes.json",notes)
print(json.dumps({"revision":"C07 r2","counts":notes["counts"],"native_units":native["native_units"],"native_error_count":len(native["result"]["errors"]),
 "native_warning_count":len(native["result"]["warnings"]),"max_planned_hook_gap_seconds_at_4_5":notes["max_planned_hook_gap_seconds_at_4_5"],
 "four_sha256":{n:sha(OUT/n) for n in ["video.json","script.md","narration-only.json","claims.json"]}},ensure_ascii=False))
