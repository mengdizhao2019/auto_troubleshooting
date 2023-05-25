import os
import json
import sys
print(os.path.abspath('.')) 
sys.path.append(os.path.abspath('.'))
#print(os.path)
import execution_obj


class category_srvc:
    def __init__(self) -> None:
        self._eoList = []

    def Load(self):
        ll = []
        category_folder = r'data/execution_objs'
        for root, dirs, files in os.walk(category_folder):
            for file in files:
                file_path = os.path.join(root, file)
                
                _, extension = os.path.splitext(file_path)
                        
                with open(file_path, 'r') as f:
                    ll.append(json.load(f, cls=  execution_obj.ExecutionObjDecoder))
        self._eoList = ll
        return ll

    def GetCategories(self):
        ll = []
        for eo in self._eoList:
            ll.append(eo._info['category'])
        ll = list(set(ll))
        ll.sort(reverse=False)
        return ll

    def GetExecutionObjsByCategory(self, category):
        ll = []
        for eo in self._eoList:
            if category == eo._info['category']:
                ll.append(eo)
        return ll

    def GetExecutionObjByName(self, name):
        for eo in self._eoList:
            if name == eo._info['name']:
                return eo
        return None

if __name__ == "__main__":
    cs = category_srvc()
    cs.Load()
    ret = cs.GetCategories()
    for c in ret:
        print(c)

