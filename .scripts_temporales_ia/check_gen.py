import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('if (eq.estado === "ABIERTO") {')
end = text.find('} else if (eq.estado === "CERRADO") {', start)

if start != -1 and end != -1:
    print(text[start:start+1000])
else:
    print("Not found")
