from Tkinter import *
from functools import partial
import time
import tkMessageBox as mb
import tkFileDialog as fd
import tkSimpleDialog as sd

name="moshe"

root = Tk()
root.resizable(width=FALSE, height=FALSE)

root.geometry('450x350')
root.title("drop_box")

#=============================================================================

buttons_frame=Frame(root)
b_font='Arial 12'
def back():pass
back_b=Button(buttons_frame, text = "back",command=back, font=b_font)
back_b.pack(side = LEFT, expand = 1)

def delete():pass
delete_b=Button(buttons_frame, text = "delete",command=delete, font=b_font)
delete_b.pack(side = LEFT, expand = 1)

def uploud():pass
uploud_b=Button(buttons_frame, text = "uploud",command=uploud, font=b_font)
uploud_b.pack(side = LEFT, expand = 1)

def downloud():pass
downloud_b=Button(buttons_frame, text = "downloud",command=downloud, font=b_font)
downloud_b.pack(side = LEFT, expand = 1)

def open_dir():pass
open_b=Button(buttons_frame, text = "open",command=open_dir, font=b_font)
open_b.pack(side = LEFT, expand = 1)

def rename():pass
rename_b=Button(buttons_frame, text = "rename",command=rename, font=b_font)
rename_b.pack(side = LEFT, expand = 1)

def replace():pass
replace_b=Button(buttons_frame, text = "replace",command=replace, font=b_font)
replace_b.pack(side = LEFT, expand = 1)

buttons_frame.pack(side=BOTTOM)


#=============================================================================



frame=Frame(root)

lb2 = Label(frame ,text="   hello   \n"+name,bg="#b0b0e0", font='Arial 15').grid(row=0,column=0)
def log_in():pass
log_in_b=Button(frame, text = "log_in",command=log_in ,  width = 10, font='Arial 12') .grid(row=1,column=0)#.pack(side = TOP, fill = X,anchor='ne')

def log_out():pass
log_out_b=Button(frame, text = "log_out",command=log_out ,  width = 10, font='Arial 12').grid(row=2,column=0)#.pack(side = TOP, fill = X)

def sgin_up():pass
log_out_b=Button(frame, text = "sign_up",command=sgin_up,  width = 10, font='Arial 12' ).grid(row=3,column=0)#.pack(side = TOP, fill = X)


frame.pack(side=LEFT,fill=Y)



lb1 = Label(root ,text="drop box",bg="#9090d0", font='Arial 22',)#title
lb1.pack(side='top', expand = 1)







listbox=Listbox(root,  width = 20,height=10, font='Arial 15')
def on_select(event):
    index= listbox.curselection()[0]
    #try:listbox.delete(index,index)
    #except:pass
    #print(listbox.get(index))

    root.title(index)
listbox.bind('<<ListboxSelect>>', on_select)

listbox.pack(side="top", expand = 1)


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