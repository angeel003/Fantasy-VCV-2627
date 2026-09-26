import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_guest_logic = """                    let d = Math.floor(diff / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diff % (1000 * 60)) / 1000);
                    applyStyle('rgba(52,152,219,0.1)', blue, ` Empieza en: ${d}d ${h}h ${m}m ${s}s`);"""

new_guest_logic = """                    let d = Math.floor(diff / (1000 * 60 * 60 * 24));
                    let h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    let m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                    let s = Math.floor((diff % (1000 * 60)) / 1000);
                    let timeStr = "";
                    if (d > 0) timeStr = `${d}d ${h}h ${m}m ${s}s`;
                    else if (h > 0) timeStr = `${h}h ${m}m ${s}s`;
                    else if (m > 0) timeStr = `${m}m ${s}s`;
                    else timeStr = `${s}s`;
                    applyStyle('rgba(52,152,219,0.1)', blue, ` Empieza en: ${timeStr}`);"""

text = text.replace(old_guest_logic, new_guest_logic)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated guest timer logic")
