import numpy as np
import random

#----------------------------------------- Clases ------------------------------------------
class Tree:
	def __init__(self,position,age=0.):
		self.position=position 
		self.age=age
		self.infected=False
		self.diaphorina_amount=0.

		#Métodos
	def infection(self):#Sortea si un árbol sano se infecta o no
		if infected==False:#if el árbol está sano
			try:
				infection_probability=1.-diaphorina_amount**(-1./2.) #calculamos la probabilidad de contagio en función de las diaforinas
			except:
				infection_probability=0 #La probabilidad infección no depende precisamente del número de diaforinas, sino del número de diaforinas infectadas
			if random.random()<infection_probability:#si un número aleatorio es menor que esa probabilidad, se contagia
				infected=True
class Diaphorina:
	def __init__(self,tree=None):#tree=none es como pass para variables
		self.tree=tree
	
		#Métodos
	def flight_to(self,tree):#?
		self.tree=tree#pass?
	def random_flight(self,list_tree):#Elige aleatoriamente un elemento de la lista de árboles
		self.tree=random.choice(list_tree)#Hay problema con que no haya sido definida aún esta lista?
class Field:
	def __init__(self,size=(100,100)):
		self.size=size
		self.positions_matrix=np.zeros(size)#The function zeros creates an array full of zeros
		forestlist_generator=[]
		for i in range(size[0]):
			forestlist_generator.append([])
			for j in range(size[1]):
				forestlist_generator[i].append(None)
		self.forestlist=list(forestlist_generator)	
	
		#Métodos
	def add_tree(self,tree):#Agrega un árbol en una posoción dada  
		if self.positions_matrix[tree.position[0],tree.position[1]]==0:#-sólo si esta está vacía-
			self.forestlist[tree.position[0]][tree.position[1]]=tree#al forestlist
			self.positions_matrix[tree.position[0],tree.position[1]]=1#y ocupa la casilla en positions_matrix.
		else:#Si no está vacía, entonces pass. Esto para evitar borrar accidentalmente
			pass#Se hará un código para el método replace_tree() y para delete_tree().
	def delete_tree(self, position, tree=None): 
		if tree!=None:#Si se da árbol, borra el árbol tree con delete_tree(None, tree)
			self.forestlist[tree.position[0]][tree.position[1]]=None
			self.positions_matrix[tree.position[0],tree.position[1]]=0
		else:#o el árbol en (a, b) con delete_tree((a,b))
			self.forestlist[position[0]][position[1]]=None
			self.positions_matrix[position[0], position[1]]=0		
	
	'''En construcción: def replace_tree(self, old_tree, new_tree):
			self.delete_tree(old_tree)
			self.add_tree(new_tree)'''
	
	def fill(self, age, diaphorina_amount, infected=False):#Nos llena el campo con árboles aleatorios
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				random_tree=Tree((i,j), age)
				random_tree.diaphorina_amount=diaphorina_amount
				if infected==True:
					random_tree.infection()
				self.forestlist[i][j]=random_tree
				self.positions_matrix[i,j]=1
				'''print(self.forestlist[i][j])
				print(self.positions_matrix[i,j])'''
	'''En construcción: def add_random_trees(self,Number_of_trees):
		field_width=self.size[0]
		field_height=self.size[1]
		x = np.random.randint(field_width, size=Number_of_trees)
		y = np.random.randint(field_height, size=Number_of_trees)
		list_to_add=[Tree((x,y)) for x,y in zip(x,y)]
		self.trees.append(list_to_add)
	Quité momentáneamente este método porque los campos comerciales no tienen  árboles distribuidos aleatoriamente, 
	están siempre en cuadrículas llenas, quizás en los traspatios sí lo estén, 
	'''
#-------------------------- Creación de Objetos --------------------------------

#Campo uno y métodos básicos
'''
field_1=Field((20,6))

print("Forestlist -Campo virgen-")
print(field_1.forestlist)
print("")

print("Posiciones -Campo virgen-")
print(field_1.positions_matrix)
print("")
tree_1=Tree((0, 4))
tree_2=Tree((2, 3))
tree_3=Tree((3, 5))

field_1.add_tree(tree_1)
field_1.add_tree(tree_2)
field_1.add_tree(tree_3)
print("Forestlist -Campo luego de add-")
print(field_1.forestlist)
print("")
print("Posiciones -Campo luego de add-")
print(field_1.positions_matrix)


field_1.delete_tree(None, tree_3)
print("Forestlist -Luego de borrar tree_3-")
print(field_1.forestlist)
print("")
print("Posiciones -Luego de borrar tree_3-")
print(field_1.positions_matrix)

field_1.delete_tree((0,4))
print("Forestlist -Luego de borrar (0,4)-")
print(field_1.forestlist)
print("")
print("Posiciones -Luego de borrar (0,4)-")
print(field_1.positions_matrix)
'''

#Campo dos y fill
field_2=Field((10, 10))
print("Forestlist -Campo2 virgen-")
print(field_2.forestlist)
print("")

print("Posiciones -Campo2 virgen-")
print(field_2.positions_matrix)
print("")

field_2.fill(age=3, diaphorina_amount=2)

print("Forestlist -Campo2 filled-")
print(field_2.forestlist)
print("")

print("Posiciones -Campo2 filled-")
print(field_2.positions_matrix)
print("")


#Hacer que si un árbol está infectado se vea como un 7 en position matrix