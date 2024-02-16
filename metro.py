import heapq
import tkinter as tk
from tkinter import Tk,ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Datos import metro_map, tiempos_estimados, estaciones_por_ruta
from PIL import ImageTk, Image


# Declaración de funciones
def calcular_heuristica_transbordos(estacion_actual, estacion_final, metro_map, estaciones_por_ruta):
    # Obtén las rutas que sirven para la estación actual y final
    rutas_estacion_actual = obtener_rutas_que_pasan_por_estacion(estacion_actual, estaciones_por_ruta)
    rutas_estacion_final = obtener_rutas_que_pasan_por_estacion(estacion_final, estaciones_por_ruta)

    # Encuentra la cantidad mínima de trasbordos necesarios
    min_transbordos = float('inf')
    for ruta_actual in rutas_estacion_actual:
        for ruta_final in rutas_estacion_final:
            transbordos = len(set(ruta_actual) & set(ruta_final))
            min_transbordos = min(min_transbordos, transbordos)

    return min_transbordos

def obtener_rutas_que_pasan_por_estacion(estacion, estaciones_por_ruta):
    rutas_que_pasan = []
    for ruta, estaciones in estaciones_por_ruta.items():
        if estacion in estaciones:
            rutas_que_pasan.append(ruta)
    return rutas_que_pasan

def a_estrella(metro_map, tiempos_estimados, estacion_inicial, estacion_final, estaciones_por_ruta):
    heap = [(0, estacion_inicial, [])]
    visitado = set()

    while heap:
        (costo_actual, estacion_actual, ruta_actual) = heapq.heappop(heap)
        print(f"COSTO ACTUAL: {costo_actual}, ESTACIÓN ACTUAL: {estacion_actual}")
        if estacion_actual in visitado:
            continue

        visitado.add(estacion_actual)
        ruta_actual = ruta_actual + [estacion_actual]

        if estacion_actual == estacion_final:
            for i, estacion in enumerate(ruta_actual):
                costo_actual = sum([tiempos_estimados.get((ruta_actual[i], ruta_actual[i + 1]), 0) for i in range(len(ruta_actual) - 1)])
            return costo_actual, ruta_actual

        for vecino in metro_map[estacion_actual]:
            costo = costo_actual + tiempos_estimados.get((estacion_actual, vecino), float('inf'))
            heuristica = calcular_heuristica_transbordos(vecino, estacion_final, metro_map, estaciones_por_ruta)
            costo_total = costo + heuristica
            heapq.heappush(heap, (costo_total, vecino, ruta_actual))

    # If destination station is not reachable from the initial station, return a high cost and an empty route
    return float('inf'), []

