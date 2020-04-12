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
    print("llllllllllllllllllllllllllllllllllllll22233")
    print( para_register)
    
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
    print("******************************************")
    
    for i in range(1,3):
        s = data[str(i)]["camera_status"]
        print(s)
        if s == "borrow":
            Dis += 1
    print("******************************************")
    return render(request,'index.html',{"Dis":Dis})



def indext_check(request):
    StudentID = request.POST['id']
    Password = request.POST['pw']
    # json_obj = api.get_data_json()
    # data = json_obj["user_info"][StudentID]
    print(StudentID)
    print(Password)

    check = api.get_data_sql("user_info", "id", StudentID)
    print("////////////////////")
    # print(check[0])
    check1 = api.get_data_sql1("user_info")
    for i in check1:
        print(i[0])
    # print(Password)
    # print(check[0][3])
    print("////////////////////")
   

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
    print("bbbbbbbbbbbbbbbbbbbbbb")
    print("print")
    json_obj = api.get_data_json()
    data = json_obj["user_info"]["1"]["id"]
    print(type(data)) 
    ran = api.sent_password(str(data))
    return render(request,'borrow.html',{"random":ran})

def Return(request):
    
    json_obj = api.get_data_json()
    data = json_obj["user_info"]["1"]["id"]
    data1 = json_obj["app_info"][str(data)]["action"]
    print("*****************")
    print((data)) 
    print("*************************")
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
        print(data1)
        print("//////////////////////////////////////")
        
        data2 = json_obj["app_info"][data1]["random_key"]
        print(data2)
        print("############################################################3")
        if str(data2) == str(key):
            print("key ="+str(data2))
            print("//////////////////////////"+" "+str(data2))
            if str(data3) == "":
                print("passssssssssssssssssssssssssssssssssssssssss")
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
    print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
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
                # api.update_json("camera_info", str(scan1), "camera_status", "borrow")
                # api.update_json("camera_info", str(scan1), "camera_data", date)
                # api.update_json("app_info", str(data1), "action", "borrow")
                # api.update_json("app_info", str(data1), "camera_id",data3)
                # api.update_json("app_info", str(data1), "datetime",date)
                
                        
    # if Number_box == "":
    #     Number_box = "FULL"
    # print("xxxx"+RFID)

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
    
    for scan1 in data:
        data2 = json_obj["camera_info"][scan1]["camera_status"]
        if data2 == "":
                data3 = json_obj["camera_info"][scan1]["camera_id"]
                if data3 == arduino:
                    api.update_json("camera_info", str(scan1), "camera_status", "borrow")
                    api.update_json("camera_info", str(scan1), "camera_data", date)
                    api.update_json("app_info", str(data1), "action", "borrow")
                    api.update_json("app_info", str(data1), "camera_id",data3)
                    api.update_json("app_info", str(data1), "datetime",date)
                    return redirect('/complete_borrow')
    
    
    messages.info(request,'***scan please***') 
    return redirect('/scan')


def complete_borrow(request):
    json_obj = api.get_data_json()
    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data4 = json_obj["app_info"][str(data1)]
    
    data5 = json_obj["app_info"][str(data1)]["camera_id"]
    # data6 = json_obj["camera_info"][str(data5)]
    print("----------------------------------")
    print(data5)
    print("----------------------------------")
    db = connect_db()
    cursor = db.cursor()
    for check in data:
        data2 = json_obj["camera_info"][check]["camera_status"]
        data6 = json_obj["camera_info"][check]
        if data2 == "borrow":
            cursor.execute(api.insert_sql("app_info", data4))
            cursor.execute(api.insert_sql("camera_info", data6))
    # cursor.execute(api.update_sql("camera_info", "camera_status", 1))
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
    
    
    for scan1 in data:
        data3 = json_obj["camera_info"][scan1]["camera_id"]
        if arduino == data5:
            api.update_json("camera_info", str(scan1), "camera_status", "return")
            api.update_json("camera_info", str(scan1), "camera_data", date)
            api.update_json("app_info", str(data1), "action", "return")
            # api.update_json("app_info", str(data1), "camera_id","")
            api.update_json("app_info", str(data1), "datetime",date)
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
   
    print("----------------------------------")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(api.insert_sql("app_info", data6))
    for i in range(1,3):
        
        s = data[str(i)]
        
        if arduino == str(data6["camera_id"]) == s["camera_id"]:
            
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

    










