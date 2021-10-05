import numpy as np
import random
import matplotlib.pyplot as plt
import pylab
import math#~
#----------------------------------------- Clases ------------------------------------------
class Tree:#--------------------------------------------------------------------------------
	def __init__(self, position,  field=None, age=0.):
		self.position=tuple(position) #La posición del árbol es de la forma (x, y)
		self.age=age
		self.infected=False #Se crean sanos de forma predeterminada, se infectan después,
		self.diaphorina_amount=0.# además de no alojar diaforinas
		self.infectious_diaphorina=0.#~
		self.field=field# cada árbol pertenece a un campo, que es un objeto de la clase Field() que será definida abajo

		#Métodos--------------------------------------------------------------------------------
	def manual_infection(self):#Sortea si un árbol sano se infecta o no,
		if self.infected==False:#if el árbol está sano, entonces
			try:
				infection_probability=1.-self.diaphorina_amount**(-1.) #calculamos la probabilidad de
			except:# contagio en función de las diaforinas que aloja (de todas, no sólo de las contagiadas),
				infection_probability=0 #si no hay diaforinas, la probabilidad es 0. Una vez se tiene la probabilidad,
			if random.random()<infection_probability:#si un número aleatorio es menor que esa probabilidad,
				self.infected=True #se contagia
				try:
					self.field.positions_matrix[self.position[0],self.position[1]]=3# y lo marcamos como contagiado en la matriz posiciones
				except:#Ver atributo positions_matrix de la clase Field()
					field.positions_matrix[self.position[0],self.position[1]]=3
				#Para una función más realista, se creará infection() en la clase diaphorina

class Field:#--------------------------------------------------------------------------------
	def __init__(self, size=(24,24)):#El default size del campo es 24x24 porque
		self.size=size#ese es el tamaño máximo que se muestra correctamente en REPL.
		self.positions_matrix=np.zeros(size)#La positions_matrix es una matriz que nos dice el estado de cada lugar del campo:
		forestlist_generator=[]# 0 si está vacía, 1 si tiene un árbol, 8 si tiene un árbol infectado.
		for i in range(size[0]):#Forestlist es una lista de listas que va uno a uno con la positions_matrix,
			forestlist_generator.append([])# sus elementos son los objetos de la clase árbol.
			for j in range(size[1]):
				forestlist_generator[i].append(None)
		self.forestlist=list(forestlist_generator)
		self.figure=None#~
		


		#Métodos--------------------------------------------------------------------------------
	def add_tree(self,tree):#Agrega un árbol en una posición dada
		if self.positions_matrix[tree.position[0],tree.position[1]]==0:#-sólo si la posición está vacía-
			self.forestlist[tree.position[0]][tree.position[1]]=tree#añade el árbol al forestlist
			if tree.infected==True:#y ocupa la casilla en positions_matrix
				self.positions_matrix[tree.position[0],tree.position[1]]=3#con 8 if infected
			else:
				self.positions_matrix[tree.position[0],tree.position[1]]=1#y con 1 if not.
		else:#Si no está vacía, entonces pass. Esto es para evitar borrar accidentalmente.
			pass#Se hará un código para el método replace_tree() y para delete_tree().
	def delete_tree(self, position, tree=None):#Borra un árbol dado, o el árbol que haya en una posición dada.
		if tree!=None:#Si se da árbol, borra el árbol tree con delete_tree(None, tree)
			self.forestlist[tree.position[0]][tree.position[1]]=None
			self.positions_matrix[tree.position[0],tree.position[1]]=0
		else:#o si se da la posición (a, b), borra el árbol con delete_tree((a,b)).
			self.forestlist[position[0]][position[1]]=None
			self.positions_matrix[position[0], position[1]]=0

