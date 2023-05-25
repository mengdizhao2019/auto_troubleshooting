import execution_obj
import param_filter

class te_query:
    def _checkMultiDC(self):
        ed = execution_obj.ExecutionDef("te multi dc", 'resourcemanager')
        ed.SetRef('multi dc issue, please see case 153798')
        ed.SetUsedCases('153798;')
        md = execution_obj.MatchDef('simple_string', 'enable DC command with empty primary database list')

        # qp1 = param_filter.QueryParam('begintime', '2022-12-01', '>', 'datetime')
        # qp2 = param_filter.QueryParam('endtime', '2022-12-30 14', '<', 'datetime')
        # md._paramFilter = param_filter.ParamFilter('time', [qp1, qp2], ['and'])
        ed._matchDefList.append(md)
        #ed._collect.append('pid')
        #ed._collect.append('time')
        ed._collect.append('msg')
        return ed

    def teHealth(self):
        ed = execution_obj.ExecutionDef("te Health check", 'task-engine')
        ed.SetRef('please use [workerserver.xfagent health check]')
        ed.SetUsedCases('154758;')
        md = execution_obj.MatchDef('simple_string', 'will not be selected')

        # qp1 = param_filter.QueryParam('begintime', '2022-12-01', '>', 'datetime')
        # qp2 = param_filter.QueryParam('endtime', '2022-12-30 14', '<', 'datetime')
        # md._paramFilter = param_filter.ParamFilter('time', [qp1, qp2], ['and'])
        ed._matchDefList.append(md)
        #ed._collect.append('pid')
        #ed._collect.append('time')
        ed._collect.append('msg')

        
        ed2 = execution_obj.ExecutionDef("te Health check from webserver", 'ng.log')
        ed2.SetRef('please use [workerserver.xfagent health check]')
        ed2.SetUsedCases('154758;')
        md2 = execution_obj.MatchDef('simple_string', 'worker server is not started')
        qp1 = param_filter.QueryParam('begintime', '2022-12-01', '>', 'datetime')
        qp2 = param_filter.QueryParam('endtime', '2022-12-30 14', '<', 'datetime')
        md2._paramFilter = param_filter.ParamFilter('time', [qp1, qp2], ['and'])
        ed2._matchDefList.append(md)
        #ed2._collect.append('pid')
        ed2._collect.append('time')
        ed2._collect.append('msg')

        eo = execution_obj.ExecutionObj([ed, ed2, self._checkMultiDC()])
        eo._info['category'] = 'Framework'
        eo._info['name'] = 'TaskEngine Health check'
        eo.SetDescription('taskengine logs; webserver logs; worker server logs')
        return [eo]
    