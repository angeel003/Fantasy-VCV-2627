import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix duplicate declarations
target = """let localTeamName = (eq.ubicacion === 'LOCAL') ? eq.equipo_local : eq.rival;
                    let visitTeamName = (eq.ubicacion === 'LOCAL') ? eq.rival : eq.equipo_local;"""

# Replace the FIRST occurrence with renamed variables
new = """let savedLocalName = (eq.ubicacion === 'LOCAL') ? eq.equipo_local : eq.rival;
                    let savedVisitName = (eq.ubicacion === 'LOCAL') ? eq.rival : eq.equipo_local;"""

if text.count(target) > 0:
    # Replace only the first one
    text = text.replace(target, new, 1)
    text = text.replace('${localTeamName} ${formattedSets} ${visitTeamName}', '${savedLocalName} ${formattedSets} ${savedVisitName}')

# Fix the currentUser issue
text = text.replace('window.currentUser', 'currentUser')
text = text.replace('window.currentPassword', 'currentPassword')


with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed syntax error and scope issues")
