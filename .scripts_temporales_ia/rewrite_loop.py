import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the Cartelera Loop
old_loop = r"""if \(eq\.estado === "ABIERTO"\) \{
                        let dt = new Date\(eq\.timestamp\);.*?</div>`;
                    \}
                \}
            \}\);"""

# wait, regex might be too complex for a multi-line with that many unknown chars.
