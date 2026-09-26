import os
import shutil
import datetime
backup_dir = 'backups/v2_stable_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(backup_dir, exist_ok=True)
shutil.copy2('v2.html', os.path.join(backup_dir, 'v2.html'))
shutil.copy2('script-v2/Código.js', os.path.join(backup_dir, 'Código.js'))
print('Backup created at ' + backup_dir)
