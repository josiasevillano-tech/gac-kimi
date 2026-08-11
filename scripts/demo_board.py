#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/demo_board.py
=====================
¡BIENVENIDO AL TALLER DEL GAC!

Este archivo es tu "mando a distancia" para jugar con el tablero.
No necesitas saber programar. Solo necesitas ejecutarlo y seguir las instrucciones.

CÓMO USARLO:
1. Abre tu terminal dentro de la carpeta gac-proyecto
2. Escribe: python scripts/demo_board.py
3. Lee el menú y elige un número.

Eso es todo.
"""

import sys
import os

# Aseguramos que Python encuentre la carpeta gac/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gac import Board, Horizontal, Vertical, Placement


def mostrar_menu():
    print("\n" + "=" * 50)
    print("   🏗️  TALLER DEL TABLERO (BOARD)")
    print("=" * 50)
    print("Elige qué quieres hacer escribiendo un número:")
    print()
    print("  1️⃣  Ver el tablero vacío")
    print("  2️⃣  Colocar una palabra de ejemplo")
    print("  3️⃣  Ver el tablero actual")
    print("  4️⃣  Ver qué palabras están colocadas")
    print("  5️⃣  Quitar la última palabra colocada")
    print("  6️⃣  Limpiar todo el tablero")
    print("  7️⃣  Colocar mi propia palabra (avanzado)")
    print("  0️⃣  Salir")
    print("=" * 50)


def pausa():
    input("\nPresiona ENTER para continuar...")


def main():
    # Creamos un tablero de 10x10 para que sea fácil de ver en pantalla
    tablero = Board(filas=10, columnas=10)
    
    # Lista de palabras de ejemplo que el usuario puede colocar con un click
    palabras_ejemplo = [
        ("ESCUELA", 2, 2, Horizontal()),
        ("PENSAR", 4, 4, Vertical()),
        ("SABIDURIA", 0, 5, Horizontal()),
        ("VERDAD", 6, 1, Horizontal()),
        ("HUMILDAD", 1, 7, Vertical()),
    ]
    
    indice_ejemplo = 0
    
    print("\n" + "🎉" * 20)
    print("¡BIENVENIDO AL GENERADOR AUTOMÁTICO DE CRUCIGRAMAS!")
    print("🎉" * 20)
    print("\nEste es tu tablero. Ahora está vacío, como un lienzo en blanco.")
    print("Vamos a poner algunas palabras para que veas cómo funciona.")
    pausa()
    
    while True:
        mostrar_menu()
        opcion = input("\nTu elección: ").strip()
        
        if opcion == "1":
            print("\n📋 TABLERO VACÍO:")
            print(tablero)
            print("\n¿Ves todos esos puntos? Son casillas vacías esperando palabras.")
            pausa()
        
        elif opcion == "2":
            if indice_ejemplo >= len(palabras_ejemplo):
                print("\n✅ Ya colocamos todas las palabras de ejemplo.")
                print("Prueba la opción 7 si quieres poner tu propia palabra.")
                pausa()
                continue
            
            palabra, fila, col, direccion = palabras_ejemplo[indice_ejemplo]
            placement = Placement(palabra, fila, col, direccion)
            
            print(f"\n➕ Colocando: '{palabra}' en fila {fila}, columna {col}, {direccion.nombre}")
            tablero.colocar(placement)
            indice_ejemplo += 1
            
            print("\n¡Listo! Así se ve ahora:")
            print(tablero)
            print(f"\nAhora hay {len(tablero.placements)} palabra(s) en el tablero.")
            pausa()
        
        elif opcion == "3":
            print("\n📋 TABLERO ACTUAL:")
            print(tablero)
            print(f"\nPalabras colocadas: {len(tablero.placements)}")
            pausa()
        
        elif opcion == "4":
            placements = tablero.placements
            if not placements:
                print("\n📭 No hay palabras colocadas todavía.")
            else:
                print("\n📋 PALABRAS COLOCADAS:")
                for i, p in enumerate(placements, 1):
                    print(f"  {i}. {p}")
            pausa()
        
        elif opcion == "5":
            placements = tablero.placements
            if not placements:
                print("\n📭 No hay nada que quitar.")
            else:
                ultimo = placements[-1]
                print(f"\n➖ Quitando: {ultimo}")
                tablero.quitar(ultimo)
                print("\nAsí se ve ahora:")
                print(tablero)
            pausa()
        
        elif opcion == "6":
            print("\n🧹 Limpiando el tablero completamente...")
            tablero.limpiar()
            indice_ejemplo = 0
            print("✅ Tablero vacío de nuevo.")
            print(tablero)
            pausa()
        
        elif opcion == "7":
            print("\n✏️  COLOCAR TU PROPIA PALABRA")
            print("Te voy a pedir 4 cosas. Si te equivocas, no pasa nada.")
            try:
                palabra = input("  Escribe la palabra (sin espacios): ").strip().upper()
                if not palabra.isalpha():
                    print("❌ Solo letras, por favor.")
                    pausa()
                    continue
                
                fila = int(input(f"  ¿En qué FILA comienza? (0 a {tablero.filas - 1}): "))
                col = int(input(f"  ¿En qué COLUMNA comienza? (0 a {tablero.columnas - 1}): "))
                
                dir_input = input("  ¿Horizontal (H) o Vertical (V)?: ").strip().upper()
                if dir_input == "H":
                    direccion = Horizontal()
                elif dir_input == "V":
                    direccion = Vertical()
                else:
                    print("❌ Escribe H o V.")
                    pausa()
                    continue
                
                placement = Placement(palabra, fila, col, direccion)
                tablero.colocar(placement)
                
                print(f"\n✅ ¡'{palabra}' colocada con éxito!")
                print(tablero)
                
            except ValueError as e:
                print(f"\n❌ Algo salió mal: {e}")
                print("No te preocupes, inténtalo de nuevo.")
            
            pausa()
        
        elif opcion == "0":
            print("\n👋 ¡Gracias por visitar el taller del GAC!")
            print("Recuerda: cada gran crucigrama empieza con un solo tablero vacío.")
            print("Nos vemos en la siguiente fase. 🏗️")
            break
        
        else:
            print("\n❓ No entendí esa opción. Elige un número del 0 al 7.")
            pausa()


if __name__ == "__main__":
    main()