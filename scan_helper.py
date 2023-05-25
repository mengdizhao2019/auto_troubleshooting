
import zipfile
import os
import traceback
import utility

class ScanHelper:
    def __init__(self):
        self._eoList = []
        self._unzipPathList = []

    def InteratorAllFiles(self, dirname):
        for rt, dirs, files in os.walk(dirname):
            for name in files:
                yield os.path.join(rt, name)
    
    def prepare(self, dirname):
        try:
            filelist = []
            for f in self.InteratorAllFiles(dirname):
                ext = f.split('.')[-1] #获取扩展名
                if ext == 'zip':
                    unzipPath = os.path.splitext(f)
                    with zipfile.ZipFile(f, 'r') as zip_ref:
                        zip_ref.extractall(unzipPath)

                    self._unzipPathList.append(unzipPath)

        except Exception as e:
            traceback.print_exc()
            print("Exection on prepare, f:{} ".format(f))

    def cleanUp(self, dirname):
        try:
            for unzipedPath in self._unzipPathList:
                utility.delete_all_files(unzipedPath)
        except Exception as e:
            traceback.print_exc()
            print("Exection on cleanUp, unzipedPath:{} ".format(unzipedPath))

    def DoScanAll(self, rootDirName, file, mm, lines):
        filename = file[0].lower()
        bFind = False
        for eo in self._eoList:
            for fileFilter in eo.GetFileFilter():
                if filename.find(fileFilter) != -1:
                    bFind = True
                    break
            if bFind:
                break

        if not bFind:
            return

        fp = open(file[0], encoding='utf-8')
        lineNO = 0
        while True:
            try:
                lineText = fp.readline()
                lineNO += 1
                if not lineText:
                    break
                try:
                    for eo in self._eoList:
                        eo.Execute(lineText, mm, filename)
                except Exception as e:
                    print("Exection error: file:{},line:{},execution:{}".format(file, lineText, eo._info))
                    traceback.print_exc()
            except:
                print("Read line exception: file:{},lineNO:{}".format(file, lineNO))
                traceback.print_exc()


    def loopDir(self, dirname, mm, lines, readfunc, key = 'NBLog.log'):
        filelist = []
        #for rt, dirs, files in os.walk(dirname):
        for f in self.InteratorAllFiles(dirname):
            if f.find(key) != -1:
                ext = f.split('.')[-1] #获取扩展名
                if ext.isdigit():
                    filelist.append((f, int(ext)))
                else:
                    filelist.append((f, 0))
                         
        filelist.sort(key=lambda x:x[1], reverse=True)#倒排序

        for k in filelist:
            readfunc(dirname, k, mm, lines)

    def __lt__(self, other):
        return self.time < other.time