from utility import find_pid_tid
import re

class CShape(dict):
    def __init__(self) -> None:
        pass
    def FindPidTid(self, line, pidonly):
        ret = re.search(r'\[(.*?)\]', line)
        if ret:
            return ret.group(1)
        return "-1"

class CplusPlus(dict):
    def __init__(self) -> None:
        pass
    def FindPidTid(self, line, pidonly):
        return find_pid_tid(line, pidonly)
    

if __name__ == "__main__":
    log = r"2022-12-18 16:59:34,921 (2022-12-18 16:59:34,921 UTC) [891] INFO  NBConfig [(null)] - Reading NBRMConfig json file D:\Program Files\NetBrain\Worker Server\conf\\fix_NBRMConfig.json whose content is: "
    #log = r'2022-12-19 20:09:57,472 (2022-12-19 20:09:57,472 UTC) [WorkPool-Session#5:Connection(81a6573f-7eaa-4045-a011-640af99c7e85,amqp://147.204.120.26:5672)] INFO  PayLoad [(null)] - Payload # nb-worker-a-2_xf_9 receives message new task selfTaskId=4594d03f-17b8-4ec1-bbe5-4a6a9e4d50d3, rootTaskId=0b7398f1-478c-4aef-a3cb-b031b19a6ebc, taskType=LiveRetrieveMultiDevice, at localtime 12/19/2022 8:09:57 PM.'
    ret = CShape().FindPidTid(log)
    print(ret)