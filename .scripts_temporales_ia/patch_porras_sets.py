import re

with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace Porras sets parsing
old_porras_logic = r"""          for\(var i=1; i<pData\.length; i\+\+\) \{
              var upUsr = pData\[i\]\[1\] \? pData\[i\]\[1\]\.toString\(\)\.trim\(\) : "";
              var upPart = pData\[i\]\[2\] \? pData\[i\]\[2\]\.toString\(\)\.trim\(\) : "";
              if\(!upUsr \|\| !upPart\) continue;
              if\(!porrasMap\[upUsr\]\) porrasMap\[upUsr\] = \{\};
              porrasMap\[upUsr\]\[upPart\] = \{ sets: pData\[i\]\[3\], puntos: pData\[i\]\[4\], signo: pData\[i\]\[5\] \};
          \}"""

new_porras_logic = """          for(var i=1; i<pData.length; i++) {
              var upUsr = pData[i][1] ? pData[i][1].toString().trim() : "";
              var upPart = pData[i][2] ? pData[i][2].toString().trim() : "";
              if(!upUsr || !upPart) continue;
              if(!porrasMap[upUsr]) porrasMap[upUsr] = {};
              var rawSets = pData[i][3];
              var setsStr = "";
              if (rawSets && typeof rawSets.getDate === 'function') { setsStr = rawSets.getDate() + "-" + (rawSets.getMonth() + 1); }
              else if (rawSets !== undefined && rawSets !== null) { setsStr = rawSets.toString().trim(); }
              porrasMap[upUsr][upPart] = { sets: setsStr, puntos: pData[i][4], signo: pData[i][5] };
          }"""

code = re.sub(old_porras_logic, new_porras_logic, code)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

