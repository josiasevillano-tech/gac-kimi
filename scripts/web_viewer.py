"""
scripts/web_viewer.py
=====================
Visualizador web de crucigramas interactivos.

Uso:
    python scripts/web_viewer.py SOL LUZ CASA MESA
    python scripts/web_viewer.py --aleatorio 22
    python scripts/web_viewer.py

Genera output/crucigrama.html y lo abre en el navegador.
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

    args = sys.argv[1:]
    modo_aleatorio = "--aleatorio" in args
    args_limpios = [a for a in args if a != "--aleatorio"]

    if modo_aleatorio:
        cantidad = int(args_limpios[0]) if args_limpios else 22
        ruta_diccionario = Path(__file__).parent.parent / 'data' / 'palabras.json'
        try:
            diccionario = DiccionarioCrucigrama(ruta_diccionario)
            seleccion = diccionario.seleccionar_para_tablero(cantidad, min_long=3, max_long=12)
            palabras = []
            definiciones = {}
            for p in seleccion:
                palabras.append(p["palabra"])
                definiciones[p["palabra"]] = p["definicion"]
            print("Seleccionadas " + str(cantidad) + " palabras del diccionario.")
        except FileNotFoundError:
            print("No se encontro el diccionario en: " + str(ruta_diccionario))
            return
    elif args_limpios:
        palabras = args_limpios
        definiciones = {}
    else:
        entrada = input("Ingresa las palabras separadas por espacio (o 'aleatorio N'): ")
        if entrada.strip().lower().startswith("aleatorio"):
            partes = entrada.strip().split()
            cantidad = int(partes[1]) if len(partes) > 1 else 22
            ruta_diccionario = Path(__file__).parent.parent / 'data' / 'palabras.json'
            try:
                diccionario = DiccionarioCrucigrama(ruta_diccionario)
                seleccion = diccionario.seleccionar_para_tablero(cantidad, min_long=3, max_long=12)
                palabras = []
                definiciones = {}
                for p in seleccion:
                    palabras.append(p["palabra"])
                    definiciones[p["palabra"]] = p["definicion"]
                print("Seleccionadas " + str(cantidad) + " palabras del diccionario.")
            except FileNotFoundError:
                print("No se encontro el diccionario en: " + str(ruta_diccionario))
                return
        else:
            palabras = entrada.strip().split()
            definiciones = {}

    if not palabras:
        print("No se ingresaron palabras.")
        return

    print("Generando crucigrama con: " + str(palabras))

    board = Board(20, 20)
    gen = CrosswordGenerator()
    exito = gen.generar(board, palabras)

    if not exito:
        print("No se pudo generar el crucigrama con esas palabras.")
        return

    numerador = PistaNumerador()
    asignaciones = numerador.numerar(board)

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
        pistas=pistas_render if definiciones else None,
        interactivo=True
    )

    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    ruta_html = output_dir / 'crucigrama.html'

    with open(ruta_html, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Crucigrama guardado en: " + str(ruta_html))
    print("Abriendo en el navegador...")

    webbrowser.open(ruta_html.as_uri())


if __name__ == '__main__':
    main()