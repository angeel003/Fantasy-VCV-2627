import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# We need to change the generation of `inputsHtml`.
# In normal login loop:
#           data.equipos.forEach(eq => {
#               ...
#               let inputsHtml = "";
#               if (eq.timestamp && eq.estado === "ABIERTO") { ... }
#
# Let's find `let inputsHtml = "";` inside `dev.html` (the one inside login success).

old_inputs_html = """                  let inputsHtml = "";
                  if(eq.timestamp && eq.estado === "ABIERTO") {
                      inputsHtml = `
                      <div class="row inputs-eq" id="inputs_eq_${eq.id_partido}">
                          <div class="form-group col-md-4">
                              <label>Sets Local</label>
                              <input type="number" id="e${eq.id_partido}_setsLocal" class="form-control" min="0" max="3" onchange="validarSets(this)" oninput="validarSets(this)">
                          </div>
                          <div class="form-group col-md-4">
                              <label>Sets Visitante</label>
                              <input type="number" id="e${eq.id_partido}_setsRival" class="form-control" min="0" max="3" onchange="validarSets(this)" oninput="validarSets(this)">
                          </div>
                          <div class="form-group col-md-4">
                              <label>Puntos Dif.</label>
                              <div class="input-group">
                                  <input type="number" id="e${eq.id_partido}_puntos" class="form-control" min="0" placeholder="Ej: 12">
                                  <select id="e${eq.id_partido}_signo" class="form-control" style="font-size:0.85rem; padding:0 5px;">
                                      <option value="A favor">A favor</option>
                                      <option value="En contra">En contra</option>
                                  </select>
                              </div>
                          </div>
                      </div>
                      `;
                  }"""

new_inputs_html = """                  let inputsHtml = "";
                  if(eq.timestamp && eq.estado === "ABIERTO") {
                      let optionLocal = "A favor";
                      let optionVisit = "En contra";
                      if (eq.es_derby) {
                          optionLocal = eq.equipo_local;
                          optionVisit = eq.rival;
                      }
                      
                      inputsHtml = `
                      <div class="row inputs-eq" id="inputs_eq_${eq.id_partido}">
                          <div class="form-group col-md-4">
                              <label>Sets Local</label>
                              <input type="number" id="e${eq.id_partido}_setsLocal" class="form-control" min="0" max="3" onchange="validarSets(this)" oninput="validarSets(this)">
                          </div>
                          <div class="form-group col-md-4">
                              <label>Sets Visitante</label>
                              <input type="number" id="e${eq.id_partido}_setsRival" class="form-control" min="0" max="3" onchange="validarSets(this)" oninput="validarSets(this)">
                          </div>
                          <div class="form-group col-md-4">
                              <label>${eq.es_derby ? "Puntos Ventaja" : "Puntos Dif."}</label>
                              <div class="input-group">
                                  <input type="number" id="e${eq.id_partido}_puntos" class="form-control" min="0" placeholder="Ej: 12">
                                  <select id="e${eq.id_partido}_signo" class="form-control" style="font-size:0.85rem; padding:0 5px;">
                                      <option value="A favor">${eq.es_derby ? "Gana " + optionLocal : optionLocal}</option>
                                      <option value="En contra">${eq.es_derby ? "Gana " + optionVisit : optionVisit}</option>
                                  </select>
                              </div>
                          </div>
                      </div>
                      `;
                  }"""

html = html.replace(old_inputs_html, new_inputs_html)

# Also add the Derby warning badge!
old_title = '<h5 style="margin-bottom: 5px; color:var(--vcv-morado); font-weight:bold; padding-right: 90px;">🏐 ${eq.equipo_local} vs ${eq.rival}${infoJornadaEq}</h5>'
new_title = '<h5 style="margin-bottom: 5px; color:var(--vcv-morado); font-weight:bold; padding-right: 90px;">🏐 ${eq.equipo_local} vs ${eq.rival}${infoJornadaEq}</h5>\n' + \
            '                      ${eq.es_derby ? `<div style="margin-bottom:10px; background:#fff3cd; color:#856404; padding:5px 10px; border-radius:5px; font-weight:bold; font-size:0.85rem; border:1px solid #ffeeba;">⚔️ ¡DERBY LOCAL! Los puntos valen DOBLE en este partido.</div>` : ""}'

html = html.replace(old_title, new_title)

# The frontend code submits "A favor" or "En contra".
# The UI sets the text correctly, but wait, the `value` is still "A favor" and "En contra"!!!
# YES! `<option value="A favor">${...}</option>`
# So the frontend data collection doesn't need to change at all! The backend receives "A favor" (which logically means `equipo_local`) and "En contra" (which logically means `rival`).
# Since my script maps the Derby dropdown to `A favor` = `equipo_local`, it works perfectly!

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("Patched dev.html UI for Derby matches")

