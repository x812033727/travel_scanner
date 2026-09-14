# Filter requirements

Given Read is completed and Build is incomplete:

- All returns Read, then Build.
- Active returns Build only.
- Completed returns Read only.
- An empty input returns an empty result for every filter.
- Filtering preserves task order and does not modify the input.

Core checks: node --test core.test.mjs
Browser check: create both tasks, complete Read, and inspect all three filters.

[Back to project](../README.md)
