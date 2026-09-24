import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_js = """                // POPULATE LIGAS
                var ligasContainer = document.getElementById('adminLigasCheckboxes');
                if (ligasContainer && data.clasificaciones) {
                    ligasContainer.innerHTML = '';
                    var allLigas = Object.keys(data.clasificaciones);
                    allLigas.forEach(function(liga) {
                        var div = document.createElement('div');
                        div.innerHTML = '<label style="margin:0; cursor:pointer;"><input type="checkbox" value="' + liga + '" style="margin-right:5px;"> ' + liga + '</label>';
                        ligasContainer.appendChild(div);
                    });
                }"""

new_js = """                // POPULATE LIGAS
                var ligasContainer = document.getElementById('adminLigasCheckboxes');
                if (ligasContainer && data.todas_las_ligas) {
                    ligasContainer.innerHTML = '';
                    var allLigas = data.todas_las_ligas;
                    allLigas.forEach(function(liga) {
                        if (!liga) return; // Skip empty columns
                        var div = document.createElement('div');
                        div.innerHTML = '<label style="margin:0; cursor:pointer;"><input type="checkbox" value="' + liga + '" style="margin-right:5px;"> ' + liga + '</label>';
                        ligasContainer.appendChild(div);
                    });
                }"""

if old_js in text:
    text = text.replace(old_js, new_js)
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated dev.html to use todas_las_ligas")
else:
    print("Could not find old_js in dev.html")

