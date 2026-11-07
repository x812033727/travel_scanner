# fix.py <locale> 'NN|text|say|emotion' ... : replace rows in lines/<locale>.txt
import sys
p=f'lines/{sys.argv[1]}.txt'
fix={a.split('|')[0]:a for a in sys.argv[2:]}
L=[fix.get(l.split('|')[0],l.rstrip('\n')) for l in open(p,encoding='utf-8')]
open(p,'w',encoding='utf-8').write('\n'.join(L)+'\n')
