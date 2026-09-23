import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

old_save_res = """        var idPart = params.id_partido;
        var sets = params.sets;
        var parciales = params.parciales;
        
        if (!sheetResultados) {
            sheetResultados = ss.insertSheet("Resultados Oficiales");
            sheetResultados.appendRow(["ID_Partido", "Sets", "Parciales"]);
        }
        var dataResAdmin = sheetResultados.getDataRange().getValues();
        var rowFound = -1;
        for(var r=1; r<dataResAdmin.length; r++) {
            if(dataResAdmin[r][0].toString().trim() === idPart) { rowFound = r + 1; break; }
        }
        if(rowFound !== -1) {
            sheetResultados.getRange(rowFound, 2).setValue(sets);
            sheetResultados.getRange(rowFound, 3).setValue(parciales);
        } else {
            sheetResultados.appendRow([idPart, sets, parciales]);
        }"""

new_save_res = """        var idPart = params.id_partido;
        var sets = params.sets || "";
        var parciales = params.parciales || "";
        var streaming = params.streaming || "";
        var frase = params.frase || "";
        
        if (!sheetResultados) {
            sheetResultados = ss.insertSheet("Resultados Oficiales");
            sheetResultados.appendRow(["ID_Partido", "Sets", "Parciales", "Frase_MVP", "Streaming"]);
        }
        var dataResAdmin = sheetResultados.getDataRange().getValues();
        var rowFound = -1;
        for(var r=1; r<dataResAdmin.length; r++) {
            if(dataResAdmin[r][0].toString().trim() === idPart) { rowFound = r + 1; break; }
        }
        if(rowFound !== -1) {
            sheetResultados.getRange(rowFound, 2).setValue(sets);
            sheetResultados.getRange(rowFound, 3).setValue(parciales);
            sheetResultados.getRange(rowFound, 4).setValue(frase);
            sheetResultados.getRange(rowFound, 5).setValue(streaming);
        } else {
            sheetResultados.appendRow([idPart, sets, parciales, frase, streaming]);
        }"""

js_content = js_content.replace(old_save_res, new_save_res)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

