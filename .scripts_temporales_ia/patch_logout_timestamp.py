import os

# 1. Update script-dev/Código.js
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

old_login_check = """    var dataUsuarios = sheetUsuarios.getDataRange().getValues();
    var valid = false;
    var mapNombresReales = {}; 
    for (var i = 1; i < dataUsuarios.length; i++) {
      var u = dataUsuarios[i][0];
      if(u) { mapNombresReales[u] = dataUsuarios[i][2] ? dataUsuarios[i][2].toString().trim() : u; }
      if (u == usuario && dataUsuarios[i][1] == password) { valid = true; }
    }
    if (!valid) return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Usuario o contraseña incorrectos."})).setMimeType(ContentService.MimeType.JSON);"""

new_login_check = """    var dataUsuarios = sheetUsuarios.getDataRange().getValues();
    var valid = false;
    var mapNombresReales = {}; 
    var filaUsuario = -1;
    for (var i = 1; i < dataUsuarios.length; i++) {
      var u = dataUsuarios[i][0];
      if(u) { mapNombresReales[u] = dataUsuarios[i][2] ? dataUsuarios[i][2].toString().trim() : u; }
      if (u == usuario && dataUsuarios[i][1] == password) { 
          valid = true; 
          filaUsuario = i + 1;
      }
    }
    if (!valid) return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Usuario o contraseña incorrectos."})).setMimeType(ContentService.MimeType.JSON);
    
    // Registrar Último Acceso si es login o get_data
    if (action === "login" || action === "get_data") {
        if (filaUsuario !== -1) {
            sheetUsuarios.getRange(filaUsuario, 4).setValue(new Date());
        }
    }"""

js_content = js_content.replace(old_login_check, new_login_check)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(js_content)


# 2. Update dev.html
with open('dev.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Add btnLogout HTML
old_header_app = """                <div class="col-md-12 text-center" style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 8px;">
                    <div style="font-size:1.4rem; font-weight:bold; color:var(--vcv-morado);" id="displayJugador"></div>
                    <div id="displayBadges" style="display:flex; flex-direction:row; flex-wrap:wrap; justify-content:center; align-items:center; gap:6px;"></div>
                </div>"""

new_header_app = """                <div class="col-md-12 text-center" style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 8px;">
                    <div style="font-size:1.4rem; font-weight:bold; color:var(--vcv-morado);" id="displayJugador"></div>
                    <div id="displayBadges" style="display:flex; flex-direction:row; flex-wrap:wrap; justify-content:center; align-items:center; gap:6px;"></div>
                </div>
                <div class="col-md-12 text-center" style="margin-top: 10px;">
                    <button id="btnLogout" class="btn btn-outline-danger btn-sm" style="border-radius: 20px; font-weight: bold; padding: 5px 15px;">⬅️ Salir / Volver atrás</button>
                </div>"""

html_content = html_content.replace(old_header_app, new_header_app)

# Add btnLogout JS event listener
js_logout_logic = """
// ------------------------------------------------------------------
// LOGICA DE BOTON VOLVER ATRAS / SALIR
// ------------------------------------------------------------------
document.getElementById('btnLogout').addEventListener('click', function() {
    currentUser = null;
    currentPassword = null;
    isGuestMode = false;
    document.getElementById('loginUsuario').value = '';
    document.getElementById('loginPassword').value = '';
    document.getElementById('appSection').style.display = 'none';
    document.getElementById('btnReload').style.display = 'none';
    document.getElementById('loginMessage').style.display = 'none';
    document.getElementById('loginSection').style.display = 'block';
});
"""

html_content = html_content.replace('// LÓGICA MODO INVITADO', js_logout_logic + '\n// LÓGICA MODO INVITADO')
html_content = html_content.replace('// LOGICA MODO INVITADO', js_logout_logic + '\n// LOGICA MODO INVITADO')


with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Added btnLogout and login timestamp successfully.")

