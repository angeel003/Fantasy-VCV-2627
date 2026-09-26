import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update HTML span to input
old_span = r'<span id="val-v2-\$\{eq\.id_partido\}">14</span>'
new_input = r'<input type="number" id="val-v2-${eq.id_partido}" value="14" oninput="sincronizarPuntosV2(\'${eq.id_partido}\')" style="background:transparent; border:none; text-align:center; font-size:1.3rem; font-weight:900; color:var(--secondary-color); width:100%; min-width:40px; outline:none; -moz-appearance:textfield; padding:0; margin:0; height:30px;">'
text = re.sub(old_span, new_input, text)

# 2. Add sincronizarPuntosV2 and update cambiarPuntosV2
old_js = r'function cambiarPuntosV2\(matchId, delta\) \{'
new_js = r"""function sincronizarPuntosV2(matchId) {
      const hiddenInput = document.getElementById('e' + matchId + '_puntos');
      const valInput = document.getElementById('val-v2-' + matchId);
      if (hiddenInput && valInput) {
          let current = parseInt(valInput.value);
          if (isNaN(current) || current < 0) {
              current = 0;
          }
          // Update the hidden input
          hiddenInput.value = current;
          actualizarEstadoEmpate(matchId, current);
      }
    }

    function actualizarEstadoEmpate(matchId, next) {
      const plusBtn = document.getElementById('signo-plus-v2-' + matchId);
      const minusBtn = document.getElementById('signo-minus-v2-' + matchId);
      const signInput = document.getElementById('e' + matchId + '_signo');
      const minusStep = document.getElementById('btn-step-minus-' + matchId);
      
      if (next === 0) {
          if (minusStep) {
              minusStep.disabled = true;
              minusStep.style.background = 'var(--secondary-color)';
              minusStep.style.color = '#000';
              minusStep.style.opacity = '1';
              minusStep.style.cursor = 'not-allowed';
          }
          if(plusBtn) {
              plusBtn.classList.add('tied-btn');
              plusBtn.disabled = true;
              plusBtn.style.pointerEvents = 'none';
          }
          if(minusBtn) {
              minusBtn.classList.add('tied-btn');
              minusBtn.disabled = true;
              minusBtn.style.pointerEvents = 'none';
          }
          if(signInput) signInput.value = 'Empate';
      } else {
          if (minusStep) {
              minusStep.disabled = false;
              minusStep.style.background = '';
              minusStep.style.color = '';
              minusStep.style.opacity = '1';
              minusStep.style.cursor = 'pointer';
          }
          if(plusBtn) {
              plusBtn.classList.remove('tied-btn');
              plusBtn.disabled = false;
              plusBtn.style.pointerEvents = 'auto';
          }
          if(minusBtn) {
              minusBtn.classList.remove('tied-btn');
              minusBtn.disabled = false;
              minusBtn.style.pointerEvents = 'auto';
          }
          if(signInput && signInput.value === 'Empate') {
              signInput.value = '';
              if(plusBtn) plusBtn.classList.remove('selected');
              if(minusBtn) minusBtn.classList.remove('selected');
          }
      }
    }

    function cambiarPuntosV2(matchId, delta) {"""

# Find the next === 0 logic in cambiarPuntosV2 to replace it with a call to actualizarEstadoEmpate
old_logic = r'if \(next === 0\) \{\s*const minusStep = document\.getElementById\(\'btn-step-minus-\' \+ matchId\);.*?(?=if\(signInput\.value === \'Empate\'\) \{)\s*if\(signInput\.value === \'Empate\'\) \{\s*signInput\.value = \'\';\s*if\(plusBtn\) plusBtn\.classList\.remove\(\'selected\'\);\s*if\(minusBtn\) minusBtn\.classList\.remove\(\'selected\'\);\s*\}\s*\}'
new_logic = r'actualizarEstadoEmpate(matchId, next);'

if 'sincronizarPuntosV2' not in text:
    text = re.sub(old_js, new_js, text)
    text = re.sub(old_logic, new_logic, text, flags=re.DOTALL)
    text = re.sub(r'valSpan\.innerText = next;', r'if(valSpan.tagName === "INPUT") valSpan.value = next; else valSpan.innerText = next;', text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Script finished execution")
