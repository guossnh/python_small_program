#-*- coding : utf-8 -*-
#高德地图信息抓取,通过云检索不断抓取高德地图的某类信息.


#导包
import urllib
from urllib import request
import sqlite3

#常量 
#洗浴推拿 编号 071400  
#诊所  编号 090300


gaode_key = "5b948aa8ff7778b745c04639d6d4517f"
keywords = ""
gaode_link = ""
goade_link_other_kew = "&offset=50&citylimit=true&types=071400"
city = ""

conn = sqlite3.connect('gaode.db')


"""
上边是变量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~变态的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
下边是程序
"""




def getlink():
    pass

def tryit():
    with urllib.request.urlopen(' http://restapi.amap.com/v3/place/text?&keywords=北京大学&city=beijing&output=xml&offset=100&page=1&key=<用户的key>&extensions=all ') as f:
         print(f.read())


def dbadd(id,name,type,typecode,biz_type,address,tel,distance,biz_ext,pname,cityname,adname):
    conn.execute("insert into gaode (id,name,type,typecode,biz_type,address,tel,distance,biz_ext,pname,cityname,adname) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(id,name,type,typecode,biz_type,address,tel,distance,biz_ext,pname,cityname,adname))
    conn.commit()


#主函数
def main():
    conn = sqlite3.connect('gaode.db')
    dbadd("B000A88EEK", "艺海国际商务会馆(联想桥店)", "生活服务;洗浴推拿场所;洗浴推拿场所","071400","", "皂君庙路2号","010-62166216", "","", "北京市", "北京市", "海淀区")
    conn.close()

if __name__ == '__main__':
    main()
