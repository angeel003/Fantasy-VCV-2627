import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add window.scrollTo(0,0) on Tab Switch
tab_switch = "if (target) target.classList.add('active-tab');"
tab_switch_new = tab_switch + "\\n        window.scrollTo({ top: 0, behavior: 'smooth' });"
text = text.replace(tab_switch, tab_switch_new)

# Add window.scrollTo(0,0) on Login success
login_hide = "document.getElementById('loginSection').style.display = \\\"none\\\";"
login_hide_new = login_hide + "\\n            window.scrollTo({ top: 0, behavior: 'smooth' });"
text = text.replace(login_hide, login_hide_new)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied scroll fixes.")