def visualizar_grafo(metro_map, ruta_optima, tiempo_optimo):
    global estacion_inicial, estacion_final
    fig = Figure(dpi=100)
    plot = fig.add_subplot()
    # Crear un grafo dirigido a partir del mapa del metro
    G = nx.DiGraph(metro_map)

    # Definir una disposición personalizada basada en la ubicación geográfica
    pos = {
        'Arcos de Zapopan': (0, 0),
        'Periferico Belenes': (1, -1),
        'Mercado del Mar': (2, -1.5),
        'Zapopan Centro': (3, -3),
        'Plaza Patria': (4, -4),
        'Circunvalacion Country': (5, -5),
        'Avila Camacho': (7, -6),
        'Normal': (8, -7),
        'Santuario': (9, -9),
        'Plaza Universidad': (9, -10),
        'Independencia': (10, -13),
        'Plaza de la Bandera': (11, -14),
        'CUCEI': (12, -15),
        'Revolucion': (13, -16),
        'Rio Nilo': (14, -17),
        'Tlaquepaque Centro': (15, -18),
        'Lazaro Cardenas': (16, -19),
        'Central de Autobuses': (17, -20),
        'Auditorio': (7, -1),
        'Periferico Norte': (7, -2),
        'Dermatologico': (7, -3),
        'Atemajac': (7, -4),
        'Division del Norte': (7, -5),
        'Mezquitan': (7, -7),
        'Refugio': (7, -8),
        'Juarez': (7, -9),
        'Mexicaltzingo': (7, -10),
        'Washington': (7, -11),
        'Santa Filomena': (7, -12),
        'Unidad Deportiva': (6, -14),
        'Urdaneta': (5, -15),
        '18 de Marzo': (4, -16),
        'Isla Raza': (3, -17),
        'Patria Sur': (2, -18),
        'España': (1, -19),
        'Tesoro': (1, -20),
        'Periferico Sur': (1, -21),
        'San Juan de Dios': (11, -11),
        'Belisario Dominguez': (12, -10),
        'Oblatos': (13, -11),
        'Cristobal de Oñate': (14, -10),
        'San Andres': (15, -11),
        'San Jacinto': (16, -10),
        'La Aurora': (17, -11),
        'Tetlan': (18, -10),
    }
    # Dibujar nodos y aristas
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color='lightblue', ax=plot)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, ax=plot)

    # Dibujar etiquetas de las estaciones
    labels = {estacion: estacion for estacion in G.nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=plot)
    
    # Colorear nodo de estación inicial en verde
    nx.draw_networkx_nodes(G, pos, nodelist=[estacion_inicial], node_size=50, node_color='green', ax=plot)
    
    # Colorear nodo de estación final en rojo+
    nx.draw_networkx_nodes(G, pos, nodelist=[estacion_final], node_size=50, node_color='red', ax=plot)
    
    # Dibujar la ruta óptima en rojo
    edges_ruta_optima = [(ruta_optima[n], ruta_optima[n + 1]) for n in range(len(ruta_optima) - 1)]
    
    nx.draw_networkx_edges(G, pos, edgelist=edges_ruta_optima, edge_color='red', width=2, ax=plot)

    # Dibujar etiquetas de las estaciones
    labels = {estacion: estacion for estacion in G.nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, ax=plot)
    ventanaRutaOptima = tk.Toplevel(ventana)
    ventanaRutaOptima.title("Ruta Óptima")
    ventanaRutaOptima.state("zoomed")
    ruta_optima_label = tk.Label(ventanaRutaOptima, text=f"Ruta óptima: {' -> '.join(ruta_optima)}", font="Arial 12 bold", wraplength=screen_width)
    ruta_optima_label.pack()
    tiempoOptimo = tk.Label(ventanaRutaOptima, text=f"Tiempo estimado: {tiempo_optimo} minutos", font="Arial 14 bold")
    tiempoOptimo.pack()
    canvas = FigureCanvasTkAgg(fig, master=ventanaRutaOptima)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Reiniciar valores estaciones
    button_dict[f"boton_{estacion_inicial}"].config(style="TButton")
    button_dict[f"boton_{estacion_final}"].config(style="TButton")
    estacion_inicial = None
    estacion_final = None

def seleccionar_estaciones(event):
    global estacion_inicial, estacion_final
    estacion_seleccionada = event.widget.cget("text")
    if estacion_seleccionada == estacion_inicial:
        button_dict[f"boton_{estacion_seleccionada}"].config(style="TButton")
        estacion_inicial = None
        print("Estación inicial deseleccionada.")
    elif estacion_seleccionada == estacion_final:
        estacion_final = None
        button_dict[f"boton_{estacion_seleccionada}"].config(style="TButton")
        print("Estación final deseleccionada.")
    elif not estacion_inicial:
        estacion_inicial = estacion_seleccionada
        button_dict[f"boton_{estacion_seleccionada}"].config(style="botonInicio.TButton") 
        print(f"Estación inicial seleccionada: {estacion_inicial}")
    elif not estacion_final:
        estacion_final = estacion_seleccionada
        button_dict[f"boton_{estacion_seleccionada}"].config(style="botonDestino.TButton")
        print(f"Estación final seleccionada: {estacion_final}")

