import re

with open('prototipo_stitch.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# We need to define the COMPLETE JS logic to replace the dummy one
new_js = """
  <script>
    const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzM7QuqH1yFRL9rSA7CAUHZX3cogU6AH3PAW36mQkWhMw2ZDnA3JhI-U2bC7TQyNOHz/exec";
    
    const appState = {
      usuario: "",
      password: "",
      nombreReal: "",
      isAdmin: false,
      isGuest: false,
      puntosTotales: 0,
      jornadaActiva: "-",
      predicciones: {},
      matchStates: {}, // To store interactive states: matchStates[id] = {sets, puntos, signo}
      appData: null // Store full server response
    };

    // INICIALIZACIÓN
    document.addEventListener("DOMContentLoaded", () => {
      lucide.createIcons();
      document.getElementById('login-modal').classList.add('show');
    });

    // --- TOAST NOTIFICATIONS ---
    function mostrarToast(msg, icon = 'info') {
      const toast = document.getElementById('vcv-toast');
      const msgEl = document.getElementById('toast-msg');
      if(toast && msgEl) {
          msgEl.innerHTML = `<i data-lucide="${icon}" style="width:16px;height:16px;margin-right:8px;"></i> ${msg}`;
          lucide.createIcons();
          toast.classList.add('show');
          setTimeout(() => toast.classList.remove('show'), 3500);
      } else {
          alert(msg);
      }
    }

    // --- NAVEGACIÓN ---
    function navegarA(viewName, btnEl) {
      document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
      document.querySelectorAll('.nav-item-btn').forEach(btn => btn.classList.remove('active'));
      const target = document.getElementById('view-' + viewName);
      if (target) {
        target.classList.add('active');
        if(btnEl) btnEl.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
    
    // --- FETCH SEGURO ---
    async function fetchSeguro(url, options, maxRetries = 2) {
      let retries = 0;
      while (retries < maxRetries) {
        try {
          let res = await fetch(url, options);
          if (res.ok) return res;
        } catch (e) {
          retries++;
          if (retries >= maxRetries) throw e;
          await new Promise(r => setTimeout(r, 1000));
        }
      }
    }

    // --- LOGIN ---
    async function handleLoginSubmit(e) {
      e.preventDefault();
      const u = document.getElementById('login-user').value.trim();
      const p = document.getElementById('login-pass').value.trim();
      if (!u || !p) return;
      
      const btn = document.getElementById('btn-login-action');
      btn.innerHTML = `<i data-lucide="loader" class="lucide-spin" style="margin-right:8px;"></i> CARGANDO...`;
      lucide.createIcons();
      btn.disabled = true;
      
      try {
        const res = await fetchSeguro(SCRIPT_URL, {
          method: 'POST',
          body: JSON.stringify({ action: 'login', usuario: u, password: p, version: '2.0.0' })
        });
        const data = await res.json();
        
        if (data.status === "success") {
          appState.usuario = u;
          appState.password = p;
          appState.isGuest = false;
          appState.isAdmin = data.is_admin || false;
          appState.nombreReal = data.nombre_real || "";
          appState.jornadaActiva = data.jornada || "-";
          appState.appData = data;
          
          document.getElementById('login-modal').classList.remove('show');
          
          // Set UI Globals
          document.getElementById('display-user-handle').innerText = u;
          const ptsObj = data.clasificaciones && data.clasificaciones['Liga General VCV'] ? data.clasificaciones['Liga General VCV'].find(x => x.usuario.toLowerCase() === u.toLowerCase()) : null;
          appState.puntosTotales = ptsObj ? ptsObj.puntos : 0;
          document.getElementById('display-user-pts').innerText = appState.puntosTotales + " pts";
          
          const adminPanel = document.getElementById('intranet-admin-panel');
          if (adminPanel) adminPanel.style.display = appState.isAdmin ? 'block' : 'none';
          
          const allJornadas = document.querySelectorAll('.badge-jornada');
          allJornadas.forEach(el => el.innerText = "Jornada " + appState.jornadaActiva);
          
          await loadPredicciones();
          
          // Render All Views Dynamically
          renderPartidos(data.equipos || []);
          renderRanking(data.clasificaciones || {}, data.ligas || []);
          renderHistorial(data.todos_partidos || []);
          renderCalendario(data.todos_partidos || []);
          
          mostrarToast("Bienvenido al Fantasy VCV", "check-circle");
        } else {
          mostrarToast(data.message || "Error al iniciar sesión", "alert-circle");
          btn.innerHTML = `<span>Entrar al Fantasy</span><i data-lucide="chevron-right"></i>`;
          lucide.createIcons();
          btn.disabled = false;
        }
      } catch(err) {
        mostrarToast("Error de red. Reintenta.", "wifi-off");
        btn.innerHTML = `<span>Entrar al Fantasy</span><i data-lucide="chevron-right"></i>`;
        lucide.createIcons();
        btn.disabled = false;
      }
    }
    
    function entrarComoInvitado() {
        mostrarToast("Modo Invitado: Solo lectura");
        appState.isGuest = true;
        document.getElementById('login-modal').classList.remove('show');
    }
    
    async function loadPredicciones() {
      try {
        const res = await fetchSeguro(SCRIPT_URL, {
            method: 'POST',
            body: JSON.stringify({ action: 'load', usuario: appState.usuario, password: appState.password })
        });
        const d = await res.json();
        if(d.status === "success" && d.data && d.data.predicciones) {
            appState.predicciones = d.data.predicciones;
        }
      } catch(e) { console.error("Error cargando predicciones", e); }
    }

    // --- INTERACCIONES DE CARTELERA ---
    function seleccionarSet(btn, val, matchId) {
      if(!appState.matchStates[matchId]) appState.matchStates[matchId] = { puntos: 14, signo: '+' };
      appState.matchStates[matchId].sets = val;
      
      const container = btn.parentElement;
      container.querySelectorAll('.set-option-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
    }
    
    function cambiarPuntos(matchId, delta) {
      if(!appState.matchStates[matchId]) appState.matchStates[matchId] = { sets: null, puntos: 14, signo: '+' };
      let p = appState.matchStates[matchId].puntos + delta;
      if (p < 1) p = 1;
      appState.matchStates[matchId].puntos = p;
      const el = document.getElementById('val-' + matchId);
      if(el) el.innerText = p;
    }
    
    function cambiarSigno(matchId, btn, val) {
      if(!appState.matchStates[matchId]) appState.matchStates[matchId] = { sets: null, puntos: 14, signo: '+' };
      appState.matchStates[matchId].signo = val;
      
      const plusBtn = document.getElementById('signo-plus-' + matchId);
      const minusBtn = document.getElementById('signo-minus-' + matchId);
      if(plusBtn) plusBtn.classList.remove('selected', 'btn-danger');
      if(minusBtn) minusBtn.classList.remove('selected', 'btn-danger');
      
      btn.classList.add('selected');
      if(val === '-') btn.classList.add('btn-danger');
    }
    
    async function guardarPronosticos(btn) {
        if(appState.isGuest) { mostrarToast("Solo lectura", "info"); return; }
        
        const toSave = {};
        for (const [id, state] of Object.entries(appState.matchStates)) {
            if(state.sets && state.puntos && state.signo) {
                toSave[id] = {
                    sets: state.sets,
                    puntos: state.puntos.toString(),
                    signo: state.signo
                };
            }
        }
        
        if(Object.keys(toSave).length === 0) {
            mostrarToast("No hay predicciones completas.", "alert-circle");
            return;
        }
        
        btn.innerHTML = `<i data-lucide="loader" class="lucide-spin"></i> Guardando...`;
        lucide.createIcons();
        btn.disabled = true;
        
        try {
            const res = await fetchSeguro(SCRIPT_URL, {
                method: 'POST',
                body: JSON.stringify({ action: 'save', usuario: appState.usuario, password: appState.password, predicciones: toSave })
            });
            const d = await res.json();
            if(d.status === "success") {
                mostrarToast("Pronósticos guardados!", "check-circle");
                btn.innerHTML = `<i data-lucide="check-circle"></i> GUARDADO OK`;
                setTimeout(() => {
                    btn.innerHTML = `Guardar Mis Pronósticos`;
                    lucide.createIcons();
                    btn.disabled = false;
                }, 2000);
            } else {
                mostrarToast("Error: " + d.message, "alert-circle");
                btn.innerHTML = `Guardar Mis Pronósticos`;
                btn.disabled = false;
            }
        } catch(e) {
            mostrarToast("Error de conexión", "wifi-off");
            btn.innerHTML = `Guardar Mis Pronósticos`;
            btn.disabled = false;
        }
    }

    // --- RENDERIZADO DOM ---
    function renderPartidos(equipos) {
        const container = document.getElementById('partidos-list-container');
        if(!container) return;
        
        const upcomingMatches = equipos.filter(eq => eq.estado_partido !== "FINALIZADO" && eq.estado_partido !== "SUSPENDIDO");
        let html = "";
        
        upcomingMatches.forEach(eq => {
            const dt = new Date(eq.timestamp);
            const isDerby = eq.nombre_equipo.toUpperCase().includes("DERBY") || (eq.isDerby === true);
            const isLocked = eq.bloqueado;
            const pred = appState.predicciones[eq.id_partido];
            
            if(pred && !isLocked) {
                appState.matchStates[eq.id_partido] = {
                    sets: pred.sets,
                    puntos: parseInt(pred.puntos) || 14,
                    signo: pred.signo || '+'
                };
            } else if (!isLocked) {
                appState.matchStates[eq.id_partido] = { sets: null, puntos: 14, signo: '+' };
            }
            const state = appState.matchStates[eq.id_partido] || {};
            
            html += `
            <div class="vcv-card match-card ${isLocked ? 'is-locked' : ''}" data-category="${eq.categoria}" data-id-partido="${eq.id_partido}">
              <div class="match-header-strip">
                <span style="color: ${isDerby ? 'var(--text-gold)' : 'var(--secondary-color)'}; font-weight: 700;">
                  ${eq.categoria.toUpperCase()} ${isDerby ? '🏆 DERBY' : ''}
                </span>
                <span><i data-lucide="calendar" style="width: 12px; height: 12px; display: inline;"></i> ${dt.toLocaleDateString()} ${dt.getHours().toString().padStart(2,'0')}:${dt.getMinutes().toString().padStart(2,'0')}</span>
              </div>

              <div class="teams-versus-container">
                <div class="team-box">
                  <div class="team-avatar vcv-local">VCV</div>
                  <span class="team-name">${eq.nombre_equipo}</span>
                  <span class="team-role" style="${eq.es_local ? 'color:var(--success)' : 'color:var(--text-muted)'}">${eq.es_local ? 'LOCAL' : 'VISITANTE'}</span>
                </div>
                <div class="vs-divider">VS</div>
                <div class="team-box">
                  <div class="team-avatar">${eq.rival.substring(0,3).toUpperCase()}</div>
                  <span class="team-name">${eq.rival}</span>
                  <span class="team-role" style="${!eq.es_local ? 'color:var(--success)' : 'color:var(--text-muted)'}">${!eq.es_local ? 'LOCAL' : 'VISITANTE'}</span>
                </div>
              </div>
            `;
            
            if(isLocked) {
                html += `
                <div style="padding: 14px; background: rgba(0,0,0,0.3); border-top: 1px solid var(--border-color); text-align: center;">
                    <span style="color: var(--secondary-color); font-weight: bold; font-size: 13px;"><i data-lucide="lock" style="width: 14px; height: 14px; display:inline;"></i> PARTIDO BLOQUEADO</span>
                    <p style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">Tu pronóstico: ${pred ? pred.sets + ' (' + pred.signo + pred.puntos + ' pts)' : 'Ninguno'}</p>
                </div>
                </div>`; 
            } else {
                html += `
              <div class="sets-grid-label">
                <span>Pronóstico de Sets</span>
                <span style="color: var(--secondary-color);">+150 pts si aciertas</span>
              </div>
              <div class="sets-selector-grid" data-group="sets-${eq.id_partido}">
                ${['3-0','3-1','3-2','2-3','1-3','0-3'].map(s => 
                    `<button class="set-option-btn ${state.sets === s ? 'selected' : ''}" onclick="seleccionarSet(this, '${s}', '${eq.id_partido}')">${s}</button>`
                ).join('')}
              </div>

              <div class="points-diff-container">
                <div class="points-header">
                  <span>PUNTOS DIFERENCIAL (TANTEO)</span>
                  <span style="color: var(--text-gold);">+100 pts exacto</span>
                </div>
                <div class="points-controls-row">
                  <div class="stepper-container">
                    <button class="btn-step" onclick="cambiarPuntos('${eq.id_partido}', -1)"><i data-lucide="minus"></i></button>
                    <div class="stepper-value">
                      <span id="val-${eq.id_partido}">${state.puntos}</span>
                      <small>PTS</small>
                    </div>
                    <button class="btn-step" onclick="cambiarPuntos('${eq.id_partido}', 1)"><i data-lucide="plus"></i></button>
                  </div>
                  <div class="sign-selector">
                    <button class="sign-btn sign-plus ${state.signo === '+' ? 'selected' : ''}" id="signo-plus-${eq.id_partido}" onclick="cambiarSigno('${eq.id_partido}', this, '+')">
                      <span>+ FAVOR</span>
                    </button>
                    <button class="sign-btn sign-minus ${state.signo === '-' ? 'selected btn-danger' : ''}" id="signo-minus-${eq.id_partido}" onclick="cambiarSigno('${eq.id_partido}', this, '-')">
                      <span>- CONTRA</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>`; 
            }
        });
        
        if(upcomingMatches.length > 0) {
            html += `<button class="btn-gold" id="btn-save-predictions" onclick="guardarPronosticos(this)">Guardar Mis Pronósticos</button>`;
        } else {
            html += `<p style="text-align:center; color:var(--text-muted);">No hay partidos activos.</p>`;
        }
        
        container.innerHTML = html;
        lucide.createIcons();
    }
    
    // --- RANKING ---
    function renderRanking(clasificaciones, ligas) {
        const btnContainer = document.getElementById('ranking-leagues-container');
        if(!btnContainer) {
            // we inject a container if it doesn't exist, wait, stitch html has a container
            const p = document.querySelector('#view-ranking .vcv-card div[style*="overflow-x: auto"]');
            if(p) p.id = 'ranking-leagues-container';
        }
        const bcont = document.getElementById('ranking-leagues-container');
        
        // Render buttons for user's leagues
        if(bcont && ligas && ligas.length > 0) {
            let bHtml = "";
            ligas.forEach((liga, idx) => {
                bHtml += `<button class="btn-outline ${idx === 0 ? 'active' : ''}" onclick="cambiarLiga('${liga}', this)">${liga}</button>`;
            });
            bcont.innerHTML = bHtml;
        }

        // Render default league
        if(ligas && ligas.length > 0) {
            cambiarLiga(ligas[0], null);
        }
    }
    
    window.cambiarLiga = function(ligaName, btn) {
        if(btn) {
            const bcont = document.getElementById('ranking-leagues-container');
            if(bcont) bcont.querySelectorAll('.btn-outline').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        } else {
            const bcont = document.getElementById('ranking-leagues-container');
            if(bcont) {
                const b = bcont.querySelector(`button:nth-child(1)`);
                if(b) b.classList.add('active');
            }
        }
        
        // Render Podium and Table
        const list = appState.appData.clasificaciones[ligaName] || [];
        
        const podiumContainer = document.querySelector('.podium-container');
        if(podiumContainer) {
            let phtml = "";
            // 2nd place
            if(list.length > 1) {
                phtml += `<div class="podium-slot rank-2"><div class="podium-avatar">${list[1].usuario.substring(1,3).toUpperCase()}</div><div class="podium-bar"><span style="font-weight: 800; font-size: 0.85rem; color: #ced6e0;">2º</span><span class="player-handle">${list[1].usuario}</span><span class="player-pts">${list[1].puntos} pts</span></div></div>`;
            } else { phtml += `<div class="podium-slot rank-2"></div>`; }
            
            // 1st place
            if(list.length > 0) {
                phtml += `<div class="podium-slot rank-1"><div class="podium-avatar"><i data-lucide="crown" class="crown-icon" style="width: 22px; height: 22px;"></i>${list[0].usuario.substring(1,3).toUpperCase()}</div><div class="podium-bar"><span style="font-weight: 800; font-size: 1rem; color: var(--text-gold);">1º</span><span class="player-handle" style="color:var(--text-gold);">${list[0].usuario}</span><span class="player-pts">${list[0].puntos} pts</span></div></div>`;
            }
            
            // 3rd place
            if(list.length > 2) {
                phtml += `<div class="podium-slot rank-3"><div class="podium-avatar">${list[2].usuario.substring(1,3).toUpperCase()}</div><div class="podium-bar"><span style="font-weight: 800; font-size: 0.75rem; color: #cd7f32;">3º</span><span class="player-handle">${list[2].usuario}</span><span class="player-pts">${list[2].puntos} pts</span></div></div>`;
            } else { phtml += `<div class="podium-slot rank-3"></div>`; }
            
            podiumContainer.innerHTML = phtml;
            lucide.createIcons();
        }
        
        const tbody = document.getElementById('ranking-list-body');
        if(tbody) {
            let html = "";
            list.slice(3).forEach((usr, idx) => { // starting from 4th place
                const isMe = (usr.usuario.toLowerCase() === appState.usuario.toLowerCase());
                let trClass = "ranking-row";
                html += `
                <tr class="${trClass}">
                  <td style="text-align: center; font-weight: 800; color: var(--text-muted);">${idx + 4}</td>
                  <td>
                    <div class="user-badge" style="${isMe ? 'border: 2px solid var(--secondary-color); background: rgba(212,175,55,0.1);' : ''}">
                      <span class="user-avatar">${usr.usuario.substring(1,3).toUpperCase()}</span>
                      <span class="user-name">${usr.usuario} ${isMe ? '(TÚ)' : ''}</span>
                    </div>
                  </td>
                  <td style="text-align: right; font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: var(--text-main); font-size: 16px;">
                    ${usr.puntos}
                  </td>
                </tr>
                `;
            });
            tbody.innerHTML = html;
        }
    }
    
    // --- HISTORIAL ---
    function renderHistorial(todos) {
        // Find historial container. Prototipo stitch might not have a specific div, we can inject into view-historial
        const view = document.getElementById('view-historial');
        if(!view) return;
        
        // Check if there's a list container, else append
        let listCont = document.getElementById('historial-list-container');
        if(!listCont) {
            listCont = document.createElement('div');
            listCont.id = 'historial-list-container';
            listCont.style.display = 'flex';
            listCont.style.flexDirection = 'column';
            listCont.style.gap = '10px';
            view.appendChild(listCont);
        }
        
        let sorted = [...todos].filter(p => p.estado_partido === "FINALIZADO");
        sorted.sort((a,b) => b.timestamp - a.timestamp);
        
        let html = "<h3 style='margin-top:15px; margin-bottom:5px;'>Partidos Finalizados</h3>";
        
        if(sorted.length === 0) {
            html += "<p style='color:var(--text-muted)'>No hay historial todavía.</p>";
        }
        
        sorted.forEach(p => {
            const pred = appState.predicciones[p.id_partido];
            let predStr = pred ? `${pred.sets} (${pred.signo}${pred.puntos} pts)` : 'Sin pronóstico';
            let resStr = p.oficial_sets ? `${p.oficial_sets} (${p.oficial_signo || ''}${p.oficial_puntos} pts)` : 'Faltan datos oficiales';
            
            html += `
            <div style="background: var(--bg-card-alt); border: 1px solid var(--border-color); border-radius: 12px; padding: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--secondary-color); font-weight: 700; margin-bottom: 8px;">
                  <span>JORNADA ${p.ronda}</span>
                  <span><i data-lucide="check-circle" style="width: 12px; height: 12px; display: inline;"></i> FINALIZADO</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="font-weight:bold; font-size:0.9rem;">${p.equipo_local}</div>
                    <div style="background:var(--primary-color); padding: 4px 8px; border-radius:6px; font-family:'Space Grotesk',sans-serif; font-weight:bold;">${p.oficial_sets || '? - ?'}</div>
                    <div style="font-weight:bold; font-size:0.9rem;">${p.rival}</div>
                </div>
                <div style="font-size: 0.8rem; color: var(--text-muted); background: var(--bg-card); padding:8px; border-radius:6px;">
                    <div style="margin-bottom:4px;">Tu pronóstico: <strong style="color:white">${predStr}</strong></div>
                    <div>Resultado Oficial: <strong style="color:white">${resStr}</strong></div>
                </div>
            </div>
            `;
        });
        
        listCont.innerHTML = html;
        lucide.createIcons();
    }
    
    // --- CALENDARIO ---
    function renderCalendario(todos) {
        const view = document.getElementById('view-calendario');
        if(!view) return;
        
        let listCont = document.getElementById('calendario-list-container');
        if(!listCont) {
            // Find the vcv-card inside view-calendario
            const card = view.querySelector('.vcv-card');
            if(card) {
                // remove existing static children if we inject dynamically
                const staticList = card.querySelector('div[style*="flex-direction: column"]');
                if(staticList) staticList.remove();
                
                listCont = document.createElement('div');
                listCont.id = 'calendario-list-container';
                listCont.style.display = 'flex';
                listCont.style.flexDirection = 'column';
                listCont.style.gap = '10px';
                card.appendChild(listCont);
            }
        }
        if(!listCont) return;
        
        let sorted = [...todos].filter(p => p.estado_partido !== "FINALIZADO");
        sorted.sort((a,b) => a.timestamp - b.timestamp);
        
        let html = "";
        sorted.forEach(p => {
            const dt = new Date(p.timestamp);
            html += `
            <div style="background: var(--bg-card-alt); border: 1px solid var(--border-color); border-radius: 12px; padding: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--secondary-color); font-weight: 700; margin-bottom: 4px;">
                  <span>JORNADA ${p.ronda} • ${p.categoria}</span>
                  <span>${dt.toLocaleDateString()} • ${dt.getHours().toString().padStart(2,'0')}:${dt.getMinutes().toString().padStart(2,'0')}</span>
                </div>
                <div style="font-weight: 700; font-size: 0.92rem;">${p.equipo_local} vs ${p.rival}</div>
                <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 2px;">
                  <i data-lucide="map-pin" style="width: 12px; height: 12px; display: inline;"></i> ${p.es_local ? 'Local' : 'Visitante'}
                </div>
            </div>
            `;
        });
        
        listCont.innerHTML = html;
        lucide.createIcons();
    }
  </script>
</body>
</html>
"""

# Replace the script block entirely
js_start = html_content.rfind('<script>')
if js_start != -1:
    html_without_js = html_content[:js_start]
    final_v2 = html_without_js + new_js
    
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(final_v2)
    print("Injected comprehensive Apps Script logic into v2.html")
else:
    print("Could not find <script> tag in prototipo_stitch.html")
