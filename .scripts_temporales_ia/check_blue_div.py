import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Locate the div start and the inserted title
idx_div = text.find('<div style="background-color: #e3f2fd;')
if idx_div != -1:
    print(text[max(0, idx_div-100):idx_div+300].encode('ascii', 'ignore').decode())