#-----------------------------------------------------------------------------------------------------------------------~Agregar a cÓdigo

	def fill_random(self,proportion,age=1):#~Llena el campo con árboles, dejando algunos huecos aleatorios
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				if random.random()<proportion :
					self.add_tree(Tree((i,j),age))

	def get_tree_positions(self):#~Nos devuelve una matriz de 2xn con las n coordenadas de los elementos que no son cero en positions_matrix
		return np.transpose(np.nonzero(self.positions_matrix))

	def set_diaphorina_in_random_tree(self,diaphorina_amount=10,infectious=False):
		positions=list(self.get_tree_positions())#Hace una lista con los elementos de la matriz generada por get_tree_positions(),
		position=random.choice(positions)#luego elige una posición de esta lista y 
		tree=self.forestlist[position[0]][position[1]]# con ella crea un árbol en ésta.
		if (infectious==True):
			tree.infectious_diaphorina=diaphorina_amount
		else:
			tree.diaphorina_amount=diaphorina_amount
		self.positions_matrix[tree.position]=2


	def get_neighbour_trees(self,position):
		neighbours = []
		if position[0]<self.size[0]-1:
			right=position + np.array([1,0])
			if (self.positions_matrix[right[0],right[1]]>0):
				neighbours.append(right)
		if position[0]>0 :
			left=position + np.array([-1,0])
			if (self.positions_matrix[left[0],left[1]]>0):
				neighbours.append(left)
		if position[1]<self.size[1]-1:
			up=position + np.array([0,1])
			if (self.positions_matrix[up[0],up[1]]>0):
				neighbours.append(up)
		if position[1]>0:
			down=position + np.array([0,-1])
			if (self.positions_matrix[down[0],down[1]]>0):
				neighbours.append(down)
		return neighbours

	def diaphorina_spread(self):
		fraction=0.3 #fraction of diaphorina that spreads to neighbor
		pos=self.positions_matrix
		diaphorina_positions = np.transpose(np.nonzero(pos==2))
		diaph_position=random.choice(diaphorina_positions)
		neighbour_trees=self.get_neighbour_trees(diaph_position)
		propagate_to=random.choice(neighbour_trees)
		tree_to=self.forestlist[propagate_to[0]][propagate_to[1]]
		tree_from=self.forestlist[diaph_position[0]][diaph_position[1]]
		tree_to.diaphorina_amount = fraction*tree_from.diaphorina_amount
		tree_to.infectious_diaphorina = fraction*tree_from.infectious_diaphorina
		tree_from.diaphorina_amount -= tree_to.diaphorina_amount
		tree_from.infectious_diaphorina -= tree_to.infectious_diaphorina
		self.positions_matrix[tree_to.position]=2

	def update_infected_trees(self):
		def hill(x):
			return math.pow(x,2)/(36. + math.pow(x,2)) #hill function of probability of infection

		pos=self.positions_matrix
		diaphorina_positions = list(np.transpose(np.nonzero(pos==2)))
		for site in diaphorina_positions:
			tree=self.forestlist[site[0]][site[1]]
			probability = hill(tree.infectious_diaphorina)
			if (random.random()<probability):
				tree.infected=True
				self.positions_matrix[tree.position]=3

	def update_infectious_diaphorina(self):
		prob=0.3 #probability of infection for diaphorina
		pos=self.positions_matrix
		infected_positions = list(np.transpose(np.nonzero(pos==3)))
		for site in infected_positions:
			tree=self.forestlist[site[0]][site[1]]
			tree.infectious_diaphorina += prob*tree.diaphorina_amount
			tree.diaphorina_amount -= prob*tree.diaphorina_amount

	def update_diaphorina_amount(self):
		def logistic_growth(x):
			r=0.1
			K=500.
			return r*x*(1. - x/K)
		pos=self.positions_matrix
		diaphorina_positions = list(np.transpose(np.nonzero(pos==2)))
		for site in diaphorina_positions:
			tree=self.forestlist[site[0]][site[1]]
			tree.infectious_diaphorina += logistic_growth(tree.diaphorina_amount)
			tree.diaphorina_amount += logistic_growth(tree.diaphorina_amount)

	def show_field(self):
		plt.ion()
		i=1
		if self.figure==None :
			self.figure = plt.figure()
			self.figure.add_subplot(111)
			i=0

		ax=self.figure.get_axes()[0]
		im=ax.imshow(self.positions_matrix,cmap=plt.cm.tab20b)
		im.set_clim(0,3)
		if(i==0):
			self.figure.colorbar(im)
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()
		#plt.matshow(self.positions_matrix)


	def update_field(self,times=1):
		for i in range(times):
		    self.diaphorina_spread()
		    self.update_diaphorina_amount()
		    self.update_infected_trees()
		    self.update_infectious_diaphorina()

