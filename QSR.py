#!/usr/bin/env python
# coding: utf-8

# # PREVENÇÃO DE ATAQUES DDOS EM NFV/SDN
# 
# ## Roteamento seguro comReinforcement Learning

# In[1]:


get_ipython().system('pip install -q gym')
get_ipython().system('pip install -q matplotlib')
get_ipython().system('pip install -q ipython')


# In[2]:


import pandas as pd
import requests as rq
import csv
import gym
import random
import numpy as np
import copy
import time
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.ttk import *


# In[3]:


def QLearning(rewards, goal_state=None, gamma=0.99, alpha=0.01, num_episode=1000, min_difference=1e-5,source=0):
    """ 
    Run Q-learning loop for num_episode iterations or till difference between Q is below min_difference.
    """
#    Q = np.asarray(pd.read_csv('Qvalues.db', sep = ';',header=None))

    Q = np.zeros(rewards.shape)
    all_states = np.arange(len(rewards))
    for i in range(num_episode):
        
        Q_old = copy.deepcopy(Q)
        
        # initialize state

        initial_state = all_states[source]
        
        action = np.random.choice(np.where(rewards[initial_state] != -float('inf'))[0]) 
        
#        print(f'ESTADO INICIAL: {Q[initial_state][action]} + {alpha} * ({rewards[initial_state][action]} + {gamma} * {np.max(Q[action])} - {Q[initial_state][action]})')

        Q[initial_state][action] = Q[initial_state][action] + alpha * (rewards[initial_state][action] + gamma * np.max(Q[action]) - Q[initial_state][action])
        
        Q[initial_state][action] = (1 - alpha) * Q[initial_state][action] + alpha * (rewards[initial_state][action] + gamma * np.max(Q[action]))
        
#        print(f'Q INICIAL: {Q[initial_state][action]}')

        cur_state = action
        
        # loop for each step of episode, until reaching goal state
        
        while cur_state != goal_state:
            
            # choose action form states using policy derived from Q
        
            action = np.random.choice(np.where(rewards[cur_state] != -float('inf'))[0])
            
#            print(f'ESTADO ATUAL: {Q[cur_state][action]} + {alpha} * ({rewards[cur_state][action]} + {gamma} * {np.max(Q[action])} - {Q[cur_state][action]})')

            #Q[cur_state][action] = Q[cur_state][action] + alpha * (rewards[cur_state][action] + gamma * np.max(Q[action]) - Q[cur_state][action])
    
            Q[cur_state][action] = (1 - alpha) * Q[cur_state][action] + alpha * (rewards[cur_state][action] + gamma * np.max(Q[action]))
        
#            print(f'Q ATUAL: {Q[cur_state][action]}')

            cur_state = action
            
    return np.around(Q/np.max(Q)*100)
#    return Q/np.max(Q)*100


# In[20]:


def sair():
    
    #Encerra a interface gráfica
    
    window.destroy()

def selecionaRotas(Q, Qdst):

    #Seleciona os caminhos com o valor Q mais alto (ORIGEM)
    
    rtable = []
    for i in range(len(nexthop)):
        temptable = []
        oldQ = 0
        print(f'Roteador {i+1} \r\n')
        for j in range(len(nexthop[i])):
            
            if Q[i][j] > oldQ:
                print(f'{Q[i][j]} > {oldQ}')
                temptable = [nexthop[i][j]] + [Q[i][j]]
                oldQ = Q[i][j]
            print(f'Roteador:{j+1} Nexthop: {nexthop[i][j]}, Valor de Q: {Q[i][j]}')
        print('\r\n')
        rtable.append(temptable)

        
        
    url = f'http://192.168.0.23:8080/router/all'
    ip = f'{{"route_id":"all"}}'
    x = rq.delete(url,data = ip)
    print(x)
    #Envia os melhores caminhos para a controladora via método POST
    
    for i in range(len(rtable)-1):

        url = f'http://192.168.0.23:8080/router/000000000000000{i+1}'
        ip = f'{{"destination":"172.16.20.0/24","gateway":"{rtable[i][0]}"}}'
        print(ip)
        x = rq.post(url,data = ip)
        print(x)
        
    #Seleciona os caminhos com o valor Q mais alto (DESTINO)  
    
    rtableDst = []
    
    for i in (range(len(nexthop))):
        temptableDst = ['0',0.0]
        oldQDst = 0

        for j in (range(len(nexthop[i]))):
            print(f'Roteador:{j+1} Nexthop: {nexthop[i][j]}, Valor de Q: {Qdst[i][j]}')

            if Qdst[i][j] > oldQDst:
                print(f'{Qdst[i][j]} > {oldQDst}')
                temptableDst = [nexthop[i][j]] + [Qdst[i][j]]
                oldQDst = Qdst[i][j]

                
        
        print('\r\n')
        rtableDst.append(temptableDst)

            #Envia os melhores caminhos para a controladora via método POST

    for i in (range(len(rtableDst))):

        print(i)
        url = f'http://192.168.0.23:8080/router/000000000000000{i+1}'
        ip = f'{{"destination":"172.16.10.0/24","gateway":"{rtableDst[i][0]}"}}'
        if rtableDst[i][1] != 0:
            print(f'{ip} - {url}')
            x = rq.post(url,data = ip)
            print(x)

