import TrialVersionClient1 as tvc
import tkinter as tk
import threading


root=tk.Tk()

label=tk.Label(root,text='hello',width=5)
label.place(x=0,y=0)

root.geometry('500x400')
label.config(text='king')

#threading.Thread(target=root.mainloop).start()

c=tvc.Client()

def fun():
    while True:
        msg=c.curMessage
        label.config(text=msg)

#threading.Thread(target=fun).start()
c.login('Bipin','Bipin')
fun()
#root.mainloop()
