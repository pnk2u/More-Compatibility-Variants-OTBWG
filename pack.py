import os
import zipfile
from jproperties import Properties
import subprocess
import shutil

folder_name = os.path.basename(os.getcwd())

configs = Properties()
with open('pack.properties', 'rb') as f:
    configs.load(f)

project_version = configs.get('project_version').data
minecraft_version = configs.get('minecraft_version').data
zip_name = f"{folder_name}-{project_version}+{minecraft_version}.zip"

required = ['data', 'pack.mcmeta', 'pack.png', 'pack.properties']
for item in required:
    if not os.path.exists(item):
        raise FileNotFoundError(f"Missing required: {item}")

seven_zip = shutil.which('7z') or shutil.which('7za') or shutil.which('7zr')

if seven_zip:
    subprocess.run([seven_zip, 'a', zip_name, 'data', 'pack.mcmeta', 'pack.png'], check=True)
else:
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('data'):
            for file in files:
                filepath = os.path.join(root, file)
                zipf.write(filepath, arcname=os.path.relpath(filepath, '.'))
        zipf.write('pack.mcmeta')
        zipf.write('pack.png')

print(f"Successfully packed to: {zip_name}")