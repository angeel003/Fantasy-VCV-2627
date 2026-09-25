import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.finditer(r'(?i)<button[^>]+>.*?(ranking|clasificaciones|partidos|historial).*?</button>', text)
for m in matches:
    print(m.group(0).encode('ascii', 'ignore').decode('ascii'))
