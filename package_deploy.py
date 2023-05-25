import zipfile
import json
import os
import shutil

zip_path = 'auto_troubleshooting.zip'

target_file = 'fix_conf.json'

with zipfile.ZipFile(zip_path, 'a') as zip_file:
    if target_file in zip_file.namelist():
        print(f"The file '{target_file}' already exists in the zip file.")
    else:
        fixconf = {
            "baseurl":'http://192.168.75.53:8081'
        }
        new_file_contents = json.dumps(fixconf)
        zip_file.writestr(target_file, new_file_contents)
        print(f"The file '{target_file}' was added to the zip file.")

web_download_folder = r'C:\temp\auto_troubleshooting\webserver\auto_troubleshooting_web_server\static\downloads'
targetPath = os.path.join(web_download_folder, zip_path)
if os.path.exists(targetPath):
    os.remove(targetPath)
shutil.copy2(zip_path, targetPath)

