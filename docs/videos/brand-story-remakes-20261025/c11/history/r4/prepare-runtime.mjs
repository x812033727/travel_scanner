// Only the newly authorized C11 project is prepared. No other episode or prior dictionary is copied.
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url));
const helper=path.resolve(here,'../prepare-runtime.mjs');
const root='/workspace/work/brand-story-20261025/c11-submission-root';
const media='/workspace/work/brand-story-20261025/media';
execFileSync(process.execPath,[helper,root,media,'c11'],{stdio:'inherit'});
