# ================================================================= #
# ==================== DEFINICIÓN DE VARIABLES ==================== #
# ================================================================= #

# Creación de la lista adyacente, diccionario en el que se almacenarán las conexiones entre nodos
metro_madrid = {}

# Creación de la lista en la que se almacenará la información del csv, guardando en sublistas que representan líneas, las estaciones de cada línea de forma ordenada
estaciones_lineas = []

# Diccionario que relaciona las sublistas de la variable de estaciones_lineas con su línea correspondiente
lineas_metro = {
    0:"LINEA 1",
    1:"LINEA 10a",
    2:"LINEA 10b",
    3:"LINEA 11",
    4:"LINEA 12-1",
    5:"LINEA 2",
    6:"LINEA 3",
    7:"LINEA 4",
    8:"LINEA 5",
    9:"LINEA 6-1",
    10:"LINEA 7a",
    11:"LINEA 7b",
    12:"LINEA 8",
    13:"LINEA 9A",
    14:"LINEA 9B",
    15:"LINEA R",
}

# ========================================================= #
# ================ DEFINICIÓN DE FUNCIONES ================ #
# ========================================================= #

# Función para crear un vértice
def create_node(node):
    node = node.upper()

    if node not in metro_madrid:
        metro_madrid[node] = []

# Función para agregar una conexión entre dos estaciones (se crean en caso de no existir, los vértices y las aristas a la vez)
def add_connection(station1, station2):
    station1 = station1.upper()
    station2 = station2.upper()
    
    if station1 not in metro_madrid:
        metro_madrid[station1] = []
    if station2 not in metro_madrid:
        metro_madrid[station2] = []

    metro_madrid[station1].append(station2)
    metro_madrid[station2].append(station1)

# Función para eliminar un vértice y todas sus aristas
def erase_node(node):
    node = node.upper()

    adjacent_nodes = find_adjacent_nodes(node)
    del metro_madrid[node]
    
    for station in adjacent_nodes:
        metro_madrid[station].remove(node)

# Función para eliminar las aristas entre dos nodos en ambos sentidos
def erase_edge(node1,node2):
    node1 = node1.upper()
    node2 = node2.upper()

    metro_madrid[node1].remove(node2)
    metro_madrid[node2].remove(node1)

    
# Función que te retorna los nodos adyacentes de un nodo dado, busca un vértice y te devuelve sus nodos adyacentes
def find_adjacent_nodes(node):
    node = node.upper()

    if node in metro_madrid:
        return metro_madrid[node]
    
    else:
        return "No existe ese vértice"

# Función para imprimir las conexiones
def show_adjacent_nodes():
    for station, connections in metro_madrid.items():
        print(f"Estación {station}: Conexiones -> {connections}")

# Función que te retorna la línea/s a la que pertenece una estación
def station_line(station):
    station = station.upper()
    lineas = []
    
    for index_line, line in enumerate(estaciones_lineas):
        if station in line:
            lineas.append(lineas_metro[index_line])
            
    return lineas

# Función que te retorna el número de vértices del grafo
def calc_nodes_number():
    return len(metro_madrid)

# ------------------->  CREACIÓN DE ALGORITMOS <------------------- #

# Función find_path mejorada, para encontrar un camino cualquiera de un punto A a un punto B
def find_path(station1, station2):
    station1 = station1.upper()
    station2 = station2.upper()
    
    # Crea un set para almacenar las estaciones visitadas
    visited = set()

    # Crea una variable path para almacenar la ruta como una lista
    path = []
    
    # Función que emplea el algoritmo depth first search para recorrer el grafo y encontrar un camino
    def dfs(current_station):
        # Añade la estación actual a path
        path.append(current_station)
        # Añade la estación actual a visited
        visited.add(current_station)

        # Si la estación en la que nos encontramos coincide con la estación de destino, retorna True
        if current_station == station2:
            return True

        # Itera sobre las estaciones adyacentes
        for adjacent_station in find_adjacent_nodes(current_station):
            # Si la estación adyacente no ha sido visitada, usa recursividad y llama la función dfs
            if adjacent_station not in visited:
                if dfs(adjacent_station):
                    return True

        # Si no encuentra ninguna ruta, elimina la estación actual de la ruta y retorna False 
        path.pop()
        return False

    # Si la station inicial no se encuentra en el grafo, retorna "No existe esta estación"
    if station1 not in metro_madrid:
        return "No existe esta estación"

    # Llama a la función dfs y le pasa station1 como parámetro de estación actual
    if dfs(station1):
        return path
    else:
        return "No path found"
        

