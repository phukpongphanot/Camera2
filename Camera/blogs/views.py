from django.shortcuts import render, redirect
from django.http import HttpResponse # คือมีการส่งข้อความตอบกลับ ต้องfrom http เข้ามาทำงาน
from django.contrib.auth.models import User,auth # เวลาที่เราจะบันทึกขึ้นมูลที่เกี่ยวข้องกับ models user ต้อง from และ import อันนี้
from django.contrib import messages  #คือการนำข้อความไปแสดงที่ถ้าเว็บเลย ในที่นี้คือเป็นข้อความ errror

from random import randrange
import pymysql
import json
import datetime


from Api import api

# Create your views here.
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
    print("llllllllllllllllllllllllllllllllllllll222")
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
    return render(request,'index.html')



def indext_check(request):
    StudentID = request.POST['id']
    Password = request.POST['pw']
    
    print(StudentID)
    print(Password)

    check = api.get_data_sql("user_info", "id", StudentID)
    print(check[0])
   
    
    if StudentID ==  str(check[0][0]) and Password == check[0][3]:
        api.update_json("user_info", "1", "id", int(StudentID))

        return redirect('/select')

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
    print(type(data)) 
    ran = api.sent_password(str(data))
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
    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data4 = json_obj["app_info"][str(data1)]
    print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
    Number_box = ""
    RFID = ""
    num = 0
    for scan1 in data:
        print(scan1)
        data2 = json_obj["camera_info"][scan1]["camera_status"]
        
        if data2 == "":
            if num == 0:
                data3 = json_obj["camera_info"][scan1]["camera_id"]
                RFID =  str(data3)
                num += 1
                Number_box = scan1
                api.update_json("app_info", str(data1), "camera_id",data3)
                print("yyyyyyyyyyyyyyyyyyyyyyyy")
                print(scan1)
                print("/////////////////////////////////////////////")
                print(data3)
                print("///////////ss///////////////////////////////////444")
                
         
    print("xxxx"+RFID)

    return render(request,'scan.html',{"Number":Number_box,"RFID":RFID})

def done_scan(request):
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    rfid = request.POST['rfid']
    json_obj = api.get_data_json()
    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data4 = json_obj["app_info"][str(data1)]["camera_id"]
    
    print("9999999999999999999999999999999999999999999999999999999999999")
    print(data4)

    if str(rfid) == str(data4): 
        num = 0
        for scan1 in data:
            data2 = json_obj["camera_info"][scan1]["camera_status"]
            if data2 == "":
                if num == 0:
                    data3 = json_obj["camera_info"][scan1]["camera_id"]
                    print("yyyyyyyyyyyyyyyyyyyyyyyy")
                    print(scan1)
                    print("/////////////////////////////////////////////")
                    print(data3)
                    print("///////////////////////////////////////////")
                    api.update_json("camera_info", str(scan1), "camera_status", "borrow")
                    api.update_json("camera_info", str(scan1), "camera_data", date)
                    api.update_json("app_info", str(data1), "action", "borrow")
                    api.update_json("app_info", str(data1), "camera_id",data3)
                    api.update_json("app_info", str(data1), "datetime",date)
        
                    return redirect('/complete_borrow')
    else:
        messages.info(request,'รหัสไม่ถูกต้อง') 
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
    rfid = request.POST['rfid']
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    json_obj = api.get_data_json()
    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data5 = json_obj["app_info"][str(data1)]["camera_id"]
    data7 = json_obj["app_info"]["61340500048"] 
    data4 = json_obj["app_info"][str(data1)]["camera_id"]
    
    if str(rfid) == str(data4): 
        for scan1 in data:
            data3 = json_obj["camera_info"][scan1]["camera_id"]
            if data3 == data5:
                api.update_json("camera_info", str(scan1), "camera_status", "")
                api.update_json("camera_info", str(scan1), "camera_data", date)
                api.update_json("app_info", str(data1), "action", "return")
                # api.update_json("app_info", str(data1), "camera_id","")
                api.update_json("app_info", str(data1), "datetime",date)
                return redirect('/complete_return')
    else:
        messages.info(request,'รหัสไม่ถูกต้อง') 
        return redirect('/scan_return')




def complete_return(request):
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    json_obj = api.get_data_json()
    data = json_obj["camera_info"]
    data1 = json_obj["user_info"]["1"]["id"]
    data4 = json_obj["app_info"][str(data1)]
    data5 = json_obj["app_info"][str(data1)]["camera_id"]
    data7 = json_obj["app_info"]["61340500048"]  
    
    # for scan1 in data:
    #     data3 = json_obj["camera_info"][scan1]["camera_id"]
    #     if data3 == data5:
    #         api.update_json("camera_info", str(scan1), "camera_status", "")
    #         api.update_json("camera_info", str(scan1), "camera_data", date)
    #         api.update_json("app_info", str(data1), "action", "")
    #         api.update_json("app_info", str(data1), "camera_id","")
    #         api.update_json("app_info", str(data1), "datetime",date)
            
    
    data6 = json_obj["app_info"][str(data1)]
    print("----------------------------------")
    print("****************************")
    print(data6)
    print("----------------------------------")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(api.insert_sql("app_info", data6))
    # cursor.execute(api.insert_sql("camerra_info", data6))
    # api.update_json('app_info', "61340500048", "action", 'return')  
    # sql = api.update_sql("app_info", "action", "random_key",data7)
    # cursor.execute(sql)
    db.commit()
    db.close()
    api.update_json("app_info", str(data1), "action", "")
    api.update_json("app_info", str(data1), "camera_id","")

    api.update_json("app_info", str(data1), "datetime","")
            
    # api.update_json('app_info', str(data1), "action", '')
    # api.update_json("app_info", str(data1), "action", "return")
    # data6 = json_obj["app_info"][str(data1)]
    
    
    print("//////////////////////////////////////////")
    print(data4)
    # cursor.execute(api.insert_sql("app_info", data6))
    # cursor.execute(api.update_sql("camera_info", "camera_status", 1))
    

    return render(request,'complete_return.html',{"user":data1,"date":date})












def test(request): #เดียวลองวน for json_obj
    # api.sent_password(str(1))
    json_obj = api.get_data_json()
    data = json_obj["app_info"]["61340500048"]                             # update_sql
    api.update_json('app_info', "61340500048", "action", 'return')          # update_sql 
    print(data)
    # print("ssssssssssssssssssssssssssssssssssssss555")
    # for data1 in data:
    #     print(data1)
    #     print("//////////////////////////////////////")
    #     # data2 = json_obj["app_info"][data1]["random_key"]
    #     print(data2)
 

    # print(data)
    # print("ssssssssssssssssssssssssssssssss")
    # update_json("user_id", "2", "password", 1456)

    # q = get_data_sql("user_info", "id", 61340500048)
    # print(q[0][0])
    
    db = connect_db()
    cursor = db.cursor()
    sql = api.delete_sql("app_info", "id", data)
    
    # sql = api.update_sql("app_info", "action", "camera_id",data)
    # sql = api.insert_sql("camera_info", data)
    cursor.execute(sql)
    db.commit()   
    db.close()

    return render(request,'test.html',{"random":data})

    










