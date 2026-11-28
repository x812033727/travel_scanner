import pathlib,json,hashlib,html,re
out=pathlib.Path('/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/dyson');d=json.loads((out/'capacity-primary-research-r4.json').read_text());sha=lambda b:hashlib.sha256(b).hexdigest();anchors=[]
for n in d['ordered_action_nodes']:
 a=[]
 for source in n['anchors']:
  s=d['sources'][source['source_id']];raw=pathlib.Path(s['raw_path']).read_bytes();assert sha(raw)==source['raw_sha256'];p=pathlib.Path(source['text_path']);b=p.read_bytes();t=b.decode('utf8','strict');assert sha(b)==source['text_sha256'];lines=t.splitlines();ctx='\n'.join(lines[source['line_start_1based']-1:source['line_end_1based']]);assert sha(ctx.encode())==source['context_sha256'];assert source['short_quote_original_language'] in ctx
  aa={**source,'raw_path':s['raw_path'],'short_quote_sha256':sha(source['short_quote_original_language'].encode()),'source_evidence_level':s['evidence_level'],'original_context_reopened_by_author':True,'context_decode':'strict UTF8; no replacement','auto_transcript_not_fully_corrected':source['source_id']=='MASTERS_SCALE','audio_listened_by_this_author':False if source['source_id']=='MASTERS_SCALE' else None}
  if source['source_id']!='OU_1993':
   rawtext=raw.decode(s.get('encoding','utf8'),'strict');assert '\ufffd' not in rawtext
   # Original HTML is read as evidence; quote must exist after entity/whitespace normalization.
   plain=html.unescape(re.sub('<[^>]+>',' ',rawtext));assert source['short_quote_original_language'].lower() in re.sub(r'\s+',' ',plain).lower()
  else:aa['pdf_page4_personally_visually_read']=True;aa['research_method_page']=2;aa['not_verbatim_interview_transcript']=True
  a.append(aa)
 anchors.append({'id':n['id'],'research_claim':n['new_information'],'evidence_level':'primary_participant_recollection_or_interview_research_with_limits','anchors':a,'limits':n['limits'],'capacity_research_node_id':n['id'],'net_new_relative_to_r3':n['status'],'author_note':'New source fact candidate only, pending full independent SOURCE QA; original research unchanged.'})
obj={'schema_version':1,'revision':'dyson-r4','role':'AUTHOR_ADOPTED_NEW_PRIMARY_ANCHORS_PENDING_INDEPENDENT_SOURCE_QA','capacity_research_json_sha256':sha((out/'capacity-primary-research-r4.json').read_bytes()),'capacity_research_md_sha256':sha((out/'capacity-primary-research-r4.md').read_bytes()),'anchors':anchors,'new_raw_fetched_by_author':0,'source_raw_reopened_and_hash_verified':True,'masters_audio_listened_by_author':False,'npr_transcript_used':False,'npr_http200_body_not_transcript':True,'bank_accounts_not_merged':'SENRA/MASTERS1992/pounds vsFORTUNE1993/dollars; R4 voice uses only SENRA process/collateral, not a synthesized date or amount.','half_factory_not_identified_as_bumpers_farm':True,'node_N10_undated_scope':'Explicit early British retail establishment; no exact date, order ratio, buyer name or identification with first catalogue buyer.','source_pass_claimed':False}
(out/'author-source-additions-r4.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('new nodes anchors',len(anchors),'source IDs',sorted({a['source_id'] for n in anchors for a in n['anchors']}))
