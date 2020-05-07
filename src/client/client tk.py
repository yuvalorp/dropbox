from Tkinter import *
from functools import partial
import time
import tkMessageBox as mb
import tkFileDialog as fd
import tkSimpleDialog as sd

name="moshe"

root = Tk()
root.geometry('350x350')
root.title("drop_box")

frame=Frame(root)
def log_in():pass
log_in_b=Button(root, text = "log_in",command=log_in ).grid(row=0,column=0)#.pack(side = TOP, fill = X,anchor='ne')

def log_out():pass
log_out_b=Button(root, text = "log_out",command=log_out ).grid(row=1,column=0)#.pack(side = TOP, fill = X)

def sgin_up():pass
log_out_b=Button(root, text = "sign_up",command=sgin_up ).grid(row=2,column=0)#.pack(side = TOP, fill = X)





lb1 = Label(root ,text="drop box",bg="#9090d0", font='Arial 22')#title
lb1.grid(row=0, column=1)

lb2 = Label(root ,text="hello "+name,bg="#9090d0", font='Arial 14')
lb2.grid(row=1, column=1)




listbox=Listbox(root)
def on_select(event):
    index= listbox.curselection()[0]
    #try:listbox.delete(index,index)
    #except:pass
    #print(listbox.get(index))

    root.title(index)
listbox.bind('<<ListboxSelect>>', on_select)

listbox.grid(row=3, column=1)


for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)
'''
txt=Entry(root, font='Arial 18', fg='blue')
txt.delete(0, END)
txt.insert(0, "a default value")
txt.grid(row=2, column=1)


def send():
    listbox.insert(0,"a") 
arg=0
#action_with_arg = partial(send, arg,lbl)#use to give arrgoments to the button
sendB=Button(root, text="send", command=send,bg="red")
sendB.grid(row=2, column=0)
'''


root.mainloop()

#answer = sd.askstring("Input", "What is your first name?",parent=root)
'''


mb.showinfo(title=None, message=None)


def callback():
    name= fd.askopenfilename()
    print(name)

errmsg = 'Error!'
tk.Button(text='File Open',
       command=callback).pack(fill=tk.X)
tk.mainloop()
'''