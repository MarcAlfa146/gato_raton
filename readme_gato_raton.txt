# 🐭🐱 Juego del Gato y el Ratón (IA Minimax) 🧀🧱

Este proyecto implementa una versión del clásico juego del Gato y el Ratón utilizando Inteligencia Artificial con el algoritmo **Minimax** y **Poda Alfa-Beta**. Tanto el Gato como el Ratón son controlados por la IA, que busca optimizar sus movimientos para ganar la partida.

---

## 🎮 Descripción del Juego

El juego se desarrolla en un tablero de `10x10` celdas, con `10` obstáculos (`🧱`) generados aleatoriamente. Los objetivos son:

Gato (🐱):Atrapar al Ratón.
Ratón (🐭):Llegar a la celda del Queso (`🧀`).

El juego tiene un límite de `10` turnos. Si el Ratón llega al Queso antes de ser atrapado o antes de que se acaben los turnos, gana. Si el Gato atrapa al Ratón, el Gato gana. Si se terminan los turnos sin que ocurra ninguna de las dos condiciones, es un empate.

Para cada turno se debe presionar ENTER

Ambos jugadores (Gato y Ratón) utilizan el algoritmo **Minimax** con **Poda Alfa-Beta** para decidir sus movimientos.

* El **Gato** actúa como el jugador **Maximizador**, buscando la evaluación más alta posible (que significa atrapar al Ratón o posicionarse para hacerlo).
* El **Ratón** actúa como el jugador **Minimizador**, buscando la evaluación más baja posible (que significa llegar al Queso o escapar del Gato).

La función de evaluación (`evaluar_estado`) asigna un puntaje a cada estado del tablero, basándose en la distancia entre el Gato y el Ratón, y la distancia entre el Ratón y el Queso. Los pesos en esta función se han ajustado para fomentar un comportamiento de persecución agresiva por parte del Gato y de evasión inteligente por parte del Ratón.

* `crear_tablero()`: Inicializa el tablero con obstáculos.
* `imprimir_tablero()`: Muestra el estado actual del juego en la consola.
* `obtener_movimientos_validos()`: Determina qué movimientos son posibles desde una posición dada.
* `calcular_distancia()`: Calcula la distancia de Manhattan entre dos puntos.
* `evaluar_estado()`: Función heurística que puntúa un estado del juego. **Es fundamental para el comportamiento de la IA.**
* `minimax()`: Implementación del algoritmo Minimax con poda Alfa-Beta. Es una función **recursiva**.
* `obtener_mejor_movimiento_gato_ia()`: Utiliza Minimax para encontrar el mejor movimiento para el Gato.
* `obtener_mejor_movimiento_raton_ia()`: Utiliza Minimax para encontrar el mejor movimiento para el Ratón.
* `jugar_partida()`: Contiene la lógica principal de un solo juego.
* `main()`: Orquesta el flujo del programa, permitiendo jugar múltiples partidas.

---