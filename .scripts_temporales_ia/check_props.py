with open('script-prod/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('updatesColumnas.push([nuevoEstado, nuevaVisibilidad]);')
if start != -1: print(text[start:start+1000].encode('ascii', 'ignore').decode('ascii'))
