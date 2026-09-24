import re
with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

for m in re.finditer(r'<([a-z]+)[^>]*id=[\'"]([^\'"]+)[\'"]', html):
    id_val = m.group(2)
    if 'cartelera' in id_val.lower() or 'partido' in id_val.lower() or 'pred' in id_val.lower():
        print(id_val)

