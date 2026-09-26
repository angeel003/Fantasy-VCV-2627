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
            let calSec2 = document.getElementById('calendarioSection');
            if (calSec2) calSec2.style.display = "block";
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
                        <li><b>Aproximarse a la diferencia</b> (margen de error de ${data.reglas.max_dist} pts): <span style="color:var(--vcv-rojo); font-weight:bold;">Puntos proporcionales</span> a tu cercanía</li>
                    `;
                }
            }

            let displayNom = data.nombre_real && data.nombre_real !== usr ? `${data.nombre_real} <span style="font-size:0.85rem; color:#666; font-weight:normal; font-family:sans-serif;">(@${usr})</span>` : usr;
            document.getElementById('displayJugador').innerHTML = "👤 " + displayNom;
            
            let misInsignias = data.insignias[usr] || [];
            let insigniasHeaderHtml = "";
            let isAdmin = false;
            
            misInsignias.forEach(b => {
                if (b.type === 'admin') isAdmin = true;
                let cssColorClass = getBadgeCSS(b.type);
                insigniasHeaderHtml += `<img src="${URL_BADGE_GENERIC}" class="badge-header ${cssColorClass}" title="${b.text}" onclick="showMobileTooltip(event, '${b.text}')">`;
            });
            document.getElementById('displayBadges').innerHTML = insigniasHeaderHtml;
            
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

                    if (eq.estado === "ABIERTO") {
                        htmlPartidos += `
                        <div class="p-3 mb-3 partido-activo card-match" style="background: var(--vcv-blanco); border-radius: 8px; border: 1px solid var(--vcv-dorado); border-left: 5px solid var(--vcv-dorado); box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            ${categoryHtml}
                            <h5 style="margin-bottom: 5px; color:var(--vcv-morado); font-weight:bold; padding-right: 90px;">🏐 ${eq.equipo_local} vs ${eq.rival}${infoJornadaEq}</h5>
                      ${eq.es_derby ? `<div style="margin-bottom:10px; background:#fff3cd; color:#856404; padding:5px 10px; border-radius:5px; font-weight:bold; font-size:0.85rem; border:1px solid #ffeeba;">⚔️ ¡DERBY LOCAL! Los puntos valen DOBLE en este partido.</div>` : ""}
                            ${infoLocFecha}
                            ${infoPabellon}
                            
                            <div class="reloj-partido" data-ts="${eq.timestamp}" data-eq="${eq.id_partido}" style="font-size:0.85rem; font-weight:bold; padding:4px 8px; background:#fff3cd; color:#856404; border-radius:4px; display:inline-block; margin-bottom:15px;">Calculando tiempo...</div>
                            <div class="row inputs-eq" id="inputs_eq_${eq.id_partido}">
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
                                    <label>Puntos Dif. <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, 'Diferencia de puntos sumando TODOS los sets. (Mira el ejemplo arriba ❓)')">❓</span></label>
                                    <input type="number" class="form-control" id="e${eq.id_partido}_puntos" placeholder="Ej: 12" min="0" style="border-color: #ddd;">
                                </div>
                                <div class="form-group col-md-4">
                                    <label>Signo <span style="cursor:pointer; font-size:0.85rem;" onclick="showMobileTooltip(event, '¿Esa diferencia de puntos es a favor de quién?')">❓</span></label>
                                    <select class="form-control" id="e${eq.id_partido}_signo" style="border-color: #ddd;">
                                        <option value="">Elige...</option>
                                        <option value="A favor">${eq.es_derby ? "A favor de " + eq.equipo_local : "A favor (+)"}</option>
                                        <option value="En contra">${eq.es_derby ? "A favor de " + eq.rival : "En contra (-)"}</option>
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
            });

            if (equiposPermitidos === 0) {
                htmlPartidos = `<div class="alert-box alert-warning" style="display:block;">No hay partidos pendientes de predecir o en curso en este momento.</div>`;
                document.getElementById('btnSubmit').style.display = "none";
            } else if (equiposPermitidos === equiposCerrados) { document.getElementById('btnSubmit').style.display = "none"; }
            
            document.getElementById('contenedorPartidos').innerHTML = htmlPartidos;
            iniciarRelojes();

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
                document.getElementById('prediccionesTotalesSection').style.display = "block";
                
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
            document.getElementById('btnReload').style.display = "flex";
            document.getElementById('btnLogout').style.display = "block";
            iniciarRelojTotales();
        } else {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = data.message; msgBox.style.display = "block";
        }
    })
    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error: " + err.message + " | " + (err.stack || ""); msgBox.style.display = "block"; })
    .finally(() => { 
        btn.innerText = "Entrar al Fantasy"; 
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

                        if (isGuestMode) {
                if (diff <= 0 && diff > -14400000) {
                    el.innerHTML = "⏱️ Partido en curso";
                    el.style.backgroundColor = "#fde8e8"; el.style.color = "var(--vcv-rojo)";
                } else if (diff <= -14400000) {
                    el.innerHTML = "🏁 Partido Finalizado";
                    el.style.backgroundColor = "#e9ecef"; el.style.color = "#495057";
                } else {
                    let d = Math.floor(diff / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diff % (1000 * 60)) / 1000);
                    el.innerHTML = `⏳ Empieza en: ${d}d ${h}h ${m}m ${s}s`;
                    el.style.backgroundColor = "#e3f2fd"; el.style.color = "#1565c0";
                }
            } else {
                if (diff <= limite && diff > -14400000) { 
                    el.innerHTML = "🔒 CERRADO (Empieza en menos de 15 min)";
                    el.style.backgroundColor = "#fde8e8"; el.style.color = "var(--vcv-rojo)";
                    if(eqId) {
                        const divInputs = document.getElementById(`inputs_eq_${eqId}`);
                        if(divInputs) divInputs.querySelectorAll('input, select').forEach(i => i.disabled = true);
                    }
                } else if (diff <= -14400000) {
                    el.innerHTML = "🏁 Partido en curso o Finalizado";
                    el.style.backgroundColor = "#e9ecef"; el.style.color = "#495057";
                } else {
                    let diffToClose = diff - limite; 
                    let d = Math.floor(diffToClose / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diffToClose % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diffToClose % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diffToClose % (1000 * 60)) / 1000);
                    el.innerHTML = `🔒 Se cierra en: ${d}d ${h}h ${m}m ${s}s`;
                    el.style.backgroundColor = "#e3f2fd"; el.style.color = "#1565c0";
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




    
    
    <!-- FAB MENU NAV (Navegación Rápida) FUERA DEL APPSECTION PARA QUE POSITION FIXED FUNCIONE BIEN -->
    <div id="fab-menu" style="position: fixed; bottom: 90px; right: 25px; z-index: 9999; text-align: right; display: none;">
        <div id="fab-links" style="display: none; flex-direction: column; gap: 8px; margin-bottom: 10px; background: rgba(255,255,255,0.95); padding: 12px; border-radius: 12px; box-shadow: 0 6px 16px rgba(0,0,0,0.25); border: 2px solid var(--vcv-dorado); text-align: left; backdrop-filter: blur(5px);">
            <a id="fab-cartelera" href="#carteleraSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">🏐 Cartelera de Partidos</a>
            <a id="fab-ranking" href="#clasificacionesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">🏆 Ranking</a>
            <a id="fab-enlaces" href="#enlacesRfevbSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">🔗 Enlaces Rfevb</a>
            <a id="fab-historial" href="#historialSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">✅ Mis Predicciones</a>
            <a id="fab-calendario" href="#calendarioSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none; border-bottom: 1px solid #ddd;">📅 Próximos encuentros</a>
            <a id="fab-totales" href="#prediccionesTotalesSection" onclick="toggleFab()" style="color: var(--vcv-morado); font-weight: bold; font-size: 1.1rem; text-decoration: none; padding: 8px 10px; display: none;">🔮 Top Secret</a>
        </div>
        <button id="fab-btn" onclick="toggleFab()" style="background: var(--vcv-dorado); color: var(--vcv-morado); border: 2px solid var(--vcv-morado); border-radius: 50%; width: 55px; height: 55px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; display: flex; align-items: center; justify-content: center; margin-left: auto; transition: transform 0.2s;">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </button>
    </div>
    
    <script>
        function toggleFab() {
            var links = document.getElementById('fab-links');
            var btn = document.getElementById('fab-btn');
            if (links.style.display === 'none' || links.style.display === '') {
                links.style.display = 'flex';
                btn.style.transform = 'rotate(45deg)';
            } else {
                links.style.display = 'none';
                btn.style.transform = 'rotate(0deg)';
            }
        }
        
        
        // Cierra el menú de la lupa al hacer click fuera
        document.addEventListener('click', function(event) {
            var fabMenu = document.getElementById('fab-menu');
            var links = document.getElementById('fab-links');
            var btn = document.getElementById('fab-btn');
            
            if (fabMenu && links && btn) {
                var isClickInside = fabMenu.contains(event.target);
                if (!isClickInside && links.style.display === 'flex') {
                    links.style.display = 'none';
                    btn.style.transform = 'rotate(0deg)';
                }
            }
        });
        
        function checkFabVisibility() {
            var appSec = document.getElementById('appSection');
            
            // NO MOSTRAR EN MODO INVITADO
            // currentUser usa 'let', así que no está en 'window'. Lo comprobamos de forma segura.
            var isGuest = true;
            try {
                if (typeof currentUser !== 'undefined' && currentUser && currentUser !== "INVITADO") {
                    isGuest = false;
                }
            } catch(e) {}
            
            if(appSec && appSec.style.display !== 'none' && !isGuest) {
                document.getElementById('fab-menu').style.display = 'block';
                
                // Show/hide specific links based on section visibility
                var cartelera = document.getElementById('carteleraSection');
                var ranking = document.getElementById('clasificacionesSection');
                var enlaces = document.getElementById('enlacesRfevbSection');
                var historial = document.getElementById('historialSection');
                var calendario = document.getElementById('calendarioSection');
                var totales = document.getElementById('prediccionesTotalesSection');
                
                document.getElementById('fab-cartelera').style.display = (cartelera && cartelera.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-ranking').style.display = (ranking && ranking.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-enlaces').style.display = (enlaces && enlaces.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-historial').style.display = (historial && historial.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-calendario').style.display = (calendario && calendario.style.display !== 'none') ? 'block' : 'none';
                document.getElementById('fab-totales').style.display = (totales && totales.style.display !== 'none') ? 'block' : 'none';
                
            } else {
                document.getElementById('fab-menu').style.display = 'none';
                document.getElementById('fab-links').style.display = 'none';
            }
        }
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                checkFabVisibility();
            });
        });
        
        var appSec = document.getElementById('appSection');
        if(appSec) {
            observer.observe(appSec, { attributes: true, subtree: true });
        }
        setInterval(checkFabVisibility, 1000);
    </script>



</body>
</html>