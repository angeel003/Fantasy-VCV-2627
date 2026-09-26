import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
if 'miCajonHTML = ""; // El usuario pidió' in text:
    print('CAJON HIDDEN')
if 'categoriaEq' in text:
    print('CATEGORIA INCLUDED')
