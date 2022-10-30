from turtle import pos
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np
import copy


def cordenada_visual(table: GameState, i: int, j: int, jugada: str) -> tuple[int, int] or None:
    if (jugada == "izquierda" and not table.col_status[i][j]) or (jugada == "arriba" and not table.row_status[i][j]):
        return (i, j)
    elif jugada == "derecha" and not table.col_status[i][j+1]:
        return (i, j+1)
    elif jugada == "abajo" and not table.row_status[i+1][j]:
        return (i+1, j)
    return None


def realizar_jugada(table: GameState, indice: tuple[int, int], indice_visual: tuple[int, int], jugada: str, player1_turn: bool) -> GameState:
    playerModifier = -1 if not player1_turn else 1
    x, y = indice
    x2, y2 = indice_visual
    table.board_status[x][y] = (
        abs(table.board_status[x][y]) + 1)*playerModifier

    if jugada == "izquierda":
        table.col_status[x2][y2] += 1
        if y > 0:
            table.board_status[x][y-1] = (
                abs(table.board_status[x][y-1]) + 1)*playerModifier

    elif jugada == "arriba":
        table.row_status[x2][y2] += 1
        if x > 0:
            table.board_status[x -
                               1][y] = (abs(table.board_status[x-1][y]) + 1)*playerModifier
    elif jugada == "derecha":
        table.col_status[x2][y2] += 1
        if y < len(table.board_status[0]) - 1:
            table.board_status[x][y +
                                  1] = (abs(table.board_status[x][y+1]) + 1)*playerModifier

    elif jugada == "abajo":
        table.row_status[x2][y2] += 1
        if x < len(table.board_status) - 1:
            # print("Se modifico: ", (x+1, y))
            table.board_status[x +
                               1][y] = (abs(table.board_status[x+1][y]) + 1)*playerModifier

    return GameState(table.board_status.copy(),
                     table.row_status.copy(),
                     table.col_status.copy(),
                     not table.player1_turn
                     )


def generar_jugadas(state: GameState) -> list[GameState]:
    jugadas = []
    codigos = set()
    jugador = -1 if state.player1_turn else 1

    dimension = len(state.board_status)
    for i in range(dimension):
        for j in range(dimension):
            if state.board_status[i][j] == 4 or state.board_status[i][j] == -4:
                continue

            for jugada in ("izquierda", "arriba", "derecha", "abajo"):
                cordenada = cordenada_visual(state, i, j, jugada)
                if cordenada == None:
                    continue

                copia_estado = GameState(state.board_status.copy(),
                                         state.row_status.copy(),
                                         state.col_status.copy(),
                                         state.player1_turn
                                         )

                nuevo_tablero = realizar_jugada(
                    copia_estado, (i, j), cordenada, jugada, jugador)

                codigo = nuevo_tablero.get_id()
                if codigo in codigos:
                    continue
                jugadas.append(nuevo_tablero)
                codigos.add(codigo)
    return jugadas


def contar(matrix, valor): return sum(
    [len([value for value in row if value == valor]) for row in matrix])


pesos = {4: 25, 3: 7, 2: -2, 1: 1, 0: 1}


def get_utility(estado: GameState, profundidad: int) -> int:
    modificador = 1 if estado.player1_turn else -1
    cantidad_4_min = contar(estado.board_status, 4)
    cantidad_4_max = contar(estado.board_status, -4)
    cantidad_3 = contar(estado.board_status, 3) + \
        contar(estado.board_status, -3)

    cantidad_2 = contar(estado.board_status, 2) + \
        contar(estado.board_status, -2)
    cantidad_1 = contar(estado.board_status, 1) + \
        contar(estado.board_status, -1)

    cantidad_0 = contar(estado.board_status, 0)

    utility = cantidad_4_max*1000 + cantidad_4_min*-1000 + cantidad_3 * \
        4*-modificador + cantidad_2*3*-modificador + \
        (cantidad_1*2 + cantidad_0*1)*modificador
    # if estado.player1_turn:
    #     utility = cantidad_4_max*11 + cantidad_4_min*-11 + cantidad_3 * \
    #         5 + cantidad_2*-1 + cantidad_0
    # else:
    #     utility = cantidad_4_min*11 + cantidad_4_max*-11 + \
    #         cantidad_3*4 + cantidad_2*1 + cantidad_0
    print("Estado analizado")
    print(estado.board_status)
    print(f"Juega jugador 1: {estado.player1_turn} - 4_min: {cantidad_4_min} - 4_max: {cantidad_4_max} - cantidad_3: {cantidad_3} - cantidad_2 {cantidad_2} - cantidad1 - {cantidad_1} - cantidad_0 {cantidad_0} - Utilidad: {utility}")
    return utility


def minimax(estado_inicial: GameState, profundidad: int):
    maximizing = estado_inicial.player1_turn
    # print(estado_inicial)
    # print(estado_inicial.is_terminal())
    # print("=========================")
    if estado_inicial.is_terminal() or profundidad == 0:
        utility = get_utility(estado_inicial, profundidad)
        # print(utility)
        return utility

    if maximizing:
        value = -float('inf')
        for jugada in generar_jugadas(estado_inicial):
            value = max(value, minimax(jugada, profundidad - 1))
        # print(value)
        return value
    else:
        value = float('inf')
        for jugada in generar_jugadas(estado_inicial):
            value = min(value, minimax(jugada, profundidad - 1))
        # print("Utilidad escogida", value)
        return value


class MinimaxBot(Bot):
    profundidad = 2

    def get_action(self, state: GameState) -> GameAction:
        maximizing = state.player1_turn
        movimiento = None
        # if maximizing:
        #     maximo = -float('inf')
        #     for jugada in generar_jugadas(state):
        #         result = minimax(
        #             jugada, MinimaxBot.profundidad)
        #         if result > maximo:
        #             maximo = result
        #             movimiento = jugada
        # else:
        minimo = float('inf')
        # print(f"Le toca jugar {'max' if state.player1_turn else 'min'}")
        # print("Tablero generados")
        for jugada in generar_jugadas(state):
            # print(jugada)
            result = minimax(
                jugada, MinimaxBot.profundidad)
            if result < minimo:
                minimo = result
                movimiento = jugada
        # if movimiento == None:
        #     print("ESTADO QUE GENERA EL NULO")
        #     print(state)
        #     estado = generar_jugadas(state)
        #     print("Estado de primer nivel")
        #     print(estado[0])
        #     print("Estado de segundo nivel")
        #     print(generar_jugadas(estado[0]))
        #     input()
        return self.__get_game_action__(state, movimiento)

    def __comparar_matrices__(self, matrix1, matrix2) -> tuple[int, int] or None:
        x = len(matrix1)
        y = len(matrix1[0])
        for i in range(x):
            for j in range(y):
                if matrix1[i][j] != matrix2[i][j]:
                    return (j, i)
        return None

    def __get_game_action__(self, state1: GameState, state2: GameState):
        action = "row"
        position = self.__comparar_matrices__(
            state1.row_status, state2.row_status)

        if position == None:
            action = "col"
            position = self.__comparar_matrices__(
                state1.col_status, state2.col_status)

        return GameAction(action, position)
