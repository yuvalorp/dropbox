# -*- coding: utf-8 -*-
from client_http import get_type,get_file_list,change_per
from Tkinter import *
from functools import partial
from move_dialog import *
class per_dialog:
    def __init__(self, root,username,conn,path,per_list):
        self.path=path[0]
        self.top = Toplevel(root)
        Label(self.top ,text="use 'delete' to remove permition\n or use 'add' to add permition", font='Arial 13').pack()
        self.listbox=Listbox(self.top,  width = 30,height=10, font='Arial 12')
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        for i in per_list:
            self.group_per_list.append(0,i)
        for i in group_per_list:
            self.group_per_list.append(0,"group"+i)

        self.listbox.pack()
        self.index=0
        self.group_per_list=group_per_list
        self.per_list=per_list


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
        if len(x)>6:
            if x[6:]=='group ' or x[6:]=='Group ' or x[6:]=='GROUP ':
                self.group_per_list.append(x[:6])
                return ()
            return ()
        self.per_list.append(x[:6])

    def ok(self):
        #q=change_per(self.path,self.per_list,self.group_per_list)
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