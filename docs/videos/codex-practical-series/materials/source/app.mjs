import * as core from './core.mjs';
import { loadStorage, saveStorage } from './storage.mjs';
import { features, storageKey } from './lesson-config.mjs';
const input=document.querySelector('#task-title'), list=document.querySelector('#tasks'),
  filter=document.querySelector('#filter'), search=document.querySelector('#search'), message=document.querySelector('#message');
for(const element of document.querySelectorAll('[data-feature]')) element.hidden=!features[element.dataset.feature];
const loaded=loadStorage(localStorage,storageKey,core.decodeTasks,features.data?'mokaair-codex-practical-v1':null);
let tasks=loaded.tasks, available=loaded.available;
if(!available) message.textContent='儲存資料損毀或不可用。原始值已保留，目前操作暫存，重新整理會失去暫存變更。';
else if(loaded.migrated) message.textContent='已讀取舊資料；未知完成時間保持未知。原本 v1 儲存值已保留。';
function persist() {
  if(available && !saveStorage(localStorage,storageKey,core.encodeTasks(tasks))) {
    available=false; message.textContent='儲存失敗；目前變更只在此分頁，請先匯出。';
  }
}
function render(focus=null) {
  list.replaceChildren();
  const shown=core.visibleTasks(tasks,filter.value,features.search?search.value:'');
  for(const task of shown) {
    const li=document.createElement('li'), label=document.createElement('label'), check=document.createElement('input'),
      title=document.createElement('span'), remove=document.createElement('button');
    check.type='checkbox'; check.checked=task.completed; check.dataset.id=task.id;
    title.textContent=task.title;
    remove.type='button'; remove.textContent='刪除'; remove.dataset.id=task.id; remove.setAttribute('aria-label',`刪除 ${task.title}`);
    check.addEventListener('change',()=>{tasks=core.toggleTask(tasks,task.id);persist();render(task.id);});
    remove.addEventListener('click',()=>{tasks=core.removeTask(tasks,task.id);persist();render(task.id);});
    label.append(check,title);li.append(label,remove);list.append(li);
  }
  document.querySelector('#count').textContent=`${tasks.filter(task=>!task.completed).length} 項未完成／共 ${tasks.length} 項`;
  document.querySelector('#empty').hidden=shown.length>0;
  if(focus) ([...list.querySelectorAll('input')].find(element=>element.dataset.id===focus)||input).focus();
}
document.querySelector('#task-form').addEventListener('submit',event=>{
  event.preventDefault();
  try {tasks=core.addTask(tasks,input.value,crypto.randomUUID());persist();input.value='';if(available)message.textContent='已新增。';render();input.focus();}
  catch {message.textContent='請輸入 1 到 100 個非空白字元。';}
});
filter.addEventListener('change',()=>render());search.addEventListener('input',()=>render());
document.querySelector('#reset').addEventListener('click',()=>{
  // v2 must keep an empty document, otherwise the preserved v1 would migrate again on reload.
  try {if(features.data){if(!saveStorage(localStorage,storageKey,core.encodeTasks([])))throw new Error('storage-denied');}
    else localStorage.removeItem(storageKey);available=true;tasks=[];message.textContent='已重設目前練習資料。';}
  catch {available=false;tasks=[];message.textContent='儲存仍不可用，目前清單只在此分頁。';} render();
});
function download(name,type,raw) {const url=URL.createObjectURL(new Blob([raw],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
if(features.data) {
  document.querySelector('#export-json').addEventListener('click',()=>download('tasks.json','application/json',core.encodeTasks(tasks)));
  document.querySelector('#export-csv').addEventListener('click',()=>download('tasks.csv','text/csv',core.encodeCsv(tasks)));
  document.querySelector('#import-file').addEventListener('change',async event=>{
    const file=event.target.files[0];if(!file)return;
    try {const raw=await file.text();const imported=file.name.toLowerCase().endsWith('.csv')?core.importCsv(tasks,raw):core.importJson(tasks,raw);
      tasks=imported;persist();if(available)message.textContent='整批匯入完成。';render();}
    catch(error) {message.textContent=`整批匯入拒絕：${error.message}。原本待辦保留。`;} finally {event.target.value='';}
  });
  document.querySelector('#report-form').addEventListener('submit',event=>{
    event.preventDefault();try {document.querySelector('#report').textContent=JSON.stringify(core.weeklyReport(tasks,document.querySelector('#from').value,document.querySelector('#to').value),null,2);}
    catch(error) {message.textContent=error.message;}
  });
}
render();
