import numpy as np
import matplotlib.pyplot as pt

#dtype=['i8', 'f8', 'i8', 'i8', 'f8', 'i8', 'i8', 'i8']

def plot_data(theta, X, y, xind = 0, yind = 3):
	X = X[:1000, :]
	y = y[:1000]

	psi = xind
	usi = yind

	pos = np.where(y == 1)
	neg = np.where(y == 0)
	pt.scatter(X[pos, psi], X[pos, usi], marker='+', c = 'b')
	pt.scatter(X[neg, psi], X[neg, usi], marker='o', c = 'r')

	pt.xlabel('pincode success rate')
	pt.ylabel('user success rate')
	pt.legend(['Deliver', 'No deliver'])

	#plot decision boundary

	pt.show()
