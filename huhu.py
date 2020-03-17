from hyp_AB import sim

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt

tosim = False

X = []
if tosim:
	for N in [ 30, ]:
		for delta in [10]:
			IA = int( (N + delta)/2 )
			IB = N - IA
			X += [ [IA, IB, sim(IA, IB)[0]] ]

	print(X)

else:
	# from previous simulations of the above code

	# small IA, IB numbers
	X = [[10, 10, 0.5101489851014899], [10, 11, 0.6127], [10, 12, 0.7202], [10, 13, 0.8061], [10, 14, 0.8728], [10, 15, 0.9157], [10, 16, 0.9533], [10, 17, 0.9677], [10, 18, 0.9834], [10, 19, 0.9891], [11, 10, 0.387], [11, 11, 0.499], [11, 12, 0.6151], [11, 13, 0.7176], [11, 14, 0.8033], [11, 15, 0.8645], [11, 16, 0.9093], [11, 17, 0.9492], [11, 18, 0.9644], [11, 19, 0.9826], [12, 10, 0.2846], [12, 11, 0.3888], [12, 12, 0.5061], [12, 13, 0.6128], [12, 14, 0.7193], [12, 15, 0.7968], [12, 16, 0.8564], [12, 17, 0.9076], [12, 18, 0.9398], [12, 19, 0.9646], [13, 10, 0.1962803719628037], [13, 11, 0.2774], [13, 12, 0.3932], [13, 13, 0.5119], [13, 14, 0.6021], [13, 15, 0.7108], [13, 16, 0.7863], [13, 17, 0.8518], [13, 18, 0.8992], [13, 19, 0.9381], [14, 10, 0.1311], [14, 11, 0.1971], [14, 12, 0.2962], [14, 13, 0.395], [14, 14, 0.502], [14, 15, 0.6003], [14, 16, 0.6964], [14, 17, 0.7736], [14, 18, 0.8533], [14, 19, 0.8972], [15, 10, 0.0804], [15, 11, 0.1378], [15, 12, 0.2022], [15, 13, 0.2916], [15, 14, 0.393], [15, 15, 0.5088], [15, 16, 0.6019], [15, 17, 0.6961], [15, 18, 0.78], [15, 19, 0.8442], [16, 10, 0.0465], [16, 11, 0.0878], [16, 12, 0.1451], [16, 13, 0.2091], [16, 14, 0.303], [16, 15, 0.3941], [16, 16, 0.4931], [16, 17, 0.606], [16, 18, 0.7025], [16, 19, 0.7721], [17, 10, 0.0279], [17, 11, 0.0573], [17, 12, 0.0907], [17, 13, 0.1518], [17, 14, 0.2206], [17, 15, 0.3061], [17, 16, 0.4021], [17, 17, 0.5025], [17, 18, 0.5895], [17, 19, 0.6794], [18, 10, 0.0162], [18, 11, 0.0311], [18, 12, 0.0567], [18, 13, 0.0955], [18, 14, 0.1536], [18, 15, 0.2236], [18, 16, 0.3061], [18, 17, 0.4055], [18, 18, 0.5021], [18, 19, 0.5975], [19, 10, 0.0081], [19, 11, 0.0188], [19, 12, 0.0338], [19, 13, 0.0665], [19, 14, 0.1021], [19, 15, 0.1554], [19, 16, 0.2271], [19, 17, 0.30196980301969806], [19, 18, 0.408], [19, 19, 0.4989]]

	ext = [[20, 10, 0.0049], [21, 9, 0.0007], [21, 9, 0.0012], [22, 8, 0.0001], [22, 8, 0.0001]]
	
	# extending to larger numbers
	ext += [[25, 25, 0.4944], [26, 24, 0.3283], [29, 21, 0.0344], [50, 50, 0.5024], [51, 49, 0.35], [54, 46, 0.0707], [75, 75, 0.4999], [76, 74, 0.3605], [79, 71, 0.0793], [100, 100, 0.4897], [101, 99, 0.3719], [104, 96, 0.0982], [125, 125, 0.5012], [126, 124, 0.3814], [129, 121, 0.1071], [150, 150, 0.4929], [151, 149, 0.3889], [154, 146, 0.121], [175, 175, 0.5038], [176, 174, 0.3842], [179, 171, 0.1272], [200, 200, 0.4953], [201, 199, 0.3924], [204, 196, 0.1351], [225, 225, 0.4991], [226, 224, 0.3872], [229, 221, 0.1387]]
	
	# and very large ones
	ext += [[500, 500, 0.5066], [501, 499, 0.4044], [504, 496, 0.1651]] + [[500, 500, 0.5006], [501, 499, 0.4108], [502, 498, 0.3139], [502, 498, 0.315], [503, 497, 0.2302], [503, 497, 0.229], [504, 496, 0.1629], [505, 495, 0.1126], [505, 495, 0.1111]] + [[506, 494, 0.0731], [506, 494, 0.0738], [507, 493, 0.0451], [507, 493, 0.0469]]

	# add all
	X += ext

	# because of symmetry with IA, IB
	# (attention this assumes that all terminated in sim)
	X += [ [x[1], x[0], 1 - x[2]] for x in ext ]


# filter (display in red those with diff 0,3,9)
Xf = [x for x in X if x[0] - x[1] in [0, 3, -3, 9, -9] ]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# plot all
xdata = [a[0] for a in X]
ydata = [a[1] for a in X]
zdata = [a[2] for a in X]
ax.scatter(xdata, ydata, zdata, marker='*', color='b')

# plot filtered ones red
xdataf = [a[0] for a in Xf]
ydataf = [a[1] for a in Xf]
zdataf = [a[2] for a in Xf]
ax.scatter(xdataf, ydataf, zdataf, marker='*', color='r')


# plot with absolute diff as x
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

X_30 = [x for x in X if x[0] + x[1] == 30]
X_1000 = [x for x in X if x[0] + x[1] == 1000]

xdata_30 = [a[0]-a[1] for a in X_30]
zdata_30 = [a[2] for a in X_30]
xdata_1000 = [a[0]-a[1] for a in X_1000]
zdata_1000 = [a[2] for a in X_1000]

ax2.plot(xdata_30, zdata_30, '*', color='b')
ax2.plot(xdata_1000, zdata_1000, 'x', color='r')

plt.savefig("diff.svg")

# plot with IA/N as x
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)

X_30 = [x for x in X if x[0] + x[1] == 30]
X_1000 = [x for x in X if x[0] + x[1] == 1000]

xdata_30 = [( a[0] )/30 for a in X_30]
zdata_30 = [a[2] for a in X_30]
xdata_1000 = [( a[0] )/1000 for a in X_1000]
zdata_1000 = [a[2] for a in X_1000]

ax3.plot(xdata_30, zdata_30, '*', color='b')
ax3.plot(xdata_1000, zdata_1000, 'x', color='r')

plt.savefig("diffrel.svg")


plt.show()
