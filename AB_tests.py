#####################################################
#													#
#	A series of CRN experiments on the AB model		#
#													#
#													#
#													#
#####################################################

from dataset import *
import run_sweep, plot_sweep,util, models


# GAMMA = BIRTH
# DELTA = DEATH

MODEL = models.AB


STANDARD_PARAMS = ({'gamma':1, 'delta':1, 'reps':400, 'max_time':None,'species':['A','B'],'IA':1000,'IB':1000,
		'plot_period':1, 'out_dir':'./output/', 'save_fig':False,'track_time':True,
		'stop_condition':models.speciesDeath})

def main():
	# each function below is an experiment, pick some and go
	time_to_stop_3d()
	print("\n\nDone.\n\n")



def time_to_stop_3d():

	params = STANDARD_PARAMS

	base_gamma = 1
	base_delta = 1
	scale = [i*100 for i in range(1,11)]

	val_keys = ['Convergence Time','Log Convergence Time']
	
	dataset = Dataset(val_keys,params)

	for i in rng(scale):
		params['IA'] = base_gamma*scale[i]

		for j in rng(scale):

			print("\rIteration %s, %s of %s            " %(i+1,j+1, len(scale)),end="") 

			params['IB'] = base_delta*scale[j]

			run_sweep.one_param_one_data_instance(MODEL,dataset, params)


	run_sweep.pickle_it(params,dataset)

	z, z_key = dataset.vals['Convergence Time']['avg'], 'Convergence Time'
	x, x_key = dataset.params['IA'], 'A_0'
	#y, y_key = dataset.params['alpha'], 'Alpha'
	y, y_key = dataset.params['IB'], 'B_0'
	plot_sweep.tri(x,y,z,x_key,y_key,z_key, params, write_params_on_img=True)

	z, z_key = dataset.vals['Log Convergence Time']['avg'], 'Log Convergence Time'
	plot_sweep.tri(x,y,z,x_key,y_key,z_key, params, write_params_on_img=True)


	z, z_key = dataset.vals['Convergence Time']['min_sd'], 'Convergence Time within 3 Std Devs'
	plot_sweep.tri(x,y,z,x_key,y_key,z_key, params, write_params_on_img=True)

	z, z_key = dataset.vals['Log Convergence Time']['min_sd'], 'Log Convergence Time within 3 Std Devs'
	plot_sweep.tri(x,y,z,x_key,y_key,z_key, params, write_params_on_img=True)







################### PROBABLY HAVE TO REFACTOR THESE ####################
def prob_ratio():

	params = {}
	params['gamma'], params['delta'],params['reps'] = 1,0,1000
	max_iter = 10000
	period = 100
	IA_base = 3
	IB_base = 1
	scale = [i for i in range(10,21)]

	val_keys = ['steps','probability off-diag']
	
	dataset = Dataset(val_keys)

	for i in util.rng(scale):
		print("\rScale is %s of %s            " %(i, len(scale)),end="") 

		params['IA'] = IA_base*scale[i]
		params['IB'] = IB_base*scale[i]

		run_sweep.one_param_mult_data_instances(MODEL,dataset, params, period, max_iter)

	plot_sweep.pr_ratio_3d(dataset, params, write_params_on_img=False)


def IA_IB_bound_dist():

	params = {}
	As = [i for i in range(1,16)]
	Bs = [i for i in range(1,16)]
	params['gamma'], params['delta'],params['reps'] = 1,1,100

	val_keys = ['dist from continuous bound','dist from discrete bound','steps','log time']
	
	dataset = Dataset(val_keys)

	for i in util.rng(As):
		params['IA'] = As[i]

		for j in util.rng(Bs):
			params['IB'] = Bs[j]

			run_sweep.one_param_one_data_instance(MODEL, dataset, params, verbose=True)

	plot_sweep.bound_comparison(dataset, params, 'IA','IB', write_params_on_img=False)


def gamma_delta_bound_dist():

	params = {}

	gammas = [i for i in range(1,16)]
	deltas = [i for i in range(1,16)]
	params['IA'], params['IB'],params['reps'] = 10,10,1000

	val_keys = ['dist from continuous bound','dist from discrete bound','steps','log time']

	dataset = Dataset(val_keys)

	for i in util.rng(gammas):
		params['gamma'] = gammas[i]

		for j in util.rng(deltas):
			params['delta'] = deltas[j]

			run_sweep.one_param_one_data_instance(MODEL, dataset, params, verbose=True)

	plot_sweep.bound_comparison(dataset, params, 'gamma','delta', write_params_on_img=False)




def alpha_test():

	# TODO: refactor this

	DELTA_INSTEAD = False # just check gamma, delta symmetry

	base_gammas, base_delta, IA, IB, repitions = [.1,10,20],1,80,60,1000

	if DELTA_INSTEAD: 
		base_deltas, base_gamma = [1,4,8],1

	COLORS = ['blue','red','green','purple','cyan','orange','brown','magenta','yellow','grey']

	dkeys = ['steps','time','time_appx']
	vkeys = ['scale','color','prediction']

	data = {k:{'avg':[],'var':[]} for k in dkeys}
	variables = {k:[] for k in vkeys}

	legend_eles = []

	for i in util.rng(base_gammas):
		if DELTA_INSTEAD: 
			base_delta = base_deltas[i]
		else:
			base_gamma = base_gammas[i]
		color = COLORS[i]
		legend_eles += [Line2D([0], [0], color=color, lw=4, label='base gamma = ' + str(base_gamma))]
	    #Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor='g', markersize=15),


		for j in range(1,10):
			
			print("\rBase gamma = %s, scale = %s" %(base_gamma, j),end="") 

			gamma, delta = base_gamma*j, base_delta*j
			one_data = run_sweep.run_one_param(gamma, delta, IA, IB, repitions)

			variables['scale'] += [j]
			variables['color'] += [color]
			for k in one_data.keys():
				data[k]['avg'] += [one_data[k]['avg']]
				data[k]['var'] += [one_data[k]['var']]

			if j==1:
				variables['prediction'] += [one_data['time']['avg']]
				base_t = one_data['time']['avg']
			else:
				variables['prediction'] += [1/j * base_t]


	params = base_gammas, base_delta, IA, IB, repitions
	plot_sweep.features(data,variables, legend_eles, params, write_params_on_img=True)




main()