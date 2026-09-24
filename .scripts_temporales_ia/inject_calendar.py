import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject HTML for Calendar Section
calendar_html = """
    <section class="section-alt" id="calendarioSection">
        <h2 style="margin-bottom: 25px;">📅 Próximos Partidos</h2>
        <div class="form-container" style="max-width: 800px; margin: 0 auto; text-align: left;">
            <div style="display:flex; gap:10px; margin-bottom:20px; flex-wrap:wrap;">
                <select id="calendarTeamSelect" class="form-control" style="flex:2; font-weight:bold; min-width:200px; border:2px solid var(--vcv-dorado);">
                    <option value="">-- Selecciona un Equipo --</option>
                </select>
                <input type="text" id="calendarSearchInput" class="form-control" placeholder="Buscar rival..." style="flex:1; min-width:150px; border:2px solid #ccc;">
            </div>
            
            <div id="calendarResults" style="display:flex; flex-direction:column; gap:12px; max-height:500px; overflow-y:auto; padding-right:5px;">
                <!-- Calendario dinámico -->
            </div>
            
            <p style="color:#888; font-size:0.8rem; margin-top:25px; font-style:italic; text-align:center; padding: 10px; border-top: 1px dashed #ccc;">
                Si alguien ve que hay alguna errata o sabe de algún cambio en algún horario de partido, notifique al correo <a href="mailto:adminfantasyvcv@gmail.com" style="color:#1565c0;">adminfantasyvcv@gmail.com</a> lo antes posible por favor, por el bien de todos.
            </p>
        </div>
    </section>
"""

# Insert before closing tag of appSection (</div>)
# appSection ends right before `</div>\n    \n    <!-- MODAL BOOTSTRAP -->` or something similar.
# Let's just find `</section>\n</div>` which should be the end of appSection.
if 'id="calendarioSection"' not in html:
    # Let's find the end of appSection safely by looking for `<div id="loginSection">` which comes later, or the last section
    last_section_end = html.find('    </section>\n</div>\n\n    <!--')
    if last_section_end == -1:
        last_section_end = html.rfind('</section>\n</div>')
    
    if last_section_end != -1:
        html = html[:last_section_end + 11] + "\n" + calendar_html + html[last_section_end + 11:]
    else:
        # Fallback, just append after historial section
        html = html.replace('</section>\n    <section class="section-alt" id="historialSection">', '</section>\n    <section class="section-alt" id="historialSection">') # Dummy

# 2. Inject JS for rendering calendar
calendar_js = """
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
    let uniqueCats = [...new Set(todos.map(p => p.categoria))].filter(c => c);
    
    let currentOptions = '<option value="">-- Ver Todos los Equipos --</option>';
    uniqueCats.forEach(cat => {
        currentOptions += `<option value="${cat}">${cat}</option>`;
    });
    catSelect.innerHTML = currentOptions;
    
    let savedCat = localStorage.getItem('pref_calendario_' + currentUser);
    if (savedCat && uniqueCats.includes(savedCat)) {
        catSelect.value = savedCat;
    }
    
    renderCalendar();
};

window.renderCalendar = function() {
    if(!window.appData || !window.appData.todos_partidos) return;
    
    let cat = document.getElementById('calendarTeamSelect').value;
    let search = document.getElementById('calendarSearchInput').value.toLowerCase().trim();
    
    localStorage.setItem('pref_calendario_' + currentUser, cat);
    
    let filtered = window.appData.todos_partidos.filter(p => {
        let matchCat = (!cat || p.categoria === cat);
        let matchSearch = (!search || p.rival.toLowerCase().includes(search) || p.equipo_local.toLowerCase().includes(search));
        return matchCat && matchSearch;
    });

    let html = "";
    if (filtered.length === 0) {
        html = `<div style="text-align:center; padding:30px; color:#888; font-weight:bold;">No se han encontrado partidos con estos filtros.</div>`;
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

            html += `<div style="background:white; padding:15px; border-radius:10px; border-left:5px solid ${esPasado ? 'var(--vcv-dorado)' : 'var(--vcv-morado)'}; box-shadow:0 2px 5px rgba(0,0,0,0.06); transition: transform 0.2s;">
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
    
    document.getElementById('calendarResults').innerHTML = html;
};

document.getElementById('calendarTeamSelect').addEventListener('change', window.renderCalendar);
document.getElementById('calendarSearchInput').addEventListener('input', window.renderCalendar);
"""

if "initCalendar()" not in html:
    html = html.replace("</script>\n</body>", calendar_js + "\n</script>\n</body>")
    
    # We also need to call initCalendar() when data is loaded.
    # Where is appData set?
    # `window.appData = data;` is right after `if(data.status === "success") { currentUser = usr;`
    html = html.replace("window.appData = data;", "window.appData = data; window.initCalendar();")

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print(f"Injected Calendar UI into {filename}")

