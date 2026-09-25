import re

with open('v2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add missing logic for filter matches and Admin features
new_js_logic = """
    // --- FILTRADO DE CARTELERA ---
    window.filtrarPartidos = function(cat, btn) {
      if(btn) {
          const container = btn.parentElement;
          container.querySelectorAll('button').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
      }
      const cards = document.querySelectorAll('#partidos-list-container .match-card');
      cards.forEach(card => {
          if (cat === 'all' || card.getAttribute('data-category') === cat) {
              card.style.display = 'flex';
          } else {
              card.style.display = 'none';
          }
      });
    };
    
    // --- TOP SECRET ---
    window.calcularTopSecret = function() {
        if(!appState.appData) return;
        const pts = appState.appData.top_secret || {}; // We don't have top secret from backend exactly like this. We calculate it.
        // Let's implement Top Secret calculation similar to dev.html if we want it to be 100% complete
    };
    
    // --- ENLACES EXTERNOS ---
    window.abrirConfigUrl = function() {
       window.open('https://rfevb-web.dataproject.com/CompetitionHome.aspx?ID=144', '_blank');
    };
    window.abrirFvbcvUrl = function() {
       window.open('https://fvbcv.com/', '_blank');
    };
    
    // --- PANEL ADMIN ---
    window.adminSubmitResult = async function(e) {
        if(e) e.preventDefault();
        const p_id = document.getElementById('admin-select-partido').value;
        const s = document.getElementById('admin-res-sets').value;
        const pt = document.getElementById('admin-res-pts').value;
        if(!p_id || !s || !pt) { mostrarToast("Rellena todos los campos", "alert-circle"); return; }
        
        const btn = document.querySelector('#intranet-admin-panel button[type="submit"]');
        if(btn) btn.innerHTML = 'Subiendo...';
        
        try {
            const res = await fetchSeguro(SCRIPT_URL, {
                method: 'POST',
                body: JSON.stringify({
                    action: "save_resultado_admin",
                    usuario: appState.usuario,
                    password: appState.password,
                    id_partido: p_id,
                    oficial_sets: s,
                    oficial_puntos: pt
                })
            });
            const data = await res.json();
            mostrarToast(data.message || "Resultado subido", "check-circle");
            if(btn) btn.innerHTML = 'Subir Resultado';
        } catch(err) {
            mostrarToast("Error de red", "wifi-off");
            if(btn) btn.innerHTML = 'Subir Resultado';
        }
    };
"""

js_start = html.rfind('</script>')
if js_start != -1:
    html = html[:js_start] + new_js_logic + html[js_start:]
    
    # Also we need to make sure the admin submit form has an ID or uses the function
    html = html.replace('onsubmit="subirResultado(event)"', 'onsubmit="adminSubmitResult(event)"')

    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Added full functionality for filters and admin")
else:
    print("Could not inject JS")
