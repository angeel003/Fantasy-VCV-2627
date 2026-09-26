document.getElementById('btnLogin').addEventListener('click', function() {
    const usr = document.getElementById('loginUsuario').value.trim();
    const pwd = document.getElementById('loginPassword').value.trim();
    const msgBox = document.getElementById('loginMessage');
    const btn = this;

    if(!usr || !pwd) { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Rellena usuario y contraseña."; msgBox.style.display = "block"; return; }
    
    btn.disabled = true; 
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Accediendo...'; 
    msgBox.style.display = "none";

    fetchSeguro(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
    .then(res => res.json())
    .then(data => {
        if(data.status === "success") {
            
            currentUser = usr; currentPassword = pwd;
            
            let promoDiv2 = document.getElementById('guestPromoBanner');
            if (promoDiv2) promoDiv2.style.display = "none";
            currentJornadaGlobal = data.jornada;
            window.appData = data;
            if(window.initCalendar) window.initCalendar();
            
            if(data.reglas) {
                let listaReglas = document.getElementById('listaReglasPuntuacion');
                if(listaReglas) {
                    listaReglas.innerHTML = `
                        <li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.sets} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.ganador} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_exacta} pts</span> extra</li>
                        <li>Acertar la <b>Diferencia aproximada (5)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_5} pts</span> extra</li>
                    `;
                }
                
                // Update match cards dynamically
                                            }

            let displayNom = data.nombre_real && data.nombre_real !== usr ? `${data.nombre_real} <span style="font-size:0.85rem; color:#666; font-weight:normal; font-family:sans-serif;">(@${usr})</span>` : usr;
            
            
            // Populating new Header V2
            document.getElementById('h2-user-name').innerText = data.nombre_real || usr;
            document.getElementById('h2-user-handle').innerText = "@" + usr;
            
            let misInsignias = data.insignias[usr] || [];
            let insigniasHeaderHtml = "";
            let insigniasH2Html = "";
            let isAdmin = false;
            
            misInsignias.forEach(b => {
                if (b.type === 'admin') isAdmin = true;
                let cssColorClass = getBadgeCSS(b.type);
                insigniasHeaderHtml += `<img src="${URL_BADGE_GENERIC}" class="badge-header ${cssColorClass}" title="${b.text}" onclick="showMobileTooltip(event, '${b.text}')">`;
                
                // NO tooltips, NO onclick for the top header badges! Just visual.
                insigniasH2Html += `<img src="${URL_BADGE_GENERIC}" class="${cssColorClass}" style="width:14px; height:14px;">`;
            });
            
            document.getElementById('h2-user-badges').innerHTML = insigniasH2Html;
            
            // Render lucide icons in the newly injected HTML
            lucide.createIcons();
            
            if (isAdmin) {
                document.getElementById('adminPanelWrapper').style.display = "block";
                renderAdminPanel(data.equipos); 
                
                // POPULATE LIGAS
                var ligasContainer = document.getElementById('adminLigasCheckboxes');
                if (ligasContainer && data.todas_las_ligas) {
                    ligasContainer.innerHTML = '';
                    var allLigas = data.todas_las_ligas;
                    allLigas.forEach(function(liga) {
                        if (!liga) return; // Skip empty columns
                        var div = document.createElement('div');
                        div.innerHTML = '<label style="margin:0; cursor:pointer;"><input type="checkbox" value="' + liga + '" style="margin-right:5px;"> ' + liga + '</label>';
                        ligasContainer.appendChild(div);
                    });
                }
            } else {
                document.getElementById('adminPanelWrapper').style.display = "none";
            }

             document.getElementById('tituloPrincipalSeccion').style.display = 'block';

            data.equipos.sort((a, b) => {
                let tsA = a.timestamp || Infinity; 
                let tsB = b.timestamp || Infinity;
                return tsA - tsB; 
            });
            
            equiposTotalesInfo = data.equipos;

            let htmlPartidos = ``;
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
                    let streamIcon = eq.streaming ? ` <a href="${eq.streaming}" target="_blank" style="margin-left:8px; display:inline-block; vertical-align:middle;" title="Ver Streaming Oficial"><img src="files/images/play_icon.png" style="width:16px; height:16px; display:block;"></a>` : "";
                    let infoLocFecha = (iconoLoc || eq.timestamp) ? `<div style="font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;">${iconoLoc} ${formatFecha(eq.timestamp)}${streamIcon}</div>` : (streamIcon ? `<div style="margin-bottom:4px;">${streamIcon}</div>` : "");
                    let infoPabellon = eq.pabellon ? `<div style="font-size:0.85rem; color:#777; margin-bottom:10px;">📍 ${eq.pabellon}</div>` : "<div style='margin-bottom:10px;'></div>";
                    
                    let categoryHtml = getCategoryHTML(eq.categoria);

                    // --- LOGICA JUGADOR DESTACADO ---
                      let destacadoHtml = "";
                      // --- FIN LOGICA JUGADOR DESTACADO ---

                    if (eq.estado === "ABIERTO" || eq.estado === "CERRADO") {
                        let dt = new Date(eq.timestamp);
                        let fechaFormateada = isNaN(dt) ? "" : `${dt.toLocaleDateString()} ${dt.getHours().toString().padStart(2,'0')}:${dt.getMinutes().toString().padStart(2,'0')}`;

                        

                        let localTeamName = (eq.ubicacion === 'LOCAL') ? eq.equipo_local : eq.rival;
                        let visitTeamName = (eq.ubicacion === 'LOCAL') ? eq.rival : eq.equipo_local;
                        
                        let abrevLocalRaw = (eq.ubicacion === 'LOCAL') ? eq.abrev_local : eq.abrev_rival;
                        let abrevVisitRaw = (eq.ubicacion === 'LOCAL') ? eq.abrev_rival : eq.abrev_local;
                        
                        let localAbrev = (abrevLocalRaw || localTeamName.substring(0,3)).toUpperCase();
                        let visitAbrev = (abrevVisitRaw || visitTeamName.substring(0,3)).toUpperCase();

                        let localLogo = `<span style="font-weight:900; font-size: 1.2rem;">${localAbrev}</span>`;
                        let visitLogo = `<span style="font-weight:900; font-size: 1.2rem;">${visitAbrev}</span>`;
                        
                        let infoPabellon = eq.pabellon ? `<div style="margin-top:2px;"><i data-lucide="map-pin" style="width: 12px; height: 12px; display: inline; vertical-align: middle; margin-top:-2px;"></i> ${eq.pabellon}</div>` : '';

                        let btnStreaming = eq.streaming 
                            ? `<a href="${eq.streaming}" target="_blank" class="btn-streaming-v2 active" style="text-decoration:none;"><i data-lucide="play" style="width:14px;height:14px;"></i> Streaming</a>` 
                            : `<button class="btn-streaming-v2 disabled" disabled><i data-lucide="play-square" style="width:14px;height:14px;"></i> Sin enlace</button>`;

                        htmlPartidos += `
                        <div class="vcv-card-v2" id="card-v2-${eq.id_partido}" data-category="${eq.categoria}">
                            <div class="match-header-strip-v2">
                                <span style="color: ${eq.es_derby ? 'var(--text-gold)' : 'var(--secondary-color)'}; font-weight: 800;">
                                  ${eq.categoria.toUpperCase()} ${eq.es_derby ? '🏆 DERBY' : ''}
                                </span>
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
                                  ${btnStreaming}
                                </div>
                                <div class="team-box-v2">
                                  <div class="team-avatar-v2">${visitLogo}</div>
                                  <span class="team-name-v2">${visitTeamName}</span>
                                  <span class="team-role-v2" style="color: var(--text-muted)">VISITANTE</span>
                                </div>
                            </div>
                            
                            

                            ${eq.estado === "CERRADO" ? `<div style="text-align:center; margin-top:15px; padding:15px; background:var(--bg-card-alt); border-radius:12px; border:1px solid var(--border-color);"><div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px;">RESULTADO OFICIAL</div><div style="font-size: 1.25rem; font-weight: 900; color: var(--text-main);">${eq.oficial_sets || 'Sin resultado'}</div><div style="font-size: 0.85rem; color: var(--text-muted);">${eq.oficial_parciales || ''}</div></div>` : `
                            <!-- HIDDEN INPUTS -->
                            <input type="hidden" id="e${eq.id_partido}_sets" value="">
                            <input type="hidden" id="e${eq.id_partido}_puntos" value="14">
                            <input type="hidden" id="e${eq.id_partido}_signo" value="">

                            <div class="inputs-eq" id="inputs_eq_${eq.id_partido}">
                                <div class="sets-grid-label-v2">
                                  <span>Pronóstico de sets</span>
                                  
                                </div>
                                <div class="sets-selector-grid-v2">
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '3-0', '${eq.id_partido}')">3-0</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '3-1', '${eq.id_partido}')">3-1</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '3-2', '${eq.id_partido}')">3-2</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '2-3', '${eq.id_partido}')">2-3</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '1-3', '${eq.id_partido}')">1-3</button>
                                    <button type="button" class="set-option-btn-v2" onclick="seleccionarSetV2(this, '0-3', '${eq.id_partido}')">0-3</button>
                                </div>

                                <div class="points-diff-container-v2">
                                  <div class="points-header-v2">
                                    <span>DIFERENCIA DE PUNTOS</span>
                                    
                                  </div>
                                  <div class="points-controls-row-v2">
                                    <div class="stepper-container-v2">
                                      <button type="button" class="btn-step-v2" onclick="cambiarPuntosV2('${eq.id_partido}', -1)">-</button>
                                      <div class="stepper-value-v2">
                                        <span id="val-v2-${eq.id_partido}">14</span>
                                        <small>PTS</small>
                                      </div>
                                      <button type="button" class="btn-step-v2" onclick="cambiarPuntosV2('${eq.id_partido}', 1)">+</button>
                                    </div>
                                    <div class="sign-selector-v2">
                                      <button type="button" class="sign-btn-v2 sign-plus-v2" id="signo-plus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, true)">
                                        <span style="font-size:0.7rem;">${localTeamName}</span>
                                      </button>
                                      <button type="button" class="sign-btn-v2 sign-minus-v2" id="signo-minus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, false)">
                                        <span style="font-size:0.7rem;">${visitTeamName}</span>
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
                            </button>`}
                            
                            ${destacadoHtml}
                        </div>`;
                    }
                }
            });

            if (equiposPermitidos === 0) {
                htmlPartidos = `<div class="alert-box alert-warning" style="display:block;">No hay partidos pendientes de predecir o en curso en este momento.</div>`;
                document.getElementById('btnSubmit').style.display = "none";
            } else if (equiposPermitidos === equiposCerrados) { document.getElementById('btnSubmit').style.display = "none"; }
            
            document.getElementById('contenedorPartidos').innerHTML = htmlPartidos;
            iniciarRelojes();
            if(window.lucide) setTimeout(() => lucide.createIcons(), 50);

            let clasifHtml = "";
            if(data.ligas.length === 0) { 
                clasifHtml = `<div class="alert-box alert-warning" style="display:block;">No estás asignado a ninguna liga privada todavía.</div>`; 
            } else {
                data.ligas.forEach(liga => {
                    clasifHtml += `
                    <details style="background:var(--vcv-blanco); border:1px solid #ddd; border-radius:8px; margin-bottom:15px; box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                        <summary style="padding:15px; font-weight:bold; color:var(--vcv-morado); font-size:1.1rem; cursor:pointer; outline:none;">
                            🏆 Liga: ${liga}
                        </summary>
                        <div style="padding: 0 15px 15px 15px;">
                            <div class="table-responsive">
                                <table style="width:100%; border-collapse:collapse; border-radius:8px; overflow:hidden; margin-bottom:0;">
                                    <thead style="background:var(--vcv-morado); color:var(--vcv-blanco);">
                                        <tr>
                                            <th style="padding:12px; text-align:left;">Posición y Jugador</th>
                                            <th style="padding:12px; text-align:center;">Puntos</th>
                                        </tr>
                                    </thead>
                                    <tbody>`;
                    
                    let ranking = data.clasificaciones[liga] || [];
                    ranking.forEach((r, index) => {
                        let pos = index + 1;
                        let medalla = pos === 1 ? "🥇" : (pos === 2 ? "🥈" : (pos === 3 ? "🥉" : ""));
                        let clase = pos === 1 ? "medal-1" : (pos === 2 ? "medal-2" : (pos === 3 ? "medal-3" : ""));
                        
                        let uBadges = data.insignias[r.jugador] || [];
                        let badgesHtmlTable = "";
                        uBadges.forEach(b => {
                             let cssColorClass = getBadgeCSS(b.type);
                             badgesHtmlTable += `<img src="${URL_BADGE_GENERIC}" class="badge-icon ${cssColorClass}" title="${b.text}" onclick="showMobileTooltip(event, '${b.text}')">`;
                        });

                        let txtJugador = r.nombre_real !== r.jugador ? `${r.nombre_real} <span style="font-size:0.85rem; color:#666; font-weight:normal; font-family:sans-serif;">(@${r.jugador})</span>` : r.jugador;
                        
                        clasifHtml += `<tr class="${clase}"><td style="padding:14px; border-bottom:1px solid #ddd; line-height:1.4;"><strong>${pos}</strong> - ${txtJugador} ${badgesHtmlTable} ${medalla}</td><td style="padding:14px; border-bottom:1px solid #ddd; font-weight:bold; font-size:1.1rem; color:var(--vcv-dorado); text-align:center;">${r.puntos}</td></tr>`;
                    });
                    clasifHtml += `</tbody></table></div></div></details>`;
                });
            }
            document.getElementById('tablasClasificacionContainer').innerHTML = clasifHtml;

            if(data.equipos_totales && data.equipos_totales.length > 0) {
                
                
                let isClosed = new Date().getTime() >= new Date("2026-10-03T00:00:00").getTime();
                
                let htmlTot = `
                <div id="relojTotales" style="font-size:1.1rem; font-weight:bold; padding:10px; background:#e3f2fd; color:#1565c0; border-radius:8px; text-align:center; margin-bottom:20px;">
                    Calculando tiempo...
                </div>`;
                
                data.equipos_totales.forEach(eq => {
                    let ptsActuales = data.puntos_reales[eq] || 0;
                    let misPts = "";
                    let listaOtros = "";
                    let porrasEq = data.predicciones_totales[eq] || [];
                    
                    porrasEq.forEach(porra => {
                        if (porra.usuario === usr) misPts = porra.puntos;
                        listaOtros += `
                        <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #eee;">
                            <span>👤 ${porra.nombre}</span>
                            <span style="font-weight:bold; color:var(--vcv-morado);">${porra.puntos} pts</span>
                        </div>`;
                    });

                    if (listaOtros === "") { listaOtros = "<div style='color:#999; font-size:0.9rem; margin-top:10px;'>Nadie ha hecho su predicción todavía.</div>"; }

                    let miCajonHTML = "";
                    if (isClosed) {
                        let textoMiPrediccion = misPts !== "" ? `${misPts} pts` : "No participaste";
                        miCajonHTML = `
                        <div style="background:var(--vcv-blanco); padding:15px; border-radius:5px; border:1px solid #ddd; margin-bottom:15px;">
                            <label style="font-weight:bold; color:#333;">Tu predicción final:</label>
                            <div style="font-size:1.2rem; font-weight:bold; color:var(--vcv-morado);">${textoMiPrediccion}</div>
                        </div>`;
                    } else {
                        miCajonHTML = `
                        <div style="background:var(--vcv-blanco); padding:15px; border-radius:5px; border:1px solid #ddd; margin-bottom:15px;">
                            <label style="font-weight:bold; color:#333;">Tu predicción final:</label>
                            <div style="display:flex; gap:10px;">
                                <input type="number" id="pt_${eq}" class="form-control" placeholder="Ej: 45" value="${misPts}">
                            </div>
                        </div>`;
                    }

                    htmlTot += `
                    <div style="background:var(--bg-general); border-radius:8px; padding:20px; margin-bottom:20px; border-left:5px solid var(--vcv-dorado);">
                        <h4 style="color:var(--vcv-morado); margin-bottom:5px; font-weight:bold;">${eq}</h4>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                            <span style="background:#d4edda; color:#155724; padding:5px 10px; border-radius:5px; font-weight:bold; font-size:0.9rem;">Llevan: ${ptsActuales} puntos reales</span>
                        </div>
                        
                        ${miCajonHTML}

                        <details>
                            <summary style="font-weight:bold; color:var(--vcv-morado); cursor:pointer; outline:none;">👀 Ver predicciones de los demás</summary>
                            <div style="margin-top:10px; background:var(--vcv-blanco); padding:10px 15px; border-radius:5px; border:1px solid #eee;">
                                ${listaOtros}
                            </div>
                        </details>
                    </div>`;
                });
                
                htmlTot += `<div id="msgPrediccionesTotales" class="alert-box mt-3" style="padding:10px;"></div>`;
                
                if (!isClosed) {
                    htmlTot += `<button class="btn btn-success btn-block mt-3" id="btnSaveTotales" style="font-weight:bold; font-size:1.1rem; padding:10px;">💾 Guardar Predicciones</button>`;
                }

                document.getElementById('contenedorPrediccionesTotales').innerHTML = htmlTot;

                if (!isClosed) {
                    document.getElementById('btnSaveTotales').addEventListener('click', function(e) {
                        e.preventDefault();
                        let prediccionesTot = {};
                        data.equipos_totales.forEach(eq => {
                            let val = document.getElementById(`pt_${eq}`).value.trim();
                            if(val !== "") prediccionesTot[eq] = val;
                        });
                        
                        const btnT = this;
                        const msgT = document.getElementById('msgPrediccionesTotales');
                        
                        btnT.disabled = true; 
                        btnT.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Guardando...'; 
                        msgT.style.display = "none";

                        fetchSeguro(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'save_totales', usuario: currentUser, password: currentPassword, predicciones_totales: prediccionesTot }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
                        .then(res => res.json())
                        .then(d => {
                            msgT.style.display = "block";
                            if(d.status === "success") { msgT.className = "alert-box alert-success"; msgT.innerText = d.message; }
                            else { msgT.className = "alert-box alert-danger"; msgT.innerText = d.message; }
                        }).catch(() => { msgT.className = "alert-box alert-danger"; msgT.innerText = "Error de conexión."; msgT.style.display = "block"; })
                        .finally(() => { btnT.disabled = false; btnT.innerText = "💾 Guardar Predicciones"; });
                    });
                }
            }

            document.getElementById('loginSection').style.display = "none";
            document.getElementById('appSection').style.display = "block";
            
            document.getElementById('btnLogout').style.display = "block";
            iniciarRelojTotales();
        } else {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = data.message; msgBox.style.display = "block";
        }
    })
    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error: " + err.message + " | " + (err.stack || ""); msgBox.style.display = "block"; })
    .finally(() => { 
        btn.innerText = "Entrar"; 
        btn.disabled = false; 
    });
});

