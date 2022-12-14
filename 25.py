import sqlite3
from datetime import datetime
cnt=sqlite3.connect('e:/SHOP.db')
islogin=False
isadmin=False
userid=""
print("open")

##################################################### TABLE users

#sql=''' CREATE TABLE users
   #  (id INTEGER PRIMARY KEY,
    #fname CHAR(20) NOT NULL,
     #lname CHAR(30) NOT NULL,
    #addr CHAR(20) NOT NULL,
    #grade INT(10) NOT NULL,
    #username CHAR(15) NOT NULL,
   #password CHAR(15) NOT NULL,
    #cpassword CHAR(15) NOT NULL,
    #edate CHAR(10) NOT NULL,
    #ncode CHAR(15) NOT NULL,
   #reserve1 CHAR(15) )'''
#cnt.execute(sql)
#print("Table created succssefully")
#cnt.close()

##################################################### TABLE products

#sql=''' CREATE TABLE products
 #    (id INTEGER PRIMARY KEY,
  #   pname CHAR(30) NOT NULL,
   # quantity CHAR(20) NOT NULL,
    #bprice INT(20) NOT NULL,
    #sprice INT(20) NOT NULL,
  # edate CHAR(15) NOT NULL,
   #exdate CHAR(15) NOT NULL,
  # brand CHAR(40) NOT NULL,
   #reserve1 CHAR(20) NOT NULL)'''
#cnt.execute(sql)
#print("Table created succssefully")
#cnt.close()
##################################################### TABLE transactions

#sql=''' CREATE TABLE transactions
 #   (id INTEGER PRIMARY KEY,
  #   uid INT(15) NOT NULL,
   #  pid INT(15) NOT NULL,
    #bdate CHAR(15) NOT NULL,
     #qnt INT(5) NOT NULL,
     #comment CHAR(50) NOT NULL,
   #  reserve1 CHAR(30) )'''
##
#cnt.execute(sql)
#print("Table created succssefully")
#cnt.close()
##################################################### main program

def validation(fname,lname,addr,username,password,cpassword,ncode):
    errorlist=[]
    if(fname=="" or lname=="" or addr=="" or username=="" or password=="" or cpassword=="" or ncode==""):
        msg="please fill all the blanks"
        errorlist.append(msg)
    if(len(password)<8):
        msg="pass length must be at least 8"
        errorlist.append(msg)
    if(password != cpassword):
        msg="pass and confirm mismatch"
        errorlist.append(msg) 
    if(not(ncode.isnumeric())):
        msg="national code shold be numeric"
        errorlist.append(msg)
    sql='select *from users where username=?'
    cursor=cnt.execute(sql,(username,))
    rows=cursor.fetchall()
    if(len(rows)!=0):
        msg='username already exist'
        errorlist.append(msg)
    return errorlist


def submit():
    fname=input("please enter your name?")
    lname=input("please enter your lname?")
    addr=input("please enter your addr?")
    grade=0
    reserve=""
    edate=datetime.today().strftime('%Y-%m-%d')
    username=input("please enter your username?")
    password=input("please enter your password?")
    cpassword=input("please enter your password confirmation?")
    ncode=input("please enter your natinal code?")
    result=validation(fname,lname,addr,username,password,cpassword,ncode)
    if(len(result)>0):
        for err_msg in result:
            print(err_msg)
        return
    
    sql='''INSERT INTO users(fname,lname,addr,grade,username,password,cpassword,edate,ncode,reserve1)\
        VALUES(?,?,?,?,?,?,?,?,?,?)'''
    cnt.execute(sql,(fname,lname,addr,grade,username,password,cpassword,edate,ncode,reserve))            
    cnt.commit()
    print("submit done successfully!")
        
def login():
    global islogin,isadmin,userid
    if (islogin): #if(islogin==True)
        print("you are already logged in")
        return
        
    user=input("please enter your username: ")
    passw=input("please enter your password: ")
    sql=''' SELECT username,id FROM users where username=? AND password=?'''
    cursor=cnt.execute(sql,(user,passw))
    row=cursor.fetchone()
    if(not(row)):
        print("wrong user or pass ")
        return
    print("welcome to your account")
    userid=row[1]
    islogin=True
    if user=="admin":
        isadmin=True

