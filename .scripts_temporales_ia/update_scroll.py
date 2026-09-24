import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the Cartelera section to have id="carteleraSection"
text = text.replace('<div id="appSection" style="display: none;">\n\n    \n\n    \n    <section>', '<div id="appSection" style="display: none;">\n\n    \n\n    \n    <section id="carteleraSection">')
text = text.replace('<div id="appSection" style="display: none;">\n\n    \n    <section>', '<div id="appSection" style="display: none;">\n\n    \n    <section id="carteleraSection">')
text = text.replace('<div id="appSection" style="display: none;">\n    <section>', '<div id="appSection" style="display: none;">\n    <section id="carteleraSection">')

# More robust regex replace:
text = re.sub(r'<div id="appSection"[^>]*>\s*<section>', '<div id="appSection" style="display: none;">\n    <section id="carteleraSection">', text)

# 2. Change the FAB link from #prediccionForm to #carteleraSection
text = text.replace('href="#prediccionForm"', 'href="#carteleraSection"')
# Also in checkFabVisibility() logic for visibility
text = text.replace("var cartelera = document.getElementById('prediccionForm');", "var cartelera = document.getElementById('carteleraSection');")

# 3. Add scroll-margin-top to section in CSS
css_injection = """    section { padding: 50px 15px; text-align: center; scroll-margin-top: calc(80px + env(safe-area-inset-top, 0px)); }"""
text = re.sub(r'section\s*\{\s*padding:\s*50px 15px;\s*text-align:\s*center;\s*\}', css_injection, text)

# Just in case it's different
if 'scroll-margin-top' not in text:
    text = text.replace('section { padding: 50px 15px; text-align: center; }', 'section { padding: 50px 15px; text-align: center; scroll-margin-top: calc(80px + env(safe-area-inset-top, 0px)); }')

with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated dev.html with scroll-margin-top and carteleraSection")
