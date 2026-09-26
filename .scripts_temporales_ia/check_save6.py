import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'if \(action === "save"\).*?if \(action === "load"\)', text, re.DOTALL)
if match:
    sys.stdout.buffer.write(match.group(0).encode('utf-8'))
