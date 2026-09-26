import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the warning message in the HTML
warning_pattern = r'<div id="warningPredicciones" style="background-color:#fde8e8; border: 1px solid var\(--vcv-rojo\); border-radius: 8px; padding: 12px; margin-top: 25px; margin-bottom: 15px; text-align: center;">\s*<p style="color:var\(--vcv-rojo\); font-size:0\.95rem; font-weight:bold; margin:0;">\s*⚠️ ATENCIÓN: Las predicciones se cerrarán automáticamente 15 minutos antes de la hora oficial de comienzo de cada partido.\s*</p>\s*</div>'
text = re.sub(warning_pattern, '', text)

# Just in case the color is different in dark mode, try a generic search
warning_generic = r'<div id="warningPredicciones"[^>]*>.*?15 minutos.*?</div>'
text = re.sub(warning_generic, '', text, flags=re.DOTALL)

# 2. Change limite = 15 * 60 * 1000; to limite = 0;
text = text.replace('const limite = 15 * 60 * 1000;', 'const limite = 0;')

# 3. Modify the countdown string in logged in mode
old_countdown_logic = """                    let diffLimit = diff - limite;
                    let d = Math.floor(diffLimit / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diffLimit % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diffLimit % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diffLimit % (1000 * 60)) / 1000);
                    if (d > 0) {
                        applyStyle('rgba(212,175,55,0.1)', yellow, ` Se cierra en: ${d}d ${h}h`);
                    } else if (h > 0) {
                        applyStyle('rgba(212,175,55,0.1)', yellow, ` Se cierra en: ${h}h ${m}m`);
                    } else if (m > 0) {
                        applyStyle('rgba(231,76,60,0.1)', red, ` Se cierra en: ${m}m ${s}s`);
                    } else {
                        applyStyle('rgba(231,76,60,0.1)', red, ` Se cierra en: ${s}s`);
                    }"""

new_countdown_logic = """                    let diffLimit = diff - limite;
                    let d = Math.floor(diffLimit / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diffLimit % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diffLimit % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diffLimit % (1000 * 60)) / 1000);
                    let timeStr = "";
                    if (d > 0) timeStr = `${d}d ${h}h ${m}m ${s}s`;
                    else if (h > 0) timeStr = `${h}h ${m}m ${s}s`;
                    else if (m > 0) timeStr = `${m}m ${s}s`;
                    else timeStr = `${s}s`;
                    
                    if (d > 0 || h > 0) {
                        applyStyle('rgba(212,175,55,0.1)', yellow, ` Faltan: ${timeStr}`);
                    } else {
                        applyStyle('rgba(231,76,60,0.1)', red, ` Faltan: ${timeStr}`);
                    }"""

text = text.replace(old_countdown_logic, new_countdown_logic)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
    
print("Updated timer logic")
