const byId = (id) => document.getElementById(id);
fetch('/health').then((r) => r.json()).then((data) => {
  byId('mode').textContent = data.mode === 'author_fixture' ? '作者合成測試模式：未呼叫 Google API' : '真實 API 模式：每次查詢可能產生費用';
}).catch(() => { byId('mode').textContent = '無法連線本機服務'; });
byId('query').addEventListener('submit', async (event) => {
  event.preventDefault();
  byId('send').disabled = true;
  byId('status').textContent = '查詢中';
  byId('citations').replaceChildren();
  try {
    const response = await fetch('/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: byId('question').value }) });
    const data = await response.json();
    if (!response.ok) throw new Error('查詢失敗，請核對輸入與伺服器設定。');
    byId('status').textContent = data.status === 'needs_claim_review' ? '找到引用，請對照原文' : '缺少可核對的證據';
    byId('answer').textContent = data.answer;
    for (const citation of data.citations) {
      const item = document.createElement('li');
      const source = document.createElement('a');
      source.href = `/sources/${encodeURIComponent(citation.document_id)}`;
      source.textContent = `${citation.document_id}／${citation.version}`;
      item.append(source, document.createTextNode(`（${citation.file_name}）：${citation.quote}`));
      byId('citations').append(item);
    }
  } catch (error) {
    byId('status').textContent = '未完成';
    byId('answer').textContent = error.message;
  } finally { byId('send').disabled = false; }
});
