// Only the newly authorized C14 project; normal immutable dictionary initialization.
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url));
execFileSync(process.execPath,[path.resolve(here,'../prepare-runtime.mjs'),'/workspace/work/brand-story-20261025/c14-submission-root','/workspace/work/brand-story-20261025/media','c14'],{stdio:'inherit'});