function iniciarRelojes() {
    if(intervalCountdown) clearInterval(intervalCountdown);
    intervalCountdown = setInterval(() => {
        const now = new Date().getTime();
        document.querySelectorAll('.reloj-partido').forEach(el => {
            const ts = parseInt(el.getAttribute('data-ts'));
            const eqId = el.getAttribute('data-eq');
            if(!ts) { el.style.display = 'none'; return; }
            
            const diff = ts - now;
            const limite = 15 * 60 * 1000; 

            const applyStyle = (bg, color, text) => {
                el.innerHTML = text;
                el.style.backgroundColor = bg;
                el.style.color = color;
                el.style.border = '1px solid ' + color;
                el.style.borderRadius = '8px';
                el.style.padding = '6px 12px';
                el.style.fontSize = '0.75rem';
                el.style.fontWeight = '800';
            };

            const darkBg = 'var(--bg-input)';
            const red = 'var(--danger)';
            const blue = '#3498db';
            const yellow = 'var(--secondary-color)';
            const green = 'var(--success)';
            const gray = 'var(--text-muted)';

            if (isGuestMode) {
                if (diff <= 0 && diff > -14400000) {
                    applyStyle('rgba(231,76,60,0.1)', red, " Partido en curso");
                } else if (diff <= -14400000) {
                    const inputs = document.getElementById('inputs_eq_' + eqId);
                    if(inputs) {
                        if(!inputs.querySelector('span') || inputs.querySelector('span').innerText !== 'El plazo para predecir este partido está cerrado.') { inputs.innerHTML = '<div style="text-align:center; margin-top:15px; padding:12px; background:var(--bg-input); border-radius:12px; border:1px dashed var(--border-color);"><span style="font-size: 0.85rem; color: var(--text-muted); font-weight:bold;">El plazo para predecir este partido está cerrado.</span></div>'; }
                    }
                    const btnSave = document.getElementById('btn-save-' + eqId);
                    if (btnSave) btnSave.style.display = 'none';
                    applyStyle('rgba(255,255,255,0.05)', gray, " Partido Finalizado");
                } else {
                    let d = Math.floor(diff / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diff % (1000 * 60)) / 1000);
                    applyStyle('rgba(52,152,219,0.1)', blue, ` Empieza en: ${d}d ${h}h ${m}m ${s}s`);
                }
            } else {
                if (diff <= limite && diff > -14400000) {
                    const inputs = document.getElementById('inputs_eq_' + eqId);
                    if(inputs) {
                        if(!inputs.querySelector('span') || inputs.querySelector('span').innerText !== 'El plazo para predecir este partido está cerrado.') { inputs.innerHTML = '<div style="text-align:center; margin-top:15px; padding:12px; background:var(--bg-input); border-radius:12px; border:1px dashed var(--border-color);"><span style="font-size: 0.85rem; color: var(--text-muted); font-weight:bold;">El plazo para predecir este partido está cerrado.</span></div>'; }
                    }
                    const btnSave = document.getElementById('btn-save-' + eqId);
                    if (btnSave) btnSave.style.display = 'none';
                    applyStyle('rgba(231,76,60,0.1)', red, " PREDICCIONES CERRADAS");
                } else if (diff <= -14400000) {
                    const inputs = document.getElementById('inputs_eq_' + eqId);
                    if(inputs) {
                        if(!inputs.querySelector('span') || inputs.querySelector('span').innerText !== 'El plazo para predecir este partido está cerrado.') { inputs.innerHTML = '<div style="text-align:center; margin-top:15px; padding:12px; background:var(--bg-input); border-radius:12px; border:1px dashed var(--border-color);"><span style="font-size: 0.85rem; color: var(--text-muted); font-weight:bold;">El plazo para predecir este partido está cerrado.</span></div>'; }
                    }
                    const btnSave = document.getElementById('btn-save-' + eqId);
                    if (btnSave) btnSave.style.display = 'none';
                    applyStyle('rgba(255,255,255,0.05)', gray, " Partido Finalizado");
                } else {
                    let diffLimit = diff - limite;
                    let d = Math.floor(diffLimit / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diffLimit % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diffLimit % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diffLimit % (1000 * 60)) / 1000);
                    if (d > 0) {
                        applyStyle('rgba(212,175,55,0.1)', yellow, ` Se cierra en: ${d}d ${h}h`);
                    } else if (h > 0) {
                        applyStyle('rgba(212,175,55,0.1)', yellow, ` Se cierra en: ${h}h ${m}m`);
                    } else if (m > 0) {
                        applyStyle('rgba(231,76,60,0.1)', red, ` Se cierra en: ${m}m ${s}s`);
                    } else {
                        applyStyle('rgba(231,76,60,0.1)', red, ` Se cierra en: ${s}s`);
                    }
                }
            }
        });
    }, 1000);
}

