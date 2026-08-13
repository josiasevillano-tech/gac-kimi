"""
tests/test_pistas.py
====================
Pruebas del numerador de pistas.

Para correr:
    python -m pytest tests/test_pistas.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gac import Board, Horizontal, Vertical, Placement
from gac.pistas import PistaNumerador


def test_tablero_vacio_sin_numeros():
    """Un tablero sin palabras no tiene numeros de pista."""
    board = Board(5, 5)
    num = PistaNumerador()
    assert num.numerar(board) == {}
    assert num.numeros_por_celda(board) == {}


def test_una_palabra_tiene_numero_1():
    """Una sola palabra lleva el numero 1."""
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    num = PistaNumerador()
    asignaciones = num.numerar(board)
    assert len(asignaciones) == 1
    assert list(asignaciones.values())[0] == 1


def test_dos_palabras_numeros_secuenciales():
    """Dos palabras en casillas diferentes llevan 1 y 2."""
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    board.colocar(Placement("LUZ", fila=4, columna=0, direccion=Horizontal()))
    num = PistaNumerador()
    asignaciones = num.numerar(board)
    assert len(asignaciones) == 2
    valores = sorted(asignaciones.values())
    assert valores == [1, 2]


def test_dos_palabras_misma_casilla_comparten_numero():
    """
    Si dos palabras empiezan en la misma casilla (cruz perpendicular),
    comparten el mismo numero de pista.
    """
    board = Board(5, 5)
    p1 = Placement("SOL", fila=2, columna=2, direccion=Horizontal())
    p2 = Placement("SAL", fila=2, columna=2, direccion=Vertical())
    board.colocar(p1)
    board.colocar(p2)
    num = PistaNumerador()
    asignaciones = num.numerar(board)
    assert asignaciones[p1] == asignaciones[p2]


def test_orden_arriba_izquierda_primero():
    """
    La palabra que empieza mas arriba y mas a la izquierda lleva el 1.
    """
    board = Board(10, 10)
    p_arriba = Placement("AAA", fila=1, columna=5, direccion=Horizontal())
    p_abajo = Placement("BBB", fila=5, columna=1, direccion=Horizontal())
    board.colocar(p_abajo)
    board.colocar(p_arriba)
    num = PistaNumerador()
    asignaciones = num.numerar(board)
    assert asignaciones[p_arriba] == 1
    assert asignaciones[p_abajo] == 2


def test_numeros_por_celda_devuelve_coordenadas():
    """numeros_por_celda devuelve {(fila, col): numero}."""
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    num = PistaNumerador()
    por_celda = num.numeros_por_celda(board)
    assert por_celda == {(2, 1): 1}