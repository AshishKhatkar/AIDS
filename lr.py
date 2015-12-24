import math
import numpy as np
from scipy.optimize import fmin_bfgs

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
	grad = 1.0 / m * (hyT.dot(X))	
	return grad

def normalize(X):
	mu = np.mean(X, axis=0)
	smin = np.amin(X, axis=0)
	smax = np.amax(X, axis=0)
	return (((X - mu) * 1.0 / (smax - smin)) + 1) / 2.0

def predict(theta, X, kwargs={}):
	# print (kwargs)
	#for external calls
	if len(kwargs.items()):
		try:
			mean = kwargs['mean']
			maxv = kwargs['maxv']
			minv = kwargs['minv']
			mean = np.reshape(mean, len(X))
			maxv = np.reshape(maxv, len(X))
			minv = np.reshape(minv, len(X))
			theta = np.reshape(theta, len(X))
			# print (mean)
			# print (maxv)
			# print (minv)
			# print (X)
			X = (((X - mean) *1.0 / (maxv - minv) + 1) / 2.0)
			# print (X)
			print (sigmoid(X.dot(theta)))
			return (sigmoid(X.dot(theta)) >= 0.5)
		except (KeyError, ValueError) as e:
			print (e.__str__())
			print ("Error, please provide a dictionary with 'mean', 'maxv', 'minv' as keys with compatible arrays as values")
			return None
	#for calls within this file (for testing)
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
	
	mean = np.mean(X, axis=0)
	minv = np.amin(X, axis=0)
	maxv = np.amax(X, axis=0)

	X = normalize(X)
	theta = fmin_bfgs(f=compute_cost, x0=theta, fprime=compute_grad, args=(X, y), maxiter=400)

	x_test = test_data[:, :-1]
	x_test = normalize(x_test)
	y_test = test_data[:, -1]
	y_predict = predict(theta, x_test)

	accuracy = (1 - sum(np.absolute(y_predict - y_test)) / len(y_test)) * 100
	print("Test set accuracy is " + str(accuracy) + "%")

	# print(X)
	# print(y)

	# plot_data(theta, X, y)

	return theta, mean, minv, maxv
