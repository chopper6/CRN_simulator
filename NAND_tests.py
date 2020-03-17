# Y1,Y0 not balanced to begin with
# so should aim to converge on the less likely Y0

# consuming: plot time & #steps to finish
# non-consuming: plot %Y0 after fixed # steps

# TODO: 
# add variable stop condition!
# add data pickling
# see plot_sweep for more
# fix dataset param_keys, curr depd on AB model
# in dataset.py: remove param key checking and just ensure that init == update for keys?

# LINGERING ISSUE:
# issue with current organization: which params are needed for which model is buried and scattered btwn files

# 2D: amplifier_duplication_rate/gate_speed x error
# 3D: z=error, y=amplifier_duplication_rate, x=gate_speed
# need x, y log on them plots

from dataset import *
import run_sweep, plot_sweep, models, copy
from util import *


##################################### FOR ALL TESTS ###################################
MODEL = models.NAND

err_rate = .25
total = 100
min_concen = int(err_rate*total)
maj_concen = total - min_concen


# had: max_time = 10, reps = 20-30
STANDARD_PARAMS = ({'consuming':False, 'gamma':.01, 'delta':.01, 'alpha':.01, 'reps':2000, 'max_time':1,
		'A1_t0':maj_concen, 'B1_t0':maj_concen, 'A0_t0':min_concen, 'B0_t0':min_concen, 'error_rate':err_rate,
		'plot_period':1, 'out_dir':'./output/', 'save_fig':False, 'correct':'Y0', 'incorrect':'Y1',
		'stop_condition':models.dontStop, 'amp_time':.1, 'track_time':True, 'write_params_on_img':True,
		'conf_interval':'manual'})


REALISTIC_PARAMS = ({'consuming':False, 'gamma':10**-2, 'delta':10**-13, 'alpha':10**-13, 'reps':100, 'max_time':1,
		'A1_t0':maj_concen, 'B1_t0':maj_concen, 'A0_t0':min_concen, 'B0_t0':min_concen, 'error_rate':err_rate,
		'plot_period':1, 'out_dir':'./output/', 'save_fig':True, 'correct':'Y0', 'incorrect':'Y1'})


def main():
	# each function below is an experiment, pick some and go
	#time_to_stop_3d()
	over_time_2d()
	print("\n\nDone.\n\n")




################################ SPECIFIC EXPERIMENTS #########################################



def Ypercent_3d():
	# appears to be depd on gate rxn rate, but not either duplication rates

	params = STANDARD_PARAMS

	output_gammas = [2**i for i in range(-4,5)]
	input_gammas = [2**i for i in range(-4,5)]
	betas = [2**i for i in range(-4,5)]
	#scale = [i for i in range(1,21)]

	val_keys = ['steps','Percent Y0','time']
	
	dataset = Dataset(val_keys,params)

	for i in rng(betas):
		#params['beta'] = betas[i]
		params['input_gamma'] = input_gammas[i]
		print("\rIteration %s of %s            " %(i, len(betas)),end="") 
		for j in rng(output_gammas):

			params['output_gamma'] = output_gammas[j]
			#params['delta'] = betas[j]

			run_sweep.one_param_one_data_instance(MODEL,dataset, params)


	run_sweep.pickle_it(params,dataset)
	z, z_key = dataset.vals['Percent Y0']['avg'], 'Percent Y0'

	#x, x_key = dataset.vals['steps']['avg'], '# Steps'
	x, x_key = dataset.params['input_gamma'], 'Input Duplication Rate'
	#x, x_key = dataset.params['beta'], 'Gate Reaction Rate'
	y, y_key = dataset.params['output_gamma'], 'Amplifier Duplication Rate'
	#y, y_key = dataset.params['delta'], 'Amplifier Death Rate'
	plot_sweep.tri(x,y,z,x_key,y_key,z_key, params, write_params_on_img=True)

	#x, x_key = dataset.vals['time']['avg'], 'Time'
	#plot_sweep.tri(x,y,z,x_key,y_key,z_key, params, write_params_on_img=True)


