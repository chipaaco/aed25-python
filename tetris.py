import os
import random
import time

# --- CONSTANTES GLOBALES ---
ANCHO_TABLERO = 10
ALTO_TABLERO = 20
PUNTAJES_ARCHIVO = "puntajes.txt"

PIEZAS = [
    [[0,0,0,0], [0,1,1,0], [0,1,1,0], [0,0,0,0]],  # Cuadrado
    [[0,1,0,0], [0,1,0,0], [0,1,0,0], [0,1,0,0]],  # Palo
    [[0,0,0,0], [0,1,1,0], [1,1,0,0], [0,0,0,0]],  # S
    [[0,0,0,0], [1,1,0,0], [0,1,1,0], [0,0,0,0]],  # S (invertida)
    [[0,0,0,0], [0,1,0,0], [1,1,1,0], [0,0,0,0]],  # T
    [[0,0,0,0], [0,0,1,0], [1,1,1,0], [0,0,0,0]],  # L
    [[0,0,0,0], [1,0,0,0], [1,1,1,0], [0,0,0,0]],  # L (invertida)
]

# --- FUNCIONES DE LÓGICA DEL JUEGO ---

def crear_tablero():
    return [[0 for _ in range(ANCHO_TABLERO)] for _ in range(ALTO_TABLERO)]

def crear_pieza_nueva():
    return random.choice(PIEZAS)

def rotar_pieza(pieza):
    transpuesta = [list(i) for i in zip(*pieza)]
    return [row[::-1] for row in transpuesta]

def es_colision(tablero, pieza, pos_x, pos_y):
    for fila_idx, fila in enumerate(pieza):
        for col_idx, celda in enumerate(fila):
            if celda == 1:
                tablero_y = pos_y + fila_idx
                tablero_x = pos_x + col_idx
                
                if not (0 <= tablero_x < ANCHO_TABLERO and 0 <= tablero_y < ALTO_TABLERO):
                    return True
                
                if tablero[tablero_y][tablero_x] == 1:
                    return True
    return False

def unir_pieza_al_tablero(tablero, pieza, pos_x, pos_y):
    for fila_idx, fila in enumerate(pieza):
        for col_idx, celda in enumerate(fila):
            if celda == 1:
                tablero_y = pos_y + fila_idx
                tablero_x = pos_x + col_idx
                if 0 <= tablero_y < ALTO_TABLERO and 0 <= tablero_x < ANCHO_TABLERO:
                    # Esta línea es un poco más robusta para evitar errores de índice
                    fila_nueva = list(tablero[tablero_y])
                    fila_nueva[tablero_x] = 1
                    tablero[tablero_y] = fila_nueva

def eliminar_lineas_completas(tablero):
    lineas_eliminadas = 0
    filas_a_mantener = [fila for fila in tablero if 0 in fila]
    
    lineas_eliminadas = ALTO_TABLERO - len(filas_a_mantener)
    nuevas_filas = [[0 for _ in range(ANCHO_TABLERO)] for _ in range(lineas_eliminadas)]
    
    nuevo_tablero = nuevas_filas + filas_a_mantener
    return nuevo_tablero, lineas_eliminadas

def calcular_puntaje(lineas):
    if lineas == 1: return 100
    elif lineas == 2: return 300
    elif lineas == 3: return 500
    elif lineas == 4: return 800
    return 0

# --- FUNCIONES DE INTERFAZ Y ARCHIVOS ---

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def dibujar_tablero(tablero, pieza_actual, pos_x, pos_y, puntaje):
    limpiar_pantalla()
    print("--- Tetris wanna be ---")
    print(f"Puntaje: {puntaje}\n")

    tablero_temporal = [fila[:] for fila in tablero]
    
    for fila_idx, fila in enumerate(pieza_actual):
        for col_idx, celda in enumerate(fila):
            if celda == 1:
                if 0 <= pos_y + fila_idx < ALTO_TABLERO and 0 <= pos_x + col_idx < ANCHO_TABLERO:
                    tablero_temporal[pos_y + fila_idx][pos_x + col_idx] = '■'

    for fila in tablero_temporal:
        linea_str = ""
        for celda in fila:
            linea_str += '■ ' if celda != 0 else '. '
        print(linea_str)
    
    # <<< CAMBIO: Se actualizó el texto de los controles.
    print("\nControles: [a] Izquierda, [d] Derecha, [r] Rotar")
    print("Apretá [Enter] para bajar un espacio (si lo mantenés la pieza baja más rápido).")

