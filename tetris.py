import os
import random
import time

# --- CONSTANTES GLOBALES ---
# Definen el tamaño del área de juego.
ANCHO_TABLERO = 10
ALTO_TABLERO = 20

# Archivo para persistir los puntajes más altos.
PUNTAJES_ARCHIVO = "puntajes.txt"

# Definición de las formas de los tetrominós.
# Cada pieza es una matriz 4x4 donde 1 representa un bloque de la pieza.
# Este enfoque es muy eficiente en memoria.
PIEZAS = [
    [[0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0]],  # O (Cuadrado)
    [[0,1,0,0], [0,1,0,0], [0,1,0,0], [0,1,0,0]],  # I (Palo)
    [[0,0,0,0], [0,1,1,0], [1,1,0,0], [0,0,0,0]],  # S
    [[0,0,0,0], [1,1,0,0], [0,1,1,0], [0,0,0,0]],  # Z
    [[0,0,0,0], [0,1,0,0], [1,1,1,0], [0,0,0,0]],  # T
    [[0,0,0,0], [0,0,1,0], [1,1,1,0], [0,0,0,0]],  # L
    [[0,0,0,0], [1,0,0,0], [1,1,1,0], [0,0,0,0]],  # J
]

# --- FUNCIONES DE LÓGICA DEL JUEGO ---

def crear_tablero():
    """Crea un tablero de juego vacío representado por una matriz de ceros."""
    return [[0 for _ in range(ANCHO_TABLERO)] for _ in range(ALTO_TABLERO)]

def crear_pieza_nueva():
    """Selecciona una pieza aleatoria de la lista de PIEZAS."""
    return random.choice(PIEZAS)

def rotar_pieza(pieza):
    """
    Rota una pieza 90 grados en sentido horario usando un algoritmo eficiente.
    1. Transposición: Las filas se convierten en columnas.
    2. Inversión de filas: Se invierte el orden de los elementos en cada fila.
    Esto es mucho más rápido que usar librerías de geometría complejas.
    """
    # Paso 1: Transponer la matriz
    transpuesta = [list(i) for i in zip(*pieza)]
    
    # Paso 2: Invertir el orden de cada fila
    return [row[::-1] for row in transpuesta]

def es_colision(tablero, pieza, pos_x, pos_y):
    """
    Verifica si una pieza en una posición dada colisiona con los bordes
    del tablero o con otras piezas ya fijadas.
    """
    for fila_idx, fila in enumerate(pieza):
        for col_idx, celda in enumerate(fila):
            if celda == 1:
                # Coordenadas en el tablero principal
                tablero_y = pos_y + fila_idx
                tablero_x = pos_x + col_idx
                
                # Comprobar colisión con los bordes
                if not (0 <= tablero_x < ANCHO_TABLERO and 0 <= tablero_y < ALTO_TABLERO):
                    return True
                
                # Comprobar colisión con otras piezas (si la celda del tablero no está vacía)
                if tablero[tablero_y][tablero_x] == 1:
                    return True
    return False

def unir_pieza_al_tablero(tablero, pieza, pos_x, pos_y):
    """
    "Estampa" la pieza en el tablero una vez que ha aterrizado,
    modificando el tablero principal.
    """
    for fila_idx, fila in enumerate(pieza):
        for col_idx, celda in enumerate(fila):
            if celda == 1:
                tablero_y = pos_y + fila_idx
                tablero_x = pos_x + col_idx
                # Asegurarse de no escribir fuera de los límites (aunque la colisión ya lo previene)
                if 0 <= tablero_y < ALTO_TABLERO and 0 <= tablero_x < ANCHO_TABLERO:
                    tablero[tablero_y] = tablero[tablero_y][:tablero_x] + [1] + tablero[tablero_y][tablero_x+1:]


