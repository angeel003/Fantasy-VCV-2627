import re

with open('v2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace root variables
refined_dark_mode = """
    :root {
      --primary-color: #783b7a;
      --primary-hover: #904c92;
      --secondary-color: #bd9b53;
      --secondary-hover: #d2b26a;
      
      /* Refined Dark Mode (less deep purple, more neutral/lighter darks) */
      --bg-surface: #1e1b24; 
      --bg-card: #2a2631; 
      --bg-card-alt: #383340; 
      --bg-input: #ffffff; /* White inputs for contrast! */
      
      --border-color: #534c5f;
      --border-glow: rgba(189, 155, 83, 0.4);
      
      --text-main: #ffffff;
      --text-muted: #b4aebf;
      --text-gold: #e5cd85;
      
      --success: #2ecc71;
      --danger: #e74c3c;
      --badge-admin: #e67e22;
      --safe-top: env(safe-area-inset-top, 0px);
      --safe-bottom: env(safe-area-inset-bottom, 16px);
    }
"""

html = re.sub(r':root\s*\{[^}]+\}', refined_dark_mode.strip(), html)

# If input background is white, text in input needs to be dark
input_css_fix = """
    .form-control {
      background-color: var(--bg-input);
      border: 1px solid var(--border-color);
      color: #1a1a1a;
      font-weight: 500;
"""
html = html.replace(".form-control {\n      background-color: var(--bg-input);\n      border: 1px solid var(--border-color);\n      color: var(--text-main);", input_css_fix)

# We might also want to change some backgrounds that are too dark in the inline styles
html = html.replace("background: linear-gradient(135deg, #26102c 0%, #15081a 100%);", "background: linear-gradient(135deg, #3d2b45 0%, #2a1c31 100%);")
html = html.replace("background: linear-gradient(145deg, #2b1138, #1a0b1e);", "background: linear-gradient(145deg, #382542, #241629);")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(html)
