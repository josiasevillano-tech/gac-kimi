"""
gac/board.py
============
El tablero es la fotografía completa de un crucigrama en un momento dado.

Imagina que tomas una foto a un crucigrama de papel. Esa foto ES un Board.
Sabe cuántas casillas tiene de ancho y de alto.
Sabe qué letra hay en cada casilla (o si está vacía).
Sabe qué palabras han sido colocadas.

Pero el tablero NO decide dónde poner las palabras. Eso es trabajo de otro.
El tablero solo "recuerda" lo que ya está puesto.
"""

from .placement import Placement


class Board:
    """
    Representa el estado completo de un crucigrama.
    
    Es como una cuadrícula de papel cuadriculado donde cada casilla puede tener:
    - Una letra (si una palabra pasa por ahí)
    - Vacía (si nadie ha puesto nada ahí todavía)
    - Nada más. (En el futuro podríamos añadir casillas bloqueadas, pero ahora no.)
    """
    
    def __init__(self, filas: int, columnas: int):
        """
        Crea un tablero vacío.
        
        Args:
            filas: Cuántas filas de alto tiene el tablero (ej: 15).
            columnas: Cuántas columnas de ancho tiene el tablero (ej: 15).
        """
        self._filas = filas
        self._columnas = columnas
        
        # La cuadrícula interna: una lista de listas.
        # Cada casilla empieza vacía (None).
        # Más adelante, una casilla puede contener una letra como "A", "B", etc.
        self._celdas = [[None for _ in range(columnas)] for _ in range(filas)]
        
        # Lista de todos los placements (palabras colocadas) en este tablero.
        # Empieza vacía porque recién se crea.
        self._placements: list[Placement] = []
    
    @property
    def filas(self) -> int:
        """Cuántas filas de alto tiene el tablero."""
        return self._filas
    
    @property
    def columnas(self) -> int:
        """Cuántas columnas de ancho tiene el tablero."""
        return self._columnas
    
    @property
    def placements(self) -> list[Placement]:
        """Todas las palabras que han sido colocadas en este tablero."""
        return list(self._placements)
    
    def esta_dentro(self, fila: int, columna: int) -> bool:
        """
        ¿Esta coordenada existe dentro del tablero?
        
        Ejemplo: en un tablero de 5x5, la fila 10 no existe.
        """
        return 0 <= fila < self._filas and 0 <= columna < self._columnas
    
    def celda(self, fila: int, columna: int) -> str | None:
        """
        ¿Qué hay en esta casilla?
        
        Devuelve:
        - Una letra (ej: "A") si hay una palabra pasando por ahí.
        - None si la casilla está vacía.
        - Lanza un error si preguntas por una casilla que no existe.
        """
        if not self.esta_dentro(fila, columna):
            raise ValueError(f"La casilla ({fila}, {columna}) está fuera del tablero. "
                           f"El tablero solo tiene {self._filas} filas y {self._columnas} columnas.")
        return self._celdas[fila][columna]
    
    def esta_vacia(self, fila: int, columna: int) -> bool:
        """¿Esta casilla está vacía (sin letra)?"""
        return self.celda(fila, columna) is None
    
    def esta_ocupada(self, fila: int, columna: int) -> bool:
        """¿Esta casilla tiene una letra?"""
        return not self.esta_vacia(fila, columna)
    
    def colocar(self, placement: Placement) -> None:
        """
        Pone una palabra en el tablero.
        
        Esto NO verifica si es legal o no. Eso es trabajo de otro (el generador).
        El tablero simplemente "recuerda" que esta palabra está aquí.
        
        Args:
            placement: Un objeto Placement que dice qué palabra, dónde y en qué dirección.
        """
        # Guardamos el placement en nuestra lista
        self._placements.append(placement)
        
        # Marcamos cada casilla que ocupa esta palabra
        for idx, (f, c) in enumerate(placement.posiciones()):
            if self.esta_dentro(f, c):
                self._celdas[f][c] = placement.palabra[idx]
    
    def quitar(self, placement: Placement) -> None:
        """
        Saca una palabra del tablero.
        
        Esto es útil cuando el generador prueba una posición, ve que no funciona,
        y necesita "deshacer" el movimiento.
        
        Args:
            placement: El placement que se desea quitar.
        """
        if placement not in self._placements:
            return  # Si no está, no hacemos nada
        
        self._placements.remove(placement)
        
        # Pero OJO: una casilla podría ser compartida por DOS palabras.
        # Si quitamos una, no debemos borrar la letra si otra palabra la necesita.
        for f, c in placement.posiciones():
            if self.esta_dentro(f, c):
                # ¿Alguna otra palabra todavía usa esta casilla?
                todavia_necesaria = False
                for otro in self._placements:
                    if otro.letra_en(f, c) is not None:
                        todavia_necesaria = True
                        break
                
                if not todavia_necesaria:
                    self._celdas[f][c] = None
    
    def limpiar(self) -> None:
        """
        Vacía completamente el tablero, como si nunca se hubiera puesto nada.
        """
        self._placements.clear()
        for f in range(self._filas):
            for c in range(self._columnas):
                self._celdas[f][c] = None
    
    def __str__(self) -> str:
        """
        Dibuja el tablero como texto para que un humano lo vea.
        
        Las casillas vacías se ven como puntos (.) para que se distingan.
        Las letras se ven en mayúsculas.
        """
        lineas = []
        # Borde superior con números de columna
        header = "    " + " ".join(f"{c:2}" for c in range(self._columnas))
        lineas.append(header)
        lineas.append("   +" + "-" * (self._columnas * 3) + "-")
        
        for f in range(self._filas):
            fila_str = f"{f:2} |"
            for c in range(self._columnas):
                contenido = self._celdas[f][c]
                fila_str += f" {contenido if contenido is not None else '.'} "
            lineas.append(fila_str)
        
        return "\n".join(lineas)
    
    def __repr__(self) -> str:
        return f"Board({self._filas}x{self._columnas}, {len(self._placements)} placements)"