def logout():
    global islogin,isadmin,userid
    islogin=False
    isadmin=False
    userid=""
    print("you are logged out now!")

def mproducts():
    global islogin,isadmin
    if (islogin==False or isadmin==False):
        print("you are not allowed for this action")
        return
    pname=input("product name? ")
    quant=input("quantity? ")
    bprice=int(input("buy price? "))
    sprice=int(input("sell price? "))
    edate=datetime.today().strftime('%Y-%m-%d')
    exdate=""
    brand=input("brand? ")
    reserve=""
    ##################
    sql='''SELECT pname FROM products WHERE pname=?'''
    cursor=cnt.execute(sql,(pname,))
    rows=cursor.fetchall()
    if(len(rows)>0):
        print("product name already exist!! ")
        return
    ##################
    sql='''insert into products (pname,quantity,bprice,sprice,edate,
        exdate,brand,reserve1) VALUES(?,?,?,?,?,?,?,?)'''
    cnt.execute(sql,(pname,quant,bprice,sprice,edate,exdate,brand,reserve))
    cnt.commit()
    print("data inserted successfully!!!")
    
def buy():
    global islogin,userid
    if(not(islogin)):
        print("you are not logged in")
        return
    bdate=datetime.today().strftime('%Y-%m-%d')
    pname=input('products name? ')
    sql='''SELECT * FROM products WHERE pname=?'''
    cursor=cnt.execute(sql,(pname,))
    row=cursor.fetchone()
    if(not(row)):
        print("wrong product name! ")
        return
    print('product:',row[1],' Q:',row[2],' brand:',row[7],' price:',row[4])
    num=int(input("number of products? "))
    if(num<=0):
        print("wrong number!")
        return
    if num>int(row[2]):
        print("not enough numbers of product!")
        return
    
    print('total cost: ',num*row[4])
    confirm=input("are you sure? yes / no")
    if(confirm!='yes'):
        print("canceled by user!")
        return
    newquant=int(row[2]) - num
    
    sql='''UPDATE products SET quantity=? WHERE pname=?'''
    cnt.execute(sql,(newquant,pname))
    
    cnt.commit()
    
    comment=""
    reserve=""
    sql='''INSERT INTO transactions (uid,pid,bdate,qnt,comment,reserve1) 
            VALUES(?,?,?,?,?,?)'''
    cnt.execute(sql,(userid,row[0],bdate,num,comment,reserve))
    cnt.commit()
    print("thanks for your shopping! ")

def plist():
    sql=''' SELECT pname,quantity FROM products WHERE quantity>0 '''
    cursor=cnt.execute(sql)
    rows=cursor.fetchall()
    for row in rows:
        print(row[0],'  Q:',row[1])
        
def alltrc():
    global islogin,isadmin
    if (not(isadmin)):
        print("you are not allowed for this action")
        return
    if (not(islogin)):
        print("you are not logged in")
        return
    sql='''SELECT users.lname,products.pname,transactions.qnt,transactions.bdate FROM transactions INNER JOIN users
        ON transactions.uid=users.id
        INNER JOIN products
        ON transactions.pid=products.id'''
    cursor=cnt.execute(sql)
    for row in cursor:
        print("user:",row[0]," product:",row[1]," QNT:",row[2]," date:",row[3])
    
    

while(True):
    plan=input("please enter your plan?")
    if(plan=="submit"):
        submit()
    elif(plan=="login"):
        login()
    elif (plan=="logout"):
        logout()
    elif(plan=="manage products"):
        mproducts()
    elif (plan=="buy"):
        buy()
    elif (plan=="products list"):
        plist()
    elif(plan=="exit"):
        break
    elif (plan=="all transactions"):
        alltrc()
    else:
        print("wrong input!!")



