import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('// FILTRO MODO INVITADO')
end = text.find('if (equiposPermitidos === 0) {')

if start != -1 and end != -1:
    old_code = text[start:end]
    new_code = r"""// FILTRO MODO INVITADO
            if (isGuestMode) {
                let nowTime = new Date().getTime();
                let limitTime = nowTime + (10 * 24 * 60 * 60 * 1000); // 10 days
                let pasadosPorEquipo = {};
                let proximosFiltrados = [];
                
                data.equipos.forEach(eq => {
                    let esPasado = eq.oficial_sets && eq.oficial_sets.includes("-");
                    if (esPasado) {
                        if (!pasadosPorEquipo[eq.equipo_local]) { pasadosPorEquipo[eq.equipo_local] = eq; }
                        else {
                            let currentTs = pasadosPorEquipo[eq.equipo_local].timestamp || 0;
                            let newTs = eq.timestamp || 0;
                            if (newTs > currentTs) { pasadosPorEquipo[eq.equipo_local] = eq; }
                        }
                    } else {
                        if (eq.timestamp && eq.timestamp <= limitTime) { proximosFiltrados.push(eq); }
                    }
                });
                let pasadosFiltrados = Object.values(pasadosPorEquipo);
                data.equipos = proximosFiltrados.concat(pasadosFiltrados);
                data.equipos.sort((a, b) => { return (a.timestamp || Infinity) - (b.timestamp || Infinity); });
            }

            let htmlPartidos = "";
            let equiposPermitidos = 0;
            let equiposCerrados = 0;

            data.equipos.forEach(eq => {
                if (eq.visibilidad !== "OCULTAR") {
                    equiposPermitidos++;
                    if (eq.estado === "CERRADO") equiposCerrados++;

                    let valJornada = String(eq.jornada_eq || "").trim();
                    let infoJornadaEq = valJornada ? (isNaN(valJornada) ? ` <span style="font-size:0.9rem; color:#888;">(${valJornada})</span>` : ` <span style="font-size:0.9rem; color:#888;">(J${valJornada})</span>`) : "";
                    
                    let dt = new Date(eq.timestamp);
                    let fechaFormateada = isNaN(dt) ? "" : `${dt.toLocaleDateString()} ${dt.getHours().toString().padStart(2,'0')}:${dt.getMinutes().toString().padStart(2,'0')}`;
                    
                    let infoPabellon = eq.pabellon_localizacion ? `<div style="font-size: 0.8rem; color: var(--text-muted); margin-top:2px;"><i data-lucide="map-pin" style="width: 10px; height: 10px; display: inline; vertical-align: middle; margin-top:-2px;"></i> ${eq.pabellon_localizacion}</div>` : "";
                    
                    let localTeamName = (eq.ubicacion === 'LOCAL') ? eq.equipo_local : eq.rival;
                    let visitTeamName = (eq.ubicacion === 'LOCAL') ? eq.rival : eq.equipo_local;
                    
                    let localLogo = data.logos && data.logos[localTeamName] ? `<img src="${data.logos[localTeamName]}" style="width:100%; height:100%; object-fit:contain;">` : `<i data-lucide="shield" style="width:24px; height:24px; color:var(--text-muted);"></i>`;
                    let visitLogo = data.logos && data.logos[visitTeamName] ? `<img src="${data.logos[visitTeamName]}" style="width:100%; height:100%; object-fit:contain;">` : `<i data-lucide="shield" style="width:24px; height:24px; color:var(--text-muted);"></i>`;

                    let abrevLocalRaw = (eq.ubicacion === 'LOCAL') ? eq.abrev_local : eq.abrev_rival;
                    let abrevVisitRaw = (eq.ubicacion === 'LOCAL') ? eq.abrev_rival : eq.abrev_local;
                    let abrevLocal = abrevLocalRaw ? abrevLocalRaw.toUpperCase() : localTeamName.substring(0,3).toUpperCase();
                    let abrevVisit = abrevVisitRaw ? abrevVisitRaw.toUpperCase() : visitTeamName.substring(0,3).toUpperCase();
                    
                    let destacadoHtml = "";

                    let inputsHtml = "";
                    if (eq.estado === "ABIERTO" && !isGuestMode) {
                        inputsHtml = `
                            <!-- PUNTOS TEXT -->
                            <div style="font-size: 0.7rem; color: var(--text-muted); text-align: center; margin-bottom: 12px; font-weight: bold;">
                                Sets Exactos: <span style="color:var(--success);">+${data.reglas?.puntos_sets_exactos || 80} pts</span> | 
                                Diferencia: <span style="color:var(--success);">+${data.reglas?.puntos_diferencia_exacta || 100} pts</span>
                            </div>
                            
                            <!-- HIDDEN INPUTS -->
                            <input type="hidden" id="e${eq.id_partido}_sets" value="">
                            <input type="hidden" id="e${eq.id_partido}_puntos" value="14">
                            <input type="hidden" id="e${eq.id_partido}_signo" value="">

                            <div class="inputs-eq" id="inputs_eq_${eq.id_partido}">
                                <div class="sets-grid-label-v2">
                                  <span>Pronóstico de Sets</span>
                                  <span style="color: var(--secondary-color);" class="sets-points-label">...</span>
                                </div>
                                <div class="sets-selector-grid-v2">
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '3-0', '${eq.id_partido}')">3-0</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '3-1', '${eq.id_partido}')">3-1</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '3-2', '${eq.id_partido}')">3-2</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '0-3', '${eq.id_partido}')">0-3</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '1-3', '${eq.id_partido}')">1-3</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '2-3', '${eq.id_partido}')">2-3</button>
                                </div>

                                <div class="sets-grid-label-v2" style="margin-top: 15px;">
                                  <span>Diferencia de Puntos (Opcional)</span>
                                  <span style="color: var(--secondary-color);" class="diff-points-label" id="lbl-puntos-${eq.id_partido}">14 pts</span>
                                </div>
                                <div class="diff-slider-container-v2">
                                  <div class="diff-val-display-v2" id="val-display-${eq.id_partido}">14</div>
                                  <input type="range" class="vcv-slider" min="2" max="25" value="14" oninput="actualizarSliderV2(this.value, '${eq.id_partido}')">
                                  
                                  <div style="display:flex; justify-content:space-between; margin-top:12px; gap:8px;">
                                    <div class="slider-side-btn-container">
                                      <div class="slider-side-label">${abrevLocal}</div>
                                      <button type="button" class="slider-side-btn btn-left" id="btn-left-${eq.id_partido}" onclick="seleccionarSignoV2('left', '${eq.id_partido}')">
                                        A favor
                                      </button>
                                    </div>
                                    <div class="slider-side-btn-container">
                                      <div class="slider-side-label">${abrevVisit}</div>
                                      <button type="button" class="slider-side-btn btn-right" id="btn-right-${eq.id_partido}" onclick="seleccionarSignoV2('right', '${eq.id_partido}')">
                                        En contra
                                      </button>
                                    </div>
                                  </div>
                                </div>
                            </div>
                            
                            <div class="summary-v2" id="summary-v2-${eq.id_partido}" style="display:none; text-align:center; padding: 15px; background:var(--bg-card-alt); border: 1px solid var(--border-color); border-radius: 12px; margin-bottom: 12px;">
                                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px;">TU PREDICCIÓN</div>
                                <div id="summary-text-${eq.id_partido}" style="font-size: 1.1rem; font-weight: 800; color: var(--secondary-color);"></div>
                            </div>

                            <button type="button" id="btn-save-${eq.id_partido}" onclick="handleSaveOrModifyV2('${eq.id_partido}')" style="width:100%; margin-top:15px; padding:12px; border-radius:10px; background:var(--secondary-color); color:#000; font-weight:800; border:none; cursor:pointer; transition: all 0.2s;">
                                Guardar Predicción
                            </button>
                        `;
                    } else if (eq.estado === "CERRADO") {
                        let resultHtml = "";
                        if (eq.oficial_sets) {
                            resultHtml = `
                            <div style="text-align:center; margin-top:15px; padding:15px; background:var(--bg-card-alt); border-radius:12px; border:1px solid var(--border-color);">
                                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px;">RESULTADO OFICIAL</div>
                                <div style="font-size: 1.25rem; font-weight: 900; color: var(--text-main);">${eq.oficial_sets}</div>
                                <div style="font-size: 0.85rem; color: var(--text-muted);">${eq.oficial_parciales || ''}</div>
                            </div>
                            `;
                        } else {
                            resultHtml = `
                            <div style="text-align:center; margin-top:15px; padding:12px; background:var(--bg-input); border-radius:12px; border:1px dashed var(--border-color);">
                                <span style="font-size: 0.85rem; color: var(--text-muted); font-weight:bold;">El plazo para predecir este partido está cerrado.</span>
                            </div>
                            `;
                        }
                        inputsHtml = resultHtml;
                    }

                    htmlPartidos += `
                        <div class="vcv-card-v2" id="card-v2-${eq.id_partido}" data-category="${eq.categoria}">
                            <div class="match-header-strip-v2">
                                <div style="display:flex; align-items:center; gap:8px;">
                                    <span style="color: ${eq.es_derby ? 'var(--text-gold)' : 'var(--secondary-color)'}; font-weight: 800;">
                                      ${eq.categoria.toUpperCase()} ${eq.es_derby ? ' DERBY' : ''}
                                    </span>
                                    <div class="reloj-partido" data-ts="${eq.timestamp}" data-eq="${eq.id_partido}" style="font-size:0.65rem; font-weight:bold; padding:2px 6px; background:rgba(212, 175, 55, 0.1); color:var(--secondary-color); border: 1px solid var(--border-glow); border-radius:4px; display:inline-block;">Calculando tiempo...</div>
                                </div>
                                <div style="text-align: right;">
                                    <div><i data-lucide="calendar" style="width: 12px; height: 12px; display: inline; vertical-align: middle; margin-top:-2px;"></i> ${fechaFormateada}</div>
                                    ${infoPabellon}
                                </div>
                            </div>

                            <div class="teams-versus-container-v2">
                                <div class="team-box-v2">
                                  <div class="team-avatar-v2">${localLogo}</div>
                                  <span class="team-name-v2">${localTeamName}</span>
                                  <span class="team-role-v2" style="color: var(--success)">LOCAL</span>
                                </div>
                                <div class="vs-divider-v2" style="display:flex; flex-direction:column; align-items:center; gap:6px;">
                                  <div>VS</div>
                                  ${eq.oficial_sets && eq.oficial_sets.includes("-") ? `<div style="font-size:1.2rem; font-weight:900; color:var(--text-main); background:var(--bg-input); padding:4px 8px; border-radius:6px;">${eq.oficial_sets}</div>` : ''}
                                </div>
                                <div class="team-box-v2">
                                  <div class="team-avatar-v2">${visitLogo}</div>
                                  <span class="team-name-v2">${visitTeamName}</span>
                                  <span class="team-role-v2" style="color: var(--danger)">VISITANTE</span>
                                </div>
                            </div>
                            
                            ${inputsHtml}
                            ${destacadoHtml}
                        </div>`;
                }
            });
            """
    text = text.replace(old_code, new_code)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully replaced block")
else:
    print("Could not find start or end")
