import os
import re
import statistics_data
import utility
import log_parser
import param_filter
import json


class MatchDef:
    def __init__(self, type, keyword, regex='', groupCollection=[], paramFilter = param_filter.ParamFilter('',[],[])) -> None:
        self._type = type #regex, simple_string
        self._keyword = keyword
        self._regex = regex
        self._groupCollection = groupCollection #[ValueDef]
        self._paramFilter = paramFilter
        
    
    def GetInputTemplate(self, inputParamMap):
        self._paramFilter.GetInputTemplate(inputParamMap)

    def SetInput(self, inputObj):
        self._paramFilter.SetInput(inputObj)

    def to_dict(self):
            return {
                "_type": self._type,
                "_keyword": self._keyword,
                "_regex": self._regex,
                "_groupCollection": [group.to_dict() for group in self._groupCollection],
                "_paramFilter": self._paramFilter.to_dict()
            }
    
    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            dict_obj["_type"],
            dict_obj["_keyword"],
            dict_obj["_regex"],
            [param_filter.ValueDef.from_dict(group) for group in dict_obj["_groupCollection"]],
            param_filter.ParamFilter.from_dict(dict_obj["_paramFilter"])
        )
    def isSimpleString(self):
        return self._type == "simple_string"

    def IsMatch(self, line):
        if self.isSimpleString():
            if line.find(self._keyword) != -1:
                return True
            return False
        else:
            if line.find(self._keyword) != -1:
                regstr = self._regex
                ret = re.search(regstr, line)
                if ret:
                    return ret
            return False
        
class SingleStrategy:
    def __init__(self, field, compare) -> None:
        self._field = field
        self._compare = compare

    def to_dict(self):
        return {
            "_field": self._field,
            "_compare": self._compare
        }

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj["_field"], dict_obj["_compare"])
    
class ExecutionDef:
    def __init__(self, name, fileFilter) -> None:
        self._name = name
        self._matchDefList = [] #MatchDef
        self._defInfo = {} # description, etc
        self._relations = []
        if isinstance(fileFilter, list):
            self._fileFilter = fileFilter
        else:
            self._fileFilter = fileFilter.lower().split('|')
        self._collect = []
        self._groupby = []
        self._orderby = []
        self._single = False
        self._singleStrategy = None
        self.initParser()
    
    def SetUsedCases(self, val):
        self._defInfo['usedCases'] = val

    def GetUsedCases(self):
        return self._defInfo['usedCases']
    
    
    def SetRef(self, val):
        self._defInfo['ref'] = val
    def GetRef(self):
        if 'ref' in self._defInfo:
            return self._defInfo['ref']
        return ""
    
    def to_dict(self):
        return {
            "_name": self._name,
            "_matchDefList": [match.to_dict() for match in self._matchDefList],
            "_defInfo": self._defInfo,
            "_relations" : self._relations,
            "_fileFilter" : self._fileFilter,
            "_collect": self._collect,
            "_groupby": self._groupby,
            '_orderby': self._orderby,
            "_single": self._single,
            "_singleStrategy": self._singleStrategy.to_dict() if self._singleStrategy is not None else None
        }

    @classmethod
    def from_dict(cls, dict_obj):
        execution_def = cls(dict_obj["_name"], dict_obj['_fileFilter'])
        execution_def._matchDefList = [MatchDef.from_dict(match) for match in dict_obj["_matchDefList"]]
        execution_def._defInfo = dict_obj["_defInfo"]
        execution_def._relations = dict_obj['_relations']
        execution_def._collect = dict_obj["_collect"]
        execution_def._groupby = dict_obj["_groupby"]
        execution_def._orderby = dict_obj['_orderby']
        execution_def._single = dict_obj["_single"]
        execution_def._singleStrategy = SingleStrategy.from_dict(dict_obj["_singleStrategy"]) if dict_obj["_singleStrategy"] is not None else None
        return execution_def
    
    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return ExecutionDef.from_dict(json_dict)
    
    def SetInput(self, inputObj):
        for matchdef in self._matchDefList:
            matchdef.SetInput(inputObj)
    def GetInputTemplate(self, inputParamMap):
        for matchdef in self._matchDefList:
            matchdef.GetInputTemplate(inputParamMap)

    def DoLogicalCheck(self, sdValues):
        if len(self._relations) == 0:
            return True
        
        if len(sdValues) > 0:
            strcode = '{} '.format(True)
            i = 1

            for relation in self._relations:
                if i < len(sdValues):
                    strcode += '{} {} '.format(relation, True)
                else:
                    strcode += '{} {}'.format(relation, False)
                i += 1

            ret = eval(strcode)
            return ret
        return False
                        
    def CanProcess(self, filepath):
        for filter in self._fileFilter:
            if filepath.find(filter) != -1:
                return True
        return False
    
    def DoExecute(self, line, mm, filepath):
        for matchdef in self._matchDefList:
            if matchdef.isSimpleString():
                if matchdef.IsMatch(line):
                    
                    sd = statistics_data.StatusData(self._name, self)
                    sd.set("error type", self._name)
                    for collectItem in self._collect:
                        self.setInternalValue(collectItem, sd, line, filepath)
        
                    if not matchdef._paramFilter or matchdef._paramFilter.Judge(sd):
                        self.doGroupBy(mm, sd)
                        return sd
            else:
                ret = matchdef.IsMatch(line)
                if ret:
                    sd = statistics_data.StatusData(self._name, self)
                    sd.set("error type", self._name)
                    for collectItem in self._collect:
                        self.setInternalValue(collectItem, sd, line, filepath)
                    
                    i = 0
                    for value in ret.groups():
                        if matchdef._groupCollection[i]._type == "int":
                            sd.set(matchdef._groupCollection[i]._name,  statistics_data.str2int(value))
                        else:
                            sd.set(matchdef._groupCollection[i]._name,  value)
                        i += 1
                                
                    if not matchdef._paramFilter or matchdef._paramFilter.Judge(sd):
                        self.doGroupBy(mm, sd)
                        return sd
        return None
    
    def initParser(self):
        if 'rmagent' in self._fileFilter:
            self._logParser = log_parser.CShape()
        else:
            self._logParser = log_parser.CplusPlus()
                               
    def doGroupBy(self, mm, sd):
        ss = "{}_".format(self._name)
        for groupby in self._groupby:
            ss += "{}_".format(sd.get(groupby))
        ss = ss.rstrip('_')
        if not self._single:
            if ss not in mm:
                mm[ss] = []
            mm[ss].append(sd)
        else:
            stragegy = self._singleStrategy
            if stragegy:
                if ss not in mm:
                    mm[ss] = sd
                else:
                    oldone = mm[ss]
                    if stragegy._compare == "<":
                        if oldone.get(stragegy._field) < sd.get(stragegy._field):
                            mm[ss] = sd
            else:
                mm[ss] = sd

    def setInternalValue(self, collectItem, sd, line, filepath):
        if collectItem == "path":
            sd.set("path", os.path.dirname(filepath))
        if collectItem == "file":
            sd.set("file", os.path.basename(filepath))
        if collectItem == "pid_tid":
            pid = self._logParser.FindPidTid(line, False)
            sd.set("pid_tid", pid)
        if collectItem == "pid":
            pid = self._logParser.FindPidTid(line, True)
            sd.set("pid", pid)
        if collectItem == "time":
            sd.set("time", utility.string_to_datetime(line))
        if collectItem == "msg":
            sd.set("msg", line.strip('\n'))

