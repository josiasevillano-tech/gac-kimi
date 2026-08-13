"""
tests/test_conflictos.py
========================
Pruebas de las reglas de conflictos avanzados del generador.

Estas reglas evitan que el crucigrama se vea "sucio".
Para correr:
    python -m pytest tests/test_conflictos.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gac import Board, Horizontal, Vertical, Placement
from gac.generator import CrosswordGenerator


# ===========================================
# REGLA 1: PARALELISMO PEGADO
# ===========================================

def test_paralelismo_pegado_dos_horizontales_consecutivas():
    """
    'SOL' en fila 2 horizontal y 'LUZ' en fila 3 horizontal, cols 0-2.
    Filas consecutivas + columnas solapadas = paralelismo pegado -> True.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    nuevo = Placement("LUZ", fila=3, columna=0, direccion=Horizontal())
    assert gen._hay_paralelismo_pegado(tablero, nuevo)


def test_paralelismo_pegado_dos_horizontales_separadas():
    """
    'SOL' en fila 2 y 'LUZ' en fila 4 (fila 3 vacia entre medio).
    No son consecutivas -> False.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    nuevo = Placement("LUZ", fila=4, columna=0, direccion=Horizontal())
    assert not gen._hay_paralelismo_pegado(tablero, nuevo)


def test_paralelismo_pegado_dos_horizontales_consecutivas_sin_solapar():
    """
    'SOL' en fila 2, cols 0-2. 'LUZ' en fila 3, cols 5-7.
    Filas consecutivas pero columnas NO se solapan -> False.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    nuevo = Placement("LUZ", fila=3, columna=5, direccion=Horizontal())
    assert not gen._hay_paralelismo_pegado(tablero, nuevo)


def test_paralelismo_pegado_dos_verticales_consecutivas():
    """
    'SOL' vertical en col 2, filas 0-2. 'LUZ' vertical en col 3, filas 0-2.
    Columnas consecutivas + filas solapadas -> True.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=0, columna=2, direccion=Vertical()))
    gen = CrosswordGenerator()
    nuevo = Placement("LUZ", fila=0, columna=3, direccion=Vertical())
    assert gen._hay_paralelismo_pegado(tablero, nuevo)


def test_paralelismo_pegado_dos_verticales_separadas():
    """
    'SOL' en col 2 y 'LUZ' en col 4 (col 3 vacia entre medio).
    No son consecutivas -> False.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=0, columna=2, direccion=Vertical()))
    gen = CrosswordGenerator()
    nuevo = Placement("LUZ", fila=0, columna=4, direccion=Vertical())
    assert not gen._hay_paralelismo_pegado(tablero, nuevo)


# ===========================================
# REGLA 2: CONTINUIDAD ILEGAL
# ===========================================

def test_continuidad_ilegal_dos_horizontales_misma_fila_pegadas():
    """
    'SOL' en fila 2, cols 0-2. 'LUZ' en fila 2, cols 3-5.
    Misma fila, adyacentes (col 2 y col 3 se tocan) -> True.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    nuevo = Placement("LUZ", fila=2, columna=3, direccion=Horizontal())
    assert gen._hay_continuidad_ilegal(tablero, nuevo)


def test_continuidad_ilegal_dos_horizontales_misma_fila_con_espacio():
    """
    'SOL' en fila 2, cols 0-2. 'LUZ' en fila 2, cols 4-6.
    Misma fila, separadas por col 3 -> False.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    nuevo = Placement("LUZ", fila=2, columna=4, direccion=Horizontal())
    assert not gen._hay_continuidad_ilegal(tablero, nuevo)


def test_continuidad_ilegal_dos_verticales_misma_columna_pegadas():
    """
    'SOL' en col 2, filas 0-2. 'LUZ' en col 2, filas 3-5.
    Misma columna, adyacentes (fila 2 y fila 3 se tocan) -> True.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=0, columna=2, direccion=Vertical()))
    gen = CrosswordGenerator()
    nuevo = Placement("LUZ", fila=3, columna=2, direccion=Vertical())
    assert gen._hay_continuidad_ilegal(tablero, nuevo)


def test_continuidad_ilegal_dos_verticales_misma_columna_con_espacio():
    """
    'SOL' en col 2, filas 0-2. 'LUZ' en col 2, filas 4-6.
    Misma columna, separadas por fila 3 -> False.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=0, columna=2, direccion=Vertical()))
    gen = CrosswordGenerator()
    nuevo = Placement("LUZ", fila=4, columna=2, direccion=Vertical())
    assert not gen._hay_continuidad_ilegal(tablero, nuevo)


