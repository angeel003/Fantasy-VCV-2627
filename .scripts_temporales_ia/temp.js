
const scriptURL = "https://script.google.com/macros/s/AKfycbzM7QuqH1yFRL9rSA7CAUHZX3cogU6AH3PAW36mQkWhMw2ZDnA3JhI-U2bC7TQyNOHz/exec";

// --- PON AQUÍ TUS ENLACES DE GITHUB CUANDO LOS TENGAS ---
const URL_BADGE_GENERIC = "https://upload.wikimedia.org/wikipedia/commons/e/e4/Twitter_Verified_Badge.svg"; 
// --------------------------------------------------------

let currentUser = ""; let currentPassword = ""; let equiposTotalesInfo = [];
let intervalCountdown = null;
let intervalTotalesCountdown = null;
let globalHistorialData = [];
let isSortDesc = true;
let currentJornadaGlobal = 0;
let isGuestMode = false;


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
}

function formatFecha(ts) {
    if(!ts) return "";
    let d = new Date(ts);
    return d.toLocaleDateString('es-ES', {day:'2-digit', month:'2-digit', hour:'2-digit', minute:'2-digit'});
}

function getBadgeCSS(type) {
    if(type === 'admin') return 'badge-admin';
    if(type === 'staff') return 'badge-staff';
    if(type === 'entrenador') return 'badge-entrenador';
    if(type === 'jugador') return 'badge-jugador';
    if(type === 'exjugador') return 'badge-exjugador';
    return '';
}

// ------------------------------------------------------------------
// LÓGICA DEL TOOLTIP FLOTANTE PARA MÓVILES
// ------------------------------------------------------------------
function showMobileTooltip(e, text) {
    e.stopPropagation(); 
    const tooltip = document.getElementById('mobileTooltip');
    tooltip.innerText = text;
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = (rect.left + rect.width / 2) + 'px';
    tooltip.style.top = rect.top + 'px';
    
    tooltip.classList.add('show');
    
    clearTimeout(tooltip.timeoutId);
    tooltip.timeoutId = setTimeout(() => {
        tooltip.classList.remove('show');
    }, 3500); 
}

document.addEventListener('click', function(e) {
    const tooltip = document.getElementById('mobileTooltip');
    if (tooltip && tooltip.classList.contains('show')) {
        tooltip.classList.remove('show');
    }
});

function mostrarToast(mensaje) {
    const toast = document.getElementById('toastNotification');
    toast.innerText = mensaje;
    toast.style.opacity = "1";
    setTimeout(() => { toast.style.opacity = "0"; }, 2500);
}

// ------------------------------------------------------------------
// BOTÓN DE RECARGAR
// ------------------------------------------------------------------
document.getElementById('btnReload').addEventListener('click', function() {
    const btn = this;
    if(btn.classList.contains('spin-anim')) return; 
    btn.classList.add('spin-anim');
    
    if (isGuestMode) { document.getElementById('btnGuest').click(); } 
    else { document.getElementById('btnLogin').click(); }
    
    let checkInterval = setInterval(() => {
        let targetBtn = isGuestMode ? document.getElementById('btnGuest') : document.getElementById('btnLogin');
        if (!targetBtn.disabled) {
            btn.classList.remove('spin-anim');
            clearInterval(checkInterval);
            mostrarToast("✅ Datos sincronizados");
        }
    }, 300);
});

// ------------------------------------------------------------------
// FUNCIONES INTRANET ADMINISTRADOR
// ------------------------------------------------------------------
function renderAdminPanel(equipos) {
    let html = "";
    equipos.forEach(eq => {
        html += `
        <div class="admin-match-box">
            <div style="font-weight:bold; margin-bottom:8px; color: #e65100;">${eq.equipo_local} vs ${eq.rival} <span style="color:#666; font-size:0.8rem; font-weight:normal;">(${eq.id_partido})</span></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="adm_sets_${eq.id_partido}" class="form-control form-control-sm" placeholder="Sets (3-1)" value="${eq.oficial_sets}">
                <input type="text" id="adm_parc_${eq.id_partido}" class="form-control form-control-sm" placeholder="Parc (25-20,25-23...)" value="${eq.oficial_parciales}">
            </div>
            <button class="btn btn-sm btn-dark mt-2" style="font-weight:bold;" onclick="guardarResultadoAdmin(event, '${eq.id_partido}')">💾 Subir Resultado</button>
        </div>`;
    });
    if (html === "") html = "<div style='color:white; font-size:0.9rem;'>No hay partidos disponibles.</div>";
    document.getElementById('adminListaPartidos').innerHTML = html;
}

