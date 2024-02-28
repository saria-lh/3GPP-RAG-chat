import os
import re
import shutil
import glob

from_folder_path = './downloaded_pdfs'
to_folder_path = './unique_pdfs'

files = os.listdir(from_folder_path)
latest_versions = {}

for file in files:
    match = re.match(r'(.+v)(\d+)((p|v|o|m)\.pdf)', file)
    if not match:
       latest_versions[file] = (0, file)
    else:
        base_name, version, ext, _ = match.groups()
        version = int(version)  # Convert version to integer for comparison
        if base_name not in latest_versions or version > latest_versions[base_name][0]:
            latest_versions[base_name] = (version, file)

for k in latest_versions.keys():
    file_name = latest_versions[k][1]
    src_path = os.path.join(from_folder_path, file_name)
    dest_path = os.path.join(to_folder_path, file_name)
    shutil.copy(src_path, dest_path)

dirs = ['ts', 'tr', 'es', 'en']
for dir_name in dirs:
    dir_path = os.path.join(to_folder_path, dir_name)
    os.makedirs(dir_path, exist_ok=True)

patterns = {
    'ts_*': 'ts',
    'tr_*': 'tr',
    'es_*': 'es',
    'en_*': 'en'
}

# Iterate over the patterns and move matching files to their target directories
for pattern, target_dir in patterns.items():
    for file_path in glob.glob(os.path.join(to_folder_path, pattern)):
        shutil.move(file_path, os.path.join(to_folder_path, target_dir))