import re
with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

appSection = html[html.find('id="appSection"'):]
matches = re.finditer(r'<(section|form|div)[^>]*id=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</\1>', appSection, re.DOTALL)
for m in matches:
    id_val = m.group(2)
    title_match = re.search(r'<h[23][^>]*>(.*?)</h[23]>', m.group(3))
    if title_match:
        title = title_match.group(1).strip()
        # ignore nested small divs
        if 'Section' in id_val or 'Form' in id_val or 'links' in id_val.lower():
            print(f'{id_val}: {title}')

