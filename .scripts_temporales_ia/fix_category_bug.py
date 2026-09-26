import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix CSS
text = text.replace(
    '.cat-filter-btn.active { background: var(--vcv-dorado); color: #000; border-color: var(--vcv-dorado); font-weight: bold; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }',
    '.cat-filter-btn.active { background: var(--secondary-color); color: #000; border-color: var(--secondary-color); font-weight: bold; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); }'
)
text = text.replace(
    '.cat-filter-btn:hover { border-color: rgba(221, 185, 103, 0.5); }',
    '.cat-filter-btn:hover { border-color: var(--secondary-color); color: var(--text-main); }'
)

# Fix JS Logic
# Old code:
# const cat = card.getAttribute('data-category');
# if(cat) {
#     categories.add(cat);
#     totalCount++;
# }

js_old = """const cat = card.getAttribute('data-category');
                if(cat) {
                    categories.add(cat);
                    totalCount++;
                }"""

js_new = """const catAttr = card.getAttribute('data-category');
                if(catAttr) {
                    let cat = catAttr.trim().toUpperCase();
                    card._normalizedCat = cat;
                    categories.add(cat);
                    totalCount++;
                }"""
text = text.replace(js_old, js_new)

# Old code:
# let count = Array.from(cards).filter(c => c.getAttribute('data-category') === cat).length;
js_count_old = "let count = Array.from(cards).filter(c => c.getAttribute('data-category') === cat).length;"
js_count_new = "let count = Array.from(cards).filter(c => c._normalizedCat === cat).length;"
text = text.replace(js_count_old, js_count_new)

# Old code:
# if(filter === 'all' || card.getAttribute('data-category') === filter) {
js_filter_old = "if(filter === 'all' || card.getAttribute('data-category') === filter) {"
js_filter_new = "if(filter === 'all' || card._normalizedCat === filter) {"
text = text.replace(js_filter_old, js_filter_new)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed CSS and JS logic")
