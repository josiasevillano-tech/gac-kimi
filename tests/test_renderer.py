"""
tests/test_renderer.py
======================
Pruebas del renderizador HTML.

Para correr:
    python -m pytest tests/test_renderer.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gac import Board, Horizontal, Placement
from gac.renderer import HtmlRenderer
from gac.pistas import PistaNumerador


def test_render_tablero_vacio():
    """Un tablero sin palabras genera HTML de vacio."""
    board = Board(5, 5)
    renderer = HtmlRenderer()
    html = renderer.render(board)
    assert "No hay palabras" in html


def test_render_contiene_letras():
    """El HTML generado contiene las letras del tablero."""
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board)
    assert "S" in html
    assert "O" in html
    assert "L" in html


def test_render_usa_grid_css():
    """El HTML usa CSS Grid para el tablero."""
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board)
    assert "display: grid" in html
    assert "grid-template-columns" in html


def test_render_recorta_al_minimo():
    """Solo muestra la region que contiene palabras, no todo el tablero."""
    board = Board(15, 15)
    board.colocar(Placement("SOL", fila=7, columna=7, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board)
    assert "repeat(5" in html or "repeat(6" in html


def test_render_titulo_personalizado():
    """El titulo del HTML se puede personalizar."""
    board = Board(5, 5)
    board.colocar(Placement("A", fila=2, columna=2, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board, titulo="Mi Crucigrama")
    assert "Mi Crucigrama" in html
    assert "<title>Mi Crucigrama</title>" in html


def test_render_clases_css():
    """Las celdas tienen las clases CSS correctas."""
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board)
    assert "cell letter" in html
    assert "cell empty" in html


def test_render_con_numeros_muestra_span():
    """Si hay numerador, el HTML incluye el span con el numero de pista."""
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    numerador = PistaNumerador()
    html = renderer.render(board, numerador=numerador)
    assert '<span class="cell-number">1</span>' in html


def test_render_sin_numerador_no_muestra_span():
    """Sin numerador, no aparece el span de numero de pista en las celdas."""
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board)
    assert '<span class="cell-number">' not in html