import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from srvc import category_srvc
import scan_helper
import json
import sys
import os
import auto_update
import ScrolledText
import utility
#from tkinter.scrolledtext import ScrolledText
    
    #resultText.config(width=width, height=height - 78)
class AutoTroubleMainUI(tk.Frame):
    _currentVersion = '1.8' 
    def on_category_select(self, event):
        if isinstance(event, ttk.Combobox):
            selection = event.get()
        else:
            selection = event.widget.get()
        print(selection)
        ret = self._categorySrvc.GetExecutionObjsByCategory(selection)
        ll = []
        for eo in ret:
            ll.append(eo._info['name'])
        ll.sort(reverse=False)
        self.oAnalysis['values'] = ll
        self.oAnalysis.current(0) 
        self.on_execution_obj_selected(self.oAnalysis)

    def CanDoAutoUpdate(self):
        bCanDo = True
        return bCanDo
    
    def LoadConf(self):
        self._baseurl = 'http://192.168.75.53:8081'
        if os.path.exists('fix_conf.json'):
            with open('fix_conf.json') as fp:
                conf = json.load(fp)
                self._baseurl = conf['baseurl']

    def LoadResourceVersion(self):
        filename = os.path.join(self.root_folder, r'data\resource_version.json')
        if os.path.exists(filename):
            with open(filename) as fp:
                conf = json.load(fp)
                return conf['version']
        return ''
    
    def __init__(self, parent):
        self.LoadConf()

        print("===================>sys.argv:", sys.argv)
        self.root_folder = os.path.dirname(os.path.abspath(__file__))

        print("current version:{}".format(self._currentVersion))
        
        resourceversion=float(self.LoadResourceVersion()/100000)

        au = auto_update.AutoUpdate(self.root_folder, self._currentVersion, self._baseurl+'/static/downloads/auto_troubleshooting.zip', self._baseurl+'/version', resourceversion)
        if self.CanDoAutoUpdate():
            if au.IsUpdateMode():
                print('do update++++++++++++++++++++')
                au.CopyBack()
            else:
                au.Update()
        
        self._categorySrvc = category_srvc.category_srvc()
        self._categorySrvc.Load()
        parent.iconbitmap("debug.ico")
        parent.title('Auto Troubleshooting V {}'.format(str(float(self._currentVersion) + resourceversion)))
        tk.Frame.__init__(self, parent)

            
        root.bind('<Configure>', self.on_resize)

        self.label = tk.Label(self, text="Feature Category:")
        self.label.place(x=0, y=0)
        self.oFeature = ttk.Combobox(self, width=50)
        self.oFeature.bind("<<ComboboxSelected>>", self.on_category_select)
        #ss = 'Benchmark;Live Access;Discover;Qapp;Topo;Deployment&Upgrade;Framework;NI;DataView'
        self.oFeature['values'] = list(self._categorySrvc.GetCategories())
        new_option = 'all'
        #self.oFeature['values'] = self.oFeature['values'] + (new_option,)
        self.oFeature.current(0) 
        self.oFeature.place(x=self.label.winfo_width(), y=0)
        self.label2 = tk.Label(self, text='IE Version:')
        self.oVersion = ttk.Combobox(self, width=50)
        self.oVersion['values'] = ['All']
        self.oVersion.current(0)  
        self.label2.place(x=self.label.winfo_width() + self.oFeature.winfo_width(), y=0)
        self.oVersion.place(x=self.label.winfo_width() +self.label2.winfo_width() + self.oFeature.winfo_width(), y=0)


        self.label3 = tk.Label(self, text="Select Analysis Item:")
        self.label3.place(x=0, y=25)
        self.oAnalysis = ttk.Combobox(self, width=35)
        self.oAnalysis.place(x=self.label3.winfo_width(), y=25)
        self.oAnalysis['values'] = ('please select a category')
        self.oAnalysis.bind("<<ComboboxSelected>>", self.on_execution_obj_selected)
        
        self.descriptionLabel = tk.Label(self, text="Description:")
        self.descriptionText = tk.Text(self)
        self.descriptionText.config(width=100, height=1)


        self.folderText = tk.Text(self, width=100, height=1)
        self.folderText.place(x=0, y=50)
        self.select_folder_btn = tk.Button(self, text='Select Folder', command=self.select_folder)
        self.select_folder_btn.place(x=self.folderText.winfo_width(), y=48)



        self.analysis_btn = tk.Button(self, text='Analysis', command=self.do_analysis)
        self.analysis_btn.place(x=self.oAnalysis.winfo_width() + self.oAnalysis.winfo_x(), y=200)

        self.open_result_btn = tk.Button(self, text='Open Result', command=self.open_result)
        self.open_result_btn.place(x=self.analysis_btn.winfo_width() + self.analysis_btn.winfo_x() + 5, y=200)

        self.save_result_btn = tk.Button(self, text='Save', command=self.save_result)
        self.save_result_btn.place(x=self.analysis_btn.winfo_width() + self.analysis_btn.winfo_x() + self.open_result_btn.winfo_x() +5 , y=200)



        self.label4 = tk.Label(self, text="input params:")
        self.label4.place(x=0, y=78)
        self.inputText = tk.Text(self)
        self.inputText.config(width=100, height=6)


        self.resultSummary = tk.Text(self, width=200, height=30)
        self.resultSummary.place(x=0, y=220)
        self.resultSummary.config(width=124, height=44)

        # self.scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        # self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # self.resultText.config(xscrollcommand=self.scrollbar_x.set)
        # #self.scrollbar_x.config(command=self.resultText.xview)
        # self.scrollbar_y = tk.Scrollbar(self)
        # self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        # self.resultText.config(yscrollcommand=self.scrollbar_y.set)
        # #self.scrollbar_y.config(command=self.resultText.yview)

            
        # self.scrollbar_y.config(command =self.resultText.yview)
        # self.scrollbar_x.config(command = self.resultText.xview)

        # self.resultText = ScrolledText(self, width=200, height=30)#, xscrollcommand = self.scrollbar_x.set,yscrollcommand = self.scrollbar_y.set )#, font=("Helvetica", 14))
        # self.resultText.pack(fill=tk.Y, side=tk.BOTTOM, expand=True)
        # #self.resultText.place(x=0, y = 220)
        # self.resultText.focus_set()

        self.folder_path = '123'
        self.AfterUICreated()

    def AfterUICreated(self):
        self.on_category_select(self.oFeature)

    def on_execution_obj_selected(self, event):
        if isinstance(event, ttk.Combobox):
            selection = event.get()
        else:
            selection = event.widget.get()
        print(selection)
        eo = self._categorySrvc.GetExecutionObjByName(selection)
        
        desc = ""
        if 'description' in eo._info:
            desc = eo._info['description']
        self.descriptionText.delete(1.0, tk.END)  # 清空文本框中的文字
        self.descriptionText.insert(tk.END, desc)  # 在文本框中插入新的文字

        inputstr = json.dumps(eo.GetInputTemplate(), indent=4)
        self.inputText.delete(1.0, tk.END)  # 清空文本框中的文字
        self.inputText.insert(tk.END, inputstr)  # 在文本框中插入新的文字

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.folderText.delete(1.0, tk.END)  # 清空文本框中的文字
        self.folderText.insert(tk.END, self.folder_path)  # 在文本框中插入新的文字

    def save_result(self):
        filetypes = [('Text files', '*.txt'), ('All files', '*.*')]
        eo = self.getSelectedExecutionObj()
        content = 'execution item:{}\ndescription:{}\n'.format(eo.GetName(), eo.GetDescription())
        content += self._result
        with  filedialog.asksaveasfile(defaultextension='.txt', filetypes=filetypes) as file:
            file.write(content)
            os.startfile(file.name)

    def getSelectedExecutionObj(self):
        selection = self.oAnalysis.get()
        eo = self._categorySrvc.GetExecutionObjByName(selection)
        return eo
    def open_result(self):
        ScrolledText.show_custom_dialog(self, self._result)

    def do_analysis(self):
        eo = self.getSelectedExecutionObj()
        
        inputJsonString = self.inputText.get('1.0', 'end-1c')
        eo.SetInput(inputJsonString)
        
        xx = scan_helper.ScanHelper()
        xx._eoList = [eo]
        lines = []
        status1 = {}
        analysisfolder = self.folderText.get('1.0', 'end-1c')
        xx.loopDir(analysisfolder, status1, lines, xx.DoScanAll, "log")
        
        retMap = {}
        for key, value in status1.items():
            if isinstance(value, list):
                keyList = []

                if len(value) > 1:
                    executionDef = value[0]._executionDef
                    if len(executionDef._orderby) == 1:
                        value.sort(key=lambda p:p.get(executionDef._orderby[0]))

                for sd in value:
                    executionDef = sd._executionDef

                    if executionDef not in retMap:
                        retMap[executionDef] = []

                    ss = ''
                    for output in executionDef._collect:
                        ss += "{}:{},".format(output, sd.get(output))

                    keyList.append(ss.rstrip(','))

                if executionDef.DoLogicalCheck(value):
                    retMap[executionDef].append((key, keyList))
            else:
                sd = value
                executionDef = sd._executionDef

                if executionDef not in retMap:
                    retMap[executionDef] = []

                ss = ''
                for output in executionDef._collect:
                    ss += "{}:{},".format(output, sd.get(output))

                for matchdef in executionDef._matchDefList:
                    for item in matchdef._groupCollection:
                        ss += "{}:{},".format(item._name, sd.get(item._name))
                retMap[executionDef].append(ss.rstrip(','))

        resultSummary = ''
        self._result = ''
        for executionDef, msgList in retMap.items():
            errortype = executionDef._name
            summary = '==={} Summary, Find Results {}. Hint:{}\n'.format(errortype, len(msgList), executionDef.GetRef())
            self._result += summary
            resultSummary += summary

            for msg in msgList:
                if isinstance(msg, str):
                    self._result += '\t{}\n'.format(msg)
                else:
                    key = msg[0]
                    keyList = msg[1]
                    self._result += '\t---{}\n'.format(key)
                    for submsg in keyList:
                        self._result += '\t\t{}\n'.format(submsg)

        resultsize = utility.convert_to_mb(len(self._result))
        self.resultSummary.delete(1.0, tk.END)  
        if resultsize > 10:
            self.resultSummary.insert(tk.END, 'Total size: {}MB. The result is too large. Please save it and check.\n{}'.format(resultsize, resultSummary))  
            self.open_result_btn.config(state="disabled")
        else:
            self.resultSummary.insert(tk.END, 'Total size: {}MB\n{}'.format(resultsize, resultSummary))  
            self.open_result_btn.config(state="normal")

    def on_resize(self, event):
        #print(self.folder_path)
        widthMain = event.width
        heightMain = event.height

        #print(f"New size: {widthMain}x{heightMain}, self.resultText:{self.resultText.winfo_width()}x{self.resultText.winfo_height()}")

        #print('label.winfo_width()=', label.winfo_width())
        self.oFeature.place(x=self.label.winfo_width()+2, y=0)

        self.label2.place(x=self.label.winfo_width() + self.oFeature.winfo_width() + 2, y=0)
        self.oVersion.place(x=self.label.winfo_width() +self.label2.winfo_width() + self.oFeature.winfo_width() + 2, y=0)

        self.select_folder_btn.place(x=self.folderText.winfo_width()+2, y=48)
        self.oAnalysis.place(x=self.label3.winfo_width() + 5, y=23)
        
        self.descriptionLabel.place(x=self.label3.winfo_width()+self.oAnalysis.winfo_width()+5, y=23)
        self.descriptionText.place(x=self.descriptionLabel.winfo_width()+self.label3.winfo_width()+self.oAnalysis.winfo_width()+5, y=23)
        self.inputText.place(x=self.label4.winfo_width() + 5, y=78)
        self.analysis_btn.place(x=self.oAnalysis.winfo_width() + self.oAnalysis.winfo_x() + 5, y=185)
        self.open_result_btn.place(x=self.analysis_btn.winfo_width() + self.analysis_btn.winfo_x() + 5, y=185)
        self.save_result_btn.place(x=self.open_result_btn.winfo_width() + self.open_result_btn.winfo_x() + 5, y=185)
        
        w = widthMain*996/1000
        h = heightMain*600/800
        #print(f"{widthMain}, {widthMain*996}, {widthMain*996/1000}, new result size{w}x{h}")
        self.resultSummary.config(width=800, height=600)


if __name__ == "__main__":
    root = tk.Tk()

    mainui = AutoTroubleMainUI(root)
    mainui.pack(fill="both", expand=True)
    s= root.geometry('1000x800+200+200')
    root.mainloop()