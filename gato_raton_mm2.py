import random
import os

TAM_TABLERO = 10
TURNOS_MAXIMOS = 10
OBSTACULOS_INICIALES = 10
PROFUNDIDAD_IA = 4 

GATO = "🐱"
RATON = "🐭"
QUESO = "🧀"
VACIO = "🟦"
OBSTACULO = "🧱"

PUNTUACION_GATO_GANA = 1000
PUNTUACION_RATON_GANA = -1000
PUNTUACION_EMPATE = 0

def crear_tablero(tam, n_obstaculos):
    tablero = [[VACIO for _ in range(tam)] for _ in range(tam)]
    for _ in range(n_obstaculos):
        while True:
            x, y = random.randint(0, tam-1), random.randint(0, tam-1)
            if tablero[x][y] == VACIO:
                tablero[x][y] = OBSTACULO
                break
    return tablero

def imprimir_tablero(tablero, pos_gato, pos_raton, pos_queso):
    os.system("cls" if os.name == "nt" else "clear")

    for i in range(len(tablero)):
        fila_str = ""
        for j in range(len(tablero[i])):
            if (i, j) == pos_gato:
                fila_str += GATO + " "
            elif (i, j) == pos_raton:
                fila_str += RATON + " "
            elif (i, j) == pos_queso:
                fila_str += QUESO + " "
            else:
                fila_str += tablero[i][j] + " "
        print(fila_str)
    print()

def obtener_movimientos_validos(tablero, pos):
    movimientos = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = pos[0] + dx, pos[1] + dy

        if 0 <= nx < len(tablero) and 0 <= ny < len(tablero[0]) and tablero[nx][ny] != OBSTACULO:
            movimientos.append((nx, ny))
    return movimientos

def calcular_distancia(pos1, pos2):
    x1, y1 = pos1[0], pos1[1]
    x2, y2 = pos2[0], pos2[1]

    diff_x = abs(x1 - x2)
    diff_y = abs(y1 - y2)
    
    return diff_x + diff_y

def evaluar_estado(pos_gato, pos_raton, pos_queso, turnos_restantes):
    if pos_gato == pos_raton:
        return PUNTUACION_GATO_GANA
    
    if pos_raton == pos_queso:
        return PUNTUACION_RATON_GANA
    
    if turnos_restantes <= 0:
        return PUNTUACION_EMPATE
    
    dist_gato_raton = calcular_distancia(pos_gato, pos_raton)
    dist_raton_queso = calcular_distancia(pos_raton, pos_queso)
    
    eval_gato_raton_component = -dist_gato_raton * 20 
    eval_raton_queso_component = -dist_raton_queso * 5 

    if dist_gato_raton == 0: 
        return PUNTUACION_GATO_GANA 
    elif dist_gato_raton == 1: 
        eval_gato_raton_component += 200 
    elif dist_gato_raton == 2: 
        eval_gato_raton_component += 70

    evaluacion_final = eval_gato_raton_component + eval_raton_queso_component
    
    return evaluacion_final

def minimax(tablero_actual, pos_gato, pos_raton, pos_queso, turnos_restantes, profundidad, es_maximizador, alpha=float('-inf'), beta=float('inf')):
    if profundidad == 0 or pos_gato == pos_raton or pos_raton == pos_queso or turnos_restantes <= 0:
        return evaluar_estado(pos_gato, pos_raton, pos_queso, turnos_restantes)

    if es_maximizador:
        max_eval = float('-inf')
        movimientos_gato = obtener_movimientos_validos(tablero_actual, pos_gato)
        
        if not movimientos_gato: 
            return PUNTUACION_RATON_GANA 

        for movimiento_gato in movimientos_gato:
            nueva_pos_gato = movimiento_gato
            eval = minimax(tablero_actual, nueva_pos_gato, pos_raton, pos_queso, turnos_restantes, profundidad - 1, False, alpha, beta)
            
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = float('inf')
        movimientos_raton = obtener_movimientos_validos(tablero_actual, pos_raton)

        if not movimientos_raton:
            return PUNTUACION_GATO_GANA 

        for movimiento_raton in movimientos_raton:
            nueva_pos_raton = movimiento_raton
            eval = minimax(tablero_actual, pos_gato, nueva_pos_raton, pos_queso, turnos_restantes - 1, profundidad - 1, True, alpha, beta)
            
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            
            if beta <= alpha:
                break
        return min_eval

