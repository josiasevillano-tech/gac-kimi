"""
tests/test_generator.py
=======================
Pruebas del Motor Generador.

Regla de oro: cada comportamiento del generador se prueba ANTES de implementarse.
Para correr:
    python -m pytest tests/test_generator.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gac import Board, Horizontal, Vertical, Placement
from gac.generator import CrosswordGenerator


# -------------------------------------------
# PRUEBA 1: Cabe en el tablero?
# -------------------------------------------

def test_palabra_cabe_dentro_del_tablero():
    """
    Una palabra de 3 letras colocada en (0,0) horizontal en un tablero 5x5 debe caber.
    """
    tablero = Board(filas=5, columnas=5)
    gen = CrosswordGenerator()
    assert gen.es_posicion_valida(tablero, "SOL", fila=0, columna=0, direccion=Horizontal())


def test_palabra_se_sale_por_la_derecha():
    """
    Una palabra de 5 letras en columna 3 de un tablero 5x5 se sale por la derecha.
    """
    tablero = Board(filas=5, columnas=5)
    gen = CrosswordGenerator()
    assert not gen.es_posicion_valida(tablero, "ESCUELA", fila=0, columna=3, direccion=Horizontal())


def test_palabra_se_sale_por_abajo():
    """
    Una palabra vertical de 4 letras en fila 3 de un tablero 5x5 se sale por abajo.
    """
    tablero = Board(filas=5, columnas=5)
    gen = CrosswordGenerator()
    assert not gen.es_posicion_valida(tablero, "LUZ", fila=3, columna=0, direccion=Vertical())


# -------------------------------------------
# PRUEBA 2: Las letras son compatibles?
# -------------------------------------------

def test_cruce_con_misma_letra_es_valido():
    """
    Si una casilla ya tiene 'L' y la nueva palabra tambien pone 'L' ahi, es valido.
    """
    tablero = Board(filas=5, columnas=5)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    assert gen.es_posicion_valida(tablero, "SAL", fila=0, columna=2, direccion=Vertical())


def test_cruce_con_letra_diferente_es_invalido():
    """
    Si una casilla ya tiene 'O' y la nueva palabra quiere poner 'A' ahi, es invalido.
    """
    tablero = Board(filas=5, columnas=5)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    assert not gen.es_posicion_valida(tablero, "SAL", fila=0, columna=1, direccion=Vertical())


# -------------------------------------------
# PRUEBA 3: Toca al menos una palabra existente?
# -------------------------------------------

def test_primera_palabra_puede_ir_donde_sea():
    """
    En un tablero vacio, cualquier posicion que quepa es valida para la primera palabra.
    """
    tablero = Board(filas=5, columnas=5)
    gen = CrosswordGenerator()
    assert gen.es_posicion_valida(tablero, "SOL", fila=0, columna=0, direccion=Horizontal())


def test_palabra_aislada_es_invalida():
    """
    Si ya hay una palabra en el tablero, una nueva palabra que NO la toque en ninguna
    casilla es invalida (no forma parte del crucigrama).
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=2, columna=2, direccion=Horizontal()))
    gen = CrosswordGenerator()
    assert not gen.es_posicion_valida(tablero, "LUZ", fila=8, columna=8, direccion=Horizontal())


def test_palabra_que_toca_en_extremo_es_invalida():
    """
    Si la nueva palabra solo "toca" a la existente en una casilla adyacente
    (no compartiendo letra), eso NO es un cruce valido. Es invalida.
    """
    tablero = Board(filas=5, columnas=5)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    assert not gen.es_posicion_valida(tablero, "LUZ", fila=2, columna=3, direccion=Horizontal())


# -------------------------------------------
# PRUEBA 4: Encontrar TODAS las posiciones validas
# -------------------------------------------

def test_encontrar_posiciones_para_primera_palabra():
    """
    En un tablero vacio 3x3, la palabra 'SOL' (3 letras) tiene:
    - Horizontal: filas 0, 1, 2 (en cada fila, columna 0 es el unico inicio que cabe)
      -> 3 posiciones horizontales
    - Vertical: columnas 0, 1, 2 (en cada columna, fila 0 es el unico inicio que cabe)
      -> 3 posiciones verticales
    Total: 6 posiciones validas.
    """
    tablero = Board(filas=3, columnas=3)
    gen = CrosswordGenerator()
    posiciones = gen.encontrar_posiciones_validas(tablero, "SOL")
    assert len(posiciones) == 6


def test_encontrar_posiciones_con_cruce_existente():
    """
    Con 'SOL' horizontal en (2,0), donde puede ir 'SAL'?
    Debe encontrar la posicion vertical en (0,2) que cruza en (2,2).
    """
    tablero = Board(filas=5, columnas=5)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    posiciones = gen.encontrar_posiciones_validas(tablero, "SAL")
    cruces = [p for p in posiciones
              if p.fila == 0 and p.columna == 2 and isinstance(p.direccion, Vertical)]
    assert len(cruces) == 1


# -------------------------------------------
# PRUEBA 5: Colocar la primera palabra en el centro
# -------------------------------------------

def test_colocar_primera_palabra_en_centro():
    """
    La primera palabra debe ir en el centro del tablero, horizontalmente.
    """
    tablero = Board(filas=10, columnas=10)
    gen = CrosswordGenerator()
    gen.colocar_primera_palabra(tablero, "ESCUELA")

    assert len(tablero.placements) == 1
    p = tablero.placements[0]
    assert p.palabra == "ESCUELA"
    assert p.fila == 5
    assert p.columna == 1
    assert isinstance(p.direccion, Horizontal)