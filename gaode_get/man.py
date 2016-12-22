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
from collections import Iterable

#常量 
#洗浴推拿 编号 071400  
#诊所  编号 090300
#090700	医疗保健服务	动物医疗场所	动物医疗场所
#090701	医疗保健服务	动物医疗场所	宠物诊所
#090702	医疗保健服务	动物医疗场所	兽医站


#319b295774592eb15f74feb5a116f5ba,a173ef77f76f2573a2f1e1a159af29b5,49986bc0637849b6d083d0329ba98ab8,b596394af04fa0bb6c76b47fbed45295
gaode_key = "acea7c613e9f98becf064f8553cc0e2c"
keywords = ""
gaode_link = ""
goade_link_other_kew = "&offset=50&citylimit=true&types=090702"
city = ""

#打开数据库
conn = sqlite3.connect('gaode.db')

now_link = ""

pagenumber = 1 #这是页面数的标记

city_num = 3152 #这是变量选择城市的标记

this_is_all_num = 0#用于判断次数,判断一个key的话  每天使用次数的话 必须小于1000次


"""
上边是变量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~变态的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
下边是程序
"""



def getlink():
    global now_link , pagenumber , city , goade_link_other_kew , gaode_key
    now_link = "http://restapi.amap.com/v3/place/text?%s&key=%s&city=%s&page=%s"%(goade_link_other_kew,gaode_key,city,pagenumber)
    pagenumber = pagenumber + 1
    return now_link


#把城市的编号存入数据库,调用方法的时候输入rowid 返回对应的城市编号 并且设置当前全局变量 'city' 的值
def get_city_number(number):
    global city , city_num
    c = conn.cursor()
    c.execute("select num from city where rowid = %s" % number)
    data=c.fetchone()
    if data is None:
        print("程序结束了")
        conn.close()
        return None
    else:
        print(data[0])
        city = data[0]
        return data[0]


#通过通过json数据的解析  把每一条数据存入数据库
def do_json():
    global now_link , pagenumber , city_num
    with urllib.request.urlopen(now_link) as f:
        get_json_data = f.read().decode('UTF-8')
        json_data = json.loads(get_json_data)
        json_data_len = len(json_data['pois'])#获取数据长度来控制链接
        if json_data_len > 0:
            for row in json_data['pois']:
                dbadd(row["id"],row["name"],row["type"],row["typecode"],row["biz_type"],row["address"],row["tel"],row["distance"],row["biz_ext"],row["pname"],row["cityname"],row["adname"])
        else:
            print("结束一个城市")
            pagenumber = 1#重置页面号码
            city_num  = city_num + 1
            get_city_number(city_num)


def dbadd(gdid,name,gdtype,typecode,biz_type,address,tel,distance,biz_ext,pname,cityname,adname):
    try:
        conn.execute("insert into pet (gdid,name,gdtype,typecode,biz_type,address,tel,distance,biz_ext,pname,cityname,adname) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(gdid,name,gdtype,typecode,biz_type,address,tel,distance,biz_ext,pname,cityname,adname))
        conn.commit()
    except:
        pass

#主函数
def main():
    global this_is_all_num , pagenumber , city_num
    get_city_number(city_num)
    while (this_is_all_num < 999):
        getlink()
        this_is_all_num = this_is_all_num + 1 #控制计数保证总数量小于1000
        do_json()#执行方法
    print("结束标记  城市rownum = '%s'  页面编号 = '%s'" %(city_num , pagenumber))
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

    with open('date.json', 'r' , encoding="utf8") as f:
     data = json.load(f)
     print(len(data['pois']))
     for row in data['pois']:
         dbadd(row["id"],row["name"],row["type"],row["typecode"],row["biz_type"],row["address"],row["tel"],row["distance"],row["biz_ext"],row["pname"],row["cityname"],row["adname"])
"""