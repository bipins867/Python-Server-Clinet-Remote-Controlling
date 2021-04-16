import GuiXprt2 as gx2
import TrialVersionClient2 as tvc
import tkinter as tk


c=tvc.Client()

print("HI")
root=tk.Tk()
root.geometry('500x400')
gx2.Global(root,c)
root.mainloop()
