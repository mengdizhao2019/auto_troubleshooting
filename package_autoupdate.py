import zipfile
import json
import os
import shutil
import auto_troubleshooting_UI

zip_path = 'auto_troubleshooting.zip'



def LoadResourceVersion(self):
    filename = os.path.join(self.root_folder, r'data\resource_version.json')
    if os.path.exists(filename):
        with open(filename) as fp:
            conf = json.load(fp)
            return conf['version']
    return ''

def zip_directory(path, zipf, dictAutoUpdate):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path)
            dictAutoUpdate[file_path] = 'replace'
        # for dir in dirs:
        #     dir_path = os.path.join(root, dir)
        #     zipf.write(dir_path, os.path.relpath(dir_path, path))
        #     #dictAutoUpdate[file_path] = 'replace'

def AddFileToZip(zipf, filename, mode, dictAutoUpdate, dest = ''):
    if dest == '':
        zipf.write(filename)
        dictAutoUpdate[filename] = mode
    else:
        zipf.write(filename, dest)
        dictAutoUpdate[dest] = mode


def LoadResourceVersion():
    filename = r'data\resource_version.json'
    if os.path.exists(filename):
        with open(filename) as fp:
            conf = json.load(fp)
            return conf['version']
    return ''

def ChangeResourceVersion():
    filename = r'data\resource_version.json'
    if os.path.exists(filename):
        with open(filename) as fp:
            conf = json.load(fp)
            conf['version'] = conf['version'] + 1

        with open(filename, 'wt') as fp:
            json_data = json.dumps(conf, indent=4)
            fp.write(json_data)
        
    return ''


ChangeResourceVersion()
dictAutoUpdate = {}
dictAutoUpdate['version'] = auto_troubleshooting_UI.AutoTroubleMainUI._currentVersion
dictAutoUpdate['resource_version'] = LoadResourceVersion()

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zip_directory('data', zipf, dictAutoUpdate)
    AddFileToZip(zipf, 'debug.ico', 'replace', dictAutoUpdate)
    AddFileToZip(zipf, 'dist\\auto_troubleshooting_UI.exe', 'restart', dictAutoUpdate, 'auto_troubleshooting_UI.exe')

    ss = json.dumps(dictAutoUpdate, indent=4)
    print(ss)
    zipf.writestr('update_list.json', ss)