function iniciarRelojTotales() {
    if(intervalTotalesCountdown) clearInterval(intervalTotalesCountdown);
    const deadline = new Date("2026-10-03T00:00:00").getTime();
    intervalTotalesCountdown = setInterval(() => {
        const el = document.getElementById('relojTotales');
        if(!el) return;
        const now = new Date().getTime();
        const diff = deadline - now;
        if(diff <= 0) {
            el.innerHTML = "🔒 PLAZO CERRADO. Las predicciones son definitivas.";
            el.style.color = "var(--vcv-rojo)";
            el.style.backgroundColor = "#fde8e8";
        } else {
            let d = Math.floor(diff / (1000 * 60 * 60 * 24));
            let h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            let s = Math.floor((diff % (1000 * 60)) / 1000);
            el.innerHTML = `⏳ El plazo de predicciones finales cierra en: ${d}d ${h}h ${m}m ${s}s`;
        }
    }, 1000);
}

function cargarDatosAntiguos() {
    fetchSeguro(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'load', usuario: currentUser, password: currentPassword }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
    .then(res => res.json())
    .then(data => {
        if(data.status === "success") {
            const setVal = (id, val) => { const el = document.getElementById(id); if (el && val != null && val !== "") el.value = String(val).trim(); };
            var preds = data.data.predicciones;
            for(var idPart in preds) {
                setVal(`e${idPart}_sets`, preds[idPart].sets);
                setVal(`e${idPart}_puntos`, preds[idPart].puntos);
                setVal(`e${idPart}_signo`, preds[idPart].signo);
                
                // --- V2 UI Sync ---
                let isFilled = false;
                if (preds[idPart].sets) {
                    const btn = document.querySelector(`button[onclick*="seleccionarSetV2(this, '${preds[idPart].sets}', '${idPart}')"]`);
                    if (btn) btn.classList.add('selected');
                    isFilled = true;
                }
                if (preds[idPart].puntos !== undefined) {
                    const span = document.getElementById(`val-v2-${idPart}`);
                    if (span) span.innerText = preds[idPart].puntos;
                    // If it's 0, we can also force the tied state just in case
                    if (parseInt(preds[idPart].puntos) === 0) {
                        const btnPlus = document.getElementById(`signo-plus-v2-${idPart}`);
                        const btnMinus = document.getElementById(`signo-minus-v2-${idPart}`);
                        if(btnPlus) { btnPlus.classList.add('tied-btn'); btnPlus.disabled = true; }
                        if(btnMinus) { btnMinus.classList.add('tied-btn'); btnMinus.disabled = true; }
                    }
                }
                if (preds[idPart].signo) {
                    const signoVal = preds[idPart].signo;
                    if (signoVal === "A favor") {
                        const btn = document.getElementById(`signo-plus-v2-${idPart}`);
                        if (btn) btn.classList.add('selected');
                    } else if (signoVal === "En contra") {
                        const btn = document.getElementById(`signo-minus-v2-${idPart}`);
                        if (btn) btn.classList.add('selected');
                    } else if (signoVal === "Empate") {
                        const btnPlus = document.getElementById(`signo-plus-v2-${idPart}`);
                        const btnMinus = document.getElementById(`signo-minus-v2-${idPart}`);
                        if(btnPlus) { btnPlus.classList.add('tied-btn'); btnPlus.disabled = true; }
                        if(btnMinus) { btnMinus.classList.add('tied-btn'); btnMinus.disabled = true; }
                    }
                }
                
                if (isFilled) {
                    const card = document.getElementById('card-v2-' + idPart);
                    const btn = document.getElementById('btn-save-' + idPart);
                    const summary = document.getElementById('summary-v2-' + idPart);
                    const inputs = document.getElementById('inputs_eq_' + idPart);
                    if(card && btn && summary && inputs) {
                        const s = preds[idPart].sets;
                        const p = preds[idPart].puntos;
                        const sig = preds[idPart].signo;
                        
                    const selectedSignBtn = document.querySelector(`#signo-plus-v2-${idPart}.selected`) || document.querySelector(`#signo-minus-v2-${idPart}.selected`);
                    let signText = selectedSignBtn ? selectedSignBtn.innerText : (sig === 'Empate' ? 'Empate' : sig);
                    if(p == 0) signText = "Empate";
                    document.getElementById('summary-text-' + idPart).innerText = `${s} | ${p} pts | ${signText}`;

                        card.classList.add('collapsed');
                        inputs.style.display = 'none';
                        summary.style.display = 'block';
                        btn.innerText = 'Modificar Predicción';
                        btn.style.background = 'transparent';
                        btn.style.color = 'var(--text-muted)';
                        btn.style.border = '1px solid var(--border-color)';
                    }
                }
            }
        }
    });
}

