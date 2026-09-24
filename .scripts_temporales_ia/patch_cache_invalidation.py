import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Change cache time from 15 to 21600
code = code.replace('cache.put(cacheKey, str, 15);', 'cache.put(cacheKey, str, 21600);')

# 2. Add clearAllCache function
clear_cache_func = """function clearAllCache() {
    var keys = ["vcv_sheet_Usuarios", "vcv_sheet_Ajustes", "vcv_sheet_Permisos_Equipos", "vcv_sheet_Ligas", "vcv_sheet_Ligas_Equipos", "vcv_sheet_Porras", "vcv_sheet_Resultados Oficiales", "vcv_sheet_Reglas_Puntuacion", "vcv_sheet_Insignias", "vcv_sheet_Peticiones_Nombre", "vcv_sheet_Predicciones_Secretas", "vcv_sheet_Permisos_Secreta"];
    try { CacheService.getScriptCache().removeAll(keys); } catch(e) {}
}

"""
# Add it right before doPost
code = code.replace("function doPost(e) {", clear_cache_func + "function doPost(e) {")

# 3. Inject clearAllCache() into write endpoints
# add_user
code = code.replace('sheetUsuarios.appendRow([new_u, new_p, new_n, new Date()]);', 
                    'sheetUsuarios.appendRow([new_u, new_p, new_n, new Date()]); clearAllCache();')

# save_resultado_admin
code = code.replace('sheetResultados.appendRow([idPart, sets, parc, new Date(), stream]);',
                    'sheetResultados.appendRow([idPart, sets, parc, new Date(), stream]); clearAllCache();')

# change_password
code = code.replace('sheetUsuarios.getRange(i, 2).setValue(new_password);',
                    'sheetUsuarios.getRange(i, 2).setValue(new_password); clearAllCache();')

# request_name_change
code = code.replace('sheetPeticiones.appendRow([new Date(), usuario, new_usuario, new_nombre, "PENDIENTE"]);',
                    'sheetPeticiones.appendRow([new Date(), usuario, new_usuario, new_nombre, "PENDIENTE"]); clearAllCache();')

# save_totales
code = code.replace('if (p.sets) { sheetPorras.appendRow([new Date(), usuario, idPart, p.sets, p.puntos, p.signo]); }',
                    'if (p.sets) { sheetPorras.appendRow([new Date(), usuario, idPart, p.sets, p.puntos, p.signo]); }') # wait, save_totales is below
code = code.replace('sheetPrediccionesTotales.appendRow([new Date(), usuario, eq, pT]);',
                    'sheetPrediccionesTotales.appendRow([new Date(), usuario, eq, pT]); clearAllCache();')

# save
code = code.replace('if (p.sets) { sheetPorras.appendRow([new Date(), usuario, idPart, p.sets, p.puntos, p.signo]); }\n        }',
                    'if (p.sets) { sheetPorras.appendRow([new Date(), usuario, idPart, p.sets, p.puntos, p.signo]); }\n        }\n        clearAllCache();')

# automatic ajustes updates (when match is closed)
code = code.replace('if(changesMade && updatesColumnas.length > 0) { sheetAjustes.getRange(2, 8, updatesColumnas.length, 2).setValues(updatesColumnas); }',
                    'if(changesMade && updatesColumnas.length > 0) { sheetAjustes.getRange(2, 8, updatesColumnas.length, 2).setValues(updatesColumnas); clearAllCache(); }')

# sync_permisos (creates a new user in permisos)
code = code.replace('sheetPermisos.appendRow(nuevaFilaPermiso);',
                    'sheetPermisos.appendRow(nuevaFilaPermiso); clearAllCache();')

# onEdit (Admin actions in spreadsheet)
code = code.replace('ss.toast("Se ha actualizado el usuario',
                    'clearAllCache();\n          ss.toast("Se ha actualizado el usuario')

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

