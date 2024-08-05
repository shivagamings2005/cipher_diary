from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkVideoPlayer import TkinterVideo as tv
import mysql.connector as mysql
from tkinter import scrolledtext
import os
import shutil
import datetime
from datetime import date
from tkcalendar import Calendar
def encrypt(inp):
    val2=""
    val3=""
    for j in inp:
        if j != '\n':
            val=hex(ord(j))[2::]
            val3+=val
            val1=""
            for i in val:
                if i.isdigit():
                    val1+=str(bin(int(i))[2::])
                    c=6-len(str(bin(int(i))[2::]))
                    if c>=0:
                        val1+=('0'*c)+'11'
                    val1+=(bin(ord('\x1f'))[2::]+('0'*(3-len(bin(c)[2::])))+bin(c)[2::])
                elif i.isalpha():
                    val1+=str(bin(int(hex(ord(i))[2::]))[2::])
                    c=7-len(str(bin(int(hex(ord(i))[2::]))[2::]))
                    if c>=0:
                        val1+=('0'*c)+'1'
                    val1+=(bin(ord('\x1e'))[2::]+('0'*(3-len(bin(c)[2::])))+bin(c)[2::])
                val2+=chr(int(val1,2)-500)
                val1=""
        else:
            val2+='\n'
    #print(val2)
    if not os.path.exists('E:/cipher diary'):
        os.mkdir('E:/cipher diary')
    if not os.path.exists('E:/cipher diary/'+unt):
        os.mkdir('E:/cipher diary/'+unt)
    with open("E:/cipher diary/"+unt+"/"+str(datetime.date.today())+".txt","w",encoding="utf-8") as file:
        file.write(val2)
    cur.execute("select total_memories from cipher_diary where username = '{}'".format(unt))
    cure=cur.fetchall()
    for i in cure:
        for j in i:
            cure=j
    if cure ==None:
        cur.execute("update cipher_diary set total_memories=1 where username='{}'".format(unt))
    else:
        cur.execute("update cipher_diary set total_memories={} where username='{}'".format(int(cure)+1,unt))
    sql.commit()
    t.destroy()
    #decrypt()
def decrypt(inp):
    v=""
    for i in inp:
         if i !='\n':
            val=bin(ord(i)+500)[2::]
            c=16-len(val)
            val=('0'*c)+val
            val1=val[0:8]
            val2=val[8:13]
            val3=int(val[13::],2)
            if val2==bin(ord('\x1f'))[2::]:
               #v+=str(int(chr(int(val1[0:(6-val3)],2)).encode().hex()))
               v+=format(int(val1[0:(6-val3)],2),'X')
            elif val2==bin(ord('\x1e'))[2::]:
               v+=chr(int(str(int(val1[0:(7-val3)],2)),16))
         else:
            v+='\n'+'鈆'
    inp=""
    for i in range(0,len(v),2):
       try:
          inp+=chr(int(v[i]+v[i+1],16))
       except ValueError:
         inp+="\n"
    return inp         
def clr():
    for i in t.winfo_children():
        if str(i) =='.!tkintervideo':
            continue
        else:
            i.destroy()
def iv():
    if vide:
        a.play()
    t.after(2,iv)
def video(vid):
    global a,vide
    t.attributes('-fullscreen', True)
    a=tv(master=t,scaled=True)
    a.load(vid)
    a.pack(expand=True,fill="both")
    vide=True
    t.after(0,iv)
    login1()
def login11():
    global unt
    unt=""
    login1()
def login1():
    global unt,pw1,pw2,chk
    try:
        if chk==1:
            chk=1
    except NameError:
        chk=0
    if chk==1:
        clr()
    tk.Label(t,text="Username").place(x=350,y=200)
    tk.Label(t,text="Password").place(x=350,y=250)
    tk.Label(t,text="Retype\nPassword").place(x=350,y=300)
    tk.Label(t,text="Date of birth").place(x=350,y=350)
    try:
        t1=tk.Text(t,height=1,width=30,font=("Arial",22))
        t1.place(x=450,y=200)
        if unt !="":
            t1.insert(END,unt)
        else:
            un=tk.Entry(t,width=30,font="Arial 22")
            un.place(x=450,y=200)
            unt=un
    except NameError: 
        un=tk.Entry(t,width=30,font="Arial 22")
        un.place(x=450,y=200)
        unt=un
    pw1=tk.Entry(t,width=30,show="*",font="Arial 22")
    pw1.place(x=450,y=250)
    pw2=tk.Entry(t,width=30,show="*",font="Arial 22")
    pw2.place(x=450,y=300)
    calc()
    cal.place(x=450,y=350)
    tk.Label(t,text="Already have account").place(x=350,y=550)
    tk.Button(t,text="sign in",command=login2).place(x=500,y=550)
    tk.Button(t,text="next",command=aq1).place(x=960,y=550)
    chk=1
