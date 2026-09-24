import os

files = ['script-dev/Código.js', 'script-prod/Código.js']

for filepath in files:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # 1. Fix clearAllCache
    old_clear = 'var keys = ["vcv_sheet_Usuarios", "vcv_sheet_Ajustes", "vcv_sheet_Permisos_Equipos", "vcv_sheet_Ligas", "vcv_sheet_Ligas_Equipos", "vcv_sheet_Porras", "vcv_sheet_Resultados Oficiales", "vcv_sheet_Reglas_Puntuacion", "vcv_sheet_Insignias", "vcv_sheet_Peticiones_Nombre", "vcv_sheet_Predicciones_Secretas", "vcv_sheet_Permisos_Secreta"];'
    new_clear = 'var keys = ["vcv_sheet_Usuarios", "vcv_sheet_Ajustes", "vcv_sheet_Partidos", "vcv_sheet_Permisos_Equipos", "vcv_sheet_Ligas", "vcv_sheet_Ligas_Equipos", "vcv_sheet_Porras", "vcv_sheet_Resultados Oficiales", "vcv_sheet_Reglas_Puntuacion", "vcv_sheet_Insignias", "vcv_sheet_Peticiones_Nombre", "vcv_sheet_Predicciones_Secretas", "vcv_sheet_Permisos_Secreta"];'
    
    code = code.replace(old_clear, new_clear)
    
    # 2. Add action == "clear_cache" inside doPost
    if 'action === "clear_cache"' not in code:
        # Find where to inject. Let's find action === "login_guest" and insert before it
        insert_point = 'if (action === "login_guest") {'
        action_code = """if (action === "clear_cache") {
        if (!esAdminAutenticado) return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Permiso denegado."})).setMimeType(ContentService.MimeType.JSON);
        clearAllCache();
        return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": " Cch borrada. Todo actualizado con el Excel."})).setMimeType(ContentService.MimeType.JSON);
    }

    """
        code = code.replace(insert_point, action_code + insert_point)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)

