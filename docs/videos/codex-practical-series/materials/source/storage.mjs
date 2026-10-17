// Storage adapter stays separate so failures can be exercised without mocking a browser.
export function loadStorage(storage,key,decode,legacyKey) {
  try { const raw=storage.getItem(key); const source=raw===null && legacyKey ? storage.getItem(legacyKey) : raw;
    return {tasks:decode(source),available:true,migrated:raw===null && source!==null}; }
  catch(error) { return {tasks:[],available:false,migrated:false,error:error.message}; }
}
export function saveStorage(storage,key,raw) {
  try { storage.setItem(key,raw); return true; } catch { return false; }
}
