with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

if 'motivos.push("Ganador (+" + pG + ")");' in text:
    print('YES Winner Fix')
else:
    print('NO Winner Fix')
