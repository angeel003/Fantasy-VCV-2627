import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

hist_old = r"""let infoLocFecha = "";
            let htmlReloj = "";
            let iconoLoc = p\.ubicacion === "CASA" \? "🏠" : \(p\.ubicacion === "FUERA" \? "🚌" : ""\);
            
            if \(esActual\) \{
                if\(iconoLoc \|\| p\.timestamp\) \{
                    infoLocFecha = `<span style="font-weight:normal; font-size:0.85rem; color:#666; margin-left:10px;">\$\{iconoLoc\} \$\{formatFecha\(p\.timestamp\)\}</span>`;
                \}"""

hist_new = r"""let streamIconHist = p.streaming ? ` <a href="${p.streaming}" target="_blank" style="color:#d32f2f; text-decoration:none; margin-left:6px; font-size:1.1rem;" title="Ver Streaming Oficial">▶️</a>` : "";
            let infoLocFecha = streamIconHist ? `<span style="margin-left:10px;">${streamIconHist}</span>` : "";
            let htmlReloj = "";
            let iconoLoc = p.ubicacion === "CASA" ? "🏠" : (p.ubicacion === "FUERA" ? "🚌" : "");
            
            if (esActual) {
                if(iconoLoc || p.timestamp) {
                    infoLocFecha = `<span style="font-weight:normal; font-size:0.85rem; color:#666; margin-left:10px;">${iconoLoc} ${formatFecha(p.timestamp)}${streamIconHist}</span>`;
                }
            }"""

html = re.sub(hist_old, hist_new, html)

# Just in case regex failed due to whitespace
html = html.replace("""let infoLocFecha = "";
            let htmlReloj = "";
            let iconoLoc = p.ubicacion === "CASA" ? "🏠" : (p.ubicacion === "FUERA" ? "🚌" : "");
            
            if (esActual) {
                if(iconoLoc || p.timestamp) {
                    infoLocFecha = `<span style="font-weight:normal; font-size:0.85rem; color:#666; margin-left:10px;">${iconoLoc} ${formatFecha(p.timestamp)}</span>`;
                }""", hist_new)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

