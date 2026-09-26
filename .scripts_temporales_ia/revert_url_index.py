import sys, re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()
    
# Replace it back to the original V1 URL
old_url = 'https://script.google.com/macros/s/AKfycbyw9L6Te3q2ibdRBaaAwaiPpEPWLbsNdb8JA9yO272DBHgxaZA2l3TLkH9ofAXlQiWfAg/exec'
new_text = re.sub(r'const scriptURL\s*=\s*[\'\"]https://script\.google\.com/[^\'\"]+[\'\"];', f'const scriptURL = "{old_url}";', text)

with open('index.html', 'w', encoding='utf-8') as f2:
    f2.write(new_text)
print("\nReverted index.html URL to V1")
