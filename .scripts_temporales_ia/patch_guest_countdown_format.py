import re

filename = 'dev.html'
with open(filename, 'r', encoding='utf-8') as f:
    html = f.read()

# We need to replace the `if (diff <= limite...` block inside `iniciarRelojes()`.
old_logic = """            if (diff <= limite && diff > -14400000) { 
                el.innerHTML = " CERRADO (Empieza en menos de 15 min)";
                el.style.backgroundColor = "#fde8e8"; el.style.color = "var(--vcv-rojo)";
                if(eqId && !isGuestMode) {
                    const divInputs = document.getElementById(`inputs_eq_${eqId}`);
                    if(divInputs) divInputs.querySelectorAll('input, select').forEach(i => i.disabled = true);
                }
            } else if (diff <= -14400000) {
                el.innerHTML = " Partido en curso o Finalizado";
                el.style.backgroundColor = "#e9ecef"; el.style.color = "#495057";
            } else {
                let diffToClose = diff - limite; 
                let d = Math.floor(diffToClose / (1000 * 60 * 60 * 24));
                let h = Math.floor((diffToClose % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                let m = Math.floor((diffToClose % (1000 * 60 * 60)) / (1000 * 60));
                let s = Math.floor((diffToClose % (1000 * 60)) / 1000);
                el.innerHTML = ` Se cierra en: ${d}d ${h}h ${m}m ${s}s`;
                el.style.backgroundColor = "#e3f2fd"; el.style.color = "#1565c0";
            }"""

new_logic = """            if (isGuestMode) {
                if (diff <= 0 && diff > -14400000) {
                    el.innerHTML = "⏱️ Partido en curso";
                    el.style.backgroundColor = "#fde8e8"; el.style.color = "var(--vcv-rojo)";
                } else if (diff <= -14400000) {
                    el.innerHTML = "🏁 Partido Finalizado";
                    el.style.backgroundColor = "#e9ecef"; el.style.color = "#495057";
                } else {
                    let d = Math.floor(diff / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diff % (1000 * 60)) / 1000);
                    el.innerHTML = `⏳ Empieza en: ${d}d ${h}h ${m}m ${s}s`;
                    el.style.backgroundColor = "#e3f2fd"; el.style.color = "#1565c0";
                }
            } else {
                if (diff <= limite && diff > -14400000) { 
                    el.innerHTML = "🔒 CERRADO (Empieza en menos de 15 min)";
                    el.style.backgroundColor = "#fde8e8"; el.style.color = "var(--vcv-rojo)";
                    if(eqId) {
                        const divInputs = document.getElementById(`inputs_eq_${eqId}`);
                        if(divInputs) divInputs.querySelectorAll('input, select').forEach(i => i.disabled = true);
                    }
                } else if (diff <= -14400000) {
                    el.innerHTML = "🏁 Partido en curso o Finalizado";
                    el.style.backgroundColor = "#e9ecef"; el.style.color = "#495057";
                } else {
                    let diffToClose = diff - limite; 
                    let d = Math.floor(diffToClose / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diffToClose % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diffToClose % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diffToClose % (1000 * 60)) / 1000);
                    el.innerHTML = `🔒 Se cierra en: ${d}d ${h}h ${m}m ${s}s`;
                    el.style.backgroundColor = "#e3f2fd"; el.style.color = "#1565c0";
                }
            }"""

# Using regex to replace it robustly:
# Because of emojis and spaces, let's just find `if (diff <= limite && diff > -14400000) {` and replace up to `}` before `});`
idx_start = html.find('if (diff <= limite && diff > -14400000) {')
idx_end = html.find('});\n    }, 1000);')
if idx_start != -1 and idx_end != -1:
    # Need to go back a bit from idx_end to include the last `}`
    idx_end_bracket = html.rfind('}', idx_start, idx_end)
    html = html[:idx_start] + new_logic + '\n        ' + html[idx_end_bracket+1:]
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Patched guest countdown logic.")
else:
    print("Could not find countdown logic block.")

