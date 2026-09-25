import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<select id="e${eq.id_partido}_sets"')
end = text.find('</select>', start)
print(text[start:end+10].encode('ascii', 'ignore').decode('ascii'))
