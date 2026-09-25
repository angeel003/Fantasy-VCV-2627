with open('.scripts_temporales_ia/build_v2_gradual2.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('} else if (eq.estado === "CERRADO_PENDIENTE" || eq.estado === "EN_JUEGO") {', '} else if (eq.estado === "CERRADO") {')

with open('.scripts_temporales_ia/build_v2_gradual2.py', 'w', encoding='utf-8') as f:
    f.write(code)
