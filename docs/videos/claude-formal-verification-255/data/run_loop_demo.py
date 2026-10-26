import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parent
source = root / 'loop.c'
binary = root / 'loop-demo'
command = [shutil.which('gcc'), '-std=c11', '-O0', '-Wall', '-Wextra', '-Werror',
           '-Wconversion', '-Wshadow', '-pedantic', str(source), '-o', str(binary)]
compiled = subprocess.run(command, text=True, capture_output=True)
assert compiled.returncode == 0, compiled.stderr

def observed(mode, n):
    argv = [str(binary), mode, str(n)]
    try:
        r = subprocess.run(argv, text=True, capture_output=True, timeout=0.25)
        assert r.returncode == 0, r.stderr
        return {'command': argv, 'exit_code': r.returncode, 'stdout': r.stdout,
                'stderr': r.stderr, 'returned_i': int(r.stdout), 'timed_out': False}
    except subprocess.TimeoutExpired:
        return {'command': argv, 'timed_out': True, 'timeout_seconds': 0.25,
                'interpretation': 'Observed timeout only; cycle analysis below establishes nontermination in the finite control model.'}

# For this loop, the entire changing control state is i; n is fixed.
# Volatile local counters keep their reads/writes observable to the C compiler.
# No pointer to them escapes; the modeled program has no external writer.
def explore(n, width):
    i = 0
    states = []
    seen = {}
    modulus = 1 << width
    while i <= n:
        if i in seen:
            return {'n': n, 'counter_bits': width, 'terminates': False,
                    'cycle_start': seen[i], 'cycle_length': len(states) - seen[i],
                    'repeated_state': i, 'states_before_repeat': states}
        seen[i] = len(states)
        states.append(i)
        i = (i + 1) % modulus
    return {'n': n, 'counter_bits': width, 'terminates': True,
            'iterations': len(states), 'exit_i': i}

cases = []
for n in range(256):
    bad_model = explore(n, 8)
    fixed_model = explore(n, 16)
    fixed_c = observed('fixed', n)
    assert fixed_model['terminates']
    assert fixed_c['returned_i'] == fixed_model['exit_i'] == n + 1
    if n < 255:
        bad_c = observed('bad', n)
        assert bad_model['terminates'] and bad_c['returned_i'] == n + 1
    else:
        bad_c = observed('bad', n)
        assert bad_c['timed_out'] and not bad_model['terminates']
        assert bad_model['cycle_length'] == 256 and bad_model['repeated_state'] == 0
    cases.append({'n': n, 'bad_model': bad_model, 'fixed_model': fixed_model,
                  'bad_compiled_c': bad_c, 'fixed_compiled_c': fixed_c})

summary = {
    'scope': 'Original finite control-graph enumeration plus actual compiled C observations; not SAT/SMT/Rocq and not vendor-proof reproduction.',
    'domain': 'n=0..255; loop starts i=0; desired exit after n+1 increments',
    'bad_nonterminating_inputs_in_model': [r['n'] for r in cases if not r['bad_model']['terminates']],
    'fixed_terminating_inputs_in_model': sum(r['fixed_model']['terminates'] for r in cases),
    'fixed_compiled_c_matches_all_256': True,
    'bad_compiled_c_255_timeout_observed': cases[255]['bad_compiled_c'],
    'bad_model_255_cycle': cases[255]['bad_model'],
    'selected': [cases[n] for n in [0, 7, 254, 255]],
    'compile': {'command': command, 'exit_code': compiled.returncode,
                'stdout': compiled.stdout, 'stderr': compiled.stderr},
    'environment': {'python': sys.version.split()[0],
                    'gcc': subprocess.run([command[0], '--version'], text=True, capture_output=True, check=True).stdout.splitlines()[0]},
    'limits': ['No unbounded native run is allowed: timeout kills the one hanging subprocess.',
               'Timeout by itself does not prove nontermination; the repeated finite control state and deterministic transition do.',
               'Only these local-counter loops, with no external writer, and n=0..255 domain are analyzed.',
               'No proof checker certificate, verified compiler, concurrency, external I/O, OS scheduling or process failure is modeled.',
               'C integer promotion occurs before the explicit narrowing cast; this is not undefined signed overflow.'],
}
(root / 'loop-all-256.json').write_text(json.dumps(cases, indent=2) + '\n')
(root / 'loop-results.json').write_text(json.dumps(summary, indent=2) + '\n')
manifest = {}
for name in ['loop.c', 'run_loop_demo.py', 'loop-demo', 'loop-all-256.json', 'loop-results.json']:
    p = root / name
    manifest[name] = {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
(root / 'loop-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({k: summary[k] for k in ['scope', 'bad_nonterminating_inputs_in_model',
    'fixed_terminating_inputs_in_model', 'fixed_compiled_c_matches_all_256',
    'bad_compiled_c_255_timeout_observed']}, indent=2))
