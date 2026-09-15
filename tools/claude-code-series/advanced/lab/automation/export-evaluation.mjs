import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
const rows=JSON.parse(readFileSync(process.argv[2]??'fixtures/evaluation.json','utf8'));
const columns=['method','case','seconds','attempts','passed'];
const cell=value=>{let text=String(value);if(/^[=+@-]/.test(text))text="'"+text;return '"'+text.replaceAll('"','""')+'"';};
mkdirSync('run-data',{recursive:true});
writeFileSync('run-data/evaluation.csv',[columns.join(','),...rows.map(row=>columns.map(key=>cell(row[key])).join(','))].join('\r\n')+'\r\n');
console.log('Saved run-data/evaluation.csv; demo fixture values are synthetic.');
