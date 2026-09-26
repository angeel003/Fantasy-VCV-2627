with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

faq_item = """
            <div class="faq-inner-item">
                <div class="faq-inner-title">¿Olvidaste tu usuario o contraseña?</div>
                <div>Si no recuerdas tus credenciales de acceso, no te preocupes. Escríbenos a nuestro correo de soporte técnico y te ayudaremos a recuperarlas: <br><a href="mailto:adminfantasyvcv@gmail.com" class="faq-email">adminfantasyvcv@gmail.com</a></div>
            </div>
"""

# Find the end of the FAQ list
# The last one on the login screen is "¿Cómo instalar la App?". Let's insert it after that.
import re
match = re.search(r'(<div class="faq-inner-title">.*?instalar la App\?</div>.*?</div>\s*</div>)', text, re.DOTALL)
if match:
    text = text.replace(match.group(1), match.group(1) + faq_item)
    with open('v2.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Injected FAQ item successfully.")
else:
    print("Failed to find injection point.")
