"""
Exact same thing as example_file.py, but using multiple cores
"""
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing

from reaction import *

## Constants
# Number of cores - can be very high on clusters
CORES = 6
# duplication kinetic rate
gamma = 1
# death kinetic rate
delta = 1
# initial number of A
IA = 75
# initial number of B
IB = 75
# Number of independant SCNs to use
# NOTA: here, just use more SCNs to get more accurate results
# One can also increase IA and IB and use parallelism to run longer simulation
NUM_SCN = CORES * 10000

# STEP 1.1 - Define Reaction
A_dup = Reaction(gamma, ["A"], ["A", "A"])
B_dup = Reaction(gamma, ["B"], ["B", "B"])
death = Reaction(delta, ["A", "B"], [])

# STEP 1.2 - Define SCN
builder = (
    SCNBuilder()
    .set_volume(1)  # 1mL = 1e-6L, respect S.I.
    .add_reaction(A_dup)
    .add_reaction(B_dup)
    .add_reaction(death)
    .set_count("A", IA)
    .set_count("B", IB)
)

# STEP 2 - Run SCNs
SCNs = [builder.build() for _ in range(NUM_SCN)]
active = SCNs.copy()


def stop_cond(scn):
    return scn.mols["A"] == 0 or scn.mols["B"] == 0


## PARALLEL DIFFERENCES
# Create a function to run a list of SCN
def run_scns(scn_list):
    active = scn_list
    while active:
        [scn.step() for scn in active]
        active = [scn for scn in active if not stop_cond(scn)]
    return scn_list


# Create a function to split the list of SCNs into CORES lists
def split_list(lst, count):
    buckets = [len(lst) // count] * count
    for i in range(len(lst) % count):
        buckets[i] += 1
    edges = [0]
    for bucket in buckets:
        edges.append(edges[-1] + bucket)
    return [lst[edges[i] : edges[i + 1]] for i in range(count)]


# Create a Pool of workers, make them each run part of the SCNs
with multiprocessing.Pool(CORES) as pool:
    results = pool.map(run_scns, split_list(SCNs, CORES))

# Result is a list of list
# Recover a single list by fusing all the list
SCNs = sum(results, [])
## END PARALLE DIFFERENCES

# STEP 3 - analysis
## Distribution
distribution = {}
for scn in SCNs:
    stop_time = len(scn.past)
    distribution[stop_time] = distribution.setdefault(stop_time, 0) + 1
expected_stop_time = sum(
    stop_time * count for stop_time, count in distribution.items()
) / sum(distribution.values())

## Time upper bound
alpha = gamma / delta
upper_bound = (2 * alpha + 1) * np.exp(alpha) * min(IA, IB)
upper_bound_cont = (
    np.exp(alpha) / delta * sum(j ** (-2) for j in range(1, min(IA, IB) + 1))
)

# STEP 3 - analysis
## Distribution
distribution = {}
for scn in SCNs:
    stop_time = len(scn.past)
    distribution[stop_time] = distribution.setdefault(stop_time, 0) + 1
expected_stop_time = sum(
    stop_time * count for stop_time, count in distribution.items()
) / sum(distribution.values())

## Time upper bound
alpha = gamma / delta
upper_bound = (2 * alpha + 1) * np.exp(alpha) * min(IA, IB)

# STEP 4 - Plot
plt.hist(
    [len(scn.past) for scn in SCNs],
    bins=range(min(distribution), max(distribution) + 2),
    label="Stop time distribution",
    color="blue",
    align="left"
)
plt.axvline(x=upper_bound, label="Upper bound", color="red")
plt.axvline(x=max(distribution.keys()), color="green", label="Empirical maximum")
plt.xlabel("stop time")
plt.ylabel("SCN count")
plt.title(
    "Distribution of stop time for %s SCNs\nE=%.2E\nMAX=%.2E"
    % (NUM_SCN, expected_stop_time, upper_bound)
)
plt.legend()
plt.show()
