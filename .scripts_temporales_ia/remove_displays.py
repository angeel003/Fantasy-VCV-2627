import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove style.display manual overrides for sections
text = re.sub(r'document\.getElementById\(\'(clasificacionesSection|historialSection|prediccionesTotalesSection)\'\)\.style\.display\s*=\s*\"[a-z]+\";', '', text)

text = re.sub(r'let calSec2 = document\.getElementById\(\'calendarioSection\'\);\s*if\s*\(calSec2\)\s*calSec2\.style\.display\s*=\s*"block";', '', text)
text = re.sub(r'let calSec = document\.getElementById\(\'calendarioSection\'\);\s*if\s*\(calSec\)\s*calSec\.style\.display\s*=\s*"none";', '', text)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("v2.html display assignments removed!")
