import re

files = ['script-dev/Código.js', 'script-prod/Código.js']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        js = f.read()

    js = js.replace('\r\n', '\n')

    old_add = """        // Lo añade a la pestaña Usuarios
        sheetUsuarios.appendRow([newU, newP, newN]);
        clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": " Usuario '" + newU + "' creado correctamente."})).setMimeType(ContentService.MimeType.JSON);"""

    new_add = """        // Lo añade a la pestaña Usuarios y a las demás para que salgan listos para ponerles una 'X'
        sheetUsuarios.appendRow([newU, newP, newN]);
        
        var sheetsToAppend = ["Permisos_Equipos", "Ligas", "Insignias", "Permisos_Secreta"];
        for(var i=0; i<sheetsToAppend.length; i++) {
            var sh = ss.getSheetByName(sheetsToAppend[i]);
            if(sh) {
                // Crear un array vacío del tamaño de las columnas, y poner el nombre en la primera
                var lc = sh.getLastColumn();
                if(lc > 0) {
                    var newRow = new Array(lc).fill("");
                    newRow[0] = newU;
                    sh.appendRow(newRow);
                } else {
                    sh.appendRow([newU]);
                }
            }
        }
        
        clearAllCache(); 
        return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": " Usuario '" + newU + "' creado e insertado en todas las tablas."})).setMimeType(ContentService.MimeType.JSON);"""

    # Also handle the unaccented version if the user has an older version locally
    old_add_2 = """        // Lo aade a la pestaa Usuarios
        sheetUsuarios.appendRow([newU, newP, newN]);
        clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": " Usuario '" + newU + "' creado correctamente."})).setMimeType(ContentService.MimeType.JSON);"""

    if old_add in js:
        js = js.replace(old_add, new_add)
    elif old_add_2 in js:
        js = js.replace(old_add_2, new_add)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"Patched add_user in {filename}")