def obtener_mejor_movimiento_gato_ia(tablero, pos_gato, pos_raton, pos_queso, turnos_restantes, profundidad_busqueda):
    mejor_eval = float('-inf')
    mejor_movimiento = None

    movimientos_validos = obtener_movimientos_validos(tablero, pos_gato)

    if not movimientos_validos:
        return pos_gato

    mejores_movimientos_posibles = []

    for movimiento in movimientos_validos:
        nueva_pos_gato = movimiento
        evaluacion = minimax(tablero, nueva_pos_gato, pos_raton, pos_queso, turnos_restantes, profundidad_busqueda - 1, False) 

        if evaluacion > mejor_eval:
            mejor_eval = evaluacion
            mejores_movimientos_posibles = [nueva_pos_gato]
        elif evaluacion == mejor_eval:
            mejores_movimientos_posibles.append(nueva_pos_gato)
    
    if mejores_movimientos_posibles:
        return random.choice(mejores_movimientos_posibles)
    else: 
        return pos_gato 

def obtener_mejor_movimiento_raton_ia(tablero, pos_gato, pos_raton, pos_queso, turnos_restantes, profundidad_busqueda):
    mejor_eval = float('inf')  
    mejor_movimiento = None

    movimientos_validos = obtener_movimientos_validos(tablero, pos_raton)

    if not movimientos_validos:
        return pos_raton 

    mejores_movimientos_posibles = []

    for movimiento in movimientos_validos:
        nueva_pos_raton = movimiento 
        evaluacion = minimax(tablero, pos_gato, nueva_pos_raton, pos_queso, turnos_restantes - 1, profundidad_busqueda - 1, True) 

        if evaluacion < mejor_eval: 
            mejor_eval = evaluacion
            mejores_movimientos_posibles = [nueva_pos_raton]
        elif evaluacion == mejor_eval:
            mejores_movimientos_posibles.append(nueva_pos_raton)
    
    if mejores_movimientos_posibles:
        return random.choice(mejores_movimientos_posibles)
    else: 
        return pos_raton 

def jugar_partida():
    tablero = crear_tablero(TAM_TABLERO, OBSTACULOS_INICIALES)
    
    while True:
        pos_gato = (random.randint(0, TAM_TABLERO-1), random.randint(0, TAM_TABLERO-1))
        pos_raton = (random.randint(0, TAM_TABLERO-1), random.randint(0, TAM_TABLERO-1))
        pos_queso = (random.randint(0, TAM_TABLERO-1), random.randint(0, TAM_TABLERO-1))

        if (tablero[pos_gato[0]][pos_gato[1]] == VACIO and
            tablero[pos_raton[0]][pos_raton[1]] == VACIO and
            tablero[pos_queso[0]][pos_queso[1]] == VACIO and
            pos_gato != pos_raton and pos_gato != pos_queso and pos_raton != pos_queso):
            break

    turnos_actuales = TURNOS_MAXIMOS

    print("¡Bienvenido al Juego del Gato y el Ratón!")
    print(f"El Gato ({GATO}) es la IA. El Ratón ({RATON}) también es IA, controlado por Enter.")
    print(f"El Queso ({QUESO}) es el objetivo del Ratón.")
    input("Presiona Enter para comenzar el juego...")

    while turnos_actuales > 0:
        imprimir_tablero(tablero, pos_gato, pos_raton, pos_queso)
        print(f"Turnos restantes: {turnos_actuales}")

        print("\n--- Turno del Gato ---")
        pos_gato = obtener_mejor_movimiento_gato_ia(tablero, pos_gato, pos_raton, pos_queso, turnos_actuales, PROFUNDIDAD_IA)
        print(f"El Gato se mueve a {pos_gato}")
        
        if pos_gato == pos_raton:
            imprimir_tablero(tablero, pos_gato, pos_raton, pos_queso)
            print("¡El Gato atrapó al Ratón! ¡El Gato gana!")
            return
        
        print("\n--- Turno del Ratón ---")
        input("Presiona Enter para el turno del Ratón...") 
        pos_raton = obtener_mejor_movimiento_raton_ia(tablero, pos_gato, pos_raton, pos_queso, turnos_actuales, PROFUNDIDAD_IA)
        print(f"El Ratón se mueve a {pos_raton}")
        
        if pos_raton == pos_queso:
            imprimir_tablero(tablero, pos_gato, pos_raton, pos_queso)
            print("¡El Ratón llegó al Queso! ¡El Ratón gana!")
            return
        
        if pos_gato == pos_raton:
            imprimir_tablero(tablero, pos_gato, pos_raton, pos_queso)
            print("¡El Gato atrapó al Ratón! ¡El Gato gana!")
            return

        turnos_actuales -= 1
        if turnos_actuales <= 0:
            imprimir_tablero(tablero, pos_gato, pos_raton, pos_queso)
            print("¡Se acabaron los turnos! Es un empate.")
            return
    
def main():
    while True:
        jugar_partida()
        print("\n--- Juego Terminado ---")
        
        while True:
            respuesta = input("¿Quieres jugar de nuevo? (S/N): ").strip().upper()
            if respuesta == 'S':
                break
            elif respuesta == 'N':
                print("¡Gracias por jugar! Adiós.")
                return
            else:
                print("Respuesta no válida. Por favor, ingresa 'S' o 'N'.")

if __name__ == "__main__":
    main()