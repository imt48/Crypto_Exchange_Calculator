
from os import name
import tkinter as tk
from tkinter.constants import CENTER, HORIZONTAL, VERTICAL
import tkinter.ttk as ttk
import tkinter.font as tkfont
from typing import Text
import pyperclip

master = tk.Tk()
master.title("Crypto Calculator v2.0")
master.geometry("384x592")
master.resizable(0,0)
master.attributes("-topmost",1,"-alpha",1)
master["bg"] = "#001E1F"


L_frame = tk.Frame(master,bg="#001E1F",bd=2,relief='groove',height=160,width=200)
L_frame.place(x=168,y=216)

reFont = tkfont.nametofont('TkDefaultFont')
reFont.config(size=10,weight=tkfont.BOLD)

# Widght New Class
class Label2(tk.Label):
    def __init__(self,tkwin,X,Y,default):
        self.txt = tk.StringVar()
        self.set,self.get = self.txt.set,self.txt.get
        self.set(default)
        super().__init__(tkwin,bg="#001e1f",fg="white",textvariable=self.txt)
        self.place(x=X,y=Y)

class Entry2(tk.Entry):
    def __init__(self,tkwin,X,Y,W,H):
        self.txt = tk.StringVar()
        self.set,self.get = self.txt.set,self.txt.get
        self.set("0")
        super().__init__(tkwin,textvariable=self.txt)
        self["validate"]="key"
        self["validatecommand"]=(limitCMD,"%P")
        self.bind("<KeyRelease>",fnc_allget)
        self.bind("<FocusIn>",lambda event:self.select_range(0,tk.END))
        self.place(x=X,y=Y,width=W,height=H)

class Combobox2(ttk.Combobox):
    def __init__(self,tkwin,X,Y,W,H):
        self.txt = tk.StringVar()
        self.set,self.get = self.txt.set,self.txt.get
        self.set("0")
        super().__init__(tkwin,values=feelist,textvariable=self.txt)
        self.current(0)
        self.bind("<<ComboboxSelected>>",fnc_allget)
        self.bind("<KeyRelease>",fnc_allget)
        self.place(x=X,y=Y,width=W,height=H)

class Button2(tk.Button):
    def __init__(self,tkwin,X,Y,W,H,BG,defualt,CMD):
        self.txt = tk.StringVar()
        self.set,self.get = self.txt.set,self.txt.get
        self.set(defualt)
        super().__init__(tkwin,textvariable=self.txt,fg="white",bg=BG,takefocus=0,command=CMD)
        self.place(x=X,y=Y,width=W,height=H)

class Scale2(tk.Scale):
    def __init__(self,tkwin,X,Y,VAR,FROM,TO,CMD):
        super().__init__(tkwin,from_=FROM,to=TO,variable=VAR \
            ,showvalue=0,troughcolor='#001E1F',command=CMD)
        self.place(x=X,y=Y)

# Variable
feelist = [0,0.018,0.02,0.036,0.04,0.075,0.1]
islong = True

# Functions
def fnc_allget(self=None):
    fnc_price()
    fnc_tax()

def fnc_price():
    opn = float(entry_price.get())
    lss = float(entry_loss.get())/100
    prft = float(entry_profit.get())/100
    opntx = float(combobox_open.get())/100
    clstx = float(combobox_close.get())/100
    lvrg = int(entry_leverage.get())
    dcml = int(label_decimal.get())
    if islong == True:
        #Long mode     
        if clstx < 1:
            tak = round(opn*(1+prft+opntx)/(1-clstx),dcml)
            stp = round(opn*(1-lss+opntx)/(1-clstx),dcml)
            evn = round(opn*(1+(opntx+clstx)/(1-clstx)),dcml)
            evn_prcnt = str(round((opntx+clstx)/(1-clstx)*100*lvrg,3))+"%"
        else:
            tak=stp=evn=evn_prcnt= "Call Police"
    else:
        #Short mode
        if opntx < 1:
            tak = round(opn*(1-prft-opntx)/(1+clstx),dcml)
            stp = round(opn*(1+lss-opntx)/(1+clstx),dcml)
            evn = round(opn*(1-(opntx+clstx)/(1+clstx)),dcml)
            evn_prcnt = str(round((opntx+clstx)/(1+clstx)*100*lvrg,3))+"%"
        else:
            tak=stp=evn=evn_prcnt= "Call Police"
    button_take.set(tak)
    button_stop.set(stp)
    button_even.set(evn)
    label_even_percent.set(evn_prcnt)

def fnc_tax():
    x = int(entry_leverage.get())   
    opntx = float(combobox_open.get())/100
    clstx = float(combobox_close.get())/100
    l = float(entry_loss.get())/100
    p = float(entry_profit.get())/100
    shwlss = round(100*l*x,2)
    shwprft = round(100*p*x,2)
    if islong == True:
        if clstx < 1:
            prtxprft ="Pretax Take\n"    +str(round(100*x* ((1+p+opntx)/(1-clstx) -1),2))+"%"
            prtxlss ="Pretax Stop\n"      +str(round(100*x* ((1-l+opntx)/(1-clstx) -1),2))+"%"
        else:
            prtxprft=prtxlss= "Call Police"
    else:
        if opntx < 1: 
            prtxprft = "Pretax Take\n"   +str(round(100*x* (1- (1-p-opntx)/(1+clstx) ),2))+"%"
            prtxlss = "Pretax Stop\n"     +str(round(100*x* (1- (1+l-opntx)/(1+clstx) ),2))+"%"
        else:
            prtxprft=prtxlss= "Call Police"
    label_profit_lvrged.set(str(shwprft)+'%')
    label_loss_lvrged.set(str(shwlss)+'%')
    label_pretax_take.set(prtxprft)
    label_pretax_stop.set(prtxlss)

