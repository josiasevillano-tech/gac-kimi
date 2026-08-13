"""
gac/diccionario.py
==================
Gestiona un diccionario de palabras con definiciones para crucigramas.

Principio: "El diccionario provee; el generador consume."
"""

import json
import random
from pathlib import Path


class DiccionarioCrucigrama:
    """
    Carga y gestiona un conjunto de palabras con sus definiciones.

    Lee desde un archivo JSON con formato:
    {
      "palabras": [
        {"palabra": "SOL", "definicion": "Estrella que ilumina el dia"},
        ...
      ]
    }
    """

    def __init__(self, ruta_json: str | Path):
        """
        Carga el diccionario desde un archivo JSON.

        Args:
            ruta_json: Ruta al archivo JSON de palabras.
        """
        self._ruta = Path(ruta_json)
        self._palabras: list[dict[str, str]] = []
        self._cargar()

    def _cargar(self) -> None:
        """Carga las palabras desde el archivo JSON."""
        if not self._ruta.exists():
            raise FileNotFoundError(f"No se encontro el diccionario: {self._ruta}")

        with open(self._ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        self._palabras = datos.get("palabras", [])

        # Normalizar: mayusculas, sin espacios
        for item in self._palabras:
            item["palabra"] = item["palabra"].upper().strip()
            item["definicion"] = item["definicion"].strip()

    @property
    def total(self) -> int:
        """Cuantas palabras hay en el diccionario."""
        return len(self._palabras)

    def todas(self) -> list[dict[str, str]]:
        """Devuelve todas las palabras con sus definiciones."""
        return list(self._palabras)

    def palabras_solo(self) -> list[str]:
        """Devuelve solo las palabras (sin definiciones)."""
        return [p["palabra"] for p in self._palabras]

    def seleccionar_aleatorias(self, cantidad: int) -> list[dict[str, str]]:
        """
        Elige N palabras al azar del diccionario.

        Args:
            cantidad: Cuantas palabras seleccionar.

        Returns:
            Lista de diccionarios {"palabra": ..., "definicion": ...}
        """
        if cantidad > len(self._palabras):
            raise ValueError(
                f"Se pidieron {cantidad} palabras pero solo hay {len(self._palabras)}"
            )
        return random.sample(self._palabras, cantidad)

    def filtrar_por_longitud(self, minimo: int = 3, maximo: int = 15) -> list[dict[str, str]]:
        """
        Devuelve solo las palabras cuya longitud este en el rango [minimo, maximo].

        Util para asegurar que las palabras quepan en el tablero.
        """
        return [
            p for p in self._palabras
            if minimo <= len(p["palabra"]) <= maximo
        ]

    def seleccionar_para_tablero(self, cantidad: int, min_long: int = 3, max_long: int = 15) -> list[dict[str, str]]:
        """
        Elige N palabras al azar que quepan en el tablero.

        Combina filtrado por longitud y seleccion aleatoria.
        """
        candidatas = self.filtrar_por_longitud(min_long, max_long)
        if cantidad > len(candidatas):
            raise ValueError(
                f"Se pidieron {cantidad} palabras pero solo {len(candidatas)} "
                f"caben en el rango de longitud [{min_long}, {max_long}]"
            )
        return random.sample(candidatas, cantidad)