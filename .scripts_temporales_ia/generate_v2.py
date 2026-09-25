import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. CSS
new_css = """
  <!-- NEW V2 STYLES PARA CARTELERA Y LOGIN -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    :root {
      --bg-card: #ffffff;
      --bg-card-alt: #f9fafb;
      --primary-color: #783b7a;
      --secondary-color: #bd9b53;
      --text-main: #1f2937;
      --text-muted: #6b7280;
      --text-gold: #b48c36;
      --success: #059669;
      --danger: #dc2626;
      --border-color: #e5e7eb;
    }

    /* LOGIN STYLES */
    #loginSection {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
      flex-direction: column;
      background: var(--bg-card-alt);
      min-height: 80vh;
    }
    .modal-card-v2 {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 20px;
      padding: 24px;
      width: 100%;
      max-width: 360px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.08);
      position: relative;
      margin-bottom: 40px;
    }
    .club-crest-v2 {
      background: var(--primary-color);
      color: var(--secondary-color);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .btn-gold-v2 {
      background: linear-gradient(135deg, var(--secondary-color) 0%, #d4af37 100%);
      color: #fff;
      border: none;
      border-radius: 12px;
      padding: 14px;
      font-weight: 800;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }
    .btn-outline-v2 {
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      border-radius: 12px;
      padding: 10px;
      font-weight: 700;
      font-size: 0.85rem;
      cursor: pointer;
    }

    /* CARTELERA STYLES */
    .vcv-card-v2 {
      background: var(--bg-card);
      border-radius: 16px;
      padding: 16px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.06);
      border: 1px solid var(--border-color);
      position: relative;
      overflow: hidden;
      margin-bottom: 20px;
    }
    .match-header-strip-v2 {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.75rem;
      margin-bottom: 14px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(0,0,0,0.05);
      color: var(--text-muted);
    }
    .teams-versus-container-v2 {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }
    .team-box-v2 {
      display: flex;
      flex-direction: column;
      align-items: center;
      flex: 1;
      text-align: center;
    }
    .team-avatar-v2 {
      width: 52px;
      height: 52px;
      border-radius: 14px;
      background: var(--bg-card-alt);
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 900;
      font-size: 1.1rem;
      color: var(--text-main);
      margin-bottom: 8px;
    }
    .team-avatar-v2.vcv-local {
      background: var(--primary-color);
      color: var(--secondary-color);
      border: 1px solid var(--secondary-color);
    }
    .team-name-v2 {
      font-weight: 700;
      font-size: 0.95rem;
      color: var(--text-main);
      line-height: 1.1;
      margin-bottom: 4px;
    }
    .team-role-v2 {
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.5px;
    }
    .vs-divider-v2 {
      font-weight: 900;
      font-size: 1rem;
      color: var(--text-muted);
      opacity: 0.4;
      padding: 0 10px;
    }
    .sets-grid-label-v2 {
      display: flex;
      justify-content: space-between;
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .sets-selector-grid-v2 {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 6px;
      margin-bottom: 16px;
    }
    .set-option-btn-v2 {
      background: var(--bg-card-alt);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      border-radius: 8px;
      padding: 10px 0;
      font-weight: 700;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .set-option-btn-v2.selected {
      background: var(--secondary-color);
      color: #fff;
      border-color: var(--secondary-color);
      box-shadow: 0 4px 12px rgba(189, 155, 83, 0.3);
      transform: translateY(-2px);
    }
    .points-diff-container-v2 {
      background: var(--bg-card-alt);
      border-radius: 12px;
      padding: 14px;
      border: 1px solid var(--border-color);
    }
    .points-header-v2 {
      display: flex;
      justify-content: space-between;
      font-size: 0.7rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 10px;
    }
    .points-controls-row-v2 {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .stepper-container-v2 {
      display: flex;
      align-items: center;
      background: var(--bg-card);
      border-radius: 10px;
      padding: 4px;
      border: 1px solid var(--border-color);
    }
    .btn-step-v2 {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      border: none;
      background: rgba(120, 59, 122, 0.1);
      color: var(--primary-color);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    .stepper-value-v2 {
      min-width: 46px;
      text-align: center;
    }
    .stepper-value-v2 span {
      font-weight: 900;
      font-size: 1.3rem;
      color: var(--secondary-color);
    }
    .stepper-value-v2 small {
      display: block;
      font-size: 0.55rem;
      font-weight: 700;
      color: var(--text-muted);
      margin-top: -2px;
    }
    .sign-selector-v2 {
      display: flex;
      gap: 6px;
      flex: 1;
    }
    .sign-btn-v2 {
      flex: 1;
      border-radius: 10px;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      color: var(--text-muted);
      font-weight: 700;
      font-size: 0.75rem;
      padding: 10px 0;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
    }
    .sign-btn-v2.selected.sign-plus-v2 {
      background: var(--primary-color);
      color: var(--secondary-color);
      border-color: var(--primary-color);
    }
    .sign-btn-v2.selected.sign-minus-v2 {
      background: rgba(220, 38, 38, 0.1);
      color: var(--danger);
      border-color: rgba(220, 38, 38, 0.3);
    }
  </style>
"""
text = text.replace('</head>', new_css + '\n</head>')


