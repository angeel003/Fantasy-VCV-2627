import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'if \(action === "login" \|\| action === "get_data"\).*?return ContentService', text, re.DOTALL)
if match:
    sys.stdout.buffer.write(text[max(0, match.start()-100):min(len(text), match.end()+200)].encode('utf-8'))
