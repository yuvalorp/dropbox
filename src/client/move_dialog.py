from client_http import get_type,get_file_list
from Tkinter import *
from functools import partial



class move_dialog:
    def __init__(self, root,username,conn):
        self.top = Toplevel(root)

        self.path='/admin/'+username[0]
        self.username=username[0]
        self.path_string=StringVar(value="")
        self.path_label=Label(self.top ,textvariable=self.path_string, font='Arial 13').pack()
        self.file_selected=["","",""]
        self.conn=conn

        self.root = root



        self.listbox=Listbox(self.top,  width = 30,height=10, font='Arial 12')
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.pack()
        write_file_list(get_file_list(self.username,self.path,conn), self.listbox)



        self.buttons_frame=Frame(self.top)
        back=partial(self.back2,self.listbox,self.path_string,self.username,self.path)



        Button(self.buttons_frame, text = 'back',command=back, font='Arial 12').pack(side = LEFT, expand = 1)
        Button(self.buttons_frame, text = 'open',command=self.open_dir, font='Arial 12').pack(side = LEFT, expand = 1)
        Button(self.buttons_frame, text = 'ok',command=self.ok, font='Arial 12').pack(side = LEFT, expand = 1)
        self.buttons_frame.pack()




    def open_dir2(self):

        if self.file_selected!=["","",""]:
            self.path+='/'+self.file_selected[0]
            write_file_list(get_file_list(self.username,self.path,self.conn),self.listbox)
            self.path_string.set(self.path[6:])
    def open_dir(self):
        file_type=self.file_selected[2]

        if file_type=='file':
            self.open_dir2()

    def back2(self,filebox,path_string):

        if len(self.path.split("/"))>2 or (self.username=='admin' and len(self.path.split("/"))>1 ):
            path="/".join(self.path.split("/")[:-1])
            write_file_list(get_file_list(self.username,path,self.conn), filebox)
            path_string.set(path[6:])

    def on_select(self,event):

        try:
            index= self.listbox.curselection()[0]
            self.file_selected=self.listbox.get(index).split(" ")
        except:pass
    def ok(self):
        self.path+='/'+self.file_selected[0]
        self.top.destroy()

def write_file_list(file_list,filebox):
    """
    get list of files and return it into the listbox
    """
    if file_list==[]:
        filebox.delete(0,'end')

    if not file_list=="there was a conection eror"  :#and not file_list==[] :
        filebox.delete(0,'end')

        for i in file_list['file_list']:
            filebox.insert(END, to_listbox_format(i))

def to_listbox_format(a):
    #return(a["name"]+"   creator: "+a["creator"]+"  type: "+a['type'])
    return(a["name"].replace(" ","_")+" "+a["creator"].replace(" ","_")+" "+a['type'])
