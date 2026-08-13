"""
scripts/web_viewer.py
=====================
Visualizador web de crucigramas.

Uso:
    python scripts/web_viewer.py SOL LUZ CASA MESA
    python scripts/web_viewer.py --aleatorio 10    (elige 10 palabras del diccionario)
    python scripts/web_viewer.py                   (pide palabras interactivamente)

Genera output/crucigrama.html y lo abre en el navegador.
No requiere dependencias externas.
"""

import sys
import os
import webbrowser
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gac import Board, CrosswordGenerator, HtmlRenderer, PistaNumerador, DiccionarioCrucigrama


def main():
    print("=" * 50)
    print("VISUALIZADOR WEB DE CRUCIGRAMAS - GAC KIMI")
    print("=" * 50)
    print()

    # Detectar modo aleatorio
    if len(sys.argv) > 1 and sys.argv[1] == "--aleatorio":
        cantidad = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        ruta_diccionario = Path(__file__).parent.parent / 'data' / 'palabras.json'
        try:
            diccionario = DiccionarioCrucigrama(ruta_diccionario)
            seleccion = diccionario.seleccionar_para_tablero(cantidad, min_long=3, max_long=12)
            palabras = [p["palabra"] for p in seleccion]
            definiciones = {p["palabra"]: p["definicion"] for p in seleccion}
            print(f"Seleccionadas {cantidad} palabras del diccionario.")
        except FileNotFoundError:
            print(f"No se encontro el diccionario en: {ruta_diccionario}")
            return
    elif len(sys.argv) > 1:
        palabras = sys.argv[1:]
        definiciones = {}
    else:
        entrada = input("Ingresa las palabras separadas por espacio (o 'aleatorio N'): ")
        if entrada.strip().lower().startswith("aleatorio"):
            partes = entrada.strip().split()
            cantidad = int(partes[1]) if len(partes) > 1 else 10
            ruta_diccionario = Path(__file__).parent.parent / 'data' / 'palabras.json'
            try:
                diccionario = DiccionarioCrucigrama(ruta_diccionario)
                seleccion = diccionario.seleccionar_para_tablero(cantidad, min_long=3, max_long=12)
                palabras = [p["palabra"] for p in seleccion]
                definiciones = {p["palabra"]: p["definicion"] for p in seleccion}
                print(f"Seleccionadas {cantidad} palabras del diccionario.")
            except FileNotFoundError:
                print(f"No se encontro el diccionario en: {ruta_diccionario}")
                return
        else:
            palabras = entrada.strip().split()
            definiciones = {}

    if not palabras:
        print("No se ingresaron palabras.")
        return

    print(f"Generando crucigrama con: {palabras}")

    board = Board(15, 15)
    gen = CrosswordGenerator()
    exito = gen.generar(board, palabras)

    if not exito:
        print("No se pudo generar el crucigrama con esas palabras.")
        return

    # Numerar pistas
    numerador = PistaNumerador()
    asignaciones = numerador.numerar(board)

    # Construir diccionario de pistas para el renderer
    pistas_render = {}
    for placement, numero in asignaciones.items():
        direccion_str = "Horizontal" if placement.direccion.es_horizontal() else "Vertical"
        definicion = definiciones.get(placement.palabra, "")
        pistas_render[numero] = {
            "palabra": placement.palabra,
            "definicion": definicion,
            "direccion": direccion_str
        }

    renderer = HtmlRenderer()
    html = renderer.render(
        board,
        titulo="Crucigrama GAC",
        numerador=numerador,
        pistas=pistas_render if definiciones else None
    )

    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    ruta_html = output_dir / 'crucigrama.html'

    with open(ruta_html, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Crucigrama guardado en: {ruta_html}")
    print("Abriendo en el navegador...")

    webbrowser.open(ruta_html.as_uri())


if __name__ == '__main__':
    main()