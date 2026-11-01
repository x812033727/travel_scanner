#!/usr/bin/env node
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { ROOT, DIRECTORY, LABELS, buildCatalog, readCatalog, renderAudit, renderTopics, select, brief } from './catalog.mjs';

const [command = 'help', id, ...extra] = process.argv.slice(2);
try {
  if (extra.length || (['build', 'check', 'list', 'help'].includes(command) && id)) throw new Error('Unexpected arguments');
  if (command === 'build') {
    const catalog = buildCatalog();
    writeFileSync(path.join(ROOT, DIRECTORY, 'catalog.json'), `${JSON.stringify(catalog, null, 2)}\n`);
    writeFileSync(path.join(ROOT, DIRECTORY, 'AUDIT.md'), renderAudit(catalog));
    writeFileSync(path.join(ROOT, DIRECTORY, 'TOPICS.md'), renderTopics(catalog));
    console.log(JSON.stringify(catalog.counts));
  } else if (command === 'check') {
    console.log(JSON.stringify({ status: 'PASS', ...readCatalog().counts, production_synced: false }));
  } else if (command === 'list') {
    const catalog = readCatalog();
    for (const topic of catalog.episodes.filter((entry) => entry.active)) console.log(`${topic.id}\t${LABELS[topic.disposition]}\t${topic.title}`);
  } else if (command === 'show' || command === 'brief') {
    if (!id) throw new Error('A topic id is required');
    const catalog = readCatalog();
    console.log(JSON.stringify(command === 'brief' ? brief(catalog, id) : select(catalog, id), null, 2));
  } else if (command === 'help') {
    console.log('Editorial selector (local only): build | check | list | show <id> | brief <active-id>');
  } else throw new Error(`Unknown command: ${command}`);
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
