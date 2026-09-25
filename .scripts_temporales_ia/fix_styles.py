import re

with open('v2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS variables to a Light Mode palette
light_mode_vars = """
    :root {
      --primary-color: #783b7a;
      --primary-hover: #5d2d5f;
      --secondary-color: #bd9b53;
      --secondary-hover: #a38546;
      --bg-surface: #f3f4f6; /* Light gray background */
      --bg-card: #ffffff; /* White card */
      --bg-card-alt: #f9fafb; /* Slightly off-white for internal boxes */
      --bg-input: #ffffff;
      --border-color: #e5e7eb;
      --border-glow: rgba(189, 155, 83, 0.4);
      --text-main: #1f2937; /* Dark gray */
      --text-muted: #6b7280;
      --text-gold: #b48c36;
      --success: #059669;
      --danger: #dc2626;
      --badge-admin: #d97706;
      --safe-top: env(safe-area-inset-top, 0px);
      --safe-bottom: env(safe-area-inset-bottom, 16px);
    }
"""

html = re.sub(r':root\s*\{[^}]+\}', light_mode_vars.strip(), html)

# 2. Fix some text colors in CSS
html = html.replace("color: #fff;", "color: var(--text-main);")
html = html.replace("background: linear-gradient(145deg, #2b1138, #1a0b1e);", "background: var(--bg-card);")
html = html.replace("background: rgba(106, 44, 112, 0.2);", "background: rgba(120, 59, 122, 0.1);")
html = html.replace("border: 1px solid rgba(212, 175, 55, 0.3);", "border: 1px solid var(--secondary-color);")

# Remove hardcoded dark inline gradients
html = re.sub(r'background:\s*linear-gradient\([^)]+\);', 'background: var(--bg-card);', html)
# Make inputs explicitly have a border
html = html.replace("border: 1px solid var(--border-color);", "border: 1px solid var(--border-color); background: var(--bg-input); color: var(--text-main);")

# Change some hardcoded label colors
html = html.replace("color: #b7a4be;", "color: var(--text-muted);")
html = html.replace("color: #f3ce5e;", "color: var(--text-gold);")
html = html.replace("background: #1d0d21;", "background: var(--bg-surface);")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(html)
