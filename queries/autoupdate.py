import execution_obj
import param_filter
from . import query

class autoupdate_query(query.query):
    
     
    def ErrorCheck(self):
        ed = execution_obj.ExecutionDef('Failed to remove folder', 'AutoUpdateClient.log')
        ed.SetUsedCases('155484;')
        ed.SetRef('Might failed update. please see case 155484')
        ed._matchDefList.append(execution_obj.MatchDef('simple_string', 'Failed to remove folder:'))
        ed._collect.append('msg')
        # ed._groupby.extend(['time'])

        ed2 = self._simple_query('Failed to dump package file', 'update','Failed to dump package file', 'not enough RAM or lack privilege on the server, see case 155694', '155694', 
                                 collectList=['msg'], groupbyList=[])

        eo = execution_obj.ExecutionObj([ed, ed2])
        eo.SetCategory('Autoupdate')
        eo.SetName('Error Check')
        eo.SetDescription('need autoupdateClient logs, KCProxy log; check update error.')

        return [eo]
