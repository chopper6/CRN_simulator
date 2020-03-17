from util import avg, var,rng
import bounds
import math
import numpy as np
from scipy.stats import t, norm


def calc_3rd_moment(a, mean, std_dev):
	#pearson's didn't work: 
	#skew = avg([math.pow((a[i]-mean)/s,3) for i in rng(a)]) # expected skew*s

	#numer = avg([math.pow(x-mean,3) for x in a])
	numer = sum([math.pow(x-mean,3) for x in a])/len(a) # 3rd sample central moment
	return numer
	#denom = math.pow(  sum([math.pow(x-mean,2) for x in a]) / (len(a)-1)  ,  3/2)
	#denom = math.pow(std_dev,3) #same as above, but quicker
	#if denom==0:
	#	return 0
	#else:
	#	return numer/denom

def calc_std_dev(a, mean):
	# unclear if should / n-1 or / n ...
	s = math.pow(  sum([math.pow(x-mean,2) for x in a]) / (len(a)-1)  ,  1/2)
	return s

def all_stats(a, params):
	# includes asymmetric confidence intervals based on an altered t-test
	# from eqn 2.7 of https://www.jstor.org/stable/pdf/2286597.pdf
	# thanks to https://stats.stackexchange.com/questions/16516/
	a = np.array(a)
	mean = np.mean(a)
	variance = var(a)
	s = calc_std_dev(a, mean)
	N = len(a)

	conf_interval = params['conf_interval']
	if conf_interval == 'normal':

		normal_conf_interval = norm.interval(0.95, loc=mean, scale=s/math.sqrt(N))

		conf_min = normal_conf_interval[0]
		conf_max = normal_conf_interval[1]

	elif conf_interval == 'manual':
		# rm top 5% and btm 5%, take max
		num_trim = int(len(a)*.05) #from both sides
		a = np.sort(a)
		conf_min = min(a[num_trim:-num_trim])
		conf_max = max(a[num_trim:-num_trim])
		#print('\n',num_trim,'\n',conf_max, max(a),'\n', conf_min, min(a))

	elif conf_interval == 't-skewed':
		m3 = calc_3rd_moment(a, mean, s)
		alpha = .05
		t_val = t.ppf(1-alpha/2, N-1) # alpha/2 since two-tailed

		sym_conf = t_val * s / math.pow(N,1/2)
		if s == 0:
			asym_conf = 0
		else:
			asym_conf = m3 / (6*math.pow(s,2)*N)

		conf_min = mean - sym_conf + asym_conf
		conf_max = mean + sym_conf + asym_conf

	else:
		assert(False)
	
	if conf_min > mean or conf_max < mean:
		print('conf_min, conf_max',conf_min, conf_max)
		print('\nu,s',mean,s,'\na',a)
		#assert(False)



	return mean, variance, max(a), min(a), conf_max, conf_min

class Dataset:
	# params are independent variables of the model
	# values are functions of the dependent variables of the model

	def __init__(self,val_keys,params):

		self.params = {p:[] for p in params.keys()}
		stat = ['avg','var', 'max','min','max_conf','min_conf']
		self.vals = {v:{s:[] for s in stat} for v in val_keys}

	def add_instance(self,instance_params,SCNs):
		for p in self.params.keys():
			if p not in instance_params.keys():
				print(p)
				raise KeyError("Must include all parameter keys of initial Dataset.")
			self.params[p] += [instance_params[p]]
		for k in self.vals.keys():
			avg,var,maxx,minn,max_conf,min_conf = self.add_val(instance_params,SCNs,k)
			self.vals[k]['avg'] += [avg]
			self.vals[k]['var'] += [var] 
			self.vals[k]['max'] += [maxx]
			self.vals[k]['min'] += [minn] 
			self.vals[k]['max_conf'] += [max_conf] 
			self.vals[k]['min_conf'] += [min_conf] 

	def add_val(self, params, SCNs, val_key):

		# downside of this implementation is that don't know which characteristics are computed first
		# and have to recalc common things such as #steps and time
		# if too slow add a pre-feature calculation step

		################################## DISCRETE MODEL CHARACTERISTICS ##################################
		if val_key == 'steps':
			steps = [scn.steps for scn in SCNs]
			return all_stats(steps, params)

		elif val_key == 'probability off-diag':
			init = params['IA']/(params['IA']+params['IB'])
			As,Bs = [scn.mols['A'] for scn in SCNs], [scn.mols['B'] for scn in SCNs]
			pr = [As[i]/(As[i]+Bs[i]) > init for i in rng(As)]
			return all_stats(pr, params)

		elif val_key == 'Percent Y0':
			ratios = []
			for scn in SCNs:
				if scn.mols['Y0']==0: 
					ratios += [0]
				else:
					ratios += [scn.mols['Y0']/(scn.mols['Y0']+scn.mols['Y1'])]
			# faster if know that sum != 0:
			#ratios = [scn.mols['Y0']/(scn.mols['Y0']+scn.mols['Y1']) for scn in SCNs]
			return all_stats(ratios, params)

		elif val_key == 'dist from discrete bound':
			discrete_bound = bounds.discrete(params['gamma'], params['delta'],params['IA'],params['IB'])
			avg_steps = avg([scn.steps for scn in SCNs])
			return math.log(discrete_bound - avg_steps,10), None, None, None, None, None

		################################## CONTINUOUS MODEL CHARACTERISTICS ##################################
		elif val_key in ['time', 'Convergence Time']:
			stop_ts = [scn.time for scn in SCNs]
			return all_stats(stop_ts, params)

		elif val_key in ['time', 'Log Convergence Time']:
			stop_ts = [math.log(scn.time,10) for scn in SCNs]
			return all_stats(stop_ts, params)

		elif val_key == 'log time':
			stop_ts = [math.log(scn.time,10) for scn in SCNs]
			return all_stats(stop_ts, params)

		elif val_key == 'expected time': #appears to be the same as time, runs faster
			stop_ts = [scn.time_mean_appx for scn in SCNs]
			return all_stats(stop_ts, params)

		elif val_key == 'dist from continuous bound':
			cont_bound = bounds.continuous(params['gamma'], params['delta'],params['IA'],params['IB'])
			avg_t = avg([scn.time for scn in SCNs]) #note that curr using exact time, may go faster with expected time
			return math.log(cont_bound - avg_t,10), None, None, None, None, None



		else: 
			raise KeyError("Unrecognized value %s, use recognized value keys when initializing Dataset (see Dataset.add_val for existing options)." %(val_key))


