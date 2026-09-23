import os

# 1. Update script-dev/Código.js
with open('script-prod/Código.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Make sure resultadosMap reads column 4 (frase)
old_res = "if(resData[i][0]) { resultadosMap[resData[i][0].toString().trim()] = { sets: resData[i][1], parciales: resData[i][2] }; }"
new_res = "if(resData[i][0]) { resultadosMap[resData[i][0].toString().trim()] = { sets: resData[i][1], parciales: resData[i][2], frase: resData[i][3] ? resData[i][3].toString().trim() : '' }; }"
js_content = js_content.replace(old_res, new_res)

# Add vote_destacado action before action === "save"
vote_destacado_code = """    if (action === "vote_destacado") {
        var idPart = params.id_partido;
        var jugador = params.jugador;
        var sheetVotos = ss.getSheetByName("Votos_Destacado");
        if (!sheetVotos) {
            sheetVotos = ss.insertSheet("Votos_Destacado");
            sheetVotos.appendRow(["ID_Partido", "Usuario", "Voto", "Timestamp"]);
        }
        var dataVotos = sheetVotos.getDataRange().getValues();
        var userVoted = false;
        for (var i = dataVotos.length - 1; i >= 1; i--) {
            if (dataVotos[i][0] && dataVotos[i][0].toString().trim() == idPart && dataVotos[i][1] && dataVotos[i][1].toString().trim() == usuario) {
                sheetVotos.getRange(i + 1, 3).setValue(jugador);
                sheetVotos.getRange(i + 1, 4).setValue(new Date());
                userVoted = true;
                break;
            }
        }
        if (!userVoted) {
            sheetVotos.appendRow([idPart, usuario, jugador, new Date()]);
        }
        return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Voto registrado!"})).setMimeType(ContentService.MimeType.JSON);
    }
"""
js_content = js_content.replace('if (action === "save") {', vote_destacado_code + '\n    if (action === "save") {')

# Add reading Plantillas and Votos_Destacado inside action === "login"
plantillas_and_votos_logic = """
        // LECTURA DE PLANTILLAS PARA JUGADOR DESTACADO
        var plantillasMap = {};
        var sheetPlantillas = ss.getSheetByName("Plantillas");
        if (sheetPlantillas) {
            var dataPlant = sheetPlantillas.getDataRange().getValues();
            if (dataPlant.length > 0) {
                var eqHeadersPlant = dataPlant[0];
                for (var c = 1; c < eqHeadersPlant.length; c++) {
                    var teamName = eqHeadersPlant[c] ? eqHeadersPlant[c].toString().trim() : "";
                    if (!teamName || teamName === "0") continue;
                    plantillasMap[teamName] = [];
                    for (var r = 1; r < dataPlant.length; r++) {
                        var jugName = dataPlant[r][c] ? dataPlant[r][c].toString().trim() : "";
                        if (jugName && jugName !== "0") {
                            plantillasMap[teamName].push(jugName);
                        }
                    }
                }
            }
        }

        // LECTURA DE VOTOS PARA JUGADOR DESTACADO
        var votosMap = {};
        var sheetVotos = ss.getSheetByName("Votos_Destacado");
        if (sheetVotos) {
            var dataVotos = sheetVotos.getDataRange().getValues();
            for (var v = 1; v < dataVotos.length; v++) {
                var pId = dataVotos[v][0] ? dataVotos[v][0].toString().trim() : "";
                var pUsr = dataVotos[v][1] ? dataVotos[v][1].toString().trim() : "";
                var pVoto = dataVotos[v][2] ? dataVotos[v][2].toString().trim() : "";
                if (!pId || !pVoto) continue;
                if (!votosMap[pId]) votosMap[pId] = { total: 0, votos: {}, my_voto: null };
                votosMap[pId].total++;
                if (!votosMap[pId].votos[pVoto]) votosMap[pId].votos[pVoto] = 0;
                votosMap[pId].votos[pVoto]++;
                if (pUsr === usuario) votosMap[pId].my_voto = pVoto;
            }
        }

        // ASOCIAR PLANTILLA, VOTOS Y DECLARACIONES A CADA PARTIDO
        for (var c = 0; c < cartelera.length; c++) {
            var cp = cartelera[c];
            cp.plantilla = plantillasMap[cp.equipo_local] || [];
            cp.votos_data = votosMap[cp.id_partido] || { total: 0, votos: {}, my_voto: null };
            var oRes = resultadosMap[cp.id_partido];
            cp.frase_destacado = (oRes && oRes.frase) ? oRes.frase : "";
        }
"""

js_content = js_content.replace('var rondaAbierta = sheetAjustes.getRange("B2").getValue() || "1";', plantillas_and_votos_logic + '\n        var rondaAbierta = sheetAjustes.getRange("B2").getValue() || "1";')

# Support action === "login" or action === "get_data"
js_content = js_content.replace('if (action === "login") {', 'if (action === "login" || action === "get_data") {')

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("script-dev/Código.js updated cleanly.")


# 2. Update dev.html from index.html base
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Switch scriptURL to dev
html_content = html_content.replace(
    'const scriptURL = "https://script.google.com/macros/s/AKfycbyw9L6Te3q2ibdRBaaAwaiPpEPWLbsNdb8JA9yO272DBHgxaZA2l3TLkH9ofAXlQiWfAg/exec";',
    'const scriptURL = "https://script.google.com/macros/s/AKfycbzM7QuqH1yFRL9rSA7CAUHZX3cogU6AH3PAW36mQkWhMw2ZDnA3JhI-U2bC7TQyNOHz/exec";'
)

# Add CSS for Jugador Destacado
css_to_add = """
    /* ESTILOS DEL JUGADOR DESTACADO */
    .mvp-box { background: #fdfbf7; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-top: 15px; }
    .mvp-title { font-weight: bold; color: var(--vcv-dorado); font-size: 1.05rem; margin-bottom: 10px; text-shadow: 1px 1px 1px rgba(0,0,0,0.1); }
    .mvp-bar-bg { background: #e9ecef; border-radius: 4px; height: 22px; width: 100%; position: relative; overflow: hidden; margin-bottom: 6px; }
    .mvp-bar-fill { background: linear-gradient(90deg, var(--vcv-morado), #9b59b6); height: 100%; width: 0%; transition: width 0.5s ease; }
    .mvp-bar-text { position: absolute; top: 0; left: 8px; line-height: 22px; font-size: 0.8rem; color: #fff; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); z-index: 2; }
    .mvp-bar-pct { position: absolute; top: 0; right: 8px; line-height: 22px; font-size: 0.8rem; color: #333; font-weight: bold; z-index: 2; }
    .mvp-winner-box { background: linear-gradient(135deg, var(--vcv-morado), #5e2e60); color: white; border-radius: 8px; padding: 15px; margin-top: 15px; text-align: center; border: 2px solid var(--vcv-dorado); }
    .mvp-quote { font-style: italic; color: #f1c40f; margin-top: 8px; font-size: 0.95rem; }
    .mvp-quote::before { content: "«"; font-size: 1.2rem; }
    .mvp-quote::after { content: "»"; font-size: 1.2rem; }
"""
html_content = html_content.replace('/* ESTILO INTRANET */', css_to_add + '\n    /* ESTILO INTRANET */')

# Add votarDestacado JS function
js_votar_func = """
window.votarDestacado = function(e, idPart) {
    e.preventDefault();
    const btn = e.target;
    const sel = document.getElementById(`sel_destacado_${idPart}`);
    if(!sel || !sel.value) { alert("Selecciona un jugador primero."); return; }
    
    btn.disabled = true; btn.innerText = "Votando...";
    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'vote_destacado', usuario: currentUser, password: currentPassword, id_partido: idPart, jugador: sel.value }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(d => {
        if(d.status === "success") {
            mostrarToast("⭐ ¡Voto registrado!");
            document.getElementById('btnReload').click();
        } else { alert("Error: " + d.message); btn.disabled = false; btn.innerText = "Votar"; }
    })
    .catch(() => { alert("Error de conexión."); btn.disabled = false; btn.innerText = "Votar"; });
};
"""
html_content = html_content.replace('function formatFecha(ts) {', js_votar_func + '\nfunction formatFecha(ts) {')

# Add Jugador Destacado UI rendering logic
old_match_render = """                let htmlReloj = "";
                let puntosInfo = "";
                
                if (eq.estado === "ABIERTO" && eq.timestamp) {"""

new_match_render = """                let htmlReloj = "";
                let puntosInfo = "";
                
                // --- LOGICA JUGADOR DESTACADO ---
                let destacadoHtml = "";
                let ts1h = eq.timestamp ? eq.timestamp + (60 * 60 * 1000) : 0;
                let ts24h = eq.timestamp ? eq.timestamp + (24 * 60 * 60 * 1000) : 0;
                
                if (eq.timestamp && nowMs < ts1h) {
                    let d = new Date(ts1h);
                    let h1 = d.getHours().toString().padStart(2, '0'); let m1 = d.getMinutes().toString().padStart(2, '0');
                    destacadoHtml = `<div class="mvp-box"><div style="color:#666; font-size:0.9rem; text-align:center;">⏳ La votación del <b>Jugador Destacado</b> se abrirá a las ${h1}:${m1}</div></div>`;
                } else if (eq.timestamp && nowMs >= ts1h && nowMs < ts24h && eq.plantilla && eq.plantilla.length > 0) {
                    if (eq.votos_data && eq.votos_data.my_voto) {
                        let resultsArray = Object.keys(eq.votos_data.votos).map(j => { return { nombre: j, votos: eq.votos_data.votos[j] }; });
                        resultsArray.sort((a,b) => b.votos - a.votos);
                        let barras = resultsArray.map(res => {
                            let pct = Math.round((res.votos / eq.votos_data.total) * 100);
                            let highlight = (res.nombre === eq.votos_data.my_voto) ? 'box-shadow: 0 0 5px var(--vcv-dorado); border: 1px solid var(--vcv-dorado);' : '';
                            return `<div class="mvp-bar-bg" style="${highlight}"><div class="mvp-bar-fill" style="width: ${pct}%;"></div><div class="mvp-bar-text">${res.nombre} ${res.nombre === eq.votos_data.my_voto ? '(Tú)' : ''}</div><div class="mvp-bar-pct">${pct}%</div></div>`;
                        }).join("");
                        destacadoHtml = `<div class="mvp-box"><div class="mvp-title">📊 Resultados Jugador Destacado</div>${barras}</div>`;
                    } else {
                        let opciones = `<option value="">Selecciona un jugador...</option>` + eq.plantilla.map(j => `<option value="${j}">${j}</option>`).join("");
                        destacadoHtml = `<div class="mvp-box" style="border-color: var(--vcv-dorado); background: #fffdf5;"><div class="mvp-title">⭐ ¡Vota al Jugador Destacado!</div><div style="display:flex; gap:10px;"><select class="form-control" id="sel_destacado_${eq.id_partido}">${opciones}</select><button class="btn btn-primary" style="font-weight:bold; white-space:nowrap;" onclick="votarDestacado(event, '${eq.id_partido}')">Votar</button></div></div>`;
                    }
                } else if (eq.timestamp && nowMs >= ts24h && eq.votos_data && eq.votos_data.total > 0) {
                    let resultsArray = Object.keys(eq.votos_data.votos).map(j => { return { nombre: j, votos: eq.votos_data.votos[j] }; });
                    resultsArray.sort((a,b) => b.votos - a.votos);
                    let ganador = resultsArray[0];
                    let pct = Math.round((ganador.votos / eq.votos_data.total) * 100);
                    let fraseHtml = eq.frase_destacado ? `<div class="mvp-quote">${eq.frase_destacado}</div>` : "";
                    
                    let photoUrl = `files/jugadores/${ganador.nombre.replace(/ /g, '_')}.png`;
                    let photoHtml = `<img src="${photoUrl}" onerror="this.style.display='none'" style="width:60px; height:60px; border-radius:50%; border:2px solid var(--vcv-dorado); background:#fff; margin-bottom:10px; object-fit:cover;">`;
                    
                    destacadoHtml = `<div class="mvp-winner-box"><div style="font-size:0.85rem; color:#f8f9fa; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px;">⭐ Jugador Destacado ⭐</div>${photoHtml}<div style="font-size:1.3rem; font-weight:bold; color:var(--vcv-dorado);">${ganador.nombre}</div><div style="font-size:0.8rem; color:#eee; margin-top:2px;">Elegido con el ${pct}% de los votos</div>${fraseHtml}</div>`;
                }
                // --- FIN LOGICA JUGADOR DESTACADO ---

                if (eq.estado === "ABIERTO" && eq.timestamp) {"""

html_content = html_content.replace(old_match_render, new_match_render)

old_html_concat = """                    ${infoLocFecha}
                    ${infoPabellon}
                    ${infoAdicional}
                    ${htmlReloj}
                </div>`;"""

new_html_concat = """                    ${infoLocFecha}
                    ${infoPabellon}
                    ${infoAdicional}
                    ${htmlReloj}
                    ${destacadoHtml}
                </div>`;"""

html_content = html_content.replace(old_html_concat, new_html_concat)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("dev.html rebuilt cleanly with 1-request login and Destacado feature.")

