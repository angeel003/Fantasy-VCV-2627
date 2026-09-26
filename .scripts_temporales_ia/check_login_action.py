import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'if \(action === "login"', text)
if match:
    sys.stdout.buffer.write(text[max(0, match.start()-100):min(len(text), match.end()+500)].encode('utf-8'))
