#这是一个模拟百度点击的程序就酱

#-*- coding : utf-8 -*-

#导入包
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time #导入时间包
import random #导入随机数包
import string #导入string包
import urllib
import binascii


#这是全局变量
kewword = ""

baiduTitle = kewword + "_百度搜索"

driver = ""#= webdriver.Firefox()#确定浏览器

profile = webdriver.FirefoxProfile()#设置浏览器基本设置



all_use_ip = 0
can_use_ip = 0


    #程序部分
"""
这部分是 代理 部分
"""


#设置火狐浏览器的代理的办法,非常好用.得区分一下是不是https的链接
def setHttpsProxy(ip,port):#参数  ip地址   端口  类型   真为https 假为http
    global driver , profile#全局变量
    profile.set_preference('network.proxy.type', 1)#设置浏览器上完方式为手动
    if 1==1:
        profile.set_preference('network.proxy.ssl', ip)
        profile.set_preference('network.proxy.ssl_port', port)
    else:
        profile.set_preference('network.proxy.http', ip)
        profile.set_preference('network.proxy.http_port', port)
    profile.update_preferences()
    driver = webdriver.Firefox(profile)
    man_page_visit()#开始访问





def tryproxy():
    global all_use_ip , can_use_ip
    while True:
        all_use_ip = all_use_ip + 1 
        data = ''
        with urllib.request.urlopen('http://qsrdk.daili666api.com/ip/?tid=556258590050521&num=1&category=2&protocol=https&foreign=none&filter=on') as f:
            data = f.read().decode()
        proxy_handler = urllib.request.ProxyHandler({'https': data})
        proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
        try:
            wocao = opener.open('https://www.zhihu.com/')
            print("链接正确")
            if wocao.status == 200:
                can_use_ip = can_use_ip + 1
                datalist = data.split(":")
                #print(datalist[0]+"+++++++++++++"+datalist[1])
                setHttpsProxy(datalist[0],datalist[1])
            else:
                pass
        except:
            time.sleep(5)
            print("链接出错,休息5个时间")
        

        print("总共检测ip为%s"% all_use_ip)
        print("可用ip为%s"% can_use_ip)


"""
这一部分  是 浏览部分
"""


#这个方法主要是页面移动停留的办法
def seePageHead():
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


#这个方法主要实现的是跳转到百度下一页 的页面.时间 的话   可以 根据 电脑 适当 的调节
def baiduNextPage():
    global baiduTitle , driver
    time.sleep(5)#等待页面载入
    assert baiduTitle in driver.title#确定页面是百度搜索页面
    driver.implicitly_wait(10)#隐试等待
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")#滚动到最下边.没什么卵用
    driver.find_element_by_link_text("下一页>").click()


#同上这个是上一页
def baiduUpPage():
    global baiduTitle , driver
    time.sleep(5)#等待页面载入
    assert baiduTitle in driver.title#确定页面是百度搜索页面
    driver.implicitly_wait(10)#隐试等待
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")#滚动到最下边.没什么卵用
    driver.find_element_by_link_text("<上一页").click()


#百度搜索开始搜索方法
def baidustart(kew):
    global driver , kewword #引入全局变量
    kewword = kew
    time.sleep(5)
    driver.get("https://www.baidu.com/s?wd="+kewword)#开始搜索关键字
    driver.maximize_window()#浏览器最大化(这个 可选)
    assert baiduTitle in driver.title#确定页面是百度搜索页面



#这个办法主要是 放一些 排除 的网站,然后  其他 的网站   都要 点击
def noClick():
    driver.execute_script("$('a:contains(315jiage.cn)').parent().parent().remove()","") #排除315价格网


#单页面的浏览功能
def baidulist():
    time.sleep(5) #时间停留5秒 增加系统容错率
    content_list_num = driver.find_elements_by_tag_name("h3")
    print("打印出  总共  有几个元素:%s"%len(content_list_num))
    for x in content_list_num:
        try:
            x.find_element_by_tag_name("a").click()
            time.sleep(5)
            driver.switch_to_window(driver.window_handles[-1])
            seePageHead()
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            time.sleep(5)
        except:
            print("wrong")
    print("it is over")


#这个办法是总 的控制 页面进行浏览 的  主要有  分页  浏览 和 页面 浏览  
#关键词   搜索关键词   翻页数量
def man_page_visit( times = 3):
    for x in ["九制黄精饮价格","富硒六味地黄丸价格","九制黄精饮"]:
        print(x)
        baidustart(x)#开始浏览关键词
        count = 0
        while (count < times):
            time.sleep(5)#休息时间增加容错
            noClick()
            baidulist()
            baiduNextPage()
            count = count + 1

    driver.close()#关闭网页




tryproxy()