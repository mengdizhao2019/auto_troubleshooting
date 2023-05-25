#utf-8
from time import time
import datetime
import os
import os.path
import string
import json
import sys
import traceback
import execution_obj
import param_filter
import scan_helper
import glob
import importlib
import queries.fs
import queries.benchmark
import queries.autoupdate
import queries.xf
import queries.worker_server
import queries.taskengine
import utility
 



class ErrorFinder:
    def __init__(self, line):
        self._current_Pid = ""
        self._eoList = []



def fs(ef):
    fs = queries.fs.fs_query()
    ef._eoList.extend(fs.screenFSError())
    ef._eoList.extend(fs.getScheduleExecutionDef())

def xf(ef):
    xf = queries.xf.xfagent_query()
    ef._eoList.extend(xf.xfagentHealth())
def te(ef):
    te = queries.taskengine.te_query()
    ef._eoList.extend(te.teHealth())

def autoupdate(ef):
    autoupdate_query =queries.autoupdate.autoupdate_query()
    ef._eoList.extend(autoupdate_query.ErrorCheck())

def workerserver(ef):
    ws= queries.worker_server.worker_server_query()
    ef._eoList.extend(ws.exportAllFindTaskExecutions())

def benchmark(ef):
    b = queries.benchmark.benchmark_query()
    ef._eoList.extend(b.deviceAccessLog())
    ef._eoList.extend(b.findUnfinishedDevice())
    ef._eoList.extend(b.screenRetrieveLive())
    ef._eoList.extend(b.liveaccessPerformance())
    ef._eoList.extend(b.fsConnectionLimitCheck())
    ef._eoList.extend(b.splitfslogs())

    

def addAll(ef):
    fs(ef)
    xf(ef)
    te(ef)
    autoupdate(ef)
    workerserver(ef)
    benchmark(ef)

def process_task(dirname, params):
    xx = scan_helper.ScanHelper()
    dirname = r'C:\temp\auto_troubleshooting\frontsvr'
    print('dirname is ', dirname)
    lines = []
    status1 = {}
    ef = ErrorFinder("")
    
    addAll(ef)

    # b = queries.benchmark.benchmark_query()
    
    # ef._eoList.extend(b.splitfslogs())

    ef._eoList[0].SetInput('{"begintime":"2019-02-04 1", "endtime":"2019-02-04 16"}')
    
    for eo in ef._eoList:
        filename = utility.convert_special_characters( "{}_{}.json".format(eo.GetCategory(), eo.GetName()))
        filename = os.path.join('data\\execution_objs\\', filename)
        print(filename)
        with open(filename, 'w') as file:
            json_data = json.dumps(eo, cls= execution_obj.ExecutionObjEncoder, indent=4)
            file.write(json_data)

    # with open('data.json', 'r') as f:
    #     ef._eoList = json.load(f, cls=  execution_obj.ExecutionObjDecoder)
        
    # with open(r'C:\temp\auto_troubleshooting\data\execution_objs\Find Unfinished Devices.json', 'r') as f:
    #     ef._eoList = [json.load(f, cls=  execution_obj.ExecutionObjDecoder)]
    xx._eoList = ef._eoList
    xx.loopDir(dirname, status1, lines, xx.DoScanAll, "log")


    retMap = {}
    for key, value in status1.items():
        if isinstance(value, list):
            keyList = []

            if len(value) > 1:
                executionDef = value[0]._executionDef
                if len(executionDef._orderby) == 1:
                    value.sort(key=lambda p:p.get(executionDef._orderby[0]))

            for sd in value:
                executionDef = sd._executionDef

                if executionDef not in retMap:
                    retMap[executionDef] = []

                ss = ''
                for output in executionDef._collect:
                    ss += "{}:{},".format(output, sd.get(output))

                keyList.append(ss.rstrip(','))

            if executionDef.DoLogicalCheck(value):
                retMap[executionDef].append((key, keyList))
        else:
            sd = value
            executionDef = sd._executionDef

            if executionDef not in retMap:
                retMap[executionDef] = []

            ss = ''
            for output in executionDef._collect:
                ss += "{}:{},".format(output, sd.get(output))

            for matchdef in executionDef._matchDefList:
                for item in matchdef._groupCollection:
                    ss += "{}:{},".format(item._name, sd.get(item._name))
            retMap[executionDef].append(ss.rstrip(','))

    for executionDef, msgList in retMap.items():
        errortype = executionDef._name
        print('==={} Summary, Find Results {}. Hint:{}'.format(errortype, len(msgList), executionDef.GetRef()))
        
        for msg in msgList:
            if isinstance(msg, str):
                print('\t'+msg)
            else:
                key = msg[0]
                keyList = msg[1]
                print('\t---{}'.format(key))
                for submsg in keyList:
                    print('\t\t' + submsg)

if __name__ == "__main__":
    param = {}
    fname = os.path.split(os.path.realpath(sys.argv[0]))[0]
    print('mzhao:', fname, sys.executable)

    try:
        cmd = sys.argv[1]
        fname = cmd
    except:
        print("cmd type is null, will ananysis whole log")
        cmd = None

    if cmd == "bydate":
        try:
            begin = sys.argv[2]
        except:
            print("begin of date is null, will ananysis whole log")
            begin = None

        try:
            end = sys.argv[3]
        except:
            print("end of date is null, will ananysis whole log")
            end = None

        try:
            fname = sys.argv[4]
        except:
            print("worker server log folder is null, will use default folder ./ to analysis.")
            print(fname)

        if begin and end:
            param["begin"] = datetime.datetime.strptime(begin, "%Y-%m-%dT%H:%M")
            param["end"] = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M")

    process_task(fname, param)

    print("end")
else:
    #dirname2 = dirname + os.sep + "!analysis"
    #if not os.path.exists(dirname2):
    #    os.mkdir(dirname2)
    pass