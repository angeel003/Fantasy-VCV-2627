with open('script-dev/Código.js', 'r', encoding='utf-8') as f:
    code = f.read()

import re
code = re.sub(
    r'\s*if \(action === "vote_destacado"\) \{.*?\n      \}\n\n      if \(action === "save"\) \{',
    '\n\n      if (action === "save") {',
    code, flags=re.DOTALL
)

with open('script-dev/Código.js', 'w', encoding='utf-8') as f:
    f.write(code)

