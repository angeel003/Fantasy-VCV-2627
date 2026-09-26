with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Fix modal-card-v2 margin
text = re.sub(r' margin-top: calc\(20px \+ env\(safe-area-inset-top, 0px\)\);', '', text)

# Add padding to #loginSection directly in HTML instead of CSS, since it has no CSS
text = text.replace('<div id="loginSection">', '<div id="loginSection" style="padding-top: calc(20px + env(safe-area-inset-top, 0px));">')

# Fix header padding bottom to be larger so it doesn't cut text
text = text.replace('padding: calc(20px + env(safe-area-inset-top, 0px)) 20px 20px 20px;', 'padding: calc(18px + env(safe-area-inset-top, 0px)) 20px 26px 20px;')

# Ensure smooth scroll on login doesn't jump weirdly
# Wait, if "no se produce el auto desplazamiento al pulsar la seccion de FAQ"
# Let's check my event listener:
# masterFaq.addEventListener('toggle', function() { ... })
# Wait, details 'toggle' event fires immediately, maybe scrolling fails because it's not open yet? 
# In my previous script I used setTimeout 150ms. Let's change it to 300ms and use window.scrollTo manually to test, or just scrollIntoView with block: 'start'.
# Actually, the user says "no se produce". Why?
# Maybe `initTabsV2` is called before DOM is fully ready? No, `initTabsV2` is inside the script.
# Let's re-inject the event listener at the very end of the file or just inside DOMContentLoaded.

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed CSS formatting')
