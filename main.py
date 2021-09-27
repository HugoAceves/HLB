import numpy as np
import random
#import matplotlib
#import pylab
#----------------------------------------- Clases ------------------------------------------
class Tree:
	def __init__(self, position, age=0., field=None):
		self.position=position 
		self.age=age
		self.infected=False
		self.diaphorina_amount=0.
		self.field=field

		#Métodos
	def manual_infection(self):#Sortea si un árbol sano se infecta o no
		if self.infected==False:#if el árbol está sano
			try:
				infection_probability=1.-self.diaphorina_amount**(-1.) #calculamos la probabilidad de contagio en función de las diaforinas
			except:
				infection_probability=0 #Esta probabilidad infección depende sólo del número de diaforinas, no del número de diaforinas infectadas
			if random.random()<infection_probability:#si un número aleatorio es menor que esa probabilidad, se contagia
				self.infected=True
				try:
					self.field.positions_matrix[tree.position[0],tree.position[1]]=7
				except:
					pass	
				#Para una función más realista, véase infection() en la clase diaphorina
class Field:
	def __init__(self, size=(100,100)):
		self.size=size
		self.positions_matrix=np.zeros(size)#The function zeros creates an array full of zeros
		forestlist_generator=[]
		for i in range(size[0]):
			forestlist_generator.append([])
			for j in range(size[1]):
				forestlist_generator[i].append(None)
		self.forestlist=list(forestlist_generator)	
	
		#Métodos
	def add_tree(self,tree):#Agrega un árbol en una posición dada  
		if self.positions_matrix[tree.position[0],tree.position[1]]==0:#-sólo si esta está vacía-
			self.forestlist[tree.position[0]][tree.position[1]]=tree#al forestlist
			if tree.infected==True:#y ocupa la casilla en positions_matrix con 7 if infected y con 1 if not
				self.positions_matrix[tree.position[0],tree.position[1]]=7
			else:
				self.positions_matrix[tree.position[0],tree.position[1]]=1
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
	
	def fill(self, age, diaphorina=False, infected=False):#Nos llena el campo con árboles aleatorios
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				random_tree=Tree((i,j), age) #Crea el árbol ijotaésimo
				if diaphorina==False:#Si no se pide que el árbol tenga diaforinas
					random_tree.diaphorina_amount=0 # Le asocia 0 diaforinas
				else:#Si se pide que tenga
					random_tree.diaphorina_amount=random.randint(300, 400) #Se le ponen entre 300 y 400

				if infected==True:
					random_tree.infection()

				self.forestlist[i][j]=random_tree #lo inserta en el bosque
				self.positions_matrix[i,j]=1 #Lo marca en la matriz de posiciones
				'''print(self.forestlist[i][j])
				print(self.positions_matrix[i,j])'''

	def run(self):
		pass
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
class Diaphorina:
	def __init__(self, field, position=(None, None)):
		self.position=position

		#Métodos
		#-----------Lo importante es programar un condicional al vuelo de la diaforina
		#Una diaforina no s queda en un árbol si no se cumple cierto coeficiente de comodidad, y vuela aleatriamente hasta encontrarlo
		#este coeficiente podrá depender de muchos factores


	def flight_to(self, position=(None, None)):#Mover una diaforina de un punto a otro particular
		if position!=(None, None):
			pass
		else:
			self.position=position
	def random_flight(self,list_tree):#Mover una diaforina de un punto a otro aleatorio de la lista de árboles
		self.position=(random.randint(0, field.size[0]-1), random.randint(0, field.size[1]-1))#Hay problema con que no haya sido definida aún esta lista?
#-------------------------- Creación de Objetos --------------------------------

