#!/usr/bin/env node
// Offline proposal only. Never writes the source episode, approvals, or a plan lock.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
const root=process.cwd();
const out=path.resolve(process.argv[2] || 'C:/Users/x8120/mokaair-work/videos/ou-de-jianghu-e001/plan/preflight-20261008-v3');
const sha=x=>createHash('sha256').update(x).digest('hex');
const bound={
 'docs/videos/ou-de-jianghu-e001/video.json':'82d221350032c02b3b2f8943e72e63795be36e221c45067acf5bd9a751d20443',
 'docs/videos/ou-de-jianghu-e001/script.md':'b172896d8a1ba5a3192dbc4101cc89c63c0daa5e95c0968b07f536e2902350a4',
 'docs/videos/ou-de-jianghu-e001/review.md':'0b6bd2408781bc7eea5093049a070d95623daa29bf81e3e736c04e0f2c05dc37',
 'docs/videos/series-plans/ou-de-jianghu/production/ep1/beats.md':'ce238ca2f162726e0c73ad2def7154ce1823b4e9a68944dcb9958e166888bc1f',
};
for(const [f,h] of Object.entries(bound)) if(sha(fs.readFileSync(path.join(root,f)))!==h)throw Error(`Source changed: ${f}. Rebase the proposal before rebuilding.`);
const source=JSON.parse(fs.readFileSync(path.join(root,Object.keys(bound)[0]),'utf8'));
const doc=structuredClone(source), byId=new Map(doc.scenes.map(s=>[s.id,s]));
const edits=[];
function change(id,data,reason,grade='B'){
 const s=byId.get(id); if(!s)throw Error(id);
 edits.push({id,reason,human_grade:grade,before:structuredClone(s.data),patch:data});
 Object.assign(s.data,data);
}
function still(id,prompt,reason,camera='Insert, eye level, slow push in'){
 change(id,{visual:'still',camera,prompt,motion:'Hold the depicted result state without changing hands or prop positions.'},reason,'A');
}
change('a02-s035',{camera:'Full shot, eye level, locked',motion:'The broad monk on screen right walks down the last three stone steps and stops in front of the kneeling woman on screen left. The slim swordsman remains on the upper step behind him.'},'固定同側鏡頭，消除跟拍與三級階同時運動；寂右姬左，殷不跟下。');
change('a02-s036',{
 camera:'Two-shot, high angle, locked',
 prompt:'Jiwen at screen right stands one step from Wushuang kneeling at screen left on the gate plaza. His open right palm is horizontal one centimetre above the solid top ridge of her black-and-silver phoenix crown without touching it yet. Five fingers together point toward screen left. Her silver chains hang clear of the contact point. Her face stays lowered and her two sleeved hands rest on the black document box across her knees. His prayer beads remain three turns around his left forearm. Left morning daylight and a restrained gold glow surround only his right palm. The framing includes his mouth and the complete contact area.',
 motion:'The monk on screen right lowers his open right palm by one centimetre until it rests on the solid top ridge of the kneeling woman\'s crown and stops. Her crown and head do not move.',
 end_frame:{prompt:'The same high-angle two-shot and blocking. The monk on screen right has his open right palm resting lightly on the solid top ridge of the black-and-silver crown of the woman kneeling on screen left. All five fingers remain above the crown with no penetration; silver chains stay clear. The box stays across her knees; left-arm beads remain three turns; morning light stays on the left.'}
},'保留不可省的掌冠接觸，首格1cm間隙、末格接觸；人工C，必在三鏡小樣，不以機器A取代人工判斷。','C');
change('a02-s037',{
 prompt:'Insert of the back of Wushuang\'s neck seen from behind and slightly above. The base of her black-and-silver phoenix crown is at the top edge and its chains are outside the neck area. Two continuous curtains of silver-white hair meet over the middle of her nape and completely hide the crescent birthmark at the first frame. The black collar is below. A restrained gold spill from the palm above and morning daylight from the left remain constant.',
 motion:'One short gust separates the two curtains of silver-white hair toward the sides of the neck and stops with one small crescent birthmark exposed at the centre of the nape.',
 end_frame:{prompt:'The same rear nape insert. Silver-white hair is parted to the two sides; exactly one small crescent birthmark is now visible at the centre of Wushuang\'s nape. The crown base stays at the top and the black collar below; the gold spill and morning light stay unchanged.'}
},'首格藏印→末格露印，接下一鏡落髮；不再從已露胎記重做揭露。');
change('a02-s030',{motion:'A soft golden aura brightens around the already open right palm while the hand stays level at chest height.'},'原ring是氣功光環，不是手指搬動小戒指；縮為單一光效。');
change('a01-s083',{motion:'The kneeling woman on screen left brings her spine upright and angles her face upward. The standing man on screen right stays still, separated from her by one full step.'},'原10C誤判：單人直背沒有碰觸燕；改為可讀的位置用語。');
change('a03-s037',{motion:'The monk on screen right raises his right forearm until two extended fingers are visible at chest height, then stops. The seated listener remains beyond the foreground shoulder without contact.'},'原10C誤判：二指表示兩名盟兵，與沈之間始終隔桌沒有碰觸。');
still('a03-s039','Wide shot from the south end of the council hall. Shen sits west at screen left; Jiwen sits east at screen right with folded arms; the Elder sits north at the back. Tea has just been poured: one filled cup is beside Shen and the small teapot stands upright beside the Elder. His empty right hand is relaxed on the table. Afternoon light comes from the upper left.','原10C：倒茶改為已倒好的結果全景，台詞「喝茶」與招待事實保留。','Wide shot, high angle, slow pull out');
still('a03-s050','Insert from Shen\'s west-seat viewpoint of Wushuang\'s joined hands at brow height. Right hand lies over left and its sleeve has already fallen to the wrist after the preceding bow. Exactly one faint gold slanted-stroke seal is exposed on the back of the right hand. The table edge is below; upper-left afternoon light. The other two men cannot see this side of her hand.','原10C：s049拜禮後直接切已露金印，不要求衣料擦過手背。');
still('a03-s054','Insert of Wushuang\'s right hand now lowered to waist height. Its black sleeve with white frost ferns fully covers the back of the right hand again; the gold mark is hidden. Her left hand rests beside the right sleeve and does not pull it. Afternoon light from upper left; dark council floor below.','補查：露印→沈反應→已遮印，袖子遮蓋發生在剪點，避免手指拉布變形。');
still('a04-s015','Insert of Bao\'s open left palm over the harbor mooring post. Exactly three square-holed copper coins lie flat on one red string with their square holes aligned. The thumb stays outside the coins. Right-side dusk light; patched ochre cuff.','原10C：數完三枚的結果；不新增第四枚，不翻錢。');
change('a04-s053',{prompt:'Shen\'s face and shoulders at screen left facing right toward the Elder across the guest-room board. Pale calm face and narrow grey eyes lowered toward the board; tall white jade crown with one feather and long ink-black hair. His hands and any stones are entirely below the lower frame edge. Warm candlelight from below and cold moonlight on the far shoulder.',motion:'Shen slowly raises his eyes from the board toward the Elder and settles his gaze.'},'原10C：原MCU看不到取子動作；取子留在畫外，臉部一個明確抬眼，s055仍可見已持黑子。');
change('a04-s090',{camera:'Medium close-up, eye level, slow push in',prompt:'The Elder seated at screen right facing left across the guest-room go board. His right forearm is already supported on the table; his right fingers already hold one white stone motionless above the board at the lower edge. His white whisk lies across his knees. Frosted window behind; faint candlelight still present and cold mist at his lips. His posture is calm and there is no wound.',motion:'One slow white breath leaves the Elder\'s lips and fades; his stone-bearing hand remains in the same position.'},'原10C：落點前持子已在首格，保留白子直到尾鏡；不用模型從棋碗夾取。');
still('a05-s032','Two-shot on the cliff corridor from the same mountain-wall side. Shen is on screen left; Bao is on screen right facing him. Bao has already stopped, bent forward and trembling; Shen\'s two open hands already rest on Bao\'s two shoulders to steady him. Neither hand grips his neck. Moonlit columns are on the right and the wall on the left; the open guest-room door is farther down the corridor.','原10C：碰撞接住改為剪入已扶穩狀態，保留求助與身體支持；不生成撞擊。','Two-shot, eye level, slow push in');
change('a05-s072',{prompt:'Bao stands in the guest-room doorway at screen left facing right into the cold moonlit room. He already holds his red string with exactly three copper coins at chest height in his right hand; his left hand stays inside his sleeve. His face is pale and sober. All coins and the hand are within the lower frame edge.',motion:'Bao gives one small firm shake of his head while the three coins stay at chest height.'},'原10C：首格已舉錢，取消再次舉起；誓言由搖頭表演，三枚道具不運算。');
// Additional manual risks missed by keyword grading: redesign with the event visible across the cut.
still('a02-s057','Insert of the black lacquered document box with silver frost-fern inlay already supported from beneath by Shen\'s left hand in one white crane-embroidered sleeve at upper right. Below at left Wushuang\'s knees are empty and both of her hands are withdrawn inside long black sleeves. Gold light from above and mist on flagstones.','補查：交接切到沈已接穩，姬兩手均退出；s058由此持匣抬高。');
change('a02-s040',{motion:'The monk lowers his chin toward the kneeling woman and finishes the threat with his jaw set.'},'補查：接觸已在pilot s036建立；本CU不再要求掌壓冠。');
still('a03-s085','Full shot inside the guest courtyard room. Wushuang stands at screen right beside the low table and lamp, facing left. Her phoenix crown has already been removed and rests upright on the table with its silver chains gathered safely beside it. Her silver-white hair is uncrowned and both hands are lowered within her long black sleeves. Half-open lattice window behind; warm lamp and blue dusk courtyard.','補查：卸冠→桌上冠結果剪點，避免雙手穿鏈；四秒保留安靜獨處節拍。','Full shot, eye level, slow push in');
still('a03-s087','Insert of the back of Wushuang\'s pale right hand beside the oil lamp. One faint gold slanted-stroke seal is visible; black sleeve rests at the wrist. The left hand stays outside frame. Warm lamplight and cold blue shadow.','補查：保留她自行查看金印，取消拇指擦皮膚的小動作。');
still('a04-s005','Full shot from the quay side. The boy is already safely on the ship deck at screen right with both feet planted. Yan stands beside him with his left hand open just behind the boy\'s collar without lifting him; the single sabre stays on Yan\'s right shoulder. Right-side dusk light and grey transport sail.','補查：孩子被抬起改成已救回甲板結果，下一鏡安撫頭部；不得變成新陌生孩子。','Full shot, eye level, slow push in');
change('a04-s006',{prompt:'Yan beside the boy safely standing on the transport ship deck. Yan\'s left hand has already withdrawn from above the boy\'s head and is lowered at his side. The sabre remains on his right shoulder with its single red tassel. Both stand at rest in right-side dusk light.',motion:'Yan gives the boy one short reassuring nod.'},'補查：頭部接觸轉為安撫點頭，台詞與關心保留。');
still('a04-s038','Insert above Bao\'s open left palm at the harbor. One white shell coin already lies at the centre of the palm; Luo\'s slender right hand has withdrawn above the top edge. Exactly one shell coin; no copper coins in this palm. Blue dusk light with a right gold edge.','補查：貝錢交接改已交付結果。');
change('a04-s039',{prompt:'Bao\'s face on the quay at screen left facing right toward Luo above. He looks with delighted recognition at a single white shell coin already held below his chin, clearly away from his closed mouth. Blue dusk light.',motion:'Bao raises his eyebrows once in delighted recognition while keeping the shell coin away from his mouth.'},'補查：咬錢改辨認反應，不生成口腔與小錢接觸，台詞保留。');
change('a04-s043',{prompt:'Rear nape insert of Luo leaning on the ship rail. Low sea-green coral crown at top; ivory collar below. At the first frame long dark blue-black hair meets over the centre of his neck, completely hiding the crescent birthmark. Blue dusk with a last gold edge from screen right.',end_frame:{prompt:'Same rear nape framing matched in scale to Wushuang a02-s037. Dark blue-black hair now parts to both sides, revealing one small crescent birthmark in the centre of Luo\'s nape. Low sea-green crown and ivory collar remain unchanged.'}},'成對伏筆：洛也由藏印開始，與姬同角度比例；不把已露首格再次分髮。');
for(const [id,prompt,reason] of [
 ['a04-s051','Insert of the go board in warm candlelight. One white stone has just been placed on its intended intersection; the Elder\'s right fingertips are already withdrawn at frame right. Existing black and white stones remain unchanged.','白子落點以結果插鏡交代。'],
 ['a04-s062','Insert of the same go board in warm candlelight. One new black stone is now on the formerly empty point; Shen\'s pale fingertips have already withdrawn at frame left. All other stones remain in their established positions.','黑子落點以结果插鏡交代。'],
 ['a04-s071','Insert of the same go board. The Elder\'s new white stone is already placed in the corner; his fingertips have withdrawn at frame right. Warm candlelight and all prior stones remain unchanged.','角落白子結果，不重新畫整局。'],
 ['a04-s079','Insert of the same go board. The challenge white stone is already resting on its intended point and the Elder\'s fingers are off the stone at frame right. Warm candlelight; all previous stones stay fixed.','關鍵一子落定結果與挑戰台詞同剪。'],
 ['a05-s028','Insert of the Elder\'s dark-teal shoulder fabric in cold moonlight. Bao\'s two fingertips already rest at the edge without pressing further. Tiny beads of melted frost are already visible beneath the touch; the shoulder is motionless.','觸肩的冰冷結果，避免指尖融霜同時模擬。'],
 ['a05-s030','Insert of the floor beside the guest-room low table. The black lacquered tea tray is already overturned; exactly one clay teapot and one cup lie on the floor beside a small pool of spilled tea. A patched ochre sleeve exits at left; cold moonlight and no blood.','茶盤翻落以結果與後期撞擊聲交代，不模擬杯壺碰撞和液體。'],
 ['a05-s036','Insert of the Elder\'s cold wrist on the guest-room table. Two pale fingers from Shen\'s right hand already rest on the inside of the wrist; no pulse movement, no wound or blood. Cold moonlight.','探脈切入已觸腕狀態。'],
 ['a05-s037','Insert of the Elder\'s throat. The dark-teal collar is already folded back, revealing smooth intact skin without wound or blood. Shen\'s pale hand rests beside the fabric outside the throat area. Cold moonlight.','翻領改為已露無傷皮膚結果。'],
 ['a05-s041','Close-up of the Elder\'s still face at screen right facing left. Both eyes are now gently closed; white frost on brows and beard; dark-teal Taoist crown and cold moonlight. Shen\'s pale hand has already withdrawn to the left edge below eye level.','闔眼切入完成後，沈台詞照留；死亡不新增痛苦反應。'],
 ['a05-s067','Insert of Jiwen\'s left forearm with exactly three turns of dark prayer beads. One bead is visibly split along one crack while still held on the string; his right fist is already closed around the strand. Cold moonlight; no extra loose beads.','碎珠結果配後期裂聲，不讓模型增殖碎片。'],
 ['a05-s077','Insert at the frosted guest-room window. Shen\'s left palm already contains one half-length frayed bowstring; his right fingertips hold the single nail clear of the wooden bar. The former nail hole is visible; no second string appears. Cold moonlight.','拔釘與接弦改完成結果，下一鏡回憶、回來手中仍一截。'],
 ['a05-s085','Two-shot beside the half-open frosted guest-room window. Jiwen is left and Shen is right; Jiwen\'s right hand already rests around Shen\'s closed left wrist at chest height. One stable hand-to-wrist contact; Shen holds the half-string within his left fist. Both look at each other, cold moonlight between them.','握腕切入已抓穩，不生成接觸過程。'],
])still(id,prompt,'補查：'+reason,/^a05-s041$/.test(id)?'Close-up, eye level, slow push in':id==='a05-s085'?'Two-shot, eye level,slow push in':undefined);
change('a04-s069',{prompt:'Shen\'s face and shoulders at screen left facing right toward the Elder; his folded white fan and the already held black stone are below frame. Warm candlelight from below; white jade crown and black hair unchanged.',motion:'Shen turns his face a few degrees toward the Elder and settles.'},'補查：棋子轉指改畫外，安慰由側轉表演。');
change('a04-s073',{prompt:'Shen\'s face at screen left facing right. The newly placed black stone is below frame on the board; both hands are below the lower edge. Warm candlelight and cold moon rim unchanged.',motion:'Shen lifts his chin a few degrees toward the Elder and stops.'},'補查：落子在畫外已完成，臉CU不承諾看不見的手動作。');
change('a04-s076',{motion:'The Elder inclines his head toward Shen with quiet curiosity; his already held white stone stays supported in his palm.'},'補查：取消掌上滾白子，詢問以頭部表演。');
change('a04-s081',{prompt:'Shen\'s face at screen left facing right in warm candlelight. His hands are already empty below frame; the unplayed black stone is back in its bowl. White jade crown with one feather; long black hair.',motion:'Shen tips his head once toward the Elder with a restrained tired smile.'},'補查：退子已在畫外完成，不在臉CU要求掉子。');
change('a05-s027',{prompt:'Two-shot in the cold guest room. Bao stands left beside the seated Elder right, leaning toward him. Bao\'s right hand is already resting lightly on the Elder\'s dark-teal shoulder, with five fingers separated from the neck. The Elder is motionless with open eyes and one white stone held above the board.',motion:'Bao leans his face a few centimetres closer to the motionless Elder; his right hand stays resting on the shoulder.'},'補查：觸肩在首格固定，只做探看表演；下一插鏡驗冰冷。');
// v3: second manual sweep. Event order, every line, and every editorial duration remain unchanged.
still('a01-s005','Insert of the black lacquered quiver hanging from the black bow at the forge. Exactly three long black arrows and one short black arrow are already fully seated point-first in the quiver. Their dark-red veins are faint; the tongs have already opened above the mouth without touching an arrow. Bow and quiver lean against the forge at frame left under left orange firelight.','v3補查：四箭放入以結果插鏡固定數量，避開四根細長物同時掉落。');
change('a01-s007',{prompt:'Medium close-up from the south side of the forge. Nie stands at screen right with his burned right arm extended left. His fingers already hold one broken half of the dark-red bowstring. The black bow with its attached quiver containing three long arrows and one short arrow has already broken free and floats at screen left in a black wind without any hand touching it. Firelight comes from left; no human shape appears in the wind.',motion:'The black wind carries the already freed bow and its attached quiver together toward screen left and out of frame; Nie\'s right hand stays holding the broken half-string.'},'v3補查：斷弦已在剪點完成，只生成弓囊作為整體被風捲走，接s008半截弦。');
still('a04-s009','Insert of the boy\'s small hand in a worn grey cuff already loosely holding the red sabre tassel. Exactly one small hand and one tassel; the dark blade back is above, Yan\'s torn rust-brown sleeve at left. The tassel does not change length. Warm dusk light from right.','v3補查：孩子碰刀穗切入已輕握結果，前s008已把穗降到可及高度。');
change('a04-s014',{prompt:'Bao sits on the mooring post at the landward quay at screen left. Exactly three square-holed copper coins on one red string lie flat across his open left palm; his right hand rests on his knee and does not manipulate them. Patched ochre clothes and pushed-back straw hat; refugees move to ships at right; gold dusk light from right and cold blue sea.',motion:'Bao dips his head over the three stationary coins while counting aloud, then keeps his head lowered.'},'v3補查：數三錢以凝視和台詞完成，手不逐枚滑錢；接s015同一三錢結果。');
change('a04-s020',{prompt:'Full shot from the quay side. Yan has just reached the transport ship at screen right: both feet are already planted on the deck and knees slightly bent in the completed landing pose. His single sabre stays in his right hand clear of the rail. The quay is at left across a narrow gap of water; right-side gold dusk light and grey transport sail.',motion:'Yan straightens from the completed landing and turns his upper body back toward the quay at screen left.'},'v3補查：不生成越水飛身和手抓欄的組合；剪入已落船、轉回岸邊，下一鏡向包交代。');
still('a05-s012','Insert of Bao\'s open right palm at frame right with patched ochre cuff. The tip of Shen\'s single folded white paper fan already rests at the centre of the palm; one pale right hand and white sleeve support the fan from frame left. No second fan or extra fingers. Cold corridor moonlight. Shen speaks off screen.','v3補查：扇點掌以已觸的結果插鏡與輕敲音效交代，不生成兩人接觸過程。');
change('a05-s040',{prompt:'Two-shot looking down on the guest-room low table. Shen kneels at screen left beside the seated Elder at right. Shen\'s right hand already rests flat on the Elder\'s dark-teal sleeve, away from skin. The Elder\'s eyes remain open and one white stone stays motionless between his right fingers above the board. Spilled tea lies on floor; cold window light.',motion:'Shen lowers his head slightly while giving the instruction toward the doorway without turning his body; both hands remain where they are.'},'v3補查：探查後手已搭袖的首格，只做低頭囑咐，避免跨人體新接觸。');
change('a05-s046',{prompt:'Medium shot from the south side of the cold guest room. Shen kneels left beside the seated Elder right. The white horsetail whisk is already laid straight across the Elder\'s knees. Shen\'s hands are withdrawn to his own lap, clear of the whisk. Go board and fixed white stone remain beside them. Jiwen speaks off screen.',motion:'Shen bows his head toward the Elder while remaining kneeling, his hands still in his own lap.'},'v3補查：整理拂塵改完成後悼念，不要求双手操縱長毛與死者衣層。');
still('a05-s089','Insert of Bao\'s coins in cold guest-room moonlight. Exactly two square-holed copper coins remain on the dangling red string at upper centre; exactly one third coin has already fallen flat on the floorboard below. His trembling fingertips hold only the string. Total coins remain three and no coin is broken.','v3補查：掉一枚改為兩留一落的結果，配銅錢落地聲；不讓孔穿線形變。');
still('a05-s091','Insert of the same unfinished go board in cold moonlight. The final white stone has already fallen into the unfinished corner at frame left. The Elder\'s age-spotted fingers remain at frame right but are now empty and motionless; frost is melting. All other black and white stones retain their established intersections.','v3補查：尾聲白子落角以結果與一聲落子交代；避免落子、彈跳、滾動同時改整盤棋。');
// Physical coverage: preserve shot-specific states. Same lens/angle/move and subject share a station;
// inserts remain individually composed. No strings are renamed merely to disguise a different view.
const spaces={
 forge:{name:'forge',axis:'南侧；爐左人隊右，火光左',place:'the south side of the forge'},
 tower:{name:'mountain/watchtower',axis:'塔南；沈左背面、包右、梯口右；沈不露正面',place:'the south side of the watchtower'},
 gate:{name:'gate plaza',axis:'西側180度半平面；廣場左、階門右，晨光左',place:'the west side of the gate plaza'},
 council:{name:'council hall',axis:'南側；沈西左、寂東右、長老北後',place:'the south half of the council hall'},
 terrace:{name:'stone terrace',axis:'南側；沈左寂右、殷後柱；夕光右',place:'the south side of the stone terrace'},
 court:{name:'guest courtyard',axis:'月洞門左、屋窗右；守衛在外',place:'the guest courtyard and its lamp-lit room'},
 port:{name:'harbor',axis:'岸側；陸左海右；洛船上、包跳板下；夕光右',place:'the shore side of the harbor quay'},
 room:{name:'guest room',axis:'桌南半平面；門左前窗右後；後段沈移窗右',place:'the south half of the guest room'},
 corridor:{name:'cliff corridor',axis:'山壁側；壁左柱右；沈左包右，門右遠端',place:'the mountain-wall side of the cliff corridor'},
};
function location(id){const a=Number(id.slice(1,3)),n=Number(id.slice(-3));if(a===1)return n<=8?'forge':n<=44?'tower':'gate';if(a===2)return 'gate';if(a===3)return n<=65?'council':n<=81?'terrace':'court';if(a===4)return n<=49?'port':'room';return n===78?'forge':n<=14||n>=17&&n<=22||n>=32&&n<=34?'corridor':n===15||n===16?'court':'room';}
function phase(id,k){const a=+id.slice(1,3),n=+id.slice(-3);if(k==='gate')return a===1?'arrival':n<30?'debate':n<44?'palm-wushuang':n<73?'palm-shen':'withdrawn';if(k==='room')return a===4?(n<86?'chess-lit':'elder-alone-frost'):n<35?'discovery':n<42?'examination':n<60?'door-confrontation':n<74?'window-confrontation':'bowstring';if(k==='court')return a===3?(n<85?'crowned':'uncrowned'):'dark-window';if(k==='council')return n<40?'three-seated':n<59?'wushuang-present':'after-departure';if(k==='port')return n<26?'transport':'merchant';return 'main';}
const coverage=[];
for(const s of doc.scenes.filter(s=>s.template==='shot')){
 const d=s.data,k=location(s.id),p=phase(s.id,k),sp=spaces[k];
 const camera=d.camera||'', insert=/insert|overhead|extreme close/i.test(camera),chars=d.characters||[];
 let station=insert?'F-insert':/wide|group|full/i.test(camera)?'A-master':/two-shot/i.test(camera)?'B-pair':/over-the-shoulder/i.test(camera)?'E-shoulder':chars[0]==='shen-guihe'||chars[0]==='ji-wushuang'||chars[0]==='bao-sanqian'?'C-left-or-protagonist':'D-right-or-partner';
 // Repeated face coverage is really framed at one stable station, not a novel camera per line.
 if(!insert && /^(?:Medium close-up|Close-up)/i.test(camera) && chars.length===1){
   const size='Medium close-up';
   const angle=k==='gate'&&chars[0]==='ji-wushuang'?'high angle':k==='gate'&&chars[0]==='ji-wen'?'low angle':k==='tower'&&chars[0]==='yan-hui'?'high angle':k==='port'&&chars[0]==='luo-qingyan'?'low angle':'eye level';
   const move=d.visual==='still'?'slow push in':'locked';
   d.camera=`${size}, ${angle}, ${move}`;
   d.prompt=`${size} of ${chars[0]} in the ${p} blocking from ${sp.place}; head and upper torso stay in the frame with the complete crown. ${d.prompt}`;
 }
 coverage.push({id:s.id,space:k,phase:p,station,axis:sp.axis,camera:d.camera,first_frame:d.prompt,motion:d.motion,end_frame:d.end_frame?.prompt||'終止在motion明列的收勢；角色、道具、光向不跨切重置',visual:d.visual||'clip',source:d.source||null});
}
// Only truly compatible reactions are cut from an earlier master. Different emotion/light/prop states stay separate.
const reuse=[
 {id:'a02-s059',source:'a02-s053',from:0.4,reason:'同一掌冠威脅階段與晨光；用寂聞向前施壓的同一臉部母鏡，取消另加一次爆光。'},
 {id:'a02-s065',source:'a02-s053',from:1.8,reason:'同一金光階段、同側寂聞；手不在臉CU內，不新增再次壓冠。'},
 {id:'a02-s069',source:'a02-s062',from:0.2,reason:'姬仍在沈後面聽；改用克制緊唇反應，刪除原一閃而逝微笑；這是明列的表演選擇。'},
 {id:'a04-s067',source:'a04-s053',from:0.2,reason:'同一燭亮對弈階段、沈左臉右視；手與黑子在畫外，短答配抬眼反應。'},
];
for(const r of reuse){const s=byId.get(r.id),o=byId.get(r.source);change(r.id,{...structuredClone(o.data),source:{shot:r.source,from_s:r.from}},'素材切用提案：'+r.reason);const row=coverage.find(x=>x.id===r.id);Object.assign(row,{camera:s.data.camera,first_frame:s.data.prompt,motion:s.data.motion,visual:'cut',source:s.data.source});}
for(const s of doc.scenes.filter(s=>s.template==='shot')){
 const absent=[...new Set((s.lines||[]).map(l=>l.speaker).filter(x=>x&&x!=='narrator'&&!(s.data.characters||[]).includes(x)))];
 if(absent.length&&!/off screen/i.test(s.data.prompt))s.data.prompt+=` ${absent.join(' and ')} speaks off screen.`;
 const row=coverage.find(x=>x.id===s.id);Object.assign(row,{camera:s.data.camera,first_frame:s.data.prompt,motion:s.data.motion,visual:s.data.source?'cut':s.data.visual||'clip',source:s.data.source||null});
}
const {planEpisode,renderMarkdown,renderCsv}=await import(pathToFileURL(path.join(root,'.agents/skills/animation-preproduction/scripts/shot_plan.mjs')));
const series=JSON.parse(fs.readFileSync(path.join(root,'docs/videos/ou-de-jianghu-e001/series.json'),'utf8'));
const flags={route:'hailuo',plan:'hailuo:max',hailuoModel:'h3',resolution:'2k',handle:0.5,clipTakes:2,expectedTakes:{A:1.2,B:1.5,C:2},pilot:['a02-s035','a02-s036','a02-s037'],series};
const oldPlan=planEpisode(source,flags),plan=planEpisode(doc,flags);
const originalCs=oldPlan.shots.filter(s=>s.visual==='clip'&&s.risk.grade==='C').map(s=>s.id);
const manual=plan.shots.map(s=>{
 const e=edits.filter(x=>x.id===s.id).at(-1);
 let grade=e?.human_grade||s.risk.grade;
 let reason=e?.reason||`未更動原單一動作；機器${s.risk.grade}理由逐鏡保留於shot-plan.json。`;
 if(['a01-s083','a03-s037'].includes(s.id)){grade='B';reason='原10C文字誤判：一人直背／一人抬兩指，沒有碰到另一人；仍須身體與手型QA。';}
 if(s.visual==='cut')grade='A';
 return {id:s.id,original_machine_c:originalCs.includes(s.id),machine_grade:s.risk.grade,human_grade:grade,reason,visual:s.visual,buy_s:s.buy_s,expected_takes:grade==='C'?2:grade==='B'?1.5:1.2};
});
const humanExpected=plan.shots.filter(s=>s.visual==='clip').reduce((sum,s)=>sum+s.cost.one*manual.find(m=>m.id===s.id).expected_takes,0);
const stableLines=JSON.stringify(source.scenes.map(s=>[s.id,s.lines,s.action_seconds]))===JSON.stringify(doc.scenes.map(s=>[s.id,s.lines,s.action_seconds]));
if(!stableLines)throw Error('Dialogue or action duration changed unexpectedly');
fs.mkdirSync(out,{recursive:true});
const json=(file,obj)=>fs.writeFileSync(path.join(out,file),JSON.stringify(obj,null,2)+'\n','utf8');
json('video.json',doc);json('series.json',series);json('proposal-edits.json',edits);json('camera-ledger.json',{spaces,rows:coverage});json('risk-ledger.json',manual);json('shot-plan.json',plan);
fs.writeFileSync(path.join(out,'shot-plan.md'),renderMarkdown(plan,'proposal/video.json'));fs.writeFileSync(path.join(out,'shot-plan.csv'),renderCsv(plan));
for(const name of ['brief.md','dictionary.json']){const f=path.join(root,'docs/videos/ou-de-jianghu-e001',name);if(fs.existsSync(f))fs.copyFileSync(f,path.join(out,name));}
json('proposal-receipt.json',{created_at:new Date().toISOString(),status:'reviewable-proposal-not-approved-not-locked',source_sha256:bound,series_sha256:sha(fs.readFileSync(path.join(root,'docs/videos/ou-de-jianghu-e001/series.json'))),video_sha256:sha(fs.readFileSync(path.join(out,'video.json'))),builder_sha256:sha(fs.readFileSync(new URL(import.meta.url))),dialogue_and_duration_unchanged:stableLines,flags:{...flags,series:undefined},original_counts:oldPlan.counts,counts:plan.counts,original_setups:oldPlan.totals.setups,proposed_setups:plan.totals.setups,original_machine_c:originalCs,manual_c:manual.filter(m=>m.human_grade==='C'),manual_expected_credits:Math.round(humanExpected*100)/100,totals:plan.totals,reuse,source_files_still_match:Object.entries(bound).every(([f,h])=>sha(fs.readFileSync(path.join(root,f)))===h),problems:plan.problems});
console.log(JSON.stringify({out,counts:plan.counts,setups:plan.totals.setups,totals:plan.totals.clip,humanExpected,problems:plan.problems},null,2));
