import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

# I will find the EXACT string and replace it.
target_str = """            if (isAdmin) {
                document.getElementById('adminPanelWrapper').style.display = "block";
                renderAdminPanel(data.equipos); """

new_str = """            if (isAdmin) {
                document.getElementById('adminPanelWrapper').style.display = "block";
                renderAdminPanel(data.equipos); 
                
                // POPULATE LIGAS
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

if target_str in text:
    text = text.replace(target_str, new_str)
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully injected populate ligas.")
else:
    print("Target string not found!")

