import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update logo to square/rounded
text = text.replace(
    '<img src="files/images/logo_vcv_circle.png" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">',
    '<img src="files/images/logo_vcv_rounded.png" style="width:100%;height:100%;object-fit:contain;border-radius:14px;">'
)

# 2. Update points selector logic (allow 0, disable buttons if 0, yellow background if tied)
js_points_logic = """
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
"""
text = re.sub(r'function cambiarPuntosV2\([^\{]+\{[\s\S]*?\n    \}', js_points_logic, text)

css_tied_btn = """
    .tied-btn {
        background: var(--secondary-color) !important;
        color: #000 !important;
        border-color: var(--secondary-color) !important;
        opacity: 0.7;
    }
"""
text = text.replace('</style>', css_tied_btn + '\n  </style>')


# 3. Fix the Sign buttons HTML (use Team Names instead of "+ Favor / - Contra")
old_sign_buttons = r"""<div class="sign-selector-v2">
                                      <button type="button" class="sign-btn-v2 sign-plus-v2" id="signo-plus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, '+')">
                                        <span>+ FAVOR</span>
                                      </button>
                                      <button type="button" class="sign-btn-v2 sign-minus-v2" id="signo-minus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, '-')">
                                        <span>- CONTRA</span>
                                      </button>
                                    </div>"""

new_sign_buttons = r"""<div class="sign-selector-v2">
                                      <button type="button" class="sign-btn-v2 sign-plus-v2" id="signo-plus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, ${localIsVcv})">
                                        <span>${localTeamName.substring(0,10)}</span>
                                      </button>
                                      <button type="button" class="sign-btn-v2 sign-minus-v2" id="signo-minus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, ${visitIsVcv})">
                                        <span>${visitTeamName.substring(0,10)}</span>
                                      </button>
                                    </div>"""
text = text.replace(old_sign_buttons, new_sign_buttons)

# 4. Update cambiarSignoV2 logic
old_cambiarSigno = r"""function cambiarSignoV2(matchId, btn, val) {
      const hiddenInput = document.getElementById('e' + matchId + '_signo');
      if (hiddenInput) {
          hiddenInput.value = val === '+' ? 'A favor' : 'En contra';
      }
      const plusBtn = document.getElementById('signo-plus-v2-' + matchId);
      const minusBtn = document.getElementById('signo-minus-v2-' + matchId);
      if(plusBtn) plusBtn.classList.remove('selected');
      if(minusBtn) minusBtn.classList.remove('selected');
      
      btn.classList.add('selected');
    }"""
new_cambiarSigno = r"""function cambiarSignoV2(matchId, btn, isVcv) {
      const hiddenInput = document.getElementById('e' + matchId + '_signo');
      if (hiddenInput) {
          hiddenInput.value = isVcv ? 'A favor' : 'En contra';
      }
      const plusBtn = document.getElementById('signo-plus-v2-' + matchId);
      const minusBtn = document.getElementById('signo-minus-v2-' + matchId);
      if(plusBtn) plusBtn.classList.remove('selected');
      if(minusBtn) minusBtn.classList.remove('selected');
      
      btn.classList.add('selected');
    }"""
text = text.replace(old_cambiarSigno, new_cambiarSigno)


# 5. Overwrite iniciarRelojes for cohesive styling
new_relojes = """function iniciarRelojes() {
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
                        inputs.style.opacity = '0.5';
                        inputs.style.pointerEvents = 'none';
                    }
                    applyStyle('rgba(231,76,60,0.1)', red, " PREDICCIONES CERRADAS");
                } else if (diff <= -14400000) {
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
}"""
text = re.sub(r'function iniciarRelojes\(\) \{[\s\S]*?\}, 1000\);\s*\}', new_relojes, text)

# Lastly, adjust summary text to use actual team names instead of "+" / "-"
# In handleSaveOrModifyV2: 
# `${s} | ${p} pts | ${sig === 'A favor' ? '+' : '-'}` 
# -> We want it to be the team name. But in that scope we don't have localTeamName easily unless we read it from the button.
# Let's just find the button that is selected.
old_summary = "document.getElementById('summary-text-' + idPart).innerText = `${s} | ${p} pts | ${sig === 'A favor' ? '+' : '-'}`;"
new_summary = """
                    const selectedSignBtn = document.querySelector(`#signo-plus-v2-${idPart}.selected`) || document.querySelector(`#signo-minus-v2-${idPart}.selected`);
                    let signText = selectedSignBtn ? selectedSignBtn.innerText : (sig === 'Empate' ? 'Empate' : sig);
                    if(p == 0) signText = "Empate";
                    document.getElementById('summary-text-' + idPart).innerText = `${s} | ${p} pts | ${signText}`;
"""
text = text.replace(old_summary, new_summary)


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated v2.html with squares, team names on points, point 0 logic, and timer styling.")
