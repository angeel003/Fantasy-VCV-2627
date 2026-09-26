import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# --- 1. Extract Admin Panel ---
admin_regex = re.compile(r'<!-- CAJA SECRETA DE INTRANET \(SOLO ADMINS\) -->.*?<div id="adminPanelWrapper".*?(<details>.*?</details>).*?</div>', re.DOTALL)
admin_match = admin_regex.search(text)
admin_inner_html = ""
if admin_match:
    # Just extract the inner content of the details tag or the whole thing
    details_content_regex = re.search(r'<div style="margin-top: 20px;">(.*?)</div>\s*</details>', admin_match.group(1), re.DOTALL)
    if details_content_regex:
        admin_inner_html = details_content_regex.group(1)
    # Remove from original location
    text = text[:admin_match.start()] + text[admin_match.end():]

# Create the new Admin Card
admin_card = f"""
<div class="vcv-card-v2" id="adminPanelWrapper" style="display:none; margin-bottom: 20px;">
    <div class="header-eq" style="background:var(--vcv-dorado); color:#000;">
        <h3 style="color:#000;"><i data-lucide="settings" style="color:#000;"></i> Intranet Administrador</h3>
    </div>
    <div style="padding:15px;">
        {admin_inner_html}
    </div>
</div>
"""

# --- 2. Extract FAQ and Settings ---
# We will extract "Gestionar mi contraseña" and "Cambiar mi usuario / nombre"
pwd_regex = re.compile(r'<div class="faq-inner-item">\s*<div class="faq-inner-title">Gestionar mi contrase.*?</div>.*?</div>\s*</div>', re.DOTALL)
name_regex = re.compile(r'<div class="faq-inner-item">\s*<div class="faq-inner-title">Cambiar mi usuario / nombre.*?</div>.*?</div>\s*</div>', re.DOTALL)

pwd_match = pwd_regex.search(text)
name_match = name_regex.search(text)

pwd_html = pwd_match.group(0) if pwd_match else ""
name_html = name_match.group(0) if name_match else ""

# Remove them from the original FAQ container on the login screen
if pwd_match:
    text = text.replace(pwd_match.group(0), "")
if name_match:
    text = text.replace(name_match.group(0), "")

# We should also extract the remaining FAQ questions to put them in the Profile?
# The user said "los apartados del faq y gestion ... pero solamente los de cambio de contraseña..."
# I will put them in a "Gestión de Cuenta" card.
settings_card = f"""
<div class="vcv-card-v2" style="margin-bottom: 20px;">
    <div class="header-eq">
        <h3><i data-lucide="user-cog"></i> Gestión de Cuenta</h3>
    </div>
    <div style="padding:15px; display:flex; flex-direction:column; gap:15px;">
        {pwd_html}
        {name_html}
    </div>
</div>
"""

# Wait, if they wanted the FAQ too, I will extract the rest of the FAQ? 
# "pongas en la pestaña de perfil los apartados del faq y gestion de la pantalla de inicio de sesión pero solamente os de cambio de contraseña y cambio de nobre de usuario o nombre real."
# Actually, if I read it literally: "put in the profile tab the sections of FAQ and Management from the login screen, BUT ONLY the change password and change name ones".
# This means DO NOT put the FAQ in the profile tab, ONLY put the password and name ones!
# "los apartados del faq y gestion de la pantalla de inicio de sesion" is the name of the section ("Preguntas Frecuentes y Gestión"). So they are referring to that section by name! They want me to take from that section ONLY the password and name change!
# Yes! "Preguntas Frecuentes y Gestión" is the exact name of the `<summary>`!
# So I leave the rest of the FAQ on the login screen!

# --- 3. Inject into enlacesRfevbSection ---
enlaces_regex = re.compile(r'(<section id="enlacesRfevbSection".*?>\s*<h2>.*?</h2>\s*<p.*?>.*?</p>)(.*?)(</section>)', re.DOTALL)

def enlaces_replacer(match):
    # match.group(1) is the <section> header and paragraph
    # match.group(2) is the inner container with RFEVB links
    # match.group(3) is </section>
    
    # We will prepend the Admin Card and Settings Card inside the section
    # And maybe wrap the RFEVB links in a vcv-card-v2 as well to match the styling
    
    rfevb_links = match.group(2)
    # Let's wrap RFEVB links in a card too for consistency
    rfevb_card = f"""
    <div class="vcv-card-v2" style="margin-bottom: 20px;">
        <div class="header-eq">
            <h3><i data-lucide="external-link"></i> Enlaces Oficiales</h3>
        </div>
        <div style="padding:15px;">
            {rfevb_links}
        </div>
    </div>
    """
    
    # Remove the old h2 and p from the section, since we have cards now
    section_start = '<section id="enlacesRfevbSection" style="display:none; padding-bottom:30px;">\n'
    
    return section_start + admin_card + settings_card + rfevb_card + match.group(3)

text = enlaces_regex.sub(enlaces_replacer, text)

# Clean up any leftover empty <div class="faq-content-v2"> if needed (it won't be empty, has other FAQs)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Profile tab built successfully.")
