Stochastic Folder
===================
This folder provides utilities for creating and running Stochastic Reaction Networks (SCNs)

# Files

The following files are defined:
- `reaction.py` provides all the utilities. Those are expressed in 3 classes, Reaction, SCNBuilder, and SCN
- `simul_AB.py` this files simulate the AB competing system. It can serves as an example on how to use `reaction.py`

# How to use - General Idea
The file `reaction.py` allows to do two important things that explain how it was design:
- define and create arbitrary SCN
- easily simulate a large number of identical SCNs to obtain average information on the scn, e.g. distribution functions of properties, expected values etc.

To fullfil those, the workflow is done in two main steps:
- define how the SCN works: what species, which reaction (with which rates), the initial counts of each species ...
This is achieved by the two classes Reaction and SCNBuilder
- actually make the SCNs and run them

Since the definition of the SCNs are programmatically distinc from the running of SCN, it is easy to use a single definiton shared between 10,000 of SCNs: they have the same reactions and *starting* species counts, but run independently

# How to use -Detailed Explanation
In this explaination, we will use `simul_AB.py` as an example

## Step 1 - Stochastic Chemical Network definition
### Step 1.1 - Reactions and species
The first step is to write the reactions that take place in the SCNs. The species are taken from the reactions (i.e. only species that may be consumed or produced are ever kept track on, and those are found automagically).
This is achived by the `Reaction` class in `reaction.py`. It takaes three arguments:
- The `rate` of the reaction, as a float
- The list of consummed species. Repeat a species multiple times if it is consumed multiple times. A list of string
- The list of produced species. Repeat a species mutliple times if it is consumed multiple times. A list of string

Let us look at simul_AB.py for example, adding commentaries

```python
# simul_AB.py

#import everuthing from reatcion.py to use it
# reaction.py must be in the same folder
from reaction import *

# define the duplication reaction A -> 2A at rate gamma
A_dup = Reaction(
    gamma, # constant defined at the start of the file, the reaction rate
    ["A"], # list of consumed species, A
    ["A", "A"] # list of produced species, 2A
)

# define the duplication B -> 2B at rate gamma (same as before)
# having a variable for gamma ensure the rates are the same
# structure is exactly as before
B_dup = Reaction(gamma, ["B"], ["B", "B"])

# define the death reaction A + B -> 0 at rate delta
death = Reaction(delta, ["A", "B"], [])

# The variables A_dup, B_dup and death now contains our reactions
```

#### Useful info on `Reaction` objects
The reaction object allows you to easily compute of access things related to the reaction

The following attributes are available:
- `re`: the mapping from reactants name to their stoechiometry.
> **Example**
>
> `A_dup.re` will give the list of reactant of the duplication of A reaction, mapped to their counts namely `{"A": 1}`
- `pr`: the mapping from products name to their stoechiometry.
> **Example**
>
> `B_dup.re` will give the list of products of the duplication of B reaction mapped to their count, namely `{"B": 2}`
- `species`: the set of involved species, irrespective of their stoechiometry
> **Example**
>
> `death.species` will yield the list of all species involved in the death reaction, namely `{"A", "B"}`

The following methods are available. When required, `counts` is a mapping from species names to their counts in the medium, e.g. the actual state of the SCN
- `is_valid(counts)`: returns if the reaction can take place, i.e. if their are enought reactants
- `propensity(volume, counts)`: returns a float, the propensity of the reaction given the state and the volume. This quantity comes straigh from the chemistry or reaction rate
- `apply(counts)`: **modifies** in-place `counts` to reflect that the reaction took place

### Step 1.2 - SCNBuilder and species starting counts
The second step is define the SCN: reactions, starting counts, volume. This is done in a SCNBuilder. You create one, add everuthing to it, and then you have a variable that contains the definition of the SCN and can make you thousands of copies of the SCN on demand

The class `SCNBuilder` (from `reaction.py`) is the thing to use. You first get a builder, then use methods `add_reaction()`, `set_volume()` and `set_count()` to define respectively the reactions, the volume and the starting counts for each species.
All the method returns the builder, so you can chain them