document.getElementById('btnAdminSync').addEventListener('click', function(e) {
    e.preventDefault();
    const btn = this;
    btn.disabled = true; btn.innerText = "⏳ Sincronizando...";
    
    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'sync_permisos', usuario: currentUser, password: currentPassword }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(d => {
        if(d.status === "success") { mostrarToast(d.message); } 
        else { alert("Error: " + d.message); }
    })
    .finally(() => { btn.disabled = false; btn.innerText = "🔄 Auto-Permisos"; });
});

window.guardarResultadoAdmin = function(e, idPart) {
    e.preventDefault();
    const btn = e.target;
    const sets = document.getElementById(`adm_sets_${idPart}`).value.trim();
    const parc = document.getElementById(`adm_parc_${idPart}`).value.trim();
    
    btn.disabled = true; btn.innerText = "Subiendo...";
    
    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'save_resultado_admin', usuario: currentUser, password: currentPassword, id_partido: idPart, sets: sets, parciales: parc }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(d => {
        if(d.status === "success") { mostrarToast("✅ Resultado subido al Excel"); } 
        else { alert("Error: " + d.message); }
    })
    .finally(() => { btn.disabled = false; btn.innerText = "💾 Subir Resultado"; });
}

window.crearUsuarioAdmin = function(e) {
    e.preventDefault();
    const btn = e.target;
    const nu = document.getElementById('addUsrName').value.trim();
    const np = document.getElementById('addUsrPwd').value.trim();
    const nr = document.getElementById('addUsrReal').value.trim();
    
    if(!nu || !np) { alert("Usuario y Contraseña son obligatorios"); return; }
    
    btn.disabled = true; btn.innerText = "Creando...";
    
    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'add_user', usuario: currentUser, password: currentPassword, new_u: nu, new_p: np, new_n: nr }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(d => {
        if(d.status === "success") { 
            mostrarToast(d.message); 
            document.getElementById('addUsrName').value = "";
            document.getElementById('addUsrPwd').value = "";
            document.getElementById('addUsrReal').value = "";
        } 
        else { alert("Error: " + d.message); }
    })
    .finally(() => { btn.disabled = false; btn.innerText = "➕ Crear Usuario"; });
}
// ------------------------------------------------------------------

function getCategoryHTML(catName) {
    if (!catName) return "";
    let safeName = catName.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
    let baseUrl = "files/categories/"; 
    let imgUrl = baseUrl + safeName + ".png";
    return `<img src="${imgUrl}" class="cat-badge-img" alt="${catName}" title="${catName}" onerror="this.onerror=null; this.outerHTML='<div class=\\'cat-badge-text\\' title=\\'${catName}\\'>${catName}</div>';">`;
}

// LÓGICA DE CAMBIO DE CONTRASEÑA
document.getElementById('btnChangePwd').addEventListener('click', function(e) {
    e.preventDefault();
    const usr = document.getElementById('cpUsuario').value.trim();
    const oldP = document.getElementById('cpOldPwd').value.trim();
    const newP1 = document.getElementById('cpNewPwd').value.trim();
    const newP2 = document.getElementById('cpNewPwd2').value.trim();
    const msgBox = document.getElementById('msgChangePwd');
    const btn = this;

    if(!usr || !oldP || !newP1 || !newP2) {
        msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Por favor, rellena todos los campos."; msgBox.style.display = "block"; return;
    }
    if(newP1 !== newP2) {
        msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Las contraseñas nuevas no coinciden."; msgBox.style.display = "block"; return;
    }

    btn.disabled = true; 
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Actualizando...'; 
    msgBox.style.display = "none";

    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'change_password', usuario: usr, old_password: oldP, new_password: newP1 }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(data => {
        msgBox.style.display = "block";
        if(data.status === "success") {
            msgBox.className = "alert-box alert-success"; msgBox.innerText = data.message;
            document.getElementById('cpOldPwd').value = ""; document.getElementById('cpNewPwd').value = ""; document.getElementById('cpNewPwd2').value = "";
        } else {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = data.message;
        }
    })
    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error de conexión."; msgBox.style.display = "block"; })
    .finally(() => { btn.innerText = "Actualizar Contraseña"; btn.disabled = false; });
});