# 2. Login Replacement: ONLY replacing the <div class="login-card"> inside <div id="loginSection">
old_card_pattern = r'<div class="login-card">.*?</div>\s*<div class="faq-container">'
# Wait, this regex is greedy. Let's just find exactly.
start_card = text.find('<div class="login-card">')
end_card = text.find('<div class="faq-container">', start_card)

new_login_card_html = """<div class="modal-card-v2">
        <div style="text-align: center; margin-bottom: 18px;">
          <div class="club-crest-v2" style="margin: 0 auto 12px; width: 52px; height: 52px;">
            <i data-lucide="shield" style="width: 30px; height: 30px;"></i>
          </div>
          <h2 style="font-size: 1.3rem; font-weight: 800; color:var(--text-main); margin-bottom:4px;">Fantasy VCV 26/27</h2>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">Acceso oficial para jugadores y socios</p>
        </div>

        <div>
          <div class="form-group text-left" style="margin-bottom:10px;">
            <label style="font-size:0.85rem; font-weight:600;">Usuario</label>
            <input type="text" id="loginUsuario" class="form-control" placeholder="@tu_usuario" required>
          </div>
          <div class="form-group text-left" style="margin-bottom:10px;">
            <label style="font-size:0.85rem; font-weight:600;">Contraseña</label>
            <input type="password" id="loginPassword" class="form-control" placeholder="••••••••" required>
          </div>

          <button id="btnLogin" class="btn-gold-v2" style="margin-top: 14px;">
            <span>Entrar al Fantasy</span>
          </button>
        </div>

        <button id="btnGuest" class="btn-outline-v2" style="width: 100%; margin-top: 10px;">
          👀 Entrar como Invitado (Solo Lectura)
        </button>
        
        <div id="loginMessage" class="alert-box" style="margin-top:10px; display:none;"></div>
    </div>

    <div class="faq-container">"""

text = text[:start_card] + new_login_card_html + text[end_card+len('<div class="faq-container">'):]


# 3. Interactive JS
interactive_js = """
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
      if (hiddenInput && valSpan) {
          let current = parseInt(hiddenInput.value) || 14; 
          let next = current + delta;
          if (next < 1) next = 1; 
          hiddenInput.value = next;
          valSpan.innerText = next;
      }
    }
    
    function cambiarSignoV2(matchId, btn, val) {
      const hiddenInput = document.getElementById('e' + matchId + '_signo');
      if (hiddenInput) {
          hiddenInput.value = val === '+' ? 'A favor' : 'En contra';
      }
      const plusBtn = document.getElementById('signo-plus-v2-' + matchId);
      const minusBtn = document.getElementById('signo-minus-v2-' + matchId);
      if(plusBtn) plusBtn.classList.remove('selected');
      if(minusBtn) minusBtn.classList.remove('selected');
      
      btn.classList.add('selected');
    }
</script>
"""
text = text.replace('</body>', interactive_js + '\n</body>')


# 4. Cartelera Match Cards
start_match = text.find('if (eq.estado === "ABIERTO") {')
end_match = text.find('} else if (eq.estado === "CERRADO") {', start_match)

