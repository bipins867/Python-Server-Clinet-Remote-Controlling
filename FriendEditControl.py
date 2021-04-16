import tkinter as tk


class FriendEditControl:


    def __init__(self,root,c,userName,stf='GL'):
        #GL
        #GO
        self.c=c
        self.userName=userName
        self.stf=stf
        btnWidth=5
        entryWidth=25
        labelWidth=21
        self.root=root
        root.title('Overall Control')

        frame=tk.Frame(root,height=400,width=500)

        #Title
        titleFrame=tk.Frame(frame,bg='#006266',height=50,width=500)

        labelTitle=tk.Label(titleFrame,text='Overall Control',font="Helvetica 20 bold ",bg='yellow',fg='red')
        labelTitle.place(x=30,y=5)

        btnRefress=tk.Button(titleFrame,text='Refress',width=btnWidth,command=self.refress)
        btnRefress.place(x=360,y=5)


        btnHelp=tk.Button(titleFrame,text='Help')
        btnHelp.place(x=450,y=5)

        btnUpdate=tk.Button(titleFrame,text='Update',command=self.update)
        btnUpdate.place(x=280,y=5)


        downFrame=tk.Frame(frame,bg='grey',height=350,width=500)


        leftFrame=tk.Frame(downFrame,bg='#58B19F',height=350,width=350)

        labelLeftTitle=tk.Label(leftFrame,text='Sending Control',font="Helvetica 10 bold ",bg='yellow',fg='red')
        labelLeftTitle.place(x=30,y=5)

        btnForward=tk.Button(leftFrame,text='Forward',width=btnWidth,command=self.forward)
        btnForward.place(x=150,y=5)

        labelFile=tk.Label(leftFrame,text='File',width=labelWidth)
        labelText=tk.Label(leftFrame,text='Text',width=labelWidth)
        labelScreenCap=tk.Label(leftFrame,text='Screen Capture',width=labelWidth)
        labelCameraCap=tk.Label(leftFrame,text='Camera Capture',width=labelWidth)
        labelVoice=tk.Label(leftFrame,text='Voice',width=labelWidth)
        labelMouse=tk.Label(leftFrame,text='Mouse',width=labelWidth)
        labelKeyboard=tk.Label(leftFrame,text='Keyboard',width=labelWidth)

        self.varFilel=tk.IntVar()
        self.varTextl=tk.IntVar()
        self.varScreenCapl=tk.IntVar()
        self.varCameraCapl=tk.IntVar()
        self.varVoicel=tk.IntVar()
        self.varMousel=tk.IntVar()
        self.varKeyboardl=tk.IntVar()

        self.varFiler=tk.IntVar()
        self.varTextr=tk.IntVar()
        self.varScreenCapr=tk.IntVar()
        self.varCameraCapr=tk.IntVar()
        self.varVoicer=tk.IntVar()
        self.varMouser=tk.IntVar()
        self.varKeyboardr=tk.IntVar()



        labelFile.place(x=30,y=40)
        labelText.place(x=30,y=80)
        labelScreenCap.place(x=30,y=120)
        labelCameraCap.place(x=30,y=160)
        labelVoice.place(x=30,y=200)
        labelMouse.place(x=30,y=240)
        labelKeyboard.place(x=30,y=280)




        laradFile=tk.Radiobutton(leftFrame,text='on',variable=self.varFilel,value=1)
        laradText=tk.Radiobutton(leftFrame,text='on',variable=self.varTextl,value=1)
        laradScreenCap=tk.Radiobutton(leftFrame,text='on',variable=self.varScreenCapl,value=1)
        laradCameraCap=tk.Radiobutton(leftFrame,text='on',variable=self.varCameraCapl,value=1)
        laradVoice=tk.Radiobutton(leftFrame,text='on',variable=self.varVoicel,value=1)
        laradMouse=tk.Radiobutton(leftFrame,text='on',variable=self.varMousel,value=1)
        laradKeyboard=tk.Radiobutton(leftFrame,text='on',variable=self.varKeyboardl,value=1)

        lbradFile=tk.Radiobutton(leftFrame,text='off',variable=self.varFilel,value=0)
        lbradText=tk.Radiobutton(leftFrame,text='off',variable=self.varTextl,value=0)
        lbradScreenCap=tk.Radiobutton(leftFrame,text='off',variable=self.varScreenCapl,value=0)
        lbradCameraCap=tk.Radiobutton(leftFrame,text='off',variable=self.varCameraCapl,value=0)
        lbradVoice=tk.Radiobutton(leftFrame,text='off',variable=self.varVoicel,value=0)
        lbradMouse=tk.Radiobutton(leftFrame,text='off',variable=self.varMousel,value=0)
        lbradKeyboard=tk.Radiobutton(leftFrame,text='off',variable=self.varKeyboardl,value=0)


        laradFile.place(x=200,y=40)
        laradText.place(x=200,y=80)
        laradScreenCap.place(x=200,y=120)
        laradCameraCap.place(x=200,y=160)
        laradVoice.place(x=200,y=200)
        laradMouse.place(x=200,y=240)
        laradKeyboard.place(x=200,y=280)

        lbradFile.place(x=280,y=40)
        lbradText.place(x=280,y=80)
        lbradScreenCap.place(x=280,y=120)
        lbradCameraCap.place(x=280,y=160)
        lbradVoice.place(x=280,y=200)
        lbradMouse.place(x=280,y=240)
        lbradKeyboard.place(x=280,y=280)



        rightFrame=tk.Frame(downFrame,bg='#9AECDB',height=350,width=150)

        raradFile=tk.Radiobutton(rightFrame,text='on',variable=self.varFiler,value=1)
        raradText=tk.Radiobutton(rightFrame,text='on',variable=self.varTextr,value=1)
        raradScreenCap=tk.Radiobutton(rightFrame,text='on',variable=self.varScreenCapr,value=1)
        raradCameraCap=tk.Radiobutton(rightFrame,text='on',variable=self.varCameraCapr,value=1)
        raradVoice=tk.Radiobutton(rightFrame,text='on',variable=self.varVoicer,value=1)
        raradMouse=tk.Radiobutton(rightFrame,text='on',variable=self.varMouser,value=1)
        raradKeyboard=tk.Radiobutton(rightFrame,text='on',variable=self.varKeyboardr,value=1)

        rbradFile=tk.Radiobutton(rightFrame,text='off',variable=self.varFiler,value=0)
        rbradText=tk.Radiobutton(rightFrame,text='off',variable=self.varTextr,value=0)
        rbradScreenCap=tk.Radiobutton(rightFrame,text='off',variable=self.varScreenCapr,value=0)
        rbradCameraCap=tk.Radiobutton(rightFrame,text='off',variable=self.varCameraCapr,value=0)
        rbradVoice=tk.Radiobutton(rightFrame,text='off',variable=self.varVoicer,value=0)
        rbradMouse=tk.Radiobutton(rightFrame,text='off',variable=self.varMouser,value=0)
        rbradKeyboard=tk.Radiobutton(rightFrame,text='off',variable=self.varKeyboardr,value=0)


        raradFile.place(x=20,y=40)
        raradText.place(x=20,y=80)
        raradScreenCap.place(x=20,y=120)
        raradCameraCap.place(x=20,y=160)
        raradVoice.place(x=20,y=200)
        raradMouse.place(x=20,y=240)
        raradKeyboard.place(x=20,y=280)

        rbradFile.place(x=90,y=40)
        rbradText.place(x=90,y=80)
        rbradScreenCap.place(x=90,y=120)
        rbradCameraCap.place(x=90,y=160)
        rbradVoice.place(x=90,y=200)
        rbradMouse.place(x=90,y=240)
        rbradKeyboard.place(x=90,y=280)







        labelRightTitle=tk.Label(rightFrame,text='Reciving Control',font="Helvetica 10 bold ",bg='yellow',fg='red')
        labelRightTitle.place(x=30,y=5)



        self.labelStatus=tk.Label(leftFrame,text='Status')
        self.labelStatus.place(x=30,y=320)

        rightFrame.place(x=350,y=0)
        leftFrame.place(x=0,y=0)
        downFrame.place(x=0,y=50)
        titleFrame.place(x=0,y=0)
        frame.place(x=0,y=0)

    def update(self):
        pass

    def refress(self):
        pass

    def forward(self):
        pass
main=__name__
print(main)
if '__main__'==main:
    c='c'
    #print("HI")
    root=tk.Tk()
    root.geometry('500x400')
    OverallControl(root,c,'userName')
    root.mainloop()



