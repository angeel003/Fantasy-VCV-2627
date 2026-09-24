with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'sheetUsuarios.getRange(filaUsuario, 4).setValue(new Date());' in line:
        lines[i] = '              var cache = CacheService.getScriptCache();\n              if (!cache.get("login_ts_" + usuario)) {\n                  try { sheetUsuarios.getRange(filaUsuario, 4).setValue(new Date()); } catch(e) {}\n                  cache.put("login_ts_" + usuario, "1", 3600);\n              }\n'
        break

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

