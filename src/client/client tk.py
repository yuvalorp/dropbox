from Tkinter import *
from functools import partial

import tkMessageBox as mb
import tkFileDialog as fd
import tkSimpleDialog as sd
from client_http import *
import httplib
try:
    conn = httplib.HTTPConnection("localhost", port=5000)
except:
    print("there was a conection eror plese try again later")
    exit()

#globals
username=""
pasward=""
path=""
file_selected=""

root = Tk()
root.resizable(width=FALSE, height=FALSE)

root.geometry('500x350')
root.title("drop_box")


#==============================================================================

def write_file_list(file_list,filebox):
    if not file_list=="there was a conection eror"  and not file_list==[] :
        listbox.delete(0,'end')
        for i in file_list['file_list']:
            listbox.insert(END, to_listbox_format(i))


def to_listbox_format(a):
    #return(a["name"]+"   creator: "+a["creator"]+"  type: "+a['type'])
    return(a["name"]+" "+a["creator"]+" "+a['type'])

listbox=Listbox(root,  width = 30,height=10, font='Arial 12')
def on_select(event):
    global  file_selected
    try:
        index= listbox.curselection()[0]
        file_selected=listbox.get(index).split(" ")
    except:pass


    #root.title(index)
    pass
listbox.bind('<<ListboxSelect>>', on_select)


#=============================================================================
'''
class move_dialog:
    def __init__(self, root,filebox):

        self.root = root
        top = self.top = Toplevel(root)

        eror_string = StringVar(value="")
        self.listbox=Listbox(top,  width = 30,height=10, font='Arial 12')
        def on_select(event):
            global  file_selected
            try:
                index= listbox.curselection()[0]
                file_selected=listbox.get(index).split(" ")
            except:pass


        new_f=partial(self.ok,eror_string,filebox)
        b = Button(top, text="OK", command=new_f)
        b.pack(pady=5)
        self.path=["","",""]
        self.file_selected=""



    def ok(self,eror_string,filebox):
        global username
        global pasward
        global conn
        global path

        username2 = self.e1.get()
        pasward2 = self.e2.get()
        s=check_pasward(username2,pasward2,conn)

        if s=="there was a conection eror":
            eror_string.set("there was a conection eror")
        elif s==False:
            eror_string.set("the username or the pasward is incorect")
        else:
            username=username2+''
            pasward=pasward2+''
            path='/'+username
            write_file_list(get_file_list(username,path,conn), filebox)
            self.top.destroy()

class change_permition:
    def __init__(self, root,filebox):

        self.root = root
        top = self.top = Toplevel(root)

        eror_string = StringVar(value="")
        self.listbox=Listbox(top,  width = 30,height=10, font='Arial 12')

'''
path_string = StringVar(value="")
path_label=Label(root ,textvariable=path_string, font='Arial 13')

buttons_frame=Frame(root)
b_font='Arial 12'
def back2(filebox,path_string):
    global username
    global path
    if len(path.split("/")[-1])!=2 or (username=='admin' and len(path.split("/")[-1])!=1 ):
        path="/".join(path.split("/")[:-1])
        write_file_list(get_file_list(username,path,conn), filebox)
        path_string.set(path)
back=partial(back2,listbox,path_string)

def delete2(filebox):
    global path
    global file_selected
    global conn
    if file_selected!=["","",""]:
        if mb.askyesno('Verify', 'you sure that you want to delete '+file_selected[0]+"?"):
            q=delete_file(username,path+'/'+file_selected[0],conn)
            if q=="the file doesnt exists":mb.showerror("Error", "Error message")
            elif q=="the user isn't have permishion to do it":mb.showerror("Error", "you dont have pemittion to do it")
            elif q=="ok":
                write_file_list(get_file_list(username,path,conn), filebox)
delete=partial(delete2,listbox)
def uploud():pass

def open_dir2(filebox,path_string):
    global path
    global file_selected
    global conn
    #if file_selected[2]=='file':
    path+='/'+file_selected[0]
    write_file_list(get_file_list(username,path,conn), filebox)
    path_string.set(path)
open_dir=partial(open_dir2,listbox,path_string)

def rename2(root,filebox):
    global path
    global file_selected
    global conn
    if file_selected!="":
        name= sd.askstring("Input", "new name",parent=root)
        q=rename_file(username,str(path+'/'+file_selected[0]),name,conn)
        file_selected[0]=name
        if q=="the file doesnt exists":mb.showerror("Error", "Error message")
        elif q=="the user isn't have permishion to do it":mb.showerror("Error", "you dont have pemittion to do it")
        elif q=="ok":
            write_file_list(get_file_list(username,path,conn), filebox)
