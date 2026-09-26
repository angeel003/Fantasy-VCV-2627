import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update padding-top of #appSection
text = re.sub(r'#appSection\s*\{\s*padding-top:\s*76px;', r'#appSection {\n        padding-top: 60px;', text)

# 2. Update scroll behavior in switchTabV2
text = re.sub(r"window\.scrollTo\(\{ top: 0, behavior: 'smooth' \}\);", r"window.scrollTo(0, 0); setTimeout(() => window.scrollTo(0, 0), 10);", text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated v2.html")
