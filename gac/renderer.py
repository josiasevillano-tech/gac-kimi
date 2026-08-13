"""
gac/renderer.py
===============
Renderiza un Board como HTML interactivo.

Principio: "El dominio sabe como se ve; el script solo lo ejecuta."
"""

from .board import Board
from .pistas import PistaNumerador


class HtmlRenderer:
    """Convierte un tablero en una pagina HTML interactiva."""

    def render(
        self, board, titulo="Crucigrama GAC",
        numerador=None, pistas=None, interactivo=True
    ):
        if not board.placements:
            return self._html_vacio(titulo)

        numeros = {}
        if numerador is not None:
            numeros = numerador.numeros_por_celda(board)

        min_fila = min(f for p in board.placements for f, c in p.posiciones())
        max_fila = max(f for p in board.placements for f, c in p.posiciones())
        min_col = min(c for p in board.placements for f, c in p.posiciones())
        max_col = max(c for p in board.placements for f, c in p.posiciones())

        min_fila = max(0, min_fila - 1)
        min_col = max(0, min_col - 1)
        max_fila = min(board.filas - 1, max_fila + 1)
        max_col = min(board.columnas - 1, max_col + 1)

        filas_vis = max_fila - min_fila + 1
        cols_vis = max_col - min_col + 1

        celdas_html = []
        soluciones_js = []
        for f in range(min_fila, max_fila + 1):
            for c in range(min_col, max_col + 1):
                letra = board.celda(f, c)
                numero = numeros.get((f, c))
                if letra:
                    num_attr = ' data-numero="' + str(numero) + '"' if numero else ''
                    if interactivo:
                        celdas_html.append(
                            '    <div class="cell letter">'
                            '<span class="cell-number">' + (str(numero) if numero else '') + '</span>'
                            '<input type="text" maxlength="1" '
                            'data-fila="' + str(f) + '" data-col="' + str(c) + '" '
                            'data-solucion="' + letra + '"' + num_attr + '>'
                            '</div>'
                        )
                        soluciones_js.append('"' + str(f) + '-' + str(c) + '":"' + letra + '"')
                    else:
                        if numero:
                            celdas_html.append(
                                '    <div class="cell letter">'
                                '<span class="cell-number">' + str(numero) + '</span>'
                                + letra + '</div>'
                            )
                        else:
                            celdas_html.append('    <div class="cell letter">' + letra + '</div>')
                else:
                    celdas_html.append('    <div class="cell empty"></div>')

        celdas_str = "\n".join(celdas_html)
        soluciones_str = "{" + ",".join(soluciones_js) + "}"

        # Construir mapa numero -> (fila, col) para el JS
        numero_a_celda = {}
        for p in board.placements:
            num = numeros.get((p.fila, p.columna))
            if num and num not in numero_a_celda:
                numero_a_celda[num] = (p.fila, p.columna)
        numero_map_js = "{" + ",".join(['"' + str(k) + '":["' + str(v[0]) + '","' + str(v[1]) + '"]' for k, v in numero_a_celda.items()]) + "}"

        pistas_html = ""
        if pistas:
            horizontales = []
            verticales = []
            for num, info in sorted(pistas.items()):
                linea = '<li class="pista-item" data-numero="' + str(num) + '" onclick="irAPalabra(' + str(num) + ')"><strong>' + str(num) + '.</strong> ' + info["definicion"] + '</li>'
                if info.get("direccion", "").lower() == "horizontal":
                    horizontales.append(linea)
                else:
                    verticales.append(linea)
            pistas_html = '<div class="pistas-panel">'
            if horizontales:
                pistas_html += '<div class="pistas-grupo"><h3>Horizontales</h3><ul>' + "".join(horizontales) + '</ul></div>'
            if verticales:
                pistas_html += '<div class="pistas-grupo"><h3>Verticales</h3><ul>' + "".join(verticales) + '</ul></div>'
            pistas_html += '</div>'

        controles_html = ""
        progreso_html = ""
        if interactivo:
            controles_html = '<div class="controles"><button id="btn-verificar">Verificar</button><button id="btn-pista">Mostrar pista</button><button id="btn-limpiar">Limpiar errores</button><button id="btn-reiniciar">Reiniciar</button></div>'
            progreso_html = '<div class="progreso-container"><div class="progreso-barra"><div id="progreso-fill"></div></div><span id="progreso-texto">0 / 0</span></div>'

        js_interactivo = ""
        if interactivo:
            js_interactivo = "<script>"
            js_interactivo += "const soluciones=" + soluciones_str + ";"
            js_interactivo += "const numeroACelda=" + numero_map_js + ";"
            js_interactivo += "const inputs=document.querySelectorAll('.cell.letter input');"
            js_interactivo += "const progresoFill=document.getElementById('progreso-fill');"
            js_interactivo += "const progresoTexto=document.getElementById('progreso-texto');"
            js_interactivo += "const total=Object.keys(soluciones).length;"
            js_interactivo += "let direccionActual='horizontal';"

            # Funcion para encontrar input por coordenadas
            js_interactivo += "function getInput(fila,col){for(const inp of inputs){if(parseInt(inp.dataset.fila)===fila&&parseInt(inp.dataset.col)===col)return inp;}return null;}"

            # Funcion para ir a una palabra por numero
            js_interactivo += "function irAPalabra(num){const coords=numeroACelda[num];if(!coords)return;const inp=getInput(parseInt(coords[0]),parseInt(coords[1]));if(inp){inp.focus();direccionActual=inp.closest('.pistas-panel')?'horizontal':'horizontal';}}"

            # Actualizar progreso
            js_interactivo += "function actualizar(){let c=0;inputs.forEach(i=>{const k=i.dataset.fila+'-'+i.dataset.col;if(i.value.toUpperCase()===soluciones[k])c++;});const pct=Math.round((c/total)*100);progresoFill.style.width=pct+'%';progresoTexto.textContent=c+' / '+total;}"

            # Navegacion con flechas basada en coordenadas
            js_interactivo += "inputs.forEach(inp=>{inp.addEventListener('keydown',function(e){const f=parseInt(this.dataset.fila);const c=parseInt(this.dataset.col);let next=null;if(e.key==='ArrowRight'){next=getInput(f,c+1);direccionActual='horizontal';}if(e.key==='ArrowLeft'){next=getInput(f,c-1);direccionActual='horizontal';}if(e.key==='ArrowDown'){next=getInput(f+1,c);direccionActual='vertical';}if(e.key==='ArrowUp'){next=getInput(f-1,c);direccionActual='vertical';}if(e.key==='Backspace'&&!this.value){let prev=null;if(direccionActual==='horizontal')prev=getInput(f,c-1);else prev=getInput(f-1,c);if(prev){prev.focus();e.preventDefault();}}if(next){next.focus();e.preventDefault();}});"

            # Input: mayusculas, sin auto-avance (el usuario navega manualmente)
            js_interactivo += "inp.addEventListener('input',function(){this.value=this.value.toUpperCase();this.classList.remove('correcto','incorrecto');actualizar();});});"

            # Botones
            js_interactivo += "document.getElementById('btn-verificar').addEventListener('click',function(){inputs.forEach(inp=>{const k=inp.dataset.fila+'-'+inp.dataset.col;const v=inp.value.toUpperCase();inp.classList.remove('correcto','incorrecto');if(v===soluciones[k])inp.classList.add('correcto');else if(v!=='')inp.classList.add('incorrecto');});actualizar();});"
            js_interactivo += "document.getElementById('btn-pista').addEventListener('click',function(){const vacias=Array.from(inputs).filter(i=>{const k=i.dataset.fila+'-'+i.dataset.col;return i.value.toUpperCase()!==soluciones[k];});if(vacias.length>0){const e=vacias[Math.floor(Math.random()*vacias.length)];const k=e.dataset.fila+'-'+e.dataset.col;e.value=soluciones[k];e.classList.remove('incorrecto');e.classList.add('correcto');actualizar();}});"
            js_interactivo += "document.getElementById('btn-limpiar').addEventListener('click',function(){inputs.forEach(inp=>{const k=inp.dataset.fila+'-'+inp.dataset.col;if(inp.value.toUpperCase()!==soluciones[k]){inp.value='';inp.classList.remove('incorrecto');}});actualizar();});"
            js_interactivo += "document.getElementById('btn-reiniciar').addEventListener('click',function(){inputs.forEach(inp=>{inp.value='';inp.classList.remove('correcto','incorrecto');});actualizar();});"
            js_interactivo += "actualizar();</script>"

        css = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
