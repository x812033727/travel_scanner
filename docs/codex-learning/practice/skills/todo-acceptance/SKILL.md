---
name: todo-acceptance
description: Verify the Small Steps todo practice website after a change, using its existing tests and browser checks. Use for acceptance checks of this exercise, not unrelated websites or feature implementation.
---

# Small Steps acceptance

Confirm the requested practice folder contains index.html, style.css, app.js,
core.mjs and core.test.mjs. If these are missing, stop and report the path checked.

Read the existing code, then run `node --test core.test.mjs` from that folder.
Do not rewrite tests or implementation to make an acceptance run pass.

If a browser is available, preview the site on a loopback address with a fresh
browser context. Add Read and Build, complete Read, check Active and Completed
filters, reload, and delete Read. Reject whitespace-only input. Check 390px and
1280px widths and visible Tab focus. Keep existing user browser data unchanged.

Report PASS, FAIL or NOT RUN for each check, with the command, observation or
limitation. Include the working folder and remaining issues. Do not claim that
tests, screenshots, deployment or publication happened without evidence.

If a check fails, report the reproduction and relevant file. If a required tool
is unavailable, report NOT RUN and the manual steps. Finish with results only;
implement fixes only when the user requests them.
