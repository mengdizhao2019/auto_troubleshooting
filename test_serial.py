import json

class ValueDef:
    def __init__(self, name, type='str'):
        self._type = type
        self._name = name

    def __dict__(self):
        return {
            '_type': self._type,
            '_name': self._name,
        }

class QueryParam(ValueDef):
    def __init__(self, name, value, compare, type='str'):
        super().__init__(name, type)
        self._compare = compare
        self._val = value

    def __dict__(self):
        base_dict = super().__dict__()
        base_dict['_compare'] = self._compare
        base_dict['_val'] = self._val
        return base_dict

class ParamFilter:
    def __init__(self, field, params, relations):
        self._field = field
        self._params = params
        self._relations = relations

    def __dict__(self):
        return {
            '_field': self._field,
            '_params': [param.__dict__() for param in self._params],
            '_relations': self._relations,
        }

    def to_json(self):
        return json.dumps(self.__dict__())

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        params = [QueryParam(param['_name'], param['_val'], param['_compare'], param['_type']) for param in json_dict['_params']]
        return cls(json_dict['_field'], params, json_dict['_relations'])


qp1 = QueryParam('1', '2022-12-19', '>', 'datetime')
qp2 = QueryParam('2', '2022-12-20 14', '<', 'datetime')
pf = ParamFilter('time', [qp1, qp2], ['and'])
str = pf.to_json()
print(str)


newpf = ParamFilter.from_json(str)
print(type(newpf))
for param in newpf._params:
    print(param._compare)