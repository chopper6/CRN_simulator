import matplotlib.pyplot as plt, util
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, rcParams
import numpy as np


#COLORS = ['blue','magenta','purple','cyan','green','orange','brown','magenta','yellow','grey']
#COLORS = ['#cc0066', '#006699', '#ff9900', '#33cc33' ,'#9933ff']
#COLORS = ['#cc0066','#3333cc','#009933','#ff6600','#9966ff']
COLORS = ['#990099','#0033cc','#e60000']
LINESTYLES = [':','--','-.','-']

rcParams['font.family'] = 'serif'
#rcParams['font.sans-serif'] = ['Gadugi','Tahoma', 'DejaVu Sans','Lucida Grande', 'Verdana']

def tri(x,y,z,x_key,y_key,z_key, params, write_params_on_img=False):

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	surf = ax.plot_trisurf(x, y, z, cmap=cm.plasma)
	fig.colorbar(surf)

	ax.set_xlabel(x_key)
	ax.set_ylabel(y_key)
	ax.set_zlabel(z_key) 

	if write_params_on_img: 
		ax = plt.gca()
		cut = 80
		#ax.text(0,-.2,-1,'PARAMS' + str(params))
		plt.title('Parameters: ' + str(params)[:cut] + '\n' + str(params)[cut:2*cut] 
			+ '\n' + str(params)[2*cut:3*cut] + '\n' + str(params)[3*cut:],fontsize=6)

	fig.tight_layout()
	plt.grid(alpha=.2)

	if params['save_fig']:
		title = params['out_dir']+util.timestamp()+'_'+x_key+'_'+y_key+'_'+z_key+'.png'
		plt.savefig(title)
	else:
		plt.show()
	plt.clf()
	plt.cla()


def over_param_2ds(x_params, x_key, y_key, z_params,z_key, dataset, params, write_params_on_img=True, prediction=None):
	# should make clearer
	# z_params is the value of the parameter that is varied for each line plot

	plt.figure(1,[16,12])
	handles = []

	for i in util.rng(z_params):

		c = COLORS[i%len(COLORS)]

		y_avg = np.array(dataset.vals[y_key]['avg'])
		y_var = np.array(dataset.vals[y_key]['var'])

		y_max, y_min = np.array(dataset.vals[y_key]['max']), np.array(dataset.vals[y_key]['min'])
		y_max_sd, y_min_sd = np.array(dataset.vals[y_key]['max_sd']), np.array(dataset.vals[y_key]['min_sd'])

		plt.plot(x_params,y_avg,alpha=.8, linewidth=2, color=c)

		#top, btm = y_avg+y_var,y_avg-y_var
		top, btm = y_max_sd, y_min_sd
		#top,btm = y_max,y_min
		plt.fill_between(np.array(x_params),top,btm,alpha=.2, color=c)
		handles += ['Simulation']
		#handles += [z_key + ' = ' + str(z_params[i])]

	if prediction != None:
		plt.plot(x_params,prediction,alpha=.8, linewidth=2, color='black', linestyle='--' )
		handles += ['Prediction']


	#legend=plt.legend(handles, fontsize=14)
	#plt.setp(legend.get_title(),fontsize=16)

	plt.xlabel(x_key,fontsize=20)
	plt.xticks(fontsize=12)
	plt.ylabel(y_key,fontsize=20)
	plt.yticks(fontsize=12)

	if write_params_on_img: 
		ax = plt.gca()
		#ax.text(0,-.2,-1,'PARAMS' + str(params))
		plt.title('Parameters: ' + str(params)[:80] + '\n' + str(params)[80:160] + '\n' + str(params)[160:],fontsize=10)
	if params['save_fig']:
		title = params['out_dir']+util.timestamp()+'_'+x_key+'_'+y_key+'_'+z_key+'.png'
		plt.savefig(title)
	else:
		plt.show()
	plt.clf()
	plt.close()



def over_time_2ds(x_key, y_key, z_params,z_key, datasets, params, predictions=None):
	# z_params is the value of the parameter that is varied for each line plot

	# TODO:
	# rcparams for font
	# write_params_on_img as param
	# dpi

	plt.figure(1,[16,12])
	handles = []

	for i in util.rng(z_params):
		dataset = datasets[i]

		c = COLORS[i%len(COLORS)]
		linestyle = LINESTYLES[i%len(LINESTYLES)]


		x = np.array(dataset.vals[x_key]['avg'])
		y_avg = np.array(dataset.vals[y_key]['avg'])
		y_var = np.array(dataset.vals[y_key]['var'])

		y_max, y_min = np.array(dataset.vals[y_key]['max_conf']), np.array(dataset.vals[y_key]['min_conf'])

		plt.plot(x,y_avg,alpha=.8, linewidth=2, color=c, linestyle=linestyle)

		plt.fill_between(np.array(x),y_max,y_min,alpha=.2, color=c, linestyle=linestyle)
		handles += [z_key + ' = ' + str(z_params[i])]


	plt.grid(alpha=.2)
	plt.axhline(y=1, color='grey', linestyle='--', alpha=.5)

	legend=plt.legend(handles, fontsize=14)
	plt.setp(legend.get_title(),fontsize=16)

	#plt.xlabel(x_key,fontsize=20)
	plt.xlabel('Time',fontsize=20)
	plt.xticks(fontsize=12)
	#plt.ylabel(y_key,fontsize=20)
	plt.ylabel('Accuracy',fontsize=20)
	plt.yticks(fontsize=12)

	if params['write_params_on_img']: 
		ax = plt.gca()
		#ax.text(0,-.2,-1,'PARAMS' + str(params))
		plt.title('Parameters: ' + str(params)[:80] + '\n' + str(params)[80:160] + '\n' + str(params)[160:],fontsize=10)
	else:
		plt.title('Accuracy of NAND Gate with Amplifier', fontsize=20)
	if params['save_fig']:
		title = params['out_dir']+util.timestamp()+'_'+x_key+'_'+y_key+'_'+z_key+'.png'
		plt.savefig(title, dpi=300)
	else:
		plt.show()
	plt.clf()
	plt.close()




