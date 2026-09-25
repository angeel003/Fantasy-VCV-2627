import re

with open('prototipo_stitch.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# The JS we want to inject
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
      matchStates: {} // To store the interactive states: matchStates[id] = {sets, puntos, signo}
    };
    
    let appData = null; // Store full server response

    // INICIALIZACIÓN
    document.addEventListener("DOMContentLoaded", () => {
      lucide.createIcons();
      // Show login modal on load
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
          appData = data;
          
          document.getElementById('login-modal').classList.remove('show');
          
          // Set UI Globals
          document.getElementById('display-user-handle').innerText = u;
          const ptsObj = data.clasificaciones && data.clasificaciones['Liga General VCV'] ? data.clasificaciones['Liga General VCV'].find(x => x.usuario.toLowerCase() === u.toLowerCase()) : null;
          appState.puntosTotales = ptsObj ? ptsObj.puntos : 0;
          document.getElementById('display-user-pts').innerText = appState.puntosTotales + " pts";
          
          const adminPanel = document.getElementById('intranet-admin-panel');
          if (adminPanel) adminPanel.style.display = appState.isAdmin ? 'block' : 'none';
          
          // Initialize match states from my previous predictions
          await loadPredicciones();
          
          // Render views
          renderPartidos(data.equipos || []);
          renderRanking(data.clasificaciones || {});
          renderHistorial(data.todos_partidos || []);
          
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
        // We could fetch public data here if we had a public endpoint
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
        if(appState.isGuest) return;
        
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
            mostrarToast("No hay predicciones completas para guardar.", "alert-circle");
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
                mostrarToast("Predicciones guardadas correctamente!", "check-circle");
                btn.innerHTML = `<i data-lucide="check-circle"></i> GUARDADO OK`;
                setTimeout(() => {
                    btn.innerHTML = `<i data-lucide="save"></i> GUARDAR PRONÓSTICOS`;
                    lucide.createIcons();
                    btn.disabled = false;
                }, 2000);
            } else {
                mostrarToast("Error: " + d.message, "alert-circle");
                btn.innerHTML = `<i data-lucide="save"></i> GUARDAR PRONÓSTICOS`;
                lucide.createIcons();
                btn.disabled = false;
            }
        } catch(e) {
            mostrarToast("Error de conexión", "wifi-off");
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
                </div>`; // Close card
            } else {
                html += `
              <!-- Selector de Sets -->
              <div class="sets-grid-label">
                <span>Pronóstico de Sets</span>
                <span style="color: var(--secondary-color);">+150 pts si aciertas</span>
              </div>
              <div class="sets-selector-grid" data-group="sets-${eq.id_partido}">
                ${['3-0','3-1','3-2','2-3','1-3','0-3'].map(s => 
                    `<button class="set-option-btn ${state.sets === s ? 'selected' : ''}" onclick="seleccionarSet(this, '${s}', '${eq.id_partido}')">${s}</button>`
                ).join('')}
              </div>

              <!-- Selector de Puntos Diferencial y Signo -->
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
            </div>`; // Close card
            }
        });
        
        container.innerHTML = html;
        lucide.createIcons();
    }
    
    function renderRanking(clasificaciones) {
        const tbody = document.getElementById('ranking-list-body');
        if(!tbody) return;
        
        // Show Liga General by default
        const list = clasificaciones['Liga General VCV'] || [];
        let html = "";
        
        list.slice(0, 15).forEach((usr, idx) => {
            const isMe = (usr.usuario.toLowerCase() === appState.usuario.toLowerCase());
            let trClass = "ranking-row";
            if(idx === 0) trClass += " top-1";
            else if(idx === 1) trClass += " top-2";
            else if(idx === 2) trClass += " top-3";
            
            html += `
            <tr class="${trClass}">
              <td style="text-align: center; font-weight: 800; color: ${idx<3 ? 'var(--secondary-color)' : 'var(--text-muted)'};">${idx + 1}</td>
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
    
    function renderHistorial(todos) {
        // Implement simple render based on finished matches for the user
        // (Skipping full render for brevity in POC, it's easily extensible)
    }

  </script>
</body>
</html>
"""

# Find JS block and replace
js_start = html_content.rfind('<script>')
if js_start != -1:
    html_without_js = html_content[:js_start]
    final_v2 = html_without_js + new_js
    
    # Save directly to v2.html
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(final_v2)
    print("Injected real Apps Script logic into prototipo_stitch.html and saved to v2.html")
else:
    print("Could not find <script> tag in prototipo_stitch.html")
