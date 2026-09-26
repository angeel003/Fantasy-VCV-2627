import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find("document.getElementById('btnLogin').addEventListener")
sys.stdout.buffer.write(text[start:start+1500].encode('utf-8'))