rename=partial(rename2,root,listbox)

def move():pass

open_b=Button(buttons_frame, text = "open",command=open_dir, font=b_font)
open_b.pack(side = LEFT, expand = 1)

def change_permition():pass
for f_name in ['back','delete','uploud','rename','move','change_permition']:
    Button(buttons_frame, text = f_name,command=eval(f_name), font=b_font).pack(side = LEFT, expand = 1)

buttons_frame.pack(side=BOTTOM)


#=============================================================================

class log_in_dialog:
    def __init__(self, root,filebox):

        self.root = root
        top = self.top = Toplevel(root)

        eror_string = StringVar(value="")
        Label(top, textvariable=eror_string).pack()
        Label(top, text="username").pack()

        self.e1 = Entry(top)
        self.e1.pack(padx=5)

        Label(top, text="pasward").pack()

        self.e2 = Entry(top)
        self.e2.pack(padx=5)

        new_f=partial(self.ok,eror_string,filebox)
        b = Button(top, text="OK", command=new_f)
        b.pack(pady=5)


    def ok(self,eror_string,filebox):
        global username
        global pasward
        global conn
        global path

        username2 = self.e1.get()
        pasward2 = self.e2.get()
        s=check_pasward(username2,pasward2,conn)

        if s=="there was a conection eror":
            eror_string.set("there was a conection eror")
        elif s==False:
            eror_string.set("the username or the pasward is incorect")
        else:
            username=username2+''
            pasward=pasward2+''
            path='/'+username
            write_file_list(get_file_list(username,path,conn), filebox)


            self.top.destroy()


class sign_up_dialog:

    def __init__(self, root):

        self.root = root
        top = self.top = Toplevel(root)

        eror_string = StringVar(value="")
        Label(top, textvariable=eror_string).pack()
        Label(top, text="username").pack()

        self.e1 = Entry(top)
        self.e1.pack(padx=5)

        Label(top, text="pasward").pack()

        self.e2 = Entry(top)
        self.e2.pack(padx=5)


        new_f=partial(self.ok,eror_string)
        b = Button(top, text="OK", command=new_f)
        b.pack(pady=5)


    def ok(self,eror_string):

        global conn

        username = self.e1.get()
        pasward = self.e2.get()
        s=create_user(username,pasward,conn)

        if s=="there was a conection eror":
            eror_string.set("there was a conection eror")
        elif s=='there is a user in this name':
            eror_string.set('there is a user in this name')
        else:
            self.top.destroy()



frame=Frame(root)
hello_text=StringVar(value="   hello   \n")
lb2 = Label(frame ,textvariable=hello_text,bg="#b0b0e0", font='Arial 15').grid(row=0,column=0)

def log_in(hello_text,lisbox,path_string):
    global path
    d = log_in_dialog(root,listbox)
    d.root.wait_window(d.top)
    hello_text.set("   hello   \n"+username)
    print(file_selected)
    if path!="":
        path_string.set(path)
log_in2=partial(log_in,hello_text,listbox,path_string)
log_in_b=Button(frame, text = "log in",command=log_in2 ,  width = 10, font='Arial 12') .grid(row=1,column=0)#.pack(side = TOP, fill = X,anchor='ne')

def log_out(hello_text,path_string):
    global username
    global pasward
    global path
    if username!='':
        if mb.askyesno('Verify', 'you sure that you want to log out?'):
            username=""
            pasward=""
            path=''
            hello_text.set("   hello   \n"+username)
            write_file_list([],listbox)
            path_string.set(path)
log_out2=partial(log_out,hello_text,path_string)
log_out_b=Button(frame, text = "log out",command=log_out2 ,  width = 10, font='Arial 12').grid(row=2,column=0)#.pack(side = TOP, fill = X)

def sign_up():
    d = sign_up_dialog(root)
    d.root.wait_window(d.top)

log_out_b=Button(frame, text = "sign up",command=sign_up,  width = 10, font='Arial 12' ).grid(row=3,column=0)#.pack(side = TOP, fill = X)


frame.pack(side=LEFT,fill=Y)



Label(root ,text="drop box",bg="#9090d0", font='Arial 22',).pack(side='top', expand=1)#title

path_label.pack(side='top', expand=1)



listbox.pack(side="top", expand=1)




root.mainloop()

