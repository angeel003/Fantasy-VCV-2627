with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js">')
if idx != -1:
    print(text[max(0, idx-1000):idx])
else:
    print("Not found")
