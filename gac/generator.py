"""
gac/generator.py
================
Motor generador de crucigramas.

Este modulo contiene la logica que decide DONDE poner las palabras.
No guarda estado (eso lo hace Board). Solo evalua y decide.

Principio: "El algoritmo se adapta al dominio; el dominio nunca al algoritmo."
"""

from .board import Board
from .placement import Placement
from .direction import Direction, Horizontal, Vertical


class CrosswordGenerator:
    """
    Servicio que construye crucigramas automaticamente.

    No tiene memoria propia. Recibe un Board, le pregunta cosas,
    y le dice que colocar. El Board es quien recuerda.
    """

    # -- Metodos auxiliares para rangos --

    def _rango_filas(self, placement: Placement) -> tuple[int, int]:
        """Devuelve (fila_inicio, fila_fin) que ocupa un placement."""
        posiciones = list(placement.posiciones())
        filas = [f for f, c in posiciones]
        return min(filas), max(filas)

    def _rango_columnas(self, placement: Placement) -> tuple[int, int]:
        """Devuelve (columna_inicio, columna_fin) que ocupa un placement."""
        posiciones = list(placement.posiciones())
        columnas = [c for f, c in posiciones]
        return min(columnas), max(columnas)

    def _rangos_se_solapan(self, a_inicio: int, a_fin: int, b_inicio: int, b_fin: int) -> bool:
        """
        Dos rangos [a_inicio, a_fin] y [b_inicio, b_fin] se solapan
        si comparten al menos un punto.
        """
        return max(a_inicio, b_inicio) <= min(a_fin, b_fin)

    # -- Regla 4: Paralelismo pegado --

    def _hay_paralelismo_pegado(self, board: Board, placement_nuevo: Placement) -> bool:
        """
        Dos palabras del mismo sentido no pueden estar en filas/columnas
        consecutivas sin una casilla de separacion.

        Ejemplo invalido:
            SOL horizontal en fila 2, cols 0-2
            LUZ horizontal en fila 3, cols 0-2
            -> Filas consecutivas (2 y 3) y columnas solapadas = pegado
        """
        nuevo_fila_ini, nuevo_fila_fin = self._rango_filas(placement_nuevo)
        nuevo_col_ini, nuevo_col_fin = self._rango_columnas(placement_nuevo)
        nueva_es_h = placement_nuevo.direccion.es_horizontal()
        nueva_es_v = placement_nuevo.direccion.es_vertical()

        for existente in board.placements:
            # Solo comparamos del mismo sentido
            misma_direccion = (
                (nueva_es_h and existente.direccion.es_horizontal()) or
                (nueva_es_v and existente.direccion.es_vertical())
            )
            if not misma_direccion:
                continue

            exist_fila_ini, exist_fila_fin = self._rango_filas(existente)
            exist_col_ini, exist_col_fin = self._rango_columnas(existente)

            if nueva_es_h:
                # Ambos horizontales: filas consecutivas?
                filas_consecutivas = abs(nuevo_fila_ini - exist_fila_ini) == 1
                cols_solapadas = self._rangos_se_solapan(
                    nuevo_col_ini, nuevo_col_fin, exist_col_ini, exist_col_fin
                )
                if filas_consecutivas and cols_solapadas:
                    return True

            if nueva_es_v:
                # Ambos verticales: columnas consecutivas?
                cols_consecutivas = abs(nuevo_col_ini - exist_col_ini) == 1
                filas_solapadas = self._rangos_se_solapan(
                    nuevo_fila_ini, nuevo_fila_fin, exist_fila_ini, exist_fila_fin
                )
                if cols_consecutivas and filas_solapadas:
                    return True

        return False

    # -- Regla 5: Continuidad ilegal --

    def _hay_continuidad_ilegal(self, board: Board, placement_nuevo: Placement) -> bool:
        """
        Dos palabras del mismo sentido no pueden estar pegadas por los
        extremos en la misma fila/columna, formando una palabra fantasma.

        Ejemplo invalido:
            SOL horizontal en fila 2, cols 0-2
            LUZ horizontal en fila 2, cols 3-5
            -> Misma fila, adyacentes (col 2 y col 3 se tocan) = continuidad ilegal

        Pero si se solapan (comparten casilla) o hay espacio entre medio, es valido.
        """
        nuevo_fila_ini, nuevo_fila_fin = self._rango_filas(placement_nuevo)
        nuevo_col_ini, nuevo_col_fin = self._rango_columnas(placement_nuevo)
        nueva_es_h = placement_nuevo.direccion.es_horizontal()
        nueva_es_v = placement_nuevo.direccion.es_vertical()

        for existente in board.placements:
            # Solo comparamos del mismo sentido
            misma_direccion = (
                (nueva_es_h and existente.direccion.es_horizontal()) or
                (nueva_es_v and existente.direccion.es_vertical())
            )
            if not misma_direccion:
                continue

            exist_fila_ini, exist_fila_fin = self._rango_filas(existente)
            exist_col_ini, exist_col_fin = self._rango_columnas(existente)

            if nueva_es_h:
                # Ambos horizontales: misma fila?
                misma_fila = nuevo_fila_ini == exist_fila_ini
                if not misma_fila:
                    continue
                # Se solapan?
                se_solapan = self._rangos_se_solapan(
                    nuevo_col_ini, nuevo_col_fin, exist_col_ini, exist_col_fin
                )
                if se_solapan:
                    continue  # Superposicion es otra regla, no continuidad ilegal
                # Estan adyacentes? (distancia 1 entre fin de uno e inicio del otro)
                distancia = min(
                    abs(nuevo_col_ini - exist_col_fin),
                    abs(exist_col_ini - nuevo_col_fin)
                )
                if distancia == 1:
                    return True

            if nueva_es_v:
                # Ambos verticales: misma columna?
                misma_col = nuevo_col_ini == exist_col_ini
                if not misma_col:
                    continue
                # Se solapan?
                se_solapan = self._rangos_se_solapan(
                    nuevo_fila_ini, nuevo_fila_fin, exist_fila_ini, exist_fila_fin
                )
                if se_solapan:
                    continue
                # Estan adyacentes?
                distancia = min(
                    abs(nuevo_fila_ini - exist_fila_fin),
                    abs(exist_fila_ini - nuevo_fila_fin)
                )
                if distancia == 1:
                    return True

        return False

    # -- Regla 6: Subpalabras de 2 letras --

    def _hay_subpalabra_dos_letras(self, board: Board, placement_nuevo: Placement) -> bool:
        """
        Evita que se formen palabras fantasma de exactamente 2 letras
        en la direccion perpendicular a la palabra nueva.

        Para cada casilla que ocupara la palabra nueva, cuenta cuantas letras
        consecutivas hay en la direccion perpendicular (incluyendo la casilla).
        Si hay exactamente 2, es invalido porque forma una subpalabra fantasma.

        Ejemplo invalido:
            SAL vertical en col 2, filas 2-3: A(2,2), L(3,2)
            SOL horizontal en fila 3, cols 0-2: S(3,0), O(3,1), L(3,2)
            -> En (3,2), verticalmente hay solo A-L = 2 letras. Invalido.
        """
        es_h = placement_nuevo.direccion.es_horizontal()

        # Direccion perpendicular: si es horizontal, miramos verticalmente
        df, dc = (1, 0) if es_h else (0, 1)

        for f, c in placement_nuevo.posiciones():
            # La casilla (f,c) tendra letra despues de colocar la palabra nueva
            conteo = 1

            # Explorar hacia un lado en la direccion perpendicular
            ff, cc = f + df, c + dc
            while board.esta_dentro(ff, cc) and not board.esta_vacia(ff, cc):
                conteo += 1
                ff += df
                cc += dc

            # Explorar hacia el otro lado
            ff, cc = f - df, c - dc
            while board.esta_dentro(ff, cc) and not board.esta_vacia(ff, cc):
                conteo += 1
                ff -= df
                cc -= dc

            if conteo == 2:
                return True

        return False

    # -- Puntuacion de posiciones --

    def _puntuar_posicion(self, board: Board, placement: Placement) -> int:
        """
        Cuantas casillas de este placement cruzan con palabras ya puestas?
        Cada cruce (casilla ocupada con la MISMA letra) vale 1 punto.
        Mas puntos = mejor posicion (mas conectada al crucigrama existente).
        """
        puntuacion = 0
        for idx, (f, c) in enumerate(placement.posiciones()):
            if board.esta_ocupada(f, c) and board.celda(f, c) == placement.palabra[idx]:
                puntuacion += 1
        return puntuacion

    # -- Metodo principal de validacion --

    def es_posicion_valida(
        self,
        board: Board,
        palabra: str,
        fila: int,
        columna: int,
        direccion: Direction
    ) -> bool:
        """
        Puedo poner esta palabra aqui sin romper las reglas?

        Verifica:
        1. La palabra cabe dentro del tablero.
        2. Cada casilla esta vacia O ya tiene la MISMA letra.
        3. Si ya hay palabras, la nueva debe CRUZARSE con al menos una.
        4. NO hay paralelismo pegado con palabras existentes.
        5. NO hay continuidad ilegal con palabras existentes.
        6. NO se forman subpalabras fantasma de 2 letras.
        """
        palabra = palabra.upper()
        recorrido = list(direccion.recorrido(fila, columna, len(palabra)))

        # Regla 1: Cabe en el tablero?
        for f, c in recorrido:
            if not board.esta_dentro(f, c):
                return False

        # Regla 2: Letras compatibles?
        for idx, (f, c) in enumerate(recorrido):
            letra_existente = board.celda(f, c)
            if letra_existente is not None and letra_existente != palabra[idx]:
                return False

        # Regla 3: Toca alguna palabra existente?
        if len(board.placements) == 0:
            return True

        toca_alguna = False
        for f, c in recorrido:
            for existente in board.placements:
                if existente.letra_en(f, c) is not None:
                    toca_alguna = True
                    break
            if toca_alguna:
                break

        if not toca_alguna:
            return False

        # Regla 4: Paralelismo pegado?
        placement_candidato = Placement(palabra, fila=fila, columna=columna, direccion=direccion)
        if self._hay_paralelismo_pegado(board, placement_candidato):
            return False

        # Regla 5: Continuidad ilegal?
        if self._hay_continuidad_ilegal(board, placement_candidato):
            return False

        # Regla 6: Subpalabras de 2 letras?
        if self._hay_subpalabra_dos_letras(board, placement_candidato):
            return False

        return True

    def encontrar_posiciones_validas(
        self,
        board: Board,
        palabra: str
    ) -> list[Placement]:
        """
        Busca TODAS las posiciones donde esta palabra podria ir legalmente.
        """
        palabra = palabra.upper()
        posiciones = []

        for f in range(board.filas):
            for c in range(board.columnas):
                for direccion in (Horizontal(), Vertical()):
                    if self.es_posicion_valida(board, palabra, f, c, direccion):
                        posiciones.append(
                            Placement(palabra, fila=f, columna=c, direccion=direccion)
                        )

        # Ordenar por puntuacion: mas cruces primero
        posiciones.sort(key=lambda p: self._puntuar_posicion(board, p), reverse=True)
        return posiciones

    def colocar_primera_palabra(self, board: Board, palabra: str) -> None:
        """
        Coloca la primera palabra en el centro del tablero, horizontalmente.
        """
        palabra = palabra.upper()
        fila_centro = board.filas // 2
        columna_centro = (board.columnas - len(palabra)) // 2
        placement = Placement(
            palabra,
            fila=fila_centro,
            columna=columna_centro,
            direccion=Horizontal()
        )
        board.colocar(placement)

    def generar(self, board: Board, palabras: list[str]) -> bool:
        """
        Intenta colocar todas las palabras en el tablero usando backtracking.

        1. Ordena palabras de mas larga a mas corta.
        2. Coloca la primera en el centro.
        3. Para cada palabra restante, prueba posiciones validas.
        4. Si una rama falla, retrocede (backtrack) y prueba otra.
        5. Devuelve True si logro colocar todas, False si es imposible.
        """
        if not palabras:
            return False

        palabras = [p.upper() for p in palabras]
        palabras_ordenadas = sorted(palabras, key=len, reverse=True)

        # Limpiar tablero por si acaso
        board.limpiar()

        # Colocar la primera palabra en el centro
        primera = palabras_ordenadas[0]
        self.colocar_primera_palabra(board, primera)

        # Intentar colocar el resto recursivamente
        resto = palabras_ordenadas[1:]
        exito = self._backtrack(board, resto, 0)

        if not exito:
            # Si fallo, dejar el tablero limpio (no dejar palabras a medias)
            board.limpiar()

        return exito

    def _backtrack(self, board: Board, palabras: list[str], indice: int) -> bool:
        """
        Recursivamente intenta colocar palabras[indice] y las siguientes.
        """
        if indice >= len(palabras):
            return True  # Todas las palabras fueron colocadas

        palabra = palabras[indice]
        posiciones = self.encontrar_posiciones_validas(board, palabra)

        for pos in posiciones:
            board.colocar(pos)
            if self._backtrack(board, palabras, indice + 1):
                return True
            board.quitar(pos)  # Backtrack: deshacer esta eleccion

        return False  # Ninguna posicion funciono para esta palabra