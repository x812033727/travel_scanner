import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import sympy
from sympy import And, Not, Or, Xor, false, symbols, true
from sympy.logic.inference import satisfiable

root=Path(__file__).resolve().parent
source=root/'guard.c'
binary=root/'guard-demo'
gcc=shutil.which('gcc')
assert gcc,'No installed GCC; this script does not install a compiler'
compile_command=[gcc,'-std=c11','-O0','-Wall','-Wextra','-Werror','-Wconversion','-Wshadow','-pedantic',str(source),'-o',str(binary)]
compiled=subprocess.run(compile_command,capture_output=True,text=True)
assert compiled.returncode==0,compiled.stderr
run=subprocess.run([str(binary)],capture_output=True,text=True,check=True)
(root/'compiled-c-results.csv').write_text(run.stdout)
rows=[{key:int(value) for key,value in row.items()} for row in csv.DictReader(io.StringIO(run.stdout))]
assert len(rows)==256 and [row['n'] for row in rows]==list(range(256))

bits=symbols('b0:8')
# The model adds 1 using a ripple carry. It keeps the final carry for the repair.
carry=true
sum_bits=[]
for bit in bits:
    sum_bits.append(Xor(bit,carry))
    carry=And(bit,carry)
carry_out=carry

# A wrapped eight-bit result is <= 8 iff bits 7..4 are zero and,
# when bit3 is one, bits 2..0 are all zero.
wrapped_le_eight=And(*(Not(sum_bits[i]) for i in range(4,8)),
    Or(Not(sum_bits[3]),And(*(Not(sum_bits[i]) for i in range(3)))))
good_widened=And(Not(carry_out),wrapped_le_eight)
# Independent mathematical specification: n+1<=8 for 0<=n<=255 iff n<=7.
spec=And(*(Not(bits[i]) for i in range(3,8)))
bad=wrapped_le_eight
good_bound=spec

model_rows=[]
for n in range(256):
    assignment={bit:bool((n>>i)&1) for i,bit in enumerate(bits)}
    values=[int(bool(formula.subs(assignment))) for formula in [bad,good_widened,good_bound,spec]]
    expected=[rows[n][key] for key in ['bad','widened','bound','mathematical_fits']]
    assert values==expected,('SAT encoding and compiled C disagree',n,values,expected)
    model_rows.append({'n':n,'symbolic_values':values,'compiled_c_values':expected})

queries={
 'bad_false_accept':And(bad,Not(spec)),
 'bad_false_reject':And(spec,Not(bad)),
 'widened_false_accept':And(good_widened,Not(spec)),
 'widened_false_reject':And(spec,Not(good_widened)),
 'reject_everything_false_accept':And(false,Not(spec)),
 'reject_everything_false_reject':And(spec,Not(false)),
}
solver_results={}
solver_transcript=[]
for name,formula in queries.items():
    start=time.perf_counter()
    answer=satisfiable(formula,algorithm='dpll2')
    elapsed=time.perf_counter()-start
    if answer is False:
        saved={'result':'UNSAT','elapsed_seconds':elapsed,'raw_result':False}
    else:
        assignment={str(key):bool(value) for key,value in answer.items() if key in bits}
        n=sum((1<<i) for i,bit in enumerate(bits) if bool(answer.get(bit,False)))
        saved={'result':'SAT','elapsed_seconds':elapsed,'input_assignment':assignment,'decoded_n':n}
    solver_results[name]=saved
    solver_transcript.append({'query':name,'formula':str(formula),'raw_sympy_result':repr(answer),'result':saved})

not_the_255_assignment=Not(And(*bits))
remainder=satisfiable(And(queries['bad_false_accept'],not_the_255_assignment),algorithm='dpll2')
assert remainder is False
solver_transcript.append({'query':'remaining_bad_false_accept_after_excluding_255','formula':str(And(queries['bad_false_accept'],not_the_255_assignment)),'raw_sympy_result':repr(remainder),'result':{'result':'UNSAT'}})

