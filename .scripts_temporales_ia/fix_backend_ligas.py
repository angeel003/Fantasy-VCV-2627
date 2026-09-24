import re
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_logic = """                if (shName === "Ligas" && params.ligas_seleccionadas && params.ligas_seleccionadas.length > 0) {
                    var ligasSel = params.ligas_seleccionadas;
                    var ligasHeaders = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
                    for (var rL = 0; rL < ligasSel.length; rL++) {
                        var cIdx = ligasHeaders.indexOf(ligasSel[rL]);
                        if (cIdx !== -1) {
                            sh.getRange(firstEmpty, cIdx + 1).setValue("X");
                        }
                    }
                }"""

new_logic = """                if (shName === "Ligas" && params.ligas_seleccionadas && params.ligas_seleccionadas.length > 0) {
                    var ligasSel = params.ligas_seleccionadas;
                    var ligasHeaders = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
                    for (var rL = 0; rL < ligasSel.length; rL++) {
                        var targetLiga = ligasSel[rL].toString().trim().toLowerCase();
                        for (var col = 0; col < ligasHeaders.length; col++) {
                            if (ligasHeaders[col] && ligasHeaders[col].toString().trim().toLowerCase() === targetLiga) {
                                sh.getRange(firstEmpty, col + 1).setValue("X");
                                break;
                            }
                        }
                    }
                }"""

if old_logic in text:
    text = text.replace(old_logic, new_logic)
    with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated backend strict string matching.")
else:
    print("Logic not found in backend.")

