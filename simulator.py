from main import *
import random
import os

#-----------------------------------------------------------Definiciones

def run_field(name='field', dimensions=(49,62), cycles=20, times=5, show='field', incubation_min=200, incubation_max=200, save=True, pesticide_period=40, pesticide_strength=0.60, cut_down_period=15, cut_down_neighbors=False):#Esta función hace correr la simulación; actualiza con times iteraciones de update_field(),
    #durante cycles ciclos. El tercer argumento puede ser 'field', 'stats', 'innocuous', 'infectious' o 'total' según la gráfica que se quiera.

    if save==True:
        os.mkdir(name)
    name_field_string=name
    print('Simulación iniciada.')#Se inicia la simulación,
    name = Field(dimensions)#se crea un campo de 17x21 huecos para árboles,
    print('Creando campo de '+str(name.size[0])+' de alto, por '+str(name.size[1])+' de ancho.')
    name.fill_random(0.999)#se llena el 98% delcampo con árboles, dejando algunos huecos aleatorios.
    name.set_diaphorina_in_random_tree(diaphorina_amount=85,infectious_diaphorina=15)#asigna a un árbol aleatorio 99 diaforinas sanas y 1 infecciosa


    for i in range(cycles):#Este es bucle que  hace que el campo evolucione mediante de la función que actualiza el campo update_field().
        
        #Después, comienza la parte encargada de graficar según el argumento show;

        if show=='field':#Si se pide el campo de árboles (la matriz de posiciones),
            name.show_field()#Muestra los árboles, si están sanos o infectados, y si son asintomáticos o si sólo alojan diaforinas.
        
        elif show=='stats':#Si se piden las estadísticas,
            name.show_stats()#Muestra el crecimiento de las poblaciones y las infeciones a través de cada paso.

        elif show=='none':
            pass

        elif show=='incubation':
            name.show_incubation(incubation_min=incubation_min, incubation_max=incubation_max)

        else:
            name.show_diaphorina(d_type=show)#Muestra la distribución y cantidad de diaforinas a través del campo, además se puede pedir que sólo muestre las infecciosas o sólo las sanas

        if save==True:
            name.save_field(name=name_field_string)
            name.save_incubation(name=name_field_string, incubation_min=incubation_min, incubation_max=incubation_max)
            name.save_stats(name=name_field_string)
            name.save_diaphorina(name=name_field_string)


        print(' Día '+str(name.day)+' de '+str(times*cycles))
        print('Comienza el ciclo '+str(i+1)+' de los '+str(cycles)+' totales. Tamaño del ciclo: '+str(times))
        name.update_field(dt=0.1, times=times, incubation_min=incubation_min, incubation_max=incubation_min, pesticide_period=pesticide_period, pesticide_strength=pesticide_strength, cut_down_period=cut_down_period, cut_down_neighbors=cut_down_neighbors)#Esta es la función update_field(); actualiza el campo con un dt=0.1, dando "times" iteraciones.

    print('\n Simulación terminada con éxito' ) 


#-----------------------------------------------------------Ejecución

#-----------------------------Simulaciones de control

run_field(name='Control1', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=40000, 
    pesticide_strength=0.0, cut_down_period=10005, cut_down_neighbors=False)
run_field(name='Control2', cycles=8, times=30, show='none', incubation_min=165, incubation_max=235, dimensions=(49,62), save=True, pesticide_period=40000, 
    pesticide_strength=0.0, cut_down_period=10005, cut_down_neighbors=False)
run_field(name='Control3', cycles=8, times=30, show='none', incubation_min=180, incubation_max=220, dimensions=(49,62), save=True, pesticide_period=40000, 
    pesticide_strength=0.0, cut_down_period=10005, cut_down_neighbors=False)

#-----------------------------Pesticidas

run_field(name='Pesticida1', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=90, 
    pesticide_strength=0.5, cut_down_period=10005, cut_down_neighbors=False)
run_field(name='Pesticida2', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=90, 
    pesticide_strength=0.7, cut_down_period=10005, cut_down_neighbors=False)
run_field(name='Pesticida3', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=90, 
    pesticide_strength=0.9, cut_down_period=10005, cut_down_neighbors=False)

run_field(name='Pesticida4', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=60, 
    pesticide_strength=0.7, cut_down_period=10005, cut_down_neighbors=False)
#run_field(name='Pesticida5', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=90, 
#    pesticide_strength=0.7, cut_down_period=10005, cut_down_neighbors=False) REPETIDO
run_field(name='Pesticida6', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=180, 
    pesticide_strength=0.7, cut_down_period=10005, cut_down_neighbors=False)

#-----------------------------Corte

run_field(name='Corte1', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=900, 
    pesticide_strength=0.7, cut_down_period=90, cut_down_neighbors=False)
run_field(name='Corte2', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=900, 
    pesticide_strength=0.7, cut_down_period=60, cut_down_neighbors=False)
run_field(name='Corte3', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=900, 
    pesticide_strength=0.7, cut_down_period=15, cut_down_neighbors=False)

run_field(name='CorteVecinos', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=90, 
    pesticide_strength=0.7, cut_down_period=90, cut_down_neighbors=True)

#-----------------------------Métodos conjuntos

run_field(name='PesticidaCorte', cycles=8, times=30, show='none', incubation_min=150, incubation_max=250, dimensions=(49,62), save=True, pesticide_period=90, 
    pesticide_strength=0.7, cut_down_period=90, cut_down_neighbors=True)