class ExecutionObj:
    def __init__(self, ed) -> None:
        if isinstance(ed, ExecutionDef):
            self._executionDefList = [ed]
        else:
            self._executionDefList = ed
        self._info = {}

    def GetInputTemplate(self):
        inputParamMap = {}
        for executionDef in self._executionDefList:
            executionDef.GetInputTemplate(inputParamMap)
        return inputParamMap

    def SetInput(self, inputStr):
        inputObj = json.loads(inputStr)
        for executionDef in self._executionDefList:
            executionDef.SetInput(inputObj)

    def GetFileFilter(self):
        ll = []
        for ed in self._executionDefList:
            ll.extend(ed._fileFilter)
        return ll
    

    def __dict__(self):
        return self.to_dict()

    def to_dict(self):
        return {
            '_executionDefList': [ed.to_dict() for ed in self._executionDefList],
            '_info' : self._info
        }

    @classmethod
    def from_dict(cls, d):
        edList =  [ExecutionDef.from_dict(ed) for ed in d["_executionDefList"]]
        eo = cls(edList)
        eo._info = d['_info']
        return eo

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return ExecutionObj.from_dict(json_dict)
    
    def Execute(self, line, mm, filepath):
        for executionDef in self._executionDefList:
            if executionDef.CanProcess(filepath):
                executionDef.DoExecute(line, mm, filepath)

    def GetName(self):
        return self._info['name']
    
    def SetName(self, val):
        self._info['name'] = val

    def SetDescription(self, val):
        self._info['description'] = val
    
    def GetDescription(self):
        if 'description' not in self._info:
            return self.GetName()
        return self._info['description']
    
    def GetCategory(self):
        return self._info['category']
    
    def SetCategory(self, val):
        self._info['category'] = val
    
        
    
class ExecutionDefEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ExecutionDef):
            return obj.to_dict()
        return super().default(obj)

class ExecutionDefDecoder(json.JSONDecoder):
    def decode(self, s):
        obj = super().decode(s)
        
        if isinstance(obj, list):
            ll = []
            for o in obj:
                eo = ExecutionDef.from_dict(o)
                ll.append(eo)
            return ll
        else:
            ed = ExecutionDef.from_dict(obj)
            return ed
        
    
class ExecutionObjEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ExecutionObj):
            return obj.to_dict()
        return super().default(obj)
    
class ExecutionObjDecoder(json.JSONDecoder):
    def decode(self, s):
        obj = super().decode(s)
        
        if isinstance(obj, list):
            ll = []
            for o in obj:
                eo = ExecutionObj.from_dict(o)
                ll.append(eo)
            return ll
        else:
            return ExecutionObj.from_dict(obj)
        
if __name__ == '__main__':
    
    ed = ExecutionDef('schedule pool')
    ed._matchDefList.append(MatchDef('regex', 'ScheduleTask] Type', 
                                                r'ScheduleTask]\s+Type:\s*(\d+),\s*SSH:\s*(\d+).\s*Queue:\s*(\d+),\s*waiting:\s*(\d+),\s*running:\s*(\d+)',
                                                [param_filter.ValueDef("type"), param_filter.ValueDef("is ssh"), param_filter.ValueDef("queue"),
                                                param_filter.ValueDef("waiting"), param_filter.ValueDef("running")]))
    ed._collect.append('pid')
    ed._collect.append('time')
    ed._groupby.extend(['pid', 'type', 'is ssh', 'queue'])
    ed._single = True
    ed._singleStrategy = SingleStrategy("waiting", "<")
    
    eo = ExecutionObj(ed, 'Scheduler_Priority.log')

    print(eo._executionDef._name)

    data = eo.to_json()
    data = json.dumps([eo, eo], cls= ExecutionObjEncoder)
    print(data)
    ll = json.loads(data, cls= ExecutionObjDecoder)
    #e2 =     ExecutionObj.from_json(data)
    for e2 in ll:
        print(e2._executionDef._name)