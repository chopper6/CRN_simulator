from random import choices
import math, numpy as np


class Reaction:
	def __init__(self, rate, reactants, products):
		self.rate = rate
		self._re = {}
		self._pr = {}
		for r in reactants:
			self._re[r] = self._re.setdefault(r, 0) + 1
		for p in products:
			self._pr[p] = self._pr.setdefault(p, 0) + 1

	def __str__(self):
		return "%s -> %s" % (
			" + ".join(str(self._re[r]) + str(r) for r in self._re),
			" + ".join(str(self._pr[p]) + str(p) for p in self._pr) or "Ø",
		)

	def __repr__(self):
		return str(self)

	@property
	def re(self):
		return self._re.copy()

	@property
	def pr(self):
		return self._pr.copy()

	@property
	def species(self):
		return set(self._re.keys()) | set(self._pr.keys())

	def is_valid(self, counts):
		return all(counts[r] >= self._re[r] for r in self._re)

	def propensity(self, volume, counts):
		p = self.rate / pow(volume, len(self._re) - 1)
		for r in self._re:
			for k in range(self._re[r]):
				p *= counts[r] - k
		return p

	def apply(self, counts):
		for r in self._re:
			counts[r] -= self._re[r]
		for p in self._pr:
			counts[p] += self._pr[p]


class SCNBuilder:
	def __init__(self):
		self.v = None
		self.rxn = list()
		self.counts = {}
		self.species = set()
		self.events = []

	def set_volume(self, volume):
		self.v = volume
		return self

	def add_reaction(self, rx: Reaction):
		self.rxn.append(rx)
		self.species.update(rx.species)
		return self

	def add_event(self,event):
		# temporary solution
		# event = {'time':time_to_start, 'effect':function_to_call(self)}
		self.events += [event]
		return self

	def set_count(self, species, count):
		self.counts[species] = count
		if species not in self.species:
			print(f"WARN: unused species {species}")
		return self

	def build(self,params):
		if self.v is None:
			raise ValueError("No volume, cannot create SCN")
		if len(self.rxn) == 0:
			raise ValueError("No reactions, cannot create SCN")
		return SCN(self.v, self.rxn, self.counts, self.events,params)


class SCN:
	def __init__(self, volume, reactions, init_counts, events,params):
		self.rxn = list(reactions)
		self.v = volume
		self.mols = {
			k: init_counts.get(k, 0)
			for k in set().union(*(rx.species for rx in self.rxn))
		}
		self.past = []
		self.time = 0
		self.time_mean_appx = 0
		self.steps = 0
		self.events = events
		self.params=params


	def add_reaction(self, rx: Reaction):
		# used for an event during execution
		self.rxn.append(rx) # fix: assumes species of rxn are already in the SCN
		return self

	def step(self): 

		if self.events != []:
			for e in self.events:
				if self.time >= e['time']:
					e['effect'](self,self.params)
					self.events.remove(e)


		rxn = [rx for rx in self.rxn if rx.is_valid(self.mols)]
		try:
			rx = choices(rxn, weights=[rx.propensity(self.v, self.mols) for rx in rxn])[
				0
			]
		except IndexError:
			return


		if self.params['track_time']:
			lambd = sum([rx.propensity(self.v, self.mols) for rx in rxn])
			self.time += np.random.exponential(scale=1/lambd)
			self.time_mean_appx += 1/lambd

		rx.apply(self.mols)
		
		self.past.append(rx)
		self.steps +=1 

