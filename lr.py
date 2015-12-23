import math
import numpy as np
from scipy.optimize import fmin_bfgs
from visualize import plot_data

theta_global = np.zeroes(5)
minv = np.zeroes(5)
maxv = np.zeroes(5)
mean = np.zeroes(5)

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
	return (((X - mu) / (smax - smin)) + 1) / 2

def predict(theta, X, appcall=1):
	if (appcall):
		X = (((X - mean) / (maxv - minv) + 1) / 2)
		return (sigmoid(X.dot(theta_global)) >= 0.5)
	else:
		return (sigmoid(X.dot(theta)) >= 0.5)

def train():
	"""
	train the logistic regression model. 
	uses training_data.csv
	returns theta, mean, min, max
	"""
	data = np.loadtxt("training_data.csv", delimiter=',', dtype=float)
	data = np.random.permutation(data)
	#pincode success rate, theft, online_or_cod, success_rate, transaction_amt, successful_transaction, delivery
	useful_data = np.array([1, 2, 3, 4, 5, 6, 7])
	data = data[:, useful_data]

	train_data = data[:int(0.7 * len(data)), :]
	test_data = data[int(0.7 * len(data)):, :]

	X = train_data[:, :-1]
	y = train_data[:, -1]
	theta = np.random.uniform(0, 1, len(X[0]))
	
	X = normalize(X)
	theta = fmin_bfgs(f=compute_cost, x0=theta, fprime=compute_grad, args=(X, y), maxiter=400)

	x_test = test_data[:, :-1]
	x_test = normalize(x_test)
	y_test = test_data[:, -1]
	y_predict = predict(theta, x_test, 0)

	accuracy = (1 - sum(np.absolute(y_predict - y_test)) / len(y_test)) * 100
	print("Test set accuracy is " + str(accuracy) + "%")

	global mean = np.mean(X, axis=0)
	global minv = np.amin(X, axis=0)
	global maxv = np.amax(X, axis=0)
	global theta_global = theta