def calcular_ruta_optima():
    global estacion_inicial, estacion_final
    if estacion_inicial and estacion_final:
        tiempo_optimo, ruta_optima = a_estrella(metro_map, tiempos_estimados, estacion_inicial, estacion_final, estaciones_por_ruta)
        visualizar_grafo(metro_map, ruta_optima, tiempo_optimo)
        
    else:
        print("Debe seleccionar una estación inicial y una estación final.")

ventana = tk.Tk()
ventana.title("Seleccionar Estaciones")
ventana.state("zoomed")

ventana.config(background="#ffffff")
# Obtener el tamaño de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

titulo= tk.Label()
titulo.config(text="METRO BLITZ",font="Arial 30 bold", justify="center")
titulo.grid(row=0, columnspan=7, column=0)
instrucciones = tk.Label()
instrucciones.config(text="Seleccione la estacion inicial y la estacion final", font="Arial 15", justify="center")
instrucciones.grid(row=1, columnspan=7, column=0)
# Abrir la imagen
image = Image.open("mapa-lineas-del-metro-guadalajara-1.png")
# Calcular la relación de aspecto de la imagen
aspect_ratio = image.width / image.height
# Calcular el nuevo tamaño manteniendo la relación de aspecto
if screen_height > screen_width:
    new_width = screen_width-200
    new_height = int(new_width / aspect_ratio)
else:
    new_height = screen_height-200
    new_width = int(new_height * aspect_ratio)

# Redimensionar la imagen al nuevo tamaño
image = image.resize((new_width, new_height), Image.LANCZOS)
# Crear un objeto PhotoImage
photo = ImageTk.PhotoImage(image)
# Crear un Label para ver la imagen
image_label = ttk.Label(ventana, image=photo)
image_label.grid(column=4, row=2, rowspan=15)  # Adjust the row and column as needed

logo = Image.open("logoMetroBlitz.png")
as_ratio = logo.width / logo.height
# Calcular el nuevo tamaño manteniendo la relación de aspecto
if screen_height > screen_width:
    nw_width = screen_width/8
    nw_height = int(nw_width / as_ratio)
else:
    nw_height = screen_height/8
    nw_width = int(nw_height * as_ratio)

logo = logo.resize((nw_width, nw_height), Image.LANCZOS)
logoTk = ImageTk.PhotoImage(logo)
logo_label = ttk.Label(ventana, image=logoTk)
logo_label.grid(column=0, row=0)  # Adjust the row and column as needed


style = ttk.Style()
style.configure(".TButton", background="#ffffff")
style.configure(".TLabel", background="#ffffff")
style.configure("botonInicio.TButton", padding=6, relief="SUNKEN", background="green", foreground="green")
style.map('botonInicio.TButton', background=[('active','green')])
style.configure("botonDestino.TButton", padding=6, relief="SUNKEN", background="red", foreground="red")
style.configure("botonBuscar.TButton", padding=6, relief="SUNKEN", font="Arial 20 bold", justify="center")
# Crear botones para las estaciones
columna = 0
fila = 2
button_dict = {}
for estacion in metro_map.keys():
    boton = ttk.Button(ventana, text=estacion)
    boton.grid(row=fila, column=columna)
    boton.bind("<Button-1>", seleccionar_estaciones)
    button_dict[f"boton_{estacion}"] = boton
    columna += 1
    if columna > 2:  # Cambiar el número 2 por el número de columnas deseado
        columna = 0
        fila += 1

# Crear botón para calcular ruta óptima
boton_calcular = ttk.Button(ventana, text="Calcular Ruta Óptima", command=calcular_ruta_optima, style="botonBuscar.TButton")
boton_calcular.grid(row=2, column=5, columnspan=2, rowspan=15)  # Cambiar el número 3 por el número de columnas deseado


# Inicializar variables
estacion_inicial = None
estacion_final = None

# Mostrar ventana
ventana.mainloop()