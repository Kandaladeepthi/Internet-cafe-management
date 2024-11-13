import sys
import sqlite3
import datetime
import time
import random

d = {}

def connection():
    conn = sqlite3.connect("cyber.db")
    return conn

def user(pc):
    heading()
    print("\n\t\t\t\t\t\t Enter anything")
    print("\t\t\t\t\t\tEnter ‘end’ to exit")
    a = ""
    while a.lower() != 'end':
        a = input()
        conn = connection()
        print("\n\t\t\t\t\t\t YOUR RESPONSE WILL HELP US A LOT")
        print("\n\t\t\t\t\t\t PLEASE ENTER YOUR FEEDBACK:")
        conn.execute("insert into feedback values(?,?)", (pc, input()))
        conn.commit()
        conn.close()

def User_login():
    heading()
    print("\n\t\t\t\t\t\t Login to Continue")
    sno = int(input("\n\t\t\t\t\t\t\t Enter User Number:"))
    pas = input("\t\t\t\t\t\t\t Enter password:")
    conn = connection()
    paid = conn.execute("select logoutTime from history where sno=? and password=?", (sno, pas))
    flag = 0
    for i in paid:
        for j in i:
            if j != None:
                print("User Number Already Used!!")
                flag = 1
                break
        if flag == 1:
            break
    if flag == 0:
        record = conn.execute("select sno,password from history")
        flag = 0
        for i in record:
            if sno in i and pas in i:
                flag = 1
                l_in = datetime.datetime.now()
                print("\n\t\t\t\t\t\t YOU HAVE SUCCESSFULLY LOGGED IN ")
                record1 = conn.execute("select pc_alloted from history where sno=? and password=?", (sno, pas))
                fl = 0
                for i in record1:
                    for j in i:
                        fl = 1
                        hk = j
                        break
                if fl == 1:
                    break
                conn.commit()
                conn.close()
                user(hk)
                conn = connection()
                l_out = datetime.datetime.now()
                time_diff = l_out - l_in
                tsecs = int(time_diff.total_seconds())
                tmins = int(tsecs / 60)
                conn.execute("update history set loginTime=? Where sno=?", (l_in, sno))
                conn.execute("update history set logoutTime=? where sno=?", (l_out, sno))
                conn.execute("update history set timeUsed=? where sno=?", (tsecs, sno))
                conn.execute("update history set money=? where sno=?", (tsecs, sno))
                break
                conn.commit()
                conn.close()
    if flag == 0:
        print("\n\t\t\t\t\t\t Incorrect Login Credentials")
        a = int(input("Enter 1 to Re-enter details and any number to go back:"))
        if a == 1:
            User_login()

def up():
    heading()
    conn = connection()
    name = input("\t\t\t\t\t\t Enter name:")
    ic = int(input("\t\t\t\t\t\t Enter IC number:"))
    record = conn.execute("select remaining from ICcard where ic_number=? and name=?", (ic, name))
    flag = 1
    for i in record:
        for j in i:
            if j != -1:
                k = f(name, ic)
                print("Your Balance=", k)
                print("\n\t\t\t\t\t Enter 1 to add money")
                print("\n\t\t\t\t\t Enter 2 to withdraw")
                ch = int(input("\t\t\t\t\t\t Enter your choice:"))
                if ch == 1:
                    ad = int(input("\t\t\t\t\t\t Enter Money to add:"))
                    k += ad
                    record = conn.execute("update ICcard set balance=? where ic_number=?", (k, ic))
                    print("your balance =", k)
                    time.sleep(3)
                    conn.commit()
                    conn.close()
                elif ch == 2:
                    rem = int(input("\t\t\t\t\t\t Enter Money to remove:"))
                    if rem > k:
                        print("error accessing excess money!!")
                        conn.commit()
                        conn.close()
                        time.sleep(3)
                        ic_op()
                    else:
                        k -= rem
                        record = conn.execute("update ICcard set balance=? where ic_number=?", (k, ic))
                        print("your balance =", k)
                        time.sleep(3)
                        conn.commit()
                        conn.close()
                else:
                    print("Incorrect choice")
            else:
                print("Your Card has been Expired")
                conn.commit()
                conn.close()
            flag = 0
            break
    if flag == 1:
        print("Sorry! You don't have an account !!")
        time.sleep(5)
        conn.commit()
        conn.close()

