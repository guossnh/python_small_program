#-*- coding : utf-8 -*-
#检测现在的网站 是否可用的一个小程序


#这里是导包
from urllib import request
import json , os , threading , time
from multiprocessing import Process


#程序部分


#这个方法是要检测链接是否是可以访问的
def check_link(link):
    for x in link:
        x = "http://%s"%x   #前边增加"http://" 防止出错
        try:
            with request.urlopen(x) as f:
                date = f.read()
                print("URL:",x)
                print("STATUS:",f.status,f.reason)
        except:
            print("bad request by",x)



def main():
    with open('date.json' , 'r' , encoding="utf8") as f:
        data = json.load(f)
    for x in data['link']:
        print(x)
        check_link([x,"www.%s"%x])




def print_something(name):
    count = 0
    while count < 5:
        count = count + 1





if __name__ == '__main__':
    #main()
    print("ok")
