import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('// If it')
sys.stdout.buffer.write(text[start:start+500].encode('utf-8'))
