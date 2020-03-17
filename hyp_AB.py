from reaction import Reaction, SCNBuilder
import numpy as np
import matplotlib.colors as clr
import matplotlib.pyplot as plt

# activate plotting
plot = False


def sim(IA, IB):
    ## Constants
    # duplication kinetic rate
    gamma = 1
    # death kinetic rate
    delta = 0.1
    # hit rate
    alpha = 0.1
    # initial number of A
    #IA = 300
    # initial number of B
    #IB = IA+30
    # number of SCNs to simultaneously simulate
    trials = 10000
    # maximum number of steps
    steps = 10000
    # stopping condition function:
    # given an SCN as argument, it returns wether the SCN should be still simulated or if
    # it has reached the stopping conditions
    stop_cond = lambda scn: scn.mols["A"] <= 0 or scn.mols["B"] <= 0

    # Reactions definitions
    A_dup = Reaction(gamma, ["A"], ["A", "A"])
    B_dup = Reaction(gamma, ["B"], ["B", "B"])
    A_death = Reaction(delta, ["A"], [])
    B_death = Reaction(delta, ["B"], [])
    hit = Reaction(alpha, ["A", "B"], [])

    # Builder - helps building identical yet independent SCNs
    builder = (
        SCNBuilder()
        .set_volume(1)  # 1mL = 1e-6L, respect S.I.
        .add_reaction(A_dup)
        .add_reaction(B_dup)
        .add_reaction(A_death)
        .add_reaction(B_death)
        .add_reaction(hit)
        .set_count("A", IA)
        .set_count("B", IB)
    )

    ## Runtime variables
    SCNs = [builder.build() for _ in range(trials)]  # all scns
    actives = SCNs.copy()  # active SCNs - those which are still simulated
    stopped = 0
    A = B = 0


    if plot:
        ## Storing paths datas
        max_A = max_B = 0
        visit_data = {}  # data holder for paths display
        # conversion from a reaction to plotting info
        # id is the index at which to store the reaction count, dir is the x,y direction of it's arrow
        conv = {
            A_dup: {"id": 0, "dir": (1, 0)},
            B_dup: {"id": 1, "dir": (0, 1)},
            hit: {"id": 2, "dir": (-1, -1)},
            A_death: {"id": 3, "dir": (-1, 0)},
            B_death: {"id": 4, "dir": (0, -1)},
        }


    for i in range(1, steps + 1):
        if len(actives) <= 0:
            break
        print(f"step {i}: {len(actives)} SCN", end="", flush=True)
        ## saves previous states for latter plotting
        states = [(scn.mols["A"], scn.mols["B"]) for scn in actives]
        ## step
        any(scn.step() for scn in actives)

        ## save a count from the previous state for the applied reaction
        ## at the same time, calculate highest reached count - speeds up plotting
        if plot:
            for scn, s in zip(actives, states):
                l = visit_data.setdefault(s, [0, 0, 0])
                l[conv[scn.past[-1]]["id"]] += 1
                if scn.mols["A"] > max_A:
                    max_A = scn.mols["A"]
                if scn.mols["B"] > max_B:
                    max_B = scn.mols["B"]

        ## count number of SCNs who stopped because they have no A or B
        A += sum(1 for scn in actives if scn.mols["A"] <= 0)
        B += sum(1 for scn in actives if scn.mols["B"] <= 0)
        temp = [scn for scn in actives if not stop_cond(scn)]
        stopped += len(actives) - len(temp)
        print(
            f" --- {len(actives) - len(temp)} SCN stopped ({(len(actives) - len(temp)) / len(actives):.0%}), tot: {A} with no A, {B} with no B"
        )
        actives = temp

    print(
        f"""After {i - 1} steps, on {trials} different SCNs:
      {stopped} have reached stop_cond
      stopping probability: {stopped / trials}""")

    # to return
    return [A/(A + B), B/(A + B)]


if plot:
    ## PLOTTING
    # Get the data in numpy format now that the actual shape of the
    # array can be determined
    visit = np.zeros((max_A + 1, max_B + 1, 3), dtype="int64")
    for state, array in visit_data.items():
        visit[state[0], state[1]] = array
    # get filters, used after
    _filter = visit > 0
    # allocate scatter arrays
    size = np.sum(_filter)
    scatter_X = np.ndarray((size,))
    scatter_Y = np.ndarray((size,))
    scatter_U = np.ndarray((size,))
    scatter_V = np.ndarray((size,))
    scatter_C = np.ndarray((size,))
    pos = 0

    # Get helper arrays
    X, Y = np.meshgrid(range(max_A + 1), range(max_B + 1), indexing="ij")
    U = np.ones(X.shape)
    V = np.ones(Y.shape)

    # insert data into the allocated arrays
    for react, info in conv.items():
        lfilter = _filter[:, :, info["id"]]
        l = np.sum(lfilter)
        scatter_X[pos : pos + l] = X[lfilter].ravel()
        scatter_Y[pos : pos + l] = Y[lfilter].ravel()
        scatter_U[pos : pos + l] = info["dir"][0] * U[lfilter].ravel()
        scatter_V[pos : pos + l] = info["dir"][1] * V[lfilter].ravel()
        scatter_C[pos : pos + l] = visit[:, :, info["id"]][lfilter].ravel()
        pos += l

    arrows = plt.quiver(
        scatter_X,
        scatter_Y,
        scatter_U,
        scatter_V,
        scatter_C,
        angles="xy",
        scale_units="xy",
        scale=1,
        pivot="tail",
        width=0.003,
        cmap="viridis",
        norm=clr.LogNorm(vmin=scatter_C.min(), vmax=scatter_C.max()),
    )
    colorbar = plt.colorbar(arrows, extend="max")
    colorbar.set_label("reaction usage count", rotation=90)
    # plt.plot(X, Y, ".k", markersize=1)
    plt.grid()
    plt.plot(IA, IB, "Xr")
    # plt.xticks(range(max_A + 1))  # make x axis use integers
    # plt.yticks(range(max_B + 1))  # make y axis use integers
    plt.xlabel("species A count")
    plt.ylabel("species B count")
    plt.title(
        fr"Reaction counts for {trials} SCN during {steps} steps, with $\gamma$={gamma} and $\delta$ = {delta}"
    )
    plt.axis("scaled")  # force x and y axis to have same scale
    plt.show()
