import re
with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_logic = r"""let localTeamName = eq.equipo_local;
                        let visitTeamName = eq.rival;
                        
                        let localAbrev = (eq.abrev_local || localTeamName.substring(0,3)).toUpperCase();
                        let visitAbrev = (eq.abrev_rival || visitTeamName.substring(0,3)).toUpperCase();"""

new_logic = r"""let localTeamName = eq.es_local ? eq.equipo_local : eq.rival;
                        let visitTeamName = eq.es_local ? eq.rival : eq.equipo_local;
                        
                        let abrevLocalRaw = eq.es_local ? eq.abrev_local : eq.abrev_rival;
                        let abrevVisitRaw = eq.es_local ? eq.abrev_rival : eq.abrev_local;
                        
                        let localAbrev = (abrevLocalRaw || localTeamName.substring(0,3)).toUpperCase();
                        let visitAbrev = (abrevVisitRaw || visitTeamName.substring(0,3)).toUpperCase();"""

text = text.replace(old_logic, new_logic)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Logic fixed!")
