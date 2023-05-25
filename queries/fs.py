import execution_obj
import param_filter

class fs_query:

    
    def _findReboot(self):
        ed = execution_obj.ExecutionDef('FS restart', 'fs.log')
        ed.SetRef('There are some issues can cause FS restart. Top issues below: CLI thread stuck, ')
        ed._matchDefList.append(execution_obj.MatchDef('simple_string', 'everything '))
        ed._collect.append('pid')
        ed._collect.append('time')
        ed._groupby.append('pid')
        return ed

    def getScheduleExecutionDef(self):
        ed = execution_obj.ExecutionDef('Schedule pool', 'Scheduler_Priority.log')
        ed._matchDefList.append(execution_obj.MatchDef('regex', 'ScheduleTask] Type',
                                                  r'ScheduleTask]\s+Type:\s*(\d+),\s*SSH:\s*(\d+).\s*Queue:\s*(\d+),\s*waiting:\s*(\d+),\s*running:\s*(\d+)',
                                                  [param_filter.ValueDef("type"), param_filter.ValueDef("is ssh"), param_filter.ValueDef("queue"),
                                                   param_filter.ValueDef("waiting"), param_filter.ValueDef("running")]))
        ed._collect.append('pid')
        ed._collect.append('time')
        ed._groupby.extend(['pid', 'type', 'is ssh', 'queue'])
        ed._single = True
        ed._singleStrategy = execution_obj.SingleStrategy("waiting", "<")


        ed2 = execution_obj.ExecutionDef('Schedule pool last value', 'Scheduler_Priority.log')
        ed2._matchDefList.append(execution_obj.MatchDef('regex', 'ScheduleTask] Type',
                                                  r'ScheduleTask]\s+Type:\s*(\d+),\s*SSH:\s*(\d+).\s*Queue:\s*(\d+),\s*waiting:\s*(\d+),\s*running:\s*(\d+)',
                                                  [param_filter.ValueDef("type"), param_filter.ValueDef("is ssh"), param_filter.ValueDef("queue"),
                                                   param_filter.ValueDef("waiting"), param_filter.ValueDef("running")]))
        ed2._collect.append('pid')
        ed2._collect.append('time')
        ed2._groupby.extend(['pid', 'type', 'is ssh', 'queue'])
        ed2._single = True

        eo = execution_obj.ExecutionObj([ed2, ed])
        eo.SetCategory('FrontServer')
        eo._info['name'] = ed._name
        eo.SetDescription('fs logs')
        return [eo]


    def screenFSError(self):
        ed = execution_obj.ExecutionDef("Stuck CLI thread issue", 'Error.log')
        ed._matchDefList.append(execution_obj.MatchDef('simple_string', 'is stuck'))
        ed.SetRef('please run [benchmark.check live access performance on FS side]')
        ed._collect.append('pid')
        ed._collect.append('time')
        ed._collect.append('msg')
        ed._groupby.append('pid')

        
        ed3 = execution_obj.ExecutionDef("CLI performance issue", 'Error.log')
        ed.SetRef('need to do')
        ed3._matchDefList.append(execution_obj.MatchDef('simple_string', 'is running too long time '))

        ed3._collect.append('pid')
        ed3._collect.append('time')
        ed3._collect.append('msg')
        ed3._groupby.append('pid')
        eo = execution_obj.ExecutionObj([ed, self._findReboot(), ed3])
        

        ed2 = execution_obj.ExecutionDef("Memory issue", 'Error.log')
        ed2._matchDefList.append(execution_obj.MatchDef('simple_string', 'the memory reached '))
        ed2._collect.append('pid')
        ed2._collect.append('time')
        ed2._collect.append('msg')
        ed2._groupby.append('pid')
        eo._executionDefList.append(ed2)
        eo.SetCategory('FrontServer')
        eo._info['name'] = 'FS health check'
        eo.SetDescription('require fs logs; to check fs health')
        eoList = [eo]
        return eoList