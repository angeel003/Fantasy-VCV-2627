import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('if (eq.estado === "ABIERTO") {')
print('Start:', start)
end = text.find('} else if (eq.estado === "CERRADO") {', start)
print('End:', end)
