"""
gac/renderer.py
===============
Renderiza un Board como HTML visual.

Principio: "El dominio sabe como se ve; el script solo lo ejecuta."
"""

from .board import Board
from .pistas import PistaNumerador


class HtmlRenderer:
    """
    Convierte un tablero de crucigrama en una pagina HTML visual.

    No tiene estado. Recibe un Board y devuelve un string HTML.
    """

    def render(
        self,
        board: Board,
        titulo: str = "Crucigrama GAC",
        numerador: PistaNumerador | None = None
    ) -> str:
        """
        Genera el HTML completo que representa el tablero.

        Si se proporciona un PistaNumerador, muestra los numeros de pista
        en la esquina superior izquierda de cada casilla inicial.

        Solo muestra la region que contiene palabras, con un margen
        de 1 celda alrededor para que no quede pegado al borde.
        """
        if not board.placements:
            return self._html_vacio(titulo)

        # Numeros de pista por celda (si hay numerador)
        numeros: dict[tuple[int, int], int] = {}
        if numerador is not None:
            numeros = numerador.numeros_por_celda(board)

        # Calcular los limites de las palabras colocadas
        min_fila = min(f for p in board.placements for f, c in p.posiciones())
        max_fila = max(f for p in board.placements for f, c in p.posiciones())
        min_col = min(c for p in board.placements for f, c in p.posiciones())
        max_col = max(c for p in board.placements for f, c in p.posiciones())

        # Margen de 1 celda
        min_fila = max(0, min_fila - 1)
        min_col = max(0, min_col - 1)
        max_fila = min(board.filas - 1, max_fila + 1)
        max_col = min(board.columnas - 1, max_col + 1)

        filas_vis = max_fila - min_fila + 1
        cols_vis = max_col - min_col + 1

        celdas_html = []
        for f in range(min_fila, max_fila + 1):
            for c in range(min_col, max_col + 1):
                letra = board.celda(f, c)
                numero = numeros.get((f, c))
                if letra:
                    if numero is not None:
                        celdas_html.append(
                            '    <div class="cell letter">'
                            '<span class="cell-number">' + str(numero) + '</span>'
                            + letra + '</div>'
                        )
                    else:
                        celdas_html.append(
                            '    <div class="cell letter">' + letra + '</div>'
                        )
                else:
                    celdas_html.append('    <div class="cell empty"></div>')

        celdas_str = "\n".join(celdas_html)

        return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>""" + titulo + """</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}
h1 {
    color: #fff;
    margin-bottom: 20px;
    font-size: 28px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
.board-container {
    background: #222;
    padding: 12px;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.board {
    display: grid;
    grid-template-columns: repeat(""" + str(cols_vis) + """, 44px);
    grid-template-rows: repeat(""" + str(filas_vis) + """, 44px);
    gap: 2px;
}
.cell {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 700;
    border-radius: 4px;
    user-select: none;
    position: relative;
}
.empty {
    background: #1a1a2e;
    border: 1px solid #16213e;
}
.letter {
    background: #fff;
    color: #1a1a2e;
    border: 1px solid #ddd;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.8);
}
.cell-number {
    position: absolute;
    top: 2px;
    left: 4px;
    font-size: 10px;
    font-weight: 400;
    color: #666;
    line-height: 1;
    pointer-events: none;
}
.info {
    color: rgba(255,255,255,0.7);
    margin-top: 16px;
    font-size: 14px;
}
</style>
</head>
<body>
<h1>""" + titulo + """</h1>
<div class="board-container">
<div class="board">
""" + celdas_str + """
</div>
</div>
<p class="info">Generado con GAC KIMI — """ + str(len(board.placements)) + """ palabras</p>
</body>
</html>"""

    def _html_vacio(self, titulo: str) -> str:
        return """<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>""" + titulo + """</title></head>
<body style="font-family:sans-serif;text-align:center;padding:50px;">
<h1>""" + titulo + """</h1>
<p>No hay palabras en el tablero.</p>
</body>
</html>"""