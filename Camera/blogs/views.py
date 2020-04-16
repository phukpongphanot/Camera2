from django.shortcuts import render, redirect
from django.http import HttpResponse # คือมีการส่งข้อความตอบกลับ ต้องfrom http เข้ามาทำงาน
from django.contrib.auth.models import User,auth # เวลาที่เราจะบันทึกขึ้นมูลที่เกี่ยวข้องกับ models user ต้อง from และ import อันนี้
from django.contrib import messages  #คือการนำข้อความไปแสดงที่ถ้าเว็บเลย ในที่นี้คือเป็นข้อความ errror

from random import randrange
import pymysql
import json
import datetime
import serial

from Api import api



g = ""
sendata = serial.Serial('COM3', 9600)
connect = False

while not connect:
    a = sendata.read()
    print(a)
    connect = True
print("Ready")

def led_on1():
    sendata.write("A".encode())
    print("Led_On")  
    # print(sendata.read())

def led_on2():
    sendata.write("B".encode())
    print("Led_On")  
    # print(sendata.read())

def led_off1():
    sendata.write("C".encode())
    print("Led_Off")
    print(sendata.read())

def led_off2():
    sendata.write("D".encode())
    print("Led_Off")
    print(sendata.read())




def connect_db():
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='',
                          db='pj_camera')
    return con

 

def register(request):
    return render(request,'register.html')

def addregister(request):
    StudentID = request.POST['id']
    FirstName = request.POST['name']
    LastName = request.POST['surname']
    Number = request.POST['number']
    Password = request.POST['password']
    RePassword = request.POST['confirm_password']
    para_register = [StudentID,FirstName,LastName,Number,Password]
    
    
    if not api.get_data_sql('user_info', "ID", StudentID):
        api.register_user(para_register)
        return render(request,'done_register.html',{"id":StudentID})
    else:
        messages.info(request,'Student ID นี้มีผู้ใช้แล้ว')     
        return redirect('/register')
    

def done_register(request):
    return render(request,'done_register.html')

   
def index(request):
    json_obj = api.get_data_json()
    data = json_obj["camera_info"]
    Dis = 0
    
    for i in range(1,3):
        s = data[str(i)]["camera_status"]
        
        if s == "borrow":
            Dis += 1
    
    return render(request,'index.html',{"Dis":Dis})



def indext_check(request):
    StudentID = request.POST['id']
    Password = request.POST['pw']
    
    check = api.get_data_sql("user_info", "id", StudentID)
    check1 = api.get_data_sql1("user_info")
    
    for i in check1:
        if i[0] ==  StudentID:
            
            if StudentID ==  str(check[0][0]) and Password == check[0][3]:
                api.update_json("user_info", "1", "id", int(StudentID))
                return redirect('/select')

            else:
                messages.info(request,'ข้อมูลไม่ถูกต้อง')
      
                return redirect('/index')
    else:
        messages.info(request,'ข้อมูลไม่ถูกต้อง')
        return redirect('/index')


def select(request):

    return render(request,'select.html')


def borrow(request):
    
    json_obj = api.get_data_json()
    data = json_obj["user_info"]["1"]["id"]
    ran = api.sent_password(str(data))
    return render(request,'borrow.html',{"random":ran})

def Return(request):
    
    json_obj = api.get_data_json()
    data = json_obj["user_info"]["1"]["id"]
    data1 = json_obj["app_info"][str(data)]["action"]
    if data1 == "borrow":
        ran = api.sent_password(str(data))
    else:
        ran = "No borrowing"

    return render(request,'return.html',{"random":ran})

#ส่วน user
#-----------------------------------------------------------------------------------------------------------------------------------
#ส่วน server


def enter(request):
    return render(request,'enter.html')

