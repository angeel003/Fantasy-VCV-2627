import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix normal login block
text = re.sub(r"document\.getElementById\('h2-user-name'\)\.innerText\s*=\s*(.*?);", r"let nameEl = document.getElementById('h2-user-name'); if(nameEl) nameEl.innerText = \1;", text)
text = re.sub(r"document\.getElementById\('h2-user-handle'\)\.innerText\s*=\s*(.*?);", r"let handleEl = document.getElementById('h2-user-handle'); if(handleEl) handleEl.innerText = \1;", text)
text = re.sub(r"document\.getElementById\('h2-user-badges'\)\.innerHTML\s*=\s*(.*?);", r"let badgesEl = document.getElementById('h2-user-badges'); if(badgesEl) badgesEl.innerHTML = \1;", text)

# Just in case, replace the guest mode too
text = re.sub(r"document\.getElementById\('h2-user-name'\)\.innerText = \"Invitado\";", r"let gn = document.getElementById('h2-user-name'); if(gn) gn.innerText = 'Invitado';", text)
text = re.sub(r"document\.getElementById\('h2-user-handle'\)\.innerText = \"@guest\";", r"let gh = document.getElementById('h2-user-handle'); if(gh) gh.innerText = '@guest';", text)
text = re.sub(r"document\.getElementById\('h2-user-badges'\)\.innerHTML = \"\";", r"let gb = document.getElementById('h2-user-badges'); if(gb) gb.innerHTML = '';", text)

# Now we must insert the JS that updates the new elements: h2-user-rank and h2-user-pts
new_js_insert = """
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
"""

# Insert right after `let isAdmin = false;` in the login block
if "let isAdmin = false;" in text and "allUsers.sort" not in text:
    text = text.replace("let isAdmin = false;", "let isAdmin = false;\n" + new_js_insert, 1)

# Guest login insertion
new_guest_insert = """
                let rankElGuest = document.getElementById('h2-user-rank');
                if(rankElGuest) rankElGuest.innerText = "Guest";
                let ptsElGuest = document.getElementById('h2-user-pts');
                if(ptsElGuest) ptsElGuest.innerText = "0 pts";
"""

guest_trigger = "let gb = document.getElementById('h2-user-badges'); if(gb) gb.innerHTML = '';"
if guest_trigger in text and "rankElGuest.innerText = \"Guest\"" not in text:
    text = text.replace(guest_trigger, guest_trigger + "\n" + new_guest_insert)

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("IDs made safe")
