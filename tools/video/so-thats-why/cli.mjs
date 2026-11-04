#!/usr/bin/env node
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { ROOT, DIRECTORY, buildCatalog, readCatalog, renderAudit, renderTopics, select } from './catalog.mjs';
import { buildProgram, readProgram, episodeBrief, renderProgram, renderDurationAudit, TIERS } from './program.mjs';

const [command = 'help', id, ...extra] = process.argv.slice(2);
try {
  if (extra.length || (['build', 'check', 'list', 'topics', 'help'].includes(command) && id)) throw new Error('Unexpected arguments');
  if (command === 'build') {
    const catalog = buildCatalog();
    const program = buildProgram(catalog);
    writeFileSync(path.join(ROOT, DIRECTORY, 'catalog.json'), `${JSON.stringify(catalog, null, 2)}\n`);
    writeFileSync(path.join(ROOT, DIRECTORY, 'AUDIT.md'), renderAudit(catalog));
    writeFileSync(path.join(ROOT, DIRECTORY, 'TOPICS.md'), renderTopics(catalog));
    writeFileSync(path.join(ROOT, DIRECTORY, 'episodes.json'), `${JSON.stringify(program, null, 2)}\n`);
    writeFileSync(path.join(ROOT, DIRECTORY, 'EPISODES.md'), renderProgram(program));
    writeFileSync(path.join(ROOT, DIRECTORY, 'DURATION-AUDIT.md'), renderDurationAudit(program, catalog));
    console.log(JSON.stringify({ catalog: catalog.counts, program: program.counts }));
  } else if (command === 'check') {
    const { catalog, program } = readProgram();
    console.log(JSON.stringify({ status: 'PASS', catalog: catalog.counts, program: program.counts, production_synced: false }));
  } else if (command === 'list') {
    for (const plan of readProgram().program.plans) console.log(`${plan.id}\t${TIERS[plan.tier]}\t${plan.range.join('–')} min\t${plan.topics.join('+')}\t${plan.title}`);
  } else if (command === 'topics') {
    for (const topic of readCatalog().episodes.filter((entry) => entry.active)) console.log(`${topic.id}\tSOURCE_POOL_ONLY\t${topic.title}`);
  } else if (command === 'show' || command === 'brief') {
    if (!id) throw new Error('A topic id is required');
    const { catalog, program } = readProgram();
    console.log(JSON.stringify(command === 'brief' ? episodeBrief(catalog, program, id) : { ...select(catalog, id), duration_decision: program.dispositions.find((entry) => entry.id === id) ?? null }, null, 2));
  } else if (command === 'help') {
    console.log('Editorial selector (local only): build | check | list (episode plans) | topics (source pool) | show <topic-id> | brief <Pxx-or-selected-topic-id>');
  } else throw new Error(`Unknown command: ${command}`);
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
