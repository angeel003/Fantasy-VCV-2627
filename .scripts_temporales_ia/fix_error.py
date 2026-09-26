import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make the error message red background with white text, or just use inline styles on the loginMessage div.
text = text.replace('<div id="loginMessage" class="alert-box" style="margin-top:10px; display:none;"></div>', 
                    '<div id="loginMessage" class="alert-box" style="margin-top:10px; display:none; background-color:#ff4444; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold;"></div>')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Error message styling fixed.")
