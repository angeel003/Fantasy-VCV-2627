with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('if (eq.estado === "ABIERTO") {')
end = text.find('} else if (eq.estado === "CERRADO_PENDIENTE" || eq.estado === "EN_JUEGO") {', start)

print(text[start:end])
