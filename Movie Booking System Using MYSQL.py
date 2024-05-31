import mysql.connector
from datetime import datetime, timedelta
import random
from os import system

db = mysql.connector.connect(host="localhost",user="root",passwd="1234")

cursor = db.cursor()
# cursor.execute("drop database if exists project")
cursor.execute("CREATE DATABASE if not exists project")
cursor.execute("use project")
cursor.execute("create table if not exists movie (code int,name varchar(50), details varchar(50), dor date, status varchar(50), show9_12 int,show12_15 int, show15_18 int, show18_21 int, show21_24 int,seat int)")
# cursor.execute("drop table if exists transaction")
cursor.execute("create table if not exists transaction (sno int AUTO_INCREMENT primary key , movie_code int , movie_name char(50) , date_of_show date ,show_time char(50), seat_number int)")
cursor.execute("update movie set status = 'not available' where show9_12 = 0 and show12_15 =0 and show15_18=0 and show18_21 = 0 and show21_24 = 0 ")
def add():
    system('cls')
    print("--<< ADD A MOVIE >>--")
    code      =  input("Enter the new movie code : ")
    name      =  input("Enter the new movie name : ")
    details   =  input("Enter some details about the movie : ")
    dor       =  input("Date of release : ")
    status    =  input("Enter the status : ")
    show9_12  =  input("Enter the status for 9 - 12 show : ")
    show12_15 = input("Enter the status for 12 - 15 show : ")
    show15_18 = input("Enter the status for 15 - 18 show : ")
    show18_21 = input("Enter the status for 18 - 21 show : ")
    show21_24 = input("Enter the status for 21 - 24 show : ")
    seats = "40"
    tupple = (code,name,details,dor,status,show9_12,show12_15,show15_18,show18_21,show21_24,seats)
    sql = "insert into movie values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,tupple)
    db.commit()
    print(cursor.rowcount,"row inserted")
    try:
        input("Press enter to continue")
    except SyntaxError:
        pass

# add()

def date():
    tomorrowsdate = datetime.now() + timedelta(1)
    tomorrowsdate = tomorrowsdate.strftime('%Y-%m-%d')
    return tomorrowsdate
def findseat():
    seatnumber = random.randint(1,40)
    # print("returning",seatnumber)
    return seatnumber

def seatnumber(code,tomsdate,time):
    i=0
    sql = "select movie_code,date_of_show,show_time,seat_number from transaction where movie_code = %s and date_of_show= %s and show_time= %s and seat_number = %s "
    seat = findseat()
    # print(seat)
    while(i<200):
        i=i+1
        # print("in while")
        tupple = (code,tomsdate,time,seat)
        cursor.execute(sql,tupple)
        data = cursor.fetchall()
        if not data:
            return seat
            break 
        else :
            seat=findseat()
    return 0

def show():
    system('cls')
    print("--<< AVAILABLE MOVIES >>--")
    sql=("select code,name,details,dor from movie where status = 'available'")
    cursor.execute(sql)
    result = cursor.fetchall()
    print("{}  {:10} {:20} {}".format("code","name","details","date of release"))
    for x in result: 
            print("{}     {:10} {:20} {}".format(x[0],x[1],x[2],x[3]))
    c = input("enter the code of the movie that you wanna watch : ")
    code = c
    c = (c,)
    # print(c)
    sql="select * from movie where status = 'available' and code = %s"
    cursor.execute(sql,c)
    x=cursor.fetchall()
    # print("x= ",x)
    i = 0 
    j = []
    moviename = x[0][1]
    if x[0][5]==1:
        i=i+1
        a = (i,"9 TO 12",5)
        print(a[0]," ",a[1])
        j.append(a)
    if x[0][6]==1:
        i=i+1
        a = (i,"12 TO 15",6)
        print(a[0]," ",a[1])
        j.append(a)
    if x[0][7]==1:
        i=i+1
        a = (i,"15 TO 18",7)
        print(a[0]," ",a[1])
        j.append(a)
    if x[0][8]==1:
        i=i+1
        a = (i,"18 TO 21",8)
        print(a[0]," ",a[1])
        j.append(a)
    if x[0][9]==1:
        i=i+1
        a = (i,"21 TO 24",9)
        print(a[0]," ",a[1])
        j.append(a)
    c = int(input("Enter the time slot that you would like : "))
    # print(j)
    time = j[c-1][1]
    tomsdate = date()
    # print(tomsdate,time)
    seatno = seatnumber(code,tomsdate,time)
    
    if seatno == 0:
        number = j[c-1][2]
        # print(number)
        if number == 5 :
            sql = "update movie set show9_12 = 0 where code = %s"
        if number == 6 :
            sql = "update movie set show12_15 = 0 where code = %s"
        if number == 7 :
            sql = "update movie set show15_18 = 0 where code = %s"
        if number == 8 :
            sql = "update movie set show18_21 = 0 where code = %s"
        if number == 9 :
           sql = "update movie set show21_24 = 0 where code = %s"        
        xx = (code,)
        # print(xx)
        cursor.execute(sql,xx)
        print("Sorry house full")
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
        show()

    # print("cameback")
    if seatno!=0:
        sql = "insert into transaction(movie_code,movie_name,date_of_show,show_time,seat_number) values (%s,%s,%s,%s,%s)"
        tupp = (code,moviename,tomsdate,time,seatno)
        cursor.execute(sql,tupp)
        db.commit()
        # print(cursor.rowcount,"row inserted")
        print("Your seat number is :",seatno)
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
# show()

while 1 :
    system('cls')
    print("--<< BOOK MY MOVIE >>--\n1. ADD A MOVIE \n2. BOOK A MOVIE \n3. EXIT PROGRAM\n")
    option = int(input("  Enter your choice : "))
    if option == 1:
        add()
    elif option == 2:
        show()
    elif option == 3:
        print("Open to Feedback")
        try:
            input("Press enter to continue")
        except SyntaxError:
            pass
        break
    else :
        print("<< invalid syntax >>")
