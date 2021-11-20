#!/usr/bin/env python
# coding: utf-8

# In[29]:


import numpy as np
import pandas as pd
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.ttk import *

def sair():
    window.destroy()

def reset():
    r = 8
    
    rewards = np.asarray(pd.read_csv('rewards.db', sep = ';',header=None))
    for i in range(len(rewards)):
        for j in range(len(rewards[i])):
            if rewards[i][j] != -float('inf'):
                if j != r - 1:
                    rewards[i][j] = 1.0
                elif j == r - 1:
                    rewards[i][j] = 100.0
                else:
                    print("Alguma coisa deu errado.")

    pd.DataFrame(rewards).to_csv('rewards.db', sep=';', header=None, index=None)
    
    r = 1
    
    rewardsDst = np.asarray(pd.read_csv('rewardsDst.db', sep = ';',header=None))
    for i in range(len(rewardsDst)):
        for j in range(len(rewardsDst[i])):
            if rewardsDst[i][j] != -float('inf'):
                if j != r - 1:
                    rewardsDst[i][j] = 1.0
                elif j == r - 1:
                    rewardsDst[i][j] = 100.0
                else:
                    print("Alguma coisa deu errado.")

    pd.DataFrame(rewardsDst).to_csv('rewardsDst.db', sep=';', header=None, index=None)
 
    refresh(rewards,rewardsDst)   
    
def ataque():
    r = int(combo.get())

    rewards = np.asarray(pd.read_csv('rewards.db', sep = ';',header=None))
    for i in range(len(rewards)):
        for j in range(len(rewards[i])):
            if j == r - 1:
                rewards[i][j] = rewards[i][j] - 1.0
                
    pd.DataFrame(rewards).to_csv('rewards.db', sep=';', header=None, index=None)
    
    rewardsDst = np.asarray(pd.read_csv('rewardsDst.db', sep = ';',header=None))
    for i in range(len(rewardsDst)):
        for j in range(len(rewardsDst[i])):
            if j == r - 1:
                rewardsDst[i][j] = rewardsDst[i][j] - 1.0
                
    pd.DataFrame(rewardsDst).to_csv('rewardsDst.db', sep=';', header=None, index=None)
    
    refresh(rewards,rewardsDst)
    
def refresh(rewards, rewardsDst):
    
    for i in tree.get_children():
        tree.delete(i)
    
    for i in range(len(rewards)):
        tree.insert("", 'end', values=(list(rewards[i])))
        
    for i in treeDst.get_children():
        treeDst.delete(i)
    
    for i in range(len(rewards)):
        treeDst.insert("", 'end', values=(list(rewardsDst[i])))
    
window = Tk()
window.title("QSR - Q-Learning Secure Routing")
window.geometry('1200x350')
window.resizable(False, False)

upt = Frame(window)
upt.pack(side='top',anchor='n')
    
upe = Frame(window)
upe.pack(side='top',anchor='n')

upw = Frame(window)
upw.pack(side='top',anchor='n')

time_label = Label(upt, font = 'calibri 12 bold', foreground = 'black')
time_label.pack(side='top')
time_label.config(text = 'Simulador de Ataques DDoS')

src_label = Label(upe, font = 'calibri 12 bold', foreground = 'black')
src_label.pack(side='left',anchor='ne',padx=200,ipadx=150)
src_label.config(text = 'Source')
    
dst_label = Label(upe, font = 'calibri 12 bold', foreground = 'black')
dst_label.pack(side='right',anchor='nw',padx=160,ipadx=100)
dst_label.config(text = 'Destination')

#Label(window, text='Selecione o roteador que quer atacar: ')
combo = Combobox(upw)
combo['values']= (1, 2, 3, 4, 5, 6, 7, 8)
combo.current(0)
combo.pack()

btn_atacar=Button(upw, text="Ataque",command=ataque).pack(side=LEFT, anchor='n')

btn_reset=Button(upw, text="Reset",command=reset).pack(side=LEFT, anchor='n')

btn_sair=Button(upw, text="Sair",command=sair).pack(side=LEFT, anchor='n')

tree = ttk.Treeview(window,columns=("R1","R2","R3","R4","R5","R6","R7","R8"), height=400)
tree.pack(side=LEFT)

tree.heading('R1', text="R1", anchor=W)
tree.heading('R2', text="R2", anchor=W)
tree.heading('R3', text="R3", anchor=W)
tree.heading('R4', text="R4", anchor=W)
tree.heading('R5', text="R5", anchor=W)
tree.heading('R6', text="R6", anchor=W)
tree.heading('R7', text="R7", anchor=W)
tree.heading('R8', text="R8", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=50)
tree.column('#1', stretch=NO, minwidth=0, width=50)
tree.column('#2', stretch=NO, minwidth=0, width=50)
tree.column('#3', stretch=NO, minwidth=0, width=50)
tree.column('#4', stretch=NO, minwidth=0, width=50)
tree.column('#5', stretch=NO, minwidth=0, width=50)
tree.column('#6', stretch=NO, minwidth=0, width=50)
tree.column('#7', stretch=NO, minwidth=0, width=50)

treeDst = ttk.Treeview(window,columns=("R1","R2","R3","R4","R5","R6","R7","R8"), height=100)
treeDst.pack(side=RIGHT)

treeDst.heading('R1', text="R1", anchor=W)
treeDst.heading('R2', text="R2", anchor=W)
treeDst.heading('R3', text="R3", anchor=W)
treeDst.heading('R4', text="R4", anchor=W)
treeDst.heading('R5', text="R5", anchor=W)
treeDst.heading('R6', text="R6", anchor=W)
treeDst.heading('R7', text="R7", anchor=W)
treeDst.heading('R8', text="R8", anchor=W)
    
treeDst.column('#0', stretch=NO, minwidth=0, width=50)
treeDst.column('#1', stretch=NO, minwidth=0, width=50)
treeDst.column('#2', stretch=NO, minwidth=0, width=50)
treeDst.column('#3', stretch=NO, minwidth=0, width=50)
treeDst.column('#4', stretch=NO, minwidth=0, width=50)
treeDst.column('#5', stretch=NO, minwidth=0, width=50)
treeDst.column('#6', stretch=NO, minwidth=0, width=50)
treeDst.column('#7', stretch=NO, minwidth=0, width=50)

rewards = np.asarray(pd.read_csv('rewards.db', sep = ';',header=None))

rewardsDst = np.asarray(pd.read_csv('rewardsDst.db', sep = ';',header=None))

refresh(rewards, rewardsDst)

tree.pack()

window.mainloop()


# In[ ]:





# In[ ]:




