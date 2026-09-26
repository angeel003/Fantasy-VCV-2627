import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('id="enlacesRfevbSection"')
end = text.find('</section>', start)
sys.stdout.buffer.write(text[start:end+10].encode('utf-8'))