def avg_var_2d(x, x_key, y_key, dataset, params, write_params_on_img=True,title=None):
	# y_key must work for a variable

	assert(False) #poss refactor needed
	plt.figure(1,[16,12])


	y_avg = np.array(dataset.vals[y_key]['avg'])
	y_var = np.array(dataset.vals[y_key]['var'])

	plt.plot(x,y_avg,alpha=1, linewidth=3)

	top, btm = y_avg+y_var,y_avg-y_var

	plt.fill_between(np.array(x),top,btm,alpha=.15)

	plt.xlabel(x_key,fontsize=20)
	plt.xticks(fontsize=16)
	

	plt.ylabel(y_key,fontsize=20)
	plt.yticks(fontsize=16)

	if write_params_on_img: # haven't checked yet
		ax = plt.gca()
		ax.text(-.2,-.2,'PARAMS' + str(params))
	if params['save_fig']:
		title = params['out_dir']+util.timestamp()+'_'+x_key+'_'+y_key+'_'+z_key+'.png'
		plt.savefig(title)
	else:
		plt.show()
	plt.clf()
	plt.close()




def pr_ratio_3d(dataset, params, write_params_on_img=True):
	z = dataset.vals['probability off-diag']['avg']
	x = dataset.vals['steps']['avg']

	Ys = ['IB'] #TO ADD: 'gamma', 

	for y_key in Ys:
		y = dataset.params[y_key]

		title = 'Probability_by_steps_by_' + y_key

		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		#ax.scatter(x, y, dist, c='blue', marker='o', alpha=.8)
		surf = ax.plot_trisurf(x, y, z, cmap=cm.plasma)
		fig.colorbar(surf)

		ax.set_xlabel('# Steps')
		ax.set_ylabel('Gamma')
		ax.set_zlabel('Probability A/(A+B) > 3/4') #note that it is coded simply as > init, and init is 3/4

		if write_params_on_img: # haven't checked yet
			ax = plt.gca()
			ax.text(0,-.2,-1,'PARAMS' + str(params))

		fig.tight_layout()
		plt.title(title)
		plt.grid(alpha=.2)
		if params['save_fig']:
			title = params['out_dir']+util.timestamp()+'_'+x_key+'_'+y_key+'_'+z_key+'.png'
			plt.savefig(title)
		else:
			plt.show()
		plt.clf()
		plt.cla()



def bound_comparison(dataset, params, x_key, y_key, write_params_on_img=True):

	# TODO: change axis to reflect log10 nature (for all except for 'steps')

	dist_bound = ['dist from discrete bound','dist from continuous bound', 'steps','log time']

	for dist_name in dist_bound:
		dist = dataset.vals[dist_name]['avg']

		x, y = dataset.params[x_key], dataset.params[y_key]
		title = dist_name + '_by_' + x_key + '_by_' + y_key

		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		#ax.scatter(x, y, dist, c='blue', marker='o', alpha=.8)
		surf = ax.plot_trisurf(x, y, dist, cmap=cm.plasma)
		fig.colorbar(surf)

		ax.set_xlabel(x_key)
		ax.set_ylabel(y_key)
		ax.set_zlabel(dist_name)

		if write_params_on_img: # haven't checked yet
			ax = plt.gca()
			ax.text(0,-.2,-1,'PARAMS' + str(params))

		fig.tight_layout()
		plt.show()
		plt.clf()
		plt.cla()




def alpha_scaling(data, variables, legend_eles, params, write_params_on_img=True):
	for key in data.keys():
		plt.figure(1,[16,10])
		ax = plt.gca()
		
		plt.errorbar(variables['scale'], data[key]['avg'], yerr=data[key]['var'], linestyle="None",color='grey',alpha=.3,capsize=4, capthick=1)
		plt.scatter(variables['scale'], data[key]['avg'],color=variables['color'],alpha=.7)

		if key in ['time','time_appx']:
			plt.scatter(variables['scale'],variables['prediction'],color='black',alpha=1,marker="*")


		if write_params_on_img: # haven't checked yet
			ax = plt.gca()
			ax.text(0,-.2,'PARAMS' + str(params))

		plt.legend(handles=legend_eles)
		plt.xlabel('Scale')
		plt.ylabel(key)
		plt.title(key + ' by Alpha')
		plt.show()
		plt.clf()



