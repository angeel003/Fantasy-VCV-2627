with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
while True:
    idx = text.find('data.status === "success"', idx)
    if idx == -1: break
    print('Found at', idx)
    idx += 1
