import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<div class="faq-container"')
sys.stdout.buffer.write(text[start-50:start+2000].encode('utf-8'))
