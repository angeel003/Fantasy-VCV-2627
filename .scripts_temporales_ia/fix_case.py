import re

with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = """if (pSig.includes('A favor')) winnerName = savedLocalName;
                    else if (pSig.includes('En contra')) winnerName = savedVisitName;"""
new1 = """if (pSig.toLowerCase().includes('a favor')) winnerName = savedLocalName;
                    else if (pSig.toLowerCase().includes('en contra')) winnerName = savedVisitName;"""

target2 = """if (sig.includes('A favor')) winnerName = localAb;
            else if (sig.includes('En contra')) winnerName = visitAb;"""
new2 = """if (sig.toLowerCase().includes('a favor')) winnerName = localAb;
            else if (sig.toLowerCase().includes('en contra')) winnerName = visitAb;"""

if target1 in text:
    text = text.replace(target1, new1)
    print("Fixed logic 1")
if target2 in text:
    text = text.replace(target2, new2)
    print("Fixed logic 2")

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)
