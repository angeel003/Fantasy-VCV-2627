with open('prototipo_stitch.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
ranking = re.search(r'<section class="view-section" id="view-ranking">.*?</section>', text, re.DOTALL)
if ranking:
    print('RANKING HTML:', ranking.group(0)[:1500])
