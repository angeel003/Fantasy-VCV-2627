with open('prototipo_stitch.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<div class="glass-card match-card"')
end = text.find('<div class="glass-card match-card"', start + 1)
print(text[start:end])
