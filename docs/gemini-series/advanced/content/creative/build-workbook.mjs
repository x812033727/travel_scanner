/** Downloadable teaching template, authored locally; no Google Sheets account operations. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const here = path.dirname(fileURLToPath(import.meta.url));
const source = path.join(here, 'examples/67');
const output = path.join(source, 'outputs/creative-lessons');
const verification = path.join(here, 'verification/workbook');
await fs.mkdir(output, { recursive: true });
await fs.mkdir(verification, { recursive: true });
const data = JSON.parse(await fs.readFile(path.join(source, 'cleaning-result.json'), 'utf8'));
const oracle = JSON.parse(await fs.readFile(path.join(source, 'expected.json'), 'utf8'));
const wb = await Workbook.fromCSV(await fs.readFile(path.join(source, 'sales-dirty.csv'), 'utf8'), { sheetName: 'Raw' });
const raw = wb.worksheets.getItem('Raw');
const report = wb.worksheets.add('Report');
const clean = wb.worksheets.add('Clean');
const excluded = wb.worksheets.add('Excluded');
const font = 'Arial'; // Windows Arial; renderer and Sheets may use a CJK fallback for Chinese glyphs.

function style(sheet, range, header) {
  sheet.showGridLines = false;
  sheet.getRange(range).format.font = { name: font, size: 11, color: '#243449' };
  sheet.getRange(range).format.columnWidthPx = 110;
  sheet.getRange(range).format.rowHeightPx = 27;
  sheet.getRange(header).format = { fill: '#365477', font: { name: font, size: 11, bold: true, color: '#ffffff' }, rowHeightPx: 34 };
}

style(raw, 'A1:I51', 'A1:I1');
raw.getRange('C1:C51').format.columnWidthPx = 130;
raw.getRange('I1:I51').format.columnWidthPx = 390;
raw.freezePanes.freezeRows(1);
raw.tables.add('A1:I51', true, 'RawSales');
// Raw text is intentionally untouched; it contains invalid/ambiguous dates and missing values.
clean.getRange('A1:K1').values = [['來源 ID', 'CSV 列號', '日期', '單號', '商品', '幣別', '數量', '單價', '交易類型', '金額', '備註']];
clean.getRange('A2:K44').values = data.accepted.map(r => [r.source_id, r.source_csv_row, new Date(r.date + 'T00:00:00Z'), r.order_id, r.product, r.currency, r.quantity, Number(r.unit_price), r.kind, null, r.note]);
clean.getRange('J2').formulas = [['=G2*H2']];
clean.getRange('J2:J44').fillDown();
style(clean, 'A1:K44', 'A1:K1');
clean.getRange('C1:C44').format.columnWidthPx = 155;
clean.getRange('C2:C44').format.horizontalAlignment = 'center';
clean.getRange('I2:I44').format.horizontalAlignment = 'center';
clean.getRange('K1:K44').format.columnWidthPx = 335;
clean.getRange('C2:C44').setNumberFormat('yyyy-mm-dd');
clean.getRange('G2:G44').setNumberFormat('#,##0');
clean.getRange('H2:H44').setNumberFormat('#,##0.00');
clean.getRange('J2:J44').setNumberFormat('#,##0.00');
clean.getRange('G2:H44').format.fill = '#fff5d9';
clean.getRange('J2:J44').format.fill = '#edf3f9';
clean.getRange('F2:F44').dataValidation = { rule: { type: 'list', values: ['TWD', 'USD'] } };
clean.freezePanes.freezeRows(1);
clean.tables.add('A1:K44', true, 'CleanSales');

const reasonLabels = { conflicting_order: '同單號內容衝突，兩列均待確認', duplicate_copy: '完整重複 S005，排除副本', missing_or_invalid_amount: '單價缺失，不補零', invalid_date: '無效日期', ambiguous_date: '日期順序不明', missing_or_unknown_currency: '幣別缺失，不推定台幣' };
excluded.getRange('A1:D1').values = [['來源 ID', 'CSV 列號', '隔離原因', '目前處理']];
excluded.getRange('A2:D8').values = data.excluded.map(r => [r.source_id, r.source_csv_row, reasonLabels[r.reason], r.reason === 'duplicate_copy' ? '保留原列 S005' : '等待補件或確認']);
style(excluded, 'A1:D8', 'A1:D1');
excluded.getRange('C1:C8').format.columnWidthPx = 380;
excluded.getRange('D1:D8').format.columnWidthPx = 230;
excluded.getRange('A11').values = [['來源為 sales-dirty.csv；原始列未刪除。']];
excluded.getRange('A11:D11').format.font = { name: font, size: 11, color: '#475f7d' };

report.getRange('A1:H29').format.font = { name: font, size: 11, color: '#243449' };
report.getRange('A1:H29').format.columnWidthPx = 110;
report.getRange('A1:H29').format.rowHeightPx = 28;
report.getRange('A1').values = [['合成銷售資料核對']];
report.getRange('A1').format.font = { name: font, size: 17, bold: true, color: '#243449' };
report.getRange('A2').values = [['2026-09 練習資料；分幣別統計，不做換匯。']];
report.getRange('A4:F4').values = [['幣別', '商品', '採用筆數', '淨數量', '金額', '人工基準差']];
report.getRange('A5:B7').values = [['TWD', 'cup'], ['TWD', 'notebook'], ['USD', 'cup']];
report.getRange('C5:F5').formulas = [["=COUNTIFS('Clean'!$F$2:$F$44,A5,'Clean'!$E$2:$E$44,B5)", "=SUMIFS('Clean'!$G$2:$G$44,'Clean'!$F$2:$F$44,A5,'Clean'!$E$2:$E$44,B5)", "=SUMIFS('Clean'!$J$2:$J$44,'Clean'!$F$2:$F$44,A5,'Clean'!$E$2:$E$44,B5)", '=E5-H5']];
report.getRange('C5:F7').fillDown();
report.getRange('G4:H4').values = [['基準幣別商品', '人工基準']];
report.getRange('G5:H7').values = oracle.totals.map(r => [r.currency + ' ' + r.product, Number(r.amount)]);
report.getRange('G1:H29').format.columnWidthPx = 165;
report.getRange('G5:H7').format.fill = '#fff5d9';
report.getRange('E5:F7').setNumberFormat('#,##0.00');
report.getRange('H5:H7').setNumberFormat('#,##0.00');
report.getRange('A4:H4').format = { fill: '#365477', font: { name: font, size: 11, bold: true, color: '#ffffff' }, rowHeightPx: 34 };
report.getRange('F5:F7').conditionalFormats.add('cellIs', { operator: 'notEqual', formula: 0, format: { fill: '#fde4d7', font: { bold: true } } });
report.getRange('A9:B11').values = [['原始筆數', null], ['採用筆數', null], ['隔離筆數', null]];
report.getRange('B9:B11').formulas = [["=COUNTA('Raw'!A2:A51)"], ["=COUNTA('Clean'!A2:A44)"], ["=COUNTA('Excluded'!A2:A8)"]];
report.getRange('D9:E11').values = [['TWD 合計', null], ['USD 合計', null], ['列數差', null]];
report.getRange('E9:E11').formulas = [['=SUMIF(A5:A7,"TWD",E5:E7)'], ['=SUMIF(A5:A7,"USD",E5:E7)'], ['=B9-B10-B11']];
report.getRange('E9:E10').setNumberFormat('#,##0.00');
const chart = report.charts.add('bar', [report.getRange('B4:B6'), report.getRange('E4:E6')]);
chart.title = '採用金額（TWD）';
chart.titleTextStyle.typeface = font;
chart.titleTextStyle.fontSize = 14;
chart.hasLegend = false;
chart.xAxis = { axisType: 'textAxis', textStyle: { typeface: font, fontSize: 11 } };
chart.yAxis = { numberFormatCode: '#,##0', numberFormatSourceLinked: false, textStyle: { typeface: font, fontSize: 11 } };
chart.setPosition('A13', 'H24');
report.getRange('A26').values = [['來源：sales-dirty.csv（作者原創合成資料）；人工基準見 expected-totals.csv。']];
report.getRange('A27').values = [['黃色格為可編輯輸入，藍色計算欄與圖表依公式更新。Clean 的 CSV 列號可回 Raw 查原文。']];
report.getRange('A28').values = [['本模板已完成本機計算，尚未驗證 Google Sheets 匯入與 Gemini 操作。']];
report.getRange('A29').values = [['圖表只含 TWD；美元另列，不將不同幣別相加。原始缺值保留於 Raw。']];
report.showGridLines = false;

const inspection = await wb.inspect({ kind: 'table', range: 'Report!A4:H11', include: 'values,formulas', tableMaxRows: 8, tableMaxCols: 8, maxChars: 6000 });
await fs.writeFile(path.join(verification, 'inspection.ndjson'), inspection.ndjson);
assert.deepEqual(report.getRange('C5:F7').values, [[23,141,42300,0],[19,38,3040,0],[1,2,50,0]]);
assert.deepEqual(report.getRange('B9:B11').values, [[50],[43],[7]]);
assert.deepEqual(report.getRange('E9:E11').values, [[45340],[50],[0]]);
// Meaningful dependency test: one accepted cup unit price changes by 1; its quantity is 1.
const before = clean.getRange('H2').values[0][0];
clean.getRange('H2').values = [[before + 1]];
assert.equal(report.getRange('E9').values[0][0], 45341);
assert.equal(report.getRange('F5').values[0][0], 1);
clean.getRange('H2').values = [[before]];
assert.equal(report.getRange('E9').values[0][0], 45340);
const errors = await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!', options: { useRegex: true, maxResults: 50 }, summary: 'formula errors' });
await fs.writeFile(path.join(verification, 'formula-errors.ndjson'), errors.ndjson);
const ranges = [['Raw','A1:I12','raw-top'],['Raw','A38:I51','raw-exceptions'],['Report','A1:H29','report'],['Clean','A1:K12','clean-top'],['Clean','A36:K44','clean-special'],['Excluded','A1:D11','excluded']];
for (const [sheetName, range, name] of process.argv.includes('--skip-previews') ? [] : ranges) {
  const image = await wb.render({ sheetName, range, scale: 1, format: 'png' });
  await fs.writeFile(path.join(verification, name + '.png'), new Uint8Array(await image.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(output, 'sales-audit.xlsx'));
await fs.writeFile(path.join(verification, 'results.json'), JSON.stringify({ checkedOn: '2026-09-14', engine: '@oai/artifact-tool', localCalculated: true, formulaDependencyTest: 'passed', accepted:43, excluded:7, TWD:45340, USD:50, googleSheetsImported:false, modelCalls:0, chart: { series: chart.series.items.map(s=>({values:s.formula,categories:s.categoryFormula})), currency:'TWD' }, previews:ranges.map(r=>r[2]+'.png') }, null, 2) + '\n');
console.log('Workbook created; 43 accepted, 7 excluded; TWD 45340 and USD 50; dependency check passed.');
// --skip-previews can re-export unchanged artwork after its previews were already reviewed.
