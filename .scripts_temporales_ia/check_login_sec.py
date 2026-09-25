with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('<section id="loginSection"')
end = text.find('</section>', start) + len('</section>')

print(text[start:start+500])
