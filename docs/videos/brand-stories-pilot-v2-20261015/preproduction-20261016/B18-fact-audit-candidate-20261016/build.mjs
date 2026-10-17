import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const sourceDir = join(here, '..');
const checklistPath = join(sourceDir, 'B18-worker-conversion-plan', 'claim-checklist.json');
const mappingPath = join(sourceDir, 'B18-authored-chapters-candidate', 'mapping.json');
const outputPath = join(here, 'claim-audit.json');
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');

const sources = {
  J: {
    title: 'J-Net21 / 中小企業基盤整備機構，元祿產業報導（2023-11-13）',
    url: 'https://j-net21.smrj.go.jp/special/expo1970/20231113.html',
    locations: {
      J1204: '「ビール工場のベルトコンベアでアイデアひらめく」第1段；網頁 L1204',
      J1205: '同節第2段；網頁 L1205',
      J1212: '「町工場の経営者が協力」第1段；網頁 L1212',
      J1213: '同節第2段；網頁 L1213',
      J1215: '同節第3段；網頁 L1215',
      J1222: '「モノレール駅前に出店」第1段；網頁 L1222',
      J1225: '同節第3段；網頁 L1225',
      J1232: '「市場規模は7500億円に」第1段；網頁 L1232',
      J1234: '同節第2段；網頁 L1234',
      J1235: '同節第3段；網頁 L1235',
      J1242: '「今も変わらぬコンベア機」第1段；網頁 L1242',
    },
  },
  M: {
    title: '日本機械學會，機械遺產第112號（2021）',
    url: 'https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html',
    locations: {
      M14: '頁首認定號及年份；網頁 L14-L16',
      M19: '首店及創辦人／啤酒線靈感；網頁 L18-L19',
      M20: '1985年現用機與另存早期板片；網頁 L20',
    },
  },
  I: {
    title: '公益社團法人發明協會，戰後日本創新100選「回転寿司」',
    url: 'https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii',
    locations: {
      I31: '「イノベーションに至る経緯」第2段；網頁 L31',
      I32: '同節首店段；網頁 L32',
      I34: '同節實用新案登錄段；網頁 L34',
      I36: '同節加盟與品牌段；網頁 L36',
      I38: '同節萬博與240家段；網頁 L38',
      I43: '同節1978／新業者／採購段；網頁 L43',
      I44: '同節1971／1974設備與後期店型段；網頁 L44',
      I49: '同節1980年代後期家庭客段；網頁 L49',
    },
  },
  C: {
    title: '日本法院判決，昭和59年(ワ)5473號等，官方掃描',
    url: 'https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf',
    locations: {
      C469: '判決理由，PDF第9頁（0-based P8），L466-L469：1960申請、1962登錄、579776號',
      C473: '判決理由，PDF第9頁（0-based P8），L470-L474：道頓堀店1962年4月',
      C508: '判決理由，PDF第9頁（0-based P8），L499-L508：早期擴張及萬博出店',
      C548: '判決理由，PDF第10頁（0-based P9），L543-L548：萬博不足以證明商標全國著名',
      C575: '判決理由，PDF第11頁（0-based P10），L574-L578：本件實用新案1972年期滿、此後已有其他經營者',
      C310: '被告答辯，PDF第6頁（0-based P5），L306-L315：1972-07-24及另一權利851953；僅屬答辯，非獨立判決認定',
    },
  },
  S: {
    title: '石野集團／北日本カコー官方沿革',
    url: 'https://www.ishino-group.com/history/',
    locations: {
      S54: '1958年元祿首店每盤50日圓；網頁 L50-L57',
      S72: '1970-1974年設備沿革；網頁 L58-L86',
      S134: '1984年郊區家庭型店記載；網頁 L130-L137',
      S173: '1991年《廣辭苑》第四版記載；網頁 L165-L173',
    },
  },
  K: {
    title: 'Kindai Picks，白石博志第一人稱訪談（2023-03-23）',
    url: 'https://kindaipicks.com/article/002589',
    locations: {
      K153: '訪談照片說明 L152-L153：給茶裝置1973年開發的另一日期',
      K157: '訪談 L155-L157、L216-L218：博志稱1970年曾在海外讀到萬博新聞',
      K182: '訪談 L180-L182：博志稱1978年「特許」到期；未提供權利號',
      K270: '訪談 L264-L270：博志稱道頓堀店1960年開幕',
    },
  },
};

