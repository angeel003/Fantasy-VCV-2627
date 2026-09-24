import re

files = ['script-dev/Código.js', 'script-prod/Código.js']

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        js = f.read()

    js = js.replace('\r\n', '\n')

    # Find the block dynamically
    start = js.find('else if (sheet.getName() === "Usuarios") {')
    end = js.find('}\n}', start) + 3
    
    if start != -1 and end != -1:
        old_block = js[start:end]
        
        new_onedit = """else if (sheet.getName() === "Usuarios") {
    if (col === 1 && row > 1) {
      if (e.oldValue && e.value && e.oldValue !== e.value) {
        var usuarioAntiguo = e.oldValue.toString().trim();
        var usuarioNuevo = e.value.toString().trim();
        
        // CHECK FOR DUPLICATES FIRST
        var usuariosData = sheet.getRange(1, 1, sheet.getLastRow(), 1).getValues();
        var duplicateFound = false;
        for (var i = 1; i < usuariosData.length; i++) {
            // Check if another row (not the one we just edited) has the new username
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
        // We bypass getSafeData for writes to ensure we get fresh row counts directly from sheets in case cache is stale
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
        ss.toast("Se ha actualizado el usuario '" + usuarioAntiguo + "' a '" + usuarioNuevo + "' en todas las pestañas.", "Actualización Mágica", 5);
      }
    }
  }
}"""
        
        js = js.replace(old_block, new_onedit)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(js)
        print(f"Patched {filename}")
    else:
        print(f"Block not found in {filename}!")

