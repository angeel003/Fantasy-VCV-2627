import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
if 'details class="vcv-faq-master"' in text and 'let htmlTot = ``;' in text:
    print('SUCCESS')
else:
    print('FAILED')
