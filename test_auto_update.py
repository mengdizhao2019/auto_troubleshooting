import auto_update
import os
import sys

print ('replaced1')
if True:
    installfolder= os.path.split(sys.argv[0])
    au = auto_update.AutoUpdate(installfolder, '1.0', 'http://localhost:8080/static/download/latest_version.zip', 'http://localhost:8080/version')
    au.Update()
    print('end2')
print ('replaced2')