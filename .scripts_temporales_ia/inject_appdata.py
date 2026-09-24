import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# For normal login
html = html.replace('currentJornadaGlobal = data.jornada;', 'currentJornadaGlobal = data.jornada;\n            window.appData = data;\n            if(window.initCalendar) window.initCalendar();')

# For guest login
html = html.replace('isGuestMode = true;', 'isGuestMode = true;\n            window.appData = data;\n            if(window.initCalendar) window.initCalendar();')

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
    print(f"Patched appData injection in {filename}")

