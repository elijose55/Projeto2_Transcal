#lte
#tol

K = [[1.59, -0.4, -0.54],
	[-0.4, 1.7, 0.4],
	[-0.54, 0.4, 0.54]]

F = [0, 150, -100]

X = []

lte = 70
tol = 0.011

for i in range(len(F)):
	X.append(0)

while(lte > 0 ):
	for i, item in enumerate(K):
		bi = F[i]
		for l in range(len(item)):
			if(i == l):
				divisor = item[l]
			else:
				bi -= item[l] * X[l] 

		X[i] = bi/divisor

	lte -= 1

print(X)

'''				
		if(((bi/divisor) - X[i])/(bi/divisor) < 0.011):
			break
'''