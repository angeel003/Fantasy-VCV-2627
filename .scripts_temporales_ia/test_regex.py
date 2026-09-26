import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'(<span class="team-role-v2"[^>]*>VISITANTE</span>\s*</div>\s*</div>)', text)
if match:
    sys.stdout.buffer.write(match.group(1).encode('utf-8'))
