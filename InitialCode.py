import numpy as np
import random
class Tree:
	# position: tupla of coordinates (x,y) or (longitude , latitude)
	def __init__(self,position,age=0.)
		self.position=position
		self.age=age
		self.infected=False
		self.diaphorina_amount=0.
	def Infection(self):
		if infected==False:
			try:
				infection_probability=1.-diaphorina_amount**(-1.)
			except:
				infection_probability=0 #La probabilidad infección no depende precisamente del número de diaforinas, sino del número de diaforinas infectadas
			if random.random()<infection_probability:
				infected=True
class Diaphorina:
	def __init__(self,tree=None)
		self.tree=tree
	def flight_to(self,tree):
		self.tree=tree
	def random_flight(self,list_tree):
		self.tree=random.choice(list_tree)
class Field:
	def __init__(self,size=(100,100)):
		self.size=size
		self.positions_matrix=np.zeros(size)
		self.identification_lists=[[None]*size[0]]*size[1]
	def add_tree(self,tree):
		if self.positions_matrix[tree.position[0],tree.position[1]]==0 :
			self.positions_matrix[tree.position[0],tree.position[1]]=1
			self.identification_lists[tree.position[0]][tree.position[1]]=tree
		else:
			#codigo para eliminar un arbol de las matrices.
	def add_random_trees(self,Number_of_trees):
		field_width=self.size[0]
		field_height=self.size[1]
		X = np.random.randint(field_width, size=Number_of_trees)
		y = np.random.randint(field_height, size=Number_of_trees)
		list_to_add=[Tree((x,y)) for x,y in zip(x,y)]
		self.trees.append(list_to_add)