document.getElementById('prediccionForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const btnSubmit = document.getElementById('btnSubmit'); 
    const msgBox = document.getElementById('appMessage');
    msgBox.style.display = "none";

    const getVal = (id) => { const el = document.getElementById(id); return el ? el.value.trim() : ""; };
    let prediccionesList = {};
    let validacionFallida = false;

    equiposTotalesInfo.forEach(eq => {
        const elSet = document.getElementById(`e${eq.id_partido}_sets`);
        if(elSet && !elSet.disabled) {
            let vSet = getVal(`e${eq.id_partido}_sets`);
            let vPuntos = getVal(`e${eq.id_partido}_puntos`);
            let vSigno = getVal(`e${eq.id_partido}_signo`);

            let numRellenos = (vSet !== "" ? 1 : 0) + (vPuntos !== "" ? 1 : 0) + (vSigno !== "" ? 1 : 0);
            if (numRellenos > 0 && numRellenos < 3) {
                validacionFallida = true;
            }

            prediccionesList[eq.id_partido] = { sets: vSet, puntos: vPuntos, signo: vSigno };
        }
    });

    if (validacionFallida) {
        msgBox.className = "alert-box alert-danger"; 
        msgBox.innerText = "❌ Si predices un partido, debes rellenar sus 3 campos (Sets, Puntos y Signo). Puedes dejar partidos enteros en blanco si no quieres jugarlos hoy."; 
        msgBox.style.display = "block";
        return; 
    }

    btnSubmit.disabled = true; 
    btnSubmit.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Guardando...'; 

    fetchSeguro(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'save', usuario: currentUser, password: currentPassword, jornada: currentJornadaGlobal, predicciones: prediccionesList }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
    .then(res => res.json())
    .then(data => {
        msgBox.style.display = "block";
        if (data.status === "success") { msgBox.className = "alert-box alert-success"; msgBox.innerText = "✅ " + data.message; } 
        else { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "❌ " + data.message; }
    })
    .catch(() => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error: " + err.message + " | " + (err.stack || ""); msgBox.style.display = "block"; })
    .finally(() => { btnSubmit.disabled = false; btnSubmit.innerText = "💾 Guardar Mis Predicciones"; });
});