#-----------------------------------------------------------------------------------------------------------------------------------------------

#En construcción:
'''
def replace_tree(self, old_tree, new_tree):
		self.delete_tree(old_tree)
		self.add_tree(new_tree)

'''

	def fill(self, age, diaphorina=False, infected=False):#Nos llena un campo con árboles aleatorios,
		for i in range(self.size[0]):#Podemos elegir si todos los árboles serán sanos y sin diaforinas o
			for j in range(self.size[1]):# si algunos árboles se crean infectados y con algunas diaforinas aleatoriamente.
				random_tree=Tree((i,j), age) #Aquí se crea el árbol ijotaésimo,
				if diaphorina==False:#si no se pide que el árbol tenga diaforinas, entonces
					random_tree.diaphorina_amount=0 #se le asocia 0 diaforinas.
				else:#Si se pide que sí tenga diaforinas, entonces
					random_tree.diaphorina_amount=random.randint(300, 400) #se le ponen entre 300 y 400 diaforinas
				if infected==True:#Si se pide que algunos estén infectados, entonces
					if random.random()<0.02:#se infectan aleatoriamente algunos árboles.
						random_tree.infected=True#Una vez que el érbol está listo,
				self.forestlist[i][j]=random_tree #se inserta en el bosque (se pone el objeto en forestlist),
				if random_tree.infected==True:#Lo registra en la matriz posiciones (positions_matrix)
					self.positions_matrix[i,j]=8 #con 8 si está sano, o
				else:
					self.positions_matrix[i,j]=1#con 1 si está infectado.

	def spread(self, radio=1):#Esparce la enfermedad de un árbol a sus vecinos.
		for i in range(self.size[0]):
			for j in range(self.size[1]):#Primero toma la posición ijotaésima,
				if self.forestlist[i][j].infected==True:#si el árbol allí está infectado, entonces
					for k in range(self.size[0]):
						for l in range(self.size[1]):#recorre nuevamente el campo árbol a árbol (esto no es para nada eficiente, se corregirá)
							if (k-i)**2+(l-j)**2<=radio**2:#si el árbol kaelésimo está en la vecindad del ijotaésimo, entonces
								self.positions_matrix[k,l]=8# lo marca como infectado en la positions_matrix.

		for k in range(self.size[0]):#No se infecta al objeto kaelésimo directamente en el bucle anterior porque if self.forestlist[i][j].infected==True:
			for l in range(self.size[1]):#contaría esos árboles como infectados, a pesar de que se acaban de infectar, y esto no es útil,
				if self.positions_matrix[k,l]==8:#Así que se hace la infección hasta el final de todas las iteraciones
					self.forestlist[k][l].infected=True#basados en la positions_matrix insfectamos a los objetos de forestlist.

	def play(self, iterations=10):#Este método sirve para hacer evolucionar el field a través del tiempo
		for i in range(iterations):#Se hace play independiente de spread para que se pueda iterar el campo sin forzosamente esparcir infecciones,
			self.spread()# esto podría ser útil en el futuro.

	'''En construcción:
		def add_random_trees(self,Number_of_trees):
		field_width=self.size[0]
		field_height=self.size[1]
		x = np.random.randint(field_width, size=Number_of_trees)
		y = np.random.randint(field_height, size=Number_of_trees)
		list_to_add=[Tree((x,y)) for x,y in zip(x,y)]
		self.trees.append(list_to_add)
	Quité momentáneamente este método porque los campos comerciales no tienen  árboles distribuidos aleatoriamente,
	están siempre en cuadrículas llenas, quizás en los traspatios sí lo estén,
	'''
class Diaphorina:#--------------------------------------------------------------------------------
	def __init__(self, field, position=(None, None)):
		self.position=position

		#Métodos--------------------------------------------------------------------------------

	def flight_to(self, position=(None, None)):#Mover una diaforina de un punto a otro particular
		if position!=(None, None):
			pass
		else:
			self.position=position
	def random_flight(self,list_tree):#Mover una diaforina de un punto a otro aleatorio de la lista de árboles
		self.position=(random.randint(0, field.size[0]-1), random.randint(0, field.size[1]-1))#Hay problema con que no haya sido definida aún esta lista?
#-------------------------- Fin de las clases --------------------------------
