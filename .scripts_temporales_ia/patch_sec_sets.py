import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

old_sec_logic = r"""          if \(sheetPredSecretas\) \{
              var sData = getSafeData\(sheetPredSecretas\);
              for\(var i=1; i<sData\.length; i\+\+\) \{
                  var spUsr = sData\[i\]\[1\] \? sData\[i\]\[1\]\.toString\(\)\.trim\(\) : "";
                  var spPart = sData\[i\]\[2\] \? sData\[i\]\[2\]\.toString\(\)\.trim\(\) : "";
                  if\(!spUsr \|\| !spPart\) continue;
                  if\(!porrasMap\[spUsr\]\) porrasMap\[spUsr\] = \{\};
                  porrasMap\[spUsr\]\[spPart\] = \{ sets: sData\[i\]\[3\], puntos: sData\[i\]\[4\], signo: sData\[i\]\[5\] \};
              \}
          \}"""

new_sec_logic = """          if (sheetPredSecretas) {
              var sData = getSafeData(sheetPredSecretas);
              for(var i=1; i<sData.length; i++) {
                  var spUsr = sData[i][1] ? sData[i][1].toString().trim() : "";
                  var spPart = sData[i][2] ? sData[i][2].toString().trim() : "";
                  if(!spUsr || !spPart) continue;
                  if(!porrasMap[spUsr]) porrasMap[spUsr] = {};
                  var rawSets = sData[i][3];
                  var setsStr = "";
                  if (rawSets && typeof rawSets.getDate === 'function') { setsStr = rawSets.getDate() + "-" + (rawSets.getMonth() + 1); }
                  else if (rawSets !== undefined && rawSets !== null) { setsStr = rawSets.toString().trim(); }
                  porrasMap[spUsr][spPart] = { sets: setsStr, puntos: sData[i][4], signo: sData[i][5] };
              }
          }"""

code = re.sub(old_sec_logic, new_sec_logic, code)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