# Función find_path mejorada, para encontrar un camino cualquiera de un punto A a un punto B, en esta versión tiene en cuenta si las dos estaciones pertenecen a la misma línea, aunque falta mejorarla, ya que en algunos casos da error 
def find_path_improved(station1, station2):
    station1 = station1.upper()
    station2 = station2.upper()

    # Si ambas estaciones pertenecen a la misma línea:
    if any(element in station_line(station2) for element in station_line(station1)):
        
        for line in estaciones_lineas:
            if station1 in line:
                
                # Al ser nuestro grafo no dirigido, es decir, que cada vértice tiene aristas bidireccionales, controlamos mediante condicionales que se haga la lectura de los datos en el orden correcto
                if line[line.index(station1):line.index(station2)+1]:
                    return line[line.index(station1):line.index(station2)+1]
                
                else:
                    return line[line.index(station2):line.index(station1)+1]
    
    # En caso de que no se encuentren en la misma línea:
    else:
    
        # Crea un set para almacenar las estaciones visitadas
        visited = set()

        # Crea una variable path para almacenar la ruta como una lista
        path = []
        
        # Función que emplea el algoritmo depth first search para recorrer el grafo y encontrar un camino
        def dfs(current_station):
            # Añade la estación actual a path
            path.append(current_station)
            # Añade la estación actual a visited
            visited.add(current_station)

            # Si la estación en la que nos encontramos coincide con la estación de destino, retorna True
            if current_station == station2:
                return True

            # Itera sobre las estaciones adyacentes
            for adjacent_station in find_adjacent_nodes(current_station):
                # Si la estación adyacente no ha sido visitada, usa recursividad y llama la función dfs
                if adjacent_station not in visited:
                    if dfs(adjacent_station):
                        return True

            # Si no encuentra ninguna ruta, elimina la estación actual de la ruta y retorna False 
            path.pop()
            return False

        # Si la station inicial no se encuentra en el grafo, retorna "No existe esta estación"
        if station1 not in metro_madrid:
            return "No existe esta estación"

        # Llama a la función dfs y le pasa station1 como parámetro de estación actual
        if dfs(station1):
            return path
        else:
            return "No path found"


# ========================================================= #
# ==================== LECTURA DEL CSV ==================== #
# ========================================================= #

# Nombre del archivo CSV a leer
nombre_archivo = 'lineas_metroMadrid.csv'

datos_lineasMetroMadrid = []

# Control de excepciones en caso de que no encuentre el archivo csv
try:
    # Abrir el archivo CSV en modo lectura
    with open(nombre_archivo, 'r') as archivo:

        # Iterar sobre cada línea en el archivo
        for linea in archivo:
            # Dividir la línea en valores separados por comas
            valores = linea.strip().split(',')
            # Agregar los valores a la lista de datos
            datos_lineasMetroMadrid.append(valores)
            
except FileNotFoundError:
    print("¡No se está encontrando el archivo csv, por favor, asegurate de que lo has descargado y que está en la misma carpeta que este programa!")   

# =============================================================== #
# ==================== PROCESAMIENTO DEL CSV ==================== #
# =============================================================== #
        
# Bucle que añade a la lista una sublista vacía por línea de metro para posteriormente añadirle las estaciones a cada una
for x in range(17):
    estaciones_lineas.append([])

# Bucle anidado que añade las estaciones de cada línea a su correspondente sublista y elimina los espacios vacíos
for i in range(0, 17):
    for index_row, row in enumerate(datos_lineasMetroMadrid):
        element = datos_lineasMetroMadrid[index_row][i]
        
        # Elimina los espacios vacíos
        if element != '':
            estaciones_lineas[i].append(datos_lineasMetroMadrid[index_row][i])

# Elimina el primer elemento de la lista
estaciones_lineas.pop(0)

# Elimina el número de línea al principio de cada sublista
estaciones_lineas = [linea[1:] for linea in estaciones_lineas]

# ==================================================================== #
# ==================== CREACIÓN DE LAS CONEXIONES ==================== #
# ==================================================================== #

# Añade las conexiones de todas las estaciones a la lista adyacente
for row_index, row in enumerate(estaciones_lineas):
    for i in range(0, len(row)-1):
        add_connection(row[i], row[i+1])  

# =============================================================== #
# ==================== EJECUCIÓN EN PANTALLA ==================== #
# =============================================================== #

# print(estaciones_lineas)

# print('-------------'*8)

# print(station_line("MONCLOA"))

# print('-------------'*8)

# print(show_adjacent_nodes())

# print(station_line("Avenida de America"))

# print(find_adjacent_nodes("Pueblo Nuevo"))

print(find_path("PUERTA DE ARGANDA","TETUAN"))
