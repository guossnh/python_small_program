#-*- coding : utf-8 -*-
# by tlk
#高德地图信息抓取,通过云检索不断抓取高德地图的某类信息.
"""
主意:高德地图如果按照市一级别来拿数据的话,只能拿到18页
"""

#导包
import urllib
from urllib import request
import sqlite3
import json
import csv

#常量 
#洗浴推拿 编号 071400  
#诊所  编号 090300

#  c07150c4cb806794cd91568a83056720,5b948aa8ff7778b745c04639d6d4517f
gaode_key = "5b948aa8ff7778b745c04639d6d4517f"
keywords = ""
gaode_link = ""
goade_link_other_kew = "&offset=50&citylimit=true&types=071400"
city = ""

#打开数据库
conn = sqlite3.connect('gaode.db')

now_link = ""

pagenumber = 1



"""
上边是变量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~变态的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
下边是程序
"""



def getlink():
    global now_link
    now_link = "http://restapi.amap.com/v3/place/text?%s&key=%s&city=%s&page=%s"%(goade_link_other_kew,gaode_key,city,pagenumber)
    return now_link


#把城市的编号存入数据库,调用方法的时候输入rowid 返回对应的城市编号 并且设置当前全局变量 'city' 的值
def get_city_number(number):
    global city
    data = conn.execute("select num from city where rowid = %s" % number)
    for row in data:
        city = row[0]
        return row[0]

def tryit():
    with urllib.request.urlopen('  ') as f:
         print(f.read())


#通过通过json数据的解析  把每一条数据存入数据库
def do_json():
    with open('date.json', 'r' , encoding="utf8") as f:
        data = json.load(f)
        print(len(data['pois']))
        # for row in data['pois']:
        #     dbadd(row["id"],row["name"],row["type"],row["typecode"],row["biz_type"],row["address"],row["tel"],row["distance"],row["biz_ext"],row["pname"],row["cityname"],row["adname"])
        


def dbadd(gdid,name,gdtype,typecode,biz_type,address,tel,distance,biz_ext,pname,cityname,adname):
    try:
        conn.execute("insert into gaode (gdid,name,gdtype,typecode,biz_type,address,tel,distance,biz_ext,pname,cityname,adname) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(gdid,name,gdtype,typecode,biz_type,address,tel,distance,biz_ext,pname,cityname,adname))
        conn.commit()
        print("add one")
    except:
        print("not add")
    



#主函数
def main():

    #conn.close()
    #do_json();
    getlink()
    print(get_city_number(2))
    conn.close()


if __name__ == '__main__':
    main()




"""
下边是保存的旧方法
    with open('city.csv','r',encoding="utf8") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            conn.execute("insert into city (num) values (%s)" % row[0])
        conn.commit()
"""