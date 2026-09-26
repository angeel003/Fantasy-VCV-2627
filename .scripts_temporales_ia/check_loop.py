with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('window.equiposActivos.forEach((eq) => {')
end = text.find('document.getElementById(\'contenedorPartidos\').innerHTML = html;', start)
print(text[start:start+1000])
