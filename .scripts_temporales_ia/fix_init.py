import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure DOMContentLoaded / login logic adds active-tab to both
# Currently it's:
# const firstSec = document.getElementById('carteleraSection');
# if (firstSec) firstSec.classList.add('active-tab');

old_init = r"""const firstSec = document.getElementById('carteleraSection');
        if (firstSec) firstSec.classList.add('active-tab');"""

new_init = r"""const firstSec = document.getElementById('carteleraSection');
        if (firstSec) firstSec.classList.add('active-tab');
        const tsSec = document.getElementById('prediccionesTotalesSection');
        if (tsSec) tsSec.classList.add('active-tab');"""

text = text.replace(old_init, new_init)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Init logic fixed!")
