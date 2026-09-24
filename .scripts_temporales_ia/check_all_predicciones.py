import re
with open('dev.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Mis Predicciones')
print(f"First match index: {idx}")
if idx != -1:
    print(text[max(0, idx-50):idx+100].encode('ascii', 'ignore').decode())

idx2 = text.find('Mis Predicciones', idx + 1)
print(f"Second match index: {idx2}")
if idx2 != -1:
    print(text[max(0, idx2-50):idx2+100].encode('ascii', 'ignore').decode())

idx3 = text.find('Mis predicciones', idx2 + 1)
print(f"Third match index: {idx3}")
if idx3 != -1:
    print(text[max(0, idx3-50):idx3+100].encode('ascii', 'ignore').decode())

# Check title tag or header
idx4 = text.find('mis predicciones')
print(f"Lowercase match index: {idx4}")

