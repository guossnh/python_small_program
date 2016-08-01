#-*- coding : utf-8 -*-
#检测现在的网站 是否可用的一个小程序


#这里是导包
from urllib import request
import json , os , threading , urllib
from multiprocessing import Process


#程序部分
mark = []

#这个方法是要检测链接是否是可以访问的
def check_link(link):
    global mark
    for x in link:
        x = "http://%s"%x   #前边增加"http://" 防止出错
        try:
            with request.urlopen(x) as f:
                date = f.read()
                #print("URL:",x)
                #print("STATUS:",f.status,f.reason)
                if f.status != 200:
                    mark.append(x)
        except:
            #print("bad request by",x)
            mark.append(x)


def main():#区分一下  手机上边 打不开本地文件  就访问远程连接  电脑上边 就直接使用本地的文件
    global mark
    print("waiting...........")
    try:#电脑上边打开
        with open('date.json' , 'r' , encoding="utf8") as f:
            data = json.load(f)
            for x in data['link']:
               check_link([x,"www.%s"%x])
    except:#电脑上边出错,然后打开链接
        with urllib.request.urlopen("http://guowenzhuo.sinaapp.com/work/date.json") as f:
            get_json_data = f.read().decode('UTF-8')
            json_data = json.loads(get_json_data)
            for x in json_data['link']:
                check_link([x,"www.%s"%x])
    for x in mark:
        print("bad request by",x)

    
if __name__ == '__main__':
    main()