// LÓGICA DE PETICIÓN DE CAMBIO DE NOMBRE
document.getElementById('btnReqName').addEventListener('click', function(e) {
    e.preventDefault();
    const usr = document.getElementById('rnUsuario').value.trim();
    const pwd = document.getElementById('rnPwd').value.trim();
    const newU = document.getElementById('rnNewUser').value.trim();
    const newN = document.getElementById('rnNewName').value.trim();
    const msgBox = document.getElementById('msgReqName');
    const btn = this;

    if(!usr || !pwd) {
        msgBox.className = "alert-box alert-danger"; msgBox.innerText = "El usuario y contraseña actuales son obligatorios."; msgBox.style.display = "block"; return;
    }
    if(!newU && !newN) {
        msgBox.className = "alert-box alert-warning"; msgBox.innerText = "Debes rellenar al menos un dato nuevo para solicitar el cambio."; msgBox.style.display = "block"; return;
    }

    btn.disabled = true; 
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...'; 
    msgBox.style.display = "none";

    fetch(scriptURL, { 
        method: 'POST', 
        body: JSON.stringify({ action: 'request_name_change', usuario: usr, password: pwd, new_usuario: newU, new_nombre: newN }), 
        headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
    })
    .then(res => res.json())
    .then(data => {
        msgBox.style.display = "block";
        if(data.status === "success") {
            msgBox.className = "alert-box alert-success"; msgBox.innerText = data.message;
            document.getElementById('rnNewUser').value = ""; document.getElementById('rnNewName').value = "";
        } else {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = data.message;
        }
    })
    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error de conexión."; msgBox.style.display = "block"; })
    .finally(() => { btn.innerText = "Enviar Solicitud"; btn.disabled = false; });
});

