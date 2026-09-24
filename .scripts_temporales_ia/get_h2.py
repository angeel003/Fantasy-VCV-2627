import re
with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

appSection = html[html.find('id="appSection"'):html.find('<!-- FAB MENU NAV')]
matches = re.finditer(r'<h[23][^>]*>.*?</h[23]>', appSection)
for m in matches:
    print(m.group(0).encode('utf-8').decode('utf-8', 'ignore'))

