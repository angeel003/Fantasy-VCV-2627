import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace crlf to lf
html = html.replace('\r\n', '\n')

old_js = """    let catSelect = document.getElementById('calendarTeamSelect');
    let uniqueCats = [...new Set(todos.map(p => p.categoria))].filter(c => c);
    
    let currentOptions = '<option value="">-- Ver Todos los Equipos --</option>';
    uniqueCats.forEach(cat => {
        currentOptions += `<option value="${cat}">${cat}</option>`;
    });
    catSelect.innerHTML = currentOptions;
    
    let savedCat = localStorage.getItem('pref_calendario_' + currentUser);
    if (savedCat && uniqueCats.includes(savedCat)) {
        catSelect.value = savedCat;
    }"""

new_js = """    let catSelect = document.getElementById('calendarTeamSelect');
    let uniqueCats = window.appData.equipos_totales || [];
    
    let currentOptions = '<option value="">-- Ver Todos los Equipos --</option>';
    uniqueCats.forEach(cat => {
        currentOptions += `<option value="${cat}">${cat}</option>`;
    });
    catSelect.innerHTML = currentOptions;
    
    let savedCat = localStorage.getItem('pref_calendario_' + currentUser);
    if (savedCat && uniqueCats.includes(savedCat)) {
        catSelect.value = savedCat;
    }"""

old_filter = """    let filtered = window.appData.todos_partidos.filter(p => {
        let matchCat = (!cat || p.categoria === cat);
        let matchSearch = (!search || p.rival.toLowerCase().includes(search) || p.equipo_local.toLowerCase().includes(search));
        return matchCat && matchSearch;
    });"""

new_filter = """    let filtered = window.appData.todos_partidos.filter(p => {
        let matchCat = (!cat || p.equipo_local === cat || p.rival === cat);
        let matchSearch = (!search || p.rival.toLowerCase().includes(search) || p.equipo_local.toLowerCase().includes(search));
        return matchCat && matchSearch;
    });"""

if old_js in html and old_filter in html:
    html = html.replace(old_js, new_js)
    html = html.replace(old_filter, new_filter)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched dev.html for team names!")
else:
    print("Blocks not found!")
