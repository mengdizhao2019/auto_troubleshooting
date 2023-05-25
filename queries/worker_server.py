import execution_obj
import param_filter

class worker_server_query:

     
    def _rmTaskFinder(self, name, key):
        ed = execution_obj.ExecutionDef(name, 'RMAgent')
        ed.SetRef('just to find tasks.')
        #md = execution_obj.MatchDef('simple_string', 'Starting sub task (LiveAccessWorker.dll LiveRetrieveMultiDevice')
        md = execution_obj.MatchDef('simple_string', key)

        qp1 = param_filter.QueryParam('begintime', '2022-12-01', '>', 'datetime')
        qp2 = param_filter.QueryParam('endtime', '2022-12-30 14', '<', 'datetime')
        md._paramFilter = param_filter.ParamFilter('time', [qp1, qp2], ['and'])
        ed._matchDefList.append(md)
        ed._collect.append('pid')
        ed._collect.append('time')
        ed._collect.append('msg')

        eo = execution_obj.ExecutionObj(ed)
        eo._info['category'] = 'Workerserver'
        eo._info['name'] = ed._name
        eo.SetDescription('need worker server log;')
        return [eo]
    
    def exportAllFindTaskExecutions(self):
        ll = [('LiveRetrieveMultiDevice','Starting sub task (LiveAccessWorker.dll LiveRetrieveMultiDevice'),
              ('QappTriggerDataAnalysisTask', 'Starting root task (RunQappWorker.dll QappTriggerDataAnalysisTask'),
              #('', ''),
              ]
        ret = []
        for item in ll:
            ret.extend(self._rmTaskFinder(item[0], item[1]))

        return ret

