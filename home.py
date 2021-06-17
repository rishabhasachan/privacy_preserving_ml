import os
import sys
from tkinter import *
import tkinter as tk
from tkinter import ttk
import phe as paillier
import json
from linmodel import LinModel


root = Tk()

root.geometry("1080x720") 

################################customer status ####################
custFrame=Frame(root, width=250, height=550, bg='#ffffff')
custFrame.pack()
custFrame.place(x=310,y=200)

t = tk.Text(custFrame, width=50, height=70)
t.pack()
t.place(x=0,y=0)

################################ company status ####################
comFrame=Frame(root, width=650, height=550, bg='#ffffff')
comFrame.pack()
comFrame.place(x=850,y=200)

t_com = tk.Text(comFrame, width=80, height=70)
t_com.pack()
t_com.place(x=0,y=0)
#t_com.insert(tk.END,str(datafile))



def storeKeys():
	public_key, private_key = paillier.generate_paillier_keypair()
	keys={}
	keys['public_key'] = {'n': public_key.n}
	keys['private_key'] = {'p': private_key.p,'q':private_key.q}
	with open('custkeys.json', 'w') as file: 
		json.dump(keys, file)
		t.delete('1.0', tk.END)
		t.insert(tk.END,str(keys))

def getKeys():
	with open('custkeys.json', 'r') as file: 
		keys=json.load(file)
		pub_key=paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
		priv_key=paillier.PaillierPrivateKey(pub_key,keys['private_key']['p'],keys['private_key']['q'])
		return pub_key, priv_key 

def serializeData(public_key, data):
	encrypted_data_list = [public_key.encrypt(x) for x in data]
	encrypted_data={}
	encrypted_data['public_key'] = {'n': public_key.n}
	encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in         encrypted_data_list]
	serialized = json.dumps(encrypted_data)
	return serialized

def loadAnswer():
    with open('answer.json', 'r') as file:
            ans=json.load(file)
            answer=json.loads(ans)
            return answer

def send_data():
    pub_key, priv_key = getKeys()
    data = [int(e_age.get()),int(e_eat.get()),int(e_life.get()),int(e_gen.get())]
    serializeData(pub_key, data)
    datafile=serializeData(pub_key, data)
    with open('data.json', 'w') as file: 
        json.dump(datafile, file)
        t_com.delete('1.0', tk.END)
        t_com.insert(tk.END,str(datafile))
    return pub_key, priv_key, data


def get_data():
    pub_key, priv_key = getKeys()
    answer_file=loadAnswer()
    answer_key=paillier.PaillierPublicKey(n=int(answer_file['pubkey']['n']))
    answer = paillier.EncryptedNumber(answer_key, int(answer_file['values'][0]), int(answer_file['values'][1]))
    if (answer_key==pub_key):
        print(priv_key.decrypt(answer))
        t.delete('1.0', tk.END)
        t.insert(tk.END,str(priv_key.decrypt(answer)))




w = Label(root, bg="#3b5998", fg="white", width=1000,height=7)
w.pack()
w.place(x=0,y=0)

w1 = Label(root,bg="#3b5998", text="Privacy preserving" ,fg="white", font=("",40))
w1.pack()
w1.place(x=50,y=40)

lcus = Label(root,bg="white", text="Customer" ,fg="black", font=("",30))
lcus.pack()
lcus.place(x=50,y=140)

lcom = Label(root,bg="white", text="Company" ,fg="black", font=("",30))
lcom.pack()
lcom.place(x=600,y=140)
  

def linm():
    os.system('linmodel.py')
    #label_status = Label(root,text =LinModel().getCoef(),fg = "blue")
    #label_status.pack()
    #label_status.place(x=600,y=300)
    t_com.delete('1.0', tk.END)
    t_com.insert(tk.END,str(LinModel().getCoef()))

# COMPANY SIDE
b2 = Button(root,text="Train model" ,bg="#3b5998", width=30, height=5, command=linm)
b2.pack()
b2.place(x=600,y=220)

# FROM CUSTOMER SIDE
bcal1 = Button(root,text="1. gen key" ,bg="#3b5998", width=30, command=storeKeys)
bcal1.pack()
bcal1.place(x=50,y=220)



e_age = Entry(root, width=40)
e_age.insert(0, 'age')
e_age.pack()
e_age.place(x=50,y=300)

e_eat = Entry(root, width=40)
e_eat.insert(0, 'healthy_eating')
e_eat.pack()
e_eat.place(x=50,y=330)

e_life = Entry(root, width=40)
e_life.insert(0, 'active_lifestyle')
e_life.pack()
e_life.place(x=50,y=360)

e_gen = Entry(root, width=40)
e_gen.insert(0, 'Gender')
e_gen.pack()
e_gen.place(x=50,y=390)


bcal2 = Button(root,text="2. send ency data" ,bg="#3b5998", width=30, command=send_data)
bcal2.pack()
bcal2.place(x=50,y=430)

bcal3 = Button(root,text="3. get data" ,bg="#3b5998", width=30, command=get_data)
bcal3.pack()
bcal3.place(x=50,y=550)




def servercalc():
    os.system('servercalc.py')
    #label_status = Label(comFrame,text =loadAnswer(),fg = "blue")
    #label_status.pack()
    #label_status.place(x=0,y=0)
    t_com.delete('1.0', tk.END)
    t_com.insert(tk.END,str(loadAnswer()))

b2 = Button(root,text="Server prediction" ,bg="#3b5998", width=30, height=5, command=servercalc)
b2.pack()
b2.place(x=600,y=450)

root.mainloop()