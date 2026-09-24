import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove Plantillas and Votos read logic
code = re.sub(
    r'\s*// LECTURA DE PLANTILLAS PARA JUGADOR DESTACADO.*?// ASOCIAR PLANTILLA, VOTOS Y DECLARACIONES A CADA PARTIDO',
    '\n\n        // ASOCIAR STREAMING A CADA PARTIDO',
    code, flags=re.DOTALL
)

# 2. Rewrite the associative loop to only do streaming
code = re.sub(
    r'// ASOCIAR STREAMING A CADA PARTIDO.*?var rondaAbierta = sheetAjustes\.getRange\("B2"\)\.getValue\(\) \|\| "1";',
    r'// ASOCIAR STREAMING A CADA PARTIDO\n        for (var c = 0; c < cartelera.length; c++) {\n            var cp = cartelera[c];\n            var oRes = resultadosMap[cp.id_partido];\n            cp.streaming = (oRes && oRes.streaming) ? oRes.streaming : "";\n        }\n\n        var rondaAbierta = sheetAjustes.getRange("B2").getValue() || "1";',
    code, flags=re.DOTALL
)

# 3. Remove vote_destacado endpoint completely
code = re.sub(
    r'\s*if \(action === "vote_destacado"\) \{.*?\n      \}\n\n      if \(action === "save"\) \{',
    '\n\n      if (action === "save") {',
    code, flags=re.DOTALL
)

# 4. Remove frase from get_data mapping
code = re.sub(
    r'resultadosMap\[resData\[i\]\[0\]\.toString\(\)\.trim\(\)\] = \{ sets: setsStr, parciales: parcStr, frase: resData\[i\]\[3\] \? resData\[i\]\[3\]\.toString\(\)\.trim\(\) : \'\', streaming: resData\[i\]\[4\] \? resData\[i\]\[4\]\.toString\(\)\.trim\(\) : \'\' \};',
    r'resultadosMap[resData[i][0].toString().trim()] = { sets: setsStr, parciales: parcStr, streaming: resData[i][4] ? resData[i][4].toString().trim() : \'\' };',
    code
)

# 5. Remove frase from save_resultado_admin
code = re.sub(
    r'var streaming = params\.streaming \|\| "";\s*var frase = params\.frase \|\| "";\s*if \(!sheetResultados\) \{.*?sheetResultados\.getRange\(rowFound, 4\)\.setValue\(frase\);\s*sheetResultados\.getRange\(rowFound, 5\)\.setValue\(streaming\);\s*\} else \{\s*sheetResultados\.appendRow\(\[idPart, sets, parciales, frase, streaming\]\);\s*\}',
    r'var streaming = params.streaming || "";\n          \n          if (!sheetResultados) {\n              sheetResultados = ss.insertSheet("Resultados Oficiales");\n              sheetResultados.appendRow(["ID_Partido", "Sets", "Parciales", "Frase_MVP", "Streaming"]);\n          }\n          var dataResAdmin = getSafeData(sheetResultados);\n          var rowFound = -1;\n          for(var r=1; r<dataResAdmin.length; r++) {\n              if(dataResAdmin[r][0].toString().trim() === idPart) { rowFound = r + 1; break; }\n          }\n          if(rowFound !== -1) {\n              sheetResultados.getRange(rowFound, 2).setValue(sets);\n              sheetResultados.getRange(rowFound, 3).setValue(parciales);\n              sheetResultados.getRange(rowFound, 5).setValue(streaming);\n          } else {\n              sheetResultados.appendRow([idPart, sets, parciales, "", streaming]);\n          }',
    code, flags=re.DOTALL
)


with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

