# fix.py <locale> 'id | text | say | emotion' ... : replace those rows in <locale>.txt
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
f = f'{here}/{sys.argv[1]}.txt'
fix = {r.split('|')[0].strip(): r for r in sys.argv[2:]}
L = open(f, encoding='utf-8').read().splitlines()
L = [fix.pop(x.split(' ')[0], x) for x in L]
assert not fix, fix
open(f, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
