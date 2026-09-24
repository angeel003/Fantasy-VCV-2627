import codecs

with codecs.open('partidos_vcv_utf8bom.txt', 'r', 'utf-8-sig') as f:
    text = f.read()

# Fix common broken accents from the RFEVB API
text = text.replace('', 'Ó').replace('VÓley', 'Vóley').replace('DumbrÓa', 'Dumbría').replace('EmevÓ', 'Emevé').replace('ENTREVÓ?AS', 'ENTREVÍAS').replace('SÓ. -', 'Sáb. -').replace('GuÓa', 'Guía')

with codecs.open('partidos_vcv.txt', 'w', 'utf-8-sig') as f:
    f.write(text)

with codecs.open('partidos_vcv.csv', 'w', 'utf-8-sig') as f:
    f.write(text)

