with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_html = text.find('loginForm')
print('HTML:', text[max(0, start_html-200):start_html+800])

start_js = text.find("getElementById('loginForm').addEventListener('submit'")
if start_js == -1:
    start_js = text.find('loginForm') # fallback
print('JS:', text[max(0, start_js-100):start_js+500])
