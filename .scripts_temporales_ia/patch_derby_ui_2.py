import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# Enhance the sets labels for Derby matches
old_html = """                          <div class="form-group col-md-4">
                              <label>Sets Local</label>
                              <input type="number" id="e${eq.id_partido}_setsLocal" class="form-control" min="0" max="3" onchange="validarSets(this)" oninput="validarSets(this)">
                          </div>
                          <div class="form-group col-md-4">
                              <label>Sets Visitante</label>
                              <input type="number" id="e${eq.id_partido}_setsRival" class="form-control" min="0" max="3" onchange="validarSets(this)" oninput="validarSets(this)">
                          </div>"""

new_html = """                          <div class="form-group col-md-4">
                              <label>${eq.es_derby ? "Sets " + eq.equipo_local : "Sets Local"}</label>
                              <input type="number" id="e${eq.id_partido}_setsLocal" class="form-control" min="0" max="3" onchange="validarSets(this)" oninput="validarSets(this)">
                          </div>
                          <div class="form-group col-md-4">
                              <label>${eq.es_derby ? "Sets " + eq.rival : "Sets Visitante"}</label>
                              <input type="number" id="e${eq.id_partido}_setsRival" class="form-control" min="0" max="3" onchange="validarSets(this)" oninput="validarSets(this)">
                          </div>"""

html = html.replace(old_html, new_html)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print("Enhanced sets labels for Derby matches.")