document.getElementById('btnToggleSort').addEventListener('click', function(e) {
    e.preventDefault();
    isSortDesc = !isSortDesc;
    this.innerText = isSortDesc ? "⬇️ Orden Descendente (Nuevos primero)" : "⬆️ Orden Ascendente (Viejos primero)";
    renderizarHistorial();
});

document.getElementById('btnHistory').addEventListener('click', function(e) {
    e.preventDefault();
    const msgBox = document.getElementById('historyMessage');
    const container = document.getElementById('historyListContainer');
    const controls = document.getElementById('historyControls');
    const btnHist = this;

    btnHist.disabled = true; 
    btnHist.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Cargando historial...'; 
    msgBox.style.display = "none";

    fetchSeguro(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'get_history', usuario: currentUser, password: currentPassword }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
    .then(res => res.json())
    .then(data => {
        if(data.status === "success") {
            if (data.history.length === 0) {
                msgBox.style.display = "block"; msgBox.className = "alert-box alert-warning"; msgBox.innerText = "Aún no tienes predicciones ni resultados."; container.style.display = "none"; controls.style.display = "none";
            } else {
                globalHistorialData = data.history;
                
                let equiposEnHistorial = new Set();
                globalHistorialData.forEach(r => {
                    r.partidos.forEach(p => { equiposEnHistorial.add(p.equipo_local); });
                });
                
                let equiposArray = Array.from(equiposEnHistorial).sort();
                let checksHtml = "";
                equiposArray.forEach(eq => {
                    checksHtml += `<label class="filter-checkbox"><input type="checkbox" class="chk-equipo" value="${eq}" checked> ${eq}</label>`;
                });
                document.getElementById('filterEquiposContainer').innerHTML = checksHtml;

                document.querySelectorAll('.chk-equipo').forEach(chk => {
                    chk.addEventListener('change', renderizarHistorial);
                });

                controls.style.display = "block"; 
                renderizarHistorial(); 
            }
        }
    })
    .finally(() => { 
        btnHist.innerText = "🔒 Cargar mi historial"; 
        btnHist.disabled = false; 
    });
});