def enter_b(request):
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    password3 = request.POST['password3']
    password4 = request.POST['password4']
    password5 = request.POST['password5']
    password6 = request.POST['password6']
    print("ttttttttttttttttttttttttttttttt")
    key = str(password1)+str(password2)+str(password3)+str(password4)+str(password5)+str(password6)
    print(key)
    
    json_obj = api.get_data_json()
    data = json_obj["app_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data3 = json_obj["app_info"][str(data1)]["action"]
   
    for data1 in data:
    
        data2 = json_obj["app_info"][data1]["random_key"]
        
        if str(data2) == str(key):
            
            if str(data3) == "":
                return redirect('/scan')
            if str(data3) == "borrow":
                return redirect('/scan_return')

    messages.info(request,'รหัสไม่ถูกต้อง')  
    return redirect('/enter')


def scan(request):
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    json_obj = api.get_data_json()

    json_obj1 = api.get_data_json1()
    arduino = json_obj1["camera_id"]  

    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data4 = json_obj["app_info"][str(data1)]

    Number_box = ""
    RFID = ""
    
    for scan1 in data:
        print(scan1)
        data2 = json_obj["camera_info"][scan1]["camera_status"]
        if data2 == "":
            data3 = json_obj["camera_info"][scan1]["camera_id"]
            if data3 == arduino:
                
                RFID =  str(data3)
                
                Number_box = scan1
              

    return render(request,'scan.html',{"Number":Number_box,"RFID":RFID})

def done_scan(request):
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    json_obj1 = api.get_data_json1()
    arduino = json_obj1["camera_id"]  

    json_obj = api.get_data_json()
    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data4 = json_obj["app_info"][str(data1)]["camera_id"]

    print("********  Wait RFID   *************")
    con = False
    G = ""
    g = ""
    while not con:
        G = str(sendata.readline())
        for i in G:
            # print(i)
            if i.isdigit():
                g = G
                break
            else:
                g = ""
        if g != "":
            # print(g)
            con = True

    g = g[2:-5]
    print(g)

    
    for scan1 in data:
        data2 = json_obj["camera_info"][scan1]["camera_status"]
        if data2 == "":
                data3 = json_obj["camera_info"][scan1]["camera_id"]
                # if data3 == arduino:
                if data3 == g:
                    api.update_json("camera_info", str(scan1), "camera_status", "borrow")
                    api.update_json("camera_info", str(scan1), "camera_data", date)
                    api.update_json("app_info", str(data1), "action", "borrow")
                    api.update_json("app_info", str(data1), "camera_id",data3)
                    api.update_json("app_info", str(data1), "datetime",date)
                    
                    if g == "185:75:154:153:241":
                        led_on1()
                    elif g == "172:72:101:163:34":
                        led_on2()
                    return redirect('/complete_borrow')

    
    
    messages.info(request,'***scan please***') 
    return redirect('/scan')


def complete_borrow(request):
    json_obj = api.get_data_json()
    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data4 = json_obj["app_info"][str(data1)]
    
    data5 = json_obj["app_info"][str(data1)]["camera_id"]
    

    db = connect_db()
    cursor = db.cursor()
    for check in data:
        data2 = json_obj["camera_info"][check]["camera_status"]
        data6 = json_obj["camera_info"][check]
        if data2 == "borrow":
            cursor.execute(api.insert_sql("app_info", data4))
            cursor.execute(api.insert_sql("camera_info", data6))
   
    db.commit()
    db.close()
    return render(request,'complete_borrow.html',{"user":data1,"id_camera":data5})

def scan_return(request):
    json_obj = api.get_data_json()
    data1 = json_obj["user_info"]["1"]["id"]
    data4 = json_obj["app_info"][str(data1)]["camera_id"]

    return render(request,'scan_return.html',{"RFID":data4})

def done_scan_return(request):
    json_obj1 = api.get_data_json1()
    arduino = json_obj1["camera_id"]  

    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    json_obj = api.get_data_json()
    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data5 = json_obj["app_info"][str(data1)]["camera_id"]
    data7 = json_obj["app_info"]["61340500048"] 
    data4 = json_obj["app_info"][str(data1)]["camera_id"]

    print("********  Wait RFID   *************")
    con = False
    G = ""
    g = ""
    while not con:
        G = str(sendata.readline())
        for i in G:
            # print(i)
            if i.isdigit():
                g = G
                break
            else:
                g = ""
        if g != "":
            # print(g)
            con = True

    g = g[2:-5]
    print(g)

    
    
    for scan1 in data:
        data3 = json_obj["camera_info"][scan1]["camera_id"]
        # if arduino == data5:
        if g == data5 == data3:
            api.update_json("camera_info", str(scan1), "camera_status", "return")
            api.update_json("camera_info", str(scan1), "camera_data", date)
            api.update_json("app_info", str(data1), "action", "return")
            api.update_json("app_info", str(data1), "datetime",date)
            if g == "185:75:154:153:241":
                led_off1() 
            elif g == "172:72:101:163:34":
                led_off2()
            return redirect('/complete_return')

    messages.info(request,'รหัสไม่ถูกต้อง') 
    return redirect('/scan_return')




def complete_return(request):
    json_obj1 = api.get_data_json1()
    arduino = json_obj1["camera_id"]  
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    json_obj = api.get_data_json()
    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data4 = json_obj["app_info"][str(data1)]
    data5 = json_obj["app_info"][str(data1)]["camera_id"]
    data7 = json_obj["app_info"]["61340500048"]  
    data6 = json_obj["app_info"][str(data1)]
   
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(api.insert_sql("app_info", data6))
    for i in range(1,3):
        
        s = data[str(i)]
        
        if str(data6["camera_id"]) == s["camera_id"]:
            
            print(s)
            cursor.execute(api.insert_sql("camera_info", s))
            api.update_json("camera_info", str(i), "camera_status", "")

    db.commit()
    db.close()
    api.update_json("app_info", str(data1), "action", "")
    api.update_json("app_info", str(data1), "camera_id","")
    api.update_json("app_info", str(data1), "datetime","")
    
    return render(request,'complete_return.html',{"user":data1,"date":date})


def test(request): 
    # api.sent_password(str(1))
    json_obj = api.get_data_json()
    data = json_obj["app_info"]["185:75:154:153:241"]                   # update_sql
    api.update_json('app_info', "61340500048", "action", '')          # update_sql 
    print(data)
    
    
    db = connect_db()
    cursor = db.cursor()
    # sql = api.delete_sql("app_info", "id", data)
    # sql = api.delete_sql("camera_info", "camera_id", data)
    sql = api.update_sql("camera_info", "camera_id", key, value_json)   
    
    cursor.execute(sql)
    db.commit()   
    db.close()

    return render(request,'test.html',{"random":data})

    










