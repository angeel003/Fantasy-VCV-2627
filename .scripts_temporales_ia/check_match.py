with open('prototipo_stitch.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('<!-- PARTIDO 1')
end = text.find('<!-- PARTIDO 2', start)
if start != -1 and end != -1:
    print(text[start:end])
else:
    start = text.find('class="match-card')
    print(text[start-50:start+2000])
