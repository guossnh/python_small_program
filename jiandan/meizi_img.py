#-*- coding : utf-8 -*-
#这是一个爬取  jiandan.net/ooxx  页面图片的爬虫  


#导包
from urllib import request
import urllib ,sqlite3 , requests , time
from bs4 import BeautifulSoup


#变量 
path = "F:\\jiandan_meizi\\"#保存路径
conn = sqlite3.connect('jiandan.db')#数据库初始化
page_link = ""
page_num = 2078

headers  = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36","Cookie":"1872800009=4988oUO1pdCDBF2%2FKuMWTULOBwZzQPr91V5A6Pl%2FUw; gif-click-load=off; PHPSESSID=1j5puhsjmp85ea37r24hn4ede6; _gat=1; 1872800009=47ddkORRjr5%2BsXUMa3ep%2FG9Nnvcu6K7MHrSMCmHN; jdna=596e6fb28c1bb47f949e65e1ae03f7f5#1470300304802; Hm_lvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1470015381; Hm_lpvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1470300305; _ga=GA1.2.881185352.1470015381","Pragma":"no-cache","Accept-Language":"zh-CN,zh;q=0.8,fr-FR;q=0.6,fr;q=0.4","Accept-Encoding":"gzip, deflate, sdch"}

#程序部分


#主要用于保存图片
def save_img(url):
    global path
    #分割字符串 提取文件名
    filename = url.split("/")[-1]
    try:
        data = request.urlopen(url).read()
        File = open(path+filename,"wb")
        File.write(data)
        File.close()
    except:
        pass#这是一个错误日志文件


#jiandan的页面生成器
def make_link():
    global page_num , page_link
    link_head = "http://jandan.net/ooxx/page-%s#comments"%(page_num)
    page_num = page_num - 1
    return link_head
    #下边 这种写法 更吊  一条代码  抗 上边 3条代码
    #return "http://jiandan.net/ooxx/page_%s#comments"%(page_num = page_num - 1)


#将链接保存到数据库里边
def dbadd(link):
    global conn
    try:
        conn.execute("insert into jiandan (link) values ('%s')" %(link))
        conn.commit()
    except:
        pass


def get_content():
    global page_num
    try:
        list_page = requests.get(make_link(),headers = headers)
        page_content = BeautifulSoup(list_page.text , "html5lib")
        print(list_page)
    except:
        print("worong")
        page_num = page_num + 1
    
    for x in page_content.find_all("a",class_ = "view_img_link"):
        img_link=x.get('href')
        dbadd(img_link)

#获取数据并且存到数据库
def get_link_to_db():
    global conn
    num = 0
    while num < 2078:
        get_content()
        num = num + 1
        print(num,"页")
    conn.close()


def get_all_num_db():
    global conn
    c = conn.cursor()
    c.execute("select count(*) from jiandan ")
    data=c.fetchone()
    return data[0]




def save_img_to_pc():#用于保存数据库中的链接
    global conn
    c = conn.cursor()
    for x in range(get_all_num_db()):
        c.execute("select * from  jiandan where rowid = '%s' " % x)
        data=c.fetchone()
        if data is None:
            pass#没数据的话 不处理
        else:
            save_img(data[0])
    conn.close()
    


def main():
    #get_link_to_db()
    #save_img_to_pc()
    pass


if __name__ == '__main__':
    main()