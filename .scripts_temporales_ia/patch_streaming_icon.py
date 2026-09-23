import re

with open('dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the large buttons completely
btn_regex = r"\$\{eq\.streaming \? `<a href=\"\$\{eq\.streaming\}\" target=\"_blank\" class=\"btn btn-sm btn-danger\" style=\"font-weight:bold; border-radius:20px; padding:3px 12px; margin-bottom:10px; display:inline-block;\">▶️ Ver Streaming Oficial</a>` : ''\}"
html = re.sub(btn_regex, "", html)


# 2. Update Guest `infoLocFecha`
guest_old = r"let infoLocFecha = \(iconoLoc \|\| eq\.timestamp\) \? `<div style=\"font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;\">\$\{iconoLoc\} \$\{formatFecha\(eq\.timestamp\)\}</div>` : \"\";"
guest_new = r"""let streamIcon = eq.streaming ? ` <a href="${eq.streaming}" target="_blank" style="color:#d32f2f; text-decoration:none; margin-left:6px; font-size:1.1rem;" title="Ver Streaming Oficial">▶️</a>` : "";
                  let infoLocFecha = (iconoLoc || eq.timestamp) ? `<div style="font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;">${iconoLoc} ${formatFecha(eq.timestamp)}${streamIcon}</div>` : (streamIcon ? `<div style="margin-bottom:4px;">${streamIcon}</div>` : "");"""
html = html.replace(
    'let infoLocFecha = (iconoLoc || eq.timestamp) ? `<div style="font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;">${iconoLoc} ${formatFecha(eq.timestamp)}</div>` : "";', 
    guest_new
)


# 3. Update User `infoLocFecha`
user_old = r"""let infoLocFecha = "";
                    if\(iconoLoc \|\| eq\.timestamp\) \{
                        infoLocFecha = `<div style="font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;">\$\{iconoLoc\} \$\{formatFecha\(eq\.timestamp\)\}</div>`;
                    \}"""
user_new = r"""let streamIcon = eq.streaming ? ` <a href="${eq.streaming}" target="_blank" style="color:#d32f2f; text-decoration:none; margin-left:6px; font-size:1.1rem;" title="Ver Streaming Oficial">▶️</a>` : "";
                    let infoLocFecha = (iconoLoc || eq.timestamp) ? `<div style="font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;">${iconoLoc} ${formatFecha(eq.timestamp)}${streamIcon}</div>` : (streamIcon ? `<div style="margin-bottom:4px;">${streamIcon}</div>` : "");"""
html = re.sub(user_old, user_new, html)

# Alternative if the regex for User failed (sometimes whitespace is tricky):
html = html.replace("""let infoLocFecha = "";
                    if(iconoLoc || eq.timestamp) {
                        infoLocFecha = `<div style="font-size:0.9rem; color:#555; margin-bottom:4px; font-weight:bold;">${iconoLoc} ${formatFecha(eq.timestamp)}</div>`;
                    }""", user_new)


with open('dev.html', 'w', encoding='utf-8') as f:
    f.write(html)

