from tkinter import *
from tkinter import colorchooser, ttk

import numpy as np

from scipy import signal
from scipy.spatial.distance import cdist


import matplotlib.pyplot as plt

import torch
import torch.nn as nn

import changetable as ct

def sin(num):
    return np.sin(num*np.pi/180)

def cos(num):
    return np.cos(num*np.pi/180)

def roundnumber(num,digit):
    tmp = round(num,digit)
    return tmp

def positive(num):
    if num<0:
        num = num*(-1)
    return num

def applytotalone(num,max):
    if max==0:
        return 0
    return round(num/max, 4)

applyone = np.vectorize(applytotalone)
applyn1 = np.vectorize(positive)

def sumofarray(arr):
    sumarr=sum(arr)
    sumarr=applyone(arr,sumarr)
    return sumarr

def maxofarray(arr):
    maxarr=max(arr)
    maxarr=applyone(arr,maxarr)
    return maxarr

def posarray(arr):
    posarr=applyn1(arr)
    return posarr

applyround=np.vectorize(roundnumber)

def toone(arr):
    tmp=[]
    toonearr=np.array(arr,dtype=float)

    for i in range(10):
        ls=ct.number2bin(i)
        ls=ct.bintolist(ls)
        ls=np.array(ls,dtype=float)
        subtracted_array = np.subtract(toonearr, ls)
        
        alltomin=applyn1(subtracted_array.tolist())
        tmp.append(sum(alltomin))

    minnum=min(tmp)
    ansarr=ct.bintolist(ct.number2bin(tmp.index(minnum)))
    ans=[]
    for i in range(len(ansarr)):
        ans.append(round((1-abs(ansarr[i]-arr[i]))*100,2))
    confidance=ans

    return tmp.index(minnum),confidance

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = torch.nn.Linear(56, 24)
        self.fc2 = torch.nn.Linear(24, 12)
        self.fc3 = torch.nn.Linear(12,6)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x


