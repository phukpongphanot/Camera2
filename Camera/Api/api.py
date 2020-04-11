from random import randrange
import pymysql
import json
import datetime

import sys, os
path2jsonn = sys.path.append('C:\\Users\\User\\Desktop\\fra241\\Camera\\Api\\data.json')
path2json = 'C:/Users/User/Desktop/fra241/Camera/Api/data.json'
def get_data_json():
    with open(path2json, 'r', encoding="utf-8") as f:
        json_obj = json.load(f)
    return json_obj

def get_data_sql(table_name, key, value):
    db = connect_db()
    cursor = db.cursor()
    sql_select_query = "SELECT * FROM `{table}` WHERE {key} = {value}".format(table=table_name,
                                                                              key=key.upper(), value=value)
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    return record

def get_data_sql1(table_name):
    db = connect_db()
    cursor = db.cursor()
    sql_select_query = "SELECT * FROM `{table}` ".format(table=table_name)
                                                                        
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    return record




def insert_json(place, item):
    """
    @param place: location you want to add item in. Such as in "user_id" , in "{some id}", in "{some id's personal}"
    or in "{wherever in json_obj}" by adding list of keys to this parameter example ["user_id", "2"]
    @param item: things that you want to add. However, Please be careful about the data-type.
    example code: insert_json(["user_id","2","personal"], {"university":"Fibo"})
    this will add new type of details to "2"'s personal.
    Former "2"'s personal have "age" and "sex" but now it'll have "university" with value="Fibo"
    """
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa44")
    json_obj = get_data_json()
    print("vvvvvvvvvvvvvvvvvvvvvv4444vvvvvvvvvvvvvvvvvvvvvv444vvv")
    print(json_obj)
    new_json_obj= json_obj
    print(new_json_obj)
    print(len(place))
    if len(place) == 1:
        json_obj[place[0]].update(item)
        print("ppppppppppppppppppppppppppp5555ppppppppppppppppppppppppp")
        print(json_obj)
        print(new_json_obj)
    elif len(place) == 2:
        json_obj[place[0]][place[1]].update(item)
    elif len(place) == 3:
        json_obj[place[0]][place[1]][place[2]].update(item)
    elif len(place) == 4:
        json_obj[place[0]][place[1]][place[2]][place[3]].update(item)
    else:
        print("too much")

    file = open(path2json, "w", encoding="utf-8")
    json.dump(json_obj, file, indent=4)
    file.close()

def insert_sql(table_name, value_json):
    sql = ""
    if table_name == 'app_info':
        sql = "INSERT INTO `app_info` ( `ID`, `ACTION`, `DATETIME`, `CAMERA_ID`, `RANDOM_KEY`) \
         VALUES ('%s', '%s', '%s', '%s', '%s')" % \
              ( value_json["id"], value_json["action"], value_json["datetime"],
               value_json["camera_id"], value_json["random_key"])
    elif table_name == 'user_info':
        sql = "INSERT INTO `user_info` (`ID`, `FIRST_NAME`, `LAST_NAME`, `PASSWORD`, `TYPE_USER`, `STATUS`,`TEL`,`HISTORY`) \
         VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %\
              (value_json["id"], value_json['first_name'], value_json["last_name"], value_json['password'], value_json["type_user"],
               value_json["status"], value_json["tel"], value_json["history"])
    elif table_name == 'camera_info':
        sql = "INSERT INTO `camera_info` (`CAMERA_ID`, `CAMERA_STATUS`, `CAMERA_DATA`) \
                 VALUES ('%d', '%s', '%s')" % \
              (value_json["camera_id"], value_json["camera_status"], value_json["camera_data"])
    return sql


def delete_json(type_user, ids):
    """
    delete entire id data
    @param type_user: "user_id" or "admin_id"
    @param ids: "1" "2"...
    @return: None
    """
    json_obj = get_data_json()
    del json_obj[type_user][ids]

    file = open(path2json, "w", encoding="utf-8")
    json.dump(json_obj, file, indent=4)
    file.close()


def update_json(type_user, ids, key, value):
    """
    @param type_user: "user_id" or "admin_id"
    @param ids: id of data you want to access
    @param key: what categories you want to change
    @param value: new value
    example code: update_json("user_id", "2", "password", 2002)
    this line of code changes password of data id "2" to 2002
    """
    json_obj = get_data_json()
    json_obj[type_user][ids][key] = value
    file = open(path2json, "w", encoding="utf-8")
    json.dump(json_obj, file, indent=4)
    file.close()


def connect_db():
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='a',
                          db='pj_camera')
    return con









def delete_sql(table_name, delete, value_json):
    sql = "DELETE FROM `{table}` WHERE {delete_what}={value}".format(table=table_name, delete_what=delete.upper()
                                                                      ,value=value_json[delete])
    return sql


def sent_password(ids):
    """
    save random password to json and mysql then return password
    @param ids: id of user you want to send him password
    @return: password
    """
    random_key = randrange(100000, 1000000)
    print(random_key)
    update_json("app_info", ids, "random_key", random_key)
    json_obj = get_data_json()
    data = json_obj["app_info"][ids]
    db = connect_db()
    try:
        cursor = db.cursor()
        cursor.execute(update_sql("app_info", "random_key",data))
        db.commit()
        
    except :
        print('error')
        db.rollback()
    db.close()

    return random_key


def register_user(data):
    print("bbbbbbbbbbbbbbbbbbbbbbbbbbb")

    if not get_data_sql('user_info', "ID", str(data[0])):
        type_id = ""
        if data[0:3] == "999" and data[-4:-1] == "999":
            type_id = "admin_id"
        else:
            type_id = "user_id"
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        json_obj = {
                    "id": str(data[0]),
                    "first_name": data[1],
                    "last_name": data[2],
                    "password": data[4],
                    "type_user": type_id,
                    "status": "init",
                    "tel": data[3],
                    "history": "register at " + str(date)
        }
        json_obj1 = {
                    "id": str(data[0]),
                    "action": "",
                    "datetime": str(date),
                    "password": data[4],
                    "camera_id": "",
                    "random_key": "",
                    
        }

        
        insert_json(["user_info"], {str(data[0]): json_obj})
        insert_json(["app_info"], {str(data[0]): json_obj1})
        
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(insert_sql("user_info", json_obj))
        
        db.commit()
        db.close()

def update_sql(table_name, update, key, value_json):
    sql = "UPDATE `{table}` SET {update_what}=\"{update_value}\" WHERE {x} = \"{y}\"".format(table=table_name,update_what=update.upper(),
                                                                                 update_value=value_json[update], x=key.upper(),
                                                                                 y=str(value_json[key]))
    return sql