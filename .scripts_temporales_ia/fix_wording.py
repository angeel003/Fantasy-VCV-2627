import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix in login() initialization
target1 = """let ptsText = pSig === 'A favor (+)' ? 'a favor' : (pSig === 'En contra (-)' ? 'en contra' : '');
                    let formStr = ptsText ? `(+${pPts} pts ${ptsText})` : `(${pPts} pts)`;
                    if(pPts == 0) formStr = `(0 pts)`;"""
new1 = """let winnerName = "";
                    if (pSig.includes('A favor')) winnerName = savedLocalName;
                    else if (pSig.includes('En contra')) winnerName = savedVisitName;
                    let formStr = winnerName ? `(+${pPts} pts para ${winnerName})` : `(${pPts} pts)`;
                    if(pPts == 0) formStr = `(0 pts)`;"""

# Fix the duplicate ptsText/formStr inside handleSaveOrModifyV2
target2 = """let ptsText = signText === 'A favor (+)' ? 'a favor' : (signText === 'En contra (-)' ? 'en contra' : '');
            let formStr = ptsText ? `(+${p} pts ${ptsText})` : `(${p} pts)`;
            if(p==0) formStr = `(0 pts)`;"""
new2 = """let winnerName = "";
            if (sig.includes('A favor')) winnerName = localAb;
            else if (sig.includes('En contra')) winnerName = visitAb;
            let formStr = winnerName ? `(+${p} pts para ${winnerName})` : `(${p} pts)`;
            if(p==0) formStr = `(0 pts)`;"""

if target1 in text:
    text = text.replace(target1, new1)
    print("Fixed login formatting")
else:
    print("Target1 not found")

if target2 in text:
    text = text.replace(target2, new2)
    print("Fixed handleSaveOrModifyV2 formatting")
else:
    print("Target2 not found")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
