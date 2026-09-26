import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'if \(action === "clear_cache"\)', text)
if match:
    sys.stdout.buffer.write(text[max(0, match.start()-50):min(len(text), match.end()+500)].encode('utf-8'))
