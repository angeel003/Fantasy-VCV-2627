with open('partidos_vcv.txt', 'r', encoding='utf-8') as f1:
    vcv_data = f1.read().strip()

with open('partidos_sj.txt', 'r', encoding='utf-8') as f2:
    sj_data = f2.read().strip()

# Combine both and save to partidos_finales.txt
with open('partidos_finales.txt', 'w', encoding='utf-8') as out:
    out.write(vcv_data + "\n" + sj_data + "\n")

# Same for CSV if it exists
try:
    with open('partidos_vcv.csv', 'r', encoding='utf-8') as f1_csv:
        vcv_csv = f1_csv.read().strip()
    with open('partidos_finales.csv', 'w', encoding='utf-8') as out_csv:
        # replace tabs with semicolons for sj_data
        sj_csv = sj_data.replace('\t', ';')
        out_csv.write(vcv_csv + "\n" + sj_csv + "\n")
    print("Combined TXT and CSV successfully.")
except Exception as e:
    print("Combined TXT successfully.", e)

