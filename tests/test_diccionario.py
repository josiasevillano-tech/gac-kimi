"""
tests/test_diccionario.py
=========================
Pruebas del diccionario de palabras.

Para correr:
    python -m pytest tests/test_diccionario.py -v
"""

import sys
import os
import json
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gac.diccionario import DiccionarioCrucigrama


def crear_diccionario_temporal(contenido: dict) -> str:
    """Helper: crea un archivo JSON temporal y devuelve su ruta."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(contenido, f)
        return f.name


def test_cargar_diccionario():
    """El diccionario carga correctamente desde un JSON."""
    ruta = crear_diccionario_temporal({
        "palabras": [
            {"palabra": "SOL", "definicion": "Estrella"},
            {"palabra": "LUNA", "definicion": "Satelite"}
        ]
    })
    dic = DiccionarioCrucigrama(ruta)
    assert dic.total == 2
    os.unlink(ruta)


def test_palabras_en_mayusculas():
    """Las palabras se normalizan a mayusculas."""
    ruta = crear_diccionario_temporal({
        "palabras": [{"palabra": "sol", "definicion": "Estrella"}]
    })
    dic = DiccionarioCrucigrama(ruta)
    assert dic.palabras_solo()[0] == "SOL"
    os.unlink(ruta)


def test_seleccionar_aleatorias():
    """Selecciona N palabras al azar."""
    ruta = crear_diccionario_temporal({
        "palabras": [
            {"palabra": "A", "definicion": "1"},
            {"palabra": "B", "definicion": "2"},
            {"palabra": "C", "definicion": "3"},
            {"palabra": "D", "definicion": "4"}
        ]
    })
    dic = DiccionarioCrucigrama(ruta)
    seleccion = dic.seleccionar_aleatorias(2)
    assert len(seleccion) == 2
    assert all("palabra" in p and "definicion" in p for p in seleccion)
    os.unlink(ruta)


def test_seleccionar_mas_de_lo_que_hay_lanza_error():
    """Pedir mas palabras de las que hay lanza ValueError."""
    ruta = crear_diccionario_temporal({
        "palabras": [{"palabra": "SOL", "definicion": "Estrella"}]
    })
    dic = DiccionarioCrucigrama(ruta)
    try:
        dic.seleccionar_aleatorias(5)
        assert False, "Deberia haber lanzado ValueError"
    except ValueError:
        pass
    os.unlink(ruta)


def test_filtrar_por_longitud():
    """Filtra palabras por longitud minima y maxima."""
    ruta = crear_diccionario_temporal({
        "palabras": [
            {"palabra": "SOL", "definicion": "3 letras"},
            {"palabra": "CASA", "definicion": "4 letras"},
            {"palabra": "ESTRELLA", "definicion": "8 letras"}
        ]
    })
    dic = DiccionarioCrucigrama(ruta)
    filtradas = dic.filtrar_por_longitud(minimo=4, maximo=6)
    palabras = [p["palabra"] for p in filtradas]
    assert "CASA" in palabras
    assert "SOL" not in palabras
    assert "ESTRELLA" not in palabras
    os.unlink(ruta)


def test_seleccionar_para_tablero():
    """Selecciona palabras que quepan en el tablero."""
    ruta = crear_diccionario_temporal({
        "palabras": [
            {"palabra": "A", "definicion": "1 letra"},
            {"palabra": "SOL", "definicion": "3 letras"},
            {"palabra": "CASA", "definicion": "4 letras"},
            {"palabra": "SUPERCALIFRAGILISTICO", "definicion": "muy larga"}
        ]
    })
    dic = DiccionarioCrucigrama(ruta)
    seleccion = dic.seleccionar_para_tablero(2, min_long=2, max_long=10)
    assert len(seleccion) == 2
    assert all(2 <= len(p["palabra"]) <= 10 for p in seleccion)
    os.unlink(ruta)


def test_archivo_no_existe_lanza_error():
    """Si el archivo JSON no existe, lanza FileNotFoundError."""
    try:
        DiccionarioCrucigrama("no_existe.json")
        assert False, "Deberia haber lanzado FileNotFoundError"
    except FileNotFoundError:
        pass