with open('dev.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if '// --- LOGICA JUGADOR DESTACADO ---' in line:
        new_lines.append(line)
        new_lines.append('                      let destacadoHtml = "";\n')
        new_lines.append('                      if (eq.plantilla && eq.plantilla.length > 0) {\n')
        skip = True
        continue
    
    if skip:
        if '// --- FIN LOGICA JUGADOR DESTACADO ---' in line:
            new_lines.append('                      }\n')
            new_lines.append(line)
            skip = False
            continue
        
        # indent line inside block
        if 'let destacadoHtml = "";' in line:
            continue # already added
            
        if 'Plantilla no disponible para votaci' in line:
            # We skip the else { destacadoHtml = ... } block entirely
            # Actually, the previous line is "} else {"
            # And next line is "}"
            pass
        else:
            # Check if this line is part of the 'else {' for missing plantilla
            if '} else {' in line and 'Plantilla no disponible' in lines[i+1]:
                pass # skip '} else {'
            elif 'Plantilla no disponible' in line:
                pass # skip
            elif '}' in line and 'Plantilla no disponible' in lines[i-1]:
                pass # skip closing '}'
            else:
                new_lines.append('    ' + line)
        continue
        
    new_lines.append(line)

with open('dev.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

