import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

css_primary_old = r"\.btn-primary:hover, \.btn-primary:focus \{ background-color: var\(--vcv-dorado\); border-color: var\(--vcv-dorado\); color: var\(--vcv-negro\); \}"
css_primary_new = r""".btn-primary:hover, .btn-primary:focus, .btn-primary:active { background-color: var(--vcv-dorado); border-color: var(--vcv-dorado); color: var(--vcv-negro); }
    .btn-primary:disabled, .btn-primary.disabled { background-color: var(--vcv-morado); border-color: var(--vcv-morado); color: var(--vcv-blanco); opacity: 0.7; }"""

css_success_old = r"\.btn-success:hover \{ background-color: #b89c45; border-color: #b89c45; color: var\(--vcv-negro\); \}"
css_success_new = r""".btn-success:hover, .btn-success:focus, .btn-success:active { background-color: #b89c45; border-color: #b89c45; color: var(--vcv-negro); }
    .btn-success:disabled, .btn-success.disabled { background-color: var(--vcv-dorado); border-color: var(--vcv-dorado); color: var(--vcv-negro); opacity: 0.7; }"""

html = re.sub(css_primary_old, css_primary_new, html)
html = re.sub(css_success_old, css_success_new, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

