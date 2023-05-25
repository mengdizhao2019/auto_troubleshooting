import shutil
import zipfile
import urllib.request
import os
import sys
import utility
import json

class AutoUpdate:
    def __init__(self, rootFolder, currentVersion, downloadUrl, checkVersionUrl, resourceversion) -> None:
        self._rootFolder = rootFolder
        self._currentVersion = float(currentVersion)
        self._downloadUrl = downloadUrl
        self._checkVersionUrl = checkVersionUrl
        self._resourceversion = resourceversion

    def IsUpdateMode(self):
        bFindUpdate = False
        for item in sys.argv:
            print('item:{}.'.format(item))
            if item.strip() == '-update':
                bFindUpdate = True
                break
        return bFindUpdate
    
    def CopyBack(self):
        path = os.path.dirname(sys.executable)
        filename = os.path.splitext(os.path.basename(sys.executable))

        newexecutable = os.path.join(self._rootFolder, '{}{}'.format(filename[0].replace('_bak', ''), filename[1]))
        shutil.copy2(sys.executable, newexecutable)

        print(sys.executable, *sys.argv, path, filename)
        python = newexecutable
        sys.argv.remove('-update')
        print('------------------------CopyBack', sys.argv)
        ret = os.execl(python, python, *sys.argv)

    def CopyAndRestart(self, newfilepath, originFilePath):
        path = os.path.dirname(sys.executable)
        filename = os.path.splitext(os.path.basename(sys.executable))

        newexecutable = os.path.join(self._rootFolder, '{}_bak{}'.format(filename[0], filename[1]))
        shutil.copy2(newfilepath, newexecutable)

        print(sys.executable, *sys.argv, path, filename)
        python = newexecutable
        sys.argv.append('-update')
        print('------------------------CopyAndRestart', sys.argv)
        ret = os.execl(python, python, *sys.argv)

    def Update(self):
        timeout = 3
        try:
            response = urllib.request.urlopen(self._checkVersionUrl, timeout=timeout)
            latest_version = float(response.read().decode('utf-8'))
            print("latest version is:{}".format(latest_version))

            if latest_version > (self._currentVersion+self._resourceversion):
                print('===>NEED TO DO AUTOUPDATE<===')
                auto_update_path = os.path.join(self._rootFolder, 'auto_update')
                print("auto update file path:", auto_update_path)
                if not os.path.exists(auto_update_path):
                    os.mkdir(auto_update_path)
                else:
                    utility.delete_all_files(auto_update_path)

                downloadFilePath = os.path.join(auto_update_path, 'latest_program.zip')
                print(downloadFilePath)
                urllib.request.urlretrieve(self._downloadUrl, downloadFilePath)
                
                
                with zipfile.ZipFile(downloadFilePath, 'r') as zip_ref:
                    zip_ref.extractall(auto_update_path)

                replaceMap = []
                with open(os.path.join(auto_update_path, 'update_list.json'), 'r') as f:
                    replaceMap = json.load(f)
                
                restart_filepath = ""
                restart_originFilePath = ""
                for filepath, operate in replaceMap.items():
                    if operate == 'replace':
                        originFilePath = os.path.join(self._rootFolder, filepath)
                        originFileFolder = os.path.dirname(originFilePath)
                        if not os.path.exists(originFileFolder):
                            os.makedirs(originFileFolder)

                        if os.path.exists(originFilePath):
                            os.remove(originFilePath)
                        newfilepath = filepath
                        shutil.copy2(os.path.join(auto_update_path, newfilepath), originFilePath)
                    elif operate == 'restart':
                        originFilePath = os.path.join(self._rootFolder, filepath)
                        originFileFolder = os.path.dirname(originFilePath)
                        if not os.path.exists(originFileFolder):
                            os.makedirs(originFileFolder)

                        newfilepath = filepath
                        restart_filepath = os.path.join(auto_update_path, newfilepath)
                        restart_originFilePath = originFilePath
                        
                if restart_filepath == "":
                    print(sys.executable, *sys.argv)
                    python = sys.executable
                    ret = os.execl(python, python, *sys.argv)
                    print(ret)
                else:
                    self.CopyAndRestart(restart_filepath, restart_originFilePath)
        except urllib.error.URLError as e:
            print('error: ', e)
