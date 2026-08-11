"""
gac/direction.py
================
Representa cómo se mueve una palabra sobre el tablero.

En el mundo real, una palabra en un crucigrama puede ir de izquierda a derecha
(HORIZONTAL) o de arriba hacia abajo (VERTICAL). Esta clase convierte esa idea
en algo que el programa puede usar para calcular posiciones.

No es solo una etiqueta. Es un comportamiento.
"""


class Direction:
    """
    Una dirección sabe cómo avanzar una casilla desde cualquier punto del tablero.
    
    Si estás en la fila 2, columna 3, y avanzas en una dirección,
    ¿a qué fila y columna llegas? Eso es lo que esta clase responde.
    """
    
    def __init__(self, nombre: str, delta_fila: int, delta_columna: int):
        """
        Crea una dirección.
        
        Args:
            nombre: Cómo se llama esta dirección (para que los humanos la entiendan).
            delta_fila: Cuántas filas avanzas cada paso (0 para horizontal, 1 para vertical).
            delta_columna: Cuántas columnas avanzas cada paso (1 para horizontal, 0 para vertical).
        """
        self._nombre = nombre
        self._delta_fila = delta_fila
        self._delta_columna = delta_columna
    
    @property
    def nombre(self) -> str:
        """El nombre humano de esta dirección."""
        return self._nombre
    
    def siguiente(self, fila: int, columna: int, pasos: int = 1) -> tuple[int, int]:
        """
        Dada una posición (fila, columna), calcula dónde quedas después de avanzar
        un número de pasos en esta dirección.
        
        Ejemplo:
            >>> h = Horizontal()
            >>> h.siguiente(2, 3, pasos=2)
            (2, 5)  # Misma fila, columna 3 + 2 = 5
        """
        return (
            fila + (self._delta_fila * pasos),
            columna + (self._delta_columna * pasos)
        )
    
    def recorrido(self, fila_inicio: int, columna_inicio: int, longitud: int):
        """
        Genera TODAS las coordenadas (fila, columna) que ocupa una palabra
        de cierta longitud que comienza en (fila_inicio, columna_inicio).
        
        Esto es útil porque una palabra no ocupa una sola casilla;
        ocupa varias casillas en línea recta.
        
        Ejemplo:
            >>> h = Horizontal()
            >>> list(h.recorrido(1, 1, longitud=4))
            [(1, 1), (1, 2), (1, 3), (1, 4)]
        """
        for paso in range(longitud):
            yield self.siguiente(fila_inicio, columna_inicio, pasos=paso)
    
    def es_horizontal(self) -> bool:
        """¿Esta dirección es horizontal?"""
        return self._delta_fila == 0
    
    def es_vertical(self) -> bool:
        """¿Esta dirección es vertical?"""
        return self._delta_columna == 0
    
    def __eq__(self, otro) -> bool:
        """Dos direcciones son iguales si avanzan de la misma manera."""
        if not isinstance(otro, Direction):
            return False
        return (self._delta_fila == otro._delta_fila and 
                self._delta_columna == otro._delta_columna)
    
    def __repr__(self) -> str:
        return f"Direction({self._nombre!r})"
    
    def __hash__(self) -> int:
        return hash((self._delta_fila, self._delta_columna))


class Horizontal(Direction):
    """La palabra avanza de izquierda a derecha. Misma fila, columna aumenta."""
    def __init__(self):
        super().__init__("Horizontal", delta_fila=0, delta_columna=1)


class Vertical(Direction):
    """La palabra avanza de arriba hacia abajo. Misma columna, fila aumenta."""
    def __init__(self):
        super().__init__("Vertical", delta_fila=1, delta_columna=0)