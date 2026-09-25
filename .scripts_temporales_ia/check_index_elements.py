with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('index btnChangePwd:', text.count('id="btnChangePwd"'))
print('index btnReqName:', text.count('id="btnReqName"'))
