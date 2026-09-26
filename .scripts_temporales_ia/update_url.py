import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'const scriptURL\s*=\s*[\'\"](https://script\.google\.com/[^\'\"]+)[\'\"];?', text)
if match:
    sys.stdout.buffer.write(match.group(0).encode('utf-8'))
    
    # Replace it!
    new_url = 'https://script.google.com/macros/s/AKfycbypusqyphzLfam-6xra5BCVAFXqGxOA-RMjVuZOAJyp4OQ5CCR_xZs-dT5tIy4EcZIEKQ/exec'
    new_text = text[:match.start(1)] + new_url + text[match.end(1):]
    with open('v2.html', 'w', encoding='utf-8') as f2:
        f2.write(new_text)
    print("\nUpdated v2.html")
