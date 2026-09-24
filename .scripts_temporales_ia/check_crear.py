import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function crearUsuarioAdmin')
if idx != -1:
    end_idx = text.find('}', idx)
    func_body = text[idx:end_idx+100]
    print(func_body.encode('ascii', 'ignore').decode())

