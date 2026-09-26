import os
import shutil
import re

base_dir = r"c:\Users\angel\Desktop\fantasy vcv 2627\Fantasy-VCV-2627"

# 1. Update index.html to disable Guest Button
index_path = os.path.join(base_dir, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

old_btn = r'<button id="btnGuest" class="btn-outline-v2" style="width: 100%; margin-top: 10px;">\s*👀 Entrar como invitado\s*</button>'
new_btn = r'<button id="btnGuest" class="btn-outline-v2" style="width: 100%; margin-top: 10px; opacity: 0.5; cursor: not-allowed;" disabled>\s*👀 Entrar como invitado (Próximamente)\s*</button>'

text = re.sub(old_btn, new_btn, text)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Create archive folder and move files
archive_dir = os.path.join(base_dir, 'obsoleto')
if not os.path.exists(archive_dir):
    os.mkdir(archive_dir)

files_to_move = [
    'v1-backup.html',
    'temp_old.html',
    'diff.txt',
    'diff2.txt',
    'match.txt',
    'scripts Fantasy Vcv 26 27.xlsx',
    'code.html'
]

for file in files_to_move:
    src = os.path.join(base_dir, file)
    if os.path.exists(src):
        shutil.move(src, os.path.join(archive_dir, file))

# Move and rename old script folder
old_script_dir = os.path.join(base_dir, 'script')
if os.path.exists(old_script_dir):
    shutil.move(old_script_dir, os.path.join(archive_dir, 'script-v1'))

# Rename script-v2 to script
script_v2_dir = os.path.join(base_dir, 'script-v2')
if os.path.exists(script_v2_dir):
    shutil.move(script_v2_dir, os.path.join(base_dir, 'script'))

# 3. Create dev.html
dev_path = os.path.join(base_dir, 'dev.html')
shutil.copy2(index_path, dev_path)

# Also update the title in dev.html to indicate it's the dev version
with open(dev_path, 'r', encoding='utf-8') as f:
    dev_text = f.read()

dev_text = dev_text.replace('<title>VCV Play 26/27</title>', '<title>DEV - VCV Play</title>')

with open(dev_path, 'w', encoding='utf-8') as f:
    f.write(dev_text)

print("Project successfully reorganized and guest button disabled.")
