import sys, re
with open('script-v2/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.findall(r'return ContentService\.createTextOutput\(JSON\.stringify\(\{.*?\}\)\)', text, re.DOTALL)
for i, m in enumerate(matches):
    sys.stdout.buffer.write(f'Match {i}: {m[:200]}...\n'.encode('utf-8'))