function renderizarHistorial() {
    const container = document.getElementById('historyListContainer');
    let sortedHistory = JSON.parse(JSON.stringify(globalHistorialData));
    
    sortedHistory.sort((a, b) => {
        let numA = parseInt(a.ronda.replace(/\D/g, '')) || 0;
        let numB = parseInt(b.ronda.replace(/\D/g, '')) || 0;
        return isSortDesc ? numB - numA : numA - numB;
    });

    let checkedEquipos = Array.from(document.querySelectorAll('.chk-equipo:checked')).map(cb => cb.value);

    let histHtml = "";
    
    sortedHistory.forEach(ronda => {
        ronda.partidos.sort((a, b) => {
            let tA = a.timestamp || 0;
            let tB = b.timestamp || 0;
            return isSortDesc ? tB - tA : tA - tB;
        });

        let esActual = (ronda.ronda == currentJornadaGlobal);
        let blockHtml = `<div style="background:var(--vcv-blanco); border-radius:10px; padding:20px; margin-bottom:20px; box-shadow:0 4px 8px rgba(0,0,0,0.05); border:1px solid #e0e0e0; border-left: 5px solid var(--vcv-dorado);">`;
        blockHtml += `<h4 style="color:var(--vcv-morado); border-bottom:2px solid var(--bg-general); padding-bottom:10px; margin-top:0; font-weight:bold;">Ronda ${ronda.ronda}</h4>`;
        
        let hayDatosEnEsteBloque = false;
        
        ronda.partidos.forEach(p => {
            if (!checkedEquipos.includes(p.equipo_local)) return; 
            
            hayDatosEnEsteBloque = true;
            let eqName = p.equipo_local;
            let rivalName = p.rival;
            
            let ofText = `<i style="color:#999;">Pendiente de disputarse</i>`;
            if (p.oficial_sets && p.oficial_sets.includes("-")) {
                let sL = parseInt(p.oficial_sets.split("-")[0]);
                let sV = parseInt(p.oficial_sets.split("-")[1]);
                let textoRes = sL > sV ? `<span style="color:#28a745; font-weight:bold; margin-left:5px;">🟢 Ganado</span>` : `<span style="color:var(--vcv-rojo); font-weight:bold; margin-left:5px;">🔴 Perdido</span>`;
                ofText = `<b style="color:var(--vcv-negro); font-size:1.05rem;">${p.oficial_sets}</b> ${textoRes} <br><span style="font-size:0.85rem;">(${p.oficial_parciales})</span>`;
            }
            
            let valJornada = String(p.jornada_eq || "").trim();
            let infoJornadaEq = "";
            if(valJornada) {
                infoJornadaEq = isNaN(valJornada) ? ` <span style="font-size:0.85rem; color:#666; font-weight:normal;">(${valJornada})</span>` : ` <span style="font-size:0.85rem; color:#666; font-weight:normal;">(Jornada ${valJornada})</span>`;
            }

            let streamIconHist = p.streaming ? ` <a href="${p.streaming}" target="_blank" style="margin-left:8px; display:inline-block; vertical-align:middle;" title="Ver Streaming Oficial"><img src="files/images/play_icon.png" style="width:16px; height:16px; display:block;"></a>` : "";
            let infoLocFecha = streamIconHist ? `<span style="margin-left:10px;">${streamIconHist}</span>` : "";
            let htmlReloj = "";
            let iconoLoc = p.ubicacion === "CASA" ? "🏠" : (p.ubicacion === "FUERA" ? "✈️" : "");
            
            if (esActual) {
                if(iconoLoc || p.timestamp) {
                    infoLocFecha = `<span style="font-weight:normal; font-size:0.85rem; color:#666; margin-left:10px;">${iconoLoc} ${formatFecha(p.timestamp)}${streamIconHist}</span>`;
                }
                if(p.timestamp && p.estado === "ABIERTO") {
                    htmlReloj = `<div class="reloj-partido" data-ts="${p.timestamp}" style="margin-top:8px; font-size:0.85rem; font-weight:bold; padding:4px 8px; background:#fff3cd; color:#856404; border-radius:4px; display:inline-block;">Calculando tiempo...</div>`;
                }
            }
            
            let puntosInfo = "";
            if (p.oficial_sets && p.oficial_parciales) {
                let pts = p.puntos_partido !== undefined ? p.puntos_partido : "?";
                let mot = p.motivos || "Cálculo pendiente";
                let bgColor = pts > 0 ? "#e8f5e9" : "#fde8e8";
                let textColor = pts > 0 ? "#2e7d32" : "var(--vcv-rojo)";
                if (mot === "No pronosticado") { bgColor = "#eeeeee"; textColor = "#666666"; }
                
                puntosInfo = `
                <div style="margin-top:10px; background:${bgColor}; border-radius:6px; padding:10px; text-align:center;">
                    <div style="color:${textColor}; font-weight:bold; font-size:1.1rem;">+${pts} Puntos</div>
                    <div style="color:#666; font-size:0.85rem; margin-top:2px;">${mot}</div>
                </div>`;
            } else {
                puntosInfo = `
                <div style="margin-top:10px; background:#fff8e1; border-radius:6px; padding:10px; text-align:center;">
                    <div style="color:#f57f17; font-weight:bold; font-size:0.9rem;">⏳ Partido sin puntuar aún</div>
                </div>`;
            }

            let txtPorraSets = p.sets ? p.sets : `<i style="color:#999;">Sin predicción</i>`;
            let txtPorraPtos = p.sets ? `<span style="font-size:0.9rem; color:#555;">| ${p.puntos} pts (${p.signo})</span>` : "";
            
            let infoPabellon = p.pabellon ? `<div style="font-size:0.85rem; color:#777; margin-top:2px;">📍 ${p.pabellon}</div>` : "";
            
            // INSIGNIA DE CATEGORÍA PARA EL HISTORIAL
            let categoryHtml = getCategoryHTML(p.categoria);

            blockHtml += `
            <div class="card-match" style="margin-bottom:20px; font-size:0.95rem; border-bottom:1px dashed #ccc; padding-bottom:15px; padding-top: 10px;">
                ${categoryHtml}
                <div style="font-weight:bold; color:#444; margin-bottom:6px; padding-right: 90px;">
                    🏐 ${eqName} vs ${rivalName}${infoJornadaEq}${infoLocFecha}
                    ${infoPabellon}
                </div>
                ${htmlReloj}
                <div style="display:flex; justify-content:space-between; flex-wrap:wrap; background:var(--bg-general); padding:12px; border-radius:6px; border-left: 4px solid var(--vcv-morado); margin-top:10px;">
                    <div style="margin-right:15px; margin-bottom:8px;">
                        <span style="color:#777; font-size:0.85rem; display:block; text-transform:uppercase; letter-spacing:0.5px;">Tu Predicción</span>
                        <span style="font-weight:bold; color:var(--vcv-morado); font-size:1.05rem;">${txtPorraSets}</span> ${txtPorraPtos}
                    </div>
                    <div>
                        <span style="color:#777; font-size:0.85rem; display:block; text-transform:uppercase; letter-spacing:0.5px;">Resultado Oficial</span>
                        ${ofText}
                    </div>
                </div>
                ${puntosInfo}
            </div>`;
        });
        
        blockHtml += `</div>`;
        
        if(hayDatosEnEsteBloque) { histHtml += blockHtml; }
    });
    
    if (histHtml === "") {
        histHtml = `<div class="alert-box alert-warning" style="display:block;">Ningún partido coincide con los filtros seleccionados.</div>`;
    }

    container.innerHTML = histHtml;
    container.style.display = "block";
    iniciarRelojes(); 
}
</script>




    <script>
        // Registrar Service Worker para PWA
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('sw.js').then(reg => {
                    reg.update(); // Forzar actualizacin siempre
                }).catch(err => console.log('SW Error:', err));
            });
        }
    
document.getElementById('btnForceSyncExcel').addEventListener('click', function(e) {
    e.preventDefault();
    const btn = this;
    const originalText = btn.innerHTML;
    btn.innerHTML = '⏳ Borrando Caché...';
    btn.disabled = true;
    
    fetchSeguro(scriptURL, {
        method: 'POST',
        body: JSON.stringify({ action: 'clear_cache', usuario: currentUser, password: currentPassword }),
        headers: { 'Content-Type': 'text/plain;charset=utf-8' }
    })
    .then(r => r.json())
    .then(data => {
        if(data.status === 'success') {
            btn.innerHTML = '✅ ¡Actualizado!';
            setTimeout(() => {
                window.location.href = window.location.pathname + '?v=' + new Date().getTime();
            }, 1000);
        } else {
            btn.innerHTML = originalText;
            btn.disabled = false;
            alert('Error: ' + data.message);
        }
    })
    .catch(err => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        alert('Error de conexión.');
    });
});