new_card_html = r"""if (eq.estado === "ABIERTO") {
                        let dt = new Date(eq.timestamp);
                        let fechaFormateada = isNaN(dt) ? "" : `${dt.toLocaleDateString()} ${dt.getHours().toString().padStart(2,'0')}:${dt.getMinutes().toString().padStart(2,'0')}`;

                        setTimeout(() => { if(window.lucide) lucide.createIcons(); }, 100);

                        htmlPartidos += `
                        <div class="vcv-card-v2" data-category="${eq.categoria}">
                            <div class="match-header-strip-v2">
                                <span style="color: ${eq.es_derby ? 'var(--text-gold)' : 'var(--secondary-color)'}; font-weight: 800;">
                                  ${eq.categoria.toUpperCase()} ${eq.es_derby ? '🏆 DERBY' : ''}
                                </span>
                                <span><i data-lucide="calendar" style="width: 12px; height: 12px; display: inline; vertical-align: middle; margin-top:-2px;"></i> ${fechaFormateada}</span>
                            </div>

                            <div class="teams-versus-container-v2">
                                <div class="team-box-v2">
                                  <div class="team-avatar-v2 ${eq.es_local ? 'vcv-local' : ''}">${eq.es_local ? 'VCV' : eq.equipo_local.substring(0,3).toUpperCase()}</div>
                                  <span class="team-name-v2">${eq.equipo_local}</span>
                                  <span class="team-role-v2" style="color: ${eq.es_local ? 'var(--success)' : 'var(--text-muted)'}">${eq.es_local ? 'LOCAL' : 'VISITANTE'}</span>
                                </div>
                                <div class="vs-divider-v2">VS</div>
                                <div class="team-box-v2">
                                  <div class="team-avatar-v2 ${!eq.es_local ? 'vcv-local' : ''}">${!eq.es_local ? 'VCV' : eq.rival.substring(0,3).toUpperCase()}</div>
                                  <span class="team-name-v2">${eq.rival}</span>
                                  <span class="team-role-v2" style="color: ${!eq.es_local ? 'var(--success)' : 'var(--text-muted)'}">${!eq.es_local ? 'LOCAL' : 'VISITANTE'}</span>
                                </div>
                            </div>
                            
                            <div class="reloj-partido" data-ts="${eq.timestamp}" data-eq="${eq.id_partido}" style="font-size:0.75rem; font-weight:bold; padding:4px 8px; background:#fff3cd; color:#856404; border-radius:4px; display:inline-block; margin-bottom:12px;">Calculando tiempo...</div>

                            <!-- HIDDEN INPUTS -->
                            <input type="hidden" id="e${eq.id_partido}_sets" value="">
                            <input type="hidden" id="e${eq.id_partido}_puntos" value="14">
                            <input type="hidden" id="e${eq.id_partido}_signo" value="">

                            <div class="inputs-eq" id="inputs_eq_${eq.id_partido}">
                                <div class="sets-grid-label-v2">
                                  <span>Pronóstico de Sets</span>
                                  <span style="color: var(--secondary-color);">+150 pts si aciertas</span>
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
                                    <span>PUNTOS DIFERENCIAL</span>
                                    <span style="color: var(--text-gold);">+100 pts exacto</span>
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
                                      <button type="button" class="sign-btn-v2 sign-plus-v2" id="signo-plus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, '+')">
                                        <span>+ FAVOR</span>
                                      </button>
                                      <button type="button" class="sign-btn-v2 sign-minus-v2" id="signo-minus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, '-')">
                                        <span>- CONTRA</span>
                                      </button>
                                    </div>
                                  </div>
                                </div>
                            </div>
                            
                            ${destacadoHtml}
                        </div>`;
"""
text = text[:start_match] + new_card_html + text[end_match:]


# 5. Sync Loop
old_loop_pattern = r'for\(var idPart in preds\) \{\s*setVal\(`e\$\{idPart\}_sets`, preds\[idPart\]\.sets\);\s*setVal\(`e\$\{idPart\}_puntos`, preds\[idPart\]\.puntos\);\s*setVal\(`e\$\{idPart\}_signo`, preds\[idPart\]\.signo\);\s*\}'
new_loop_block = r"""for(var idPart in preds) {
                setVal(`e${idPart}_sets`, preds[idPart].sets);
                setVal(`e${idPart}_puntos`, preds[idPart].puntos);
                setVal(`e${idPart}_signo`, preds[idPart].signo);
                
                // --- V2 UI Sync ---
                if (preds[idPart].sets) {
                    const btn = document.querySelector(`button[onclick*="seleccionarSetV2(this, '${preds[idPart].sets}', '${idPart}')"]`);
                    if (btn) btn.classList.add('selected');
                }
                if (preds[idPart].puntos) {
                    const span = document.getElementById(`val-v2-${idPart}`);
                    if (span) span.innerText = preds[idPart].puntos;
                }
                if (preds[idPart].signo) {
                    const signoVal = preds[idPart].signo;
                    if (signoVal === "A favor") {
                        const btn = document.getElementById(`signo-plus-v2-${idPart}`);
                        if (btn) btn.classList.add('selected');
                    } else if (signoVal === "En contra") {
                        const btn = document.getElementById(`signo-minus-v2-${idPart}`);
                        if (btn) btn.classList.add('selected');
                    }
                }
            }"""
text = re.sub(old_loop_pattern, new_loop_block, text)


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("v2.html fixed for REAL (kept FAQ so JS doesn't crash)!")
