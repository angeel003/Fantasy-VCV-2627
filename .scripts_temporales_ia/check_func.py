with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('function generarTarjetaPartidoV2(eq) {')
end = text.find('return `', start)
print(text[start:end+50])
