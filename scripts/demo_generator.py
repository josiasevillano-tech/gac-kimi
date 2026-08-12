"""
scripts/demo_generator.py
=========================
Demo interactivo del generador de crucigramas.

Para correr:
    python scripts/demo_generator.py

Dibuja el crucigrama resuelto en la terminal con las palabras de ejemplo.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gac import Board, CrosswordGenerator


def main():
    # Lista de palabras de ejemplo
    palabras = [
        "ESCUELA",
        "SOL",
        "SAL",
        "LUZ",
        "CASA",
        "MES",
    ]

    print("=" * 50)
    print("  GENERADOR DE CRUCIGRAMAS - DEMO")
    print("=" * 50)
    print(f"Palabras a colocar: {palabras}")
    print()

    # Crear tablero y generador
    tablero = Board(filas=15, columnas=15)
    gen = CrosswordGenerator()

    # Intentar generar
    exito = gen.generar(tablero, palabras)

    if exito:
        print("CRUCIGRAMA RESUELTO")
        print("-" * 50)
        print(tablero)
        print("-" * 50)
        print()
        print("PALABRAS COLOCADAS:")
        for i, p in enumerate(tablero.placements, 1):
            dir_str = "Horizontal" if p.direccion.es_horizontal() else "Vertical"
            print(f"  {i}. {p.palabra} -> fila {p.fila}, col {p.columna}, {dir_str}")
        print()
        print(f"Total: {len(tablero.placements)} palabras colocadas")
    else:
        print("NO SE PUDO RESOLVER EL CRUCIGRAMA")
        print("Las palabras no tienen cruces compatibles.")
        print()
        print("Sugerencia: prueba con palabras que compartan letras.")

    print("=" * 50)


if __name__ == "__main__":
    main()