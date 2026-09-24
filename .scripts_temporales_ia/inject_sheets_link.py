import re

sheets_link_html = """
      <div id="sheetsLinkDiv" style="display:none; margin-top: 20px; text-align:center; padding-top: 15px;">
          <a href="https://docs.google.com/spreadsheets/" target="_blank" class="btn btn-outline-warning btn-sm" style="font-weight:bold; border-width:2px; font-size:1.1rem; padding:10px 20px; background:var(--vcv-dorado); color:var(--vcv-morado);">📄 Abrir Base de Datos (Google Sheets)</a>
      </div>
"""

js_toggle = """
        document.getElementById('adminPanelWrapper').style.display = 'block';
        document.getElementById('sheetsLinkDiv').style.display = 'block';
    } else {
        document.body.classList.remove('admin-dark-mode');
        document.getElementById('app-tabs').style.display = 'flex';
        // Restore active tab logic roughly (default to predicciones)
        document.getElementById('prediccionesList').style.display = 'block';
        document.getElementById('tituloPrincipalSeccion').style.display = 'block';
        document.getElementById('btnSubmit').style.display = 'block';
        
        document.getElementById('adminPanelWrapper').style.display = 'none';
        document.getElementById('sheetsLinkDiv').style.display = 'none';
    }
"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'sheetsLinkDiv' not in html:
        # append right before toastNotification
        html = html.replace('<div id="toastNotification">', sheets_link_html + '\n  <div id="toastNotification">')
        html = html.replace("document.getElementById('adminPanelWrapper').style.display = 'block';", "document.getElementById('adminPanelWrapper').style.display = 'block';\n        document.getElementById('sheetsLinkDiv').style.display = 'block';")
        html = html.replace("document.getElementById('adminPanelWrapper').style.display = 'none';", "document.getElementById('adminPanelWrapper').style.display = 'none';\n        document.getElementById('sheetsLinkDiv').style.display = 'none';")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