// LOGICA MODO INVITADO
document.getElementById('btnGuest').addEventListener('click', function(e) {
    e.preventDefault();
    const msgBox = document.getElementById('loginMessage');
    const btn = this;
    
    btn.disabled = true; 
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Entrando...'; 
    msgBox.style.display = "none";

    fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_guest' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
    .then(res => res.json())
    .then(data => {
        if(data.status === "success") {
            isGuestMode = true;
            document.getElementById('displayJugador').innerText = "👀 Modo Invitado";
            document.getElementById('tituloPrincipalSeccion').innerText = "Cartelera Pública";
            
            document.getElementById('appSection').style.display = "block";
            document.getElementById('btnReload').style.display = "flex"; 
            document.querySelector('#prediccionForm > div').style.display = "none"; 
            document.getElementById('adminPanelWrapper').style.display = "none";
            
            document.getElementById('btnSubmit').style.display = "none";
            document.getElementById('warningPredicciones').style.display = "none";
            document.getElementById('clasificacionesSection').style.display = "none";
            document.getElementById('historialSection').style.display = "none";
            document.getElementById('prediccionesTotalesSection').style.display = "none";

            data.equipos.sort((a, b) => {
                let tsA = a.timestamp || Infinity; 
                let tsB = b.timestamp || Infinity;
                return tsA - tsB; 
            });

            let htmlProximos = "";
            let htmlPasados = "";

            data.equipos.forEach(eq => {
                let valJornada = String(eq.jornada_eq || "").trim();
                let infoJornadaEq = valJornada ? (isNaN(valJornada) ? ` <span style="font-size:0.9rem; color:#666; font-weight:normal;">(${valJornada})</span>` : ` <span style="font-size:0.9rem; color:#666; font-weight:normal;">(Jornada ${valJornada})</span>`) : "";
                let iconoLoc = eq.ubicacion === "CASA" ? "🏠" : (eq.ubicacion === "FUERA" ? "✈️" : "");
                let infoLocFecha = (iconoLoc || eq.timestamp) ? `<div style="font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;">${iconoLoc} ${formatFecha(eq.timestamp)}</div>` : "";
                let infoPabellon = eq.pabellon ? `<div style="font-size:0.85rem; color:#777; margin-bottom:10px;">📍 ${eq.pabellon}</div>` : "<div style='margin-bottom:10px;'></div>";

                let infoAdicional = "";
                let esPasado = false;

                if (eq.oficial_sets && eq.oficial_sets.includes("-")) {
                    esPasado = true;
                    let sL = parseInt(eq.oficial_sets.split("-")[0]);
                    let sV = parseInt(eq.oficial_sets.split("-")[1]);
                    let textoRes = sL > sV ? `<span style="color:#28a745; font-weight:bold; margin-left:5px;">🟢 Ganado</span>` : `<span style="color:var(--vcv-rojo); font-weight:bold; margin-left:5px;">🔴 Perdido</span>`;
                    
                    infoAdicional = `
                    <div style="margin-top:10px; background:var(--bg-general); border-left:4px solid var(--vcv-morado); padding:10px; border-radius:4px;">
                        <span style="font-size:0.85rem; color:#666; text-transform:uppercase; letter-spacing:0.5px;">Resultado Oficial</span><br>
                        <b style="font-size:1.1rem; color:var(--vcv-negro);">${eq.oficial_sets}</b> ${textoRes} <br>
                        <span style="font-size:0.9rem; color:#555;">(${eq.oficial_parciales})</span>
                    </div>`;
                } else if (eq.estado === "CERRADO" || eq.visibilidad === "OCULTAR") {
                    esPasado = true;
                    infoAdicional = `<div style="margin-top:10px;"><span style="background-color:#e2e3e5; color:#383d41; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:0.85rem;">🔒 Partido finalizado</span></div>`;
                } else {
                    infoAdicional = `<div style="margin-top:10px;"><span style="background-color:#d4edda; color:#155724; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:0.85rem;">🟢 Próximamente</span></div>`;
                }
                
                let categoryHtml = getCategoryHTML(eq.categoria);

                let cardHtml = `
                <div class="p-3 mb-3 card-match" style="background: var(--vcv-blanco); border-radius: 8px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    ${categoryHtml}
                    <h5 style="margin-bottom: 5px; color:var(--vcv-morado); font-weight:bold; padding-right: 90px;">🏐 ${eq.equipo_local} vs ${eq.rival}${infoJornadaEq}</h5>
                    ${infoLocFecha}
                    ${infoPabellon}
                    ${infoAdicional}
                </div>`;

                if (esPasado) { htmlPasados = cardHtml + htmlPasados; } 
                else { htmlProximos += cardHtml; }
            });

            let finalHtml = "";
            if(htmlProximos !== "") finalHtml += `<h4 style="color:var(--vcv-morado); margin-bottom:15px; text-align:left; border-bottom:2px solid var(--vcv-dorado); padding-bottom:5px;">Próximos Partidos</h4>` + htmlProximos;
            if(htmlPasados !== "") finalHtml += `<h4 style="color:var(--vcv-morado); margin-top:30px; margin-bottom:15px; text-align:left; border-bottom:2px solid var(--vcv-dorado); padding-bottom:5px;">Últimos Resultados</h4>` + htmlPasados;
            
            if(finalHtml === "") finalHtml = `<div class="alert-box alert-info" style="display:block;">No hay partidos públicos disponibles en este momento.</div>`;

            document.getElementById('contenedorPartidos').innerHTML = finalHtml;
            document.getElementById('loginSection').style.display = "none";
        } else {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error cargando modo invitado."; msgBox.style.display = "block";
        }
    })
    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error de conexión."; msgBox.style.display = "block"; })
    .finally(() => { 
        btn.innerText = "👀 Entrar como Invitado"; 
        btn.disabled = false; 
    });
});

