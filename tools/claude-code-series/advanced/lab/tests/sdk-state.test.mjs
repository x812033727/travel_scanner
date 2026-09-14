import test from 'node:test';import assert from 'node:assert/strict';
import {successfulResult,requireResumeState} from '../automation/sdk/state.mjs';
test('SDK state requires a final valid result and does not accept authentication failures',()=>{
 const good={type:'result',subtype:'success',is_error:false,result:'MOKAAIR-SDK-94'};
 assert.equal(successfulResult(good),true);
 for(const change of [{type:'assistant'},{subtype:'error_max_turns'},{is_error:true},{result:'Failed to authenticate: OAuth session expired MOKAAIR-SDK-94'},{result:''}])assert.equal(successfulResult({...good,...change}),false);
 for(const previous of [null,{}, {schemaVersion:1,sessionId:null},{schemaVersion:2,sessionId:'x'}])assert.throws(()=>requireResumeState(previous));
 assert.equal(requireResumeState({schemaVersion:1,sessionId:'test-session'}).sessionId,'test-session');
});
