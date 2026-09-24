import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()
    app = text[text.find('id="appSection"'):]
    matches = re.findall(r'<h[23][^>]*>.*?</h[23]>', app)
    for m in matches:
        print(m.encode('utf-8').decode('utf-8', 'ignore'))

