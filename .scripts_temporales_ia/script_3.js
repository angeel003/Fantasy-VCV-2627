
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
            btn.innerText = '${isPredicted ? "Modificar Predicción" : "Guardar Predicción"}';
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

            // OPTIMISTIC UI UPDATE
            const selectedSignBtn = document.querySelector(`#signo-plus-v2-${idPart}.selected`) || document.querySelector(`#signo-minus-v2-${idPart}.selected`);
            let signText = selectedSignBtn ? selectedSignBtn.innerText : (sig === 'Empate' ? 'Empate' : sig);
            if(p == 0) signText = "Empate";
            
            let ptsText = signText === 'A favor (+)' ? 'a favor' : (signText === 'En contra (-)' ? 'en contra' : '');
            let formStr = ptsText ? `(+${p} pts ${ptsText})` : `(${p} pts)`;
            if(p==0) formStr = `(0 pts)`;
            document.getElementById('summary-text-' + idPart).innerHTML = `<span style="font-weight:normal; color:var(--text-muted);">Predicción configurada:</span><br><b style="font-size:1.1rem; color:var(--text-main);">${s}</b> <span style="color:var(--primary-color); font-weight:800;">${formStr}</span>`;

            card.classList.add('collapsed');
            inputs.style.display = 'none';
            summary.style.display = 'block';
            
            const oldBtnHtml = btn.innerHTML;
            btn.innerHTML = 'Guardando... <span class="spinner-border spinner-border-sm" style="width:12px;height:12px;border-width:2px;margin-left:5px;"></span>';
            btn.style.background = 'transparent';
            btn.style.color = 'var(--text-muted)';
            btn.style.border = '1px solid var(--border-color)';
            btn.disabled = true;

            let singlePred = {};
            singlePred[idPart] = { sets: s, puntos: p, signo: sig };

            window.fetchSeguro(window.scriptURL, {
                method: 'POST',
                body: JSON.stringify({ action: 'guardar', usuario: window.currentUser, password: window.currentPassword, predicciones: singlePred }),
                headers: { 'Content-Type': 'text/plain;charset=utf-8' }
            }).then(res => res.json()).then(data => {
                if(data.status === "success") {
                    btn.disabled = false;
                    btn.innerText = 'Modificar Predicción';
                } else {
                    alert('Error al guardar: ' + data.message);
                    card.classList.remove('collapsed');
                    summary.style.display = 'none';
                    inputs.style.display = 'block';
                    btn.innerHTML = oldBtnHtml;
                    btn.style.background = 'var(--secondary-color)';
                    btn.style.color = '#000';
                    btn.style.border = 'none';
                    btn.disabled = false;
                }
            }).catch(err => {
                alert('Error de conexión.');
                card.classList.remove('collapsed');
                summary.style.display = 'none';
                inputs.style.display = 'block';
                btn.innerHTML = oldBtnHtml;
                btn.style.background = 'var(--secondary-color)';
                btn.style.color = '#000';
                btn.style.border = 'none';
                btn.disabled = false;
            });
        }
    }
