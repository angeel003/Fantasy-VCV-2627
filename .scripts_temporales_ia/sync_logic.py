import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Update cargarDatosAntiguos sync logic for the new Empate and Team buttons
old_sync = r"""if (preds[idPart].signo) {
                    const signoVal = preds[idPart].signo;
                    if (signoVal === "A favor") {
                        const btn = document.getElementById(`signo-plus-v2-${idPart}`);
                        if (btn) btn.classList.add('selected');
                    } else if (signoVal === "En contra") {
                        const btn = document.getElementById(`signo-minus-v2-${idPart}`);
                        if (btn) btn.classList.add('selected');
                    }
                }"""

new_sync = r"""if (preds[idPart].signo) {
                    const signoVal = preds[idPart].signo;
                    if (signoVal === "A favor") {
                        const btn = document.querySelector(`button[id^="signo-"][id$="-${idPart}"][onclick*=" true)"]`);
                        if (btn) btn.classList.add('selected');
                    } else if (signoVal === "En contra") {
                        const btn = document.querySelector(`button[id^="signo-"][id$="-${idPart}"][onclick*=" false)"]`);
                        if (btn) btn.classList.add('selected');
                    } else if (signoVal === "Empate") {
                        const btnPlus = document.getElementById(`signo-plus-v2-${idPart}`);
                        const btnMinus = document.getElementById(`signo-minus-v2-${idPart}`);
                        if(btnPlus) { btnPlus.classList.add('tied-btn'); btnPlus.disabled = true; }
                        if(btnMinus) { btnMinus.classList.add('tied-btn'); btnMinus.disabled = true; }
                    }
                }"""
text = text.replace(old_sync, new_sync)


# Also ensure that when we sync points, if it's 0 we do the right thing:
old_points_sync = r"""if (preds[idPart].puntos) {
                    const span = document.getElementById(`val-v2-${idPart}`);
                    if (span) span.innerText = preds[idPart].puntos;
                }"""

new_points_sync = r"""if (preds[idPart].puntos !== undefined) {
                    const span = document.getElementById(`val-v2-${idPart}`);
                    if (span) span.innerText = preds[idPart].puntos;
                    // If it's 0, we can also force the tied state just in case
                    if (parseInt(preds[idPart].puntos) === 0) {
                        const btnPlus = document.getElementById(`signo-plus-v2-${idPart}`);
                        const btnMinus = document.getElementById(`signo-minus-v2-${idPart}`);
                        if(btnPlus) { btnPlus.classList.add('tied-btn'); btnPlus.disabled = true; }
                        if(btnMinus) { btnMinus.classList.add('tied-btn'); btnMinus.disabled = true; }
                    }
                }"""
text = text.replace(old_points_sync, new_points_sync)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated sync logic.")