// ---------------------------------------------------
// LOGICA DE CALENDARIO / PROXIMOS PARTIDOS
// ---------------------------------------------------
window.initCalendar = function() {
    if(!window.appData || !window.appData.todos_partidos) return;
    
    let todos = window.appData.todos_partidos;
    
    // Sort by timestamp
    todos.sort((a, b) => {
        let tsA = a.timestamp || Infinity; 
        let tsB = b.timestamp || Infinity;
        return tsA - tsB; 
    });

    let catSelect = document.getElementById('calendarTeamSelect');
    let uniqueCats = window.appData.mis_equipos_siguiendo || [];
    
    let currentOptions = '<option value="">-- Ver Todos los Equipos --</option>';
    uniqueCats.forEach(cat => {
        currentOptions += `<option value="${cat}">${cat}</option>`;
    });
    catSelect.innerHTML = currentOptions;
    
    let savedCat = localStorage.getItem('pref_calendario_' + currentUser);
    if (savedCat && uniqueCats.includes(savedCat)) {
        catSelect.value = savedCat;
    }
    
    window.renderCalendar();
};

window.renderCalendar = function() {
    if(!window.appData || !window.appData.todos_partidos) return;
    
    let cat = document.getElementById('calendarTeamSelect').value;
    let search = document.getElementById('calendarSearchInput').value.toLowerCase().trim();
    
    localStorage.setItem('pref_calendario_' + currentUser, cat);
    
    let filtered = window.appData.todos_partidos.filter(p => {
        let matchCat = (!cat || p.equipo_local === cat || p.rival === cat);
        let matchSearch = (!search || p.rival.toLowerCase().includes(search) || p.equipo_local.toLowerCase().includes(search));
        return matchCat && matchSearch;
    });

    let html_res = "";
    if (filtered.length === 0) {
        html_res = `<div style="text-align:center; padding:30px; color:#888; font-weight:bold;">No se han encontrado partidos con estos filtros.</div>`;
    } else {
        filtered.forEach(p => {
            let fechaStr = "Fecha por confirmar";
            if (p.timestamp) {
                let d = new Date(p.timestamp);
                let dias = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
                let mes = (d.getMonth() + 1).toString().padStart(2, '0');
                let dia = d.getDate().toString().padStart(2, '0');
                let h = d.getHours().toString().padStart(2, '0');
                let m = d.getMinutes().toString().padStart(2, '0');
                fechaStr = `${dias[d.getDay()]} ${dia}/${mes} - ${h}:${m}`;
            }
            
            let esPasado = p.oficial_sets && p.oficial_sets.trim() !== "";
            let estadoHtml = esPasado 
                ? `<span style="background:var(--vcv-dorado); color:#fff; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:bold;">Finalizado: ${p.oficial_sets}</span>`
                : `<span style="background:#e9ecef; color:#555; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:bold;">Próximamente</span>`;
                
            let titulo = p.ubicacion === 'LOCAL' ? `<b>${p.equipo_local}</b> vs ${p.rival}` : `${p.rival} vs <b>${p.equipo_local}</b>`;
            let pabellonStr = p.pabellon ? `<div style="font-size:0.8rem; color:#777; margin-top:5px;">📍 ${p.pabellon}</div>` : '';
            let streamStr = p.streaming ? `<div style="margin-top:5px;"><a href="${p.streaming}" target="_blank" class="btn btn-sm" style="background:#ff0000; color:white; font-size:0.7rem; font-weight:bold; padding:2px 6px; border-radius:4px;">▶ Ver Streaming</a></div>` : '';

            html_res += `<div style="background:white; padding:15px; border-radius:10px; border-left:5px solid ${esPasado ? 'var(--vcv-dorado)' : 'var(--vcv-morado)'}; box-shadow:0 2px 5px rgba(0,0,0,0.06); transition: transform 0.2s;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:0.85rem; font-weight:bold; color:var(--vcv-morado);">${fechaStr}</span>
                    ${estadoHtml}
                </div>
                <div style="font-size:1.05rem; color:#222; margin-bottom:2px;">
                    ${titulo}
                </div>
                <div style="font-size:0.8rem; font-weight:bold; color:#1565c0; margin-bottom:2px;">🏆 ${p.categoria} - Jornada ${p.jornada_eq}</div>
                ${pabellonStr}
                ${streamStr}
            </div>`;
        });
    }
    
    document.getElementById('calendarResults').innerHTML = html_res;
};

document.getElementById('calendarTeamSelect').addEventListener('change', window.renderCalendar);
document.getElementById('calendarSearchInput').addEventListener('input', window.renderCalendar);

</script>




    
    
    




