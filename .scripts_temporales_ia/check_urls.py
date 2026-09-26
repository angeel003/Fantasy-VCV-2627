import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text2 = f.read()
with open('index.html', 'r', encoding='utf-8') as f:
    text1 = f.read()

m2 = re.search(r'const scriptURL\s*=\s*"(.*?)"', text2)
m1 = re.search(r'const scriptURL\s*=\s*"(.*?)"', text1)

print('V2 URL:', m2.group(1) if m2 else 'None')
print('V1 URL:', m1.group(1) if m1 else 'None')
