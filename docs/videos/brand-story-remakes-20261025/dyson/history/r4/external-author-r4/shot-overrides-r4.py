import pathlib
p=pathlib.Path('/workspace/work/brand-remakes-source/docs/videos/brand-story-remakes-20261025/dyson/build-candidate.mjs');s=p.read_text();needle='const oldVideo='
insert="""const r4ShotOverrides={
'sthq':'Medium shot in a small project office, an anonymous inventor holding an unmarked prototype housing beside a closed plain planning folder, soft interior light.',
 'ti4n':'Close-up at a factory collection station, an anonymous worker holding the edge of a broad powder-covered cloth filter beside a plain metal rack, mild overhead light.',
 'xmha':'Wide shot in a domestic room, an anonymous owner looking inside a plain storage cupboard beside an unmarked upright appliance, muted daylight.',
 'uj7b':'Close-up at a domestic inspection table, an anonymous owner opening a plain dust bag to reveal a fine dusty lining, soft window light.',
 '3v4y':'Wide shot at an explanation table, an anonymous experimenter holding a clogged plain fabric bag beside a small wordless airflow model, diffuse light.',
 'y5py':'Medium close-up at a home experiment table, an anonymous maker attaching a plain cardboard cone to an unmarked flexible hose, mild lamp light.',
 'e74a':'Wide shot in a small home workshop, an anonymous maker opening a plain box of small hand tools beside a metal workpiece, soft side light.',
 '3b3d':'Medium shot at a test bench, an anonymous experimenter setting one plain test chamber beside a similar altered model and an unlettered notebook, soft interior light.',
 '5uh4':'Close-up at a model shelf, an anonymous researcher lifting a small plain metal model from a shallow tray beside simple transparent models, muted window light.',
 'shcn':'Medium shot at an earlier dispatch table, an anonymous clerk standing beside an unmarked appliance carton on a plain trolley, mild overhead light.',
 'ucyp':'Close-up in a design reading room, an anonymous reader holding a closed wordless design book with an abstract appliance silhouette on its cover, diffuse light.',
 'uih5':'Medium shot at a modest meeting table, an anonymous coordinator placing an unlettered order form beside a loose plain housing piece, soft interior light.',
 'sby4':'Wide shot at a demonstration table, an anonymous technician holding a plain cone-shaped chamber above a simple cylindrical collection bin, muted daylight.',
 'n6tt':'Close-up at a component experiment bench, an anonymous technician lifting one plain perforated cup from a shallow tray beside a cup with differently shaped holes, soft side light.',
 'v4g4':'Wide shot at an unmarked workshop doorway, an anonymous visiting engineer stepping inside while holding a closed plain notebook, mild indoor light.',
 'xw4x':'Medium shot at a tilted drafting board, an anonymous designer pointing at a wordless floor-head outline beside a simple plain cleaner-head model, soft overhead light.',
 'inii':'Medium close-up at a small shop counter, an anonymous adult holding an unmarked price tag beside a closed plain appliance carton, soft window light.',
 '6w42':'Wide shot in a quiet room, an anonymous adult looking toward a simple house through a window while holding a closed plain folder, muted daylight.',
 'x8ph':'Close-up at an assembly bench, an anonymous worker holding a plain housing beside unmarked parts bins and a closed cardboard box, mild overhead light.',
 'dahx':'Medium shot in an archive room, an anonymous reader keeping two closed unlettered folders apart on a clear table, soft interior light.',
 'hp4p':'Medium close-up in a demonstration room, an anonymous demonstrator holding a plain powder container beside a carpet patch covered in dry cleaning powder, diffuse light.',
 '2566':'Close-up at a mail-order planning table, an anonymous buyer pointing at an empty unlettered catalogue slot beside a plain product carton, soft lamp light.',
 'b4dg':'Medium shot in a catalogue office, an anonymous buyer placing a small unmarked appliance parcel beside a closed wordless catalogue, muted interior light.',
 '3qra':'Wide shot at a shop storage doorway, an anonymous coordinator considering a bare unmarked display shelf beside a plain appliance carton, soft window light.',
 'jtzs':'Close-up at a retail demonstration counter, an anonymous shop worker holding a plain transparent dust container beside an unmarked display stand, mild overhead light.',
 'kiud':'Medium shot in a plain room, an anonymous owner looking into a transparent collection container with visible dust, soft side light.',
 '6m9s':'Medium close-up in a shop office, an anonymous representative reviewing an unlettered information sheet beside a plain appliance stand, diffuse light.',
 'cvp5':'Medium shot in a modest retail meeting room, an anonymous retailer pointing toward a blank unmarked television screen beside a closed folder, soft interior light.',
 'hnrg':'Close-up at a planning desk, an anonymous planner placing an unlettered order folder beside a plain blank television screen, mild lamp light.',
 'r2i6':'Wide shot near a shop doorway, an anonymous representative closing a plain agreement folder beside an unmarked appliance carton, muted daylight.'
};for(const r of rows)if(r4ShotOverrides[r.id])r.prompt=r4ShotOverrides[r.id];
"""
assert needle in s;s=s.replace(needle,insert+needle,1);p.write_text(s)