// One independently read source location per planning claim, plus exceptions.
// Statuses are editorial evidence only: they never mutate worker UNCHECKED verdicts.
const decisionsText = `
H01-1|SUPPORTED|J1205|1948、吹田、啤酒工廠均有記載；廠牌仍不明。
H01-2|SUPPORTED|J1204,J1205|白石身份與工廠參訪相合。
H01-3|SUPPORTED|J1205|手遞壽司耗時是原文的經營瓶頸。
H02-1|SUPPORTED|J1215,M19|1958年4月首店另由機械學會佐證。
H02-2|SUPPORTED|J1212|屬反覆開發難題；不可畫成可查證的一次事故。
H02-3|SUPPORTED|J1222,I38,C508|1970萬博出店；法院亦載實際出店。
H02-4|HOLD_SOURCE_CONFLICT|I43,J1234,K182,C469,C575|發明協會、J-Net21及博志回憶說1978；法院認定同名基本實用新案579776於1972期滿，不能把1978當確定日期。
O01-1|SUPPORTED|J1204|1947愛媛到布施先開料理店，非1958迴轉首店。
O01-2|SUPPORTED|J1204|工廠青年與學生為立食壽司客群。
O01-3|SUPPORTED|J1204,I31|早期立食店四貫20日圓，與首店50日圓分開。
O02-1|SUPPORTED|J1204|節慶料理是報導中的時代背景。
O02-2|SUPPORTED|J1204|明示價格有記載。
O02-3|SUPPORTED|J1204|比其他店便宜約三成有記載。
O02-4|SUPPORTED|J1204|原報導描述生意興旺。
O03-1|SUPPORTED|I31|發明協會記載訂單超出師傅握製能力。
O03-2|SUPPORTED|J1205|年輕師傅因忙碌很快離職。
O04-1|SUPPORTED|J1205,I31|工廠線與將輸送方式搬到壽司店的想法有記載。
O04-2|SOURCE_POINTER_FIX|J1205,M19|循環吧台由J-Net21／機械學會支持；目前綁source=2的發明協會該段只說送盤，應補可讀來源指向。
I01-1|SUPPORTED|J1212|轉角擁塞掉盤是原文的開發難題；不要當單次現場紀錄。
I01-2|SUPPORTED|J1212,I31|附近工廠經營者／鐵工所合作有記載。
I02-1|ATTRIBUTION_REQUIRED|J1212|撲克牌說法只可明指J-Net21版本。
I02-2|ATTRIBUTION_REQUIRED|I31|名片說法只可明指發明協會版本；兩說不可合併為同一現場。
I03-1|SUPPORTED|J1212,I31|扇形板片可通過轉角；源版本描述角度不同但結果相容。
I03-2|TRANSLATION_NOTE|J1212,M20|來源稱ウロコ／うろこ；魚鱗板是中文解說名，正式卡片宜保留原日文。
I04-1|SUPPORTED|J1212,I31|約十年是機構常見記述，不寫精確開發年數。
I04-2|SUPPORTED|J1213|1957試作機及原日文機名見J-Net21。
I04-3|SUPPORTED|J1213|材料防鏽考量有記載。
I04-4|ATTRIBUTION_REQUIRED|J1213|材料費預付為兒子博志追述。
I04-5|ATTRIBUTION_REQUIRED|J1213|工廠願合作的原因是博志推測，旁白不可升格為確定動機。
E01-1|SUPPORTED|J1215,M19|1958年4月布施首店，機械學會支持。
E01-2|SUPPORTED|I32|約20坪且只有吧台座位。
E02-1|SUPPORTED|I32,S54|迴轉首店四貫50日圓；早期立食20日圓另有來源。
E02-2|SUPPORTED|J1215|店外可見輸送帶轉動。
E03-1|HOLD_SOURCE_CONFLICT|J1215,K270,C473|J-Net21和博志第一人稱訪談說1960年道頓堀第二店；法院認定原告道頓堀店1962年4月。未釐清店名／法人是否指不同店前不可確定旁白。
E03-2|SUPPORTED|I34,C469|1962年白石名義的實用新案，法院並確認579776號；J-Net21稱特許屬分類衝突。
E03-3|TRANSLATION_NOTE|I34,C469|正式日文權利名為コンベヤ附調理食台；中文譯名只作說明，不冒充登錄原名。
E04-1|SUPPORTED|J1232|東京大阪聘律師與弁理士警告類似店，J-Net21有記載。
E04-2|ATTRIBUTION_REQUIRED|I36,C575|發明協會說一度幾乎等於元祿品牌；法院亦認定1972後其他業者已入場，須限定時期。
E05-1|SUPPORTED|J1222|地方商工會議所徵求東大阪參展業者，白石接受。
E05-2|SUPPORTED|J1222|場內單軌列車西口站前。
E05-3|SUPPORTED|J1222|300日圓握壽司套組置壽司桶並上輸送帶；非首店單盤價。
E05-4|SOURCE_VARIANT|J1222,K157|J-Net21記博志暑假赴萬博幫忙；Kindai訪談中博志說1970年身在海外、靠報紙得知萬博盛況。可能期間不同，但現有來源未排清，避免當確定且連續的現場回憶。
T01-1|SUPPORTED|I38|萬博出店受表彰；法院證明出店但未證表彰。
T01-2|ATTRIBUTION_REQUIRED|I38,C548|發明協會稱全國認識吃法；法院只否定由萬博單獨證明商標法律上全國著名，兩種命題不同，旁白維持明確歸屬。
T01-3|SUPPORTED|J1225|J-Net21報導外國訪客；不是精確人數。
T01-4|SOURCE_VARIANT|I38,J1232|發明協會約240店，J-Net21報導高峰含直營約250店；本稿明示發明協會口徑。
T01a-1|SOURCE_VARIANT|I44,S72,K153|發明協會說1971供應元祿自動給茶；石野官方沿革記1970開發、1971賣附給茶裝置輸送機，Kindai照片說明稱1973年開發，應區分裝置／整機／安裝年份。
T01a-2|SUPPORTED|I44,S72|發明協會及石野官網均記1974整合設備。
T02-1|HOLD_SOURCE_CONFLICT|I43,J1234,K182,C469,C575|法院判決理由認定同名1962基本實用新案1972年期滿；1978的回顧說法不能確定指此權利。
T02-2|HOLD_CAUSAL_CHAIN|I43,C575|發明協會寫1978後大批進場；法院認定1972基本權利屆滿後已有多家獨立業者，不能呈現1978才打開市場。
T02-3|HOLD_CAUSAL_CHAIN|J1234,C575|J-Net21寫加盟店獨立掛新招牌；放在1978唯一轉折後會誤導，須另核對年份與法律／加盟關係。
T03-1|SUPPORTED_WITH_CONTEXT|I36,I38,J1232,C548|萬博先於權利爭議且店已擴張；法院不承認僅由萬博可證全國商標著名，避免此推論。
T03-2|SUPPORTED|I44|一些新業者開發從後場出餐的直線輸送帶；不是所有店。
T04-1|SUPPORTED|I43|部分業者改直接向漁民或漁協進貨。
T04-2|SUPPORTED|I44|用盤色／裝飾分不同價位。
T04-3|SUPPORTED|I44,S134|1980年代中期郊區大店；石野官方也列1984郊區家庭店。
T04-4|SUPPORTED|I49,S134|發明協會說80年代後期成家庭用餐地；石野官方記1984已有家庭型郊區店，採漸變敘述。
N01-1|SUPPORTED|J1235,S173|1991《廣辭苑》第四版收入，石野官方沿革亦記。
N01-2|SUPPORTED|M14,M20|2021認定，機器製於1985。
N01-3|SUPPORTED|M20|2021認定時堺東店仍使用該1985機器；不外推今天仍在使用。
N01-4|SUPPORTED|M14|機械遺產第112號。
N01-5|TRANSLATION_NOTE|M20,J1212|機械學會指另由元祿產業保存的早期うろこ／三日月板片；不是1985機上零件。魚鱗板是中文說明。
N02-1|ATTRIBUTION_REQUIRED|J1234|2023年J-Net21轉述富士經濟之2022年7252億日圓數；原調查未取得，需保持轉述。
N02-2|ATTRIBUTION_REQUIRED|J1234|超過7500億為2023年當時預估，非實績或2026現值。
N03-1|ATTRIBUTION_REQUIRED|J1242|超過4000店是2023年J-Net21當時報導，不能當今天店數。
`;

