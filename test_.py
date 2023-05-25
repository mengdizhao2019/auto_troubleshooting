import zipfile
import json

# 打开zip文件
with zipfile.ZipFile('auto_troubleshooting.zip', 'r') as zip_file:
    # 读取zip文件中的所有文件名
    filenames = zip_file.namelist()
    for filename in filenames:
        # 如果文件名以.txt结尾，就打印文件内容
        if filename.endswith('update_list.json'):
            with zip_file.open(filename) as file:
                contents = file.read()
                updateinfo = json.loads(contents)
                print(updateinfo['version'])
                break
