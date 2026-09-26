with open('v2.html', 'r', encoding='utf-8') as f:
    text = f.read()

if 'vSet !== ""' in text:
    print('SAVE LOGIC SET')
else:
    print('SAVE LOGIC FAILED')

if '${pSets}' in text:
    print('HIDDEN INPUTS SET')
else:
    print('HIDDEN INPUTS FAILED')
