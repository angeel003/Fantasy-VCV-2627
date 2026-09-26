import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Modify Header Sizes and Safe Area Puddings in CSS
text = text.replace('padding:  14px 18px;', 'padding: calc(20px + env(safe-area-inset-top, 0px)) 20px 20px 20px;')
text = text.replace('width:  44px; height:  44px;', 'width: 48px; height: 48px;')
text = text.replace('font-size: 1.2rem;', 'font-size: 1.25rem;')
# appSection padding
text = re.sub(r'(\#appSection\s*\{[^}]*padding-top:\s*)76px', r'\1calc(86px + env(safe-area-inset-top, 0px))', text)
# loginSection safe area
text = re.sub(r'(\#loginSection\s*\{[^}]*padding:\s*40px\s*20px;)', r'padding-top: calc(40px + env(safe-area-inset-top, 0px)); padding-bottom: 40px; padding-left: 20px; padding-right: 20px;', text)

# 2. Add scroll-margin-top to masterFaq in CSS (just append to its inline style or add class)
text = text.replace('id="masterFaq"', 'id="masterFaq" style="scroll-margin-top: calc(20px + env(safe-area-inset-top, 0px));"')

# 3. Add window.scrollTo(0,0) on Tab Switch
tab_switch = "if (target) target.classList.add('active-tab');"
tab_switch_new = tab_switch + "\n        window.scrollTo({ top: 0, behavior: 'smooth' });"
text = text.replace(tab_switch, tab_switch_new)

# 4. Add window.scrollTo(0,0) on Login success
login_hide = "document.getElementById('loginSection').style.display = \"none\";"
login_hide_new = login_hide + "\n            window.scrollTo({ top: 0, behavior: 'smooth' });"
text = text.replace(login_hide, login_hide_new)

# 5. Add Forgot Password to FAQ
faq_item = """
            <div class="faq-inner-item">
                <div class="faq-inner-title">¿Olvidaste tu usuario o contraseña?</div>
                <div>Si no recuerdas tus credenciales de acceso, no te preocupes. Escríbenos a nuestro correo de soporte técnico y te ayudaremos a recuperarlas: <br><a href="mailto:adminfantasyvcv@gmail.com" class="faq-email">adminfantasyvcv@gmail.com</a></div>
            </div>
"""
# Insert it at the end of the faq-content-v2 in login screen
# Wait, the end of faq-content-v2 has "Contacto y Problemas". Let's insert it before it, or just anywhere inside.
text = text.replace('<div class="faq-inner-item">\n                <div class="faq-inner-title">Contacto y Problemas</div>', 
                    faq_item + '\n            <div class="faq-inner-item">\n                <div class="faq-inner-title">Contacto y Problemas</div>')

# 6. Add JS listener for masterFaq scroll
js_listener = """
    // Scroll to top of FAQ when opened
    const masterFaq = document.getElementById('masterFaq');
    if(masterFaq) {
        masterFaq.addEventListener('toggle', function() {
            if(this.open) {
                setTimeout(() => {
                    this.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 150);
            }
        });
    }
"""
# Inject into the main <script> tag before it ends. 
text = text.replace('initTabsV2();', 'initTabsV2();\n' + js_listener)


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied UI and Scroll fixes.")
