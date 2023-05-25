from tkinter import Tk, Label, Button, Toplevel, Y, BOTTOM, END
from tkinter.scrolledtext import ScrolledText

class ResultDlg(Toplevel):
    def __init__(self, parent, result) -> None:
        Toplevel.__init__(self, parent)
        self.title("Result")
        self.resultText = ScrolledText(self, width=200, height=30)#, xscrollcommand = self.scrollbar_x.set,yscrollcommand = self.scrollbar_y.set )#, font=("Helvetica", 14))
        self.resultText.pack(fill=Y, side=BOTTOM, expand=True)
        self.resultText.focus_set()

        self.resultText.delete(1.0, END)  
        self.resultText.insert(END, result)

        self.grab_set()
        self.focus_set()
        self.wait_window()

def show_custom_dialog(parent, result):
    # Create a new window
    dlg = ResultDlg(parent, result)

 
if __name__ == "__main__":
    window = Tk()
    window.title("Main Window")

    show_custom_dialog(window, '123')
