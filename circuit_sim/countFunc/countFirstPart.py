# This script count all functions of the form:
# x1-----|---|-- o1
# x2 \   |   |
# x3 ----|---|-- o2
#
# The output is of the following form:
# It gives each calculated function in the format f(000) ... f(111)
# And the number of circuits that computes it


import itertools
import operator

def f(c,x):
	alpha1 = c[0][(x[0])]
	alpha2 = c[1][(x[1])+2*(x[2])]
	r1 = c[2][(alpha1)+2*(alpha2)]
	r2 = c[3][(alpha1)+2*(alpha2)]
	return str(r1)+str(r2)

f1 = list(itertools.product([0,1], repeat=2))
f2 = list(itertools.product([0,1], repeat=4))
g1 = list(itertools.product([0,1], repeat=4)) 
g2 = list(itertools.product([0,1], repeat=4))
poss = list(itertools.product(f1,f2,g1,g2))

what = {}

for c in poss:
	res = ""
	for b in list(itertools.product([0,1], repeat=3)):
		res += f(c,b)
	if not res in what:
		what[res] = 0
	what[res] += 1

what = sorted(what.items(), key=operator.itemgetter(1), reverse=True)
for f in what:
	print(f[0]+str(" ")+str(f[1]))