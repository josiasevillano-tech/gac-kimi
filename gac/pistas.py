"""
gac/pistas.py
=============
Asigna numeros de pista a las palabras de un crucigrama.

En un crucigrama de papel, cada palabra lleva un numero pequeno
en su casilla inicial. Este modulo decide que numero le toca a cada una.

Principio: "El numerador decide; el renderer muestra."
"""

from .board import Board
from .placement import Placement


class PistaNumerador:
    """
    Asigna numeros secuenciales a las palabras de un tablero.

    El numero 1 va a la palabra cuya casilla inicial este mas arriba
    y mas a la izquierda. Luego 2, 3... en orden de lectura
    (de arriba a abajo, de izquierda a derecha).

    Si dos palabras empiezan en la misma casilla, comparten el mismo numero.
    """

    def numerar(self, board: Board) -> dict[Placement, int]:
        """
        Devuelve un diccionario: placement -> numero_de_pista.

        Las palabras se ordenan por (fila_inicial, columna_inicial).
        """
        if not board.placements:
            return {}

        # Ordenar por fila inicial, luego columna inicial
        ordenadas = sorted(
            board.placements,
            key=lambda p: (p.fila, p.columna)
        )

        # Asignar numeros: si dos palabras empiezan en la misma casilla,
        # comparten numero
        resultado: dict[Placement, int] = {}
        numero_actual = 1
        ultima_casilla: tuple[int, int] | None = None

        for p in ordenadas:
            casilla = (p.fila, p.columna)
            if casilla != ultima_casilla:
                numero_actual += 1 if ultima_casilla is not None else 0
                if ultima_casilla is None:
                    numero_actual = 1
                ultima_casilla = casilla
            resultado[p] = numero_actual

        return resultado

    def numeros_por_celda(self, board: Board) -> dict[tuple[int, int], int]:
        """
        Devuelve un diccionario: (fila, columna) -> numero_de_pista.

        Util para el renderer: sabe que numero pintar en cada celda.
        """
        asignaciones = self.numerar(board)
        resultado: dict[tuple[int, int], int] = {}
        for placement, numero in asignaciones.items():
            casilla = (placement.fila, placement.columna)
            resultado[casilla] = numero
        return resultado