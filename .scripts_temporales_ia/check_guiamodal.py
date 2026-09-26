import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('id="guiaModal"')
end = text.find('</div>', text.find('</div>', text.find('</div>', start)+1)+1)+1
sys.stdout.buffer.write(text[start:end].encode('utf-8'))