def fnc_longshort():
    global islong
    if islong == True:
        button_mode.set("SHORT")
        button_take['bg']="firebrick"
        button_stop['bg']="mediumseagreen"
        islong = False
    else:
        button_mode.set("LONG")
        button_take['bg']="mediumseagreen"
        button_stop['bg']="firebrick"
        islong = True
    fnc_allget()

# Secondary Functions
def fnc_zero_set(event=None):
    if  entry_price.get():
        pass
    else:
        entry_price.set(0)
        entry_price.select_to(1)
    fnc_price()
    fnc_tax()

def fnc_wheel(event,name,n,isfloat):
    if isfloat:
        if event.delta >0 :
            name.set(round(float(name.get())+n,2))
        else :
            name.set(round(float(name.get())-n,2))
    else:
        if event.delta >0 :
            name.set(round(int(name.get())+n,2))
        else :
            name.set(round(int(name.get())-n,2))
    fnc_zero_set()

def fnc_limit(content):
    result=False
    valist=["0","1","2","3","4","5","6","7","8","9","."]
    pointvali=list(content)
    if len (content) > 1:    
        del pointvali[-1]
    for j in pointvali:
        if j==".":
            valist=["0","1","2","3","4","5","6","7","8","9"]
            break           
    for i in valist:
        if  content=="" or content[-1]==i :
            result=True            
            break
    return result
limitCMD = master.register(fnc_limit)    

## Create Widget ##
entry_price = Entry2(master,16,16,352,72)
entry_loss = Entry2(master,16,128,104,40)
entry_profit = Entry2(master,16,208,104,40)
entry_leverage = Entry2(master,16,304,104,40)

combobox_open = Combobox2(master,16,400,104,40)
combobox_close = Combobox2(master,16,480,104,40)

label_loss = Label2(master,16,96,"Loss:")
label_loss_lvrged = Label2(master,64,96,"0.0%")
label_profit = Label2(master,16,176,"Profit:")
label_profit_lvrged = Label2(master,60,176,"0.0%")
label_lvrg = Label2(master,16,272,"Leverage")
label_decimal = Label2(master,200,176,0)
label_open = Label2(master,16,368,"OpenFee")
label_close = Label2(master,16,448,"CloseFee")
label_even_percent = Label2(master,80,448,None)
label_pretax_stop = Label2(L_frame,8,96,"Pretax Stop\n0.0%") 
label_pretax_take = Label2(L_frame,104,96,"Pretax Take\n0.0%")

button_stop = Button2(master,192,104,152,56,"firebrick","Stop Loss",None)
button_take = Button2(master,192,392,152,56,"mediumseagreen","Take Profit",None)
button_mode = Button2(master,16,536,104,40,"steelblue","LONG",fnc_longshort)
button_even = Button2(L_frame,32,24,136,48,"black","Even",None)

scale_leverage = Scale2(master,132,174,entry_leverage.txt,125,1,None)
scale_decimal = Scale2(master,224,176,label_decimal.txt,0,8,None) 


## adjust widget ##
entry_price.config(justify="center",font=("Bahnschrift",28))

label_loss_lvrged.config(fg="lightpink")
label_profit_lvrged.config(fg="lightgreen")
label_pretax_stop.config(fg="lightpink")
label_pretax_take.config(fg="lightgreen")

button_stop.config(command=lambda :pyperclip.copy(button_stop.get()))
button_even.config(command=lambda :pyperclip.copy(button_even.get()))
button_take.config(command=lambda :pyperclip.copy(button_take.get()))
button_mode.config(activeforeground='white',activebackground='steelblue',font=('Bahnschrift Bold',18))

scale_leverage.config(length=260)
scale_decimal.config(orient=HORIZONTAL)

## binding ##
entry_loss.bind("<MouseWheel>",lambda event:fnc_wheel(event,entry_loss,0.05,True))
entry_profit.bind("<MouseWheel>",lambda event:fnc_wheel(event,entry_profit,0.05,True))
entry_leverage.bind("<MouseWheel>",lambda event:fnc_wheel(event,entry_leverage,5,False))

scale_leverage["command"]=fnc_allget
scale_decimal["command"]=fnc_allget

entry_price.focus()
master.mainloop()

####計算機算式####
# Long
# take = open*(1+profit+openfee)/(1-closefee) √
# stop = open*(1-loss+openfee)/(1-closefee) √

# Short
# take = open*(1-profit-openfee)/(1+closefee) √
# stop = open*(1+loss-openfee)/(1+closefee) √

# Lvrg Long Percentage
# pretax% = X *((1+profit+openfee)/(1-closefee))-1) √
# pretax% = X *((1-loss+openfee)/(1-closefee))-1) √

# Lvrg Short Percentage
# pretax% = X *(1-(1-profit-openfee)/(1+closefee)) √
# pretax% = X *(1-(1+loss-openfee)/(1+closefee)) √

# Even Price (Long)
# even_var = open*(1+((openfee+closefee)/(1-closefee))) √
# Even Price (Short)
# even_var = open*(1-((openfee+closefee)/(1+closefee))) √

# Even% (Long)
# even_percent_label_var = X *(openfee+closefee)/(1-closefee)
# Even% (Short)
# even_percent_label_var = X *(openfee+closefee)/(1+closefee)
