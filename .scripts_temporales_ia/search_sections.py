import sys

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

def print_element(search_str):
    start = text.find(search_str)
    if start != -1:
        sys.stdout.buffer.write(f"\n--- FOUND {search_str} ---\n".encode('utf-8'))
        sys.stdout.buffer.write(text[max(0, start-100):start+1500].encode('utf-8'))
    else:
        sys.stdout.buffer.write(f"\n--- NOT FOUND {search_str} ---\n".encode('utf-8'))

print_element('id="adminPanelContainer"')
print_element('Contraseña')
print_element('nombre real')
