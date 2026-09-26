import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('class="teams-versus-container-v2"')
end = text.find('</div>', text.find('</div>', text.find('</div>', text.find('</div>', start)+1)+1)+1)+6
sys.stdout.buffer.write(text[start:end+200].encode('utf-8'))
