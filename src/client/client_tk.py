from Tkinter import *
from functools import partial

import tkMessageBox as mb
import tkFileDialog as fd
import tkSimpleDialog as sd
from client_http import *
import httplib
from move_dialog import *
from permition_dialog import *
from LOG_dialog import log_dialog
from  upload import post_multipart as uploud
host="localhost"
port=5000
try:
    conn = httplib.HTTPConnection(host, port=port)
except:
    print("there was a conection eror plese try again later")
    exit()

#globals

username=[""]
pasward=""
path="/root"
file_selected=["","",""]

root = Tk()
root.resizable(width=FALSE, height=FALSE)

root.geometry('650x350')
root.title("drop_box")


#==============================================================================



listbox=Listbox(root,  width = 30,height=10, font='Arial 12')
def on_select(event):
    global  file_selected

    try:
        index= listbox.curselection()[0]
        x=listbox.get(index).split(" ")
        file_selected[0]=x[0]
        file_selected[1]=x[1]
        file_selected[2]=x[2]

    except:pass


    #root.title(index)
    pass
listbox.bind('<<ListboxSelect>>', on_select)


#=============================================================================

path_string = StringVar(value="")
path_label=Label(root ,textvariable=path_string, font='Arial 13')

buttons_frame=Frame(root)
b_font='Arial 12'
def back2(filebox,path_string):
    global username
    global path

    if len(path.split("/"))>1 :
        path="/".join(path.split("/")[:-1])
        x=get_file_list(username[0],path,conn)

        if  type(x)!=str and type(x['file_list'])!=unicode :
            write_file_list(x, filebox)
            path_string.set(path[6:])
back=partial(back2,listbox,path_string)

def delete2(filebox):
    global path
    global file_selected
    global conn
    if file_selected!=["","",""]:
        if mb.askyesno('Verify', 'you sure that you want to delete '+file_selected[0]+"?"):
            q=delete_file(username[0],path+'/'+file_selected[0],conn)
            if q=="the file doesnt exists":mb.showerror("Error", "the file dont exist")
            elif q=="the user isn't have permishion to do it":mb.showerror("Error", "you dont have pemittion to do it")
            elif q=="ok":
                write_file_list(get_file_list(username[0],path,conn), filebox)
delete=partial(delete2,listbox)

def uploud_file2(root,host,port):
    global username
    global path
    root.filename = fd.askopenfilename(initialdir = "/",title = "Select file")
    uploud(host,port,username[0],path,root.filename)
uploud_file=partial(uploud_file2,root,host,port)

def create_directory():
    global username,path,conn
    name=sd.askstring("","what the name of the directory?")
    put_dir(username[0],path,name,conn)





def open_dir2(filebox ,path_string,conn):
    global path
    global file_selected
    #if file_selected[2]=='file':
    if file_selected!=["","",""]:
        path+='/'+file_selected[0]

        if file_selected[2]=='file':
            x=get_file_list(username[0],path,conn)
        else:
            x=get_file(username[0],path,conn)
        if  type(x)!=str and type(x['file_list'])!=unicode :
            write_file_list(x, filebox)
            path_string.set(path[6:])
open_dir=partial(open_dir2,listbox,path_string,conn)

#def open_dir():global file_selected;print(file_selected)

def rename2(root,filebox):
    global path
    global file_selected
    global conn
    if file_selected!=["","",""]:
        name= sd.askstring("Input", "new name",parent=root)
        q=rename_file(username[0],str(path+'/'+file_selected[0]),name,conn)
        file_selected[0]=name
        if q=="the file doesnt exists":mb.showerror("Error", "Error message")
        elif q=="the user isn't have permishion to do it":mb.showerror("Error", "you dont have pemittion to do it")
        elif q=="ok":
            write_file_list(get_file_list(username[0],path,conn), filebox)
rename=partial(rename2,root,listbox)


