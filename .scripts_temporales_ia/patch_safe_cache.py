import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

replacements = [
    ('return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "✅ Sincronizado', 
     'clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "✅ Sincronizado'),
    ('return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "✅ Añadidos', 
     'clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "✅ Añadidos'),
    ('return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "✅ Usuario \'', 
     'clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "✅ Usuario \''),
    ('return ContentService.createTextOutput(JSON.stringify({"status": "success"})).setMimeType', 
     'clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success"})).setMimeType'), 
    ('return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Contraseña actualizada con éxito!"}))', 
     'clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Contraseña actualizada con éxito!"}))'),
    ('return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "Solicitud enviada.', 
     'clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "Solicitud enviada.'),
    ('return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Tus predicciones a final de temporada', 
     'clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Tus predicciones a final de temporada'),
    ('return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Predicciones guardadas!"}))', 
     'clearAllCache(); return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "¡Predicciones guardadas!"}))')
]

for old, new in replacements:
    code = code.replace(old, new)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

