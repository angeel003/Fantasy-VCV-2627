import re
with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the sheets loop in add_user
old_sheets_logic = """        var sheetsToAppend = ["Permisos_Equipos", "Ligas", "Insignias", "Permisos_Secreta"];
        for(var i=0; i<sheetsToAppend.length; i++) {
            var sh = ss.getSheetByName(sheetsToAppend[i]);
            if(sh) {
                var vals = sh.getRange(1, 1, sh.getMaxRows(), 1).getValues();
                var firstEmpty = 1;
                for(var j=0; j<vals.length; j++){
                    if(!vals[j][0] || vals[j][0].toString().trim() === "") {
                        firstEmpty = j + 1;
                        break;
                    }
                }
                sh.getRange(firstEmpty, 1).setValue(newU);
            }
        }"""

new_sheets_logic = """        var sheetsToAppend = ["Permisos_Equipos", "Ligas", "Insignias", "Permisos_Secreta"];
        for(var i=0; i<sheetsToAppend.length; i++) {
            var shName = sheetsToAppend[i];
            var sh = ss.getSheetByName(shName);
            if(sh) {
                var vals = sh.getRange(1, 1, sh.getMaxRows(), 1).getValues();
                var firstEmpty = 1;
                for(var j=0; j<vals.length; j++){
                    if(!vals[j][0] || vals[j][0].toString().trim() === "") {
                        firstEmpty = j + 1;
                        break;
                    }
                }
                sh.getRange(firstEmpty, 1).setValue(newU);
                
                if (shName === "Ligas" && params.ligas_seleccionadas && params.ligas_seleccionadas.length > 0) {
                    var ligasSel = params.ligas_seleccionadas;
                    var ligasHeaders = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
                    for (var rL = 0; rL < ligasSel.length; rL++) {
                        var cIdx = ligasHeaders.indexOf(ligasSel[rL]);
                        if (cIdx !== -1) {
                            sh.getRange(firstEmpty, cIdx + 1).setValue("X");
                        }
                    }
                }
            }
        }"""

if old_sheets_logic in text:
    text = text.replace(old_sheets_logic, new_sheets_logic)
    with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated Código.js backend to support ligas.")
else:
    print("Could not find the target code in Código.js")