def eliminar_lineas_completas(tablero):
    """
    Busca filas completas, las elimina y añade filas vacías en la parte superior.
    Devuelve la cantidad de líneas eliminadas para calcular el puntaje.
    """
    lineas_eliminadas = 0
    filas_a_mantener = []
    
    for fila in tablero:
        # Si la fila NO está llena de 1s (es decir, no contiene ceros), la mantenemos.
        if 0 in fila:
            filas_a_mantener.append(fila)
        else:
            lineas_eliminadas += 1
            
    # Calculamos cuántas filas nuevas (vacías) necesitamos añadir arriba
    nuevas_filas = [[0 for _ in range(ANCHO_TABLERO)] for _ in range(lineas_eliminadas)]
    
    # El nuevo tablero es la combinación de las nuevas filas y las que se mantuvieron
    nuevo_tablero = nuevas_filas + filas_a_mantener
    return nuevo_tablero, lineas_eliminadas

def calcular_puntaje(lineas):
    """Calcula el puntaje basado en el número de líneas eliminadas a la vez."""
    if lineas == 1:
        return 100
    elif lineas == 2:
        return 300
    elif lineas == 3:
        return 500
    elif lineas == 4:
        return 800  # ¡Tetris!
    return 0

# --- FUNCIONES DE INTERFAZ Y ARCHIVOS ---

