import math

# gamma = birth rate
# delta = death rate
# m = min(A_0, B_0)   CHECK THIS

def discrete(gamma, delta,IA,IB):
	m = min(IA,IB)
	alpha = gamma/delta
	return (2*alpha + 1)*math.exp(alpha)*m


def continuous(gamma, delta,IA, IB):
	m = min(IA,IB)
	alpha = gamma/delta
	return math.exp(alpha)/delta * sum([1/math.pow(j,2) for j in range(1,m+1)])