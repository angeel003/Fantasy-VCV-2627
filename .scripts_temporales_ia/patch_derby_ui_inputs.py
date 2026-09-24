import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

old_block = """                            <div class="row inputs-eq" id="inputs_eq_${eq.id_partido}">
                                <div class="form-group col-md-4">
                                    <label>Sets</label>
                                    <select class="form-control" id="e${eq.id_partido}_sets" style="border-color: #ddd;">
                                        <option value="">Elige...</option>
                                        <option value="3-0">Victoria 3-0</option>
                                        <option value="3-1">Victoria 3-1</option>
                                        <option value="3-2">Victoria 3-2</option>
                                        <option value="2-3">Derrota 2-3</option>
                                        <option value="1-3">Derrota 1-3</option>
                                        <option value="0-3">Derrota 0-3</option>
                                    </select>
                                </div>
                                <div class="form-group col-md-4">
                                    <label>Puntos Dif. <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, 'Diferencia de puntos sumando TODOS los sets. (Mira el ejemplo arriba 👆)')">❓</span></label>
                                    <input type="number" class="form-control" id="e${eq.id_partido}_puntos" placeholder="Ej: 12" min="0" style="border-color: #ddd;">
                                </div>
                                <div class="form-group col-md-4">
                                    <label>Signo <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, 'Esa diferencia de puntos es a favor del VCV o en contra?')">❓</span></label>
                                    <select class="form-control" id="e${eq.id_partido}_signo" style="border-color: #ddd;">
                                        <option value="">Elige...</option>
                                        <option value="A favor">A favor (+)</option>
                                        <option value="En contra">En contra (-)</option>
                                    </select>
                                </div>
                            </div>"""

new_block = """                            <div class="row inputs-eq" id="inputs_eq_${eq.id_partido}">
                                <div class="form-group col-md-4">
                                    <label>Sets</label>
                                    <select class="form-control" id="e${eq.id_partido}_sets" style="border-color: #ddd;">
                                        <option value="">Elige...</option>
                                        <option value="3-0">${eq.es_derby ? "Gana " + eq.equipo_local + " 3-0" : "Victoria 3-0"}</option>
                                        <option value="3-1">${eq.es_derby ? "Gana " + eq.equipo_local + " 3-1" : "Victoria 3-1"}</option>
                                        <option value="3-2">${eq.es_derby ? "Gana " + eq.equipo_local + " 3-2" : "Victoria 3-2"}</option>
                                        <option value="2-3">${eq.es_derby ? "Gana " + eq.rival + " 3-2" : "Derrota 2-3"}</option>
                                        <option value="1-3">${eq.es_derby ? "Gana " + eq.rival + " 3-1" : "Derrota 1-3"}</option>
                                        <option value="0-3">${eq.es_derby ? "Gana " + eq.rival + " 3-0" : "Derrota 0-3"}</option>
                                    </select>
                                </div>
                                <div class="form-group col-md-4">
                                    <label>Puntos Dif. <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, 'Diferencia de puntos sumando TODOS los sets. (Mira el ejemplo arriba 👆)')">❓</span></label>
                                    <input type="number" class="form-control" id="e${eq.id_partido}_puntos" placeholder="Ej: 12" min="0" style="border-color: #ddd;">
                                </div>
                                <div class="form-group col-md-4">
                                    <label>Signo <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, 'Esa diferencia de puntos es a favor de quién?')">❓</span></label>
                                    <select class="form-control" id="e${eq.id_partido}_signo" style="border-color: #ddd;">
                                        <option value="">Elige...</option>
                                        <option value="A favor">${eq.es_derby ? "A favor de " + eq.equipo_local : "A favor (+)"}</option>
                                        <option value="En contra">${eq.es_derby ? "A favor de " + eq.rival : "En contra (-)"}</option>
                                    </select>
                                </div>
                            </div>"""

# Replace crlf to lf for safe replacement
html_lines = html.replace('\r\n', '\n')
if old_block in html_lines:
    html_new = html_lines.replace(old_block, new_block)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_new)
    print("Patched dev.html!")
else:
    print("Not found in html_lines!")

