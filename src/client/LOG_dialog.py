from client_http import get_log
from Tkinter import *
from datetime import timedelta

class log_dialog:
    def __init__(self, root,username,conn):
        self.top = Toplevel(root)



        #self.path_label=Label(self.top ,text="LOG", font='Arial 15').pack()


        self.listbox=Listbox(self.top,  width = 30,height=10, font='Arial 12',yscrollcommand=True)
        log=get_log(conn)
        for log_line in log:
            self.listbox.insert(0, log_line[1]+"   time="+timedelta(log_line[0]))
        #self.listbox.bind('<<ListboxSelect>>', on_select)
        self.listbox.pack()




def on_select(event):
    pass