sample=[0,1,2,3,4]
bad_false_accepts=[row['n'] for row in rows if row['bad'] and not row['mathematical_fits']]
bad_false_rejects=[row['n'] for row in rows if not row['bad'] and row['mathematical_fits']]
assert bad_false_accepts==[255] and bad_false_rejects==[]
assert all(row['widened']==row['mathematical_fits']==row['bound'] for row in rows)
assert solver_results['bad_false_accept']['decoded_n']==255
assert all(solver_results[name]['result']=='UNSAT' for name in ['bad_false_reject','widened_false_accept','widened_false_reject'])
assert solver_results['reject_everything_false_accept']['result']=='UNSAT'
assert solver_results['reject_everything_false_reject']['result']=='SAT'

result={
 'scope':'Original finite-domain 8-bit arithmetic specification and guard-only compiled C; SymPy propositional SAT, not SMT, not Rocq, not a vendor-library reproduction. No buffer writes are executed.',
 'domain':{'input_n':'integer payload byte length 0..255','input_boolean_bits':8,'capacity_bytes':8,'terminator_bytes':1,'mathematical_requirement':'n+1 <= 8 in unbounded arithmetic'},
 'c_semantics':'n+1 is promoted to int; converting the total to uint8_t maps 256 to 0. This conversion is defined modulo 256, not undefined signed overflow.',
 'sample_inputs':sample,
 'sample_rows':[rows[n] for n in sample],
 'boundary_rows':[rows[n] for n in [7,8,254,255]],
 'complete_domain_size':256,
 'bad_false_accepts':bad_false_accepts,
 'bad_false_rejects':bad_false_rejects,
 'widened_false_accepts':[],
 'widened_false_rejects':[],
 'full_compiled_c_vs_symbolic_model_comparison':{'rows':len(model_rows),'all_match':True},
 'sat_solver':{'library':'SymPy','version':sympy.__version__,'algorithm':'dpll2','kind':'propositional SAT','proof_certificate_exported_or_independently_checked':False,'queries':solver_results,'remaining_bad_false_accept_after_excluding_255':'UNSAT'},
 'environment':{'python':sys.version.split()[0],'gcc_version_first_line':subprocess.run([gcc,'--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],'installed_executables':{name:shutil.which(name) for name in ['rocq','coqc','lean','lake','z3','cvc5','boolector','gcc']}},
 'compile':{'command':compile_command,'exit_code':compiled.returncode,'stdout':compiled.stdout,'stderr':compiled.stderr},
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),
 'limitations':['Only this 0..255 length domain and fixed capacity 8 are checked.','The model does not execute real buffer writes, parse strings, model concurrency, or check a whole application.','The SAT solver result is a bounded propositional-model result, not a Rocq theorem or an independently checked proof certificate.','The C-to-Boolean correspondence is exhaustively checked on this finite domain; it is not a general verified compiler translation.','No claim is made about the 123 libraries or 239 entry points in the vendor research.'],
}
(root/'results.json').write_text(json.dumps(result,indent=2)+'\n')
(root/'symbolic-vs-c.json').write_text(json.dumps(model_rows,indent=2)+'\n')
(root/'all-256-cases.json').write_text(json.dumps(rows,indent=2)+'\n')
(root/'sat-output.json').write_text(json.dumps(solver_transcript,indent=2)+'\n')
summary={key:result[key] for key in ['scope','boundary_rows','bad_false_accepts','widened_false_accepts','full_compiled_c_vs_symbolic_model_comparison','sat_solver','environment']}
stdout=json.dumps(summary,indent=2)
(root/'run-demo.stdout.json').write_text(stdout+'\n')
names=['guard.c','run_demo.py','guard-demo','compiled-c-results.csv','all-256-cases.json','symbolic-vs-c.json','sat-output.json','results.json','run-demo.stdout.json']
manifest={name:{'bytes':(root/name).stat().st_size,'sha256':hashlib.sha256((root/name).read_bytes()).hexdigest()} for name in names}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(stdout)
