# -*- coding: utf-8 -*-
from client_http import get_type,get_file_list,change_per
from Tkinter import *
from functools import partial
from move_dialog import *
class per_dialog:
    def __init__(self, root,username,conn,path,per_list):
        self.username=username
        self.conn=conn


        self.path=path
        self.top = Toplevel(root)
        Label(self.top ,text="use 'delete' to remove permition\n or use 'add' to add permition", font='Arial 13').pack()
        self.listbox=Listbox(self.top,  width = 30,height=10, font='Arial 12')
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.per_list=per_list
        if type(per_list):
            for i in per_list:
                self.per_list.append(0,i)


        self.listbox.pack()
        self.index=0




        self.txt=Entry(self.top, font='Arial 14')


        self.buttons_frame=Frame(self.top)


        Button(self.buttons_frame, text = 'delete',command=self.delete, font='Arial 12').pack(side = LEFT, expand = 1)
        Button(self.buttons_frame, text = 'add',command=self.add, font='Arial 12').pack(side = LEFT, expand = 1)
        Button(self.buttons_frame, text = 'ok',command=self.ok, font='Arial 12').pack(side = LEFT, expand = 1)
        Button(self.buttons_frame, text = 'cancel',command=self.cancel, font='Arial 12').pack(side = LEFT, expand = 1)
        self.buttons_frame.pack()


    def delete(self):

        x=self.file_selected



        self.per_list.remove(x)
        self.listbox.delete(self.index,self.index)


    def add(self):
        x=self.txt.get()
        self.listbox.insert('end',x)

        self.per_list.append(x)

    def ok(self):

        q=change_per(self.username,self.path,self.per_list,self.conn)
        self.top.destroy()
    def cancel(self):self.top.destroy()
    def on_select(self,event):
        try:
            self.index= self.listfile.curselection()[0]
            self.file_selected=self.listfile.get(self.index).split(" ")
        except:pass




def main():
    """
    Add Documentation here
    """
    pass  # Replace Pass with Your Code


if __name__ == '__main__':
    main()