import re

dom_check = """
  // Comprobar si venimos de darle al botón Atrás para hacer la animación de la izquierda
  if (sessionStorage.getItem('vcv_slide_left') === 'true') {
      document.getElementById('loginSection').classList.add('slide-in-left');
      sessionStorage.removeItem('vcv_slide_left');
  }
"""

for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'Comprobar si venimos' not in html:
        html = re.sub(r'(const scriptURL\s*=)', dom_check + r'\n\1', html)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

