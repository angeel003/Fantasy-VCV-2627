with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Count btnLogin:', text.count('id="btnLogin"'))
print('Count loginUsuario:', text.count('id="loginUsuario"'))
print('Count loginSection:', text.count('id="loginSection"'))
