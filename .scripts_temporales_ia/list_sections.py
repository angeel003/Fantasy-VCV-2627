import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<div id="appSection".*?>(.*?)<div id="bottomNavWrapperV2"', text, re.DOTALL)
if m:
    html = m.group(1)
    sections = re.findall(r'<div\s+id="([^"]*?Section)"', html)
    print("Div sections:", sections)
    
    sections_tags = re.findall(r'<(div|section)\s+id="([^"]*?Section)"', html)
    print("All sections:", sections_tags)