def limpiar_pantalla():
    """Limpia la consola. Funciona en Windows, Linux y macOS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def dibujar_tablero(tablero, pieza_actual, pos_x, pos_y, puntaje):
    """
    Dibuja el estado completo del juego en la consola.
    Crea un tablero temporal para mostrar la pieza en movimiento sin alterar el tablero principal.
    """
    limpiar_pantalla()
    print("--- Retro-Eficiencia: Tetris Verde ---")
    print(f"Puntaje: {puntaje}\n")

    # Creamos una copia profunda del tablero para no modificar el original
    tablero_temporal = [fila[:] for fila in tablero]
    
    # "Dibujamos" la pieza actual sobre el tablero temporal
    for fila_idx, fila in enumerate(pieza_actual):
        for col_idx, celda in enumerate(fila):
            if celda == 1:
                if 0 <= pos_y + fila_idx < ALTO_TABLERO and 0 <= pos_x + col_idx < ANCHO_TABLERO:
                    tablero_temporal[pos_y + fila_idx][pos_x + col_idx] = '■'

    # Imprimimos el tablero temporal
    for fila in tablero_temporal:
        linea_str = ""
        for celda in fila:
            linea_str += '■ ' if celda != 0 else '. '
        print(linea_str)
    
    print("\nControles: [a] Izquierda, [d] Derecha, [w] Rotar, [s] Bajar | Presiona Enter")

def guardar_puntaje(nombre, puntos):
    """Añade un nuevo puntaje al archivo de texto."""
    try:
        with open(PUNTAJES_ARCHIVO, 'a') as f:
            f.write(f"{nombre},{puntos}\n")
    except IOError:
        print("Error: No se pudo guardar el puntaje.")

def mostrar_mejores_puntajes():
    """Lee, ordena y muestra los mejores puntajes desde el archivo."""
    limpiar_pantalla()
    print("--- Mejores Puntajes ---")
    if not os.path.exists(PUNTAJES_ARCHIVO):
        print("Aún no hay puntajes registrados. ¡Sé el primero!")
    else:
        try:
            with open(PUNTAJES_ARCHIVO, 'r') as f:
                puntajes = []
                for linea in f:
                    try:
                        nombre, puntos = linea.strip().split(',')
                        puntajes.append((int(puntos), nombre))
                    except ValueError:
                        continue # Ignora líneas mal formateadas
                
                # Ordenar de mayor a menor puntaje
                puntajes.sort(reverse=True)
                
                for i, (puntos, nombre) in enumerate(puntajes[:10]): # Muestra los 10 mejores
                    print(f"{i+1}. {nombre} - {puntos} puntos")

        except IOError:
            print("Error: No se pudo leer el archivo de puntajes.")
    
    input("\nPresiona Enter para volver al menú...")


def mostrar_menu():
    """Muestra el menú principal y solicita una opción al usuario."""
    limpiar_pantalla()
    print("========================================")
    print("   Retro-Eficiencia: Un Tributo a Tetris")
    print("   (Proyecto de Green Software)")
    print("========================================")
    print("\n1. Jugar")
    print("2. Ver Mejores Puntajes")
    print("3. Salir")
    return input("\nElige una opción: ")

# --- BUCLE PRINCIPAL DEL JUEGO ---

def bucle_principal_del_juego():
    tablero = crear_tablero()
    pieza_actual = crear_pieza_nueva()
    pos_x, pos_y = ANCHO_TABLERO // 2 - 2, 0 # Posición inicial de la pieza
    puntaje = 0
    game_over = False
    
    # Velocidad inicial del juego (segundos por caída)
    velocidad = 0.8
    tiempo_desde_ultima_caida = time.time()

    while not game_over:
        dibujar_tablero(tablero, pieza_actual, pos_x, pos_y, puntaje)
        
        # MANEJO DE ENTRADA (SIMPLE Y EFICIENTE)
        # Se pide una acción. Si no se ingresa nada, el juego avanza por gravedad.
        accion = input("Acción: ").lower()
        
        # Movimiento lateral y rotación
        if accion == 'a': # Mover a la izquierda
            if not es_colision(tablero, pieza_actual, pos_x - 1, pos_y):
                pos_x -= 1
        elif accion == 'd': # Mover a la derecha
            if not es_colision(tablero, pieza_actual, pos_x + 1, pos_y):
                pos_x += 1
        elif accion == 'w': # Rotar
            pieza_rotada = rotar_pieza(pieza_actual)
            if not es_colision(tablero, pieza_rotada, pos_x, pos_y):
                pieza_actual = pieza_rotada
        
        # Gravedad o bajada por el usuario
        if accion == 's' or time.time() - tiempo_desde_ultima_caida > velocidad:
            if not es_colision(tablero, pieza_actual, pos_x, pos_y + 1):
                pos_y += 1
                tiempo_desde_ultima_caida = time.time()
            else:
                # La pieza ha aterrizado
                unir_pieza_al_tablero(tablero, pieza_actual, pos_x, pos_y)
                tablero, lineas = eliminar_lineas_completas(tablero)
                
                # Calcular y añadir puntaje
                puntos_ganados = calcular_puntaje(lineas)
                puntaje += puntos_ganados

                # Aumentar la velocidad del juego
                if puntos_ganados > 0 and velocidad > 0.2:
                    velocidad -= 0.05
                
                # Crear nueva pieza
                pieza_actual = crear_pieza_nueva()
                pos_x, pos_y = ANCHO_TABLERO // 2 - 2, 0
                
                # Comprobar si el juego ha terminado
                if es_colision(tablero, pieza_actual, pos_x, pos_y):
                    game_over = True

    # Fin del juego
    dibujar_tablero(tablero, [], 0, 0, puntaje) # Muestra el tablero final
    print("\n\n--- ¡JUEGO TERMINADO! ---")
    print(f"Tu puntaje final es: {puntaje}")
    nombre = input("Ingresa tu nombre para guardar el puntaje: ")
    if nombre:
        guardar_puntaje(nombre, puntaje)

# --- EJECUCIÓN DEL PROGRAMA ---

if __name__ == "__main__":
    while True:
        opcion = mostrar_menu()
        if opcion == '1':
            bucle_principal_del_juego()
        elif opcion == '2':
            mostrar_mejores_puntajes()
        elif opcion == '3':
            print("¡Gracias por jugar! El software eficiente ayuda al planeta.")
            break
        else:
            input("Opción no válida. Presiona Enter para continuar...")
