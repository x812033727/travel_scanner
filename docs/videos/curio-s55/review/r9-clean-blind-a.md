# Curio S55 R9: clean blind narrative ballot A

Reviewed only `script.md` against the 13 questions returned by `narrative --slug curio-s55 --json`. No episode reviews, briefs, sources, or other ballots were read before the vote.

Script SHA-256 before: `b72d5d03ef71f86673b68b59c616b06ec404ea40c8cb46e02a682ea6f716c45f`<br>
Script SHA-256 after: `b72d5d03ef71f86673b68b59c616b06ec404ea40c8cb46e02a682ea6f716c45f`

| Question | Vote | Script evidence |
| --- | --- | --- |
| `scene_first` | **Yes** | [s55001] puts Franklin at a Paris area garden watching an occupied balloon; [s55002]–[s55004] give the tree collision and fire danger. |
| `no_spoiler` | **Yes** | [s55002]–[s55005] stop before the tree incident's outcome; [s55007] and [s55008] ask about the earlier balloon and the letter date. |
| `one_line` | **Yes** | After the preview, [s55009], [s55044], [s55064], [s55094], and [s55115] move from empty balloon to animals, tethered passengers, tree test, then free flight. |
| `no_toc` | **Yes** | [s55006] and [s55008] plant factual mysteries; [s55091] names the next test as an event, without outlining the video. |
| `chapters_link` | **Yes** | [s55009]→[s55010], [s55043]→[s55044], [s55063]→[s55064], [s55093]→[s55094], and [s55114]→[s55115] carry the previous question or action into the next chapter. |
| `open_loops` | **Yes** | Concrete questions recur at [s55018], [s55027], [s55049], [s55070], [s55088], [s55107], [s55124], and [s55137], without an apparent 90 second gap. |
| `payoffs` | **Yes** | [s55007]→[s55016] answers the earlier balloon; [s55027]→[s55030] its landing; [s55049]→[s55057] the animals; [s55089]→[s55110] the tether; [s55129]→[s55131] the passengers; [s55008]→[s55134]–[s55140] the date. |
| `no_recap` | **No** | [s55018] gives Charles's balloon as twelve feet wide; [s55038] repeats the same twelve foot figure. The comparison adds context, but the repeated number is not explicitly marked as a recall. |
| `chapters_are_events` | **Yes** | The headings describe the collision [s55002], empty ascent [s55027], animals ascending [s55044], a tethered human ascent [s55064], the tree test [s55104], and free flight [s55115]. |
| `outro_no_next` | **Yes** | [s55998] asks for a comment and [s55999] asks for a subscription; neither mentions another episode. |
| `opening_hooks` | **Yes** | After the first scene, [s55003]–[s55005] raise fall, fire, and release risks; [s55007] and [s55008] add the earlier balloon and date mystery. |
| `one_thread` | **Yes** | The challenge of reaching human free flight carries from [s55005] through [s55034], [s55058], [s55088], and [s55115] to [s55145]. |
| `no_detour` | **Yes** | The earlier balloon [s55016], animals [s55057], tethered trials [s55071] and [s55110], and date check [s55140]–[s55143] all establish what counts as the first human free flight. |

**Result: 12 yes, 1 no.** The `no_recap` vote is based on the repeated twelve foot measurement at [s55018] and [s55038].

The narrative CLI accepted all 13 cited answers and returned exit code 1 with `failed: [no_recap]`, as expected for this ballot.
