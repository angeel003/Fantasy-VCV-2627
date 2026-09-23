with open('dev.html', 'r', encoding='utf-8') as f:
    content = f.read()

target_loop = """            let htmlPartidos = `<h4 style="color: var(--vcv-morado); margin-bottom: 20px;">Cartelera de Partidos</h4>`;
            let equiposPermitidos = 0;
            let equiposCerrados = 0;
            
            data.equipos.forEach(eq => {
                if (eq.permitido && eq.visibilidad === "MOSTRAR") {
                    equiposPermitidos++;
                    let valJornada = String(eq.jornada_eq || "").trim();
                    let infoJornadaEq = "";
                    if(valJornada) {
                        infoJornadaEq = isNaN(valJornada) ? ` <span style="font-size:0.9rem; color:#666; font-weight:normal;">(${valJornada})</span>` : ` <span style="font-size:0.9rem; color:#666; font-weight:normal;">(Jornada ${valJornada})</span>`;
                    }
                    
                    let iconoLoc = eq.ubicacion === "CASA" ? "🏠" : (eq.ubicacion === "FUERA" ? "✈️" : "");
                    let infoLocFecha = "";
                    if(iconoLoc || eq.timestamp) {
                        infoLocFecha = `<div style="font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;">${iconoLoc} ${formatFecha(eq.timestamp)}</div>`;
                    }
                    let infoPabellon = eq.pabellon ? `<div style="font-size:0.85rem; color:#777; margin-bottom:10px;">📍 ${eq.pabellon}</div>` : "<div style='margin-bottom:10px;'></div>";
                    
                    let categoryHtml = getCategoryHTML(eq.categoria);

                    if (eq.estado === "ABIERTO") {
                        htmlPartidos += `
                        <div class="p-3 mb-3 partido-activo card-match" style="background: var(--vcv-blanco); border-radius: 8px; border: 1px solid var(--vcv-dorado); border-left: 5px solid var(--vcv-dorado); box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            ${categoryHtml}
                            <h5 style="margin-bottom: 5px; color:var(--vcv-morado); font-weight:bold; padding-right: 90px;">🏐 ${eq.equipo_local} vs ${eq.rival}${infoJornadaEq}</h5>
                            ${infoLocFecha}
                            ${infoPabellon}
                            <div class="reloj-partido" data-ts="${eq.timestamp}" data-eq="${eq.id_partido}" style="font-size:0.85rem; font-weight:bold; padding:4px 8px; background:#fff3cd; color:#856404; border-radius:4px; display:inline-block; margin-bottom:15px;">Calculando tiempo...</div>
                            <div class="row inputs-eq" id="inputs_eq_${eq.id_partido}">
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
                                    <label>Puntos Dif. <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, 'Diferencia de puntos sumando TODOS los sets. (Mira el ejemplo arriba ❓)')">❓</span></label>
                                    <input type="number" class="form-control" id="e${eq.id_partido}_puntos" placeholder="Ej: 12" min="0" style="border-color: #ddd;">
                                </div>
                                <div class="form-group col-md-4">
                                    <label>Signo <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, '¿Esa diferencia de puntos es a favor del VCV o en contra?')">❓</span></label>
                                    <select class="form-control" id="e${eq.id_partido}_signo" style="border-color: #ddd;">
                                        <option value="">Elige...</option>
                                        <option value="A favor">A favor (+)</option>
                                        <option value="En contra">En contra (-)</option>
                                    </select>
                                </div>
                            </div>
                        </div>`;
                    } else if (eq.estado === "CERRADO") {
                        equiposCerrados++;
                        htmlPartidos += `
                        <div class="p-3 mb-3 card-match" style="background: var(--bg-general); border-radius: 8px; border: 1px solid #dee2e6; border-left: 5px solid #6c757d;">
                            ${categoryHtml}
                            <h5 style="margin-bottom: 5px; color: #495057; font-weight:bold; padding-right: 90px;">🔒 ${eq.equipo_local} vs ${eq.rival}${infoJornadaEq}</h5>
                            ${infoLocFecha}
                            ${infoPabellon}
                            <small style="color:#6c757d; font-weight:bold;">El plazo para predecir este partido está cerrado.</small>
                        </div>`;
                    }
                }
            });"""

