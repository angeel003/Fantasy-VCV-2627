import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """if (parseInt(preds[idPart].puntos) === 0) {
                        const btnPlus = document.getElementById(`signo-plus-v2-${idPart}`);
                        const btnMinus = document.getElementById(`signo-minus-v2-${idPart}`);
                        if(btnPlus) { btnPlus.classList.add('tied-btn'); btnPlus.disabled = true; }
                        if(btnMinus) { btnMinus.classList.add('tied-btn'); btnMinus.disabled = true; }
                    }"""

new = """if (parseInt(preds[idPart].puntos) === 0) {
                        const btnPlus = document.getElementById(`signo-plus-v2-${idPart}`);
                        const btnMinus = document.getElementById(`signo-minus-v2-${idPart}`);
                        const btnStepMinus = document.getElementById(`btn-step-minus-${idPart}`);
                        if(btnPlus) { btnPlus.classList.add('tied-btn'); btnPlus.disabled = true; }
                        if(btnMinus) { btnMinus.classList.add('tied-btn'); btnMinus.disabled = true; }
                        if(btnStepMinus) {
                            btnStepMinus.disabled = true;
                            btnStepMinus.style.background = 'var(--secondary-color)';
                            btnStepMinus.style.color = '#000';
                            btnStepMinus.style.cursor = 'not-allowed';
                        }
                    }"""

if target in text:
    text = text.replace(target, new)
else:
    print("Not found logic target")

# Also, when the HTML is generated, if there is no previous prediction but pPts defaults to something... wait, by default it's 14!
# Let me check if pPts defaults to 14 in the HTML generation.

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated init logic")
