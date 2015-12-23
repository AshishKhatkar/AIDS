import numpy as np
import matplotlib.pyplot as pt

#dtype=['i8', 'f8', 'i8', 'i8', 'f8', 'i8', 'i8', 'i8']

data = np.loadtxt('training_data.csv', delimiter = ',')
print (data)

X = data[:, 0:-1]
y = data[:, -1]
psi = 1
usi = 4

pos = np.where(y == 1)
neg = np.where(y == 0)
print (pos)
print (neg)
pt.scatter(X[pos, psi], X[pos, usi], marker='+', c = 'b')
pt.scatter(X[neg, psi], X[neg, usi], marker='o', c = 'r')

pt.xlabel('pincode success rate')
pt.ylabel('user success rate')
pt.legend(['Deliver', 'No deliver'])
pt.show()
