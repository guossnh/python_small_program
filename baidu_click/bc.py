#更新一下 百度点击 的程序  需要增加 一些功能 
#  关键词 用户 自己 添加  更改 这次 努力 完善一下 

#-*- coding : utf-8 -*-


#还是导包  真JB烦人  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time #导入时间包
import random #导入随机数包
import string #导入string包
import urllib
import binascii
import csv  #引入csv文件

#这里放一些变量
kewword = ""

baiduTitle = kewword + "_百度搜索"

driver = ""#= webdriver.Firefox()#确定浏览器

profile = ""#设置浏览器基本设置

#代理的两个变量  用于 计数
all_use_ip = 0
can_use_ip = 0

#这里是百度 翻页 的数字  写在这里   方便控制   第一个是方法1  第二个 是方法2
baidupagenumber1 = 5
baidupagenumber2 = 5

#两个变量设置代理的ip和端口
bc_ip = ""
bc_proxy = ""

#firefox 用户配置文件地址
profileDir = "C:\\Users\\Administrator\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\witrfxpv.default"

"""
下边是方法部分
"""

"""
这是 设置 代理的两个方法
""" 

#设置火狐浏览器的代理的办法,非常好用.得区分一下是不是https的链接
def setHttpsProxy(ip,port):#参数  ip地址   端口  类型   真为https 假为http
    global driver , profile#全局变量
    profile = webdriver.FirefoxProfile(profileDir)
    try:
        profile.set_preference('network.proxy.type', 1)#设置浏览器上完方式为手动
        #if 1==1:
        profile.set_preference('network.proxy.ssl', ip)
        profile.set_preference('network.proxy.ssl_port', port)
        #else:
        #    profile.set_preference('network.proxy.http', ip)
        #    profile.set_preference('network.proxy.http_port', port)
        profile.update_preferences()
        driver = webdriver.Firefox(profile)
        return True;
    except:
        return False;

def tryproxy():
    global all_use_ip , can_use_ip , bc_ip , bc_proxy
    all_use_ip = all_use_ip + 1 
    data = ''
    with urllib.request.urlopen('http://qsrdk.daili666api.com/ip/?tid=556258590050521&num=1&category=2&protocol=https&foreign=none&filter=on') as f:
        data = f.read().decode()
    proxy_handler = urllib.request.ProxyHandler({'https': data})
    proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    try:
        wocao = opener.open('https://baidu.com')#测试链接是否可用
        print("链接正确")
        if wocao.status == 200:
            can_use_ip = can_use_ip + 1
            datalist = data.split(":")
            print("代理查找完毕,开始 设置浏览器代理")
            bc_ip = datalist[0]
            bc_proxy = datalist[1]
            return True
            #setHttpsProxy(datalist[0],datalist[1])
        else:
            return False
    except:
        time.sleep(3)
        print("链接出错")
        return False
    print("总共检测ip为%s可用ip为%s"% (all_use_ip,can_use_ip))




#这个方法主要是页面移动停留的办法   想想我觉得这个方法是骗自己的 https的代理  不是 http的代理
def pageReader():
    global driver#全局变量
    time.sleep(3) #先休息3秒防止出错
    num = 180   #固定值是180根据百度搜多搜索页面高度1879
    for x in range(1,int(random.uniform(4,10))): #循环  设置循环表示要跳转几次. 上线 的话 可以多添加 几次
        time.sleep(2)   #每次循环之后 添加停留时间  增加容错率
        if random.sample([0,1],1) == 1:     #这条判断是随机表示跳转
            num = num + 180  
        else:
            num = abs(num - 180)
        #num = abs(num + int(random.sample([180,-180],1)))   #这种写法更吊  但是  出错  有时间看看 修改一下
        driver.execute_script("window.scrollBy(0,%s)" % num,"") #最后了  开始 跳转  就酱



#百度搜索开始搜索方法
def baidustart(kew):
    global driver , kewword , baiduTitle #引入全局变量
    #driver = webdriver.Firefox()#这句话  测试完 之后 要 删除的
    setHttpsProxy(bc_ip , bc_proxy)#设置浏览器的代理
    kewword = kew
    time.sleep(5)
    driver.get("https://www.baidu.com/s?wd="+kewword)#开始搜索关键字
    driver.maximize_window()#浏览器最大化(这个 可选)
    assert baiduTitle in driver.title#确定页面是百度搜索页面


#这个办法主要是 放一些 排除 的网站,然后  其他 的网站   都要 点击
def noClick():
    driver.execute_script("$('a:contains(315jiage.cn)').parent().parent().remove()","") #排除315价格网
    driver.execute_script("$('h3:contains(九制黄精饮什么牌子的是真药?另外一盒多少钱?_百度知道)').parent().remove()","")#一个百度知道 


#这个方法主要实现的是跳转到百度下一页 的页面.时间 的话   可以 根据 电脑 适当 的调节
def baiduNextPage():
    global baiduTitle , driver
    time.sleep(5)#等待页面载入
    assert baiduTitle in driver.title#确定页面是百度搜索页面
    driver.implicitly_wait(10)#隐试等待
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")#滚动到最下边.没什么卵用
    driver.find_element_by_link_text("下一页>").click()

#提供随机数  直接返回布尔值  默认为70%
def suiji(sum = 7):
    if int(random.uniform(0,10))<sum:
        return True
    else:
        return False

#下边是两套规则
#规则1  除了过滤器其他的 都点
def type1():
    time.sleep(5) #时间停留5秒 增加系统容错率
    i = 0
    while i<=baidupagenumber1:#这是翻页的循环
        i = i + 1
        noClick()#过滤掉不要的链接
        content_list_num = driver.find_elements_by_tag_name("h3")
        print("打印出  总共  有几个元素:%s"%len(content_list_num))
        for x in content_list_num:
            if suiji():
                print("随机数打印到了")
                try:
                    x.find_element_by_tag_name("a").click()
                    time.sleep(5)
                    driver.switch_to_window(driver.window_handles[-1])
                    pageReader()
                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])
                    time.sleep(5)
                except:
                    print("错误一次")
            else:
                print("随机数没有打印到")
        baiduNextPage()
        print("结束.开始第二页")


#规则2  点击特定的页面   其他的不点
def type2(link):
    time.sleep(5) #时间停留5秒 增加系统容错率
    i = 0
    while i<=baidupagenumber2:#这是翻页的循环
        i= i + 1
        try:
            driver.find_element_by_partial_link_text(link).click()
            time.sleep(5)
            driver.switch_to_window(driver.window_handles[-1])
            pageReader()
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            time.sleep(5)
            print("找到链接,并且浏览成功")
        except:
            print("没找到")
        baiduNextPage()
    print("结束.离开")

def readFile():
    global driver #引入全局变量
    with open('date.csv', "rt" , encoding="utf8") as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            #在这里 打开浏览器然后 分开浏览
            baidustart(row[1])
            if row[0]=='1' and suiji(8):
                type2(row[2])
            elif suiji(8):
                type1()
            else:
                print("运气不好这一次没有被随机到哎")
            driver.close()#关闭网页
#主程序
def main():
    global bc_proxy , bc_ip
    while True:
        #分步走开始  :)
        #查找可用代理
        while True:
            if tryproxy():
                break
        #开始设置  这里一般的话 不会出错   直接写了
        # if setHttpsProxy(bc_ip , bc_proxy):
        #     print("设置成功")
        # else:
        #     print("卧槽这么简单 的还会 出错")
        #读取配置文件获取
        readFile()


if __name__ == '__main__':
    main()