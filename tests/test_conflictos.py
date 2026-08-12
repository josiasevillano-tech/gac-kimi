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