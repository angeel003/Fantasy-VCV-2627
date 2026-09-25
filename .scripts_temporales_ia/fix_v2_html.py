import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the sign logic for the buttons. 
# Left button is ALWAYS Local -> "A favor" (true)
# Right button is ALWAYS Visitor -> "En contra" (false)
old_buttons = r"""<div class="sign-selector-v2">
                                      <button type="button" class="sign-btn-v2 sign-plus-v2" id="signo-plus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, ${eq.es_local})">
                                        <span style="font-size:0.7rem;">${localTeamName}</span>
                                      </button>
                                      <button type="button" class="sign-btn-v2 sign-minus-v2" id="signo-minus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, ${!eq.es_local})">
                                        <span style="font-size:0.7rem;">${visitTeamName}</span>
                                      </button>
                                    </div>"""

new_buttons = r"""<div class="sign-selector-v2">
                                      <button type="button" class="sign-btn-v2 sign-plus-v2" id="signo-plus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, true)">
                                        <span style="font-size:0.7rem;">${localTeamName}</span>
                                      </button>
                                      <button type="button" class="sign-btn-v2 sign-minus-v2" id="signo-minus-v2-${eq.id_partido}" onclick="cambiarSignoV2('${eq.id_partido}', this, false)">
                                        <span style="font-size:0.7rem;">${visitTeamName}</span>
                                      </button>
                                    </div>"""
text = text.replace(old_buttons, new_buttons)

# Fix the changing function parameter name to avoid confusion
text = text.replace('function cambiarSignoV2(matchId, btn, isVcv) {', 'function cambiarSignoV2(matchId, btn, isLocal) {')
text = text.replace('hiddenInput.value = isVcv ? \'A favor\' : \'En contra\';', 'hiddenInput.value = isLocal ? \'A favor\' : \'En contra\';')

# Fix the restore logic in cargarDatosAntiguos
old_sync = r"""if (signoVal === "A favor") {
                        const btn = document.querySelector(`button[id^="signo-"][id$="-${idPart}"][onclick*=" true)"]`);
                        if (btn) btn.classList.add('selected');
                    } else if (signoVal === "En contra") {
                        const btn = document.querySelector(`button[id^="signo-"][id$="-${idPart}"][onclick*=" false)"]`);
                        if (btn) btn.classList.add('selected');
                    }"""

new_sync = r"""if (signoVal === "A favor") {
                        const btn = document.getElementById(`signo-plus-v2-${idPart}`);
                        if (btn) btn.classList.add('selected');
                    } else if (signoVal === "En contra") {
                        const btn = document.getElementById(`signo-minus-v2-${idPart}`);
                        if (btn) btn.classList.add('selected');
                    }"""
text = text.replace(old_sync, new_sync)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("v2.html sign logic fixed!")
