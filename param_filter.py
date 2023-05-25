from datetime import datetime
import utility
import json


class ValueDef:
    def __init__(self, name, type = 'str') -> None:
        self._type = type
        self._name = name

    def __dict__(self):
        return {
            '_type': self._type,
            '_name': self._name,
        }
    def to_dict(self):
        return self.__dict__()
    
    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj["_name"], dict_obj["_type"])
    
class QueryParam(ValueDef):
    def __init__(self, name, value, compare, type='str') -> None:
        super().__init__(name, type)
        self._compare = compare
        self._val = value
    def GetInputTemplate(self, inputParamMap):
        inputParamMap[self._name] = self._val
        

    def SetInput(self, inputObj):
        if self._name in inputObj:
            self._val = inputObj[self._name]
        else:
            self._type = "" #if we could not find the param, ignore this param

    def __dict__(self):
        base_dict = super().__dict__()
        base_dict['_compare'] = self._compare
        base_dict['_val'] = self._val
        return base_dict
    
    def Compare(self, val):
        if self._type == 'datetime':
            return True
        elif self._type == 'datetime':
            dt = utility.str_to_datetime(self._val)
            if self._compare == '>':
                if val > dt:
                    return True
            elif self._compare == '<':
                if val < dt:
                    return True
        elif self._type == "str":
            if self._compare == 'contents':
                if val.find(self._val) != -1:
                    return True
                
        return False

class ParamFilter:
    def __init__(self, field, params, relations) -> None:
        self._field = field
        self._params = params
        self._relations = relations

    def GetInputTemplate(self, inputParamMap):
        for param in self._params:
            param.GetInputTemplate(inputParamMap)
        
    def SetInput(self, inputObj):
        for param in self._params:
            param.SetInput(inputObj)

    def __dict__(self):
        return {
            '_field': self._field,
            '_params': [param.__dict__() for param in self._params],
            '_relations': self._relations,
        }
    
    def to_dict(self):
        return self.__dict__()
    def to_json(self):
        return json.dumps(self.__dict__())

    @classmethod
    def from_dict(cls, json_dict):
        params = [QueryParam(param['_name'], param['_val'], param['_compare'], param['_type']) for param in json_dict['_params']]
        return cls(json_dict['_field'], params, json_dict['_relations'])
    
    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return ParamFilter.from_dict(json_dict)
    
    def Judge(self, sd):
        if len(self._params) == 0:
            return True
        retList = []
        for param in self._params:
            retList.append(param.Compare(sd.get('time')))

        strcode = '{} '.format(retList[0])
        i = 1
        for relation in self._relations:
            strcode += '{} {} '.format(relation, retList[i])
            i += 1

        ret = eval(strcode)
        return ret

if __name__ == '__main__':
    

    qp1 = QueryParam('1', '2022-12-19', '>', 'datetime')
    qp2 = QueryParam('2', '2022-12-20 14', '<', 'datetime')
    pf = ParamFilter('time', [qp1, qp2], ['and'])
    str = pf.to_json()
    print(str)


    newpf = ParamFilter.from_json(str)
    print(type(newpf))
    for param in newpf._params:
        print(param._compare)
    pass
