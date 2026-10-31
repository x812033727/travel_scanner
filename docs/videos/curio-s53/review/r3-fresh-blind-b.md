# S53 R3 fresh blind narrative review — panel B

**Result:** 11 pass, 2 fail (`scene_first`, `payoffs`). Judged only from `narrative --slug curio-s53 --json`; the script file was hashed without reading its prose.

## Hash basis

| Object | SHA-256 | Basis |
| --- | --- | --- |
| `docs/videos/curio-s53/script.md` | `06f5fda2ff565fa20ab698fa1a4ffcf4e4528beffc94ce16a0185c95aaaf7548` | Raw script-file bytes |
| JSON `narration` | `0a33a405997285f75fbe1870bbd27ada63f10f352162a76f9066ca26c1bf9d2e` | Parsed narration string, encoded as UTF-8 with line breaks |

## Official questions

| ID | Verdict | Evidence and reason |
| --- | --- | --- |
| `scene_first` | **Fail** | `s53001–s53004`: the cottages merely remain in a 1907 square; the next line moves to a 1913 report, then two lines explain permission and ownership. The first four lines do not enact one moment. Anchor the recorded June 1907 clearance demand in the square and retain the report as attribution. |
| `no_spoiler` | Pass | `s53001–s53009` raises the clearance, payment, and survey questions; the installment change (`s53058`), relocation requirement (`s53072`), and survey count (`s53105`) wait until later. |
| `one_line` | Pass | After the 1907 preview (`s53001`), the story moves from the 1906 disaster (`s53010`) through building (`s53028`), purchase (`s53049`), clearance (`s53069`), moves (`s53084`), and the 1908 survey (`s53101`). |
| `no_toc` | Pass | `s53006–s53008`, `s53048`, `s53083`, and `s53097` pose story questions; none announces a chapter plan or list. |
| `chapters_link` | Pass | The chapter handoffs connect the origin (`s53009→s53010`), building (`s53027→s53028`), acquisition (`s53048→s53049`), deadline (`s53068→s53069`), moves (`s53083→s53084`), and fieldwork (`s53100→s53101`). |
| `open_loops` | Pass | Hooks recur within 90 seconds across the body: `s53007`, `s53023`, `s53048`, `s53061`, `s53074`, `s53094`, `s53097`, `s53111`, `s53123`, `s53129`. |
| `payoffs` | **Fail** | The rent, moving-cost, and survey hooks get facts (`s53006→s53058`, `s53007→s53091`, `s53008→s53105`). But `s53116` asks if a cottage can remain after its land lease ends, and `s53117` only says the survey could not predict it. No later line supplies the outcome. State that uncertainty as a finding, or supply a sourced outcome. |
| `no_recap` | Pass | The deadline in `s53069` explicitly calls back to the opening `s53002`; the one-year permission (`s53025–s53026`) and later clearance order are separate actions. `s53084–s53087` and `s53103–s53107` distinguish counts rather than repeat them. |
| `chapters_are_events` | Pass | The headings correspond to the cottages remaining (`s53001`), tents occupying ground (`s53010`), building and assignment (`s53028`), rent changing to purchase (`s53058`), delayed clearance (`s53071`), relocation (`s53084`), and partial survey discovery (`s53105`). |
| `outro_no_next` | Pass | `s53997–s53999` revisits the rent dilemma and asks for a subscription; it names no next installment. |
| `opening_hooks` | Pass | `s53006–s53009` offers four delayed moments: installments, moving costs, fieldwork, and the land-and-cost problem. |
| `one_thread` | Pass | The same cottages and their placement problem link `s53005`, `s53027`, `s53048`, `s53060`, `s53072`, `s53093`, `s53110`, and `s53997`. |
| `no_detour` | Pass | Supply trouble (`s53019–s53022`) explains construction delay (`s53031`); totals (`s53039–s53043`) set scale for relocated houses (`s53084`); water and repossession (`s53124`, `s53130`) show relocation consequences. |
