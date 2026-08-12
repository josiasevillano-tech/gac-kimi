"""
tests/test_board.py
===================
Pruebas de calidad del tablero.

Para correrlas:
    python -m pytest tests/test_board.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gac import Board, Horizontal, Vertical, Placement


def test_tablero_vacio_tiene_dimensiones_correctas():
    """Un tablero nuevo debe saber cuanto mide."""
    tablero = Board(filas=5, columnas=8)
    assert tablero.filas == 5
    assert tablero.columnas == 8


def test_tablero_nuevo_esta_vacio():
    """Al crear un tablero, no debe haber palabras ni letras."""
    tablero = Board(filas=3, columnas=3)
    assert len(tablero.placements) == 0
    assert tablero.esta_vacia(0, 0)
    assert tablero.esta_vacia(2, 2)


def test_colocar_una_palabra_horizontal():
    """Si pongo 'SOL' horizontal en (1,1), las celdas (1,1), (1,2), (1,3) deben tener letras."""
    tablero = Board(filas=5, columnas=5)
    p = Placement("SOL", fila=1, columna=1, direccion=Horizontal())
    tablero.colocar(p)
    assert tablero.celda(1, 1) == "S"
    assert tablero.celda(1, 2) == "O"
    assert tablero.celda(1, 3) == "L"
    assert tablero.esta_vacia(1, 4)


def test_colocar_una_palabra_vertical():
    """Si pongo 'LUZ' vertical en (0,0), las celdas (0,0), (1,0), (2,0) deben tener letras."""
    tablero = Board(filas=5, columnas=5)
    p = Placement("LUZ", fila=0, columna=0, direccion=Vertical())
    tablero.colocar(p)
    assert tablero.celda(0, 0) == "L"
    assert tablero.celda(1, 0) == "U"
    assert tablero.celda(2, 0) == "Z"


def test_dos_palabras_se_cruzan():
    """Si dos palabras comparten una casilla, ambas deben estar registradas."""
    tablero = Board(filas=5, columnas=5)

    # CRUCE REAL: "SOL" horizontal en (2,0): S-O-L
    # "SAL" vertical en (0,2): S-A-L -> se cruzan en (2,2) con la letra 'L'
    p_sol = Placement("SOL", fila=2, columna=0, direccion=Horizontal())
    p_sal = Placement("SAL", fila=0, columna=2, direccion=Vertical())

    tablero.colocar(p_sol)
    tablero.colocar(p_sal)

    assert tablero.celda(2, 2) == "L"  # Ambas palabras ponen 'L' aqui
    assert len(tablero.placements) == 2


def test_quitar_palabra_libera_celdas():
    """Si quito una palabra, sus casillas deben volver a estar vacias."""
    tablero = Board(filas=5, columnas=5)
    p = Placement("SOL", fila=1, columna=1, direccion=Horizontal())
    tablero.colocar(p)
    tablero.quitar(p)
    assert tablero.esta_vacia(1, 1)
    assert tablero.esta_vacia(1, 2)
    assert tablero.esta_vacia(1, 3)
    assert len(tablero.placements) == 0


def test_quitar_palabra_no_borra_cruce():
    """Si dos palabras comparten una casilla y quito una, la otra debe seguir ahi."""
    tablero = Board(filas=5, columnas=5)
    p1 = Placement("SOL", fila=2, columna=0, direccion=Horizontal())
    p2 = Placement("SAL", fila=0, columna=2, direccion=Vertical())

    tablero.colocar(p1)
    tablero.colocar(p2)
    tablero.quitar(p1)  # Quitamos SOL, pero SAL sigue

    assert tablero.celda(2, 2) == "L"  # SAL todavia pone 'L' aqui
    assert tablero.esta_vacia(2, 0)  # La 'S' de SOL desaparecio
    assert tablero.esta_vacia(2, 1)  # La 'O' de SOL desaparecio
    assert tablero.esta_vacia(2, 3)  # La 'L' de SOL desaparecio


def test_limpiar_tablero():
    """Limpiar debe dejar todo como nuevo."""
    tablero = Board(filas=3, columnas=3)
    tablero.colocar(Placement("SOL", 0, 0, Horizontal()))
    tablero.limpiar()
    assert len(tablero.placements) == 0
    assert tablero.esta_vacia(0, 0)


def test_consultar_fuera_de_limites():
    """Preguntar por una casilla que no existe debe dar error."""
    tablero = Board(filas=3, columnas=3)
    try:
        tablero.celda(10, 10)
        assert False, "Deberia haber dado error"
    except ValueError:
        pass  # Esto es lo correcto