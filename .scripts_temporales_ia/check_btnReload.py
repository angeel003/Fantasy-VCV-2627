with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
print('btnReload count:', text.count('id="btnReload"'))
