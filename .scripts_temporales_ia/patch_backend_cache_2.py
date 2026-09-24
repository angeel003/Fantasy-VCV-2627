import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_str = """      if (action === "login" || action === "get_data") {
          if (filaUsuario !== -1) {
              sheetUsuarios.getRange(filaUsuario, 4).setValue(new Date());
          }
      }"""

new_str = """      if (action === "login" || action === "get_data") {
          if (filaUsuario !== -1) {
              var cache = CacheService.getScriptCache();
              if (!cache.get("login_ts_" + usuario)) {
                  try { sheetUsuarios.getRange(filaUsuario, 4).setValue(new Date()); } catch(e) {}
                  cache.put("login_ts_" + usuario, "1", 3600); // 1 hour
              }
          }
      }"""

code = code.replace(old_str, new_str)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

