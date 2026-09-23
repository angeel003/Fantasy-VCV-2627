with open('dev.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'let infoLocFecha = "";' in line and 'let htmlReloj = "";' in lines[i+1] and 'if (esActual) {' in lines[i+4]:
        lines[i] = '            let streamIconHist = p.streaming ? ` <a href="${p.streaming}" target="_blank" style="color:#d32f2f; text-decoration:none; margin-left:6px; font-size:1.1rem;" title="Ver Streaming Oficial">▶️</a>` : "";\n'
        lines[i] += '            let infoLocFecha = streamIconHist ? `<span style="margin-left:10px;">${streamIconHist}</span>` : "";\n'
        lines[i+6] = '                    infoLocFecha = `<span style="font-weight:normal; font-size:0.85rem; color:#666; margin-left:10px;">${iconoLoc} ${formatFecha(p.timestamp)}${streamIconHist}</span>`;\n'
        break

with open('dev.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