def login2():
    global unt,pw1,chk
    if chk==1:
        clr()
    tk.Label(t,text="Username").place(x=350,y=400)
    tk.Label(t,text="Password").place(x=350,y=450)
    un=tk.Entry(t,width=30,font="Arial 22")
    un.place(x=450,y=400)
    unt=un
    pw1=tk.Entry(t,width=30,show="*",font="Arial 22")
    pw1.place(x=450,y=450)
    tk.Label(t,text="Don't have account").place(x=350,y=550)
    tk.Button(t,text="Create It",command=login11).place(x=500,y=550)
    tk.Button(t,text="next",command=aq2).place(x=960,y=550)
    chk=1
def aq1():
    global unt,chk,vid
    try:
        unt=unt.get()
        usa=0
        if len(unt)>20:
            messagebox.showerror("Warning","Allowed username length is 20")
            chk=0
            unt=""
            login1()
        if len(unt)<5:
            messagebox.showerror("Warning","username length must be 5")
            chk=0
            unt=""
            login1()
        cur.execute("select username from cipher_diary")
        usc=cur.fetchall()
        for j in usc:
            for i in j:
                if i ==unt:
                    usa=1
                    break
        if usa ==1:
            messagebox.showerror("Warning","Username already exists")
            chk=0
            unt=""
            login1()
        if usa==0 and unt.strip()=="":
            messagebox.showerror("Warning","Username empty")
            login1()
        elif usa ==0:
            if pw1.get()==pw2.get():
                if len(pw1.get())>=6:
                    cur.execute("insert into cipher_diary (username,passwd,dob) values('{}','{}','{}')".format(unt,pw1.get(),cal.selection_get().strftime("%Y-%m-%d")))
                    sql.commit()
                    vide=False
                    cn()
                else:
                    messagebox.showerror("Warning","Password Must be 6 characters")
                    login1()
            else:
                messagebox.showerror("Warning","Password Mismatch")
                login1()
    except AttributeError:
        print("")
def aq2():
    global unt
    try:
        unt=unt.get()
        cur.execute("select username from cipher_diary")
        usc=cur.fetchall()
        usa=0
        if len(unt)>10:
            messagebox.showerror("Warning","Allowed username length is 20")
            chk=0
            unt=""
            login1()
        for i in usc:
            if str(i)[2:-3] ==unt:
                usa=1
                break
        if usa==1:
            cur.execute("select passwd from cipher_diary where username='{}'".format(unt))
            pws=cur.fetchall()
            if (str(pws)[3:-4])==(str(pw1.get())):
               cre()
            else:
                pyn=messagebox.askyesno("Warning","Password incorrect\nWant to create new password?")
                if pyn==1:
                    fp()
                else:
                    messagebox.showinfo("Note","Retype your password")
                    login2()
        else:
            messagebox.showerror("Warning","Username doesn't exists")
            yn=messagebox.askyesno("Note","Username doesn't exists\nWant to create account")
            if yn==1:
                login1()
            else:
                t.destroy()
    except AttributeError:
        print("")
def calc():
    global cal
    cal = Calendar(t,year = date.today().year, month = date.today().month,
               day = date.today().day,background="#000000",foreground="#01fefd",
               bordercolor="#90fefd",disabledbackground="#000000",
               disabledforeground="#ffffff",headersbackground="#ffffff",
               normalbackground="#000000",normalforeground="#01fefd",
               weekendbackground="#000000",weekendforeground="#01fefd",
               othermonthbackground="#696969",othermonthforeground="#01fefd",
               othermonthwebackground="#696969",othermonthweforeground="01fefd")
def cre():
    if os.path.exists("E:/cipher diary/"+unt+"/"+str(datetime.date.today())+".txt")==1:
        clr()
        #logim=PhotoImage(file="C:/Users/user/Downloads/1.png")
        #logim2=Label(image=logim)
        tk.Button(t,text="Delete Account",command=da).place(x=560,y=550)
        tk.Button(t,text="View Memories",command=vm).place(x=760,y=550)
        tk.Button(t,text="Modify today's",command=ee).place(x=960,y=550)
    elif os.path.exists("E:/cipher diary/"+unt)==1:
        clr()
        tk.Button(t,text="Delete Account",command=da).place(x=560,y=550)
        tk.Button(t,text="View Memories",command=vm).place(x=760,y=550)
        tk.Button(t,text="Create New",command=cn).place(x=960,y=550)
    else:
        cn()
