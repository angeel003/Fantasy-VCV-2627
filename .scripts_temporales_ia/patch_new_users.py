import re

files = ['script-dev/Código.js', 'script-prod/Código.js']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        js = f.read()

    js = js.replace('\r\n', '\n')

    # 1. Update onEdit for NEW users added manually in Excel
    start = js.find('else if (sheet.getName() === "Usuarios") {')
    end = js.find('}\n}', start) + 3
    
    if start != -1 and end != -1:
        old_block = js[start:end]
        
        new_onedit = """else if (sheet.getName() === "Usuarios") {
    if (col === 1 && row > 1) {
      // SI CAMBIA UN NOMBRE EXISTENTE
      if (e.oldValue && e.value && e.oldValue !== e.value) {
        var usuarioAntiguo = e.oldValue.toString().trim();
        var usuarioNuevo = e.value.toString().trim();
        
        // CHECK FOR DUPLICATES FIRST
        var usuariosData = sheet.getRange(1, 1, sheet.getLastRow(), 1).getValues();
        var duplicateFound = false;
        for (var i = 1; i < usuariosData.length; i++) {
            if (i + 1 !== row && usuariosData[i][0] && usuariosData[i][0].toString().trim().toLowerCase() === usuarioNuevo.toLowerCase()) {
                duplicateFound = true;
                break;
            }
        }
        
        if (duplicateFound) {
            sheet.getRange(row, col).setValue(usuarioAntiguo); // REVERT
            ss.toast("Error: El usuario '" + usuarioNuevo + "' ya existe en la base de datos.", "Cambio Rechazado", 5);
            return;
        }
        
        // PROCEED WITH UPDATE
        var sheetsColA = ["Permisos_Equipos", "Ligas", "Insignias", "Permisos_Secreta"]; 
        for (var s = 0; s < sheetsColA.length; s++) {
          var sh = ss.getSheetByName(sheetsColA[s]);
          if (sh && sh.getLastRow() > 0) {
            var d = sh.getRange(1, 1, sh.getLastRow(), 1).getValues();
            for (var r = 1; r < d.length; r++) { 
                var celdaU = d[r][0] ? d[r][0].toString().trim() : "";
                if (celdaU.toLowerCase() === usuarioAntiguo.toLowerCase()) { 
                    sh.getRange(r + 1, 1).setValue(usuarioNuevo); 
                } 
            }
          }
        }
        
        var sheetsColB = ["Porras", "Predicciones_Secretas", "Peticiones_Nombre"];
        for (var s = 0; s < sheetsColB.length; s++) {
          var sh = ss.getSheetByName(sheetsColB[s]);
          if (sh && sh.getLastRow() > 0) {
            var d = sh.getRange(1, 1, sh.getLastRow(), 2).getValues();
            for (var r = 1; r < d.length; r++) { 
                var celdaU = d[r][1] ? d[r][1].toString().trim() : "";
                if (celdaU.toLowerCase() === usuarioAntiguo.toLowerCase()) { 
                    sh.getRange(r + 1, 2).setValue(usuarioNuevo); 
                } 
            }
          }
        }
        
        clearAllCache();
        ss.toast("Se ha actualizado el usuario en todas las pestañas.", "Actualización", 5);
      }
      // SI AÑADE UN USUARIO NUEVO DIRECTAMENTE EN LA CELDA VACÍA DEL EXCEL
      else if (!e.oldValue && e.value) {
        var usuarioNuevo = e.value.toString().trim();
        
        // CHECK FOR DUPLICATES
        var usuariosData = sheet.getRange(1, 1, sheet.getLastRow(), 1).getValues();
        var duplicateFound = false;
        for (var i = 1; i < usuariosData.length; i++) {
            if (i + 1 !== row && usuariosData[i][0] && usuariosData[i][0].toString().trim().toLowerCase() === usuarioNuevo.toLowerCase()) {
                duplicateFound = true; break;
            }
        }
        
        if (duplicateFound) {
            sheet.getRange(row, col).clearContent();
            ss.toast("Error: El usuario '" + usuarioNuevo + "' ya existe.", "Rechazado", 5);
            return;
        }
        
        var sheetsToAppend = ["Permisos_Equipos", "Ligas", "Insignias", "Permisos_Secreta"];
        for(var i=0; i<sheetsToAppend.length; i++) {
            var sh = ss.getSheetByName(sheetsToAppend[i]);
            if(sh) {
                // Buscamos la primera fila vacia en la columna A
                var vals = sh.getRange(1, 1, sh.getMaxRows(), 1).getValues();
                var firstEmpty = 1;
                for(var j=0; j<vals.length; j++){
                    if(!vals[j][0] || vals[j][0].toString().trim() === "") {
                        firstEmpty = j + 1;
                        break;
                    }
                }
                if(firstEmpty > sh.getMaxRows()) sh.appendRow([""]); // Just in case
                
                sh.getRange(firstEmpty, 1).setValue(usuarioNuevo);
            }
        }
        
        clearAllCache();
        ss.toast("Usuario añadido a Permisos, Ligas e Insignias.", "Nuevo Usuario", 5);
      }
    }
  }
}"""
        
        js = js.replace(old_block, new_onedit)


    # 2. Update add_user (API) to use the same robust "find first empty row" logic
    start_add = js.find('if (action === "add_user") {')
    end_add = js.find('if (action === "save_resultado_admin")', start_add)
    
    if start_add != -1 and end_add != -1:
        old_add_block = js[start_add:end_add]
        
        new_add_block = """if (action === "add_user") {
        if (!esAdminAutenticado) return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Permiso denegado."})).setMimeType(ContentService.MimeType.JSON);
        
        var newU = params.new_u ? params.new_u.toString().trim() : "";
        var newP = params.new_p ? params.new_p.toString().trim() : "";
        var newN = params.new_n ? params.new_n.toString().trim() : "";
        
        if (!newU || !newP) {
            return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "El usuario y la contraseña son obligatorios."})).setMimeType(ContentService.MimeType.JSON);
        }
        
        var dataUsr = getSafeData(sheetUsuarios);
        for(var i=1; i<dataUsr.length; i++) {
            if(dataUsr[i][0] && dataUsr[i][0].toString().toLowerCase() === newU.toLowerCase()) {
                return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": " El usuario ya existe en la base de datos."})).setMimeType(ContentService.MimeType.JSON);
            }
        }
        
        // Find first empty row in Usuarios
        var valsU = sheetUsuarios.getRange(1, 1, sheetUsuarios.getMaxRows(), 1).getValues();
        var firstEmptyU = 1;
        for(var j=0; j<valsU.length; j++){
            if(!valsU[j][0] || valsU[j][0].toString().trim() === "") {
                firstEmptyU = j + 1;
                break;
            }
        }
        sheetUsuarios.getRange(firstEmptyU, 1).setValue(newU);
        sheetUsuarios.getRange(firstEmptyU, 2).setValue(newP);
        sheetUsuarios.getRange(firstEmptyU, 3).setValue(newN);
        
        // Also add to other sheets
        var sheetsToAppend = ["Permisos_Equipos", "Ligas", "Insignias", "Permisos_Secreta"];
        for(var i=0; i<sheetsToAppend.length; i++) {
            var sh = ss.getSheetByName(sheetsToAppend[i]);
            if(sh) {
                var vals = sh.getRange(1, 1, sh.getMaxRows(), 1).getValues();
                var firstEmpty = 1;
                for(var j=0; j<vals.length; j++){
                    if(!vals[j][0] || vals[j][0].toString().trim() === "") {
                        firstEmpty = j + 1;
                        break;
                    }
                }
                sh.getRange(firstEmpty, 1).setValue(newU);
            }
        }
        
        clearAllCache(); 
        return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": " Usuario '" + newU + "' creado e insertado en todas las tablas."})).setMimeType(ContentService.MimeType.JSON);
    }

    """
        js = js.replace(old_add_block, new_add_block)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(js)
        print(f"Patched {filename}")
    else:
        print(f"Blocks not found in {filename}")