def interfaceGrafica():
   
    def refresh():
  
        def getQ():

            #Origem e Destino definidos pela interface gráfica
            
            #Recompensas
            rewards = np.asarray(pd.read_csv('rewards.db', sep = ';',header=None))
            rewardsDst = np.asarray(pd.read_csv('rewardsDst.db', sep = ';',header=None))

            #Calcula Q
            Q = []
            Qdst = []

            Q = QLearning(rewards, goal_state=goal_state, gamma=gamma, alpha=alpha, num_episode=num_episode, min_difference=min_difference, source=source)           
            
            Qdst = QLearning(rewardsDst, goal_state=source, gamma=gamma, alpha=alpha, num_episode=num_episode, min_difference=min_difference, source=goal_state)

            #Grava o resultado da tabela Q em banco
            
            pd.DataFrame(Q).to_csv('Qvalues.db', sep=';', header=None, index=None)
            pd.DataFrame(Qdst).to_csv('QvaluesDst.db', sep=';', header=None, index=None)

            return Q, Qdst
        
        #Popula a tela do QSR com os dados de Q

        Q,Qdst = getQ()
        
        selecionaRotas(Q, Qdst)

        for i in tree.get_children():
            tree.delete(i)
        for i in treeDst.get_children():
            treeDst.delete(i)

        for i in range(len(Q)):
            tree.insert("", 'end', values=(list(Q[i])))
        for i in range(len(Qdst)):
            treeDst.insert("", 'end', values=(list(Qdst[i])))
            
        #Executa novamente o refresh a cada 30s      
        time_label.after(30000, refresh)
    
    #Interface gráfica


    upt = Frame(window)
    upt.pack(side='top',anchor='n')
    
    upe = Frame(window)
    upe.pack(side='top',anchor='n')


    time_label = Label(upt, font = 'calibri 12 bold', foreground = 'black')
    time_label.pack(side='top')
    time_label.config(text = 'QSR - Q-Learning Secure Routing')

    src_label = Label(upe, font = 'calibri 12 bold', foreground = 'black')
    src_label.pack(side='left',anchor='ne',padx=200,ipadx=150)
    src_label.config(text = 'Source')
    
    dst_label = Label(upe, font = 'calibri 12 bold', foreground = 'black')
    dst_label.pack(side='right',anchor='nw',padx=160,ipadx=100)
    dst_label.config(text = 'Destination')
    
    btn_sair=Button(window, text="Sair",command=sair).pack()
    
    tree = ttk.Treeview(window,columns=("R1","R2","R3","R4","R5","R6","R7","R8"), height=100)
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
        
    refresh()

    window.mainloop()      

if __name__ == "__main__":

    # Parâmetros Q-Learning

    gamma = 0.8 #Fator de desconto
    alpha = 0.01 #Taxa de Aprendizado
    num_episode = 2000 #Número de loops
    min_difference = 1e-3 #Diferença mínima entre valores de Q para convergência
    goal_state = 7 #Roteador destino
    source = 0 #Roteador origem
    
    #Método POST para registro interfaces

    ips = pd.read_csv('db_interfaces.csv', sep = ';')

    for r in ips['Router']:

        url = f'http://192.168.0.23:8080/router/000000000000000{r}'

        for i in ips.iloc[r-1]:
            if type(i) == str:
                ip = f'{{"address":"{i}"}}'
                x = rq.post(url,data = ip)
                #print(x)
    
    #Registro dos NextHops
    
    nexthop = [
    #R1
    [0,'192.168.200.2','192.168.200.10',0,'192.168.200.6',0,0,0],
    #R2
    ['192.168.200.1',0,'192.168.200.14','192.168.200.22','192.168.200.18',0,0,0],
    #R3
    ['192.168.200.9','192.168.200.13',0,'192.168.200.26','192.168.200.34','192.168.200.30','192.168.200.38',0],
    #R4
    [0,'192.168.200.21','192.168.200.25',0,'192.168.200.42','192.168.200.54','192.168.200.46','192.168.200.50'],
    #R5
    ['192.168.200.5','192.168.200.17','192.168.200.33','192.168.200.41',0,'192.168.200.58','192.168.200.62',0],
    #R6
    [0,0,'192.168.200.29','192.168.200.53','192.168.200.57',0,'192.168.200.66','192.168.200.70'],
    #R7
    [0,0,'192.168.200.37','192.168.200.45','192.168.200.61','192.168.200.65',0,'192.168.200.74'],
    #R8
    [0,0,0,'192.168.200.49',0,'192.168.200.69','192.168.200.73',0]
]

    #Inicialização da Interface Gráfica
    
    window = Tk()
    window.title("QSR - Q-Learning Secure Routing")
    window.geometry('1200x300')
    window.resizable(False, False)
    interfaceGrafica()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




