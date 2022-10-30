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
    playerModifier = -1 if player1_turn else 1
    x, y = indice
    x2, y2 = indice_visual
    table.board_status[x][y] = abs(table.board_status[x][y]) + 1
    # Me falta otra regla para generar estados
    table.board_status[x][y] *= playerModifier
    if jugada == "izquierda" or jugada == "derecha":
        table.col_status[x2][y2] += 1
    else:
        table.row_status[x2][y2] += 1
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


def get_utility(estado: GameState, profundidad: int) -> int:
    jugador = 1 if estado.player1_turn else -1
    cantidad_4_max = contar(estado.board_status, 4)
    cantidad_4_min = contar(estado.board_status, -4)
    cantidad_3 = contar(estado.board_status, 3) + \
        contar(estado.board_status, -3)

    cantidad_2 = contar(estado.board_status, 2) + \
        contar(estado.board_status, -2)
    cantidad_2 = contar(estado.board_status, 1) + \
        contar(estado.board_status, -1)
    cantidad_0 = contar(estado.board_status, 0)

    if estado.player1_turn:
        utility = cantidad_4_max*11 + cantidad_4_min*-11 + cantidad_3 * \
            4 + cantidad_2*-2 + cantidad_0 + profundidad*10
    else:
        utility = cantidad_4_min*11 + cantidad_4_max*-11 + \
            cantidad_3*4 + cantidad_2*-2 + cantidad_0 + profundidad*10

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
        # print(value)
        return value


class MinimaxBot(Bot):
    profundidad = 3

    def get_action(self, state: GameState) -> GameAction:
        maximizing = state.player1_turn
        movimiento = None
        if maximizing:
            maximo = -float('inf')
            for jugada in generar_jugadas(state):
                result = minimax(
                    jugada, MinimaxBot.profundidad)
                if result > maximo:
                    maximo = result
                    movimiento = jugada
        else:
            minimo = float('inf')
            for jugada in generar_jugadas(state):
                result = minimax(
                    jugada, MinimaxBot.profundidad)
                if result < minimo:
                    minimo = result
                    movimiento = jugada
        if movimiento == None:
            print("ESTADO QUE GENERA EL NULO")
            print(state)
            estado = generar_jugadas(state)
            print("Estado de primer nivel")
            print(estado[0])
            print("Estado de segundo nivel")
            print(generar_jugadas(estado[0]))
            input()
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
