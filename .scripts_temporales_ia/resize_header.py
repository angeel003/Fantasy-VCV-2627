import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the HTML
old_header_html = """        <div>
          <div class="header-title-row">
            <h1 class="header-title-text">VCV PLAY</h1>
            <span class="header-title-badge">26/27</span>
          </div>
          <p class="header-subtitle">Club Voleibol Valencia</p>
        </div>"""

new_header_html = """        <div>
          <div class="header-title-row">
            <h1 class="header-title-text">VCV PLAY</h1>
            <span class="header-title-badge">26/27</span>
          </div>
          <div class="header-subtitle" style="display:flex; align-items:center; gap:5px; flex-wrap:wrap; margin-top:4px;">
            <span id="h2-user-name" style="color: #fff; font-weight:600;"></span>
            <span id="h2-user-handle" style="color: #a1a1aa; font-family:monospace; font-size:10px;"></span>
            <div id="h2-user-badges" style="display:flex; align-items:center; gap:3px;"></div>
          </div>
        </div>"""

text = text.replace(old_header_html, new_header_html)

# 2. Update CSS for slight size increase
text = re.sub(r'(\.app-header-v2 \{[^}]*padding: )12px 16px', r'\1 14px 18px', text)
text = re.sub(r'(\.header-logo-circle \{[^}]*width: )40px(; height: )40px', r'\1 44px\2 44px', text)
text = re.sub(r'(\.header-title-text \{[^}]*font-size: )1\.125rem', r'\1 1.2rem', text)
text = re.sub(r'(\.header-bell-btn \{[^}]*width: )36px(; height: )36px', r'\1 40px\2 40px', text)
text = re.sub(r'(\.header-user-chip \{[^}]*padding: )6px 10px', r'\1 8px 12px', text)

# In fix_ids, I had `nameEl.innerText = data.nombre_real || usr;`
# But the user specifically wants the handle too, which I also set: `handleEl.innerText = "@" + usr;`
# And badges: `badgesEl.innerHTML = insigniasHeaderHtml;`
# Let's verify that the guest mode has a handle update!
# Guest mode is updated in my fix_ids logic.

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Header customized")
