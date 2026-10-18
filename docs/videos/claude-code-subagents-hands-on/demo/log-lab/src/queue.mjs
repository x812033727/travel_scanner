const stamp = () => new Date().toISOString().slice(11, 19);

export function logLine(verb, job, detail) {
  return `${stamp()} ${verb.padEnd(5)} ${job} ${detail}`;
}

export const VERBS = ['start', 'step', 'retry', 'done', 'beat'];