Let us look at `simul_AB.py` for an example
```python
# simul_AB.py

builder = SCNBuilder() # get the builder
builder.set_volume(1) # set the volume to 1 I.U.
builder.add_reaction(A_dup) # add the A duplication reaction
builder.add_reaction(B_dup) # add the duplication of B reaction
builder.add_reaction(death) # add the death reaction
builder.set_count("A", IA) # set the starting count of species A to the value of the variable `IA`
builder.set_count("B", IB) # set the starting count of species A to the value of the variable `IA`

# Method calls can be chained
# those familiar with Java will recognize the pattern
# the parenthesis tells python that this is a single line -- this is better that using \ at the end of each lines
builder = (
    SCNBuilder()
    .set_volume(1)  # 1mL = 1e-6L, respect S.I.
    .add_reaction(A_dup)
    .add_reaction(B_dup)
    .add_reaction(death)
    .set_count("A", IA)
    .set_count("B", IB)
)
# the variable builder now contains a definition of our SCN, that can create any number of them
```

## Step 2 - run the SCNs
The next step is to actually make the SCN and to run them. This is actually very easy:
- First, call the method `SCNBuilder.build()` to get an actual SCN object
- Second, go for a step using the `SCN.step()` method

Let us first look at a simple example, with two SCNs that are identical but independant

```python
# get two independant SCN from the definition above
scn_1 = builder.build()
scn_2 = builder.build()

# run them each for 10,000 steps
for _ in range(10000):
    scn_1.step()
    scn_2.step()

# look at the last 10 reaction that took place for each of them
print(scn_1.past[-10:0])
print(scn_2.past[-10:0])
```

In reality, if you need robust info on the SCN definition, for instance the distribution of the number of steps or the expected value of the number of step to terminate, you need to run more that 2 SCN, more in the 10,000 counts. This is what simul_AB.py does.

simul_AB.py uses a function, stop_cond, to test if a SCN is in a stop state: in our case, what is interesting is whether one of the species count is 0.
Then, it creates and run 10,000 SCNs and at each steps, stop running those that have terminated. They are still available in the `SCNs` variable.

> **NOTE**:
>
> When I wrote `simul_AB.py`, we didn't knew the SCN would always die. To prevent simulating them ad vitam aeternam, I used a maximum number of steps. This can be removed. See the example below to do that


> **NOTE**:
>
> `simul_AB.py` also has code to visualize the paths of the SCNs. Those are in `if plot:` code blocks and can be ingored

```python
# simul_AB.py

SCNs = [builder.build() for _ in range(10000)] # create 10,000 independant SCN that works the same
active = SCNs # intially, all SCNs are active

# define what it means for a single SCN to have finished
def stop_cond(scn):
    # SCN has finished if the count of A or B is 0
    return scn.mols["A"] == 0 or scn.mols["B"] == 0

# Run the SCN
# finite number of step version for 10,000 steps
# for _ in range(10,000):

# infinite version
while active: # this test if the list has a len > 0
    # make all active SCN do 1 step
    for scn in active:
        scn.step()
    
    # keep only unfinished scn into the active variable
    active = [scn for scn in active if not stop_cond(scn)]

# Now, active = [] (all SCNs have finished) and SCNs contains all the scns
```

If you'd like to get the number of steps required for each SCNs to reach the end state, you can do it like this.

```python
# extra code !

# distribution of stop time (number of steps to reach end state)
# mapping from stop_time -> number of SCN that required this stop time
# This is an empirical distribution, and will get closed to the real one
# with increasing numbers of SNCs simulated
distribution = {}
for scn in SCNs:
    # if undefine, start at 0
    # add 1 to the count of scn that reaquired len(scn.past) step to finish
    stop_time = len(scn.past)
    distribution[stop_time] = distribution.setdefault(stop_time, 0) + 1

# expected value
expected_stop_time = sum(stop_time * count for stop_time, count in distribution.items()) / sum(distribution.values())

## OPTIONAL
## histogram plot using matplotlib
import matplotlib.pyplot as plt

plt.hist([len(scn.past) for scn in SCNs], bins=range(min(distribution), max(distribution)+2))
plt.xlabel("stop time")
plt.ylabel("SCN count")
plt.title("Distribution of stop time for 10,000 SCNs\nexpected value:%s" % expected_stop_time)
plt.show()
```