# ===========================================
# REGLA 3: SUBPALABRAS DE 2 LETRAS
# ===========================================

def test_subpalabra_dos_letras_vertical_por_extremo():
    """
    'AL' vertical en col 2, filas 2-3: A(2,2), L(3,2).
    'SOL' horizontal en fila 3, cols 0-2: S(3,0), O(3,1), L(3,2).
    En (3,2), verticalmente: A(2,2), L(3,2) = exactamente 2 letras -> True.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("AL", fila=2, columna=2, direccion=Vertical()))
    gen = CrosswordGenerator()
    nuevo = Placement("SOL", fila=3, columna=0, direccion=Horizontal())
    assert gen._hay_subpalabra_dos_letras(tablero, nuevo)


def test_subpalabra_dos_letras_horizontal_por_extremo():
    """
    'LA' horizontal en fila 2, cols 3-4: L(2,3), A(2,4).
    'SAL' vertical en col 3, filas 0-2: S(0,3), A(1,3), L(2,3).
    En (2,3), horizontalmente: L(2,3), A(2,4) = 2 letras -> True.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("LA", fila=2, columna=3, direccion=Horizontal()))
    gen = CrosswordGenerator()
    nuevo = Placement("SAL", fila=0, columna=3, direccion=Vertical())
    assert gen._hay_subpalabra_dos_letras(tablero, nuevo)


def test_no_subpalabra_dos_letras_cuando_hay_tres():
    """
    'SAL' vertical en col 2, filas 0-2. 'LAS' horizontal en fila 2, cols 0-2.
    En (2,2), verticalmente: S(0,2), A(1,2), L(2,2) = 3 letras -> False.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SAL", fila=0, columna=2, direccion=Vertical()))
    gen = CrosswordGenerator()
    nuevo = Placement("LAS", fila=2, columna=0, direccion=Horizontal())
    assert not gen._hay_subpalabra_dos_letras(tablero, nuevo)


def test_no_subpalabra_dos_letras_sin_vecinos():
    """
    'SOL' horizontal en fila 2. 'SAL' vertical en col 5, no toca a SOL.
    Ninguna casilla de SAL tiene vecinos perpendiculares -> False.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    nuevo = Placement("SAL", fila=0, columna=5, direccion=Vertical())
    assert not gen._hay_subpalabra_dos_letras(tablero, nuevo)


def test_es_posicion_valida_rechaza_subpalabra_dos_letras():
    """
    'AL' vertical en col 2, filas 2-3. 'SOL' horizontal en fila 3, cols 0-2.
    SOL comparte (3,2) con AL. Pero verticalmente en col 2 solo hay 2 letras.
    es_posicion_valida debe rechazar por regla 6.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("AL", fila=2, columna=2, direccion=Vertical()))
    gen = CrosswordGenerator()
    assert not gen.es_posicion_valida(tablero, "SOL", fila=3, columna=0, direccion=Horizontal())


# ===========================================
# CASOS ESPECIALES
# ===========================================

def test_continuidad_ilegal_no_afecta_cruce_perpendicular():
    """
    'SOL' horizontal en (2,0). 'SAL' vertical en (0,2) cruzando en (2,2).
    Direcciones diferentes -> no aplica continuidad ilegal -> False.
    """
    tablero = Board(filas=5, columnas=5)
    tablero.colocar(Placement("SOL", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    nuevo = Placement("SAL", fila=0, columna=2, direccion=Vertical())
    assert not gen._hay_continuidad_ilegal(tablero, nuevo)


def test_continuidad_ilegal_no_afecta_superposicion():
    """
    'SOLA' horizontal en (2,0): S-O-L-A (cols 0,1,2,3).
    'ALTO' horizontal en (2,3): A-L-T-O (cols 3,4,5,6).
    Comparten la 'A' en col 3. Eso es superposicion, no continuidad ilegal -> False.
    """
    tablero = Board(filas=10, columnas=10)
    tablero.colocar(Placement("SOLA", fila=2, columna=0, direccion=Horizontal()))
    gen = CrosswordGenerator()
    nuevo = Placement("ALTO", fila=2, columna=3, direccion=Horizontal())
    assert not gen._hay_continuidad_ilegal(tablero, nuevo)