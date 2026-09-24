import re

# 1. Patch Código.js to add "ping" action
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

ping_logic = """
      // ACCIÓN DE PING (PRE-FETCHING)
      if (action === "ping") {
          // Leer una celda cualquiera para asegurar que la conexión a Google Sheets se despierte
          try { SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Ajustes").getRange("A1").getValue(); } catch(e){}
          return ContentService.createTextOutput(JSON.stringify({"status": "ok"})).setMimeType(ContentService.MimeType.JSON);
      }
"""

if "action === \"ping\"" not in code:
    code = code.replace("var action = params.action;", "var action = params.action;\n" + ping_logic)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

# 2. Patch dev.html to send "ping" silently on load
with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

prefetch_logic = """
  // --- PRE-CALENTAMIENTO (PRE-FETCHING) ---
  // Lanzamos un ping invisible medio segundo después de abrir la web para despertar al servidor
  setTimeout(() => {
      fetch(scriptURL, { 
          method: 'POST', 
          body: JSON.stringify({ action: 'ping' }), 
          headers: { 'Content-Type': 'text/plain;charset=utf-8' } 
      }).catch(e => console.log("Ping pre-fetching fallido", e));
  }, 500);
"""

if "PRE-CALENTAMIENTO" not in html:
    html = html.replace("let isGuestMode = false;", prefetch_logic + "\n  let isGuestMode = false;")

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

