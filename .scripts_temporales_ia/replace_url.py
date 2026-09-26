import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the V2 script URL with the official V1 script URL
v2_url = "https://script.google.com/macros/s/AKfycbypusqyphzLfam-6xra5BCVAFXqGxOA-RMjVuZOAJyp4OQ5CCR_xZs-dT5tIy4EcZIEKQ/exec"
v1_url = "https://script.google.com/macros/s/AKfycbyw9L6Te3q2ibdRBaaAwaiPpEPWLbsNdb8JA9yO272DBHgxaZA2l3TLkH9ofAXlQiWfAg/exec"

text = text.replace(v2_url, v1_url)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("URL replaced in v2.html")
