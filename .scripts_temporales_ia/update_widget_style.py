import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the top margin and the target predictions text
old_widget_top = r'<div style="padding: 16px; border-radius: 16px; background: linear-gradient\(to right, rgba\(93, 23, 137, 0\.4\), var\(--bg-card\), var\(--bg-card\)\); border: 1px solid var\(--border-color\); position: relative; overflow: hidden; box-shadow: 0 4px 6px -1px rgba\(0,0,0,0\.1\), 0 2px 4px -1px rgba\(0,0,0,0\.06\); margin-bottom: 20px;">\s*<div style="display: flex; align-items: center; justify-content: space-between; font-size: 0\.75rem; margin-bottom: 12px;">\s*<span style="display: inline-flex; align-items: center; font-weight: bold; padding: 3px 10px; border-radius: 9999px; background: rgba\(16, 185, 129, 0\.15\); color: #10b981; border: 1px solid rgba\(16, 185, 129, 0\.3\);">\s*<span style="width: 6px; height: 6px; border-radius: 9999px; background: #10b981; margin-right: 6px; animation: pulse 2s cubic-bezier\(0\.4, 0, 0\.6, 1\) infinite;"></span> Jornada \$\{data\.jornada \|\| "Activa"\}\s*</span>\s*<span style="display: flex; align-items: center; color: var\(--vcv-dorado\); font-weight: 700;">\s*<span style="margin-right: 4px;">🎯</span> \$\{predictedOpen\}/\$\{totalOpen\} Predicciones\s*</span>\s*</div>'

new_widget_top = r"""<div style="padding: 14px; border-radius: 16px; background: linear-gradient(to right, rgba(93, 23, 137, 0.4), var(--bg-card), var(--bg-card)); border: 1px solid var(--border-color); position: relative; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); margin-top: -12px; margin-bottom: 20px;">
              <div style="display: flex; align-items: center; justify-content: flex-start; font-size: 0.75rem; margin-bottom: 12px;">
                <span style="display: inline-flex; align-items: center; font-weight: bold; padding: 3px 10px; border-radius: 9999px; background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3);">
                  <span style="width: 6px; height: 6px; border-radius: 9999px; background: #10b981; margin-right: 6px; animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;"></span> Jornada ${data.jornada || "Activa"}
                </span>
              </div>"""

if re.search(old_widget_top, text):
    text = re.sub(old_widget_top, new_widget_top, text)
else:
    print("Warning: old_widget_top not found")


# 2. Update font size and layout of greeting
old_greeting = r'<h2 style="font-size: 1\.15rem; font-weight: bold; color: var\(--text-main\); margin:0;">¡Hola \$\{data\.nombre_real \|\| currentUser\}!</h2>'
new_greeting = r'<h2 style="font-size: 1.55rem; font-weight: 800; color: var(--text-main); margin:0; letter-spacing:-0.5px; line-height:1.1;">¡Hola ${data.nombre_real || currentUser}!</h2>'

if re.search(old_greeting, text):
    text = re.sub(old_greeting, new_greeting, text)
else:
    print("Warning: old_greeting not found")


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated v2.html script executed')
