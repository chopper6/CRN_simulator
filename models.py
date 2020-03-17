import numpy as np, math

import util, bounds
from reaction import *



################################# STOP CONDITIONS ##################################

# TRUE = STOP!
# FALSE = KEEP GOING

def speciesDeath(scn, params):
	for s in params['species']:
		if scn.mols[s]==0:
			return True
	return False

def stopTime(scn, params):
	if scn.time >= params['max_time']:
		return True
	else:
		return False

def stopSteps(scn, params):
	if scn.steps >= params['max_steps']:
		return True
	else:
		return False

def allCorrect(scn, params):
	if scn.mols[params['correct']] == 0:
		return False # no correct species currently
	elif scn.mols[params['incorrect']] == 0:
		return True # 100% correct
	else:
		return False

def mostCorrect(scn,params,most=.9):
	if scn.mols[params['correct']] == 0:
		return False # no correct species currently
	elif scn.mols[params['correct']]/ (scn.mols[params['correct']] + scn.mols[params['incorrect']]) >= most:
		return True # 100% correct
	else:
		return False

def dontStop(scn, params):
	return False

################################# EVENTS ######################################

def add_amplifier(scn,params):
	amp = Reaction(params['delta'], ['Y0','Y1'], [])
	scn.add_reaction(amp)


################################# MODELS ######################################

def AB(params):
	A_dup = Reaction(params['gamma'], ["A"], ["A", "A"])
	B_dup = Reaction(params['gamma'], ["B"], ["B", "B"])
	death = Reaction(params['delta'], ["A", "B"], [])

	builder = (
		SCNBuilder()
		.set_volume(1)  # 1mL = 1e-6L, respect S.I.
		.add_reaction(A_dup)
		.add_reaction(B_dup)
		.add_reaction(death)
		.set_count("A", params['IA'])
		.set_count("B", params['IB'])
	)

	SCNs = [builder.build(params) for _ in range(params['reps'])]

	stop_cond = params['stop_condition']

	return SCNs, stop_cond


def NAND(params):
	# PARAMS: gamma, delta, beta, consuming, reps, A0_t0, A1_t0, B0_t0, B1_t0

	rxns = []
	for y in ['Y0','Y1']:
		rxns += [Reaction(params['gamma'], [y], [y, y])]

	rxns += [Reaction(params['delta'], ['Y0','Y1'], [])]

	for s in ['A0','A1','B0','B1']:
		rxns += [Reaction(params['gamma'], [s], [s, s])]

	if params['consuming']:
		rxns += [Reaction(params['alpha'], ["A0","B0"], ["Y1"])]
		rxns += [Reaction(params['alpha'], ["A1","B0"], ["Y1"])]
		rxns += [Reaction(params['alpha'], ["A0","B1"], ["Y1"])]
		rxns += [Reaction(params['alpha'], ["A1","B1"], ["Y0"])]
	else:
		rxns += [Reaction(params['alpha'], ["A0","B0"], ["Y1","A0","B0"])]
		rxns += [Reaction(params['alpha'], ["A1","B0"], ["Y1","A1","B0"])]
		rxns += [Reaction(params['alpha'], ["A0","B1"], ["Y1","A0","B1"])]
		rxns += [Reaction(params['alpha'], ["A1","B1"], ["Y0","A1","B1"])]

	init_species = ['A0','A1','B0','B1']		

	builder = (
		SCNBuilder()
		.set_volume(1)  # 1mL = 1e-6L, respect S.I.
	)
	for r in rxns:
		builder.add_reaction(r)
	for s in init_species:
		builder.set_count(s, params[s+'_t0'])

	SCNs = [builder.build(params) for _ in range(params['reps'])]

	stop_cond = params['stop_condition'] #allCorrect #stopTime

	return SCNs, stop_cond


def NAND_sep_amp(params):

	rxns = []
	for y in ['Y0','Y1']:
		rxns += [Reaction(params['gamma'], [y], [y, y])]

	for s in ['A0','A1','B0','B1']:
		rxns += [Reaction(params['gamma'], [s], [s, s])]

	if params['consuming']:
		rxns += [Reaction(params['alpha'], ["A0","B0"], ["Y1"])]
		rxns += [Reaction(params['alpha'], ["A1","B0"], ["Y1"])]
		rxns += [Reaction(params['alpha'], ["A0","B1"], ["Y1"])]
		rxns += [Reaction(params['alpha'], ["A1","B1"], ["Y0"])]
	else:
		rxns += [Reaction(params['alpha'], ["A0","B0"], ["Y1","A0","B0"])]
		rxns += [Reaction(params['alpha'], ["A1","B0"], ["Y1","A1","B0"])]
		rxns += [Reaction(params['alpha'], ["A0","B1"], ["Y1","A0","B1"])]
		rxns += [Reaction(params['alpha'], ["A1","B1"], ["Y0","A1","B1"])]

	init_species = ['A0','A1','B0','B1']		
	amplifier_event = {'time':params['amp_time'], 'effect':add_amplifier}	

	builder = (
		SCNBuilder()
		.set_volume(1)  # 1mL = 1e-6L, respect S.I.
		.add_event(amplifier_event)
	)
	for r in rxns:
		builder.add_reaction(r)
	for s in init_species:
		builder.set_count(s, params[s+'_t0'])

	SCNs = [builder.build(params) for _ in range(params['reps'])]

	stop_cond = params['stop_condition'] #allCorrect #stopTime

	return SCNs, stop_cond
