import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '<button type="button" class="btn-step-v2" onclick="cambiarPuntosV2(\'${eq.id_partido}\', -1)">-</button>',
    '<button type="button" class="btn-step-v2" id="btn-step-minus-${eq.id_partido}" onclick="cambiarPuntosV2(\'${eq.id_partido}\', -1)">-</button>'
)

text = text.replace(
    '<button type="button" class="btn-step-v2" onclick="cambiarPuntosV2(\'${eq.id_partido}\', 1)">+</button>',
    '<button type="button" class="btn-step-v2" id="btn-step-plus-${eq.id_partido}" onclick="cambiarPuntosV2(\'${eq.id_partido}\', 1)">+</button>'
)

target_js_old = """if (next === 0) {
              if(plusBtn) {"""
target_js_new = """if (next === 0) {
              const minusStep = document.getElementById('btn-step-minus-' + matchId);
              if (minusStep) {
                  minusStep.disabled = true;
                  minusStep.style.background = 'var(--secondary-color)';
                  minusStep.style.color = '#000';
                  minusStep.style.opacity = '1';
                  minusStep.style.cursor = 'not-allowed';
              }
              if(plusBtn) {"""
text = text.replace(target_js_old, target_js_new)

target_js_old2 = """} else {
              if(plusBtn) {"""
target_js_new2 = """} else {
              const minusStep = document.getElementById('btn-step-minus-' + matchId);
              if (minusStep) {
                  minusStep.disabled = false;
                  minusStep.style.background = '';
                  minusStep.style.color = '';
                  minusStep.style.opacity = '1';
                  minusStep.style.cursor = 'pointer';
              }
              if(plusBtn) {"""
text = text.replace(target_js_old2, target_js_new2)


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied UI state changes")