def time_to_stop_3d():

	params = STANDARD_PARAMS

	base_gamma = .001
	base_delta = 1
	params['delta'] = base_delta
	#scale = [i*.2 for i in range(1,9)]
	scale = [i for i in range(1,9)]
	# ofc high gamma, low delta might not stop at all
	# ofc high delta -> faster convergence 
	# ofc higher alpha -> faster convergence
	# ofc higher gamma -> slower convergence (but seems less relv than the others)
	# if gamma and alpha both occur via conjugation, set to same rates?

	val_keys = ['Convergence Time','Log Convergence Time']
	

	dataset = Dataset(val_keys,params)

	for i in rng(scale):
		params['gamma'] = base_gamma*scale[i]

		for j in rng(scale):

			print("\rIteration %s, %s of %s            " %(i+1,j+1, len(scale)),end="") 

			params['alpha'] = base_delta*scale[j]
			params['delta'] = base_delta*scale[j]

			run_sweep.one_param_one_data_instance(MODEL,dataset, params)


	run_sweep.pickle_it(params,dataset)

	z, z_key = dataset.vals['Convergence Time']['avg'], 'Convergence Time'
	x, x_key = dataset.params['gamma'], 'Gamma'
	#y, y_key = dataset.params['alpha'], 'Alpha'
	y, y_key = dataset.params['delta'], 'Alpha = Delta'
	plot_sweep.tri(x,y,z,x_key,y_key,z_key, params, write_params_on_img=True)

	z, z_key = dataset.vals['Log Convergence Time']['avg'], 'Log Convergence Time'
	plot_sweep.tri(x,y,z,x_key,y_key,z_key, params, write_params_on_img=True)



def over_time_2d():

	params = STANDARD_PARAMS

	val_keys = ['Percent Y0','time']
	params['stop_condition'] = models.stopTime
	
	l,h = .001,.1
	params['gamma'] = .01
	#gad = [[l,l],[l,h],[h,l],[h,h]]
	#gad = [[.001,.1],[.01,.01],[.1,.001]] #THIS
	gad = [[.001,.001,.1],[.001,.1,.001],[.1,.001,.001]] # AND THIS

	#gad = [[.01,.01,.1],[.01,.01,.2],[.01,.01,.25],[.01,.01,.28],[.01,.01,.3]]

	dsets= []
	for i in rng(gad):
		print("\rIteration %s of %s            " %(i, len(gad)),end="") 

		if False: # for variable err rate
			err_rate = gad[i][2]
			total = 100
			min_concen = int(err_rate*total)
			maj_concen = total - min_concen
			params['A1_t0'] = params['B1_t0'] = maj_concen
			params['A0_t0'] = params['B0_t0'] = min_concen
		

		params['alpha'] = gad[i][0]
		params['delta'] = gad[i][1]
		params['gamma'] = gad[i][2]
		dataset = Dataset(val_keys,params)

		run_sweep.one_param_mult_data_instances(MODEL,dataset, params)
		dsets += [dataset]

	run_sweep.pickle_it(params,dataset)
	legend_str = r'[$\alpha$, $\delta$, $\gamma$]'
	plot_sweep.over_time_2ds('time', 'Percent Y0', gad, legend_str, dsets, params)


def over_param_2d():

	params = STANDARD_PARAMS

	val_keys = ['time']
	params['stop_condition'] = models.mostCorrect

	OGs = [.001*i for i in range(1,21)]
	#OGs = [.1,1,10]
	base_gamma = 1
	val_keys = ['Convergence Time']
	dataset = Dataset(val_keys,params)

	for i in rng(OGs):
		print("\rIteration %s of %s            " %(i+1, len(OGs)),end="") 		
		params['delta'] = base_gamma*OGs[i]
		params['gamma'] = .01 + (.01 - base_gamma*OGs[i])/2
		params['alpha'] = .01 + (.01 - base_gamma*OGs[i])/2

		run_sweep.one_param_one_data_instance(MODEL,dataset, params)

	orig = dataset.vals['Convergence Time']['avg']

	run_sweep.pickle_it(params,dataset)
	plot_sweep.over_param_2ds(OGs,'Delta', 'Convergence Time', ['only one'], 'only one', dataset, params)


def scaling_prediction():

	params = STANDARD_PARAMS

	val_keys = ['time']
	params['stop_condition'] = models.mostCorrect

	OGs = [.01*i for i in range(1,21)]
	#OGs = [.1,1,10]
	base_gamma = 1
	val_keys = ['Convergence Time']
	dataset = Dataset(val_keys,params)
	prediction = []
	for i in rng(OGs):
		print("\rIteration %s of %s            " %(i+1, len(OGs)),end="") 		
		params['gamma'] = base_gamma*OGs[i]
		params['alpha'] = base_gamma*OGs[i]
		params['delta'] = base_gamma*OGs[i]

		run_sweep.one_param_one_data_instance(MODEL,dataset, params)

	orig = dataset.vals['Convergence Time']['avg']
	prediction = [orig[0]] + [orig[0]*(OGs[0]/OGs[i]) for i in range(1,len(OGs))]

	run_sweep.pickle_it(params,dataset)
	plot_sweep.over_param_2ds(OGs,'gamma = alpha = delta', 'Convergence Time', ['only one'], 'only one', dataset, params, write_params_on_img=True,prediction=prediction)


main()


