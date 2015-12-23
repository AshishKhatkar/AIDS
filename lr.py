import math
import numpy as np
from scipy.optimize import fmin_bfgs
from visualize import plot_data

def sigmoid(a):
	return 1 / (1 + math.e ** (-a))

def compute_cost(theta, X, y):
	"""
	compute cost for current theta
	"""
	h = sigmoid(X.dot(theta))
	#print(X.dot(theta))
	#print(theta)
	#print(X)
	m = len(X)
	yT = np.transpose(y)
	J = -1 / m * (yT.dot(np.log(h)) + (1 - yT).dot(np.log(1 - h)))
	#print(h)
	#print(m)
	return J

def compute_grad(theta, X, y):
	"""
	compute gradient for current theta
	"""
	h = sigmoid(X.dot(theta))
	hyT = np.transpose(h - y)
	m = len(X)
	grad = 1 / m * (hyT.dot(X))	
	return grad

def normalize(X):
	mu = np.mean(X, axis=0)
	smin = np.amin(X, axis=0)
	smax = np.amax(X, axis=0)
	return (X - mu) / (smax - smin)

def main():
	#print (sigmoid(0))
	data = np.loadtxt("training_data.csv", delimiter=',', dtype=float)
	data = np.random.permutation(data)
	useful_data = np.array([1, 2, 3, 4, 5, 6, 7])
	data = data[:, useful_data]
	X = data[:, :-1]
	y = data[:, -1]
	theta = np.random.uniform(0, 1, len(X[0]))
	
	X = normalize(X)
	theta = fmin_bfgs(f=compute_cost, x0=theta, fprime=compute_grad, args=(X, y), maxiter=400)

	plot_data(theta, X, y)

if __name__ == "__main__":
	main()
