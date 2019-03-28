    ke_model_matrix     = np.array([  # Matrix that defines Element's Stiffness
    [ cos**2, 2, -(cos**2), -2],                  # 1 = cos²    | -1 = -cos²
    [ 2, 3, -2, -3],                  # 2 = cos*sin | -2 = -cos*sin
    [-(cos**2) ,-2,  cos**2,  2],                  # 3 = sin²    | -3 = -sin²
    [-2,-3,  2,  3]])

        ke_matrix_values = {              # Matrix that defines values in model_matrix
      1 : cos_squared,
     -1 : cos_squared_neg,
      2 : cos_times_sin,
     -2 : cos_times_sin_neg,
      3 : sin_squared,
     -3 : sin_squared_neg,
      4 : cos_pos,
     -4 : cos_neg,
      5 : sin_pos,
     -5 : sin_neg
      }
element.

#########################

import numpy as np

# MATRIZ PARA CADA ELEMENTO

EA_L = (element.elasticity_value * element.area)/length

c2 = element.cos**2
cs = element.cos * element.sen
s2 = element.sen**2

c2 *= EA_L
cs *= EA_L
s2 *= EA_L

ke_matrix = [	[c2, cs, -c2, -cs],
      			[cs, s2, -cs, -s2],
      			[-c2, -cs, c2, cs],
      			[-cs, -s2, cs, s2]]


x1 = element.node_1.degrees[0]
y1 = element.node_1.degrees[1]
x2 = element.node_2.degrees[0]
y2 = element.node_2.degrees[1]

ke_matrix[0][0] = [ke_matrix[0][0], x1, x1]
ke_matrix[0][1] = [ke_matrix[0][1], x1, y1]
ke_matrix[0][2] = [ke_matrix[0][2], x1, x2]
ke_matrix[0][3] = [ke_matrix[0][3], x1, y2]

ke_matrix[1][0] = [ke_matrix[1][0], y1, x1]
ke_matrix[1][1] = [ke_matrix[1][1], y1, y1]
ke_matrix[1][2] = [ke_matrix[1][2], y1, x2]
ke_matrix[1][3] = [ke_matrix[1][3], y1, y2]

ke_matrix[2][0] = [ke_matrix[2][0], x2, x1]
ke_matrix[2][1] = [ke_matrix[2][1], x2, y1]
ke_matrix[2][2] = [ke_matrix[2][2], x2, x2]
ke_matrix[2][3] = [ke_matrix[1][3], x2, y2]

ke_matrix[3][0] = [ke_matrix[3][0], y2, x1]
ke_matrix[3][1] = [ke_matrix[3][1], y2, y1]
ke_matrix[3][2] = [ke_matrix[3][2], y2, x2]
ke_matrix[3][3] = [ke_matrix[3][3], y2, y2]

print(ke_matrix)


#####################################################################
##### matriz global

# DEFINIR
number_of_nodes = 3 

#lista com todos os elementos = elementos

def matriz_global(elementos):
	global_matrix = np.zeros((number_of_nodes, number_of_nodes))

	for e in elementos:
		ke_matrix = e.matrix

		for line in ke_matrix:
			for c in line:
				global_matrix[c[1]][c[2]] += c[0]

	#global_matrix = np.multiply(10**8, global_matrix)


#####################################################################
####### Vetor global das forcas

global_list = []		#cond de contorno nao aplicadas
new_global_list = []	#cond de contorno aplicadas

#node.load = [x, y]   	---> formato do load dos nodes
#nodes = []				---> lista com todos os nodes da estrutura

for n in nodes:  #populando a lista completa
	global_list.append(n.load[0])
	global_list.append(n.load[1])


for n in nodes:  #populando a lista com as cond de controno aplicadas
	if(n != "x"): #so adiciona os termos numericos e conhecidos
		new_global_list.append(n.load[0])
		new_global_list.append(n.load[1])

new_global_vector = np.array(new_global_list)
global_vector = np.array(global_list)

#####################################################################
######  Aplicar as condicoes de contorno na matriz global

for i, item in enumerate(global_vector):
	if(item == "x"): #nos itens q tiverem com uma incognita significa q tem uma codicao de contorno (tira o index deles da matriz)
		new_global_matrix = numpy.delete(global_matrix, (i), axis=0)
		new_global_matrix = numpy.delete(new_global_matrix, (i), axis=1)


#####################################################################	
######  1 - resolver os sistemas de equacoes
'''
U_vector = np.linalg.solve(new_global_matrix, global_vector)
'''
######  2 - resolver os sistemas de equacoes por solucao numerica
U_vector = []

lte = 100
tol = 0.011

for i in range(len(global_vector)):
	X.append(0)

while(lte > 0 ):
	for i, item in enumerate(new_global_matrix):
		bi = global_vector[i]
		for l in range(len(item)):
			if(i == l):
				divisor = item[l]
			else:
				bi -= item[l] * U_vector[l] 

		U_vector[i] = bi/divisor

	lte -= 1

print(U_vector)

#####################################################################
###### completando o vetor U com os zeros

int index_u = 0
full_U_vector = []  #lista com os zeros e os valores encontrados

for i, item in enumerate(global_vector):
	if(item == "x"):
		full_U_vector.append(0)
	else:
		full_U_vector.append(U_vector[index_u])
		index_u += 1

#####################################################################
###### descobrindo o vetor de reacoes completo


full_global_vector = np.matmul(global_matrix, full_U_vector)




