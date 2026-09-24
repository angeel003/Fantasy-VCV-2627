import re

css_slide_in = """
    @keyframes slideInLeft {
        0% { opacity: 0; transform: translateX(-50px); }
        100% { opacity: 1; transform: none; }
    }
    .slide-in-left {
        animation: slideInLeft 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    }
"""

js_old_click = """document.getElementById('btnLogout').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    localStorage.removeItem('vcv_cache_creds');
    
    document.getElementById('appSection').classList.add('slide-out-right');
    this.style.transform = 'translateY(-50%) translateX(-100%)'; // Hide tab as well
    
    setTimeout(() => {
        window.location.reload();
    }, 280);
});"""

js_new_click = """document.getElementById('btnLogout').addEventListener('click', function() {
    localStorage.removeItem('vcv_cache_data');
    localStorage.removeItem('vcv_cache_type');
    localStorage.removeItem('vcv_cache_creds');
    sessionStorage.setItem('vcv_slide_left', 'true');
    
    document.getElementById('appSection').classList.add('slide-out-right');
    this.style.transform = 'translateY(-50%) translateX(-100%)';
    
    setTimeout(() => {
        window.location.reload();
    }, 280);
});"""


for filename in ['dev.html', 'index.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Inject CSS for slide in
    if '.slide-in-left' not in html:
        html = html.replace('.slide-out-right {', css_slide_in + '\n    .slide-out-right {')
        
    # 2. Update Click handler
    html = html.replace(js_old_click, js_new_click)
    
    # 3. Add script check
    dom_check = """
  // Comprobar si venimos de darle al botón Atrás para hacer la animación de la izquierda
  if (sessionStorage.getItem('vcv_slide_left') === 'true') {
      document.getElementById('loginSection').classList.add('slide-in-left');
      sessionStorage.removeItem('vcv_slide_left');
  }
  """
    if 'vcv_slide_left' not in html:
        # inject right after const fetchSeguro ... block ends, or just after <script>
        html = html.replace('const scriptURL =', dom_check + '\n  const scriptURL =')
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

