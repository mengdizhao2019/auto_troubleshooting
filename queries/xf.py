import execution_obj
import param_filter

class xfagent_query:
    
    def xfagentHealth(self):
        ed = execution_obj.ExecutionDef("xfagent Health check", 'RMAgent')
        ed.SetRef('might caused by rmq, see case 154758. please use [task engine.health check]')
        ed.SetUsedCases('154758;')
        md = execution_obj.MatchDef('simple_string', 'Taskengine is long time not to reply XFAgent stops now')

        qp1 = param_filter.QueryParam('begintime', '2022-12-01', '>', 'datetime')
        qp2 = param_filter.QueryParam('endtime', '2022-12-30 14', '<', 'datetime')
        md._paramFilter = param_filter.ParamFilter('time', [qp1, qp2], ['and'])
        ed._matchDefList.append(md)
        #ed._collect.append('pid')
        ed._collect.append('time')
        ed._collect.append('msg')

        
        ed2 = execution_obj.ExecutionDef("xfagent Health check", 'RMAgent')
        ed2.SetRef('might caused by rmq, see case 154758. please use [task engine.health check]')
        ed2.SetUsedCases('154758;')
        md2 = execution_obj.MatchDef('simple_string', 'Failed to connect to RabbitMQ')

        qp1 = param_filter.QueryParam('begintime', '2022-12-01', '>', 'datetime')
        qp2 = param_filter.QueryParam('endtime', '2022-12-30 14', '<', 'datetime')
        md2._paramFilter = param_filter.ParamFilter('time', [qp1, qp2], ['and'])
        ed2._matchDefList.append(md2)
        #ed._collect.append('pid')
        ed2._collect.append('time')
        ed2._collect.append('msg')

        eo = execution_obj.ExecutionObj([ed,ed2])
        eo._info['category'] = 'Framework'
        eo._info['name'] = 'XFAgent Health check'
        eo.SetDescription('worker server logs; ')
        return [eo]
    