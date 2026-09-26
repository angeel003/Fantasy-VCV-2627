import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Populate hidden inputs with existing predictions (pSets, pPts, pSig)
old_hidden = """<!-- HIDDEN INPUTS -->
                            <input type="hidden" id="e${eq.id_partido}_sets" value="">
                            <input type="hidden" id="e${eq.id_partido}_puntos" value="14">
                            <input type="hidden" id="e${eq.id_partido}_signo" value="">"""

new_hidden = """<!-- HIDDEN INPUTS -->
                            <input type="hidden" id="e${eq.id_partido}_sets" value="${pSets}">
                            <input type="hidden" id="e${eq.id_partido}_puntos" value="${pPts || '14'}">
                            <input type="hidden" id="e${eq.id_partido}_signo" value="${pSig}">"""

if old_hidden in text:
    text = text.replace(old_hidden, new_hidden)
else:
    print("Warning: old_hidden not found, might have slightly different spacing.")
    text = re.sub(
        r'<input type="hidden" id="e\$\{eq\.id_partido\}_sets" value="">\s*<input type="hidden" id="e\$\{eq\.id_partido\}_puntos" value="14">\s*<input type="hidden" id="e\$\{eq\.id_partido\}_signo" value="">',
        r'<input type="hidden" id="e${eq.id_partido}_sets" value="${pSets}">\n                            <input type="hidden" id="e${eq.id_partido}_puntos" value="${pPts || \'14\'}">\n                            <input type="hidden" id="e${eq.id_partido}_signo" value="${pSig}">',
        text
    )

# 2. Prevent the global save button from sending empty predictions!
old_save_loop = """            let vSet = getVal(`e${eq.id_partido}_sets`);
            let vPuntos = getVal(`e${eq.id_partido}_puntos`);
            let vSigno = getVal(`e${eq.id_partido}_signo`);

            

            prediccionesList[eq.id_partido] = { sets: vSet, puntos: vPuntos, signo: vSigno };"""

new_save_loop = """            let vSet = getVal(`e${eq.id_partido}_sets`);
            let vPuntos = getVal(`e${eq.id_partido}_puntos`);
            let vSigno = getVal(`e${eq.id_partido}_signo`);

            // ONLY send this prediction if the user has actually made one (or is modifying an existing one).
            // This prevents overwriting valid backend predictions with empty ones.
            if (vSet !== "") {
                prediccionesList[eq.id_partido] = { sets: vSet, puntos: vPuntos, signo: vSigno };
            }"""

if old_save_loop in text:
    text = text.replace(old_save_loop, new_save_loop)
else:
    print("Warning: old_save_loop not found. Using regex.")
    text = re.sub(
        r'let vSet = getVal\(`e\$\{eq\.id_partido\}_sets`\);\s*let vPuntos = getVal\(`e\$\{eq\.id_partido\}_puntos`\);\s*let vSigno = getVal\(`e\$\{eq\.id_partido\}_signo`\);\s*prediccionesList\[eq\.id_partido\] = \{ sets: vSet, puntos: vPuntos, signo: vSigno \};',
        r'let vSet = getVal(`e${eq.id_partido}_sets`);\n            let vPuntos = getVal(`e${eq.id_partido}_puntos`);\n            let vSigno = getVal(`e${eq.id_partido}_signo`);\n\n            if (vSet !== "") {\n                prediccionesList[eq.id_partido] = { sets: vSet, puntos: vPuntos, signo: vSigno };\n            }',
        text
    )

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("SUCCESS data loss bug fixed")