replacement_loop = """            let htmlPartidos = `<h4 style="color: var(--vcv-morado); margin-bottom: 20px;">Cartelera de Partidos</h4>`;
            let equiposPermitidos = 0;
            let equiposCerrados = 0;
            let nowMs = new Date().getTime();
            
            data.equipos.forEach(eq => {
                if (eq.permitido && eq.visibilidad === "MOSTRAR") {
                    equiposPermitidos++;
                    let valJornada = String(eq.jornada_eq || "").trim();
                    let infoJornadaEq = "";
                    if(valJornada) {
                        infoJornadaEq = isNaN(valJornada) ? ` <span style="font-size:0.9rem; color:#666; font-weight:normal;">(${valJornada})</span>` : ` <span style="font-size:0.9rem; color:#666; font-weight:normal;">(Jornada ${valJornada})</span>`;
                    }
                    
                    let iconoLoc = eq.ubicacion === "CASA" ? "🏠" : (eq.ubicacion === "FUERA" ? "✈️" : "");
                    let infoLocFecha = "";
                    if(iconoLoc || eq.timestamp) {
                        infoLocFecha = `<div style="font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;">${iconoLoc} ${formatFecha(eq.timestamp)}</div>`;
                    }
                    let infoPabellon = eq.pabellon ? `<div style="font-size:0.85rem; color:#777; margin-bottom:10px;">📍 ${eq.pabellon}</div>` : "<div style='margin-bottom:10px;'></div>";
                    
                    let categoryHtml = getCategoryHTML(eq.categoria);

                    // --- LOGICA JUGADOR DESTACADO ---
                    let destacadoHtml = "";
                    let ts1h = eq.timestamp ? (eq.timestamp + (60 * 60 * 1000)) : 0;
                    let ts24h = eq.timestamp ? (eq.timestamp + (24 * 60 * 60 * 1000)) : 0;
                    
                    if (eq.timestamp && nowMs < ts1h) {
                        let d = new Date(ts1h);
                        let h1 = d.getHours().toString().padStart(2, '0'); let m1 = d.getMinutes().toString().padStart(2, '0');
                        destacadoHtml = `<div class="mvp-box"><div style="color:#666; font-size:0.9rem; text-align:center;">⏳ La votación del <b>Jugador Destacado</b> se abrirá a las ${h1}:${m1}</div></div>`;
                    } else if (eq.timestamp && nowMs >= ts1h && nowMs < ts24h) {
                        if (eq.plantilla && eq.plantilla.length > 0) {
                            if (eq.votos_data && eq.votos_data.my_voto) {
                                let resultsArray = Object.keys(eq.votos_data.votos).map(j => { return { nombre: j, votos: eq.votos_data.votos[j] }; });
                                resultsArray.sort((a,b) => b.votos - a.votos);
                                let totalVotos = eq.votos_data.total || 1;
                                let barras = resultsArray.map(res => {
                                    let pct = Math.round((res.votos / totalVotos) * 100);
                                    let highlight = (res.nombre === eq.votos_data.my_voto) ? 'box-shadow: 0 0 5px var(--vcv-dorado); border: 1px solid var(--vcv-dorado);' : '';
                                    return `<div class="mvp-bar-bg" style="${highlight}"><div class="mvp-bar-fill" style="width: ${pct}%;"></div><div class="mvp-bar-text">${res.nombre} ${res.nombre === eq.votos_data.my_voto ? '(Tú)' : ''}</div><div class="mvp-bar-pct">${pct}% (${res.votos})</div></div>`;
                                }).join("");
                                destacadoHtml = `<div class="mvp-box"><div class="mvp-title">📊 Resultados Jugador Destacado</div>${barras}</div>`;
                            } else {
                                let opciones = `<option value="">Selecciona un jugador...</option>` + eq.plantilla.map(j => `<option value="${j}">${j}</option>`).join("");
                                destacadoHtml = `<div class="mvp-box" style="border-color: var(--vcv-dorado); background: #fffdf5;"><div class="mvp-title">⭐ ¡Vota al Jugador Destacado!</div><div style="display:flex; gap:10px;"><select class="form-control" id="sel_destacado_${eq.id_partido}">${opciones}</select><button class="btn btn-primary" style="font-weight:bold; white-space:nowrap;" onclick="votarDestacado(event, '${eq.id_partido}')">Votar</button></div></div>`;
                            }
                        } else {
                            destacadoHtml = `<div class="mvp-box"><div style="color:#888; font-size:0.85rem; text-align:center;">Plantilla no disponible para votación.</div></div>`;
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

                    if (eq.estado === "ABIERTO") {
                        htmlPartidos += `
                        <div class="p-3 mb-3 partido-activo card-match" style="background: var(--vcv-blanco); border-radius: 8px; border: 1px solid var(--vcv-dorado); border-left: 5px solid var(--vcv-dorado); box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            ${categoryHtml}
                            <h5 style="margin-bottom: 5px; color:var(--vcv-morado); font-weight:bold; padding-right: 90px;">🏐 ${eq.equipo_local} vs ${eq.rival}${infoJornadaEq}</h5>
                            ${infoLocFecha}
                            ${infoPabellon}
                            <div class="reloj-partido" data-ts="${eq.timestamp}" data-eq="${eq.id_partido}" style="font-size:0.85rem; font-weight:bold; padding:4px 8px; background:#fff3cd; color:#856404; border-radius:4px; display:inline-block; margin-bottom:15px;">Calculando tiempo...</div>
                            <div class="row inputs-eq" id="inputs_eq_${eq.id_partido}">
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
                                    <label>Puntos Dif. <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, 'Diferencia de puntos sumando TODOS los sets. (Mira el ejemplo arriba ❓)')">❓</span></label>
                                    <input type="number" class="form-control" id="e${eq.id_partido}_puntos" placeholder="Ej: 12" min="0" style="border-color: #ddd;">
                                </div>
                                <div class="form-group col-md-4">
                                    <label>Signo <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, '¿Esa diferencia de puntos es a favor del VCV o en contra?')">❓</span></label>
                                    <select class="form-control" id="e${eq.id_partido}_signo" style="border-color: #ddd;">
                                        <option value="">Elige...</option>
                                        <option value="A favor">A favor (+)</option>
                                        <option value="En contra">En contra (-)</option>
                                    </select>
                                </div>
                            </div>
                            ${destacadoHtml}
                        </div>`;
                    } else if (eq.estado === "CERRADO") {
                        equiposCerrados++;
                        htmlPartidos += `
                        <div class="p-3 mb-3 card-match" style="background: var(--bg-general); border-radius: 8px; border: 1px solid #dee2e6; border-left: 5px solid #6c757d;">
                            ${categoryHtml}
                            <h5 style="margin-bottom: 5px; color: #495057; font-weight:bold; padding-right: 90px;">🔒 ${eq.equipo_local} vs ${eq.rival}${infoJornadaEq}</h5>
                            ${infoLocFecha}
                            ${infoPabellon}
                            <small style="color:#6c757d; font-weight:bold;">El plazo para predecir este partido está cerrado.</small>
                            ${destacadoHtml}
                        </div>`;
                    }
                }
            });"""

if target_loop in content:
    content = content.replace(target_loop, replacement_loop)
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Match cards patched with destacadoHtml successfully.")
else:
    print("Error: target_loop not found in dev.html")

