import sys
import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="enlacesRfevbSection"')
sys.stdout.buffer.write(text[start-50:start+1000].encode('utf-8'))
