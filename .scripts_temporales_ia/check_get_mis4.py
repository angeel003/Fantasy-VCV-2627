import sys
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('if (action === "get_mis_predicciones")')
sys.stdout.buffer.write(text[start:start+1500].encode('utf-8'))
