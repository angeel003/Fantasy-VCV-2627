import sys
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()
if 'window.updateCategoryFilter = function()' in text:
    print('GLOBAL FUNCTION SET')
else:
    print('GLOBAL FUNCTION FAILED')

if '<button type="button" class="cat-filter-btn' in text:
    print('BUTTON TYPE SET')
else:
    print('BUTTON TYPE FAILED')