class main:
    def __init__(self, master):
        self.master = master
        self.color_fg = 'Black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.pen_width = 3
        self.drawWidgets()
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

        self.buttonswitch=1
        self.xarr=[]
        self.yarr=[]
        self.gradarr=[]

        self.count_tick=0
        self.old_v5_x = None
        self.old_v5_y = None

        self.init_x = None
        self.init_y = None
        self.graphsw = 0


    def paint(self, e):

        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, e.x, e.y, width = self.pen_width, fill = self.color_fg, capstyle='round', smooth = True)
            self.count_tick += 1

        if self.count_tick > 6 :
            if self.old_v5_x and self.old_v5_y:    
                distance = np.hypot(e.x-self.old_v5_x, e.y -self.old_v5_y)  

                deltaY=e.y-self.old_v5_y
                deltaX=e.x-self.old_v5_x          
                gradient1= np.arctan2(deltaY, deltaX)* 180/ np.pi
                gradient1=gradient1+90
                if gradient1<0:
                    gradient1=360-gradient1*(-1)
                
                self.gradarr.append(int(gradient1))
                #print(distance)

            self.count_tick = 0
            self.old_v5_x = e.x
            self.old_v5_y = e.y

            if self.buttonswitch == 1:
                self.xarr.append(e.x)
                self.yarr.append(e.y)
        self.old_x = e.x
        self.old_y = e.y
        #print(e.x,e.y,self.buttonswitch)

    def angle(self,oldsymbol): 


        xinit=self.xarr[0]
        yinit=self.yarr[0]
        xcor=self.xarr[1:]
        ycor=self.yarr[1:]
    
        #distance of point
        x = np.array([[xinit,yinit]])
        X_Y = [[xcor[i], ycor[i]] for i in range(len(xcor))]
        y = np.array(X_Y)
        d = cdist(x,y)
        disforminit=np.hstack([d[0][1],signal.resample(d[0][0:-1],14),d[0][-1]]).tolist()
        disforminit=posarray(disforminit)
        disforminit=maxofarray(disforminit)

        #print(disforminit)

        anglecount=[0,0,0,0,0,0,0,0]
        anglecount[0] = sum(map(lambda item: item >=338 or item<23,oldsymbol))
        anglecount[1] = sum(map(lambda item: item >=23 and item<68, oldsymbol))
        anglecount[2] = sum(map(lambda item: item >=68 and item<113, oldsymbol))
        anglecount[3] = sum(map(lambda item: item >=113 and item<158, oldsymbol))
        anglecount[4] = sum(map(lambda item: item >=158 and item<203, oldsymbol))
        anglecount[5] = sum(map(lambda item: item >=203 and item<248, oldsymbol))
        anglecount[6] = sum(map(lambda item: item >=248 and item<293, oldsymbol))
        anglecount[7] = sum(map(lambda item: item >=293 and item<338, oldsymbol))

        anglecount=sumofarray(anglecount)
        #angle
        applysin = np.vectorize(sin)
        sinarr=applysin(oldsymbol)
        newsin=signal.resample(sinarr,16)
        newsin=applyround(newsin,6)

        applycos =np.vectorize(cos)
        cosarr=applycos(oldsymbol)
        newcos=signal.resample(cosarr,16)
        newcos=applyround(newcos,6)

        angle=np.array([newsin],dtype=float)
        angle=np.append(angle,newcos)


        angle=np.append(angle,anglecount)
        angle=np.append(angle,disforminit)

        return  angle
    
    def reset(self, e):
        self.old_x = None
        self.old_y = None
        self.old_v5_x = None
        self.old_v5_y = None
        self.init_x = None
        self.init_y = None
    
    def changedW(self, width):
        self.pen_width = width
    
    def clearcanvas(self):
        self.c.delete(ALL)
    
    def change_fg(self):
        self.color_fg = colorchooser.askcolor(color=self.color_fg)[1]
    
    def change_bg(self):
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg

    #new
    def startend(self,tmp):

        if self.buttonswitch > 0:
            self.button1.configure(text="Start")
            self.state.configure(text="Press to \n Start Recording")
            #print(self.xarr)
            #print(self.yarr)
            #print(self.gradarr)


            if self.xarr and self.yarr:
                tmp=self.angle(self.gradarr)
                print(tmp)

                if(self.graphsw==1): #debuging
                    showdata=tmp.tolist()
                    X = np.linspace(0,56, 56, endpoint=False)
                    print(showdata)
                    plt.figure(figsize=(10, 6))
                    plt.plot(X,showdata,'go-')
                    plt.xticks(np.arange(0, 57, 4))
                    
                    plt.grid()
                    plt.show()

                model = Net()
                model.load_state_dict(torch.load('savemodel.txt'))
                b=model(torch.from_numpy(tmp).float())
                c=[b[0].item(),b[1].item(),b[2].item(),b[3].item(),b[4].item(),b[5].item()]
                #print(c)
                
                resultout,resultcon=toone(c)
                #print(resultout,resultcon,"%")
                self.num.configure(text=resultout)

            self.xarr=[]
            self.yarr=[]
            self.gradarr=[]

            print("in start")


        if self.buttonswitch < 0:
            self.button1.configure(text="OK")
            self.state.configure(text="Writting \n Recording")
            print("in ok")
        
        self.buttonswitch = self.buttonswitch*(-1) 
        print(tmp)

    def clear(self):
        if self.buttonswitch > 0:
            self.clearcanvas()
            print("in clear")

    def ploting(self):
        if self.graphsw == 0:
            self.graphsw = 1

        if self.graphsw < 0:
            self.graph.configure(text="Now Showing")
            print("graph")

        if self.graphsw > 0:
            self.graph.configure(text="Not showing")
            print("nograph")       
        self.graphsw = self.graphsw*(-1) 


    def drawWidgets(self):
        self.controls = Frame(self.master, padx=5, pady=5)
        textpw = Label(self.controls, text='Pen Width', font='Georgia 16')
        textpw.grid(row=0, column=0)
        self.slider = ttk.Scale(self.controls, from_=3, to=100, command=self.changedW, orient='vertical')
        self.slider.set(self.pen_width)
        self.slider.grid(row=0, column=1)
        self.controls.pack(side="left")
        self.c = Canvas(self.master, width=500, height=400, bg=self.color_bg)
        self.c.pack(fill=BOTH, expand=True)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Menu', menu=optionmenu)
        optionmenu.add_command(label='Brush Color', command=self.change_fg)
        optionmenu.add_command(label='Background Color', command=self.change_bg)
        optionmenu.add_command(label='Clear Canvas', command=self.clearcanvas)
        optionmenu.add_command(label='Exit', command=self.master.destroy)

        self.button1 = ttk.Button(self.controls,command=lambda a = "Button Click" :[self.startend(a),self.clear()], text="Enter")
        self.button1.grid(row=1000, column=0)

        self.state = Label(self.controls, text='Not Writting', font='Georgia 16')
        self.state.grid(row=500, column=0)
        self.num = Label(self.controls, text='Predict number', font='Georgia 24')
        self.num.grid(row=1500, column=0)
        self.graph = ttk.Button(self.controls,command=self.ploting, text="Show Graph")
        self.graph.grid(row=2000, column=0)




win = Tk()
win.title("Paint App")
main(win)
win.mainloop()