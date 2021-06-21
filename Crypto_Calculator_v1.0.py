
from os import name
import tkinter as tk
from tkinter.constants import CENTER
import tkinter.ttk as ttk
import tkinter.font as tkfont
from typing import Text
import pyperclip

master = tk.Tk()
master.title("Crypto Calculator ver_1.0")
master.geometry("384x592")
master.resizable(0,0)
master.iconbitmap('my_first_program\crycal.ico')
master.title("Crypto Calculator ver_1.1")
master.geometry("384x592")
master.resizable(0,0)
#master.iconbitmap('my_first_program\crycal.ico')
master.attributes("-topmost",1,"-alpha",1)
master['bg']= "#001E1F"

modifyfont = tkfont.nametofont('TkDefaultFont')
modifyfont.config(size=10,weight=tkfont.BOLD)

### Button & function ###

open=loss=profit=openfee=closefee=take=stop=even=leverage = 0
take_button_var = tk.StringVar()
loss_button_var = tk.StringVar()
even_button_var = tk.StringVar()
take_button_var.set("Take Profit")
loss_button_var.set("Stop Loss")
even_button_var.set("Even")
islong = True

def fnc_Lvrg_cal():
    x = float(lvrg_var.get())   
    openfe = float(box_openfee.get())/100
    closefee = float(box_closefee.get())/100
    a = round(profit_var.get()*lvrg_var.get(),2)
    b = round(loss_var.get()*lvrg_var.get(),2)
    if islong == True:
        if float(box_closefee.get()) < 100:
            m ="Pretax Profit\n"    +str(round(100*x* ((1+profit_var.get()  /100+openfe)/(1-closefee) -1),2))+"%"
            n ="Pretax Loss\n"      +str(round(100*x* ((1-loss_var.get()    /100+openfe)/(1-closefee) -1),2))+"%"
        else:
            m=n= "Call Police"
    else:
        if float(box_openfee.get()) < 100: 
            m = "Pretax Profit\n"   +str(round(100*x* (1- (1-profit_var.get()   /100-openfe)/(1+closefee) ),2))+"%"
            n = "Pretax Loss\n"     +str(round(100*x* (1- (1+loss_var.get()     /100-openfe)/(1+closefee) ),2))+"%"
        else:
            m=n= "Call Police"
    label_Profit_lvrged.config(text= str(a)+'%')
    label_Loss_lvrged.config(text= str(b)+'%')
    label_Pretax_profit.config(text= m)
    label_Pretax_loss.config(text= n)

def fnc_Calculate():
    global open,loss,profit,openfee,closefee,take,stop,even,leverage
    open = float(price_var.get())
    loss = loss_var.get()/100
    profit = profit_var.get()/100
    openfee = float(box_openfee.get())/100
    closefee = float(box_closefee.get())/100
    leverage = float(entry_Lvrg.get())
    if islong == True:    #Long mode
        if float(box_closefee.get()) < 100:
            take = round(open*(1+profit+openfee)/(1-closefee),int(decimal_var.get()))
            stop = round(open*(1-loss+openfee)/(1-closefee),int(decimal_var.get()))
            even = round(open*(1+(openfee+closefee)/(1-closefee)),int(decimal_var.get()))
            even_percent = str(round((openfee+closefee)/(1-closefee)*100*leverage,3))+"%"
        else:
            take=stop=even=even_percent= "Call Police"
    else:               #Short mode
        if float(box_openfee.get()) < 100:
            take = round(open*(1-profit-openfee)/(1+closefee),decimal_var.get())
            stop = round(open*(1+loss-openfee)/(1+closefee),decimal_var.get())
            even = round(open*(1-(openfee+closefee)/(1+closefee)),int(decimal_var.get()))
            even_percent = str(round((openfee+closefee)/(1+closefee)*100*leverage,3))+"%"
        else:
            take=stop=even=even_percent= "Call Police"
    take_button_var.set(take)
    loss_button_var.set(stop)
    even_button_var.set(even)
    even_percent_label_var.set(even_percent)


def fnc_Longshort():
    global islong
    if islong == True:
        button_MODE.config(text='SHORT')
        button_Take.config(bg='firebrick')
        button_Stop.config(bg='mediumseagreen')
        islong = False
    else:
        button_MODE.config(text='LONG')
        button_Take.config(bg='mediumseagreen')
        button_Stop.config(bg='firebrick')

        islong = True
    fnc_Calculate()
    fnc_Lvrg_cal()

def fnc_Widget_cal(event=None):
    fnc_Calculate()
    fnc_Lvrg_cal()

def fnc_scroll(event,name,n):
    if event.delta >0 :
        name.set(round(name.get()+n,2))
    else :
        name.set(round(name.get()-n,2))
    fnc_Widget_cal()


### Entry ###

price_var = tk.StringVar()
price_var.set(2048)
entry_Price = tk.Entry(master,textvariable=price_var,font=("Arial",28),justify='center')
entry_Price.bind('<Return>',fnc_Widget_cal)
entry_Price.bind("<FocusIn>",lambda self :entry_Price.select_range(0,tk.END))

loss_var = tk.DoubleVar()
entry_Loss = tk.Entry(master,textvariable=loss_var)
entry_Loss.bind('<Return>',fnc_Widget_cal)
entry_Loss.bind('<MouseWheel>',lambda self:fnc_scroll(self,loss_var,0.05))

