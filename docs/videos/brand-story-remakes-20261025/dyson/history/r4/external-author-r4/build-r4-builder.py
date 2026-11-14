import pathlib
out=pathlib.Path('/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/dyson');s=(out/'history/r3/build-candidate.mjs').read_text().split('const framings=')[0]
s=s.replace('author-r3/runtime','author-r4/runtime').replace('author-r3/media','author-r4/media')
s=s.replace("addedR3=read(path.join(OUT,'author-source-additions-r3.json'));", "addedR3=read(path.join(OUT,'author-source-additions-r3.json')),addedR4=read(path.join(OUT,'author-source-additions-r4.json')),capacityResearch=read(path.join(OUT,'capacity-primary-research-r4.json'));")
s=s.replace('[...research.claim_candidates,...added.anchors,...addedR3.anchors]', '[...research.claim_candidates,...added.anchors,...addedR3.anchors,...addedR4.anchors]')
s=s.replace("sourceRegistry=Object.fromEntries(research.source_inventory.map(s=>[s.id,s]));", "sourceRegistry={...Object.fromEntries(research.source_inventory.map(s=>[s.id,s])),...capacityResearch.sources};")
s=s.replace("beforePath='/workspace/work/brand-story-20261025/dyson-audit/author-r3/protected-before-r3.json'", "beforePath='/workspace/work/brand-story-20261025/dyson-audit/author-r4/protected-before-r4.json'")
s=s.replace("voicePath=path.join(OUT,'history/r2/video.json')", "voicePath=path.join(OUT,'history/r3/video.json')")
# Original source quotes and exact1-based line contexts are revalidated on every build.
s += "\nfor(const c of addedR4.anchors)for(const a of c.anchors){assert.equal(fileSha(a.text_path),a.text_sha256);const text=fs.readFileSync(a.text_path,'utf8'),ctx=text.split(/\\r?\\n/).slice(a.line_start_1based-1,a.line_end_1based).join('\\n');assert.equal(sha(ctx),a.context_sha256);assert(ctx.includes(a.short_quote_original_language));}\n"
(out/'build-candidate.mjs').write_text(s)
