import matplotlib.pyplot as plt
import numpy as np, math, pickle

import util, bounds, models
from reaction import *

def pickle_it(params, dataset):
	with open(params['out_dir'] + '/pickles/' + util.timestamp() + '_dump.pickle','wb') as file:
		data = {'dataset':dataset, 'params':params}
		pickle.dump(data, file) 



def one_param_mult_data_instances(model, dataset, params, verbose=True):

	SCNs, stop_cond_func = model(params)
	active = SCNs.copy()

	step = 0
	while active:

		[scn.step() for scn in active] 

		active = [scn for scn in active if not stop_cond_func(scn,params)]

		step+=1
		if step % params['plot_period'] == 0:
			dataset.add_instance(params, SCNs)




def one_param_one_data_instance(model,dataset, params, verbose=True):

	SCNs, stop_cond_func = model(params)
	active = SCNs.copy()

	step = 0
	while active:
		# NOTE: this 1-liner is *way* faster than a for loop (uses C implementation)
		[scn.step() for scn in active]
		active = [scn for scn in active if not stop_cond_func(scn, params)]

	dataset.add_instance(params, SCNs)

