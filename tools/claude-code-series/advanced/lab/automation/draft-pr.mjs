import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
const issue=JSON.parse(readFileSync('fixtures/issue.json','utf8'));
const directory='run-data';mkdirSync(directory,{recursive:true});
const body=`# 待辦篩選草稿\n\n## 問題\n${issue.title??'待辦清單需要三種篩選'}\n\n## 變更\n待填入實際差異與檔案。\n\n## 驗證\n待填入本機實際命令及結果；未執行的項目明列。\n\n這是本機草稿，尚未建立或送出 GitHub PR。\n`;
writeFileSync(directory+'/draft-pr.md',body);console.log('Created local run-data/draft-pr.md; no network request.');