<script>
    // --- V2 INTERACTIVE LOGIC ---
    document.addEventListener("DOMContentLoaded", () => {
        if(window.lucide) lucide.createIcons();
    });

    function seleccionarSetV2(btn, val, matchId) {
      const hiddenInput = document.getElementById('e' + matchId + '_sets');
      if (hiddenInput) {
          hiddenInput.value = val;
      }
      const container = btn.parentElement;
      container.querySelectorAll('.set-option-btn-v2').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
    }
    
    
    function cambiarPuntosV2(matchId, delta) {
      const hiddenInput = document.getElementById('e' + matchId + '_puntos');
      const valSpan = document.getElementById('val-v2-' + matchId);
      const plusBtn = document.getElementById('signo-plus-v2-' + matchId);
      const minusBtn = document.getElementById('signo-minus-v2-' + matchId);
      const signInput = document.getElementById('e' + matchId + '_signo');

      if (hiddenInput && valSpan) {
          let current = parseInt(hiddenInput.value) || 14; 
          let next = current + delta;
          if (next < 0) next = 0; 
          
          hiddenInput.value = next;
          valSpan.innerText = next;

          if (next === 0) {
              if(plusBtn) {
                  plusBtn.classList.add('tied-btn');
                  plusBtn.disabled = true;
                  plusBtn.style.pointerEvents = 'none';
              }
              if(minusBtn) {
                  minusBtn.classList.add('tied-btn');
                  minusBtn.disabled = true;
                  minusBtn.style.pointerEvents = 'none';
              }
              if(signInput) signInput.value = 'Empate';
          } else {
              if(plusBtn) {
                  plusBtn.classList.remove('tied-btn');
                  plusBtn.disabled = false;
                  plusBtn.style.pointerEvents = 'auto';
              }
              if(minusBtn) {
                  minusBtn.classList.remove('tied-btn');
                  minusBtn.disabled = false;
                  minusBtn.style.pointerEvents = 'auto';
              }
              if(signInput.value === 'Empate') {
                  signInput.value = '';
                  if(plusBtn) plusBtn.classList.remove('selected');
                  if(minusBtn) minusBtn.classList.remove('selected');
              }
          }
      }
    }

    
    function cambiarSignoV2(matchId, btn, isLocal) {
      const hiddenInput = document.getElementById('e' + matchId + '_signo');
      if (hiddenInput) {
          hiddenInput.value = isLocal ? 'A favor' : 'En contra';
      }
      const plusBtn = document.getElementById('signo-plus-v2-' + matchId);
      const minusBtn = document.getElementById('signo-minus-v2-' + matchId);
      if(plusBtn) plusBtn.classList.remove('selected');
      if(minusBtn) minusBtn.classList.remove('selected');
      
      btn.classList.add('selected');
    }
    
    
    
    // Observer for Bottom Nav
    document.addEventListener("DOMContentLoaded", () => {
        const appSec = document.getElementById('appSection');
        const navWrap = document.getElementById('bottomNavWrapperV2');
        if(appSec && navWrap) {
            const observer = new MutationObserver(() => {
                if(appSec.style.display !== 'none') {
                    navWrap.style.display = 'block';
                } else {
                    navWrap.style.display = 'none';
                }
            });
            observer.observe(appSec, { attributes: true, attributeFilter: ['style'] });
        }
    });

    function switchTabV2(sectionId, btn) {
        // Hide all sections in appSection
        const sections = ['carteleraSection', 'clasificacionesSection', 'historialSection', 'calendarioSection', 'enlacesRfevbSection', 'prediccionesTotalesSection'];
        sections.forEach(s => {
            const el = document.getElementById(s);
            if (el) el.classList.remove('active-tab');
        });
        
        // Show target section
        const target = document.getElementById(sectionId);
        if (target) target.classList.add('active-tab');
        
        // If historial, also show prediccionesTotalesSection right below it (if they were separate)
        if (sectionId === 'carteleraSection') {
            const extra = document.getElementById('prediccionesTotalesSection');
            if (extra) extra.classList.add('active-tab');
        }

        // Update active button state
        document.querySelectorAll('.nav-item-v2').forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    document.addEventListener("DOMContentLoaded", () => {
        // Initialize first tab as active
        const firstSec = document.getElementById('carteleraSection');
        if (firstSec) firstSec.classList.add('active-tab');
        const tsSec = document.getElementById('prediccionesTotalesSection');
        if (tsSec) tsSec.classList.add('active-tab');
    });

    function handleSaveOrModifyV2(idPart) {
        const card = document.getElementById('card-v2-' + idPart);
        const btn = document.getElementById('btn-save-' + idPart);
        const summary = document.getElementById('summary-v2-' + idPart);
        const inputs = document.getElementById('inputs_eq_' + idPart);
        const isCollapsed = card.classList.contains('collapsed');

        if (isCollapsed) {
            card.classList.remove('collapsed');
            summary.style.display = 'none';
            inputs.style.display = 'block';
            btn.innerText = 'Guardar Predicción';
            btn.style.background = 'var(--secondary-color)';
            btn.style.color = '#000';
            btn.style.border = 'none';
        } else {
            const s = document.getElementById('e' + idPart + '_sets').value;
            const p = document.getElementById('e' + idPart + '_puntos').value;
            const sig = document.getElementById('e' + idPart + '_signo').value;

            if (!s || !p || !sig) {
                alert('Faltan campos por rellenar en este partido.');
                return;
            }
            if(window.isGuestMode) { alert("Modo invitado. No puedes guardar."); return; }
            if(!window.currentUser) { alert("Tu sesión ha expirado."); window.location.reload(); return; }

            const oldText = btn.innerText;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
            btn.disabled = true;

            let singlePred = {};
            singlePred[idPart] = { sets: s, puntos: p, signo: sig };

            window.fetchSeguro(window.scriptURL, {
                method: 'POST',
                body: JSON.stringify({
                    action: 'guardar',
                    usuario: window.currentUser,
                    password: window.currentPassword,
                    predicciones: singlePred
                }),
                headers: { 'Content-Type': 'text/plain;charset=utf-8' }
            })
            .then(res => res.json())
            .then(data => {
                btn.disabled = false;
                if(data.status === "success") {
                    
                    const selectedSignBtn = document.querySelector(`#signo-plus-v2-${idPart}.selected`) || document.querySelector(`#signo-minus-v2-${idPart}.selected`);
                    let signText = selectedSignBtn ? selectedSignBtn.innerText : (sig === 'Empate' ? 'Empate' : sig);
                    if(p == 0) signText = "Empate";
                    document.getElementById('summary-text-' + idPart).innerText = `${s} | ${p} pts | ${signText}`;

                    card.classList.add('collapsed');
                    inputs.style.display = 'none';
                    summary.style.display = 'block';
                    btn.innerText = 'Modificar Predicción';
                    btn.style.background = 'transparent';
                    btn.style.color = 'var(--text-muted)';
                    btn.style.border = '1px solid var(--border-color)';
                } else {
                    alert('Error al guardar: ' + data.message);
                    btn.innerText = oldText;
                }
            })
            .catch(err => {
                btn.disabled = false;
                btn.innerText = oldText;
                alert('Error de conexión.');
            });
        }
    }
</script>


<!-- MODAL NOTIFICACIONES -->
<div id="notificacionesModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:9999; align-items:center; justify-content:center; backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);">
    <div style="background:var(--bg-card); width:90%; max-width:400px; border-radius:16px; padding:24px; box-shadow:0 10px 40px rgba(0,0,0,0.5); position:relative; border: 1px solid var(--border-color);">
        <button onclick="document.getElementById('notificacionesModal').style.display='none'" style="position:absolute; top:12px; right:12px; background:none; border:none; color:var(--text-muted); font-size:1.8rem; cursor:pointer; line-height:1;">&times;</button>
        
        <h3 style="margin-top:0; margin-bottom:20px; color:var(--text-main); font-weight:800; font-family:'Space Grotesk', sans-serif; display:flex; align-items:center; gap:8px;">
            <i data-lucide="bell" style="width:20px; height:20px;"></i> Notificaciones
        </h3>
        
        <div style="background:var(--bg-input); border:1px dashed var(--border-color); border-radius:12px; padding:30px 20px; text-align:center; color:var(--text-muted);">
            <i data-lucide="hammer" style="width:36px; height:36px; margin-bottom:12px; color:var(--primary-color);"></i>
            <p style="margin:0; font-size:0.95rem; line-height:1.5;"><strong>¡En construcción!</strong><br><br>Estoy trabajando para implementar las notificaciones reales más adelante. :)</p>
        </div>
        
        <button onclick="document.getElementById('notificacionesModal').style.display='none'" class="btn btn-primary btn-block mt-4" style="background:var(--primary-color); border:none; font-weight:bold; border-radius:8px;">Entendido</button>
    </div>
</div>
</body>

</html>