def bal():
    heading()
    conn = connection()
    print("\n\t\t\t\t\tEnter User's Details")
    name = input("\t\t\t\t\t Enter name:")
    ic = int(input("\t\t\t\t\t Enter IC number:"))
    j = f(name, ic)
    if j == None:
        print("Sorry! You don't have an account !!")
    else:
        print("Your Balance=", j)
    time.sleep(5)
    conn.commit()
    conn.close()

def apply():
    heading()
    conn = connection()
    print("\n\t\t\t\t\t Enter User's Details")
    name = input("\t\t\t\t\t\t Enter name:")
    bal = int(input("\t\t\t\t\t\t Enter deposit:"))
    phno = input("\t\t\t\t\t\t Enter Phone number:")
    record = conn.execute("select ic_number from ICcard where name=? and phno=?", (name, phno))
    flag = 0
    for i in record:
        for j in i:
            if j != None:
                flag = 1
                print("You already have an account with IC number=", j)
                time.sleep(5)
                break
    if flag == 0:
        record = conn.execute("select ic_number from ICcard")
        k = []
        a = random.randint(1, 100000)
        for i in record:
            for j in i:
                if j != None:
                    k.append(j)
        a = check(a, k)
        today = datetime.datetime.now()
        qwe = conn.execute("SELECT DATETIME(?, ?)", (today, '48 hours'))
        for i in qwe:
            for j in i:
                nex = datetime.datetime.strptime(j, '%Y-%m-%d %H:%M:%S')
                break
        conn.execute("insert into ICcard values(?,?,?,?,?,?,?)", (name, a, bal, phno, today, nex, exp(nex, today)))
        print("Congratulations on Creating an IC card with id=", a)
        time.sleep(4)
        conn.commit()
        conn.close()
def f(name, ic):
    conn = connection()
    record = conn.execute("select balance from ICcard where name=? and ic_number=?", (name, ic))
    balance = None
    for i in record:
        for j in i:
            balance = j
            break
    conn.commit()
    conn.close()
    return balance

def exp(exp_date, curr_date):
    if exp_date > curr_date:
        return 1
    return -1

def check(num, existing_nums):
    while num in existing_nums:
        num = random.randint(1, 100000)
    return num

def ic_op():
    heading()
    print("\n\t\t\t\t\t\t 1. Create a New Card")
    print("\t\t\t\t\t\t 2. Update/Add Balance")
    print("\t\t\t\t\t\t 3. Check Balance")
    print("\t\t\t\t\t\t 4. Exit")
    ch = int(input("\t\t\t\t\t\t Enter your choice:"))
    if ch == 1:
        apply()
    elif ch == 2:
        up()
    elif ch == 3:
        bal()
    elif ch == 4:
        return
    else:
        print("Invalid choice")
        ic_op()

def heading():
    print("\n" + "-" * 70)
    print("\t\t\t\t   WELCOME TO CYBER CAFE MANAGEMENT")
    print("-" * 70)

def main_menu():
    heading()
    print("\n\t\t\t\t 1. Login")
    print("\t\t\t\t 2. IC Card Management")
    print("\t\t\t\t 3. Exit")
    ch = int(input("\n\t\t\t\t Enter your choice:"))
    if ch == 1:
        User_login()
    elif ch == 2:
        ic_op()
    elif ch == 3:
        sys.exit()
    else:
        print("Invalid choice")
        main_menu()

if __name__ == "__main__":
    main_menu()
