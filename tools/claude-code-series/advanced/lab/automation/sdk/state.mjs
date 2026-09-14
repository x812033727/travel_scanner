export function successfulResult(message){
 return message.type==='result'&&message.subtype==='success'&&!message.is_error&&typeof message.result==='string'&&message.result.includes('MOKAAIR-SDK-94')&&!/failed to authenticate|OAuth session expired/i.test(message.result);
}
export function requireResumeState(previous){
 if(!previous||previous.schemaVersion!==1||typeof previous.sessionId!=='string'||!previous.sessionId.trim())throw new Error('No compatible saved session id; start a new run');
 return previous;
}