// LOGICA USUARIO NORMAL
document.getElementById('btnLogin').addEventListener('click', function() {
    const usr = document.getElementById('loginUsuario').value.trim();
    const pwd = document.getElementById('loginPassword').value.trim();
    const msgBox = document.getElementById('loginMessage');
    const btn = this;

    if(!usr || !pwd) { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Rellena usuario y contraseña."; msgBox.style.display = "block"; return; }
    
    btn.disabled = true; 
    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Accediendo...'; 
    msgBox.style.display = "none";

    fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'login_auth', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
    .then(res => res.json())
    .then(dataAuth => {
        if (dataAuth.status !== "success") {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = dataAuth.message; msgBox.style.display = "block";
            btn.disabled = false; btn.innerText = "Entrar al Fantasy"; return;
        }
        currentUser = usr; currentPassword = pwd;
        document.getElementById('displayJugador').innerHTML = "👤 " + (dataAuth.nombre_real || usr);
        let misInsignias = dataAuth.insignias[usr] || [];
        let insigniasHeaderHtml = ""; let isAdmin = false;
        misInsignias.forEach(b => {
            if (b.type === 'admin') isAdmin = true;
            insigniasHeaderHtml += `<img src="${URL_BADGE_GENERIC}" class="badge-header ${getBadgeCSS(b.type)}" title="${b.text}" onclick="showMobileTooltip(event, '${b.text}')">`;
        });
        document.getElementById('displayBadges').innerHTML = insigniasHeaderHtml;
        if (isAdmin) { document.getElementById('adminPanelWrapper').style.display = "block"; }
        
        msgBox.className = "alert-box alert-success"; msgBox.innerText = "¡Credenciales correctas! Descargando cartelera de partidos..."; msgBox.style.display = "block";
        
        fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'get_data', usuario: usr, password: pwd }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
        .then(res => res.json())
        .then(data => {
        if(data.status === "success") {
            currentUser = usr; currentPassword = pwd;
            currentJornadaGlobal = data.jornada;
            
            if(data.reglas) {
                let listaReglas = document.getElementById('listaReglasPuntuacion');
                if(listaReglas) {
                    listaReglas.innerHTML = `
                        <li>Acertar el <b>Resultado Exacto (Sets)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.sets} pts</span></li>
                        <li>Acertar el <b>Ganador del partido</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.ganador} pts</span></li>
                        <li>Acertar la <b>Diferencia de puntos exacta</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_exacta} pts</span> extra</li>
                        <li>Acertar la <b>Diferencia aproximada (±5)</b>: <span style="color:var(--vcv-rojo); font-weight:bold;">+${data.reglas.diff_5} pts</span> extra</li>
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
            } else {
                document.getElementById('adminPanelWrapper').style.display = "none";
            }

            document.getElementById('tituloPrincipalSeccion').innerText = "Mis Predicciones";

            data.equipos.sort((a, b) => {
                let tsA = a.timestamp || Infinity; 
                let tsB = b.timestamp || Infinity;
                return tsA - tsB; 
            });
            
            equiposTotalesInfo = data.equipos;

            let htmlPartidos = `<h4 style="color: var(--vcv-morado); margin-bottom: 20px;">Cartelera de Partidos</h4>`;
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

                        fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'save_totales', usuario: currentUser, password: currentPassword, predicciones_totales: prediccionesTot }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
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
            cargarDatosAntiguos();
            iniciarRelojTotales();
        } else {
            msgBox.className = "alert-box alert-danger"; msgBox.innerText = data.message; msgBox.style.display = "block";
        }
    })
    .catch(err => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error de conexión."; msgBox.style.display = "block"; })
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

            if (diff <= limite && diff > -14400000) { 
                el.innerHTML = "🔒 CERRADO (Empieza en menos de 15 min)";
                el.style.backgroundColor = "#fde8e8"; el.style.color = "var(--vcv-rojo)";
                if(eqId && !isGuestMode) {
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
                el.innerHTML = `⏳ Se cierra en: ${d}d ${h}h ${m}m ${s}s`;
                el.style.backgroundColor = "#e3f2fd"; el.style.color = "#1565c0";
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
    fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'load', usuario: currentUser, password: currentPassword }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
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

    fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'save', usuario: currentUser, password: currentPassword, jornada: currentJornadaGlobal, predicciones: prediccionesList }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
    .then(res => res.json())
    .then(data => {
        msgBox.style.display = "block";
        if (data.status === "success") { msgBox.className = "alert-box alert-success"; msgBox.innerText = "✅ " + data.message; } 
        else { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "❌ " + data.message; }
    })
    .catch(() => { msgBox.className = "alert-box alert-danger"; msgBox.innerText = "Error de conexión."; msgBox.style.display = "block"; })
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

    fetch(scriptURL, { method: 'POST', body: JSON.stringify({ action: 'get_history', usuario: currentUser, password: currentPassword }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } })
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

            let infoLocFecha = "";
            let htmlReloj = "";
            let iconoLoc = p.ubicacion === "CASA" ? "🏠" : (p.ubicacion === "FUERA" ? "✈️" : "");
            
            if (esActual) {
                if(iconoLoc || p.timestamp) {
                    infoLocFecha = `<span style="font-weight:normal; font-size:0.85rem; color:#666; margin-left:10px;">${iconoLoc} ${formatFecha(p.timestamp)}</span>`;
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
