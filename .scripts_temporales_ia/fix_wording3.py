import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = """ptsText = pSig === 'A favor (+)' ? 'a favor' : (pSig === 'En contra (-)' ? 'en contra' : '');
                    formStr = ptsText ? `(+${pPts} pts ${ptsText})` : `(${pPts} pts)`;
                    if(pPts == 0) formStr = `(0 pts)`;"""
new1 = """let winnerName = "";
                    if (pSig.includes('A favor')) winnerName = savedLocalName;
                    else if (pSig.includes('En contra')) winnerName = savedVisitName;
                    formStr = winnerName ? `(+${pPts} pts para ${winnerName})` : `(${pPts} pts)`;
                    if(pPts == 0) formStr = `(0 pts)`;"""

if target1 in text:
    text = text.replace(target1, new1)
    print("Fixed login formatting")
else:
    print("Target1 not found")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
