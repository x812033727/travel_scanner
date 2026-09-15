export function parseResult(text) {
 const envelope=JSON.parse(text);
 if(envelope.type!=='result' || envelope.subtype!=='success' || envelope.is_error===true) throw new Error('Claude did not return a successful result');
 const data=envelope.structured_output;
 if(!data || typeof data.summary!=='string' || !data.summary.trim() || !Array.isArray(data.taskIds) || data.taskIds.some(id=>typeof id!=='string'||!id)) throw new Error('Invalid structured_output');
 if(new Set(data.taskIds).size!==data.taskIds.length)throw new Error('Duplicate task ids');
 return {summary:data.summary,taskIds:data.taskIds};
}
export function lastResult(stream) {
 const events=stream.split(/\r?\n/).filter(Boolean).map(line=>JSON.parse(line));
 const results=events.filter(event=>event.type==='result');
 if(results.length!==1)throw new Error('Expected exactly one final result');
 return parseResult(JSON.stringify(results[0]));
}
