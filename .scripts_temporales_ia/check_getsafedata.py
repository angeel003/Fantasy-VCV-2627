import sys
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('function getSafeData')
sys.stdout.buffer.write(text[start:start+700].encode('utf-8'))
