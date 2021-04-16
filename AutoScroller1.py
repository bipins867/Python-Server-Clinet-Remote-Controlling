Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import dbquery as db
>>> mydb=db.genMdb()
>>> cursor=mydb.cursor()
>>> cb=db.cb1(cursor,'xprtnot')
>>> d=cb.selectAllData('c_bipin_userName')
>>> d
[]
>>> import DataShare as ds
>>> f=ds.prepSend(d)
>>> f
['gAAAAABe7DDf-MQOAr5g4dPbbk17qbFkKgQ0yUBt_fS8-GupOviLcL5it9AjeCbGZo_i31k7-UavdNCcyZizc535Jjd4BX0bRg==', 'float64', '(0,)']
>>> k=ds.remodifyData(f[0],f[1],[f2])
Traceback (most recent call last):
  File "<pyshell#9>", line 1, in <module>
    k=ds.remodifyData(f[0],f[1],[f2])
NameError: name 'f2' is not defined
>>> k=ds.remodifyData(f[0],f[1],f[2])
>>> k
array([], dtype=float64)
>>> k
array([], dtype=float64)
>>> ds.prepSend(None)
['gAAAAABe7DE6C5n81VUDroF9MLEPan3od2qfLdmMWK6fKQUjYiSWHoB5AQQPKr8JraZ_-SUdDW3jXJzVnJ55cnYbQioDan9B5g==', 'float64', '(0,)']
>>> import tkinter as tk
>>> r=tk.Tk()
>>> frame=tk.Frame()
>>> r.winfo_children
<bound method Misc.winfo_children of <tkinter.Tk object .>>
>>> r.winfo_children()
[<tkinter.Frame object .!frame>]
>>> frame.winfo_children()
[]
>>> import numpy as np
>>> a=np.array([])
>>> a
array([], dtype=float64)
>>> a ==[]
array([], dtype=bool)
>>> for i in a:
	print("HI")

	
>>> len(a)
0
>>> 
=========================== RESTART: C:\Python\gx1.py ==========================
GuiXprt1
It is error
client is connected
HI
I AM HANDLER
I AM OK
Error
0.2621774673461914I AM USERNAMW

I AM HANDLER
I AM OK
Error
0.06065011024475098

Warning (from warnings module):
  File "C:\Python\GuiXprt1.py", line 641
    if (d != [])and(d is not None) :
FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison

================================ RESTART: Shell ================================
>>> 
=========================== RESTART: C:\Python\gx1.py ==========================
GuiXprt1
It is error
client is connected
HI
I AM HANDLER
I AM OK
Error
0.24207520484924316I AM USERNAMW

I AM HANDLER
I AM OK
Error
0.020214080810546875

Warning (from warnings module):
  File "C:\Python\GuiXprt1.py", line 641
    if (d != [])and(d is not None) :
FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
I AM HANDLER
I AM OK
Error
0.10140800476074219
Warning (from warnings module):
  File "C:\Python\GuiXprt1.py", line 2603
    if d==[]:
FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison

I AM OK
Data
0.29450535774230957
I AM OK
Data
0.6468572616577148

=========================== RESTART: C:\Python\gx1.py ==========================
GuiXprt1
It is error
client is connected
HI

================================ RESTART: Shell ================================
>>> import tkinter as tk
>>> import Gui_Creation as gc
>>> r=tk.Tk()
>>> frame=tk.Frame(r,width=200,height=50)
>>> list1=gc.scrollableFrame(frame,400,300)
>>> frame.place(x=10,y=10)
>>> l1=tk.Label(list1,text='kkr')
>>> l1.pack()
>>> for i in range(20):
	l1=tk.Label(list1,text='kkr')
	l1.pack()

	
>>> 
================================ RESTART: Shell ================================
>>> import tkinter as tk
>>> import Gui_Creation as gc
>>> r=tk.Tk()
>>> r2=tk.Toplevel
>>> r2=tk.Toplevel()
>>> frame=tk.Frame(r2,width=200,height=50)
>>> list1=gc.scrollableFrame(frame,400,300)
>>> frame.place(x=10,y=10)
>>> for i in range(20):
	l1=tk.Label(list1,text='kkr')
	l1.pack()

	
>>> 
=========================== RESTART: C:\Python\gx1.py ==========================



=========================== RESTART: C:\Python\gx1.py ==========================









=========================== RESTART: C:\Python\gx1.py ==========================





================================ RESTART: Shell ================================
>>> import tkinter as tk
>>> import Gui_Creation as gc
>>> r=tk.Tk()
>>> frame=tk.Frame(r,width=200,height=50)
>>> list1=gc.scrollableFrame(frame,400,300)
>>> frame.place(x=10,y=10)
>>> for i in range(20):
	fram2=tk.Frame(list1,bg='green',width=300,height=50)
	l1=tk.Label(fram2,text='kkr')
	l1.pack()
	fram2.pack()

	
>>> 
================================ RESTART: Shell ================================
>>> import tkinter as tk
>>> import Gui_Creation as gc
>>> r=tk.Tk()
>>> frame=tk.Frame(r,width=300,height=600)
>>> list1=gc.scrollableFrame(frame,600,300)
>>> frame.place(x=10,y=10)
>>> for i in range(20):
	fram2=tk.Frame(list1,bg='green',width=300,height=50)
	l1=tk.Label(fram2,text='kkr')
	l1.place(x=20,y=20)
	fram2.pack()

	