const decisions = new Map();
for (const line of decisionsText.trim().split('\n')) {
  const [shortId, verdict, refText, note] = line.split('|');
  if (!shortId || !verdict || !refText || !note || decisions.has(shortId)) throw Error(`bad audit row: ${line}`);
  const refs = refText.split(',').map((key) => {
    const source = sources[key[0]];
    if (!source?.locations[key]) throw Error(`unknown source key: ${key}`);
    return { key, source_title: source.title, url: source.url, location: source.locations[key] };
  });
  decisions.set(shortId, { audit_verdict: verdict, evidence: refs, note });
}

const checklistBytes = readFileSync(checklistPath);
const mappingBytes = readFileSync(mappingPath);
const checklist = JSON.parse(checklistBytes);
const mapping = JSON.parse(mappingBytes);
const mappedClaims = new Map(mapping.claims.map((row) => [row.planning_id, row]));
const rows = checklist.rows.map((row) => {
  const shortId = row.planning_id.replace(/^B18-PC-/, '');
  const decision = decisions.get(shortId);
  const mapped = mappedClaims.get(row.planning_id);
  if (!decision || !mapped || mapped.native.claim !== row.quote || mapped.native.verdict !== 'UNCHECKED') {
    throw Error(`source mismatch or missing decision for ${row.planning_id}`);
  }
  return {
    planning_id: row.planning_id,
    chapter: row.chapter,
    paragraph_id: row.paragraph_id,
    claim_id: mapped.claim_id,
    scene_id: mapped.native.scene,
    line_ids: mapped.all_line_ids,
    exact_spoken_quote: row.quote,
    existing_source_index: row.source_index_zero_based,
    existing_source_url: row.source_url,
    existing_fact_index: row.fact_index_zero_based,
    worker_verdict_unchanged: row.verdict,
    ...decision,
  };
});
if (rows.length !== 65 || decisions.size !== rows.length || mappedClaims.size !== rows.length) {
  throw Error(`unexpected row count: checklist=${rows.length} decisions=${decisions.size} mapping=${mappedClaims.size}`);
}
const counts = Object.fromEntries([...new Set(rows.map((row) => row.audit_verdict))].sort().map((status) => [status, rows.filter((row) => row.audit_verdict === status).length]));
const result = {
  schema_version: 1,
  status: 'OFFLINE_INDEPENDENT_EDITORIAL_FACT_AUDIT_HOLD',
  as_of: '2026-10-16',
  scope: 'B18 authored 65 claims; not a formal worker verifier, listener, narrative or script-review receipt',
  input_sha256: {
    planning_checklist: sha256(checklistBytes),
    authored_mapping: sha256(mappingBytes),
  },
  counts,
  source_conflict: 'Official court judgment finds basic utility-model 579776 expired in 1972, contrary to J-Net21 and Japan Institute of Invention and Innovation 1978 summaries; another utility model 851953 is mentioned but its expiry was not established.',
  rows,
};
const output = `${JSON.stringify(result, null, 2)}\n`;
if (process.argv.includes('--write')) writeFileSync(outputPath, output, 'utf8');
else if (process.argv.includes('--check')) {
  if (readFileSync(outputPath, 'utf8') !== output) throw Error('claim-audit.json differs from current inputs/decisions');
} else throw Error('pass --write or --check');
console.log(JSON.stringify({ rows: rows.length, counts, output_sha256: sha256(Buffer.from(output)), status: result.status }));
