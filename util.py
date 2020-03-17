import os, math
from datetime import datetime, date

def bool(x):
	if x in [0,'0','False',False,'false','unuh','noway','gtfofh']:
		return False
	elif x in [1,'1','True',True,'true','yeaya','fosho','nodoubt']:
		return True

def timestamp():
	now = datetime.now()
	curr_date = str(date.today()).strip('2020-')
	curr_time = str(datetime.now().strftime("%H-%M-%S"))
	tstamp = curr_date+'_'+curr_time
	return tstamp


def rng(x):
    return range(len(x))

def avg(x):
	return sum(x)/len(x)

def avg_by_key(X,key):
	summ = 0
	for x in X:
		summ += x[key]
	return summ/len(x)

def var_by_key(X,key):
	varr = 0
	the_avg = avg_by_key(X,key)
	for x in X:
		varr += math.pow(the_avg-x[key],2)
	return math.pow(varr/len(x),1/2)

def var(x,mean=None):
	if mean is None: mean = avg(x)
	var = avg([math.pow(mean-x[i],2) for i in rng(x)])
	return var


def check_build_dir(dirr):
    if not os.path.exists(dirr):
        print("\nCreating new directory for output at: " + str(dirr) + '\n')
        os.makedirs(dirr)

def safe_div_array(A,B):
	# a is numerator, b is divisor
	assert(len(A) == len(B))
	z=[]
	for i in rng(A):
		if B[i] == 0: z+=[0]
		else: z+=[A[i]/B[i]]
	return z


def get_timestamp():
	now = datetime.now()
	curr_date = str(date.today()).strip('2020-')
	curr_time = str(datetime.now().strftime("%H-%M-%S"))
	tstamp = curr_date+'_'+curr_time
	return tstamp