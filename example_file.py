import matplotlib.pyplot as plt
import numpy as np

from reaction import *

## Constants
# duplication kinetic rate
gamma = 1
# death kinetic rate
delta = 1
# initial number of A
IA = 50
# initial number of B
IB = 75
# Number of independant SCNs to use
NUM_SCN = 10000

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


print("running")
step = 0
while active:
    # NOTA: this 1-liner is *way* faster than a for loop (uses C implementation)
    [scn.step() for scn in active]
    active = [scn for scn in active if not stop_cond(scn)]
    # SUPPLEMENTARY CODE - display how many have stopped
    step += 1
    if step % 10 == 0:
        stopped = len(SCNs) - len(active)
        print(
            "\rstep %s - %5s/%5s stopped (%.1f%%)"
            % (step, stopped, len(SCNs), 100 * stopped / len(SCNs)),
            end="",
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
