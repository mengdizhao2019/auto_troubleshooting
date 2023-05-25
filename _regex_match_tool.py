import re

line = r''

regstr = r''
ret = re.search(regstr, line)
if ret:
    for value in ret.groups():
        print(value)