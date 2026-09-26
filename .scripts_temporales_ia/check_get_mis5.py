import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'if \(action === "get_mis_predicciones"\)', text)
if match:
    sys.stdout.buffer.write(text[max(0, match.start()):min(len(text), match.end()+1000)].encode('utf-8'))
