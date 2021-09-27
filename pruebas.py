from main import *

#Prueba: creación de campo, de árbol; positions_matrix, forestlist. Métodos delete y add.
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

#Prueba: Método fill
'''field_2=Field((10, 10))
print("Forestlist -Campo2 virgen-")
print(field_2.forestlist)
print("")
print("Posiciones -Campo2 virgen-")
print(field_2.positions_matrix)
print("")
field_2.fill(age=3, diaphorina=True)
print("Forestlist -Campo2 filled-")
print(field_2.forestlist)
print("")
print("Posiciones -Campo2 filled-")
print(field_2.positions_matrix)
print("")
'''

#Prueba: Objeto diaforina, método infection. Se quiere ver si los árboles infectados se ven con 7 en position_matrix
'''
field_3=Field((20,10))
diaforina_1=Diaphorina(field_3)
tree_1=Tree((0, 4), field=field_3)
tree_2=Tree((2, 3), field=field_3)
tree_3=Tree((3, 5), field=field_3)
field_3.add_tree(tree_1)
field_3.add_tree(tree_2)
field_3.add_tree(tree_3)
tree_1.diaphorina_amount=10
tree_1.manual_infection()
print('It is '+str(tree_1.infected)+' that this tree is infected')
tree_2.diaphorina_amount=10
tree_2.manual_infection()
tree_3.diaphorina_amount=0
tree_3.manual_infection()
print("Forestlist")
print(field_3.forestlist)
print("")
print("Posiciones")
print(field_3.positions_matrix)
print("")
'''

#Prueba: infectar aleatoriamente un campo filled

field_4=Field((10,10))
field_4.fill(age=1, diaphorina=True, infected=True)
print(field_4.positions_matrix)















#Commit 19/9/21:
#-Completado	Definir la clase diaforina

#Commit del 27/9/21:
#-Completado	Hacer que si un árbol está infectado se vea como un 7 en position matrix (no se muestra ningún 7 luego de usar manual_infection)

#Pendientes:
#Crear una diaphorina_matrix que nos diga el número de diaforinas que hay 
#Hacer que al crear un árbol, se creen los objetos diaforina en él si es que diaphorina_amount!=0
#Dar una forma de distribuir las diaforinas con el modelo hecho en el capítulo 19
#Hacer algo para verlo gráficamente
#Hacer una librería HLB para sólo llamar las clases