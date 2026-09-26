import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the old name injection block in normal login
old_js = """let displayNom = data.nombre_real && data.nombre_real !== usr ? `${data.nombre_real}` : usr;
            document.getElementById('h2-user-name').innerText = displayNom;
            document.getElementById('h2-user-handle').innerText = "@" + usr;
            
            let misInsignias = data.insignias[usr] || [];
            let insigniasHeaderHtml = "";
            let isAdmin = false;
            
            misInsignias.forEach(b => {
                if (b.type === 'admin') isAdmin = true;
                let cssColorClass = getBadgeCSS(b.type);
                insigniasHeaderHtml += `<img src="${URL_BADGE_GENERIC}" class="badge-header ${cssColorClass}" title="${b.text}" onclick="showMobileTooltip(event, '${b.text}')">`;
            });
            document.getElementById('h2-user-badges').innerHTML = insigniasHeaderHtml;"""

new_js = """let displayNom = data.nombre_real && data.nombre_real !== usr ? `${data.nombre_real}` : usr;
            
            // Calculate Rank
            let allUsers = Object.keys(data.totales || {});
            allUsers.sort((a,b) => (data.totales[b] || 0) - (data.totales[a] || 0));
            let myRank = allUsers.indexOf(usr) + 1;
            let rankText = myRank > 0 ? "Top " + myRank : "-";
            
            let myPoints = data.totales && data.totales[usr] ? data.totales[usr] : 0;
            
            let rankEl = document.getElementById('h2-user-rank');
            if(rankEl) rankEl.innerText = rankText;
            let ptsEl = document.getElementById('h2-user-pts');
            if(ptsEl) ptsEl.innerText = myPoints + " pts";
            
            let misInsignias = data.insignias[usr] || [];
            let isAdmin = false;
            misInsignias.forEach(b => {
                if (b.type === 'admin') isAdmin = true;
            });"""

text = text.replace(old_js, new_js)

# Replace the Guest login injection block as well
old_guest_js = """document.getElementById('h2-user-name').innerText = "Invitado";
                document.getElementById('h2-user-handle').innerText = "@guest";
                document.getElementById('h2-user-badges').innerHTML = "";"""

new_guest_js = """let rankElGuest = document.getElementById('h2-user-rank');
                if(rankElGuest) rankElGuest.innerText = "Guest";
                let ptsElGuest = document.getElementById('h2-user-pts');
                if(ptsElGuest) ptsElGuest.innerText = "0 pts";"""

text = text.replace(old_guest_js, new_guest_js)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("JS updated.")
