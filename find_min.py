import numpy as np
import matplotlib.pyplot as plt


def f(q, i, l):
    if l <= i:
        raise ValueError("l <= i")
    return (
        i * (q ** (l + 2 - i)) / (l + 1)
        + q / (i + 1)
        + sum(i * (q ** k) / ((i + k) * (i + k - 1)) for k in range(2, l + 2 - i))
    )


for i in {5, 10, 15, 30, 50}:
    fig = plt.figure()
    for p in range(1, 4):
        for c in {7,5,3,1}:
            q = c * 10 ** (-p)
            X = np.array(range(i+1, i + 51))
            Y = np.fromiter((f(q, i, l) for l in X), dtype="float64")
            plt.plot(X, Y, label=f"q={q}")
    plt.title(f"i={i}")
    plt.legend()

plt.show()
