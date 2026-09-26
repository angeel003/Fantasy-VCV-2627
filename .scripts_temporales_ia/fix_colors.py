with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('class="section-alt" id="clasificacionesSection"', 'id="clasificacionesSection"')
text = text.replace('class="section-alt" id="historialSection"', 'id="historialSection"')
text = text.replace('class="section-alt" id="calendarioSection"', 'id="calendarioSection"')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Removed section-alt')
