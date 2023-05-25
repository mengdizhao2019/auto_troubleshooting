import execution_obj
import param_filter

class query:


    def _simple_query(self, name, logfilter, key, ref, useredcases, collectList, groupbyList):
        ed4 = execution_obj.ExecutionDef(name, logfilter)
        ed4.SetUsedCases(useredcases)
        ed4.SetRef(ref)
        md4 = execution_obj.MatchDef('simple_string', key)
        ed4._matchDefList.append(md4)
        ed4._collect = collectList
        ed4._groupby = groupbyList
        return ed4