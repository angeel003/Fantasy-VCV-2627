import sys, re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
if 'sincronizarPuntosV2' in text:
    print('SUCCESS! Sync func exists')
else:
    print('FAILED to add sync func')

if '<input type="number" id="val-v2-' in text:
    print('SUCCESS! Input exists')
else:
    print('FAILED to add input')
