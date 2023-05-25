
class StatusData:
    def __init__(self, name, executionDef = None):
        self._dict = {}
        self._name = name
        self._executionDef = executionDef
        

    def get(self, key):
        if key in self._dict:
            return self._dict[key]
        else:
            return "N/A"
    def set(self, key, value):
        self._dict[key] = value