profit_var = tk.DoubleVar()
entry_Profit = tk.Entry(master,textvariable=profit_var)
entry_Profit.bind('<Return>',fnc_Widget_cal)
entry_Profit.bind('<MouseWheel>',lambda self:fnc_scroll(self,profit_var,0.05))

lvrg_var =tk.IntVar()
lvrg_var.set(1)
entry_Lvrg = tk.Entry(master,textvariable=lvrg_var)
entry_Lvrg.bind('<Return>',fnc_Widget_cal)
entry_Lvrg.bind('<MouseWheel>',lambda self:fnc_scroll(self,lvrg_var,1))

### Combobox ###
feelist = [0,0.018,0.02,0.036,0.04,0.075,0.1]
box_openfee = ttk.Combobox(master,values=feelist)
box_openfee.current(0)
box_openfee.bind('<<ComboboxSelected>>',fnc_Widget_cal)
box_openfee.bind('<Return>',fnc_Widget_cal)
box_closefee = ttk.Combobox(master,values=feelist)
box_closefee.current(0)
box_closefee.bind('<<ComboboxSelected>>',fnc_Widget_cal)
box_closefee.bind('<Return>',fnc_Widget_cal)

### Button ###

button_MODE = tk.Button(master,text="LONG",command=fnc_Longshort, \
    activeforeground='white',fg='white',activebackground='steelblue',bg='steelblue',font=('arial',18,'bold'))
button_Take = tk.Button(master,textvariable=take_button_var,fg="white",bg="mediumseagreen",command=lambda :pyperclip.copy(take))
button_Stop = tk.Button(master,textvariable=loss_button_var,fg="white",bg="firebrick",command=lambda :pyperclip.copy(stop))

### Lable ###
label_Profit = tk.Label(master,text="Profit:",fg="white",bg="#001E1F")
label_Loss = tk.Label(master,text="Loss:",fg="white",bg="#001E1F")


label_openfe = tk.Label(master,text="Openfee",fg="white",bg="#001E1F")
label_closefee = tk.Label(master,text="Closefee",fg="white",bg="#001E1F")

#### Controller ####

scale_Lvrg = tk.Scale(master,variable=lvrg_var,showvalue=0,from_=125,to=1,troughcolor='#001E1F',command=fnc_Widget_cal)

decimal_var = tk.IntVar()
decimal_var.set(2)
scale_Decimal = tk.Scale(master,variable=decimal_var,from_=0,to=8, \
    showvalue=0,troughcolor='#001E1F',orient='horizontal',command=fnc_Widget_cal)
label_Decimal_var = tk.Label(master,textvariable=decimal_var)

### Leverage ###
lvrgframe = tk.Frame(master,bg="#001E1F",bd=2,relief='groove',height=160,width=200)
lvrgframe.place(x=168,y=216)                            #[槓桿框架]

label_Lvrg = tk.Label(master,text="Leverage",fg="white",bg="#001E1F")
label_Profit_lvrged = tk.Label(master,text="Goal%",fg="lightgreen",bg="#001E1F")
label_Loss_lvrged = tk.Label(master,text="Goal%",fg="lightpink",bg="#001E1F")

even_percent_label_var = tk.StringVar()
even_percent_label_var.set("Even%")
label_Even_percent = tk.Label(master,textvariable=even_percent_label_var,fg="white",bg="#001E1F")

### Frame ###

pretax_profit_var = tk.DoubleVar()
pretax_profit_var.set(0)
label_Pretax_profit = tk.Label(lvrgframe,text="Pretax Profit\nGoal%",fg="lightgreen",bg="#001E1F")
pretax_loss_var = tk.DoubleVar()
pretax_loss_var.set(0)
label_Pretax_loss = tk.Label(lvrgframe,text="Pretax Loss\nGoal%",fg="lightpink",bg="#001E1F")

button_Even = tk.Button(lvrgframe,textvariable=even_button_var,fg="white",bg="black",command=lambda :pyperclip.copy(even))


button_Even.place(x=32,y=24,width=136,height=48)        #成本按鈕
label_Pretax_profit.place(x=8,y=96)
label_Pretax_loss.place(x=104,y=96)                    #稅前損利率標籤

### Widgets Placer ###

entry_Price.place(x=16,y=16,width=352,height=72)        #價格輸入

label_Loss.place(x=16,y=96)
label_Loss_lvrged.place(x=64,y=96)
entry_Loss.place(x=16,y=128,width=104,height=40)        #虧損率輸入

label_Profit.place(x=16,y=176)
label_Profit_lvrged.place(x=64,y=176)
entry_Profit.place(x=16,y=208,width=104,height=40)      #利潤率輸入

scale_Lvrg.place(x=132,y=174)
scale_Lvrg['length']=260
label_Lvrg.place(x=16,y=272)
entry_Lvrg.place(x=16,y=304,width=104,height=40)        #槓桿輸入


button_Stop.place(x=192,y=104,width=152,height=56)      #止損按鈕

label_Decimal_var.place(x=200,y=176)
scale_Decimal.place(x=224,y=176)                        #小數點滑桿

button_Take.place(x=192,y=392,width=152,height=56)      #止盈按鈕


label_openfe.place(x=16,y=368)
box_openfee.place(x=16,y=400,width=104,height=40)       #開倉稅

label_closefee.place(x=16,y=448)
box_closefee.place(x=16,y=480,width=104,height=40)      #平倉稅
label_Even_percent.place(x=80,y=448)                    #成本率


button_MODE.place(x=16,y=536,width=104,height=40)       #多空按鈕

entry_Price.focus()
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