h1 { color: #fff; margin-bottom: 12px; font-size: 28px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
.main-container { display: flex; flex-wrap: wrap; gap: 24px; justify-content: center; align-items: flex-start; }
.board-container { background: #222; padding: 12px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }
.board { display: grid; gap: 2px; }
.cell { width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 700; border-radius: 4px; user-select: none; position: relative; }
.empty { background: #1a1a2e; border: 1px solid #16213e; }
.letter { background: #fff; color: #1a1a2e; border: 1px solid #ddd; box-shadow: inset 0 1px 0 rgba(255,255,255,0.8); }
.letter input { width: 100%; height: 100%; border: none; background: transparent; text-align: center; font-size: 22px; font-weight: 700; color: #1a1a2e; text-transform: uppercase; outline: none; padding: 0; margin: 0; cursor: text; }
.letter input.correcto { background: #c8e6c9; color: #2e7d32; }
.letter input.incorrecto { background: #ffcdd2; color: #c62828; }
.cell-number { position: absolute; top: 2px; left: 4px; font-size: 10px; font-weight: 400; color: #666; line-height: 1; pointer-events: none; z-index: 2; }
.controles { display: flex; gap: 10px; margin-bottom: 12px; flex-wrap: wrap; justify-content: center; }
.controles button { padding: 10px 18px; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: transform 0.1s, box-shadow 0.2s; }
.controles button:hover { transform: translateY(-2px); }
#btn-verificar { background: #4caf50; color: #fff; }
#btn-pista { background: #ff9800; color: #fff; }
#btn-limpiar { background: #f44336; color: #fff; }
#btn-reiniciar { background: #9e9e9e; color: #fff; }
.progreso-container { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; background: rgba(255,255,255,0.15); padding: 10px 16px; border-radius: 8px; width: 100%; max-width: 500px; }
.progreso-barra { flex: 1; height: 12px; background: rgba(255,255,255,0.3); border-radius: 6px; overflow: hidden; }
#progreso-fill { height: 100%; background: #4caf50; width: 0%; transition: width 0.3s ease; border-radius: 6px; }
#progreso-texto { color: #fff; font-weight: 600; font-size: 14px; min-width: 60px; text-align: right; }
.pistas-panel { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); max-width: 340px; min-width: 280px; max-height: 70vh; overflow-y: auto; }
.pistas-panel h3 { color: #1e3c72; margin-bottom: 10px; font-size: 18px; border-bottom: 2px solid #2a5298; padding-bottom: 4px; }
.pistas-grupo { margin-bottom: 16px; }
.pistas-grupo ul { list-style: none; padding: 0; }
.pista-item { padding: 6px 0; border-bottom: 1px solid #eee; color: #333; font-size: 14px; line-height: 1.4; cursor: pointer; transition: background 0.2s; }
.pista-item:hover { background: #e3f2fd; border-radius: 4px; padding-left: 6px; }
.pistas-grupo li:last-child { border-bottom: none; }
.info { color: rgba(255,255,255,0.7); margin-top: 16px; font-size: 14px; }
"""

        css += ".board { grid-template-columns: repeat(" + str(cols_vis) + ", 44px); grid-template-rows: repeat(" + str(filas_vis) + ", 44px); }"
        css += "@media (max-width: 768px) { .main-container { flex-direction: column; align-items: center; } .pistas-panel { max-width: 100%; width: 100%; } .board { grid-template-columns: repeat(" + str(cols_vis) + ", 36px); grid-template-rows: repeat(" + str(filas_vis) + ", 36px); } .cell { width: 36px; height: 36px; font-size: 18px; } .letter input { font-size: 18px; } }"

        html = "<!DOCTYPE html><html lang=\"es\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>" + titulo + "</title><style>" + css + "</style></head><body><h1>" + titulo + "</h1>" + progreso_html + controles_html + "<div class=\"main-container\"><div class=\"board-container\"><div class=\"board\">" + celdas_str + "</div></div>" + pistas_html + "</div><p class=\"info\">Generado con GAC KIMI - " + str(len(board.placements)) + " palabras</p>" + js_interactivo + "</body></html>"
        return html

    def _html_vacio(self, titulo):
        return "<!DOCTYPE html><html lang=\"es\"><head><meta charset=\"UTF-8\"><title>" + titulo + "</title></head><body style=\"font-family:sans-serif;text-align:center;padding:50px;\"><h1>" + titulo + "</h1><p>No hay palabras en el tablero.</p></body></html>"