import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Make sure we don't duplicate if already exists
if 'var isWriteAction =' not in code:
    code = code.replace('var action = params.action;', 'var action = params.action;\n      var isWriteAction = ["save", "save_resultado_admin", "add_user", "sync_permisos", "change_password", "request_name_change", "save_totales"].indexOf(action) !== -1;')
    
    code = code.replace('return ContentService', 'if (isWriteAction && typeof clearAllCache === "function") { clearAllCache(); }\n      return ContentService')

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

