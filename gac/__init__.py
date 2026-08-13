"""
gac/__init__.py
===============
Paquete del Generador Automatico de Crucigramas (GAC).

Exporta las piezas principales del dominio para que el usuario pueda hacer:
    from gac import Board, CrosswordGenerator, HtmlRenderer, PistaNumerador
"""

from .direction import Direction, Horizontal, Vertical
from .placement import Placement
from .board import Board
from .generator import CrosswordGenerator
from .renderer import HtmlRenderer
from .pistas import PistaNumerador

__all__ = [
    "Direction",
    "Horizontal", 
    "Vertical",
    "Placement",
    "Board",
    "CrosswordGenerator",
    "HtmlRenderer",
    "PistaNumerador",
]