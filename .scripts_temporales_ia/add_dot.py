with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('if(cat === "SM2") displayName = "Superliga Masc 2";', 'if(cat === "SM2") displayName = "Superliga Masc. 2";')

with open('v2.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added dot to Superliga Masc. 2")