def fp():
    clr()
    tk.Label(t,text="Enter your date of birth").place(x=50,y=100)
    calc()
    cal.place(x=80,y=100)
    tk.Button(t,text="next",command=fp1).place(x=960,y=550)
def fp1():
    global pw1,pw2
    cur.execute("select dob from cipher_diary where username='{}'".format(unt))
    cdob=cur.fetchall()
    cdob=str(cdob)[16:-4].replace(', ','-')
    cdob=cdob.split('-')
    if len(cdob[0])!=4:
        cdob[0]=str(0*(4-len(cdob[0])))+cdob[0]
    if len(cdob[1])!=2:
        cdob[1]=str(0*(4-len(cdob[1])))+cdob[1]
    if len(cdob[2])!=2:
        cdob[2]=str(0*(4-len(cdob[2])))+cdob[2]
    cdob='-'.join(cdob)
    print(str(cal.selection_get().strftime("%Y-%m-%d")),(cdob))
    if str(cal.selection_get().strftime("%Y-%m-%d"))==cdob:
        clr()
        tk.Label(t,text="Password").place(x=350,y=250)
        tk.Label(t,text="Retype\nPassword").place(x=350,y=300)
        pw1=tk.Entry(t,width=30,font="Arial 22")
        pw1.place(x=450,y=250)
        pw2=tk.Entry(t,width=30,font="Arial 22")
        pw2.place(x=450,y=300)
        tk.Button(t,text="next",command=fp2).place(x=960,y=550)
    else:
        messagebox.showerror("Warning","Date of birth mismatch")
        t.destroy()
def fp2():
    if pw1.get()==pw2.get():
        if len(pw1.get())>=6:
            cur.execute("update cipher_diary set passwd= '{}' where username ='{}'".format(pw1.get(),unt))
            sql.commit()
            cre()
        else:
            messagebox.showerror("Warning","Password Must be 6 characters")
            fp1()
    else:
        messagebox.showerror("Warning","Password Mismatch")
        fp1()
def cn():
    global st
    clr()
    st= scrolledtext.ScrolledText(t,wrap = tk.WORD,width = 124,height = 30,font = ("Times New Roman",15))
    st.place(x=10,y=10)
    st.focus()
    st.insert(END,"")
    tk.Button(t,text="Finish",command=cn1).place(x=960,y=550)
def cn1():
    encrypt(st.get(1.0, "end-1c"))
    t.destroy()
def vm():
    clr()
    calc()
    cal.place(x=20,y=100)
    Button(t, text = "Next",command = vm1).place(x=100,y=400)
def vm1():
    try:
        with open("E:/cipher diary/"+unt+"/"+str(cal.selection_get().strftime("%Y-%m-%d"))+".txt","r",encoding="utf-8") as file:
            inp=file.read()
        inp=decrypt(inp)
        clr()
        st= scrolledtext.ScrolledText(t,width = 124,height = 30,font = ("Times New Roman",15))
        st.place(x=10,y=10)
        st.insert(tk.INSERT,inp)
        st.configure(state='disabled')
        tk.Button(t,text="Finish",command=t.destroy).place(x=960,y=550)
    except FileNotFoundError:
        yn=messagebox.askyesno("Note","File not found\nChange date ?")
        if yn==1:
            vm()
        else:
            t.destroy()
def ee():
    global st
    with open("E:/cipher diary/"+unt+"/"+str(datetime.date.today())+".txt","r",encoding="utf-8") as file:
        inp=file.read()
    inp=decrypt(inp)
    clr()
    st= scrolledtext.ScrolledText(t,wrap = tk.WORD,width = 124,height = 30,font = ("Times New Roman",15))
    st.place(x=10,y=10)
    st.focus()
    st.insert(END,inp)
    tk.Button(t,text="Finish",command=cn1).place(x=960,y=550)
def da():
    shutil.rmtree('E:/cipher diary/'+unt)
    cur.execute("delete from cipher_diary where username='{}'".format(unt))
    sql.commit()
    t.destroy()
sql=mysql.connect(host="localhost",user="root",passwd="SSS!A!55",database="sss")
cur=sql.cursor()
t=Tk()
video("D:\my projects/num.mov")
t.mainloop()
