import heapq
import networkx as nx
import matplotlib.pyplot as plt

#bing chilling


#clase estacion con nombre y conexiones
class Estacion:
    def __init__(self, nombre):
        self.nombre = nombre
        
    def __lt__(self, other):
        return self.nombre < other.nombre

# Lista de conexiones
conexiones = []

def agregar_conexion(origen, destino, tiempo):
    conexiones.append((origen, destino, tiempo))

def ruta_mas_rapida(origen, destino):
    nodosVisitados=[]
    ruta=[]
    nodoActual=origen
    #while destino not in nodosVisitados:

def ruta_mas_optima(origen, destino):
    # Crear un grafo vacío
    grafo = nx.Graph()

    # Agregar las conexiones al grafo
    for conexion in conexiones:
        origen, destino, tiempo = conexion
        grafo.add_edge(origen, destino, weight=tiempo)

    # Calcular la ruta más óptima utilizando A*
    ruta_optima = nx.astar_path(grafo, origen, destino, weight='weight')

    return ruta_optima

# Llamar a la función para obtener la ruta más óptima
ruta_optima = ruta_mas_optima(inicio, fin)

# Imprimir la ruta más óptima
print(ruta_optima)
    
#clase ruta con estaciones
class Ruta:
    def __init__(self):
        self.estaciones = []

    def agregar_estacion(self, estacion):
        self.estaciones.append(estacion)

#funcion que calcula la ruta mas rapida

inicio = Estacion("Inicio")
fin = Estacion("Fin")
estacion_a = Estacion("Estacion A")
estacion_b = Estacion("Estacion B")
agregar_conexion(inicio, estacion_a, 5)
agregar_conexion(inicio, estacion_b, 7)
agregar_conexion(estacion_a, fin, 3)
agregar_conexion(estacion_b, fin, 4)
ruta = ruta_mas_optima(inicio, fin)