import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

helper_fn = """
  // HELPER PARA EVITAR QUE GOOGLE SHEETS ROMPA TEXTOS COMO "3-1" O "25-20" CONVIRTIENDOLOS A FECHAS
  function parseSheetText(val) {
      if (val && typeof val.getDate === 'function') {
          return val.getDate() + "-" + (val.getMonth() + 1);
      } else if (val !== undefined && val !== null) {
          return val.toString().trim();
      }
      return "";
  }
"""

if "function parseSheetText" not in code:
    code = code.replace("function getSafeData(sheet) {", helper_fn + "\n  function getSafeData(sheet) {")

old_res = """              var rawSets = resData[i][1];
              var setsStr = "";
              if (rawSets && typeof rawSets.getDate === 'function') {
                  setsStr = rawSets.getDate() + "-" + (rawSets.getMonth() + 1);
              } else if (rawSets !== undefined && rawSets !== null) {
                  setsStr = rawSets.toString().trim();
              }
              resultadosMap[resData[i][0].toString().trim()] = { sets: setsStr, parciales: resData[i][2], frase: resData[i][3] ? resData[i][3].toString().trim() : '', streaming: resData[i][4] ? resData[i][4].toString().trim() : '' };"""

new_res = """              var setsStr = parseSheetText(resData[i][1]);
              var parcStr = parseSheetText(resData[i][2]);
              resultadosMap[resData[i][0].toString().trim()] = { sets: setsStr, parciales: parcStr, frase: resData[i][3] ? resData[i][3].toString().trim() : '', streaming: resData[i][4] ? resData[i][4].toString().trim() : '' };"""

code = code.replace(old_res, new_res)

old_porras = """              var rawSets = pData[i][3];
              var setsStr = "";
              if (rawSets && typeof rawSets.getDate === 'function') { setsStr = rawSets.getDate() + "-" + (rawSets.getMonth() + 1); }
              else if (rawSets !== undefined && rawSets !== null) { setsStr = rawSets.toString().trim(); }
              porrasMap[upUsr][upPart] = { sets: setsStr, puntos: pData[i][4], signo: pData[i][5] };"""

new_porras = """              var setsStr = parseSheetText(pData[i][3]);
              porrasMap[upUsr][upPart] = { sets: setsStr, puntos: pData[i][4], signo: pData[i][5] };"""

code = code.replace(old_porras, new_porras)

old_sec = """                  var rawSets = sData[i][3];
                  var setsStr = "";
                  if (rawSets && typeof rawSets.getDate === 'function') { setsStr = rawSets.getDate() + "-" + (rawSets.getMonth() + 1); }
                  else if (rawSets !== undefined && rawSets !== null) { setsStr = rawSets.toString().trim(); }
                  porrasMap[spUsr][spPart] = { sets: setsStr, puntos: sData[i][4], signo: sData[i][5] };"""

new_sec = """                  var setsStr = parseSheetText(sData[i][3]);
                  porrasMap[spUsr][spPart] = { sets: setsStr, puntos: sData[i][4], signo: sData[i][5] };"""

code = code.replace(old_sec, new_sec)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

