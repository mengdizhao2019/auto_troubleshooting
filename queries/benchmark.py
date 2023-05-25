import execution_obj
import param_filter

class benchmark_query:
    def fsConnectionLimitCheck(self):
        ed = execution_obj.ExecutionDef("Check connection limit", 'l3discover.log')
        ed.SetUsedCases('143844;150050')
        ed.SetRef('may caused by child device concurrency issue, see case 143844')
        ed._matchDefList.append(execution_obj.MatchDef('regex', 'reached its connection limit',
                                                       r'Device (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) reached its', [param_filter.ValueDef('ip')]))
        ed._collect.append('time')
        ed._collect.append('msg')
        ed._groupby.append('ip')
        ed._single = True
        eo = execution_obj.ExecutionObj([ed])
        eo.SetName('Connection limit check')
        eo._info['category'] = 'Benchmark'
        eo.SetDescription('need fs logs')
        return [eo]
        
    def liveaccessPerformance(self):
        ed = execution_obj.ExecutionDef("Check vt-100 performance", 'l3discover.log')
        ed._matchDefList.append(execution_obj.MatchDef('simple_string', 'process_cli_data() in ProcessReceive'))
        ed.SetUsedCases('15061;')
        ed.SetRef('vt-100 performance issues, please try the solution of case 150619. If it does not work please transfer to Dev Team')
        ed._collect.append('pid_tid')
        ed._collect.append('time')
        ed._collect.append('msg')
        ed._groupby.append('pid_tid')
        eo = execution_obj.ExecutionObj([ed])
        eo._info['category'] = 'Benchmark'

        # ed2 = execution_obj.ExecutionDef("memory issue", 'Error.log')
        # ed2._matchDefList.append(execution_obj.MatchDef('simple_string', 'the memory reached '))
        # ed2._collect.append('pid')
        # ed2._collect.append('time')
        # ed2._collect.append('msg')
        # ed2._groupby.append('pid')
        # eo._executionDefList.append(ed2)
        eo._info['name'] = 'Check live access performance on FS side'
        eo.SetDescription('require fs logs;')
        eoList = [eo]
        return eoList

    def splitfslogs(self):
        ed = execution_obj.ExecutionDef("Splitfslogs", 'l3discover.log')
        ed._matchDefList.append(execution_obj.MatchDef('simple_string', ''))
        ed._collect.append('pid_tid')
        ed._collect.append('time')
        ed._collect.append('msg')
        ed._groupby.append('pid_tid')
        ed._orderby.append('time')
        eo = execution_obj.ExecutionObj([ed])
        eo._info['category'] = 'Benchmark'


        eo._info['name'] = 'Split fs logs'
        eo.SetDescription('require fs logs;')
        eoList = [eo]
        return eoList

    def _addOneDeviceAccessLog(self, name, key, ref, useredcases):
        ed4 = execution_obj.ExecutionDef(name, 'log|txt')
        ed4.SetUsedCases(useredcases)
        ed4.SetRef(ref)
        md4 = execution_obj.MatchDef('simple_string', key)
        ed4._matchDefList.append(md4)
        ed4._collect.append('file')
        ed4._collect.append('msg')
        ed4._groupby.extend(['file'])
        return ed4

    def deviceAccessLog(self):
        ed = execution_obj.ExecutionDef("Device log-jumpbox timeout", 'log|txt')
        ed.SetUsedCases('155030;')
        ed.SetRef('cannot response cli result, ref to case 155030 the second issue(jumpbox timeout issue)')
        md = execution_obj.MatchDef('regex', 'CLI command takes too long',
                                            r'CLI command takes too long \(\d* second*\) Disconnect from Jumpbox',
                                            [param_filter.ValueDef("taskid"), param_filter.ValueDef("devicename")])
        ed._matchDefList.append(md)
        ed._collect.append('file')
        ed._collect.append('msg')
        ed._groupby.extend(['file'])

        
        ed2 = execution_obj.ExecutionDef("Device log-key exchange", 'log|txt')
        ed2.SetUsedCases('151149;')
        ed2.SetRef('ssh key exchange algothrims issue, see case 151149')
        md2 = execution_obj.MatchDef('simple_string', 'end disconnected during key negotiation')
        ed2._matchDefList.append(md2)
        ed2._collect.append('file')
        ed2._collect.append('msg')
        ed2._groupby.extend(['file'])

        ed3 = execution_obj.ExecutionDef("Device log-key exchange", 'log|txt')
        ed3.SetUsedCases('151149;')
        ed3.SetRef('ssh key exchange algothrims issue, see case 151149')
        md3 = execution_obj.MatchDef('simple_string', 'error code: 1001')
        ed3._matchDefList.append(md3)
        ed3._collect.append('file')
        ed3._collect.append('msg')
        ed3._groupby.extend(['file'])

        
        ed4 = execution_obj.ExecutionDef("Device log-network latency issue", 'log|txt')
        ed4.SetUsedCases('140447;')
        ed4.SetRef('network latency issue, see case 140447')
        md4 = execution_obj.MatchDef('simple_string', 'error code: 301')
        ed4._matchDefList.append(md4)
        ed4._collect.append('file')
        ed4._collect.append('msg')
        ed4._groupby.extend(['file'])
        ed5 = self._addOneDeviceAccessLog(name='Device log-tacacs concurrency issue', key='error code: 1032', 
                                          ref='may caused by TACACS concurrency issue, see case 152892', useredcases='151282')
        
        ed6 = self._addOneDeviceAccessLog(name='Device log-child device concurrency issue', key='is too busy to handle event', 
                                          ref='may caused by child device concurrency issue, see case 143844. run [benchmark.connection limit check]', 
                                          useredcases='143844;150050')
        
        eo = execution_obj.ExecutionObj([ed, ed2, ed3, ed4, ed5, ed6])
        eo._info['category'] = 'Benchmark'
        eo._info['name'] = "Screen Error From Device Logs"
        eo.SetDescription('device logs')
        return [eo]

    def findUnfinishedDevice(self):
        ed = execution_obj.ExecutionDef("RetrieveDevice_begin_and_end", 'NBLog.log')
        ed.SetUsedCases('154882;155030;')
        md = execution_obj.MatchDef('regex', 'OnBeginRetrieve:44]',
                                            'OnBeginRetrieve:44] {(.*?)} (.*?)$',
                                            [param_filter.ValueDef("taskid"), param_filter.ValueDef("devicename")])
        ed._matchDefList.append(md)
        ed._relations.append('and')
        
        md2 = execution_obj.MatchDef('regex', 'OnEndRetrieve','OnEndRetrieve {(.*?)} (.*?)$',
                                     [param_filter.ValueDef("taskid"), param_filter.ValueDef("devicename")])
        ed._matchDefList.append(md2)

        ed._collect.append('path')
        ed._collect.append('pid')
        #ed._collect.append('time')
        ed._collect.append('msg')
        ed._groupby.extend(['devicename', 'taskid', 'path'])

        ed2 = execution_obj.ExecutionDef("RetrieveDevice_begin", 'NBLog.log')
        md3 = execution_obj.MatchDef('regex', 'OnBeginRetrieve:44]',
                                            'OnBeginRetrieve:44] {(.*?)} (.*?)$',
                                            [param_filter.ValueDef("taskid"), param_filter.ValueDef("devicename")])
        ed2._matchDefList.append(md3)
        
        ed2._collect.append('path')
        ed2._collect.append('pid')
        #ed._collect.append('time')
        ed2._collect.append('msg')
        ed2._groupby.extend(['devicename', 'taskid', 'path'])

        eo = execution_obj.ExecutionObj([ed2, ed])
        eo._info['category'] = 'Benchmark'
        eo._info['name'] = "Find Unfinished Devices"
        eo.SetDescription('worker server logs')

        return [eo]
            

    def screenRetrieveLive(self):
        ed = execution_obj.ExecutionDef("LiveRetrieveMultiDevice", 'NBLog.log')
        md = execution_obj.MatchDef('simple_string', 'LiveAccessWorker.dll, LiveRetrieveMultiDevice')
        ed._matchDefList.append(md)
        ed._relations.append('and')
        
        md2 = execution_obj.MatchDef('simple_string', 'WorkerShell shutdown')
        ed._matchDefList.append(md2)

        ed._collect.append('path')
        ed._collect.append('pid')
        #ed._collect.append('time')
        ed._collect.append('msg')
        ed._groupby.extend(['path', 'pid'])

        ed2 = execution_obj.ExecutionDef("LiveRetrieveMultiDevice_begin", 'NBLog.log')
        md3 = execution_obj.MatchDef('simple_string', 'LiveAccessWorker.dll, LiveRetrieveMultiDevice')
        ed2._matchDefList.append(md3)
        
        ed2._collect.append('path')
        ed2._collect.append('pid')
        #ed._collect.append('time')
        ed2._collect.append('msg')
        ed2._groupby.extend(['path', 'pid'])

        eo = execution_obj.ExecutionObj([ed2, ed])
        eo._info['category'] = 'Benchmark'
        eo._info['name'] = "Find Unfinished LiveRetrieveMultiDevice Process"
        eo.SetDescription('worker server logs')

        return [eo]
    
