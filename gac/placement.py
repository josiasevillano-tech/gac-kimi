"""
gac/placement.py
================
Representa el hecho concreto de haber puesto una palabra en un tablero.

Una palabra por sí sola es solo texto. Pero cuando la "pones" en un crucigrama,
eso es un Placement: sabe QUÉ palabra es, DÓNDE comienza, y HACIA DÓNDE va.

Gracias a esto, puedes reconstruir completamente cualquier crucigrama.
"""

from .direction import Direction


class Placement:
    """
    El acto de colocar una palabra en el tablero.
    
    Piensa en esto como una ficha de archivo que dice:
    "La palabra 'PYTHON' comienza en la fila 3, columna 5, y va horizontalmente."
    """
    
    def __init__(self, palabra: str, fila: int, columna: int, direccion: Direction):
        """
        Crea un Placement.
        
        Args:
            palabra: El texto de la palabra (ej: "EDUCACION").
            fila: La fila donde comienza (0 es la primera fila arriba).
            columna: La columna donde comienza (0 es la primera columna a la izquierda).
            direccion: Un objeto Direction (Horizontal o Vertical) que indica hacia dónde crece.
        """
        self._palabra = palabra.upper()
        self._fila = fila
        self._columna = columna
        self._direccion = direccion
    
    @property
    def palabra(self) -> str:
        """El texto de la palabra colocada."""
        return self._palabra
    
    @property
    def fila(self) -> int:
        """La fila donde comienza esta palabra."""
        return self._fila
    
    @property
    def columna(self) -> int:
        """La columna donde comienza esta palabra."""
        return self._columna
    
    @property
    def direccion(self) -> Direction:
        """La dirección en la que avanza esta palabra."""
        return self._direccion
    
    @property
    def longitud(self) -> int:
        """Cuántas letras tiene esta palabra."""
        return len(self._palabra)
    
    def posiciones(self):
        """
        Genera todas las coordenadas (fila, columna) que ocupa esta palabra.
        
        Ejemplo:
            Si la palabra es "SOL" en fila 1, columna 1, horizontal:
            → (1, 1), (1, 2), (1, 3)
        """
        return self._direccion.recorrido(self._fila, self._columna, self.longitud)
    
    def letra_en(self, fila: int, columna: int) -> str | None:
        """
        Si la casilla (fila, columna) es parte de esta palabra,
        devuelve la letra que va ahí. Si no, devuelve None.
        
        Esto es crucial para saber si dos palabras se cruzan correctamente.
        """
        for idx, (f, c) in enumerate(self.posiciones()):
            if f == fila and c == columna:
                return self._palabra[idx]
        return None
    
    def __repr__(self) -> str:
        return (f"Placement({self._palabra!r}, fila={self._fila}, "
                f"columna={self._columna}, {self._direccion.nombre})")
    
    def __eq__(self, otro) -> bool:
        """Dos placements son iguales si colocan la misma palabra en el mismo lugar."""
        if not isinstance(otro, Placement):
            return False
        return (self._palabra == otro._palabra and 
                self._fila == otro._fila and 
                self._columna == otro._columna and 
                self._direccion == otro._direccion)
    
    def __hash__(self) -> int:
        return hash((self._palabra, self._fila, self._columna, self._direccion))