>>> for i in range(20):
	fram2=tk.Frame(list1,bg='green',width=300,height=50)
	l1=tk.Label(fram2,text='kkr'+str(i))
	l1.place(x=20,y=20)
	fram2.pack()

	
>>> for i in range(20,100):
	fram2=tk.Frame(list1,bg='green',width=300,height=50)
	l1=tk.Label(fram2,text='kkr'+str(i))
	l1.place(x=20,y=20)
	fram2.pack()

	
>>> for i in range(100,500):
	fram2=tk.Frame(list1,bg='green',width=300,height=50)
	l1=tk.Label(fram2,text='kkr sldfjklsd fls dkjfs lkjsdlkfklsdf sdkflsdkjflksdjflkjsdlfjsdlfjdksfj sdjfksdlfsd'+str(i))
	l1.place(x=20,y=20)
	fram2.pack()

	
>>> 
>>> def fun():
	for i in range(100,500):
		fram2=tk.Frame(list1,bg='green',width=300,height=50)
		l1=tk.Label(fram2,text='kkrksfj sdjfksdlfsd'+str(i))
		l1.place(x=20,y=20)
		fram2.pack()

		
>>> 
>>> import threading
>>> threading.Thread(target=fun).start()
>>> 

>>> r.mainloop()
>>> import tkinter as tk
>>> import Gui_Creation as gc
>>> r=tk.Tk()
>>> frame=tk.Frame(r,width=300,height=600)
>>> frame=tk.Frame(r,width=300,height=300)
>>> list1=gc.scrollableFrame(frame,600,300)
>>> frame.place(x=10,y=10)
>>> for i in range(20,100):
	fram2=tk.Frame(list1,bg='green',width=300,height=50)
	l1=tk.Label(fram2,text='kkr'+str(i))
	l1.place(x=20,y=20)
	fram2.pack()

	
>>> 
================================ RESTART: Shell ================================
>>> import tkinter as tk
>>> import Gui_Creation as gc

>>> 
>>> r=tk.Tk()
>>> frame=tk.Frame(r,width=300,height=300)
>>> list1=gc.scrollableFrame(frame,600,300)
>>> frame.place(x=10,y=10)
>>> for i in range(20,100):
	fram2=tk.Frame(list1,bg='green',width=300,height=50)
	l1=tk.Label(fram2,text='kkr'+str(i))
	l1.place(x=20,y=20)
	fram2.pack()

	
>>> 
>>> list1.get()
Traceback (most recent call last):
  File "<pyshell#101>", line 1, in <module>
    list1.get()
AttributeError: 'Frame' object has no attribute 'get'
>>> 
================================ RESTART: Shell ================================
>>> import tkinter as tk
>>> r=tk.Tk()
>>> scrollbar=tk.Scrollbar(r)
>>> scrollbar.pack(side=tk.RIGHT,fill='y')
>>> mylist=tk.Listbox(root,yscrollcommand=scrollbar.set)
Traceback (most recent call last):
  File "<pyshell#106>", line 1, in <module>
    mylist=tk.Listbox(root,yscrollcommand=scrollbar.set)
NameError: name 'root' is not defined
>>> mylist=tk.Listbox(r,yscrollcommand=scrollbar.set)
>>> for i in range(100):
	mylist.insert(tk.END,' This is line number '+str(i))

	
>>> mylist.pack( side = tk.LEFT, fill = tk.BOTH )
>>> scrollbar.config(command=mylist.yview)
>>> scrollbar.get()
(0.0, 0.1)
>>> scrollbar.get()
(0.64, 0.74)
>>> scrollbar.set(0.0,0.1)
>>> for i in range(100,200):
	mylist.insert(tk.END,' This is line number '+str(i))

	
>>> mylist.see('end')
>>> 
================================ RESTART: Shell ================================
>>> import Gui_Creation as gc
>>> import tkinter as tk
>>> r=tk.Tk()
>>> frame=tk.Frame(r,width=300,height=300)
>>> list1=gc.scrollableFrame(frame,600,300)
>>> frame.place(x=10,y=10)
>>> for i in range(20,100):
	fram2=tk.Frame(list1,bg='green',width=300,height=50)
	l1=tk.Label(fram2,text='kkr'+str(i))
	l1.place(x=20,y=20)
	fram2.pack()

	
>>> 
====================== RESTART: C:\Python\Gui_Creation.py ======================
>>> import Gui_Creation as gc
>>> import tkinter as tk
>>> r=tk.Tk()
>>> frame=tk.Frame(r,width=300,height=300)
>>> list1,can=gc.scrollableFrame(frame,600,300)
>>> frame.place(x=10,y=10)
>>> for i in range(20,100):
	fram2=tk.Frame(list1,bg='green',width=300,height=50)
	l1=tk.Label(fram2,text='kkr'+str(i))
	l1.place(x=20,y=20)
	fram2.pack()

	
>>> can.grab_current()
>>> can.yview_moveto(0)
>>> can.yview_moveto(0.9)
>>> can.yview_moveto(1)
>>> can.yview_moveto(0)
>>> can.yview_moveto(1)
>>> 