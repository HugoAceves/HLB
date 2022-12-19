import numpy as np
import random
import matplotlib.pyplot as plt
import math
from math import floor
from math import ceil
from matplotlib.colors import LinearSegmentedColormap
from numpy import array_equal

colormap=LinearSegmentedColormap.from_list('colormap', ['#858A51','#24912F','#99675a', '#991A37', '#246330'], N=5)#Esta variabe determina el código de colores de las gráficas de la Positions matrix.


#----------------------------------------- Clases ------------------------------------------
class Tree:#------------------------------- Árbol-------------------------------------------------
	def __init__(self, position,  field=None, age=0.):
		self.position=tuple(position) #La posición del árbol: en el array de forma [x, y], donde x representa el número de casillas hacia abajo, y y el número de casillas a la derecha.
		self.age=age #Edad del árbol (sin usar)
		self.infected=False #Se crean sanos de forma predeterminada, se pueden infectar después,
		self.diaphorina_amount=0# además de no alojar diaforinas sanas
		self.infectious_diaphorina=0#ni infecciosas.
		self.diaphorina_total=0#El total de las diaforinas es la suma de las sanas e infecciosas (las dos anteriores)
		self.field=field# cada árbol pertenece a un campo, que es un objeto de la clase Field() que será definida abajo
		self.incubation=0 #El período de incubación

		#Métodos--------------------------------------------------------------------------------
	def manual_infection(self):#Sortea si un árbol sano se infecta o no,
		print('Infectando árbol mediante la función manual_infection.')
		if self.infected==False:#if el árbol está sano, entonces
			try:
				infection_probability=1.-self.diaphorina_amount**(-1.) #calculamos la probabilidad de
			except:# contagio en función de las diaforinas que aloja (de todas, no sólo de las contagiadas),
				infection_probability=0. #si no hay diaforinas, la probabilidad es 0. Una vez se tiene la probabilidad,
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
		self.positions_matrix=np.zeros(size, dtype=int)#La positions_matrix es una matriz que nos dice el estado de cada lugar del campo:

		forestlist_generator=[]# 0 si está vacía, 1 si tiene un árbol, 3 si tiene un árbol infectado, 2 si aloja diaforinas.
		for i in range(size[0]):#Forestlist es una lista de listas que va uno a uno con la positions_matrix,
			forestlist_generator.append([])# sus elementos son los objetos de la clase árbol.
			for j in range(size[1]):
				forestlist_generator[i].append(None)
		self.forestlist=list(forestlist_generator)

		self.diaphorina_scalar_field=np.zeros(size)#Creamos una especie de campo escalar que asigna a cada punto (cada árbol) la cantidad de diaforinas SANAS que contiene,
		self.infected_diaphorina_scalar_field=np.zeros(size)#lo mismo para las infectadas,
		self.diaphorina_total_scalar_field=np.zeros(size)#y para las totales, que son la suma de las dos anteriores.
		#Comenzamos estos campos con ceros, se modifican cuando se crean diaforinas a través de set_diaphorina_in_random_tree, cuando se mueven usando diaphorina_spread y finalmente por update_infectious_diaphorina.
		self.figure=None#~Es el atributo figura para matplotlib.
		self.figure_saved=None
		self.figure_stats=None#Esta es la figura de la gráfica de estadísticas
		self.figure_s=None
		self.figure_i=None
		self.figure_t=None
		self.incubation_graph=False
		self.are_there_diaphorinas=False #Este parámetro nos dice si el campo tiene diaforinas, este ayuda a evitar errores en la ejecución de algunas funciones
		#Debería quitarse are_there_diaphorinas puesto que para saber si hay o no diaforinas en un árbol basta con mirar la positions matrix

		self.stats_infected_trees=[]#Similar que la anterior para árboles infectados
		self.stats_asymptomatic_trees=[]#Similar que la anterior para árboles asintomáticos
		self.stats_asymptomatic_fraction=[]

		self.stats_diaphorina_amount=[]#en esta lista se registra la población de diaforinas, es modificada a través de update_field() en donde se repasa la positions_matrix
		self.stats_infectious_diaphorina=[]#Similar que la anterior para diaforinas infecciosas
		self.stats_diaphorina_total=[]#Similar que la anterior para el total de diaforinas

		self.day=1


		#Métodos internos--------------------------------------------------------------------------------
	def add_tree(self,tree):#Agrega un árbol en una posición dada
		if self.positions_matrix[tree.position[0],tree.position[1]]==0:#-sólo si la posición está vacía-
			self.forestlist[tree.position[0]][tree.position[1]]=tree#añade el árbol al forestlist
			if tree.infected==True:#y ocupa la casilla en positions_matrix
				self.positions_matrix[tree.position[0],tree.position[1]]=3#con 3 if infected
			else:
				self.positions_matrix[tree.position[0],tree.position[1]]=1#y con 1 if not.
		else:#Si no está vacía, entonces pass. Esto es para evitar borrar accidentalmente.
			pass#Se hará un código para el método replace_tree() y para delete_tree().

	def delete_tree(self, position=None, tree=None):#Borra un árbol dado, o el árbol que haya en una posición dada.
		print('Borrando árbol mdiante la función delete_tree.')
		if tree!=None:#Si se da árbol, borra el árbol tree con delete_tree(None, tree)
			self.forestlist[tree.position[0]][tree.position[1]]=None
			self.positions_matrix[tree.position[0],tree.position[1]]=0
		else:#o si se da la posición (a, b), borra el árbol con delete_tree((a,b)).
			self.forestlist[position[0]][position[1]]=None
			self.positions_matrix[position[0], position[1]]=0

	def fill_random(self,proportion,age=1):#~Llena el campo con árboles, dejando algunos huecos aleatorios
		print('Llenando el campo mediante la función fill_random.')
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				if random.random()<proportion :
					self.add_tree(Tree((i,j),age))

		print('Se ha llenado el '+str(proportion*100)+'% del campo con árboles de '+str(age)+' años.')

	def get_tree_positions(self):#~Nos devuelve una matriz de 2xn con las n coordenadas de los elementos que no son cero en positions_matrix

		return np.transpose(np.nonzero(self.positions_matrix))

	def set_diaphorina_in_random_tree(self, diaphorina_amount=0,infectious_diaphorina=0):#Asigna a un árbol aleatorio diaforinas sanas o enfermas según se quiera PARA UN CAMPO DE RECIENTE CREACIÓN.
	#Primero elige algún lugar aleatorio del campo y se asegura de que tenga árbol.
		positions=list(self.get_tree_positions())#Para esto, hace una lista con los elementos de la matriz generada por get_tree_positions(), esta matriz toma todos los árboles menos los huecos,
		position=random.choice(positions)#luego elige una posición aleatoria de esta lista y 
		tree=self.forestlist[position[0]][position[1]]# se toma al árbol en ésta llamándolo tree.

		if infectious_diaphorina>0:#Si se pide en el argumento, al árbol se le AGREGA (POR ESO EL +=)
			tree.infectious_diaphorina+=infectious_diaphorina#una cantidad infectious_diaphorina de diaforinas infectadas en su atributo,
			self.infected_diaphorina_scalar_field[tree.position[0],tree.position[1]]+=tree.infectious_diaphorina#finalemnte se registra en el campo de diaforinas infectadas.
		if diaphorina_amount>0:#Luego, si se pide en el argumento, se agrega al árbol (importante que se usa +=),
			tree.diaphorina_amount+=diaphorina_amount# una cantidad diaphorina_amount de diaforinas sanas en su atributo,
			self.diaphorina_scalar_field[tree.position[0],tree.position[1]]+=tree.diaphorina_amount#finalemnte se registra en el campo de diaforinas sanas.

		tree.diaphorina_total=tree.diaphorina_amount+tree.infectious_diaphorina#Además actualizamos el total de diaforinas del árbol
		#Una vez actualizados los campos de diaforinas sanas y de infectadas, 
		self.diaphorina_total_scalar_field[tree.position[0],tree.position[1]]+=(diaphorina_amount+infectious_diaphorina)#se actualiza el total en el campo de diaforinas totales.
		
		if (infectious_diaphorina>0 or diaphorina_amount>0):#Comprueba si efectivamente se agregaron diaforinas (esta disyunción no es exclusiva; es verdadera si uno o los dos son verdaderos),
			self.positions_matrix[tree.position]=2#y si sí, entonces tree es ahora un árbol con diaforinas, así que se marca con un 2 en la matriz de posiciones.
		
		self.are_there_diaphorinas=True#ESTA LÍNEA SE QUITARÁ EN EL FUTURO, puesto que para saber si hay o no diaforinas en un árbol basta con mirar la positions matrix.




		print('Se han colocado '+str(diaphorina_amount)+' diaforinas sanas y '+str(infectious_diaphorina)+' infectadas en el árbol de coordenadas '+str(position+[1, 1])+'.\n')


	def get_neighbour_trees(self,position):#Nos devuelve una lista de los árboles vecinos dada una posición (latitud, longitud)
		neighbours = []
		if position[0]<self.size[0]-1:#Si la longitud es menor al ancho del campo (si fuera igual, no tendría vecino a la derecha),
			right=position + np.array([1,0])#entonces nombra right al espacio de la derecha (mediante una suma vectorial unitaria î)
			if (self.positions_matrix[right[0],right[1]]>0):#si en positions_matrix hay árbol en la posición right,
				neighbours.append(right)#entonces agrega lo que haya en right (un objeto árbol) a la lista de vecinos.
		if position[0]>0 :#Análogo para la izquierda
			left=position + np.array([-1,0])
			if (self.positions_matrix[left[0],left[1]]>0):
				neighbours.append(left)
		if position[1]<self.size[1]-1:#Análogo para arriba
			up=position + np.array([0,1])
			if (self.positions_matrix[up[0],up[1]]>0):
				neighbours.append(up)
		if position[1]>0:#Análogo para abajo
			down=position + np.array([0,-1])
			if (self.positions_matrix[down[0],down[1]]>0):
				neighbours.append(down)
		return neighbours#Finalmente nos devuelve la lista de vecinos

	def diaphorina_spread(self, strength=0, dt=1):#~Toma una fraction de las diaforinas de cierca cantidad de árboles aleatorios del tipo 2 dados por la fracción strength, 
		#y las mueve a algún vecino aleatorio. (strength todavía no se implementa, pero será la proporción de árboles elegidos para que sus diaforinas emigren)
		fraction=0.3 #Esta, como se dijo antes, es la fracción de diaforinas que se esparcirá a otros árboles.
		pos=self.positions_matrix#Llamamos pos a la matriz de posiciones cuyos valores son 0: sin árbol, 1: árbol sano, 2: árbol con diaforinas, 3: árbol infectado 4: árbol asintomático,
		diaphorina_positions = np.transpose(np.nonzero(pos>1))# de modo que esta es la matriz 2xn con las n coordenadas de los elementos mayores a 1 en pos (los elementos con diaforinas).


		try:#Este try es consecuencia de que en ocasiones el campo se queda sin diaforinas, de modo que la matriz anterior el vacía y nos da un error al aplicar choice en ella()
			diaph_position=random.choice(diaphorina_positions)#se elige una posición aleatoria que tenga diaforinas y se le llama diaph_position,


			#Estas dos líneas serán cambiadas cuando se sustituya get_neighbour_trees() por choice_destinaton().
			neighbour_trees=self.get_neighbour_trees(diaph_position)#luego se calcula la lista neighbour_trees, que son los vecinos de esa posición.
			propagate_to=random.choice(neighbour_trees)#Propagate_to es una posición (una tupla) vecina elegida aletoriamente,


			#Aquí probablemente se hará un bucle que vaya pasando las diaforinas de unos árboles a otros
			tree_to=self.forestlist[propagate_to[0]][propagate_to[1]]#y es aquí donde se toma el objeto árbol basados en esa posición,
			tree_from=self.forestlist[diaph_position[0]][diaph_position[1]]#así como el árbol desde el que parte la diaforina.

			if (tree_from.diaphorina_amount*fraction)*dt>=random.random():#Si una fracción de las diaforinas rebasa cierto umbral random,
				out=1
			else:
				out=0

			if (tree_from.infectious_diaphorina*fraction)*dt>=random.random():
				out_infected=1
			else:
				out_infected=0
			
			#print(tree_from.diaphorina_amount)
			#print(tree_from.infectious_diaphorina)


			tree_to.diaphorina_amount += out#se suma a la cantidad de diaforinas sanas que llegan al otro árbol 
			self.diaphorina_scalar_field[tree_to.position[0],tree_to.position[1]]=tree_to.diaphorina_amount

			tree_from.diaphorina_amount -= out#se resta del primer árbol la fracción de diaforina sana que se va al segundo
			if tree_from.diaphorina_amount<0:#Este if no debería afectar a lo que está arriba (la idea es que no las resete como se hace arriba si es que ya hay cero diaforinas. Incluso hay que tener cuidado, porque la fraction depende de la cantidad iniicial de diaforinas, de modo que la fraction de caro es cero y por tanto se resta cero) 
				tree_from.diaphorina_amount=0#entonces no se hace
			self.diaphorina_scalar_field[tree_from.position[0],tree_from.position[1]]=tree_from.diaphorina_amount
			

			tree_to.infectious_diaphorina += out_infected#se esparce al otro árbol la fracción de diaforina infectada
			self.infected_diaphorina_scalar_field[tree_to.position[0],tree_to.position[1]]+=tree_to.infectious_diaphorina
			tree_from.infectious_diaphorina -= out_infected#se resta del primer árbol la fracción de diaforina enferma que se va al segundo
			if tree_from.infectious_diaphorina<0:
					tree_from.infectious_diaphorina=0
			self.infected_diaphorina_scalar_field[tree_from.position[0],tree_from.position[1]]=tree_from.infectious_diaphorina
			if self.positions_matrix[tree_to.position]==1:
				self.positions_matrix[tree_to.position]=2#El segundo árbol es registrado como un árbol con diaforinas infectadas



		except Exception as e:
			print('La simulación terminó debido a que el número de diaforinas llegó a cero y la función diaphorina_spread()'
			'no ha podido continuar. Es posible que los parámetros sean tales que las diaforinas se extinguen más de lo que nacen.')
			print(str(e))
			self.are_there_diaphorinas=False
			return False


	#Métodos de dinámica--------------------------------------------------------------------------------

	#Suposición 1: Supongamos que las diaforinas sanas emigran tanto como las infectadas.
	#suposición 2: Supongamos que el patrón de siembra, hace que sea más sencillo que las diaforinas se esparzan más lejos verticalmente que horizontalmente.

	def list_origin_trees(self, strength=0):#Devuelve una lista de posiciones llenada con cierta proporción strength tomada de árboles con diaforinas de forma aleatoria.
		#Strength es la fracción de los árboles con diaforinas que enviarán diaforinas a otros árboles
		
	
		print('-Calculando los árboles que esparcirán sus diaforinas mediante la función list_origin_trees con una fuerza del '+str(strength*100)+'%:')
		origin_trees_list=[]#Esta es la lista de posiciones que llenará y devolverá la función.

		diaphorina_trees_amount=np.count_nonzero(self.positions_matrix>1) #Primero calcula cuántos árboles con diaforinas tiene el campo y a esa cantidad la llama diaphorina_trees_amount,

		#(notar que los árboles marcados con algún número mayor que 1, además de 2, pueden ser 3 o 4, estos últimos pueden ser elementos con diaforinas o ya no serlo, 
		#esto es, que podrían estar infectados (3) pero no tener diaforinas, así que diaphorina_trees_amount eventualmente podría contemplar árboles que tuvieron diaforinas como árboles que tienen,
		#esto no es un problema ahora porque en las líneas que siguen, una vez se selecciona una posición candidata, se descarta si su árbol no aloja diaforinas)

		if strength==0:#luego se asegura de no dividir por cero y,
			print('%ERROR: Se ha llamado a la función list_origin_trees pero su argumento no puede ser 0')#si ese es el caso, lo avisa y luego,
			return#si ese es el caso, sale de la función.

		origin_trees_amount=int(diaphorina_trees_amount//(strength)**-1)#Después calcula cuántos árboles tomará en función de strength y de los árboles con diaforinas que haya en el campo:
		#Mediante diaphorina_trees_amount//strength. Recordemos que el // da sólo el cociente, o sea, la parte entera de la división, de modo que,
		#origin_trees_amount es la cantidad de iteraciones del bucle en el que se elegirán las posiciones de los árboles (uno a la vez), así que al final del bucle se completará la cantidad de posiciones que se necesiten.
		
		if origin_trees_amount<1:
			origin_trees_amount=1
			print('Se ha fijado origin_trees_amount porque resultaba menor que 0 debido a que hay '+str(diaphorina_trees_amount)+' árboles con diaforinas y se strength es '+str(strength*100)+'%. (ESTO ES NORMAL EN LOS PRIMEROS CICLOS DE LA SIMULACIÓN)')
		candidates_list=np.transpose(np.nonzero(self.positions_matrix>1))#Enlista primero las posiciones de los árboles con diaforinas, estas posiciones son candidatas para su elección.
		
		print('--Eligiendo '+str(origin_trees_amount)+' árboles de entre '+str(len(candidates_list)))
		for i in range(origin_trees_amount):#Comienza el bucle en el que se llenará la lista de posiciones de árboles, para esto,
			selected=False#establece esta variable para mostrar que no se ha elegido aún una posición candidata,

			while selected==False:#luego comienza el bucle que terminará hasta que se elija al candidato i,
				candidate=random.choice(candidates_list)#luego elige una posición aleatoria de la lista de posiciones candidatas y,
				
				#(sería muy sencillo y natural que esta línea fuese if candidate in origin_trees_list:, pero da un extraño error que tiene que ver con numpy, de modo que se ha tomado el siguiente if,
				#de la primer respuesta de https://stackoverflow.com/questions/23979146/check-if-numpy-array-is-in-list-of-numpy-arrays y se la ha adaptado sin entender a profundidad)
				#candidated=[candidate[0], candidate[1]]
				#if candidated in origin_trees_list:

				if next((True for elem in origin_trees_list if array_equal(elem, candidate)), False):#comprueba si el árbol ya ha sido elegido, o sea, que ya esté en la lista de candidatos,
					selected=False#si ese es el caso, regresa el bucle para elegir una posición candidata nueva,
					print('--Se ha rechazado el candidadto' +str(candidate+[1, 1])+' porque ya pertenece a la lista.')
				elif self.forestlist[candidate[0]][candidate[1]].diaphorina_total==0:#después se asegura de que el árbol de la posición candidata tiene diaforinas,
					selected=False#si ese NO es el caso (o sea, no tiene diaforinas), regresa el bucle para elegir posición candidata nueva,
					print('--Se ha rechazado el candidadto' +str(candidate+[1, 1])+' porque no tiene diaforinas.')
				else:#la posición candidata pasa los filtros anteriores, se la agrega a la lista de posiciones de los árboles de origen,
					origin_trees_list.append(candidate)#recordemos que esto agrega una posición y no un objeto árbol
					print('--El candidato '+str(candidate+[1, 1])+' ha sido agregado a la lista y tiene '+str(self.forestlist[candidate[0]][candidate[1]].diaphorina_total)+' diaforinas')
					selected=True#finalmente se establece que ha sido elegido uno de los candidatos para salir del bucle de elección.

		print('--list_origin_trees finalizada. \n')
		return origin_trees_list #Los árboles puestos en la lista list_origin_trees se devuelven con un return

	def choose_destination_tree(self, tree_from_position):#Dada la posición de un árbol (con diaforinas para evitar errores), devuelve un árbol destino.
		#Hace esta elección considerando la probabilidad en función del patrón de siembra, la distancia y la relación que haya entre la cantidad de diaforinas del árbol origen al destino.
		print('-Encontrando un árbol destino para el árbol de posición '+str(tree_from_position+[1, 1])+' a través de choose_destination_tree:')
		field_height=self.size[0]-1#Primero establece la altura del campo,
		field_width=self.size[1]-1#y la anchura, después

		exit_position_loop=False#se establece el parámetro para salir del bucle de posición,
		exit_ratio_loop=False#luego se establece el parámetro para salir del bucle de proporción (en el que se decide si las cantidades de diaforinas propician la migración)
		exit_exhaustive=3#Este establece el número de veces máximas que el bucle ratio_loop puede ejecutarse sin éxito debido a que el árbol candidato alberga más diaforinas que el origen

		while exit_ratio_loop==False:
			exit_position_loop=False
			while exit_position_loop==False:#En el bucle de posición se elige una posición de forma aleatoria binomial que esté dentro de los márgenes del campo, primero
				print('---Buscando una posición candidata.')

				horizontal_dispacement=np.random.normal(loc=0, scale=4)#se elige con probabilidad binomial centrada en 0, el desplazamiento y luego lo redondea (motar que horizontal_dispacement tiene un scales de 1.5)
				if horizontal_dispacement>0.5:#hacia arriba si el número es positivo mayor que 0.5,
					horizontal_dispacement=ceil(horizontal_dispacement)
				elif horizontal_dispacement<-0.5:#o hacia abajo si el número es negativo menor que -0.5,
					horizontal_dispacement=floor(horizontal_dispacement)
				else:
					horizontal_dispacement=0#finalmemte, si alguna vez el número fuese suficientemente cercano a cero, lo convertiría en cero.

				vertical_dispacement=np.random.normal(loc=0, scale=6)#Luego se elige el desplazamiento vertical, que es por lo general, más extenso que el horizontal por el patrón de siembra,
				if vertical_dispacement>0.5:# se redondea hacia arriba si el número es positivo mayor que 0.5,
					vertical_dispacement=ceil(vertical_dispacement)
				elif vertical_dispacement<-0.5:#o hacia abajo si el número es negativo menor que -0.5,
					vertical_dispacement=floor(vertical_dispacement)
				else:
					vertical_dispacement=0#finalmemte, si alguna vez el número fuese suficientemente cercano a cero, lo convertiría en cero.

				dest=tree_from_position+np.array([vertical_dispacement, horizontal_dispacement])#Llamamos dest a la posición del árbol candidato dada por la posición origen mas el desplazamiento,
				if (tree_from_position[0]+vertical_dispacement)>field_height or (tree_from_position[1]+horizontal_dispacement)>field_width:#Por último comprueba si los desplazamientos no rebasan 
					exit_position_loop=False#las dimensiones del campo positivamente
					print('----Se ha descartado la posición candidata debido a que está fuera del campo.')
				elif (tree_from_position[0]+vertical_dispacement)<0 or (tree_from_position[1]+horizontal_dispacement)<0:#o negativamente
					exit_position_loop=False
					print('----Se ha descartado la posición candidata debido a que está fuera del campo.')
				elif self.positions_matrix[dest[0], dest[1]]==0:#luego comprobamos que esa posición no esté vacía, si lo está,
					exit_position_loop=False#se elige otra.
					print('----Se ha descartado la posición candidata debido a que no tiene árbol.')
				elif horizontal_dispacement==0 and vertical_dispacement==0:#o si ambos son cero al mismo tiempo (esto haría que el desplazamiento total fuera cero, cosa que no es deseable)
					exit_position_loop=False#y mientras se den algunos de estos casos, se seguirá en el bucle,
					print('----Se ha descartado la posición candidata debido a que es idéntica al origen.')
				else:#si no,
					exit_position_loop=True#se sale del bucle.

				print('---La posición candidata es '+str(dest+[1, 1]))

			destination=tree_from_position+np.array([vertical_dispacement, horizontal_dispacement])


			
			#Una vez se tiene al candidato destination, se sortea su elección. El criterio se basa en la proporción de diaforinas que hay entre el árbol origen y el receptor,
			#cuantas menos diaforinas tenga el árbol candidato a recibirlas, en comparación con el emisor, es más probable éstas emigren.tiene más diaforinas que el emisor.

			tree_from_diaphorinas=self.forestlist[tree_from_position[0]][tree_from_position[1]].diaphorina_total#Tomamos la cantidad de diaforinas del árbol emisor (llamada from en los comentarios),
			tree_to_diaphorinas=self.forestlist[destination[0]][destination[1]].diaphorina_total#luego tomamos la cantidad de diaforinas del árbol receptor (llamada to en los comentarios),
			ratio=tree_to_diaphorinas/tree_from_diaphorinas#y después calculamos la relación entre estas dos cantidades como ratio=to/from.

			#Entenderemos a to/from como la probabilidad de que las diaforinas NO emigren. Esto se puede ver de que entre más diaforonas haya en el árbol destino con respecto al origen, menos deseable sería emigrar,
			#lo mismo en el otro caso, entre menos diaforinas haya en el árbol destino con respecto al origen, más deseable sería emigrar.

			#Antes de seguir, recordemos que from no puede ser cero porque la función se aplicará sobre la list_origin_trees, que contempla árboles con diaforinas (además to y from son siempre mayores que cero).
			rand=random.random()#Se elige un aleatorio entre 1 y 0 para usarse en el bucle que viene,
			
			if ratio>=1:#si to=from entonces to/from=1 y es seguro que las diaforinas NO emigran, lo mismo si to>from, porque entonces to/from>1,
				exit_ratio_loop=False#de modo que el bucle se reinicia para buscar a otro candidato para recibirlas,
				print('---Se ha descartado la posición candidata debido a que alberga más diaforinas que el árbol origen')
				exit_exhaustive-=1
				print('---Hasta ahora, se han descartado '+str(5-exit_exhaustive)+' candidatos para '+str(tree_from_position+[1, 1])+' y restan '+str(exit_exhaustive)+' intentos.')

			elif ratio==0:#si to=0 entonces to/from=0,
				exit_ratio_loop=True#e igualmente hay que buscar a un nuevo candidato,

			elif ratio<0:#ratio puede ser 0 como vimos, pero no puede ser menor a él, puesto que ni to ni from son negativos en ningún caso, pues no tendría sentido que tuvieran diaforinas negativas,
				print('%ERROR: Se ha llamado a la función choose_destination_tree, sin embargo ratio<=0 puesto que to='+str(tree_to_diaphorinas)+' y from='+str(tree_from_diaphorinas))
				exit_ratio_loop=True#si esto sucediese, se corta el bucle y se muestra un error,

			else:#finalmente en este punto sólo queda la opción 0<to/from<1, que es la probabilidad de que las diaforinas no emigren,
				if ratio<=rand:#si el aleatorio es mayor a la probabilidad
					exit_ratio_loop=True#se sale del bucle y las diaforinas emigran
				else:#si no,
					exit_ratio_loop=False#se busca un nuevo candidato, y
				print('---Se ha descartado la posición candidata debido a que no ha salido sorteada')

			if exit_exhaustive==0:#Si 5 candidatos han sido descartados por tener más diaforinas que el origen, se sale del bucle
				exit_ratio_loop=True
				destination=tree_from_position
			#se sale del bucle hasta que se tenga uno elegido.

		if exit_exhaustive==0:
			print('--Luego de varios intentos, no se ha podido encontrar un candidato con menos diaforinas que el origen, de modo que el propio origen ha sido elegido como destino.')
		else:	
			print('--Se ha elegido destino a '+str(vertical_dispacement)+' celdas verticalmente, y a '+str(horizontal_dispacement)+' horizontalmente, en el punto '+str(destination+[1, 1])+',')
			print('--en el árbol origen hay '+str(tree_from_diaphorinas)+' diaforinas y en el destino '+str(tree_to_diaphorinas)+', de modo que la proporción es '+str(ratio)+',')
			print('--concluye choose_destination_tree con '+str(tree_from_position+[1, 1])+' y '+str(destination+[1, 1])+' emparejados. \n')

		return destination#Finalmente nos devuelve la posición del árbol destino


	def diaphorina_spread2(self, strength=0.3, dt=1):#usa las dos funciones anteriores para modificar los campos, los árboles de foerstlist y la positions matrix
		#Strength es la fracción de los árboles con diaforinas que enviarán diaforinas a otros árboles
		print('Difundiendo diaforinas mediante diaphorina_spread2 con una fuerza del '+str(strength*100)+'%.')
		origin_trees_list=self.list_origin_trees(strength)#Primero se toma a la lista de árboles origen,
		
		for i in range(len(origin_trees_list)): #Para cada elemento de la matriz de árboles origen
			print('Moviendo las diaforinas del árbol '+str(i+1)+' de la list_origin_trees.')

		#Encuentra un árbol destino mediante choose_destination_tree para cada árbol origen,
			tree_from_position=origin_trees_list[i]#toma la posición iésima de la lista de árboles origen y
			tree_to_position=self.choose_destination_tree(tree_from_position) #encuentra un árbol destino mediante choose_destination_tree,

		#	Calcula la fracción a pasar, por ahora será la fracción 0<to/from<1 (pero sería deseable que la cantidad demendiese de la distancia y del ratio de alguna forma sofisticada)
		#	Por ahora nos conformaremos con tomar una porción strength
			portion=strength/2#así, cuando se quiera cambiar, solamente se cambia esta igualdad por las líneas de código necesarias para calcular portion
			if portion==1:
				print('%ATENCIÓN, la porción de diaforinas que se tomará es del cien por ciento, de modo que se dejará al árbol emisor sin diaforinas y esto puede causar errores')

			tree_from=self.forestlist[tree_from_position[0]][tree_from_position[1]]#Árbol from
			tree_to=self.forestlist[tree_to_position[0]][tree_to_position[1]]#Árbol to

			tree_from_diaphorinas=self.forestlist[tree_from_position[0]][tree_from_position[1]].diaphorina_amount#Cantidad de diaforinas sanas del Árbol from
			tree_to_diaphorinas=self.forestlist[tree_to_position[0]][tree_to_position[1]].diaphorina_amount#Cantidad de diaforinas sanas del Árbol to

			tree_from_infectious_diaphorinas=self.forestlist[tree_from_position[0]][tree_from_position[1]].infectious_diaphorina#Cantidad de diaforinas infecciosas del Árbol from
			tree_to_infectious_diaphorinas=self.forestlist[tree_to_position[0]][tree_to_position[1]].infectious_diaphorina#Cantidad de diaforinas infecciosas del Árbol to

			tree_from_diaphorinas_total=self.forestlist[tree_from_position[0]][tree_from_position[1]].diaphorina_total#Cantidad de diaforinas totales del Árbol from
			tree_to_diaphorinas_total=self.forestlist[tree_to_position[0]][tree_to_position[1]].diaphorina_total#Cantidad de diaforinas totales del Árbol to

			migrants=int((tree_from_diaphorinas-tree_to_diaphorinas)//(portion)**-1)#con esto, calcula las cantidades de diaforinas (sanas e infecciosas),
			infectious_migrants=int((tree_from_infectious_diaphorinas-tree_to_infectious_diaphorinas)//(portion)**-1)#basándose en la diferencia de diaforinas.

			print('El árbol origen de '+str(tree_from_position+[1, 1])+' tiene '+str(tree_from_diaphorinas)+' diaforinas sanas y enviará el '+str(portion*100)+'% de la diferencia ('+str(migrants)+ ' diaforinas) al de '+str(tree_to_position+[1, 1])+' que tiene '+str(tree_to_diaphorinas))
			print('El árbol origen de '+str(tree_from_position+[1, 1])+' tiene '+str(tree_from_infectious_diaphorinas)+' diaforinas infecciosas y enviará el '+str(portion*100)+'% de la diferencia ('+str(infectious_migrants)+ ' diaforinas) al de '+str(tree_to_position+[1, 1])+' que tiene '+str(tree_to_infectious_diaphorinas))
			print('Los totales de diaforinas antes de los cambios son: '+str(tree_from_diaphorinas+tree_from_infectious_diaphorinas)+' en el árbol origen, y '+str(tree_to_diaphorinas+tree_to_infectious_diaphorinas)+' en el árbol destino.')
			print('')

		#	Modifica la cantidad de diaforinas a cada árbol desde foerstlist:
		#	Sanas
			self.forestlist[tree_from_position[0]][tree_from_position[1]].diaphorina_amount-=migrants#resta las migrantes a from y
			self.forestlist[tree_to_position[0]][tree_to_position[1]].diaphorina_amount+=migrants#las suma a to.
		#	Infecciosas
			self.forestlist[tree_from_position[0]][tree_from_position[1]].infectious_diaphorina-=infectious_migrants#resta las migrantes a from y
			self.forestlist[tree_to_position[0]][tree_to_position[1]].infectious_diaphorina+=infectious_migrants#las suma a to.


			#Actualiza las variables de diaforinas infecciosas y de sanas
			tree_from_diaphorinas=self.forestlist[tree_from_position[0]][tree_from_position[1]].diaphorina_amount#Cantidad de diaforinas sanas del Árbol from
			tree_to_diaphorinas=self.forestlist[tree_to_position[0]][tree_to_position[1]].diaphorina_amount#Cantidad de diaforinas sanas del Árbol to
			tree_from_infectious_diaphorinas=self.forestlist[tree_from_position[0]][tree_from_position[1]].infectious_diaphorina#Cantidad de diaforinas infecciosas del Árbol from
			tree_to_infectious_diaphorinas=self.forestlist[tree_to_position[0]][tree_to_position[1]].infectious_diaphorina#Cantidad de diaforinas infecciosas del Árbol to

		#	Total
			self.forestlist[tree_from_position[0]][tree_from_position[1]].diaphorina_total=tree_from_diaphorinas+tree_from_infectious_diaphorinas#Suma las nuevas cantidades de sanas e infecciosas de From
			self.forestlist[tree_to_position[0]][tree_to_position[1]].diaphorina_total=tree_to_diaphorinas+tree_to_infectious_diaphorinas#y luego suma las nuevas cantidades de sanas e infecciosas de to.

			#Actualiza las variables de diaforinas totales
			tree_from_diaphorinas_total=self.forestlist[tree_from_position[0]][tree_from_position[1]].diaphorina_total#Cantidad de diaforinas totales del Árbol from
			tree_to_diaphorinas_total=self.forestlist[tree_to_position[0]][tree_to_position[1]].diaphorina_total#Cantidad de diaforinas totales del Árbol to


			#tree_from_diaphorinas=self.forestlist[tree_from_position[0]][tree_from_position[1]].diaphorina_amount
			print('Luego de los cambios, el árbol origen tiene '+str(tree_from_diaphorinas)+' diaforinas, '+str(migrants)+ ' menos que antes, mismas que ganó el árbol destino, que ahora tiene '+str(tree_to_diaphorinas))
			print('Luego de los cambios, el árbol origen tiene '+str(tree_from_infectious_diaphorinas)+' diaforinas, '+str(infectious_migrants)+ ' menos que antes, mismas que ganó el árbol destino, que ahora tiene '+str(tree_to_infectious_diaphorinas))
			print('Los nuevos totales de diaforinas son: '+str(tree_from_diaphorinas_total)+' en el árbol origen, y '+str(tree_to_diaphorinas_total)+' en el árbol destino.\n')


		#	Modifica los campos escalares

		#	Diaforinas sanas
			self.diaphorina_scalar_field[tree_from_position[0]][tree_from_position[1]]-=migrants#from
			self.diaphorina_scalar_field[tree_to_position[0]][tree_to_position[1]]+=migrants#to

		#	Diaforinas infecciosas
			self.infected_diaphorina_scalar_field[tree_from_position[0]][tree_from_position[1]]-=infectious_migrants#from
			self.infected_diaphorina_scalar_field[tree_to_position[0]][tree_to_position[1]]+=infectious_migrants#to

		#	Diaforinas totales
			self.diaphorina_total_scalar_field[tree_from_position[0]][tree_from_position[1]]-=migrants+infectious_migrants#from
			self.diaphorina_total_scalar_field[tree_to_position[0]][tree_to_position[1]]+=migrants+infectious_migrants#to

		#	Hace los cambios pertinentes en los árboles en la positions matrix:
			if self.forestlist[tree_to_position[0]][tree_to_position[1]].diaphorina_total>0:#si el árbol to recibió diaforinas,
				if self.positions_matrix[tree_to_position[0], tree_to_position[1]]==1:#y si está en 1, 
					self.positions_matrix[tree_to_position[0], tree_to_position[1]]=2#se marca con un 2. Si ya fuera 4 o 3, no tendría sentido cambiar a 2.


			if 	self.forestlist[tree_from_position[0]][tree_from_position[1]].diaphorina_total==0:
				print('%ATENCIÓN, el árbol origen de '+str(tree_from_position+[1, 1])+' se ha quedado sin diaforinas, se lo ha marcado con un 1 para evitar errores, pero esto puede ser un error.')
		





	def update_infected_trees(self, incubation_min=200, incubation_max=200, dt=1):#Recorre toda la position matrix y sortea si se infectan árboles en función de la cantidad de diaforinas que alojen 
		
		#--------Actualización de asintomáticos

		pos=self.positions_matrix#Se llama pos a la positions matrix
		asymptomatic_positions = list(np.transpose(np.nonzero(pos==4)))#se llama asymptomatic_positions la lista 2xn con las n posiciones de los elementos iguales a 4 en pos.
		
		for site in asymptomatic_positions:#Para cada posición en la lista de árboles con asintomáticos,
			tree=self.forestlist[site[0]][site[1]]#llamamos Tree al árbol sitésimo,
			tree.incubation-=1#restamos un día a los días de incumación del árbol
			if tree.incubation==0:
				self.positions_matrix[tree.position]=3



		#--------Infección 

		def hill(x=1, incubation_min=incubation_min, incubation_max=incubation_max):#Da la probabilidad de infección en función de la ecuación de Hill
			return math.pow(x/2,2)/(1500. + math.pow(x/2,2)) #hill function of probability of infection

		pos=self.positions_matrix
		diaphorina_positions = list(np.transpose(np.nonzero(pos==2)))#es la lista 2xn con las n posiciones de los elementos iguales a 2 en pos.
		
		for site in diaphorina_positions:#Para cada posición en la lista de árboles con diaforinas,
			tree=self.forestlist[site[0]][site[1]]#llamamos Tree al árbol en esa posición,
			probability = hill(x=tree.infectious_diaphorina)*dt#probability a hill(número de diaforinas INFECTADAS del árbol)
			if random.random()<probability:
				tree.infected=True#Sorteamos si el árbol se infecta, basados en hill(número de diaforinas infectadas del árbol)
				self.positions_matrix[tree.position]=4#y lo marcamos con un 4 para asintomáticos
				tree.incubation=random.randint(incubation_min, incubation_max)#Supongamos que el período de incubación promedio es ~20 en lugar de ~200



	def update_infectious_diaphorina(self, dt=1):#Recorre position_matrix e infecta una fracción (frac) de las diaforinas de un árbol infectado (ESTA FUNCIÓN SERÁ MODIFICADA, TENER CUIDADO AQUÍ, PORQUE TOMA SOLAMENTE LOS ÁRBOLES DEL TIPO 3, Y TAMBIÉN LOS ÁRBOLES 4 INFECTAN DIAFORINAS)
		frac=0.01*dt#Esta cantidad representa la proporción de diaforinas que serán infectadas.
		pos=self.positions_matrix#Se da un alias a positions matrix.
		infected_positions = list(np.transpose(np.nonzero(pos>=3)))#Se toma una lista con las posiciones de todos los árboles infectados, tanto siontomáticos como asintomáticos,

		for site in infected_positions:#luego para elemento de esta lista;
			tree=self.forestlist[site[0]][site[1]]#da el alias tree al objeto árbol que se encuentre en site,

			tree.infectious_diaphorina += int(frac*tree.diaphorina_amount)#toma la facción frac de las diaforinas totales, y las suma a las infectadas,
			tree.diaphorina_amount -= int(frac*tree.diaphorina_amount)#y naturalmente luego las resta de las diaforinas sanas.
			self.infected_diaphorina_scalar_field[tree.position[0],tree.position[1]]=tree.infectious_diaphorina #Actualiza el campo escalar de diaforinas infectadas
			self.diaphorina_scalar_field[tree.position[0],tree.position[1]]=tree.diaphorina_amount# al igual que las sanas
			self.diaphorina_total_scalar_field[[0],tree.position[1]]=tree.infectious_diaphorina+tree.diaphorina_amount



	def update_diaphorina_amount(self, dt=1):#Hace crecer a la población de diaforinas logísticamente (ESTA FUNCIÓN SERÁ MODIFICADA, TENER CUIDADO AQUÍ, PORQUE TOMA SOLAMENTE LOS ÁRBOLES DEL TIPO 2)
		
		def logistic_growth(n):#Nos da un incremento logístico
			r=0.1
			K=400.#Alrededor de 11 mil diaforinas caben en un árbol
			return r*n*(1. - n/K)

		pos=self.positions_matrix
		diaphorina_positions = list(np.transpose(np.nonzero(pos>=2)))#Toma una lista con los árboles del tipo 2, 3, o 4.

		for site in diaphorina_positions:#Recorre las posiciones de árboles con diaforinas, y las incrementa logísticamente
			tree=self.forestlist[site[0]][site[1]]#mediante logistic_growth,
			tree.infectious_diaphorina += int((tree.infectious_diaphorina/tree.diaphorina_total)*logistic_growth(tree.diaphorina_total)*dt) #tanto a las infectadas
			tree.diaphorina_amount += int((tree.diaphorina_amount/tree.diaphorina_total)*logistic_growth(tree.diaphorina_total)*dt) #como a las sanas.
			self.infected_diaphorina_scalar_field[tree.position[0],tree.position[1]]+=tree.infectious_diaphorina #Actualiza el campo escalar de diaforinas infectadas
			self.diaphorina_scalar_field[tree.position[0],tree.position[1]]+=tree.diaphorina_amount# al igual que las sanas
			self.diaphorina_total_scalar_field[tree.position[0],tree.position[1]]+=tree.diaphorina_amount+tree.infectious_diaphorina
	
	def control(self, pesticide_period=40, pesticide_strength=0.60, cut_down_period=15, cut_down_neighbors=False):
		pos=self.positions_matrix

		#Pesticide
		if self.day%pesticide_period==0:#Si el número de día es múltiplo del período de fumigación:
			diaphorina_positions = list(np.transpose(np.nonzero(pos>=2)))
			for site in diaphorina_positions:#recorre las posiciones de árboles con diaforinas,
				tree=self.forestlist[site[0]][site[1]]#a cada árbol con diaforinas, les restará una porción pesticide_strength
				tree.infectious_diaphorina-=floor(pesticide_strength*tree.infectious_diaphorina)
				tree.diaphorina_amount-=floor(pesticide_strength*tree.diaphorina_amount)
				self.infected_diaphorina_scalar_field[tree.position[0],tree.position[1]]-=tree.infectious_diaphorina #Actualiza el campo escalar de diaforinas infectadas
				self.diaphorina_scalar_field[tree.position[0],tree.position[1]]-=tree.diaphorina_amount# al igual que las sanas
				self.diaphorina_total_scalar_field[tree.position[0],tree.position[1]]-=tree.diaphorina_amount+tree.infectious_diaphorina


		#Cut down
		if self.day%cut_down_period==0:#Si el número de día es múltiplo del período de examinación para corte:
			symptomatic_positions = list(np.transpose(np.nonzero(pos==3)))
			for site in symptomatic_positions:
				tree=self.forestlist[site[0]][site[1]]
				self.delete_tree(tree=tree)

				if cut_down_neighbors==True:
					neighbour_trees=self.get_neighbour_trees(position=site)
					for neighbour in neighbour_trees:
						tree_n=self.forestlist[neighbour[0]][neighbour[1]]
						self.delete_tree(tree=tree_n)




	def update_field(self, dt=0.1, times=2, incubation_min=200, incubation_max=200, pesticide_period=40, pesticide_strength=0.60, cut_down_period=15, cut_down_neighbors=False):#Actualiza el campo y equivale a un paso si times=1
		if self.are_there_diaphorinas==True:#Primero comprueba si el campo tiene diaforinas, si se cumple entonces
			for i in range(times):
				self.day+=1
				self.diaphorina_spread2(strength=0.3, dt=1)#toma una fraction de las diaforinas de un árbol aleatorio del tipo 2, y las mueve a algún vecino aleatorio,
				self.update_diaphorina_amount()#luego hace crecer a la población de diaforinas logísticamente, después
				self.update_infected_trees(incubation_min=incubation_min, incubation_max=incubation_min)#recorre position matrix y sortea la infección de árboles en función de la cantidad de diaforinas que alojen,
				self.update_infectious_diaphorina()#finalmente recorre position_matrix e infecta una fracción de las diaforinas de un árbol infectado.
				self.control(pesticide_period=pesticide_period, pesticide_strength=pesticide_strength, cut_down_period=cut_down_period, cut_down_neighbors=cut_down_neighbors)

			   #Modificación de las listas de stats
				self.stats_infected_trees.append(np.count_nonzero(self.positions_matrix==3))#
				self.stats_asymptomatic_trees.append(np.count_nonzero(self.positions_matrix==4))
				try:
					self.stats_asymptomatic_fraction.append(np.count_nonzero(self.positions_matrix==4)/(np.count_nonzero(self.positions_matrix==4)+np.count_nonzero(self.positions_matrix==3)))
				except:
					self.stats_asymptomatic_fraction.append(0)


				diaphorina_sum=0#Variable local mediante la que se contará el número de diaforinas que hay en el momento en el campo
				pos=self.positions_matrix#Llamamos pos a la positions_matrix
				diaphorina_positions = list(np.transpose(np.nonzero(pos!=0)))#es la lista 2xn con las n posiciones de los elementos iguales a 2 en pos.
				for site in diaphorina_positions:#Para cada posición en la lista de árboles con diaforinas infectadas
					tree=self.forestlist[site[0]][site[1]]#Llamamos Tree al árbol en esa posición,
					diaphorina_sum+=tree.diaphorina_amount#Agrega la cantidad de diaforinas del árbol tree a la suma total
				self.stats_diaphorina_amount.append(diaphorina_sum)#Agrega la cantidad de diaforinas contadas en todos los árboles en ese momento a la lista

				infected_diaphorina_sum=0#Variable local mediante la que se contará el número de diaforinas INFECTADAS que hay en el momento en el campo
				pos=self.positions_matrix#Llamamos pos a la positions_matrix
				diaphorina_positions = list(np.transpose(np.nonzero(pos!=0)))#es la lista 2xn con las n posiciones de los elementos iguales a 2 en pos.
				for site in diaphorina_positions:#Para cada posición en la lista de árboles con diaforinas infectadas
					tree=self.forestlist[site[0]][site[1]]#Llamamos Tree al árbol en esa posición,
					infected_diaphorina_sum+=tree.infectious_diaphorina#Agrega la cantidad de diaforinas INFECTADAS del árbol tree a la suma total
				self.stats_infectious_diaphorina.append(infected_diaphorina_sum)#Agrega la cantidad de diaforinas INFECTADAS contadas en todos los árboles en ese momento a la lista

				self.stats_diaphorina_total.append(diaphorina_sum+infected_diaphorina_sum)#Suma las infectadas y las sanas para obtener el total
		print('El ciclo ha concluído.')
		print('---------------------------------------------------------------------------------------------\n \n \n')



		#Métodos explícitos de interfaz--------------------------------------------------------------------------------

	def show_field(self):#~Muestra la interfaz del campo
		plt.ion()#Enciende el modo interactivo

		i=1
		if self.figure==None :
			self.figure = plt.figure()#Se da a este atributo una figura
			self.figure.add_subplot(1,1,1)#.add_subplot(x,y,z) divide la ventana en una cuadrícula de x por y t coloca a la gráfica en el lugar z 
			i=0

		plt.title('Estado del Campo en el día '+str(self.day))#Titula la gráfica
		try:
			plt.xlabel('De los '+str(self.stats_infected_trees[-1]+self.stats_asymptomatic_trees[-1])+' árboles infectados, '+str(self.stats_asymptomatic_trees[-1])+' son asintomáticos ('+str(round((100*self.stats_asymptomatic_fraction[-1]), 1))+'%)')
		except:
			pass
		ax=self.figure.get_axes()[0]
		im=ax.imshow(self.positions_matrix,cmap=colormap)
		labels=('Hueco \nsin \nárbol', 'Árbol', 'Árbol con \npsílidos', 'Árbol Infectado', 'Árbol \nasintomático')
		im.set_clim(0,4)#Aquí se configura el número de elementos a graficar (corresponden con los elementos en labels y los colores de colormap)
		if(i==0): #estas líneas han sido eliminadas debido a que no es necesaria una colorbar porque los números en esta ilustración no son importantes, lo mejor para reemplazar son etiquetas
			cb=self.figure.colorbar(im, ticks=range(5))
			cb.ax.set_yticklabels(labels)

		self.figure.canvas.draw()
		self.figure.canvas.flush_events()
		#plt.matshow(self.positions_matrix)

	def show_diaphorina(self, d_type='total'):#~Muestra la interfaz del número de diaforinas SANAS (falta incluir las enfermas) en cada punto del campo

		if d_type=='innocuous':#Si se pide que se grafiquen las diaforinas inocuas se entra en este bucle
			plt.ion()#Enciende el modo interactivo
			i=1
			if self.figure==None :
				self.figure = plt.figure()
				self.figure.add_subplot(1,1,1)#
				i=0

			plt.title('Distribución y cantidad de psílidos sanos en el día '+str(self.day))#Titula la gráfica
			ax=self.figure.get_axes()[0]
			im=ax.imshow(self.diaphorina_scalar_field,cmap='Greens')
			im.set_clim(0,300)
			if(i==0):
				self.figure.colorbar(im)
			self.figure.canvas.draw()
			self.figure.canvas.flush_events()
			#plt.matshow(self.positions_matrix)

		elif  d_type=='infectious':
			plt.ion()#Enciende el modo interactivo
			i=1
			if self.figure==None :
				self.figure = plt.figure()#Se da a este atributo una figura
				self.figure.add_subplot(1,1,1)#? 
				i=0

			plt.title('Distribución y cantidad de psílidos infectados en el día '+str(self.day))#Titula la gráfica
			ax=self.figure.get_axes()[0]
			im=ax.imshow(self.infected_diaphorina_scalar_field,cmap='Oranges')
			im.set_clim(0,300)
			if(i==0):
				self.figure.colorbar(im)
			self.figure.canvas.draw()
			self.figure.canvas.flush_events()
			#plt.matshow(self.positions_matrix)

		elif  d_type=='total':
			plt.ion()#Enciende el modo interactivo
			i=1
			if self.figure==None :
				self.figure = plt.figure()#Se da a este atributo una figura
				self.figure.add_subplot(1,1,1)#? 
				i=0

			plt.title('Distribución y cantidad de psílidos totales en el día '+str(self.day))#Titula la gráfica
			ax=self.figure.get_axes()[0]
			im=ax.imshow(self.diaphorina_total_scalar_field,cmap='Blues')
			im.set_clim(0,300)
			if(i==0):
				self.figure.colorbar(im)
			self.figure.canvas.draw()
			self.figure.canvas.flush_events()
			#plt.matshow(self.positions_matrix)

		elif d_type=='all_types':
			pass#Aquí se va a modificar la parte self.figure.add_subplot(1,1,1)# para que se muestren varias gráficas 

		else:
			print('\n \n %ERROR: La función show_diaphorina ha sido llamada pero no se ha podido ejecutar debido a que el argumento d_type es erróneo: '+str(d_type)+', comprueba su sintáxis.\n \n ')


	def show_stats(self):#Muestra en una gráfica la evolución respecto al tiempo de árboles infectados, población de diaforinas, diaforinas infectadas
		
		plt.ion()#Enciende el modo interactivo
		if self.figure_stats==None :
			self.figure_stats = plt.figure()#Se da a este atributo una figura
			self.figure_stats.add_subplot(1,1,1)#?

		ax=self.figure_stats.get_axes()[0]
		#im=ax.plot(self.stats_infected_trees, marker='.', color='darkred', label='Árboles Expuestos')
		#im=ax.plot(self.stats_asymptomatic_trees, marker='.', color='blue', label='Árboles Asintomáticos')
		im=ax.plot(self.stats_diaphorina_amount, linestyle='--', color='steelblue', label='Diaforinas Sanas')
		im=ax.plot(self.stats_infectious_diaphorina, linestyle='--', color='goldenrod', label='Diaforinas Infectadas')
		im=ax.plot(self.stats_diaphorina_total, linestyle='-', color='gray', label='Total de diaforinas')

		if self.incubation_graph==False:
			plt.legend(loc='upper left')
			self.incubation_graph=True
		self.figure_stats.canvas.draw()
		self.figure_stats.canvas.flush_events()

	def show_incubation(self, incubation_min=200, incubation_max=200):
		plt.figure(figsize=(15,6))
		plt.plot(self.stats_infected_trees, marker='.', color='darkred', label='Árboles Expuestos')
		plt.plot(self.stats_asymptomatic_trees, marker='.', color='#217531', label='Árboles Asintomáticos')
		plt.xlabel('Día')#Titula el eje x
		plt.ylabel('Cantidad de árboles')#Titula el eje y
		plt.title('Intervalo de incubación entre '+str(incubation_min)+' y '+str(incubation_max)+' días.')
		plt.legend(loc='upper left')


		plt.show()

	#Métodos implícitos de interfaz--------------------------------------------------------------------------------

	def save_field(self, name='name'):#~Muestra la interfaz del campo

		self.figure_saved = plt.figure()#Se da a este atributo una figura
		self.figure_saved.add_subplot(1,1,1)#.add_subplot(x,y,z) divide la ventana en una cuadrícula de x por y t coloca a la gráfica en el lugar z 
		plt.title('Estado del Campo en el día '+str(self.day))#Titula la gráfica
		try:
			plt.xlabel('De los '+str(self.stats_infected_trees[-1]+self.stats_asymptomatic_trees[-1])+' árboles infectados, '+str(self.stats_asymptomatic_trees[-1])+' son asintomáticos ('+str(round((100*self.stats_asymptomatic_fraction[-1]), 1))+'%)')
		except:
			pass
		ax=self.figure_saved.get_axes()[0]
		im=ax.imshow(self.positions_matrix,cmap=colormap)
		labels=('Hueco', 'Árbol', 'Diaforinas', 'Árbol Infectado', 'Árbol \nasintomático')
		im.set_clim(0,4)#Aquí se configura el número de elementos a graficar (corresponden con los elementos en labels y los colores de colormap)
		cb=self.figure_saved.colorbar(im, ticks=range(5))
		cb.ax.set_yticklabels(labels)

		self.figure_saved.canvas.draw()
		self.figure_saved.canvas.flush_events()
		plt.savefig(name+'/'+name+' día '+str(self.day))
		plt.close(self.figure_saved)

	def save_incubation(self, name='field', incubation_min=200, incubation_max=200):
		plt.figure(figsize=(15,6))
		plt.plot(self.stats_infected_trees, marker='.', color='darkred', label='Árboles Infectados')
		plt.plot(self.stats_asymptomatic_trees, marker='.', color='#217531', label='Árboles Asintomáticos')
		plt.xlabel('Día')#Titula el eje x
		plt.ylabel('Cantidad de árboles')#Titula el eje y
		plt.title('Intervalo de incubación entre '+str(incubation_min)+' y '+str(incubation_max)+' días.')
		plt.legend(loc='upper left')
		plt.savefig(name+'/árboles '+name+' día '+str(self.day))
		plt.close()

	def save_stats(self, name='field'):#Muestra en una gráfica la evolución respecto al tiempo de árboles infectados, población de diaforinas, diaforinas infectadas
		
		plt.figure()#Se da a este atributo una figura
		plt.plot(self.stats_diaphorina_amount, linestyle='--', color='steelblue', label='Psílidos Sanos')
		plt.plot(self.stats_infectious_diaphorina, linestyle='--', color='goldenrod', label='Psílidos Infectados')
		plt.plot(self.stats_diaphorina_total, linestyle='-', color='gray', label='Total de Psílidos')
		plt.xlabel('Centenas de psílidos')#Titula el eje x
		plt.ylabel('Tiempo en días')#Titula el eje y
		#plt.title('Intervalo de incubación entre '+str(incubation_min)+' y '+str(incubation_max)+' días.')
		plt.legend(loc='upper left')
		plt.savefig(name+'/diaforinas '+name+' día '+str(self.day))
		plt.close()

	def save_diaphorina(self, name='field'):#~Muestra la interfaz del número de diaforinas SANAS (falta incluir las enfermas) en cada punto del campo

		self.figure_s= plt.figure()
		self.figure_s.add_subplot(1,1,1)#
		plt.title('Distribución de psílidos sanos en el día '+str(self.day))#Titula la gráfica
		ax=self.figure_s.get_axes()[0]
		im=ax.imshow(self.diaphorina_scalar_field,cmap='Greens')
		im.set_clim(0,300)
		self.figure_s.colorbar(im)
		self.figure_s.canvas.draw()
		self.figure_s.canvas.flush_events()
		plt.savefig(name+'/sanas '+name+' día '+str(self.day))
		plt.close(self.figure_s)

		self.figure_i= plt.figure()#Se da a este atributo una figura
		self.figure_i.add_subplot(1,1,1)#? 
		plt.title('Distribución de psílidos infectados en el día '+str(self.day))#Titula la gráfica
		ax=self.figure_i.get_axes()[0]
		im=ax.imshow(self.infected_diaphorina_scalar_field,cmap='Oranges')
		im.set_clim(0,300)
		self.figure_i.colorbar(im)
		self.figure_i.canvas.draw()
		self.figure_i.canvas.flush_events()
		plt.savefig(name+'/infectadas '+name+' día '+str(self.day))
		plt.close(self.figure_i)

		self.figure_t= plt.figure()#Se da a este atributo una figura
		self.figure_t.add_subplot(1,1,1)#? 
		plt.title('Distribución de psílidos totales en el día '+str(self.day))#Titula la gráfica
		ax=self.figure_t.get_axes()[0]
		im=ax.imshow(self.diaphorina_total_scalar_field,cmap='Blues')
		im.set_clim(0,300)
		self.figure_t.colorbar(im)
		self.figure_t.canvas.draw()
		self.figure_t.canvas.flush_events()
		plt.savefig(name+'/totales '+name+' día '+str(self.day))
		plt.close(self.figure_t)



#-------------------------- Fin de las clases --------------------------------


#Tabla de números de estado de la forestlist:
'''
0: Si la casilla no tiene árbol
1: Si la casilla tiene un árbol normal
2: Si aloja diaforinas
3: Si el árbol está infectado
4: Si el árbol está infectado y es asintomático
'''


