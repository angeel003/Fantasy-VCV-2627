import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_rank_code = """// Calculate Rank
            let allUsers = Object.keys(data.totales || {});
            allUsers.sort((a,b) => (data.totales[b] || 0) - (data.totales[a] || 0));
            let myRank = allUsers.indexOf(usr) + 1;
            let rankText = myRank > 0 ? "Top " + myRank : "-";
            
            let myPoints = data.totales && data.totales[usr] ? data.totales[usr] : 0;"""

new_rank_code = """// Calculate Rank from Global Leaderboard
            let globalRankList = data.clasificaciones && data.clasificaciones["Global"] ? data.clasificaciones["Global"] : [];
            let myRankIndex = globalRankList.findIndex(r => r.jugador === usr);
            let myRank = myRankIndex !== -1 ? myRankIndex + 1 : 0;
            let rankText = myRank > 0 ? "Top " + myRank : "-";
            
            let myPoints = myRankIndex !== -1 ? globalRankList[myRankIndex].puntos : 0;"""

text = text.replace(old_rank_code, new_rank_code)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Rank logic updated")
