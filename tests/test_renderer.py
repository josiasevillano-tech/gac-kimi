"""
tests/test_renderer.py
======================
Pruebas del renderizador HTML interactivo.

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
    board = Board(5, 5)
    renderer = HtmlRenderer()
    html = renderer.render(board)
    assert "No hay palabras" in html


def test_render_contiene_inputs_interactivos():
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board, interactivo=True)
    assert '<input type="text"' in html
    assert 'data-solucion="S"' in html


def test_render_modo_estatico_no_tiene_inputs():
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board, interactivo=False)
    assert '<input type="text"' not in html


def test_render_contiene_botones():
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board, interactivo=True)
    assert 'id="btn-verificar"' in html
    assert 'id="btn-pista"' in html
    assert 'id="btn-limpiar"' in html
    assert 'id="btn-reiniciar"' in html


def test_render_contiene_barra_progreso():
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board, interactivo=True)
    assert 'id="progreso-fill"' in html
    assert 'id="progreso-texto"' in html


def test_render_click_en_pistas_tiene_onclick():
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    numerador = PistaNumerador()
    pistas = {1: {"palabra": "SOL", "definicion": "Estrella", "direccion": "Horizontal"}}
    html = renderer.render(board, numerador=numerador, pistas=pistas, interactivo=True)
    assert 'onclick="irAPalabra(1)"' in html
    assert 'class="pista-item"' in html


def test_render_navegacion_por_coordenadas():
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board, interactivo=True)
    assert "getInput(" in html


def test_render_sin_auto_avance():
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board, interactivo=True)
    assert "inputs[idx+1]" not in html


def test_render_con_pistas_muestra_panel():
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    numerador = PistaNumerador()
    pistas = {1: {"palabra": "SOL", "definicion": "Estrella del dia", "direccion": "Horizontal"}}
    html = renderer.render(board, numerador=numerador, pistas=pistas)
    assert 'class="pistas-panel"' in html
    assert "Horizontales" in html


def test_render_contiene_javascript():
    board = Board(5, 5)
    board.colocar(Placement("SOL", fila=2, columna=1, direccion=Horizontal()))
    renderer = HtmlRenderer()
    html = renderer.render(board, interactivo=True)
    assert "<script>" in html
    assert "soluciones=" in html
    assert "irAPalabra" in html