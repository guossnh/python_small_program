#-*- coding : utf-8 -*-
#高德地图信息抓取,通过云检索不断抓取高德地图的某类信息.


#导包
import urllib
from urllib import request

#常量 
#洗浴推拿 编号 071400  
#诊所  编号 090300


gaode_key = "5b948aa8ff7778b745c04639d6d4517f"
keywords = ""
gaode_link = ""
goade_link_other_kew = "&offset=50&citylimit=true&types=071400"
city = ""


def getlink():
    pass

def tryit():
    with urllib.request.urlopen(' http://restapi.amap.com/v3/place/text?&keywords=北京大学&city=beijing&output=xml&offset=100&page=1&key=<用户的key>&extensions=all ') as f:
         print(f.read())



#主函数
def main():
    tryit()

if __name__ == '__main__':
    main()