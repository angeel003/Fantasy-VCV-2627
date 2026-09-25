with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

elements = [
    'btnReload', 'btnAdminSync', 'btnChangePwd', 'btnReqName', 
    'btnLogin', 'btnGuest', 'mobileTooltip', 'toastNotification'
]
for e in elements:
    print(f'{e}:', text.count(f'id="{e}"'))
