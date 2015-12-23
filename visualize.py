from numpy import genfromtext, where
from pylab import scatter, show, legend, xlabel, ylabel

data = genfromtext('test.csv', delimiter=',')

X = data[:, 0:-1]
y = data[:, -1]
psi = 1
usi = 4

pos = where(y == 1)
neg = where(y == 0)
scatter(X[pos, psi], X[pos, usi], marker='+', c = 'b')
scatter(X[neg, usi], X[neg, usi], marker='o', c = 'r')

xlabel('pincode success rate')
ylabel('user success rate')
legend(['Deliver', 'No deliver'])
show()
