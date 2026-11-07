# Independent review of a finished cut (brief for a reviewer agent that did not make the episode)

The maker reviews its own picks and missed what the owner then saw at once (e004-r2: the casket grew and shrank, the door
moved relative to the wok, Xu Yan came out and the figure was not where he looked). So before a cut goes to the owner, an
agent that took no part in making it reviews it from the script. It spends no money and changes nothing.

## When
Twice per episode (owner 2026-11-07): after the drafts are picked and before they are refined (sheets made from
`runpod/a/st1/out` with `continuity-sheets.py` in picks mode), and again on the finished cut. Severe and medium findings
are fixed, minor ones accepted.

## What the reviewer gets
- `docs/videos/zhong-tian-qu-qi-eNNN-r2/script.md` — the storyboard: what each shot must show, who is where, props, light.
- The continuity sheets (`continuity-sheets.py` output): one image per scene, each shot as a row of start / middle / end
  frames in cut order, labelled with the shot id and its first line.
- The results of `cut-qa.py`, `cut-jumps.py` and `audio-qa.py` (so it does not repeat them).

## What the reviewer checks, scene by scene, against the script
1. **Props**: the same object at the same size, shape and colour in every shot (a casket the size of a book stays that
   size; a knife keeps its blade; a paper stays folded or blank); it is in the hand or place the script says.
2. **Places**: the same layout and distances shot to shot (door, stove, table, gate, well, fence on the same sides).
3. **Eyelines and reactions**: when someone looks at something or reacts to it, it is in that direction and visible in
   the shot before or after; a reaction shot is in the place the script puts the person.
4. **People**: the right number; nobody twice; faces, hair and clothes match the cast; nobody is missing who must be there;
   a low neckline on Tang Xiaotang is fine (owner 2026-11-07), only see-through or bare is a finding; expressions as written (a "not smiling" line that smiles is a finding).
5. **Story**: each shot shows the action its row describes; the scene's ending (結尾) reads; a question is answered where
   the script says.
6. **Look**: anything drawn that should not be — writing on paper or signs, a system panel drawn into the picture, glowing
   eyes, modern objects, specks on skin, cartoon-looking people, a flash of another picture; a night shot whose window,
   door or sky is lit like day.
7. **What still frames miss** (《恁祖媽今年18》 e001, 2026-11-07: two review rounds passed, the owner then saw at once a bell
   nobody could hear, a doorway bright as day, a hand fused into the paper it held): step frame by frame through every
   hand that holds, passes or tucks away an object; measure each signature sound effect's second (`ebur128`) against the
   seconds around it; and in a shot where a line is placed at the start but the action at the end, say that the sound
   comes seconds before the picture.

## What it returns
A list, most serious first. Each item: shot id, what is wrong, what the script says, and the fix it suggests
(trim with `stage-clips.sh NN sNN@SECS`, retake with a rewritten line, or accept). Items it is unsure of are marked as
such. If a scene has no problem, it says so. No praise, no summary of the plot.
