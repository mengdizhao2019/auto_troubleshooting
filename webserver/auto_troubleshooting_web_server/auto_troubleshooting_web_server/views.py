
from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime, timedelta

import sys
import os
import zipfile
import json

def mainpage(request):
    context          = {}
    return render(request, 'main.html', context)

def version(request):
    root_folder = os.path.dirname(os.path.abspath(__file__))
    root_folder = os.path.dirname(root_folder)
    print(root_folder)
    # 打开zip文件
    with zipfile.ZipFile(os.path.join(root_folder, 'static\downloads\\auto_troubleshooting.zip'), 'r') as zip_file:
        # 读取zip文件中的所有文件名
        filenames = zip_file.namelist()
        for filename in filenames:
            # 如果文件名以.txt结尾，就打印文件内容
            if filename.endswith('update_list.json'):
                with zip_file.open(filename) as file:
                    contents = file.read()
                    updateinfo = json.loads(contents)
                    mainversion = updateinfo['version']
                    resource_version = updateinfo['resource_version']
                    ss = '{}'.format(str(float(mainversion)+float(float(resource_version)/100000)))
                    return HttpResponse(ss)

    return HttpResponse('1.0')