def guardar_puntaje(nombre, puntos):
    try:
        with open(PUNTAJES_ARCHIVO, 'a') as f:
            f.write(f"{nombre},{puntos}\n")
    except IOError:
        print("Error: No se pudo guardar el puntaje.")

def mostrar_mejores_puntajes():
    limpiar_pantalla()
    print("--- Mejores Puntajes ---")
    if not os.path.exists(PUNTAJES_ARCHIVO):
        print("Todavía no hay puntajes registrados. ¡Podés ser el primero!")
    else:
        try:
            with open(PUNTAJES_ARCHIVO, 'r') as f:
                puntajes = []
                for linea in f:
                    try:
                        nombre, puntos = linea.strip().split(',')
                        puntajes.append((int(puntos), nombre))
                    except ValueError:
                        continue
                
                puntajes.sort(reverse=True)
                
                for i, (puntos, nombre) in enumerate(puntajes[:10]):
                    print(f"{i+1}. {nombre} - {puntos} puntos")
        except IOError:
            print("Error: No se pudo leer el archivo de puntajes.")
    
    input("\nApretá Enter para volver al menú...")


def mostrar_menu():
    limpiar_pantalla()
    print("========================================")
    print("   Tetris wanna be")
    print("   (Laboratorio python AED2025)")
    print("========================================")
    print("\n1. Jugar")
    print("2. Ver Mejores Puntajes")
    print("3. Salir")
    return input("\nElegí una opción: ")

# --- BUCLE PRINCIPAL DEL JUEGO ---

def bucle_principal_del_juego():
    tablero = crear_tablero()
    pieza_actual = crear_pieza_nueva()
    pos_x, pos_y = ANCHO_TABLERO // 2 - 2, 0
    puntaje = 0
    game_over = False

    while not game_over:
        dibujar_tablero(tablero, pieza_actual, pos_x, pos_y, puntaje)
        
        accion = input("Acción: ").lower()
        
        # <<< CAMBIO: Ahora 'r' es para rotar. 'w' ya no hace nada.
        if accion == 'a':
            if not es_colision(tablero, pieza_actual, pos_x - 1, pos_y):
                pos_x -= 1
        elif accion == 'd':
            if not es_colision(tablero, pieza_actual, pos_x + 1, pos_y):
                pos_x += 1
        elif accion == 'r': # Rotar
            pieza_rotada = rotar_pieza(pieza_actual)
            if not es_colision(tablero, pieza_rotada, pos_x, pos_y):
                pieza_actual = pieza_rotada
        
        # <<< CAMBIO: Ahora presionar Enter (acción vacía) o 's' baja la pieza.
        if accion == '':
            if not es_colision(tablero, pieza_actual, pos_x, pos_y + 1):
                pos_y += 1
            else:
                unir_pieza_al_tablero(tablero, pieza_actual, pos_x, pos_y)
                tablero, lineas = eliminar_lineas_completas(tablero)
                
                puntos_ganados = calcular_puntaje(lineas)
                puntaje += puntos_ganados
                
                pieza_actual = crear_pieza_nueva()
                pos_x, pos_y = ANCHO_TABLERO // 2 - 2, 0
                
                if es_colision(tablero, pieza_actual, pos_x, pos_y):
                    game_over = True

    dibujar_tablero(tablero, [], 0, 0, puntaje)
    print("\n\n--- ¡JUEGO TERMINADO! ---")
    print(f"Tu puntaje final es: {puntaje}")
    nombre = input("Ingresá tu nombre para guardar el puntaje: ")
    if nombre:
        guardar_puntaje(nombre.strip(), puntaje)

# --- EJECUCIÓN DEL PROGRAMA ---

if __name__ == "__main__":
    while True:
        opcion = mostrar_menu()
        if opcion == '1':
            bucle_principal_del_juego()
        elif opcion == '2':
            mostrar_mejores_puntajes()
        elif opcion == '3':
            print("¡Gracias por jugar! Chau")
            break
        else:
            input("Opción no válida. Apretá Enter para continuar...")