def move2(root,username,conn,filebox):
    global path
    global file_selected


    d = move_dialog(root,username,conn)
    try:d.root.wait_window(d.top)
    except:pass
    q=replace(username[0],path+'/'+file_selected[0],d.path,conn)
    if q=='ok':

        write_file_list(get_file_list(username,path,conn), filebox)
    else:
        mb.showerror('error','the file moving didnt secseed')
move=partial(move2,username,conn,listbox)




open_b=Button(buttons_frame, text = "open",command=open_dir, font=b_font)
open_b.pack(side = LEFT, expand = 1)


def change_permition():
    global username,conn, path
    per_list=get_per (path,conn)
    d = per_dialog(root,username,conn,path+'/'+file_selected[0],per_list)
    d.root.wait_window(d.top)



    #mb.showerror('error','the file change_permition didnt secseed')

for f_name in ['back','delete','uploud_file','create_directory','rename','move','change_permition']:
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

            username[0]=username2
            pasward=pasward2+''


            path='/root/'+username[0]
            #print(get_file_list(username,path,conn))
            write_file_list(get_file_list(username[0],path,conn), filebox)


            self.top.destroy()


class sign_up_dialog:

    def __init__(self, root):

        self.root = root
        top = self.top = Toplevel(root)
        self.groups=set()

        eror_string = StringVar(value="")
        Label(top, textvariable=eror_string).pack()
        Label(top, text="username").pack()

        self.e1 = Entry(top)
        self.e1.pack(padx=5)

        Label(top, text="pasward").pack()

        self.e2 = Entry(top)
        self.e2.pack(padx=5)

        Label(top, text="add groups").pack()

        self.e3 = Entry(top)
        self.e3.pack(padx=5)

        add_b = Button(top, text="add", command=self.add_f)
        add_b.pack(pady=5)


        new_f=partial(self.ok,eror_string)

        b = Button(top, text="OK", command=new_f)
        b.pack(pady=5)


    def add_f(self):
        self.groups.add(self.e3.get())

    def ok(self,eror_string):

        global conn

        username = self.e1.get()
        pasward = self.e2.get()
        s=create_user(username,pasward,self.groups,conn)

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
    hello_text.set("   hello   \n"+username[0])

    path_string.set(path)
log_in2=partial(log_in,hello_text,listbox,path_string)
log_in_b=Button(frame, text = "log in",command=log_in2 ,  width = 10, font='Arial 12') .grid(row=1,column=0)#.pack(side = TOP, fill = X,anchor='ne')



def log_out(hello_text,path_string):
    global username
    global pasward
    global path
    if username[0]!='':
        if mb.askyesno('Verify', 'you sure that you want to log out?'):
            username[0]=""
            pasward=""
            path='/root'
            hello_text.set("   hello   \n"+username[0])

            write_file_list([],listbox)
            path_string.set(path)
log_out2=partial(log_out,hello_text,path_string)
log_out_b=Button(frame, text = "log out",command=log_out2 ,  width = 10, font='Arial 12').grid(row=2,column=0)#.pack(side = TOP, fill = X)

def sign_up():
    d = sign_up_dialog(root)
    d.root.wait_window(d.top)

log_out_b=Button(frame, text = "sign up",command=sign_up,  width = 10, font='Arial 12' ).grid(row=3,column=0)#.pack(side = TOP, fill = X)

def show_log():
    global conn
    global username

    if username[0]=='admin':

        d = log_dialog(root,conn)
        d.root.wait_window(d.top)

LOG_b=Button(frame, text = "see LOG",command=show_log,  width = 10, font='Arial 12' )
LOG_b.grid(row=5,column=0)

frame.pack(side=LEFT,fill=Y)



Label(root ,text="drop box",bg="#9090d0", font='Arial 22',).pack(side='top', expand=1)#title

path_label.pack(side='top', expand=1)



listbox.pack(side="top", expand=1)


root.mainloop()

