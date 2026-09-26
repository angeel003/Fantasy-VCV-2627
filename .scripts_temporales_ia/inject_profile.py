import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace HTML
target_html = r'<h2 id="tituloPrincipalSeccion">🏐 Cartelera de Partidos</h2>\s*<p style="color:#555; margin-bottom:20px; font-weight: 500; font-size: 0\.95rem;">Predice los resultados de tus equipos favoritos esta jornada\.</p>'
new_html = r'<div id="perfilUsuarioTop"></div>'

text = re.sub(target_html, new_html, text)

# 2. Inject JS
target_js = r'(currentUser = usr; currentPassword = pwd;\s*)(let promoDiv2 = document\.getElementById\(\'guestPromoBanner\'\);)'

new_js = r"""\1
            let totalOpen = 0;
            let predictedOpen = 0;
            if (data.equipos && data.equipos.length > 0) {
                data.equipos.forEach(eq => {
                    if (eq.estado !== "CERRADO") {
                        totalOpen++;
                        if (data.predicciones_usuario && data.predicciones_usuario[eq.id_partido]) { predictedOpen++; }
                    }
                });
            }
            let porcentaje = totalOpen > 0 ? Math.round((predictedOpen / totalOpen) * 100) : 100;
            
            let myBadges = data.insignias ? (data.insignias[currentUser] || []) : [];
            let insigniasHTML = "";
            if (myBadges.length > 0) {
                insigniasHTML += `<div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:8px;">`;
                myBadges.forEach(b => {
                    let cssColorClass = getBadgeCSS(b.type);
                    insigniasHTML += `<div style="display:inline-flex; align-items:center; gap:4px; font-size:0.7rem; padding:2px 6px; border-radius:4px; background:var(--bg-general); border:1px solid var(--border-color);"><img src="${URL_BADGE_GENERIC}" class="badge-icon ${cssColorClass}" style="width:12px; height:12px;"><span style="color:var(--text-muted); font-weight:600;">${b.text}</span></div>`;
                });
                insigniasHTML += `</div>`;
            }

            let htmlPerfil = `
            <div style="padding: 16px; border-radius: 16px; background: linear-gradient(to right, rgba(93, 23, 137, 0.4), var(--bg-card), var(--bg-card)); border: 1px solid var(--border-color); position: relative; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); margin-bottom: 20px;">
              <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.75rem; margin-bottom: 12px;">
                <span style="display: inline-flex; align-items: center; font-weight: bold; padding: 3px 10px; border-radius: 9999px; background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3);">
                  <span style="width: 6px; height: 6px; border-radius: 9999px; background: #10b981; margin-right: 6px; animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;"></span> Jornada ${data.jornada || "Activa"}
                </span>
                <span style="display: flex; align-items: center; color: var(--vcv-dorado); font-weight: 700;">
                  <span style="margin-right: 4px;">🎯</span> ${predictedOpen}/${totalOpen} Predicciones
                </span>
              </div>
              
              <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                <div>
                  <h2 style="font-size: 1.15rem; font-weight: bold; color: var(--text-main); margin:0;">Pronósticos del Club</h2>
                  <p style="font-size: 0.8rem; color: var(--text-muted); margin: 4px 0 0 0;">
                    Jugador: <span style="color: var(--vcv-dorado); font-weight: 700;">@${currentUser}</span> • ${data.nombre_real !== currentUser ? data.nombre_real : '¡Demuestra quién sabe más!'}
                  </p>
                  ${insigniasHTML}
                </div>
                <span style="font-size: 0.8rem; font-weight: bold; color: var(--vcv-dorado); background: rgba(212, 175, 55, 0.1); padding: 4px 8px; border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.3); white-space: nowrap; margin-left:10px;">${porcentaje}% Listo</span>
              </div>

              <div style="width: 100%; background: rgba(0, 0, 0, 0.15); border-radius: 9999px; height: 6px; margin-top: 14px; overflow: hidden;">
                <div style="background: linear-gradient(to right, var(--vcv-morado), var(--vcv-dorado)); height: 100%; border-radius: 9999px; width: ${porcentaje}%; transition: width 1s ease-in-out;"></div>
              </div>
            </div>`;
            document.getElementById('perfilUsuarioTop').innerHTML = htmlPerfil;
            
            \2"""

text = re.sub(target_js, new_js, text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated v2.html successfully")
