import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

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
    
    window.renderCalendar();
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

            html_res += `<div style="background:white; padding:15px; border-radius:10px; border-left:5px solid ${esPasado ? 'var(--vcv-dorado)' : 'var(--vcv-morado)'}; box-shadow:0 2px 5px rgba(0,0,0,0.06); transition: transform 0.2s; margin-bottom:10px;">
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
"""

if 'LOGICA DE CALENDARIO' not in html:
    # insert before the last </script>
    # <script>
    #   if ('serviceWorker' in navigator) { ... }
    # </script>
    # </body>
    idx_body = html.rfind('</body>')
    if idx_body != -1:
        # Find the script tag closing just before body
        idx_script = html.rfind('</script>', 0, idx_body)
        if idx_script != -1:
            html = html[:idx_script] + calendar_js + "\n" + html[idx_script:]
            print("Injected JS")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
        else:
            print("Could not find script tag")
else:
    print("Already injected JS")

