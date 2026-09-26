import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Inject FAQ Item
faq_item = """
            <div class="faq-inner-item">
                <div class="faq-inner-title">¿Olvidaste tu usuario o contraseña?</div>
                <div>Si no recuerdas tus credenciales de acceso, no te preocupes. Escríbenos a nuestro correo de soporte técnico y te ayudaremos a recuperarlas: <br><a href="mailto:adminfantasyvcv@gmail.com" class="faq-email">adminfantasyvcv@gmail.com</a></div>
            </div>
"""
match = re.search(r'(<div class="faq-inner-title">.*?instalar la App\?</div>.*?</div>\s*</div>)', text, re.DOTALL)
if match:
    text = text.replace(match.group(1), match.group(1) + faq_item)

# 2. Inject scroll-margin-top to masterFaq
text = text.replace('id="masterFaq"', 'id="masterFaq" style="scroll-margin-top: calc(20px + env(safe-area-inset-top, 0px));"')

# 3. Inject auto-scroll JS for FAQ
new_script = """    // Add FAQ scroll behavior directly
    (function() {
        const masterFaq = document.getElementById('masterFaq');
        if(masterFaq) {
            masterFaq.addEventListener('toggle', function(e) {
                if(this.open) {
                    setTimeout(() => {
                        this.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 150);
                }
            });
        }
    })();
</script>
"""
start = text.rfind('</script>')
if start != -1:
    text = text[:start] + new_script + text[start+9:]

# 4. Hide content and add Construction message to 3 sections
construction_msg = """
    <div style="padding: 60px 20px; text-align: center; color: var(--text-muted);">
        <i data-lucide="hammer" style="width: 48px; height: 48px; color: var(--vcv-dorado); margin-bottom: 16px;"></i>
        <h3 style="color: var(--text-main); margin-bottom: 8px;">En construcción</h3>
        <p>¡Estoy trabajando en implementar esto cuanto antes! 😊</p>
    </div>
"""

def replace_section(section_id, content):
    pattern = r'(<section[^>]*id="' + section_id + r'"[^>]*>)(.*?)(</section>)'
    def replacer(m):
        return m.group(1) + construction_msg + '<div style="display:none;">' + m.group(2) + '</div>' + m.group(3)
    return re.sub(pattern, replacer, content, flags=re.DOTALL)

text = replace_section('clasificacionesSection', text)
text = replace_section('historialSection', text)
text = replace_section('calendarioSection', text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Applied safe changes')
